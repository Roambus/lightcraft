# LightCraft 汉化（网页版默认简体中文 + 术语对齐 Adobe 官方）

这个目录是 **本站 fork** 的汉化改动，针对 LightCraft 的**网页构建**与 `zh-hans` 目录。
上游自带简体中文（`crates/ui-egui/locales/zh-hans.json`），但：

1. **网页版的「自动」语言靠浏览器**。`apps/lightcraft-web/src/web.rs` 的
   `install_browser_language()` 取 `navigator.languages` 里第一个它认识的语言。本机浏览器
   语言是英文时打开就是英文 —— 中文用户要先自己进设置切一次。
2. **几个模块/面板名与 Lightroom Classic 中文版不一致**，用户对着教程找不到：

   | 英文 | 上游 | Lightroom Classic 中文 |
   | --- | --- | --- |
   | Develop | 编辑 | 修改照片 |
   | Filmstrip | 胶片窗格 | 胶片显示窗格 |
   | Keyword | 关键字 | 关键词 |
   | Slideshow | 幻灯片播放 | 幻灯片放映 |
   | Exposure | 曝光 | 曝光度 |

## 这个目录里有什么

| 文件 | 用途 |
| --- | --- |
| `fixes/fix-lightcraft.tsv` | 术语修正（`English<TAB>原译文<TAB>新译文`），键与 `zh-hans.json` 逐字节一致 |
| `glossary.tsv` | 对照表：English / 上游译文 / Adobe 官方中文 / 建议 / 等级 / 依据 URL / 字节差 |
| `report.md` | 审校方法与依据（含未核实项，已标注） |
| `craft_catalog_patch.py` | 把修正等长写进已编译 wasm（发布包）的工具 |

源码目录的修正已经直接提交在 `crates/ui-egui/locales/zh-hans.json`（本分支的改动之一），
`fixes/` 与词表是给「改发布包 / 上游复用」准备的。

## 默认简体中文（网页版）

上游的「自动」不是读存储，而是读 `navigator.languages`。所以要让首次打开就是中文，
在页面启动应用**之前**改写它即可（`index.html` 里的同步脚本）：

```js
var tags = ['zh-CN', 'zh-Hans-CN', 'zh'];
Object.defineProperty(navigator, 'languages', { configurable: true, get: () => tags });
Object.defineProperty(navigator, 'language', { configurable: true, get: () => tags[0] });
```

用户之后在「设置 › 常规 › 语言」里选的语言会存进浏览器本地图库的 `ui.json`，优先级高于
这个默认值，不会被反复覆盖。注意不要写死到 `ui.json` 里：它属于用户的图库，且 LightCraft
同一时间只允许一个标签页持有图库。

## 改已发布 wasm（可选路径）

发布包里的 `lightcraft_web_bg.wasm` 把目录按 JSON 嵌在 data 段里。**直接改长度会让后面所有
`(ptr, len)` 错位**，所以工具做的是等长替换：紧凑序列化后在收尾 `}` 前补空格（JSON 空白不参与
语义），文件大小与偏移全不变。

```sh
python3 hanhua/craft_catalog_patch.py check --app lr --wasm lightcraft_web_bg.wasm \
    --fixes hanhua/fixes/fix-lightcraft.tsv
python3 hanhua/craft_catalog_patch.py apply --app lr --wasm lightcraft_web_bg.wasm \
    --fixes hanhua/fixes/fix-lightcraft.tsv
gzip -9 -k -f lightcraft_web_bg.wasm     # 站点用 gzip_static 时
```

改完用 `node -e 'WebAssembly.compile(fs.readFileSync("lightcraft_web_bg.wasm"))'` 自检。

## 中文字形

上游已把 **Noto Sans CJK SC** 作为独立文件 `lightcraft_zh_hans.otf` 随站点分发，页面
`fetch` 后传给 `start(font)`；SIL OFL 1.1，许可证文件 `OFL-noto-sans-cjk-sc.txt` 在包内。
不需要额外处理。

## 许可证与归属

LightCraft 是 MIT OR Apache-2.0；本目录改动同样是 MIT OR Apache-2.0。
译文为原创文本，对照的是 Adobe 公开帮助文档里的中文术语，未使用任何商业产品的本地化资源。
