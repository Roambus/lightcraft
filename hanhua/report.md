# Adobe 中文术语审校报告（PhotoCraft / LightCraft）

**审校对象**：`i18n/photocraft.tsv`（2630 行）、`i18n/common.tsv`（1286 行）、
`storytold/lightcraft` 的 `crates/ui-egui/locales/zh-hans.json`（2455 条键）  
**基准**：Adobe 官方简体中文帮助中心 helpx.adobe.com/cn（Photoshop 桌面版 + Lightroom Classic）  
**产出**：`glossary.tsv`、`fix-photocraft.tsv`、`fix-common.tsv`、`fix-lightcraft.tsv`、`apply_fixes.py`、本报告

---

## 1. 方法

### 1.1 取数

两个 TSV 直接读（TAB 三列，行首 `#` 为注释）。LightCraft 的 JSON 走 GitHub API：
`raw.githubusercontent.com` 被墙，改用 `api.github.com/repos/storytold/lightcraft/contents/...`
取 base64 解码，一次成功，2455 条键。

### 1.2 建立 Adobe 官方语料

不凭印象写「官方译法」。做法是把 Adobe 帮助站简体中文页抓下来、剥掉导航壳、只留正文，
建成可比对语料，再逐词回查。共抓取 **59 个 `/cn/` 简体页面**（另有 2 个 `/tw/` 繁体页仅作旁证），涵盖 Photoshop 桌面版各功能页、
混合模式页、工具概述页、滤镜效果参考，以及 Lightroom Classic「修改照片」模块系列页；
最终 **43 个页面**成为词条的引用依据。

### 1.3 核实规则（关系到本报告可信度）

每一条「Adobe 官方中文」必须在**它所引用的那一个页面正文里逐字出现**，否则不采信。
脚本机械校验：160 行词条**全部通过，0 条未核实**；`delta_bytes` 也逐行用 UTF-8 字节数复算过。
所以任何一个 A/B 级条目，点开 `source_url` 都能自己看到那个中文词。

### 1.4 没能核实、已明确标注的部分

下面这些**没有**写进 `glossary.tsv` 和 fix 文件（宁缺勿造）：

- **Desaturate**（去饱和 / 去色）：上游 common.tsv 作「去饱和」，photocraft 作「去色」。Photoshop「图像 > 调整 > 去色」命令名应为「去色」，但本次抓取的页面里没有出现该命令本身（只出现「去边」语境下的「去色」二字），无法给出可核实链接，故标 unverified、不写入 fix。
- **Diffuse Glow**（扩散亮光）：上游 common.tsv 作「扩散亮光」。Photoshop 扭曲滤镜官方名应为「扩散亮光」，但本次语料里「扩散亮光」零命中（只有修复画笔的「扩散」等无关语境），无法核实，标 unverified。
- **HDR Toning / HDR 色调**（—）：「HDR 色调」在本次语料中零命中，未能核实官方写法。
- **Equalize**（色彩均化）：已在词条表中按「色彩均化」处理并核实；此处仅说明：旧译「色调均化」在语料中零命中，进一步佐证其非官方名。
- **Lock transparent pixels 等锁定项**（—）：「锁定透明像素/锁定图像像素/锁定位置/锁定全部」在语料中零命中，未能核实。
- **Flatten Image**（拼合图像）：「拼合图像」在语料中零命中（只有「拼合曲线」），未能核实。
- **Camera Raw 滤镜**（—）：「Camera Raw 滤镜」在已抓取页面中零命中，未能核实。
- **LightCraft Screen/Overlay/Darken**（屏幕 / 叠加显示 / 压暗）：疑似混合模式与 Photoshop 官方（滤色/叠加/变暗）不符，但无法确认这些键在 LightCraft 中就是混合模式（Screen 也可能指「屏幕」），证据不足，标 unverified。

### 1.5 其他说明

- **Adobe 帮助站是网页文档，不是软件资源文件。** 个别菜单字串可能与安装包有细微出入。最典型是 Lightroom 的
  Dehaze：同一官方站点里「去朦胧」（基本面板段落）与「去除薄雾」（局部调整段落）并存——**官方自己就不统一**。
  本报告按面板语境取「去朦胧」，并在词条说明里注明这一冲突。
- **繁体（`/tw/`）页面只作旁证。** LrC 部分 `/cn/` 路径会回退成英文，`/tw/` 能拿到繁体；但繁体用词
  （「色版」「選取範圍」）与大陆简体不同，未直接采信，只用于确认概念对应。
- **没有安装 Photoshop / Lightroom，未做截图级核对。** 全部结论来自官方文档文字。

## 2. 统计

| 指标 | 数值 |
|---|---|
| 覆盖英文词条（去重） | **138** 个（要求 ≥120 ✅） |
| 词条行数（同一英文在多文件/多 context 各占一行） | 160 行 |
| 引用 Adobe 官方页面 | 43 个（全部 HTTP 200，逐一验活） |
| 无法核实、已标注 unverified | 8 组（见 1.4，未写入词条表） |

分级（**逐行**判定：一行本身已与 Adobe 一致就记 C，不替别的行背锅）：

| 等级 | 含义 | **需改**行数 | **需改**去重词条 | 该级全部词条 |
|---|---|---|---|---|
| A | 意思错 / 会误解 | 31 | 30 | 30 |
| B | 用词不同但可懂 | 16 | 11 | 11 |
| C | 可接受差异（多为已一致） | 1 | 1 | 97 |

**一致率**

| 口径 | 计算 | 结果 |
|---|---|---|
| 按词条 | 138 个词条中 96 个在所有出现位置都已与 Adobe 一致 | **69.6%** |
| 按行 | 160 行中 112 行已一致 | 70.0% |
| 需改动 | **42 个词条 / 48 行** | — |

需改动分布：`photocraft.tsv` 20 行、`common.tsv` 23 行、`lightcraft.json` 5 行。

需改行数多于词条数，是因为同一个英文词在两个文件里各错一次（如 `Channels`：common 作「声道」、
photocraft 作「通道」），或同一文件里两种译法并存（如 `Masking`：「蒙版」与「蒙版保护」）。

## 2.1 等长替换用：delta_bytes 分布

`delta_bytes` = 建议译文 UTF-8 字节数 − 上游译文字节数（第 7 列，已逐行复算）。

| delta_bytes | 行数 | 含义 |
|---|---|---|
| -6 | 3 | 更短 |
| -3 | 2 | 更短 |
| +0 | 25 | 等长，可直接原地替换 |
| +3 | 12 | 更长 |
| +6 | 5 | 更长 |
| +9 | 1 | 更长 |

**18 行会比原文长**，最长 +9 字节；其余 30 行等长或更短。最长的几条：

| English | 上游 | 建议 | delta | 能否压短 |
|---|---|---|---|---|
| High Pass | 高通 | 高反差保留 | +9 | 不能。官方就是「高反差保留」，「高通」是信号处理术语。 |
| Develop | 编辑 | 修改照片 | +6 | 不能。官方模块名就是「修改照片」。 |
| Blacks | 黑色 | 黑色色阶 | +6 | 不能。官方滑块名就是「黑色色阶」。 |
| Whites | 白色 | 白色色阶 | +6 | 不能。官方滑块名就是「白色色阶」。 |
| Group | 组 | 图层组 | +6 | 不能。官方叫「图层组」。 |
| Filmstrip | 胶片窗格 | 胶片显示窗格 | +6 | 可考虑「胶片窗格」（-3），但官方原文是「胶片显示窗格」。 |
## 3. A 级：意思错、会误解（逐条）

只列**真正需要改动**的条目。`依据` 链接点开，页面正文里就能看到该中文用词。

### A1. Channels — 「声道」→「通道」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **通道** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/hdr-and-channel-manipulation/channels-in-photoshop.html |

上游 common.tsv 译「声道」——这是音频术语，Photoshop 的「通道」面板与它完全无关；而同一项目的 photocraft.tsv 又译作「通道」，两个文件互相矛盾。

### A2. Channel — 「色版」→「通道」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **通道** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/hdr-and-channel-manipulation/channels-in-photoshop.html |

上游 common.tsv 译「色版」（台湾用语）；大陆官方为「通道」，且与 Channels 的译法在同一个文件里打架。

### A3. Clipping Mask — 「剪切蒙版」→「剪贴蒙版」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **剪贴蒙版** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/create-masks/layer-masks/create-and-manage-clipping-masks.html |

官方术语为「剪贴蒙版」，Adobe 帮助页标题即《创建和管理剪贴蒙版》。上游「剪切蒙版」既与菜单不符，又容易被误解为「剪切」命令（Cut）。

### A4. Dehaze — 「去雾」→「去朦胧」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv` |
| Adobe 官方 | **去朦胧** |
| delta_bytes | +3 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html |

LrC 基本面板该滑块官方中文为「去朦胧」（Camera Raw/局部调整中同一功能作「去除薄雾」）。上游「去雾」两种都不是，用户对照 Adobe 界面时找不到。

### A5. Color Grading — 「色彩分级」→「颜色分级」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv` |
| Adobe 官方 | **颜色分级** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html |

LrC 的 Color Grading 面板官方中文是「颜色分级」。上游译「色彩分级」，而同一项目里 Color Mixer 又译「颜色混合器」，Color 的译法前后不一。

### A6. Develop — 「编辑」→「修改照片」

| 项 | 内容 |
|---|---|
| 上游位置 | `lightcraft.json` |
| Adobe 官方 | **修改照片** |
| delta_bytes | +6 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/develop-module-options.html |

Lightroom Classic 的 Develop 模块官方中文是「修改照片」模块（如「修改照片模块选项」帮助页）。上游译「编辑」，用户按 Adobe 教程找不到对应模块。

### A7. Library — 「库」→「图库」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **图库** |
| delta_bytes | +3 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html |

LrC 的 Library 模块官方中文是「图库」（「图库模块」「图库视图选项」）。上游 common.tsv 译「库」，与 Adobe 界面不符。

### A8. Hard Mix — 「硬混合」→「实色混合」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **实色混合** |
| delta_bytes | +3 |
| 依据 | https://helpx.adobe.com/cn/photoshop/using/blending-modes.html |

混合模式 Hard Mix 官方中文为「实色混合」。上游 photocraft 正确，但 common.tsv 译「硬混合」——同一产品两个译名，用户会以为是两种模式。

### A9. Divide — 「分割」→「划分」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **划分** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/using/blending-modes.html |

Adobe 混合模式列表里 Divide 官方中文是「划分」。上游 common.tsv 译「分割」，在 Photoshop 语境里「分割」指拆分通道（Split Channels），会造成误操作。

### A10. Luminosity — 「亮度」→「明度」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **明度** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/using/blending-modes.html |

混合模式 HSL 组的 Luminosity 官方中文是「明度」（「用基色的色相和饱和度以及混合色的明亮度创建结果色」）。上游 common.tsv 译「亮度」，与 Lightness/Brightness 混淆。

### A11. Luminance — 「亮度」→「明亮度」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **明亮度** |
| delta_bytes | +3 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html |

LrC 的 Luminance 官方作「明亮度」（颜色混合器的 L 滑块、明亮度范围蒙版）。上游 common.tsv 译「亮度」，与 Brightness 撞车，HSL 三要素会读错。

### A12. Blacks — 「黑色」→「黑色色阶」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **黑色色阶** |
| delta_bytes | +6 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html |

LrC 基本面板 Blacks 官方中文是「黑色色阶」。上游 common.tsv 只写「黑色」，在面板里会被理解成纯黑颜色而非色阶端点。

### A13. Whites — 「白色」→「白色色阶」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **白色色阶** |
| delta_bytes | +6 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html |

同上：官方为「白色色阶」，上游 common.tsv 的「白色」无法表达「色阶端点」这一含义。

### A14. Anti-alias — 「抗锯齿」→「消除锯齿」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv` |
| Adobe 官方 | **消除锯齿** |
| delta_bytes | +3 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/make-selections/refine-modify-selections/select-pixels-using-anti-aliasing.html |

Adobe 帮助页标题即《使用消除锯齿功能选择像素》，复选框文字为「消除锯齿」。上游 photocraft 用「抗锯齿」——那是游戏/3D 渲染圈的说法。

### A15. Equalize — 「色调均化」→「色彩均化」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv` |
| Adobe 官方 | **色彩均化** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/color-corrections/equalize-brightness-values-in-an-image.html |

该命令（图像 > 调整 > 色彩均化）官方中文是「色彩均化」，帮助页标题《均化图像中的亮度值》。上游「色调均化」在菜单里搜不到。

### A16. Tint — 「色偏」→「色调」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv`（context=`cameraRaw`） |
| Adobe 官方 | **色调** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html |

LrC 基本面板 Tint 官方是「色调」（绿-洋红补偿，与色温配对）。上游 photocraft 的 cameraRaw 上下文译「色偏」，那是另一个概念（color cast）。

### A17. Masking — 「蒙版保护」→「蒙版」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv`（context=`cameraRaw`） |
| Adobe 官方 | **蒙版** |
| delta_bytes | -6 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/retouch-photos.html |

LrC「细节」面板锐化区的 Masking 官方滑块名就是「蒙版」（「控制边缘蒙版……设置为 100 时锐化主要限制在饱和度最高的边缘」）。上游译「蒙版保护」添加了原文没有的含义。

### A18. Selection — 「所选内容」→「选区」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **选区** |
| delta_bytes | -6 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |

Photoshop 官方一律用「选区」（「取消选区」Ctrl+D、「建立选区」）。上游 common.tsv 译「所选内容」，是英文直译，且与 photocraft 的「选区」不一致。

### A19. Behind — 「后面」→「背后」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv` |
| Adobe 官方 | **背后** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/using/blending-modes.html |

混合模式 Behind 官方中文是「背后」（「仅在图层的透明部分编辑或绘画」）。上游译「后面」，非官方名。

### A20. Median — 「中位数」→「中间值」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **中间值** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/blur-sharpen-filters/filter-effects-reference.html |

PhotonShop 的 Median 滤镜官方中文是「中间值」（「中间值 混合选区内像素的亮度以减少噪声」）。上游「中位数」是统计学译法，菜单里对不上。

### A21. Maximum — 「最高」→「最大值」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **最大值** |
| delta_bytes | +3 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/blur-sharpen-filters/filter-effects-reference.html |

「最大值」滤镜官方中文为「最大值」（「最大值 扩展白色区域并收缩黑色区域，可用于修改遮罩」）。common.tsv 译「最高」，同一项目 photocraft 又译「最大值」，自相矛盾。

### A22. Reduce Noise — 「降低噪声」→「减少杂色」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **减少杂色** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/develop-module-options.html |

官方命令名是「减少杂色」（滤镜 > 杂色 > 减少杂色）。上游「降低噪声」不是菜单用词。

### A23. Unsharp Mask — 「Unsharp Mask」→「钝化蒙版」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv` |
| Adobe 官方 | **钝化蒙版** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/smart-filters/sharpening-overview.html |

USM 滤镜官方中文是「钝化蒙版」。上游 photocraft 竟是未翻译的「Unsharp Mask」，common 的「反锐化遮罩」也非官方名。

### A24. Unsharp Mask — 「反锐化遮罩」→「钝化蒙版」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **钝化蒙版** |
| delta_bytes | -3 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/smart-filters/sharpening-overview.html |

USM 滤镜官方中文是「钝化蒙版」。上游 photocraft 竟是未翻译的「Unsharp Mask」，common 的「反锐化遮罩」也非官方名。

### A25. Pointillize — 「点彩」→「点状化」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **点状化** |
| delta_bytes | +3 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/blur-sharpen-filters/filter-effects-reference.html |

像素化滤镜 Pointillize 官方中文是「点状化」。上游「点彩」是绘画流派译名，菜单里搜不到。

### A26. Keyword — 「关键字」→「关键词」

| 项 | 内容 |
|---|---|
| 上游位置 | `lightcraft.json` |
| Adobe 官方 | **关键词** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/organize-photos-in-lightroom-classic/keywords.html |

Lightroom 官方一律用「关键词」（帮助页《在 Lightroom Classic 中如何使用关键词》）。LightCraft 译「关键字」，「字」与「词」一字之差但不符合 Adobe 用词。

### A27. Slideshow — 「幻灯片播放」→「幻灯片放映」

| 项 | 内容 |
|---|---|
| 上游位置 | `lightcraft.json` |
| Adobe 官方 | **幻灯片放映** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-presets.html |

LrC 模块名官方是「幻灯片放映」模块。LightCraft 译「幻灯片播放」，把模块名译成了动作。

### A28. Skew — 「倾斜」→「斜切」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **斜切** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/transform-images-shapes-and-paths.html |

Photoshop「变换」子菜单里 Skew 官方中文是「斜切」（官方原文：「缩放、旋转、斜切、扭曲、透视和变形」）。上游 common.tsv 译「倾斜」，与「透视」「变形」并列时指代不清。

### A29. Content-Aware Scale — 「内容识别缩放」→「内容识别比例」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv` |
| Adobe 官方 | **内容识别比例** |
| delta_bytes | +0 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/transform-images-shapes-and-paths.html |

官方命令名是「内容识别比例」。上游 photocraft 译「内容识别缩放」——注意「缩放」是 Scale（自由变换里的普通缩放），加在「内容识别」后面会与「内容识别填充」的命名规律混淆。

### A30. Blur Gallery — 「模糊库」→「模糊画廊」

| 项 | 内容 |
|---|---|
| 上游位置 | `photocraft.tsv` |
| Adobe 官方 | **模糊画廊** |
| delta_bytes | +3 |
| 依据 | https://helpx.adobe.com/cn/photoshop/using/blur-gallery.html |

官方菜单名是「模糊画廊」（「使用模糊画廊」）。上游 photocraft 译「模糊库」，少一个字但与菜单不符。

### A31. High Pass — 「高通」→「高反差保留」

| 项 | 内容 |
|---|---|
| 上游位置 | `common.tsv` |
| Adobe 官方 | **高反差保留** |
| delta_bytes | +9 |
| 依据 | https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/blur-sharpen-filters/filter-effects-reference.html |

滤镜 High Pass 官方中文是「高反差保留」（「高反差保留 在发生明显颜色过渡的指定半径内保留边缘细节」）。上游 common.tsv 译「高通」——那是信号处理/音频滤波器术语。

## 4. B 级：用词不同但可懂（逐条）

**B1. Group**（`photocraft.tsv`）：「组」→「图层组」  
Photoshop 把图层容器叫「图层组」，把「编组」留给命令/动作。上游 photocraft 用「组」、common.tsv 用「编组」，与 Adobe 菜单不对应。  
delta=+6　依据：https://helpx.adobe.com/cn/photoshop/desktop/create-masks/layer-masks/create-and-manage-clipping-masks.html

**B2. Group**（`common.tsv`）：「编组」→「图层组」  
Photoshop 把图层容器叫「图层组」，把「编组」留给命令/动作。上游 photocraft 用「组」、common.tsv 用「编组」，与 Adobe 菜单不对应。  
delta=+3　依据：https://helpx.adobe.com/cn/photoshop/desktop/create-masks/layer-masks/create-and-manage-clipping-masks.html

**B3. Vibrance**（`common.tsv`）：「自然饱和度」→「鲜艳度」  
LrC 基本面板 Vibrance 官方是「鲜艳度」。注意 Photoshop 的 Vibrance 调整图层叫「自然饱和度」——要按产品区分；上游未区分，LrC 界面里应作「鲜艳度」。  
delta=-6　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html

**B4. Darks**（`photocraft.tsv`）：「暗部」→「阴影」  
上游 photocraft 的 cameraRaw 上下文自造了「暗调」滑块，Adobe 对应控件是「阴影」。用户会以为存在名为「暗调」的滑块。  
delta=+0　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B5. Darks**（`photocraft.tsv`，context=`cameraRaw`）：「暗调」→「阴影」  
上游 photocraft 的 cameraRaw 上下文自造了「暗调」滑块，Adobe 对应控件是「阴影」。用户会以为存在名为「暗调」的滑块。  
delta=+0　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B6. Lights**（`photocraft.tsv`）：「亮部」→「高光」  
同上：上游自造「亮调」，Adobe 对应控件是「高光」（Highlights）。  
delta=+0　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B7. Lights**（`photocraft.tsv`，context=`cameraRaw`）：「亮调」→「高光」  
同上：上游自造「亮调」，Adobe 对应控件是「高光」（Highlights）。  
delta=+0　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B8. Refine Edge**（`photocraft.tsv`）：「调整边缘」→「选择并遮住」  
旧版 Refine Edge 命令在 CC 之后官方改为「选择并遮住」（Select and Mask）工作区。上游沿用旧名，老用户能懂，新用户按新菜单找不到。  
delta=+3　依据：https://helpx.adobe.com/cn/photoshop/using/blur-gallery.html

**B9. Pressure**（`photocraft.tsv`）：「压感」→「压力」  
液化/画笔的 Pressure 官方中文是「压力」（「在液化面板中调整画笔大小、压力和密度」）。上游「压感」是输入设备圈的俗称。  
delta=+0　依据：https://helpx.adobe.com/cn/photoshop/using/liquify-filter.html

**B10. Density**（`photocraft.tsv`）：「浓度」→「密度」  
调整画笔的 Density 官方中文是「密度」（「密度：控制描边中的透明度程度」）。上游译「浓度」，可懂但不同。  
delta=+0　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B11. Amount**（`photocraft.tsv`，context=`cameraRaw`）：「强度」→「数量」  
LrC 细节面板的 Amount 官方是「数量」（锐化区也写「锐化量」）。上游 photocraft 的 cameraRaw.Amount 译「强度」，与「预设强度」等混淆。  
delta=+0　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B12. Exposure**（`photocraft.tsv`，context=`cameraData`）：「曝光时间」→「曝光度」  
LrC 基本面板滑块与 Photoshop 曝光度调整图层，官方都作「曝光度」。上游「曝光」少了「度」，可懂但不是界面用词。  
delta=-3　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B13. Exposure**（`common.tsv`）：「曝光」→「曝光度」  
LrC 基本面板滑块与 Photoshop 曝光度调整图层，官方都作「曝光度」。上游「曝光」少了「度」，可懂但不是界面用词。  
delta=+3　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B14. Filmstrip**（`lightcraft.json`）：「胶片窗格」→「胶片显示窗格」  
LrC 官方叫「胶片显示窗格」。LightCraft 译「胶片窗格」，少了「显示」二字，可懂。  
delta=+6　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B15. Exposure**（`lightcraft.json`）：「曝光」→「曝光度」  
LrC 基本面板滑块官方是「曝光度」。LightCraft 译「曝光」，可读但与 Adobe 界面不一致。  
delta=+3　依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html

**B16. Photocopy**（`common.tsv`）：「复印」→「影印」  
素描滤镜 Photocopy 官方中文是「影印」（「影印 模拟图像的影印效果」）。上游「复印」可懂但不是菜单用词。  
delta=+0　依据：https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/blur-sharpen-filters/filter-effects-reference.html

## 5. C 级里唯一需要动的一行

**Reset**（`common.tsv`）：「重置」→「复位」  
LrC 官方按钮为「复位」。上游 photocraft 用「复位」、common.tsv 用「重置」，按上下文择一即可，属可接受差异。  
依据：https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html
## 6. 上游已与 Adobe 一致的词条（举例）

并不是全都错了 —— 大量基础图形术语本来就译对了。以下这些经逐条核对，**在它出现的所有位置**
都与 Adobe 官方完全相同，**建议不要动**：

- **图层与蒙版**（9）：Layer、Layers、Layer Mask、Mask、Fill Layer、Smart Object、Smart Filter、Artboard、Rasterize
- **选择与裁剪**（4）：Marquee、Lasso、Crop、Feather
- **绘画与修饰**（13）：Brush、Stroke、Fill、Gradient、Clone Stamp、Healing Brush、Spot Healing Brush、Dodge、Burn、Sponge、History、Pen、Path
- **调整命令**（14）：Levels、Curves、Hue/Saturation、Color Balance、Threshold、Gradient Map、Gaussian Blur、Invert、Posterize、Color Lookup、Selective Color、Photo Filter、Channel Mixer、Black & White
- **混合模式**（25）：Normal、Dissolve、Multiply、Screen、Darken、Lighten、Overlay、Soft Light、Hard Light、Vivid Light、Linear Light、Pin Light、Difference、Exclusion、Color Dodge、Color Burn、Linear Burn、Darker Color、Lighter Color、Hue、Saturation、Color、Clear、Merge、Flatten
- **Lightroom 面板**（18）：Contrast、Highlights、Shadows、Texture、Clarity、Grain、Sharpen、Detail、Radius、Histogram、White Balance、Temperature、Tone Curve、Sync Settings、Noise Reduction、Flow、Vignette、Color Mixer
- **界面与文件**（11）：Preset、Swatches、Export、Preferences、Image Size、Free Transform、Content-Aware Fill、Blend Mode、Opacity、Zoom、Hand

合计 **96** 个词条无需改动（上表按主题举例 94 个）。
它们同样逐条回查过官方页面，只是结论是「上游本来就对」，因此不出现在 fix 文件里。

> 注意区分：`Selection`、`Blacks`、`Whites`、`Reset`、`Channels` 这类词，
> **不是**「完全正确」——它们在 `photocraft.tsv` 里译对了，但在 `common.tsv` 里译错了（或反之）。
> 这类「一半对一半错」的条目已列在 A/B 级，**只改错的那一边**，对的那边保持不动。

## 7. 交付物与用法

| 文件 | 说明 |
|---|---|
| `glossary.tsv` | 160 行 × 7 列：`english⇥upstream_zh⇥adobe_zh⇥suggested_zh⇥grade⇥source_url⇥delta_bytes` |
| `fix-photocraft.tsv` | 20 行，只含要改的条目，格式与上游 TSV 一致 |
| `fix-common.tsv` | 23 行，同上 |
| `fix-lightcraft.tsv` | 5 行，`⇥English⇥建议中文`，第二列与 lightcraft.json 的键逐字节一致 |
| `apply_fixes.py` | 套用脚本（TSV 版），`--check` / `--write` |

```bash
cd /root/artcraft/i18n/audit
python3 apply_fixes.py --check   # 只报差异，退出码 0=无需改 1=有差异 2=出错
python3 apply_fixes.py --write   # 写回 ../photocraft.tsv 与 ../common.tsv
```

脚本特性（都实测过）：
- **幂等**：第二次 `--write` 改写 0 条、已一致 20/23 条。
- **只动第三列**：`diff` 验证 —— 除译文列外，注释、空行、列结构逐字节不变。
- **原子写入**：先写 `.tmp` 再 `replace`，中途失败不会留下半个文件。
- 按 `(context, English)` 二元组定位，所以 `cameraRaw⇥Tint` 与裸 `Tint` 能分别处理。
- 键在上游找不到会告警（`未命中 N 条`），不静默忽略。

> `fix-lightcraft.tsv` 是 JSON 目录（键→值），未提供对应 apply 脚本；
> 请在合并时按 key 精确匹配，线上构建若嵌旧版目录、某键不存在，跳过该条即可（不要模糊匹配）。

## 8. LightCraft 单独说明

`lightcraft.json` 是扁平「英文→中文」JSON，没有 TSV 的 context 机制，因此单独给 `fix-lightcraft.tsv`
（两列，第二列为键，已逐字节比对，5 个键全部命中）。核查结果：

| 英文键 | 上游 | Adobe 官方 | 结论 |
|---|---|---|---|
| Develop | 编辑 | **修改照片** | ❌ A 级，需改 |
| Keyword | 关键字 | **关键词** | ❌ A 级，需改 |
| Slideshow | 幻灯片播放 | **幻灯片放映** | ❌ A 级，需改 |
| Luminance | 明度 | **明亮度** | ❌ A 级，需改 |
| Exposure | 曝光 | **曝光度** | ⚠️ B 级 |
| Filmstrip | 胶片窗格 | **胶片显示窗格** | ⚠️ B 级 |
| Dehaze | 去朦胧 | 去朦胧 | ✅ 一致 |
| Vibrance | 鲜艳度 | 鲜艳度 | ✅ 一致 |
| Blacks / Whites | 黑色色阶 / 白色色阶 | 同左 | ✅ 一致 |
| Color Grading / Color Mixer | 颜色分级 / 颜色混合器 | 同左 | ✅ 一致 |
| Tone Curve / Grain / Vignette | 色调曲线 / 颗粒 / 暗角 | 同左 | ✅ 一致 |
| Sync Settings | 同步设置 | 同步设置 | ✅ 一致 |
| Library | 图库 | 图库 | ✅ 一致 |

**结论**：LightCraft 的 Lightroom 侧术语质量明显好于 PhotoCraft，多数滑块已贴合 LrC 官方中文；
但**模块级命名**错了两个（`Develop→编辑`、`Slideshow→幻灯片播放`），这类错误影响最大——
用户对照 Adobe 教程会找不到模块。
另外 `Darken→压暗`、`Screen→屏幕`、`Overlay→叠加显示` 疑似混合模式与 Photoshop 官方
（变暗/滤色/叠加）不符，但**无法确认这些键在此项目里就是混合模式**（`Screen` 也可能真是「屏幕」），
证据不足，**已列入 1.4 unverified，不写入 fix 文件、不计入统计**。

## 9. 结论与建议

1. **优先修 A 级 31 行**。危害最大的五条：
   - `Channels/Channel → 声道/色版`（应为**通道**）—— 音频术语混进图像软件，且 common 与 photocraft 自相矛盾；
   - `Clipping Mask → 剪切蒙版`（应为**剪贴蒙版**）—— 官方帮助页标题就是「剪贴蒙版」；
   - `Develop → 编辑`（应为**修改照片**，LightCraft）—— 整个模块名错了；
   - `Dehaze → 去雾`（应为**去朦胧**）—— 对照 Lightroom 面板找不到；
   - `High Pass → 高通`（应为**高反差保留**）—— 信号处理术语，滤镜菜单里搜不到。
2. **先解决自相矛盾**。同一个英文词在 photocraft 与 common 给了两个译法的情况，
   哪怕暂不换用词，也必须统一，否则同一套 UI 会出现两个名字。
3. **等长替换注意**：18 行会比原文长（最长 +9 字节），其余 30 行等长或更短；
   若线上做严格等长替换，优先挑 delta≤0 的先上，长的那些另做变长方案。
4. **B 级 16 行**可在版本迭代中慢慢靠拢，不必紧急。
5. **C 级唯一的 `Reset`**（photocraft「复位」vs common「重置」）本质是上下文差异，
   本次按 Adobe 的「复位」统一；若后续发现「重置」在别处更自然，保留双译也说得通。

---

## 10. 逐条来源索引

词条表每一行都有 `source_url`。全部 **43 个**引用页面如下（均已 curl 验活，HTTP 200）：

- https://helpx.adobe.com/cn/lightroom-classic/desktop/organize-photos-in-lightroom-classic/keywords.html
- https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-local-adjustments.html
- https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/apply-presets.html
- https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/color-mixer.html
- https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/develop-module-options.html
- https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html
- https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/lens-blur.html
- https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/masking.html
- https://helpx.adobe.com/cn/lightroom-classic/desktop/process-and-develop-photos/retouch-photos.html
- https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/choose-colors/work-with-the-swatches-panel.html
- https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html
- https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/color-corrections/apply-color-balance-and-photo-filter-adjustments.html
- https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/color-corrections/color-adjustment-commands.html
- https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/color-corrections/equalize-brightness-values-in-an-image.html
- https://helpx.adobe.com/cn/photoshop/desktop/adjust-color/hdr-and-channel-manipulation/channels-in-photoshop.html
- https://helpx.adobe.com/cn/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/content-aware-fills.html
- https://helpx.adobe.com/cn/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html
- https://helpx.adobe.com/cn/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-and-fill-layers-overview.html
- https://helpx.adobe.com/cn/photoshop/desktop/create-manage-layers/get-started-layers/merge-and-stamp-layers.html
- https://helpx.adobe.com/cn/photoshop/desktop/create-masks/layer-masks/create-and-manage-clipping-masks.html
- https://helpx.adobe.com/cn/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/change-the-canvas-size.html
- https://helpx.adobe.com/cn/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/transform-images-shapes-and-paths.html
- https://helpx.adobe.com/cn/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html
- https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/blur-sharpen-filters/filter-effects-reference.html
- https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/blur-sharpen-filters/overview-of-adding-blur-to-images.html
- https://helpx.adobe.com/cn/photoshop/desktop/effects-filters/smart-filters/sharpening-overview.html
- https://helpx.adobe.com/cn/photoshop/desktop/get-started/learn-the-basics/navigate-and-pan-images.html
- https://helpx.adobe.com/cn/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html
- https://helpx.adobe.com/cn/photoshop/desktop/make-selections/refine-modify-selections/select-pixels-using-anti-aliasing.html
- https://helpx.adobe.com/cn/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html
- https://helpx.adobe.com/cn/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html
- https://helpx.adobe.com/cn/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html
- https://helpx.adobe.com/cn/photoshop/using/adjustment-fill-layers.html
- https://helpx.adobe.com/cn/photoshop/using/artboards.html
- https://helpx.adobe.com/cn/photoshop/using/blending-modes.html
- https://helpx.adobe.com/cn/photoshop/using/blur-gallery.html
- https://helpx.adobe.com/cn/photoshop/using/crop-straighten-photos.html
- https://helpx.adobe.com/cn/photoshop/using/curves-adjustment.html
- https://helpx.adobe.com/cn/photoshop/using/drawing.html
- https://helpx.adobe.com/cn/photoshop/using/levels-adjustment.html
- https://helpx.adobe.com/cn/photoshop/using/liquify-filter.html
- https://helpx.adobe.com/cn/photoshop/using/masking-layers.html
- https://helpx.adobe.com/cn/photoshop/using/preferences.html

*本报告所有 Adobe 中文用词均可于所列 URL 页面正文检索到；未核实项已在 1.4 明确列出，未计入词条表。*