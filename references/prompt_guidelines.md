# Prompt 撰写铁律 · Amazon 视觉策划专用

> 本文件是 `amazon-visual-aplus-generator` v2 的 Prompt 撰写规范参考。
> 所有生成的 image_generation_prompt 必须遵循以下规则。

---

## 铁律一：颜色必须用 HEX 码

❌ 错误写法：
```
温暖金色点缀、白色背景、浅木色桌面
```

✅ 正确写法：
```
background: #FFFFFF (pure white)
accent color: #D4AF37 (premium gold)
desktop surface: #F5DEB3 (warm light wood)
text overlay: #1A1A1A (near-black, high contrast)
brand color: #2E8B57 (seafoam green, pet brand)
```

**原因：** AI 图像模型对颜色形容词理解不稳定。"金色"可能生成黄铜色、土黄色或亮黄色。HEX 码是唯一精确控制方式。

---

## 铁律二：产品占比必须数字化

每张图的 `product_coverage_ratio` 字段必须填写具体百分比：

| 图片类型 | 产品占比 | 说明 |
|---|---:|---|
| Amazon 主图（白底） | 85-90% | 搜索结果页第一印象，主体要满 |
| 副图 · 核心卖点图 | 40-50% | 产品 + 功能说明各占一半 |
| 副图 · 场景生活图 | 25-35% | 场景和情绪优先，产品是配角 |
| 副图 · 尺寸对比图 | 30-40% | 产品 + 参照物（硬币/手机/手） |
| 副图 · 功能拆解图 | 50-60% | 爆炸图/结构图，产品为主体 |
| A+ 桌面版模块图 | 35-45% | 横版构图，产品偏一侧 |
| A+ 移动版模块图 | 40-50% | 竖版构图，产品居中偏上 |
| Before/After 对比图 | 20-30% | 产品只在 After 侧出现 |

**JSON 中必须包含：**
```json
"product_coverage_ratio": "40-50%",
"product_position": "right side, vertically centered"
```

---

## 铁律三：必须带 negative_prompt

每张图的 Prompt 生成后，必须附带标准负面约束。根据图片类型选择对应模板。

### 通用负面约束（所有图片必带）

```
negative_prompt:
  - "no fake logos, no watermark, no unreadable text"
  - "no exaggerated claims text in image"
  - "no distorted product shape, no extra parts not in reference"
  - "no celebrity, no trademarked brand imitation"
  - "no medical claims without verification"
  - "no fake certifications, no unverified badges"
```

### 主图专用负面约束（额外增加）

```
  - "no text of any kind on main image"
  - "no props, no accessories not included in package"
  - "no human hands, no models, no animals not in scene"
  - "no colored background, must be pure white #FFFFFF"
```

### 场景图负面约束（额外增加）

```
  - "no messy cluttered background"
  - "no inappropriate age group for product"
  - "no unsafe product usage demonstration"
```

---

## 铁律四：认证/功效/性能表述必须有依据

在 `claims_to_avoid` 字段中，必须列出所有未经证实的表述：

```json
"claims_to_avoid": [
  "IPX7 waterproof — only state if test report provided",
  "BPA Free — only state if material cert provided",
  "FDA approved — DO NOT use, FDA does not approve pet products",
  "eliminates 99% bacteria — requires lab test report",
  "lasts 3 years — requires durability test report"
]
```

**规则：** 如果 `product_info.md` 里没有提供证明文件的表述，一律写进 `claims_to_avoid`，不写进 Prompt。

---

## 铁律五：Prompt 结构标准化

每张图的生成 Prompt 必须按照以下顺序组装：

```
[主体描述] + [场景/背景] + [光线/氛围] + [构图] + [质量标签] + [负面约束]
```

### 示例：副图 · 场景生活图

```
Prompt:
A stainless steel pet water fountain (product: #1E88E5 blue, spout: #FFD700 gold)
placed on a light wood floor (#F5DEB3) in a modern living room.
Natural morning sunlight (#FFF8DC) streaming from left, soft shadows.
Product positioned right side, 35% frame coverage.
Lifestyle photography, warm and inviting atmosphere,
8K, photorealistic, professional e-commerce.

Negative:
no text, no fake logos, no watermark, no distorted shape,
no unverified claims, no medical claims, no celebrity.
```

---

## 铁律六：Style Lock 必须贯穿所有图片

多张图任务时，在 Phase 2 开始前列出 Style Lock，后续每张图的 Prompt 必须原样带入。

### Style Lock 模板

```json
"style_lock": {
  "color_palette": {
    "primary": "#2E8B57",
    "accent": "#FFD700",
    "background": "#FFFFFF,#F5F1E8",
    "text": "#1A1A1A"
  },
  "lighting": "natural morning light, soft and warm",
  "layout_logic": "product right, text/icon left, consistent margins",
  "icon_style": "outline icons, 2px stroke, rounded corners",
  "font_mood": "clean sans-serif, premium but approachable",
  "negative_prompt_base": "no text in image, no fake logos, ..."
}
```

**锁定后，每张图的 JSON 中必须包含：**
```json
"style_lock_ref": "locked-v1",
"style_lock_deviation": "none"   // 或说明哪里的合理调整
```

---

## 铁律七：Amazon 主图绝不 AI 生成

主图处理规则（不可违反）：

1. 读取 `white_images/` 中的白底图
2. 检查合规：纯白背景？主体占比 ≥85%？无文字/道具？
3. 如不合规 → 输出问题清单，要求用户补拍，**不生成**
4. 如合规 → 可直接使用，或做轻微增强（去背景杂色、提亮度）
5. **绝不**让 AI 模型"画一张主图"

```json
"main_image_strategy": "use_provided_white_bg_only",
"main_image_checklist": [
  "background_is_pure_white",
  "product_coverage_≥85%",
  "no_text_no_logo_no_prop"
]
```

---

## 快速检查清单

生成每张图之前，快速过一遍：

- [ ] 颜色用了 HEX 码（不用形容词）
- [ ] 产品占比填了具体百分比
- [ ] `negative_prompt` 已填写
- [ ] 所有认证/功效表述有依据（或已列入 `claims_to_avoid`）
- [ ] Prompt 按顺序组装（主体→场景→光线→构图→质量→负面）
- [ ] Style Lock 已建立，本图无偏离（或说明了合理调整）
- [ ] 主图确认不是 AI 生成的
