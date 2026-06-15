# Amazon Visual & A+ Generator

> 一套通用 AI Skill，跑完亚马逊副图 + A+ 全流程：从市场调研、视觉策划、JSON 脚本到生图裁切。把跨境人的视觉工作流收进一条指令。适用于 ChatGPT、Claude、Codex、Gemini 等主流大模型平台。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-AI%20Skill%20(Cross--Platform)-blueviolet)]()

---

## 为什么需要这个 Skill？

以前做一套亚马逊图片，通常要经历一条很长的链路：

> 运营整理卖点 → 找竞品图片 → 写需求文档 → 设计师理解产品 → 反复沟通"这个功能怎么表达？场景准不准确？尺寸图有没有参数？" → 一版、二版、三版来回改。

如果产品有英语站、小语种站，或者同时要做副图、A+ 桌面版、A+ 移动版，工作量继续翻倍。

**这个 Skill 换了一种做法：** 把产品资料和白底图丢给它，它先做市场调研和视觉策划，确认方向没问题后，再生成每张图的详细脚本（标题、副标题、图标、构图、尺寸参数），最后调用图像模型生成图片并裁切成亚马逊需要的尺寸。

---

## 它不是什么

**这⾥必须先踩刹车：AI 不是替你"乱画图"。**

| 视觉任务 | Skill 适合做什么 | 你必须把关什么 |
|---------|----------------|--------------|
| **主图** | 检查白底、主体占比、清晰度、是否有多余文字和道具 | 产品必须真实，不能虚构功能、配件和包装 |
| **副图** | 把五点卖点翻译成场景图、功能图、尺寸图、对比图 | 标题、数据、认证、效果对比必须有依据 |
| **A+ 页面** | 规划品牌故事、痛点场景、产品结构、使用方式和移动端重构 | 最终文案和图片要符合品牌调性和类目合规 |

**Skill 的定位不是"AI 设计师"，而是一个懂亚马逊转化逻辑的视觉策划助手。**

---

## 5 阶段工作流

```
输入产品文件夹 → 联网调研 → [确认闸门] → JSON 细化 → 生图 → 裁切
```

### Phase 0 — 输入验证

检查产品文件夹是否完整，缺什么告诉你补什么。

### Phase 1 — 调研 + 策划方案（不生图）

**联网调研 5 个维度：**

| 调研维度 | 要提炼什么 |
|---------|-----------|
| 市场基本情况 | 类目常见价格带、功能表达、图片风格、主流卖点 |
| 目标人群 | 谁在买、为什么买、什么场景触发购买 |
| 竞品图片 | 竞品怎么讲卖点，哪些图做得好，哪些信息重复严重 |
| 评论痛点 | 用户最常抱怨的问题，能不能转成视觉解释 |
| 合规边界 | 哪些词不能随便写，哪些认证必须有证明 |

**输出策划方案：**

- **主图审计**：检查白底、主体占比、清晰度、违规元素
- **6 张副图规划**：每张图解决哪个购买顾虑
- **7 张 A+ 模块规划**：从品牌开场到售后承诺的完整叙事线
- **合规风险提醒**：哪些表述需要你提供证据

> 💡 **举例：** 一个厨房收纳产品，普通运营写"节省空间、安装简单、材质耐用"。Skill 调研后会拆成更具体的视觉方向——台面太乱做前后对比、租房用户做免打孔场景、担心承重做结构拆解、不知道尺寸做实物参考。这才是图片策划的核心：**把购买阻力一个个拆掉。**

### 🔴 确认闸门

策划方案输出后，**Skill 会停下来等你确认**。你可以直接批准，也可以定向调整：

> "副图 2 改成露营场景"  
> "A+ 第 3 张改成安装步骤"  
> "整体风格换家庭温暖风"

**这样做的好处很直接：不会因为前期方向错了，一次性生成 20 张没法用的图。**

### Phase 2 — JSON 细化 + 生图 + 裁切

你确认后，Skill 才会进入第二阶段。

**第一步：生成 `approved_image_plan.json`**

每张图拆成可执行的 JSON 条目：

```json
{
  "id": "secondary-01",
  "asset_type": "secondary_image",
  "final_size": {"width": 1200, "height": 1600},
  "generation_size": {"width": 1200, "height": 1600},
  "safe_area": "keep key text and product inside center 86%",
  "source_product_images": ["white_images/main-front.png"],
  "headline": "More Space, Less Mess",
  "subheadline": "Organize your kitchen in minutes",
  "icon_labels": ["No drilling", "Strong hold", "Easy clean"],
  "scene": "bright modern kitchen countertop",
  "composition": "product on right, before/after scene on left, icons at bottom",
  "claims_to_avoid": ["unverified weight capacity"],
  "prompt": "final image-generation prompt"
}
```

> **为什么用 JSON？** 一套图不是一张图——副图 + A+ 桌面版 + A+ 移动版加起来可能是 20 张以上。只靠自然语言很容易漏尺寸、漏标题、漏图标。JSON 把视觉任务变成可检查、可复用、可批量执行的清单。

**第二步：逐张生成图片**

调用图像模型按 Prompt 逐张生成，一张一张来，控制质量。

**第三步：尺寸裁切**

这是最容易踩坑的地方。A+ 桌面版的 **1464 × 600** 不能被 16 整除（GPT Image 2 的硬性要求），所以生成画布和最终上传尺寸要分开管理：

| 类型 | Amazon 上传尺寸 | 模型生成画布 | 说明 |
|------|:---:|:---:|------|
| 副图 | 1200 × 1600 | 1200 × 1600 | 直接生成，无需裁切 |
| A+ 桌面版 | 1464 × 600 | **1488 × 608** | ⚠️ 生成后裁切 |
| A+ 移动版 | 1600 × 1200 | 1600 × 1200 | 直接生成，无需裁切 |

---

## 需要你准备什么

先建一个产品文件夹：

```
my-product/
├── product_info.md        # 必填：标题、五点、描述、主打卖点、适用人群、使用场景、已验证的认证
├── white_images/          # 必填：至少 1 张真实产品白底图
│   ├── main-front.png
│   └── main-side.png
├── brand_assets/          # 选填：品牌 Logo + 色板
│   ├── logo.png
│   └── brand-colors.md
└── requirements.md        # 选填：特殊需求（指定场景、禁止元素、风格偏好等）
```

**`product_info.md` 必须包含：**

| 字段 | 说明 |
|------|------|
| 产品标题 | Amazon Listing Title |
| 五点卖点 | 5 Bullet Points |
| 产品描述 | Product Description |
| 核心功能 | Key Features / 主打卖点 |
| 目标人群 | 谁在买、为什么买 |
| 使用场景 | 用在什么地方 |
| 已验证的认证 | FCC/CE/RoHS/FDA 等有证明的 |
| 敏感表达 | 哪些词不能写（如有） |

> 💡 还没整理？直接把当前 Amazon Listing 文案复制进去也行，Skill 会先帮你梳理。

---

## 怎么用

### 1. 下载 Skill

```bash
git clone https://github.com/nzsto721/amazon-visual-aplus-generator.git
```

### 2. 配置到你的 AI 平台

将仓库内容作为 System Prompt / Project Instructions / Custom Skill 导入到你使用的 AI 平台。核心文件是 `SKILL.md`，它包含了完整的工作流指令和约束规则。

各平台配置方式：

| 平台 | 配置入口 |
|------|---------|
| ChatGPT | Custom GPT → Instructions 粘贴 SKILL.md |
| Claude | Project Knowledge → 上传 SKILL.md |
| Gemini | System Instructions → 粘贴 SKILL.md |
| 其他支持 System Prompt 的平台 | 将 SKILL.md 作为系统提示词注入 |

### 3. 安装 Python 依赖

```bash
pip install Pillow
```

### 4. 启动 Skill

将产品文件夹准备好后，在对话中输入：

```
用 amazon-visual-aplus-generator 给这个产品策划副图和 A+，产品文件夹路径：[你的路径]
第一阶段只输出策划草案，等我确认后再生图。
```

### 5. 控制流程

| 你的回复 | 效果 |
|---------|------|
| "确认" / "approved" / "go ahead" | 进入 Phase 2，开始 JSON 细化和生图 |
| "副图 3 改成 xx 场景" / "A+ 第 2 张不要讲材料" | Skill 修改方案后重新呈现 |
| 任何其他调整意见 | Skill 按你的方向修正后再确认 |

---

## 最终交付物

当 Skill 跑完全流程，你会得到：

```
my-product/
├── approved_image_plan.json   # 所有图片的完整脚本（可复查、可复用）
├── generated/                 # 模型原始输出
│   ├── secondary-01.png
│   ├── secondary-02.png
│   ├── ...
│   ├── aplus-desktop-01.png
│   ├── aplus-mobile-01.png
│   └── ...
└── final/                     # 裁切后可直接上传 Amazon 的图片
    ├── secondary-01.jpg
    ├── secondary-02.jpg
    ├── ...
    ├── aplus-desktop-01.jpg
    ├── aplus-mobile-01.jpg
    └── ...
```

---

## 上传前必查清单

AI 可以把效率拉得很高，但亚马逊图片不是发朋友圈。最终上线前至少检查这些：

- [ ] 产品外观有没有被 AI 改错？
- [ ] 图片里的英文有没有拼写错误？
- [ ] 有没有写了没有证据的认证、功效、承重、环保、医疗相关表述？
- [ ] 移动端小图能不能看清核心文字？
- [ ] A+ 桌面版和移动版是不是都符合上传尺寸？
- [ ] 主图是否符合 Amazon 白底图全部要求？

> **核心原则：Skill 负责把 0 到 1 的视觉策划和初稿生成跑起来，运营负责最终判断是否符合产品事实和平台规则。**

---

## 设计哲学

真正让图片变好的，不是图像模型，而是前面的判断：

- 这张图解决哪个购买疑虑？
- 有没有重复上一张图的信息？
- 文字手机端能不能看清？
- 这个功能有没有证据？能不能写进图里？
- A+ 桌面版和移动版是不是分别重新构图？

如果这些问题没想清楚，再好的图像模型也只是帮你把错误方向画得更漂亮。

---

## 文件结构

```
amazon-visual-aplus-generator/
├── SKILL.md                          # Skill 核心定义（5 阶段工作流 + 约束规则）
├── README.md                         # 本文件
├── .gitignore
├── scripts/
│   └── visual_size_helper.py         # 尺寸处理脚本
│                                      #   python visual_size_helper.py plan
│                                      #   python visual_size_helper.py finalize --type aplus_desktop ...
│                                      #   python visual_size_helper.py batch --manifest plan.json ...
└── references/
    ├── amazon_image_specs.md          # Amazon 图片规范 + GPT Image 2 约束（280 行完整参考）
    └── json_schema.md                 # approved_image_plan.json 字段级 Schema 定义
```

---

## 依赖

- **Pillow**：`pip install Pillow`（尺寸处理脚本需要）
- **支持 System Prompt / Custom Instructions 的 AI 平台**（ChatGPT / Claude / Gemini / Codex 等）
- **图像生成能力**：需要平台支持图像生成 API（如 DALL·E / GPT Image / Imagen 等）

---

## 常见问题

**Q: 主图能不能让 AI 直接生成？**  
A: 不能。主图必须用真实产品白底图，Skill 只负责检查合规性，不会凭空生成一个不存在的产品。

**Q: 联网调研的数据准不准？**  
A: 只作为方向参考。如果要做严肃的市场判断，建议结合卖家精灵、Sif 关键词或其他第三方 MCP 服务器获取更精准的数据。

**Q: 生成 20 张图要多久？**  
A: 取决于图像模型 API 速度，通常在 5-15 分钟。因为每张图都是逐张生成的，可以保证质量控制。

**Q: 能不能只做副图、不做 A+？**  
A: 可以。在策划阶段告诉 Skill 你的需求即可，比如"只要副图，不要 A+"。

---

## 许可证

MIT © [nzsto721](https://github.com/nzsto721)

---

## 参考资料

- [Amazon Seller Central: Product Image Requirements](https://sellercentral.amazon.com/help/hub/reference/external/1881)
- [Amazon Seller Central: A+ Content Guidelines](https://sellercentral.amazon.com/help/hub/reference/G202094180)
- [OpenAI: Image Generation API](https://platform.openai.com/docs/guides/images)
