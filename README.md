# Amazon Visual & A+ Generator · v2

> **一套通用 AI Skill，让不会设计的运营也能做出专业级 Amazon 副图 + A+ 内容。**
> 适用于 ChatGPT、Claude、Gemini、Codex 等任意支持 System Prompt 的 AI 平台。

[![Platform](https://img.shields.io/badge/Platform-AI%20Skill-blue)](https://openai.com)
[![Version](https://img.shields.io/badge/Version-v2.0-green)](https://github.com/nzsto721/amazon-visual-aplus-generator)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)

---

## 📖 目录

- [写给完全小白的你](#写给完全小白的你)
- [名词解释（小白必读）](#名词解释小白必读)
- [它解决什么问题](#它解决什么问题)
- [v2 新增特性](#v2-新增特性)
- [前置准备清单](#前置准备清单)
- [需要提供什么（详细版）](#需要提供什么详细版)
- [怎么用（手把手教程）](#怎么用手把手教程)
- [各平台配置详解](#各平台配置详解)
- [对话示例（你应该怎么和 AI 对话）](#对话示例你应该怎么和ai对话)
- [交付物说明](#交付物说明)
- [生成后如何使用](#生成后如何使用)
- [验收清单](#验收清单)
- [FAQ（更多问题）](#faq更多问题)
- [文件结构](#文件结构)

---

## 写给完全小白的你

如果你符合以下任何一条，这一节就是为你写的：

- 不知道什么是 "AI Skill"、"System Prompt"、"JSON"
- 没有用过 ChatGPT 的高级功能
- 不知道怎么准备产品资料
- 担心"我看不懂，用不起来"

**请放心，这个工具就是为让你用起来的。** 你只需要会三件事：

1. **准备一个文件夹**（里面放产品资料和图片）
2. **复制一段文字发给 AI**
3. **看 AI 的回复，回复"确认"或提出修改意见**

不需要写代码，不需要懂设计，不需要懂英文提示词。

---

## 名词解释（小白必读）

| 名词 | 大白话解释 |
|---|---|
| **AI Skill** | 一套"教会 AI 怎么帮你干活"的指令文件。就像给新员工一套工作手册。 |
| **System Prompt / 系统指令** | 你给 AI 的"身份设定"。告诉 AI："你现在是一个 Amazon 视觉策划专家。" |
| **JSON** | 一种数据格式，长这样：`{"name": "value"}`。AI 用它来整理图片计划，你不需要自己写，AI 会自动生成。 |
| **API Key** | 一串字母数字，用来让 AI 直接帮你生成图片。没有也没关系，AI 可以只输出提示词，你自己拿去别的工具生图。 |
| **Prompt** | 发给生图 AI 的"画图指令"。比如："一只猫在喝水的照片，白色背景。" |
| **White Background Image / 白底图** | 产品放在纯白色背景上的照片。Amazon 主图必须是这种。 |
| **副图** | Amazon 产品页面上，主图旁边的 6 张补充图片。 |
| **A+ Content** | Amazon 产品页面下方那块"品牌故事+产品详情"的区域，有图片有文字。 |
| **Style Lock / 风格锁定** | 保证一套图片风格统一的方法。比如：所有图都用同样的色板、同样的光线方向。 |

---

## 它解决什么问题

### 以前做一套 Amazon 图片，通常要经历：

```
运营整理卖点（2小时）
    ↓
找竞品图片参考（1小时）
    ↓
写设计需求文档（1小时）
    ↓
发给设计师（等待1-3天）
    ↓
设计师返稿，来回修改 3-5 轮（3-7天）
    ↓
多站点、多尺寸重复沟通（再花 2-3 天）
    ↓
总耗时：7-15 天
总沟通成本：高
```

### 现在用这个 Skill：

```
准备产品文件夹（30分钟，只需要做一次）
    ↓
启动 Skill，AI 自动调研 + 出策划方案（5分钟）
    ↓
你看方案，说"确认"或"改一下"（2分钟）
    ↓
AI 生成图片计划 + 生图（10-20分钟）
    ↓
你验收，微调（10分钟）
    ↓
总耗时：约 1 小时（第二次只需 20 分钟）
```

---

## v2 新增特性

### 🆕 模板系统（25 种图片类型）

每种图片类型都有对应的 JSON 模板，AI 会自动匹配最适合的模板。

覆盖类型：

| 编号 | 模板名称 | 适用场景 |
|---|---|---|
| 01 | hero-image | 主图/核心卖点图 |
| 02 | lifestyle-scene | 场景生活图（产品在真实使用场景） |
| 03 | flat-lay | 平铺图（产品+配件平铺拍摄） |
| 04 | detail-macro | 微距细节图（材质/工艺特写） |
| 05 | before-after | Before/After 对比图 |
| 06 | packaging-front | 包装正面图 |
| 07 | packaging-back | 包装背面/侧面图 |
| 08 | infographic | 信息图（数据/功能可视化） |
| 09 | size-spec | 尺寸规格图 |
| 10 | color-options | 颜色选项图 |
| 11 | infographic-aplus | A+ 信息图 |
| 12 | brand-story | 品牌故事图 |
| 13-25 | ... | 更多模板 |

### 🆕 Style Lock（风格锁定）

多张图任务时，AI 先建立一份 Style Lock（色板 HEX、光线方向、布局逻辑、图标风格），后续每张图的 Prompt 都原样带入，保证系列图风格一致。

**没有 Style Lock 会怎样？** 6 张副图可能每张色调都不一样，看起来像 6 个不同的产品拍的。

### 🆕 Prompt 铁律（7 条）

AI 生成图片时必须遵守的 7 条规则，防止生成废图：

| 铁律 | 内容 | 为什么重要 |
|---|---|---|
| 一 | 颜色必须用 HEX 码（不用"红色"这种模糊词） | AI 不知道你说的"红色"是哪红 |
| 二 | 产品占比必须数字化（填写具体百分比） | 防止产品画太大或太小 |
| 三 | 必须带 `negative_prompt`（负面约束） | 告诉 AI "不要什么"和"要什么"一样重要 |
| 四 | 认证/功效/性能表述必须有依据 | Amazon 会查，乱写会被封 |
| 五 | Prompt 结构标准化 | 保证每张图的质量稳定 |
| 六 | Style Lock 必须贯穿所有图片 | 保证风格统一 |
| 七 | Amazon 主图绝不 AI 生成 | 主图必须用真实产品白底图 |

### 🆕 OpenAI 兼容 API 支持

`scripts/generate_image.py` 支持任意 OpenAI 兼容 API（不限于 OpenAI，国内大模型网关也可使用）。

支持三种模式：
- **API 模式**：配置 API Key 后自动生图（最省事）
- **Prompt-only 模式**：只输出 Prompt，不调用 API（复制到任意生图工具）
- **批量模式**：从 `approved_image_plan.json` 批量生成（一次性出 20 张）

---

## 前置准备清单

在开始之前，请确保你有以下东西：

### ✅ 必须有的

| 项目 | 说明 | 怎么获取 |
|---|---|---|
| **AI 平台账号** | ChatGPT Plus / Claude / Gemini 等 | 注册对应平台账号 |
| **产品白底图** | 纯白色背景的产品照片，至少 1 张 | 自己拍，或让供应商提供 |
| **产品资料** | 标题、五点描述、产品说明 | 从现有 Amazon Listing 复制 |

### ⭕ 可选（有了更好）

| 项目 | 说明 |
|---|---|
| **AI 图像生成 API Key** | OpenAI / 国内大模型网关的 API Key（没有就用 Prompt-only 模式） |
| **品牌 Logo** | 用于 A+ 品牌故事页 |
| **品牌色板** | 你的品牌主色/辅色（HEX 格式，比如 `#FF5733`） |

### 💻 软件准备

| 软件 | 用途 | 必须？ |
|---|---|---|
| **解压缩软件**（WinRAR/7-Zip） | 解压下载的 Skill 文件 | ✅ 必须 |
| **文本编辑器**（记事本/VS Code） | 编辑 `product_info.md` | ✅ 必须 |
| **Python 3.8+** | 运行尺寸裁切脚本（可选） | ⭕ 可选 |

> **不会用 Python？** 没关系，AI 可以直接输出图片文件给你，不需要运行脚本。脚本只是帮你批量裁切尺寸。

---

## 需要提供什么（详细版）

### 必填（缺任何一项 Skill 不启动）

#### ① `product_info.md` — 产品信息文件

这个文件告诉 AI 你的产品是什么、卖点是什么、卖给谁。

**最简单的方式：** 直接把你的 Amazon Listing 文案复制进去，AI 会帮你整理。

**标准格式（推荐）：**

```markdown
# 产品标题（直接复制 Amazon 上的标题）
Premium Stainless Steel Dog Water Fountain, 2.5L Pet Drinking Fountain with 3 Filters...

# 五点卖点（直接复制 Amazon 上的五点）
- 🐾 Large Capacity: 2.5L water capacity perfect for medium dogs...
- 🔇 Super Quiet: Updated pump with silent design, noise level <30dB...
- 💧 Triple Filtration: High-density cotton + activated carbon + rope...
- 🛡️ Safe Material: Food-grade 304 stainless steel...
- ⚡ Easy to Clean: Dishwasher safe parts...

# 产品描述
This premium pet water fountain is designed for...

# 核心功能/主打卖点（用你的话总结，3-5 条）
- 水电分离设计，安全
- 花瓣出水，模拟活水
- 6 种颜色可选

# 目标人群（谁会买）
- 养中大型犬的家庭
- 关注宠物饮水健康的铲屎官
- 喜欢静音电器的用户

# 使用场景（在哪里用）
- 家庭客厅/厨房
- 办公室宠物区
- 宠物店

# 已验证的认证（必须有证明才写）
- CE Certified
- FCC Certified
- RoHS Compliant

# 不能使用的敏感表达（写上你知道的禁用词）
- 不要写"medical grade"（没有医疗认证）
- 不要写"100% bacteria free"（无法证明）
```

**示例：宠物饮水机完整填写示例**

见 `references/product_info_example.md`（Skill 包内已包含示例）

#### ② `white_images/` — 产品白底图文件夹

把你的产品白底图放在这个文件夹里。

**要求：**
- 纯白色背景（RGB 255,255,255）
- 产品占比 ≥ 85%（产品要占满画面）
- 至少 1600px 长边（像素要够大）
- 无文字 / 无 Logo / 无道具

**建议准备 3-5 张：** 正面、侧面、45°角、使用状态、配件特写

```
white_images/
├── main-front.png    ← 正面（必备，主图用这个）
├── main-side.png     ← 侧面（建议）
├── main-angle.png    ← 45°角（建议）
├── main-usage.png    ← 使用状态（建议）
└── accessory.png     ← 配件特写（可选）
```

> **没有白底图？** 用手机拍一张纯白色背景的产品照片，或者用 Remove.bg 等工具去掉背景。

---

### 选填（有就更好，没有也能跑）

| 文件 | 内容 | 用途 |
|---|---|---|
| `brand_assets/logo.png` | 品牌 Logo（透明背景 PNG） | A+ 品牌故事页使用 |
| `brand_assets/brand-colors.md` | 品牌主色/辅色（HEX 格式） | 统一画面调性 |
| `requirements.md` | 特殊需求 | 指定场景、必须包含/排除的元素、风格偏好 |

**`brand-colors.md` 示例：**

```markdown
# 品牌色板

## 主色
- 品牌红：#E74C3C
- 深灰：#2C3E50

## 辅色
- 浅灰：#ECF0F1
- 金色：#F39C12

## 禁忌色
- 不要使用亮黄色（和竞品重复）
```

---

### 最终文件夹结构

```
my-product/                    ← 你在电脑上建的文件夹，名字随便取
├── product_info.md            ← 必填（按上面的格式填写）
├── white_images/              ← 必填（放白底图）
│   ├── main-front.png
│   ├── main-side.png
│   └── main-angle.png
├── brand_assets/              ← 选填
│   ├── logo.png
│   └── brand-colors.md
└── requirements.md            ← 选填
```

> **小贴士：** 文件夹可以放在电脑任何位置，只要记住路径就行。比如 `C:\my-product\` 或 `桌面\pet-fountain\`

---

## 怎么用（手把手教程）

### 第一步：下载并安装 Skill

**方式 A：Git Clone（推荐，有 Git 的用这个）**

```bash
# 放到对应平台的 skills 目录
git clone https://github.com/nzsto721/amazon-visual-aplus-generator.git
```

**方式 B：下载 ZIP 解压**

1. 打开 https://github.com/nzsto721/amazon-visual-aplus-generator
2. 点绿色的 "Code" 按钮 → "Download ZIP"
3. 解压到你的 AI 平台对应的 skills 目录

---

### 第二步：配置到你的 AI 平台

#### ChatGPT 用户

1. 打开 ChatGPT → 右上角头像 → **Settings**
2. 左侧选 **Personalization**
3. 找到 **Custom instructions**
4. 打开 `SKILL.md` 文件（用记事本打开）
5. **全选复制** → 粘贴到 Custom instructions 的 **"How would you like ChatGPT to respond?"** 框里
6. 点 Save

> **注意：** ChatGPT 免费用户可能没有 Custom instructions 功能，需要 Plus 订阅。

#### Claude 用户

1. 打开 Claude → 左侧 **Create Project**
2. Project 名称填：`Amazon Visual Generator`
3. 找到 **Project instructions** 框
4. 打开 `SKILL.md` 文件 → **全选复制** → 粘贴到 Project instructions 框里
5. 点 Create Project

以后每次用，都在这个 Project 里对话即可。

#### Gemini 用户

1. 打开 Gemini
2. 点左上角 **Menu** → **Gem manager**
3. 点 **New Gem** → 名称填：`Amazon Visual Generator`
4. 找到 **System Instructions** 框
5. 打开 `SKILL.md` 文件 → **全选复制** → 粘贴到 System Instructions 框里
6. 点 Save

#### Codex / WorkBuddy 用户

把整个 `amazon-visual-aplus-generator` 文件夹放到 `~/.workbuddy/skills/` 目录即可，Skill 会自动加载。

---

### 第三步：准备产品文件夹

按照「需要提供什么」一节，准备好 `product_info.md` + `white_images/`。

**不会写 `product_info.md`？** 最简单的方法：

1. 打开你的 Amazon 产品页面
2. 复制标题、五点、描述
3. 粘贴到 `product_info.md`，AI 会帮你整理

---

### 第四步：启动 Skill

在 AI 对话窗口输入（通用指令，各平台均可使用）：

```
请用 amazon-visual-aplus-generator 为以下产品策划 Amazon 副图和 A+ 内容：

产品文件夹路径：C:\my-product

请先只输出策划方案（Phase 1），不要生成图片，等我确认后再继续。
```

> **路径怎么写？** 找到你的产品文件夹，在地址栏复制完整路径。比如 `C:\Users\你的用户名\Desktop\pet-fountain`

---

### 第五步：和 AI 对话，确认方案

AI 会先输出策划方案（不会直接生图）。你需要：

**如果方案 OK：** 回复 `确认` 或 `approved` 或 `go ahead`

**如果方案需要修改：** 直接说，比如：
- `副图 2 不要讲厨房场景，改成露营场景`
- `A+ 第 3 张不要讲材料，改成安装步骤`
- `整体风格不要太科技，改成家庭温暖风`
- `产品目标人群改成养猫的人`

AI 会修改方案，再次等你确认。

---

### 第六步：等待生成

确认后，AI 会：
1. 生成详细的 JSON 图片计划（`approved_image_plan.json`）
2. 为每张图生成 Prompt
3. 调用图像生成 API 生图（如果配置了 API Key）
4. 或只输出 Prompt（如果没有 API Key，你手动拿 Prompt 去生图）

---

## 各平台配置详解

### ChatGPT 配置截图说明

```
步骤示意图（你需要在这些位置操作）：

[ChatGPT 主界面]
    ↓
[右上角头像] → Settings
    ↓
[左侧菜单] → Personalization
    ↓
[Custom instructions] 按钮 → 点击打开
    ↓
[How would you like ChatGPT to respond?] 文本框
    ↓
粘贴 SKILL.md 全文
    ↓
[Save] 按钮 → 点击保存
```

### Claude Project 配置截图说明

```
步骤示意图：

[Claude 主界面]
    ↓
[左侧栏] → "+ Create Project"
    ↓
[Project Name] → 填写 "Amazon Visual Generator"
    ↓
[Project Instructions] 文本框
    ↓
粘贴 SKILL.md 全文
    ↓
[Create Project] 按钮 → 点击创建
```

---

## 对话示例（你应该怎么和 AI 对话）

### 第一次对话：启动 Skill

**你：**
```
请用 amazon-visual-aplus-generator 为以下产品策划 Amazon 副图和 A+ 内容：

产品文件夹路径：C:\pet-fountain

请先只输出策划方案（Phase 1），不要生成图片，等我确认后再继续。
```

**AI 回复：**（会先读取你的产品资料，然后输出策划方案，包含副图 6 张 + A+ 7 张的详细策划）

### 第二次对话：确认或修改

**你（如果方案 OK）：**
```
确认，继续生成详细 JSON 参数和图片。
```

**你（如果方案需要修改）：**
```
副图 2 的场景改成养猫场景，不要养狗。
A+ 第 1 张的标题改成更吸引人的。
整体风格改成温暖家居风，不要用冷色调。
```

**AI 回复：**（修改方案，再次等你确认）

### 第三次对话：生成完成后的验收

**你：**
```
生成的图片我看了一下，第 3 张的文字有点看不清，能重新生成一张吗？
```

**AI 回复：**（重新生成那张图）

---

## 交付物说明

生成完成后，你的产品文件夹里会多出这些文件：

```
my-product/
├── product_info.md              ← 你提供的原始文件
├── white_images/               ← 你提供的白底图
├── approved_image_plan.json    ← AI 生成的图片计划（可复用、可检查）
├── generated/                  ← 原始生成图（未裁切，AI 直接生成的）
│   ├── secondary-01.png
│   ├── secondary-02.png
│   ├── aplus-desktop-01.png
│   └── ...
└── final/                     ← Amazon 上传尺寸（已裁切，直接用这个）
    ├── secondary-01.jpg       ← 1200×1600，副图用
    ├── secondary-02.jpg
    ├── aplus-desktop-01.jpg  ← 1464×600，A+ 桌面版用
    ├── aplus-mobile-01.jpg   ← 1600×1200，A+ 移动版用
    └── ...
```

**哪个文件夹里的图是最终要上传的？** → `final/` 文件夹

---

## 生成后如何使用

### 上传到 Amazon Seller Central

1. 打开 Amazon Seller Central → 库存 → 管理库存
2. 找到你的产品 → 编辑
3. 切到 **图片** 标签页
4. 上传 `final/` 文件夹里的图片：
   - 主图：用 `white_images/main-front.png`（不要传 AI 生成的主图）
   - 副图 1-6：用 `final/secondary-01.jpg` 到 `secondary-06.jpg`
5. 切到 **A+ Content** 标签页
6. 创建或编辑 A+ Content，插入 `final/aplus-desktop-*.jpg`

### 图片顺序建议

| 位置 | 建议内容 |
|---|---|
| 主图 | 白底产品图（真实拍摄，不要 AI 生成） |
| 副图 1 | 核心卖点图（一眼看懂产品最大的价值） |
| 副图 2 | 场景图（产品在真实使用场景） |
| 副图 3 | 功能拆解图（结构、材料、核心功能） |
| 副图 4 | 尺寸/兼容图（降低买错风险） |
| 副图 5 | 使用步骤图（降低操作门槛） |
| 副图 6 | 包装清单/配件图（减少售后误解） |

---

## 验收清单

AI 生成图后，**必须人工检查**以下内容，确认没问题再上传 Amazon：

- [ ] 产品外观有没有被 AI 改错？（颜色、形状、配件是否和实物一致）
- [ ] 图片里的英文有没有拼写错误？
- [ ] 有没有写没有证据的认证、功效、承重、环保、医疗相关表述？
- [ ] 移动端小图能不能看清核心文字？（用手机看一下）
- [ ] A+ 桌面版和移动版是不是都符合上传尺寸？
- [ ] 系列图的风格是否一致（Style Lock 有无被偏离）？
- [ ] 颜色是否和计划中 HEX 码一致？（用取色器检查）
- [ ] 图片是否清晰？有没有 AI 常见的"多手指"、"文字乱码"等错误？

> **⚠️ 重要：** Amazon 对图片审核很严格，违规图片会导致产品被下架。一定要检查完再上传！

---

## FAQ（更多问题）

### Q：我是完全小白，不会用怎么办？

A：按照本 README 的「手把手教程」一节，一步一步来。如果还有问题，可以在 GitHub 仓库提 Issue，或联系作者。

### Q：主图可以用 AI 生成吗？

A：**不可以。** Amazon 规定主图必须是真实产品照片。本 Skill 设计上就禁止 AI 生成主图，只会帮你检查白底图是否合规。

### Q：如果我没有设计师，也没有 API Key，能用吗？

A：**可以。** Skill 支持 Prompt-only 模式，只输出 Prompt，你复制到任意生图工具（Midjourney、DALL-E、Stable Diffusion 等）即可。

### Q：这套 Skill 只适用于宠物用品吗？

A：**不是。** 适用于任何 Amazon 品类。只需在 `product_info.md` 中提供对应产品的信息。模板系统里已经包含了 beauty / electronics / home / fashion 等类目的定制提示。

### Q：Style Lock 一定要用吗？

A：多张图任务（比如一套 6 张副图 + 7 张 A+）**强烈建议使用**，否则系列图风格容易不一致。单张图可以不使用。

### Q：生成的图片可以直接上传 Amazon 吗？

A：**需先通过验收清单。** AI 生成图可能存在产品变形、文字错误、多手指等问题，必须人工验收后再上传。

### Q：API Key 怎么获取？

A：**OpenAI API Key：** 打开 https://platform.openai.com/api-keys → 登录 → Create new secret key

**国内大模型网关：** 阿里云百炼、腾讯云 AI 等都有 OpenAI 兼容接口，获取方式参见对应平台文档。

### Q：生成图片要花钱吗？

A：如果用 OpenAI API，每张图约 $0.04-$0.08（取决于尺寸和质量）。如果只用 Prompt-only 模式（不调用 API），则不花钱，但需要你有 Midjourney 等生图工具的订阅。

### Q：生成的图片分辨率是多少？

A：
- 副图：1200×1600px（Amazon 推荐尺寸）
- A+ 桌面版：1464×600px（Amazon 规定尺寸）
- A+ 移动版：1600×1200px（Amazon 规定尺寸）

### Q：我是 Mac 用户，路径怎么写？

A：Mac 的路径格式和 Windows 不同，比如：`/Users/你的用户名/Desktop/my-product`

在 Skill 启动时，把路径改成 Mac 格式即可，其他完全一样。

### Q：可以同时给多个产品生成图片吗？

A：可以，但建议一个一个来。每个产品单独建一个文件夹，分别启动 Skill。

---

## 文件结构

```
amazon-visual-aplus-generator/
├── SKILL.md                          # Skill 核心定义（v2 工作流 + 约束规则）
├── README.md                         # 本文件）
├── .gitignore                       # Git 忽略文件配置
├── scripts/
│   ├── visual_size_helper.py         # 尺寸裁切脚本（Pillow，可选）
│   └── generate_image.py            # 图像生成脚本（OpenAI 兼容 API）
├── references/
│   ├── amazon_image_specs.md        # Amazon 图片规范详解（含宠物用品类目规则）
│   ├── json_schema.md               # approved_image_plan.json 字段定义（v2）
│   ├── prompt_guidelines.md         # Prompt 撰写 7 条铁律
│   └── product_info_example.md      # product_info.md 填写示例
└── templates/                       # 图片类型 JSON 模板（25 个）
    ├── 01-hero-image.json
    ├── 02-lifestyle-scene.json
    ├── 03-flat-lay.json
    ├── 04-detail-macro.json
    ├── 05-before-after.json
    ├── 11-infographic.json          # A+ 信息图核心模板
    ├── 13-size-spec.json            # 尺寸规格图模板
    └── ...
```

---

## 依赖

- **支持 System Prompt 的 AI 平台**（ChatGPT / Claude / Gemini / Codex / 等）
- **图像生成能力**（AI 平台自带，或配置 OpenAI 兼容 API）
- **Pillow**（可选）：`pip install Pillow`（`visual_size_helper.py` 需要，不用脚本可不装）

---

## License

MIT — 可自由使用、修改、分发。

---

> 真正被改变的，不只是「图片能不能 AI 画」。
> 而是一个普通运营，也可以拥有一套接近专业视觉团队的工作流。

---

## 更新日志

### v2.0（2025-06-15）

- ✅ 新增 25 个图片类型 JSON 模板
- ✅ 新增 Style Lock（风格锁定）机制
- ✅ 新增 Prompt 铁律（7 条规则）
- ✅ 新增 `generate_image.py`（OpenAI 兼容 API 生图脚本）
- ✅ 新增 `prompt_guidelines.md`（Prompt 撰写参考）
- ✅ 更新 `json_schema.md`（增加 negative_prompt / style_lock / product_coverage_ratio 字段）
- ✅ 重写 README（详细版，让小白也能看懂）

### v1.0（2025-06-15）

- ✅ 初始版本发布
- ✅ 5 阶段工作流（确认闸门机制）
- ✅ Amazon 图片规范参考
- ✅ `visual_size_helper.py` 尺寸裁切脚本
