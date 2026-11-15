#!/usr/bin/env python3
"""在官方 web 构建的 wasm 里就地改简体中文界面目录的译文（术语对齐 Adobe 官方用词）。

为什么必须「等长」：
  PhotoCraft / LightCraft 的界面目录是编译期嵌进 wasm 的（PhotoCraft 是 craft-i18n 的
  TSV，LightCraft 是一份 JSON），运行时不做任何外部加载。wasm 的 data 段按**固定内存偏移**
  铺进去，目录之后紧跟着别的字符串——段内总字节一旦变化，后面所有 (ptr, len) 全部错位，
  模块必崩。所以这里保证**整个目录块的字节数与原来完全相等**：

  * TSV：逐行改译文会让总长变化，差额用**注释块**吸收（注释行解析时不读，可以任意增减）；
  * JSON：先紧凑序列化，再在收尾 `}` 前用空格补齐（JSON 里的空白不参与语义）。

  这样文件长度、data 段长度、所有偏移都不变，只重新 gzip。

用法：
  ./craft_catalog_patch.py extract --app ps|lr --wasm <wasm> --out-dir dir/
  ./craft_catalog_patch.py check   --app ps|lr --wasm <wasm> --fixes fixes.tsv
  ./craft_catalog_patch.py apply   --app ps|lr --wasm <wasm> --fixes fixes.tsv [--out <wasm>]

fixes.tsv 三列：english<TAB>old_zh<TAB>new_zh（行首 # 为注释）。
english 必须与嵌入目录的英文键**逐字节一致**（LightCraft 的键含前导空格与 `·` …），
old_zh 是嵌入目录里的现值，用来确认改的确实是那一行。
占位符 `{name}` 与结尾 `…` 会被校验：丢了就不改。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------- 定位嵌入目录

PC_COMMON = "# 简体中文 (zh-hans) interface catalog for every Crafting App.".encode()
PC_APP = "# 简体中文 (zh-hans) interface catalog for PhotoCraft.".encode()
PC_NEXT = "# 繁體中文 (zh-hant) interface catalog for every Crafting App.".encode()
LR_ANSI_MARK = "（图库默认值）".encode()


def find_pc_catalogs(wasm: bytes) -> list[tuple[int, int, str]]:
    a = wasm.find(PC_COMMON)
    b = wasm.find(PC_APP)
    if a < 0 or b < 0:
        raise SystemExit("找不到 PhotoCraft 的 zh-hans 目录（wasm 版本不对？）")
    if wasm.find(PC_COMMON, a + 1) != -1 or wasm.find(PC_APP, b + 1) != -1:
        raise SystemExit("目录在 wasm 里出现多次，等长替换不安全，停止")
    end = wasm.find(PC_NEXT, b)
    if end < 0:
        raise SystemExit("找不到 zh-hant 目录起点，无法确定 photocraft 目录结尾")
    return [(a, b, "common"), (b, end, "photocraft")]


def find_lr_catalog(wasm: bytes) -> tuple[int, int]:
    """LightCraft 每门语言一份 JSON，开头几个键一模一样；靠简体那份的值认人。

    目录可能是上游的「两空格缩进」排版，也可能是本脚本改写过的紧凑排版，
    所以不假定开头长什么样：先找到简体独有的值，再往前回溯到那一行的 `{`。
    """
    marker = wasm.find(LR_ANSI_MARK)
    if marker < 0:
        raise SystemExit("找不到 LightCraft 的 zh-hans 目录")
    # 回溯到本对象开头：`{"`（紧凑）或 `{\n`（缩进排版）里离 marker 最近的那个
    cand = max(wasm.rfind(b'{"', 0, marker), wasm.rfind(b'{\n', 0, marker))
    while cand >= 0:
        end = _json_object_end(wasm, cand)
        if end > 0:
            try:
                parsed = json.loads(wasm[cand:end].decode("utf-8"))
            except Exception:
                parsed = None
            if isinstance(parsed, dict) and any(LR_ANSI_MARK.decode() in str(v) for v in parsed.values()):
                return cand, end
        cand = max(wasm.rfind(b'{"', 0, cand), wasm.rfind(b'{\n', 0, cand))
    raise SystemExit("找不到 LightCraft 的 zh-hans 目录")


def _json_object_end(wasm: bytes, start: int) -> int:
    """从 start 的 `{` 起做括号匹配（跳过字符串与转义），返回对象结尾之后的下标；失败返回 -1。"""
    i, depth, in_str, esc = start, 0, False, False
    while i < len(wasm):
        c = wasm[i]
        if in_str:
            if esc:
                esc = False
            elif c == 0x5C:
                esc = True
            elif c == 0x22:
                in_str = False
        else:
            if c == 0x22:
                in_str = True
            elif c == 0x7B:
                depth += 1
            elif c == 0x7D:
                depth -= 1
                if depth == 0:
                    return i + 1
        i += 1
    return -1


# ---------------------------------------------------------------- TSV / JSON 文本


def split_tsv(text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """拆成 (注释头, 行列表)。注释头原样保留，用来吸收长度差。"""
    header_end = 0
    for line in text.splitlines(keepends=True):
        if line.startswith("#") or line.strip() == "":
            header_end += len(line)
        else:
            break
    header = text[:header_end]
    rows = []
    for line in text[header_end:].splitlines():
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            raise SystemExit(f"目录行不是三列：{line!r}")
        rows.append((parts[0], parts[1], parts[2]))
    return header, rows


def unescape(field: str) -> str:
    return field.replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")


def escape(field: str) -> str:
    return field.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


def render_tsv(header: str, rows: list[tuple[str, str, str]], target: int) -> bytes:
    body = "".join("\t".join((ctx, en, zh)) + "\n" for ctx, en, zh in rows).encode("utf-8")
    room = target - len(body)
    if room < 0:
        raise SystemExit(f"译文变长超出了注释块可吸收的范围（还差 {-room} 字节）")
    head = fit_header(header, room)
    out = head + body
    assert len(out) == target, (len(out), target)
    return out


def fit_header(header: str, size: int) -> bytes:
    """把注释头调整到正好 size 字节。

    做法：原样保留尽量多的注释行，剩下的字节用最后一行 `#` + 空格 + 换行补齐。
    注释内容不参与解析（解析器只跳过长行），所以空格填充是安全的；
    实在放不下就丢尾巴上的注释行，最后总会剩一行 `#…\n`（>=2 字节）。
    """
    raw = header.encode("utf-8")
    if len(raw) == size:
        return raw
    lines = header.splitlines(keepends=True)
    kept = 0
    used = 0
    for line in lines:
        n = len(line.encode("utf-8"))
        if used + n + 2 > size:      # 还要给收尾的 "#\n" 留位置
            break
        used += n
        kept += 1
    prefix = "".join(lines[:kept]).encode("utf-8")
    rest = size - used
    if rest == 0:
        tail = b""
    elif rest == 1:
        tail = b"\n"                 # 一个空行，解析时同样被跳过
    else:
        tail = b"#" + b" " * (rest - 2) + b"\n"
    out = prefix + tail
    if len(out) != size:
        raise SystemExit(f"注释头调整失败（{len(out)} != {size}）")
    return out


def render_json(catalog: dict[str, str], target: int) -> bytes:
    """紧凑序列化后用空格补齐到 target 字节；JSON 空白不参与语义。"""
    compact = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    data = compact.encode("utf-8")
    if len(data) > target:
        raise SystemExit(f"译文变长到 {len(data)} 字节，超过原目录 {target} 字节")
    pad = target - len(data)
    # 补在收尾 '}' 之前：{"a":"b"   }  —— 合法的 JSON 空白
    data = compact[:-1].encode("utf-8") + b" " * pad + b"}"
    assert len(data) == target
    return data

# ---------------------------------------------------------------- 校验


def placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{[^{}]*\}", text))


def check_pair(en: str, old: str, new: str) -> list[str]:
    problems = []
    if new.strip() == "":
        problems.append("译文为空")
    if placeholders(en) != placeholders(new):
        problems.append(f"占位符不一致 {sorted(placeholders(old))} -> {sorted(placeholders(new))}")
    if old.endswith("…") != new.endswith("…"):
        problems.append("结尾省略号 … 必须与原译一致")
    if old.startswith(" ") != new.startswith(" "):
        problems.append("前导空格必须与原译一致")
    return problems


def load_fixes(path: str) -> list[tuple[str, str, str]]:
    fixes = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                raise SystemExit(f"{path}:{n}: 需要三列 english/old/new：{line!r}")
            fixes.append((parts[0], parts[1], parts[2]))
    return fixes

# ---------------------------------------------------------------- 两个 app 的改法


def patch_photocraft(wasm: bytearray, fixes, dry: bool, only: str | None = None) -> list[str]:
    log: list[str] = []
    for start, end, kind in find_pc_catalogs(bytes(wasm)):
        if only and kind != only:
            continue
        target = end - start
        header, rows = split_tsv(bytes(wasm[start:end]).decode("utf-8"))
        by_key: dict[tuple[str, str], int] = {}
        for i, (_ctx, en, zh) in enumerate(rows):
            by_key.setdefault((unescape(en), unescape(zh)), i)
        changed = 0
        for en, old, new in fixes:
            hit = by_key.get((en, old))
            if hit is None:
                same_en = [rows[i][2] for i, r in enumerate(rows) if unescape(r[1]) == en]
                if same_en:
                    log.append(f"[{kind}] 跳过（现值是 {same_en!r}，不是 {old!r}）：{en!r}")
                continue
            problems = check_pair(en, old, new)
            if problems:
                log.append(f"[{kind}] 拒绝 {en!r}: " + "；".join(problems))
                continue
            ctx, en_field, _zh = rows[hit]
            rows[hit] = (ctx, en_field, escape(new))
            changed += 1
            log.append(f"[{kind}] {en!r}: {old} → {new}")
        if dry or changed == 0:
            continue
        wasm[start:end] = render_tsv(header, rows, target)
    return log


def patch_lightcraft(wasm: bytearray, fixes, dry: bool) -> list[str]:
    log: list[str] = []
    start, end = find_lr_catalog(bytes(wasm))
    target = end - start
    catalog = json.loads(bytes(wasm[start:end]).decode("utf-8"))
    changed = 0
    for en, old, new in fixes:
        if en not in catalog:
            continue
        if catalog[en] != old:
            log.append(f"[lightcraft] 跳过（现值 {catalog[en]!r}）：{en!r}")
            continue
        problems = check_pair(en, old, new)
        if problems:
            log.append(f"[lightcraft] 拒绝 {en!r}: " + "；".join(problems))
            continue
        catalog[en] = new
        changed += 1
        log.append(f"[lightcraft] {en!r}: {old} → {new}")
    if not dry and changed:
        wasm[start:end] = render_json(catalog, target)
    return log

# ---------------------------------------------------------------- CLI


def main() -> int:
    ap = argparse.ArgumentParser(description="就地改写嵌入 wasm 的简体中文界面目录（等长）")
    ap.add_argument("action", choices=["extract", "check", "apply"])
    ap.add_argument("--app", required=True, choices=["ps", "lr"])
    ap.add_argument("--wasm", required=True)
    ap.add_argument("--fixes")
    ap.add_argument("--out")
    ap.add_argument("--out-dir")
    ap.add_argument("--catalog", choices=["common", "photocraft"], help="PhotoCraft 有两份目录，只改其中一份")
    args = ap.parse_args()

    raw = open(args.wasm, "rb").read()
    wasm = bytearray(raw)

    if args.action == "extract":
        os.makedirs(args.out_dir, exist_ok=True)
        if args.app == "ps":
            for start, end, kind in find_pc_catalogs(raw):
                name = "zh-hans-common.tsv" if kind == "common" else "zh-hans-photocraft.tsv"
                open(os.path.join(args.out_dir, name), "wb").write(raw[start:end])
                print(f"{name}: {end - start} bytes")
        else:
            start, end = find_lr_catalog(raw)
            open(os.path.join(args.out_dir, "zh-hans.json"), "wb").write(raw[start:end])
            print(f"zh-hans.json: {end - start} bytes")
        return 0

    if not args.fixes:
        raise SystemExit(f"{args.action} 需要 --fixes")
    fixes = load_fixes(args.fixes)
    log = patch_photocraft(wasm, fixes, dry=args.action == "check", only=args.catalog) if args.app == "ps" \
        else patch_lightcraft(wasm, fixes, dry=args.action == "check")

    for line in log:
        print(line)
    applied = sum(1 for line in log if "→" in line)
    print(f"# {args.action}: 改 {applied} 条，跳过 {len(log) - applied} 条")

    if args.action == "apply":
        if len(wasm) != len(raw):
            raise SystemExit("文件长度变了，拒绝写回")
        out = args.out or args.wasm
        with open(out, "wb") as fh:
            fh.write(wasm)
        print(f"# 写出 {out}（{len(wasm)} bytes，与原文等长）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
