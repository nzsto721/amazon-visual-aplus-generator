# Amazon Visual & A+ Generator · v2

> 一套通用 AI Skill，适用于 ChatGPT、Claude、Gemini、Codex 等任意支持 System Prompt 的 AI 平台。
> 从市场调研、视觉策划、模板匹配、Style Lock、JSON 脚本到生图裁切，一套指令跑完 Amazon 副图 + A+ 全流程。

[![Platform](https://img.shields.io/badge/Platform-AI%20Skill-blue)](https://openai.com)
[![Version](https://img.shields.io/badge/Version-v2.0-green)](https://github.com/nzsto721/amazon-visual-aplus-generator)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)

---

## 目录

- [它解决什么问题](#它解决什么问题)
- [v2 新增特性](#v2-新增特性)
- [设计哲学](#设计哲学)
- [工作流总览](#工作流总览)
- [需要提供什么](#需要提供什么)
- [怎么用](#怎么用)
- [交付物](#交付物)
- [验收清单](#验收清单)
- [FAQ](#faq)
- [文件结构](#文件结构)

---

## 它解决什么问题

以前做一套 Amazon 图片，通常要经历一条很长的链路：

```
运营整理卖点 → 找竞品图片 → 写需求文档 → 设计师理解产品
→ 一版二版三版来回改 → 多站点多尺寸重复劳动
```

现在：

```
准备产品文件夹 → 启动 Skill → 确认策划方案 → 等待生成 → 得到 20 张合规图
```

---

## v2 新增特性

### 🆕 模板系统（25 种图片类型）

每种图片类型都有对应的 JSON 模板，包含 Prompt 骨架、默认参数、风格变体、类目定制提示和参考示例。

覆盖类型：主图、场景生活图、平铺图、微距细节图、海报横幅、社媒图、UGC 风格、模特展示、Before/After、包装图、信息图/A+、创意概念、尺寸规格图等。

### 🆕 Style Lock（风格锁定）

多张图任务时，先建立一份 Style Lock（色板 HEX、光线、布局逻辑、图标风格），后续每张图的 Prompt 原样带入，保证系列图风格一致。

### 🆕 Prompt 铁律（7 条）

| 铁律 | 内容 |
|---|---|
| 一 | 颜色必须用 HEX 码（不用形容词） |
| 二 | 产品占比必须数字化（填写具体百分比） |
| 三 | 必须带 `negative_prompt`（标准负面约束） |
| 四 | 认证/功效/性能表述必须有依据 |
| 五 | Prompt 结构标准化（主体→场景→光线→构图→质量→负面） |
| 六 | Style Lock 必须贯穿所有图片 |
| 七 | Amazon 主图绝不 AI 生成 |

详见 `references/prompt_guidelines.md`。

### 🆕 OpenAI 兼容 API 支持

`scripts/generate_image.py` 支持任意 OpenAI 兼容 API，不限于 OpenAI。国内大模型网关也可使用。

支持三种模式：
- **API 模式**：配置 API Key 后自动生图
- **Prompt-only 模式**：只输出 Prompt，不调用 API（复制到任意生图工具）
- **批量模式**：从 `approved_image_plan.json` 批量生成

---

## 设计哲学

> **先想清楚，再画。每张图解决一个购买顾虑。**

| AI 适合做什么 | 你必须把关什么 |
|---|---|
| 副图场景、功能图、尺寸图 | 标题、数据、认证必须有依据 |
| A+ 品牌故事、痛点场景、结构说明 | 最终文案和图片符合品牌调性 |
| 信息图排版布局 | 移动端小图能看清核心文字 |
| 风格一致性（Style Lock） | 系列图是否真的风格统一 |

**它不是 AI 设计师，而是一个懂 Amazon 转化逻辑的视觉策划助手。**

---

## 工作流总览

```
Phase 0  输入验证 + 模板匹配
    ↓
Phase 1  联网调研 + 输出策划方案 ← 你确认 ← ← ← ← ←
    ↓（确认后）
Phase 2  JSON 细化 + Style Lock + 生图 + 裁切
    ↓
交付      20 张 Amazon 合规图
```

### Phase 1 输出（等你确认，不画图）

| 模块 | 建议结构 |
|---|---|
| 主图审计 | 白底、主体占比、清晰度、是否有文字/道具 |
| 副图 ×6 | 核心利益 / 场景痛点 / 功能拆解 / 尺寸兼容 / 使用步骤 / 包装清单 |
| A+ ×7 | 品牌开场 / 痛点场景 / 核心技术 / 细节卖点 / 使用场景 / 对比说明 / 售后承诺 |
| Style Lock | 色板 HEX / 光线 / 布局 / 图标风格 |

### 确认后 Phase 2 才继续

Skill 收到"确认"后才进入 JSON 细化和生图阶段。不会在方向错误时一次性生成 20 张废图。

---

## 需要提供什么

### 必填（缺任何一项 Skill 不启动）

**① `product_info.md`**

```markdown
# 必须提供
- 产品标题（Amazon Listing Title）
- 五点卖点（5 Bullet Points）
- 产品描述（Product Description）
- 核心功能 / 主打卖点（Key Features）
- 目标人群（Target Audience）
- 使用场景（Usage Scenarios）
- 已验证的认证（Verified Certifications）

# 强烈建议提供
- 不能使用的敏感表达（Forbidden Claims）
```

> 偷懒方式：直接把当前 Amazon Listing 文案原文复制进去，Skill 会先帮你梳理提取。

**② `white_images/`** — 至少 1 张纯白底产品图（PNG/JPG）

```
white_images/
├── main-front.png    # 正面白底图（必备）
├── main-side.png     # 侧面白底图（建议）
└── main-angle.png    # 45度角白底图（建议）
```

要求：纯白背景 (RGB 255,255,255)、主体占比 ≥85%、至少 1600px 长边、无文字/Logo/道具。

### 选填（有就更好，没有也能跑）

| 文件 | 内容 | 用途 |
|---|---|---|
| `brand_assets/logo.png` | 品牌 Logo | A+ 品牌故事页 |
| `brand_assets/brand-colors.md` | 品牌主色/辅色 | 统一画面调性 |
| `requirements.md` | 特殊需求 | 指定场景、必须包含/排除的元素 |

### 最终文件夹结构

```
my-product/
├── product_info.md
├── white_images/
│   ├── main-front.png
│   └── main-side.png
├── brand_assets/        ← 选填
│   ├── logo.png
│   └── brand-colors.md
└── requirements.md       ← 选填
```

---

## 怎么用

### 1. 安装 Skill

**方式 A：Git Clone**
```bash
# 放到对应平台的 skills 目录
git clone https://github.com/nzsto721/amazon-visual-aplus-generator.git
```

**方式 B：下载 ZIP 解压**

### 2. 配置到你的 AI 平台

| 平台 | 配置方式 |
|---|---|
| **ChatGPT** | Settings → Personalization → Custom instructions → 粘贴 SKILL.md 全文 |
| **Claude** | Project → Project instructions → 粘贴 SKILL.md 全文 |
| **Codex / WorkBuddy** | 把文件夹放到 `~/.workbuddy/skills/` 目录 |
| **Gemini** | Gem → System Instructions → 粘贴 SKILL.md 全文 |

### 3. 准备产品文件夹

按「需要提供什么」一节准备好 `product_info.md` + `white_images/`。

### 4. 启动 Skill

在对话中输入（通用指令，各平台均可使用）：

```
请用 amazon-visual-aplus-generator 为以下产品策划 Amazon 副图和 A+ 内容：

产品文件夹路径：/path/to/my-product

请先只输出策划方案（Phase 1），不要生成图片，等我确认后再继续。
```

### 5. 控制流程

| 你说的话 | Skill 行为 |
|---|---|
| （无操作） | 输出策划方案，等待确认 |
| 「确认」/「approved」/「go ahead」 | 继续 Phase 2，生成 JSON + 生图 |
| 「副图 2 改成露营场景」 | 修改方案，重新输出等待确认 |
| 「整体风格不要太科技，改成家庭温暖风」 | 修改 Style Lock，重新输出 |

---

## 交付物

```
my-product/
├── approved_image_plan.json    # 完整图片计划（可复用、可检查）
├── generated/                  # 原始生成图（未裁切）
│   ├── secondary-01.png
│   ├── aplus-desktop-01.png
│   └── ...
└── final/                     # Amazon 上传尺寸（已裁切）
    ├── secondary-01.jpg       # 1200×1600
    ├── aplus-desktop-01.jpg  # 1464×600
    └── ...
```

---

## 验收清单

AI 可以把效率拉得很高，但 Amazon 图片不是发朋友圈。上传前至少检查：

- [ ] 产品外观有没有被 AI 改错？
- [ ] 图片里的英文有没有拼写错误？
- [ ] 有没有写没有证据的认证、功效、承重、环保、医疗相关表述？
- [ ] 移动端小图能不能看清核心文字？
- [ ] A+ 桌面版和移动版是不是都符合上传尺寸？
- [ ] 系列图的风格是否一致（Style Lock 有无被偏离）？
- [ ] 颜色是否和计划中 HEX 码一致？

---

## FAQ

**Q：主图可以用 AI 生成吗？**
A：不可以。主图必须用真实产品白底图。Skill 只做合规审计，不生成主图。

**Q：如果我没有设计师，也没有 API Key，能用吗？**
A：可以。Skill 支持 Prompt-only 模式，只输出 Prompt，你复制到任意生图工具即可。

**Q：这套 Skill 只适用于宠物用品吗？**
A：不是。适用于任何 Amazon 品类。只需在 `product_info.md` 中提供对应产品的信息。

**Q：Style Lock 一定要用吗？**
A：多张图任务强烈建议使用，否则系列图风格容易不一致。单张图可以不使用。

**Q：生成的图片可以直接上传 Amazon 吗？**
A：需先通过验收清单。AI 生成图可能存在产品变形、文字错误等问题，必须人工验收。

---

## 文件结构

```
amazon-visual-aplus-generator/
├── SKILL.md                          # Skill 核心定义（v2 工作流 + 约束规则）
├── README.md                         # 本文件
├── .gitignore
├── scripts/
│   ├── visual_size_helper.py         # 尺寸裁切脚本（Pillow）
│   └── generate_image.py            # 图像生成脚本（OpenAI 兼容 API）
├── references/
│   ├── amazon_image_specs.md        # Amazon 图片规范详解
│   ├── json_schema.md                # approved_image_plan.json 字段定义（v2）
│   └── prompt_guidelines.md        # Prompt 铁律（7 条规则）
└── templates/                       # 图片类型 JSON 模板（25 个）
    ├── 01-hero-image.json
    ├── 02-lifestyle-scene.json
    ├── 11-infographic.json
    ├── 13-size-spec.json
    └── ...
```

---

## 依赖

- **支持 System Prompt 的 AI 平台**（ChatGPT / Claude / Gemini / Codex / 等）
- **图像生成能力**（AI 平台自带，或配置 OpenAI 兼容 API）
- **Pillow**：`pip install Pillow`（`visual_size_helper.py` 需要）

---

## License

MIT — 可自由使用、修改、分发。

---

> 真正被改变的，不只是「图片能不能 AI 画」。
> 而是一个普通运营，也可以拥有一套接近专业视觉团队的工作流。
