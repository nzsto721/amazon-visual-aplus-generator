# Image Plan JSON Schema · v2

本文件定义 `approved_image_plan.json` 的完整字段结构。
v2 新增字段：`negative_prompt`、`style_lock`、`product_coverage_ratio`、`prompt_guidelines_ref`。

---

## 顶层结构

```json
{
  "product_name": "Product name as in listing",
  "asin": "B0XXXXXXXXX (optional)",
  "generated_at": "ISO 8601 datetime",
  "style_lock": { },
  "images": [ { } ]
}
```

---

## style_lock 对象

多张图任务时必填。所有图片的 Prompt 必须与此保持一致。

```json
"style_lock": {
  "version": "locked-v1",
  "color_palette_hex": {
    "primary": "#2E8B57",
    "accent": "#FFD700",
    "background": ["#FFFFFF", "#F5F1E8"],
    "text": "#1A1A1A"
  },
  "lighting": "natural morning light, soft and warm, no harsh flash",
  "layout_logic": "product right side (35-45%), text/icon left side, consistent 48px margin",
  "icon_style": "outline icons, 2px stroke, rounded corners, single color #1A1A1A",
  "font_mood": "clean sans-serif, premium but approachable, no serif for modern products",
  "negative_prompt_base": "no text in image, no fake logos, no watermark, no distorted product shape, no unverified claims, no celebrity, no trademarked brand imitation",
  "product_texture_note": "stainless steel with brushed finish, visible but not overpowering",
  "model_or_actor": "none (pet products: use pet only, no human hands unless specified)"
}
```

---

## Image Entry Schema · v2

每个 `images` 数组中的条目遵循以下结构。

```json
{
  "id": "secondary-01",
  "asset_type": "secondary_image",
  "module_position": 1,
  "template_id": "lifestyle-scene",
  "final_size": { "width": 1200, "height": 1600 },
  "generation_size": { "width": 1200, "height": 1600 },
  "safe_area": "keep key text and product inside center 86% of generation canvas",
  "crop_strategy": "direct generation — 1200x1600 is already valid for GPT Image 2",
  "source_product_images": ["white_images/main-front.png"],
  "visual_goal": "explain the core benefit in one glance",
  "headline": "More Space, Less Mess",
  "subheadline": "Organize your kitchen in minutes",
  "icon_labels": ["No drilling", "Strong hold", "Easy clean"],
  "scene_description": "bright modern kitchen countertop, morning light, #FFF8DC sunlight",
  "composition": "product positioned right 40%, before/after scene on left, three icon badges at bottom",
  "tone_and_style": "modern clean, warm neutral tones, natural lighting, #F5DEB3 wood surface",
  "text_placement": "headline top-left, subheadline below headline, icons bottom strip",
  "product_coverage_ratio": "40-50%",
  "product_position": "right side, vertically centered",
  "color_palette_hex": {
    "background": "#FFFFFF",
    "product_accent": "#1E88E5",
    "text": "#1A1A1A"
  },
  "claims_to_avoid": ["unverified weight capacity", "medical-grade", "FDA approved (not for pet products)"],
  "negative_prompt": "no fake logos, no watermark, no unreadable text, no exaggerated claims text in image, no distorted product shape, no extra parts not in reference, no celebrity, no trademarked brand imitation, no medical claims without verification, no fake certifications, no unverified badges, no text on main image, no colored background for main image",
  "prompt": "Full English image-generation prompt with all visual details, HEX codes, and negative constraints",
  "style_lock_ref": "locked-v1",
  "style_lock_deviation": "none",
  "notes": "Optional: any special instructions"
}
```

---

## 字段逐条说明 · v2 新增标 🆕

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 唯一 ID，如 `secondary-01`、`aplus-desktop-03` |
| `asset_type` | string | `secondary_image` / `aplus_desktop` / `aplus_mobile` / `brand_story_desktop` / `brand_story_mobile` |
| `module_position` | int | 模块序号（从 1 开始） |
| `template_id` 🆕 | string | 匹配的模板 ID，如 `lifestyle-scene`、`infographic`（参考 `templates/` 目录） |
| `final_size` | object | `{width, height}` — Amazon 上传尺寸 |
| `generation_size` | object | `{width, height}` — 传给图像模型的画布尺寸 |
| `safe_area` | string | 安全区域说明（裁切时不被切掉的区域） |
| `crop_strategy` | string | 生成输出裁切到最终尺寸的方式 |
| `source_product_images` | array | 用作视觉参考的产品白底图路径 |
| `visual_goal` | string | 这张图要传达的核心信息（一句话） |
| `headline` | string | 图片主标题（建议 ≤5 词） |
| `subheadline` | string | 副标题（≤10 词） |
| `icon_labels` | array | 图标标签文字（3-5 项） |
| `scene_description` | string | 完整场景描述：环境、光线、氛围、**颜色用 HEX 码** |
| `composition` | string | 构图描述：各元素位置 |
| `tone_and_style` | string | 视觉风格方向：色板、摄影风格、氛围，**颜色用 HEX 码** |
| `text_placement` | string | 文字元素位置 |
| `product_coverage_ratio` 🆕 | string | 产品占画面的百分比，如 `"40-50%"` |
| `product_position` 🆕 | string | 产品在画面中的位置，如 `"right side, vertically centered"` |
| `color_palette_hex` 🆕 | object | 本图使用的颜色 HEX 码（覆盖 Style Lock 时填写） |
| `claims_to_avoid` | array | 图片中**不得出现**的认证/功效/性能表述 |
| `negative_prompt` 🆕 | string | 标准负面约束，传给图像模型 |
| `prompt` | string | 完整的英文图像生成 Prompt |
| `style_lock_ref` 🆕 | string | 引用的 Style Lock 版本，如 `"locked-v1"` |
| `style_lock_deviation` 🆕 | string | 本图对 Style Lock 的合理调整说明，`"none"` 表示完全遵守 |
| `notes` | string | 可选：额外说明 |

---

## asset_type 取值

| 值 | 最终尺寸 | 模块上限 | 说明 |
|---|---|---|---|
| `secondary_image` | 1200 × 1600 | 6-9 张 | Listing 副图 |
| `aplus_desktop` | 1464 × 600 | 7 个/页 | A+ Content 桌面版模块 |
| `aplus_mobile` | 1600 × 1200 | 7 个/页 | A+ Content 移动版模块 |
| `brand_story_desktop` | 1464 × 600 | 19 张 | Brand Story 轮播桌面版 |
| `brand_story_mobile` | 1600 × 1200 | 19 张 | Brand Story 轮播移动版 |

---

## 标准图片规划模板

典型 Amazon Listing 图片规划：

| ID | asset_type | 用途 |
|---|---|---|
| `secondary-01` | secondary_image | 核心卖点 / 价值主张 |
| `secondary-02` | secondary_image | 场景 / 痛点展示 |
| `secondary-03` | secondary_image | 功能拆解 / 结构图 |
| `secondary-04` | secondary_image | 尺寸 / 兼容性指南 |
| `secondary-05` | secondary_image | 使用步骤 / 应用场景 |
| `secondary-06` | secondary_image | 包装清单 / 配件 |
| `aplus-desktop-01` | aplus_desktop | 品牌开场 / 情感钩子 |
| `aplus-desktop-02` | aplus_desktop | 痛点 / 问题场景 |
| `aplus-desktop-03` | aplus_desktop | 核心技术 / 材质 |
| `aplus-desktop-04` | aplus_desktop | 细节卖点展示 |
| `aplus-desktop-05` | aplus_desktop | 使用场景 / 生活方式 |
| `aplus-desktop-06` | aplus_desktop | 对比 / 为什么选我们 |
| `aplus-desktop-07` | aplus_desktop | 售后 / 品牌承诺 |
| `aplus-mobile-01` | aplus_mobile | （同上，移动端重构构图） |
| ... | ... | （重复 7 个移动端模块） |

---

## Prompt 撰写规范

`prompt` 字段应是完整的英文图像生成 Prompt。遵循以下规则（详见 `references/prompt_guidelines.md`）：

1. **颜色必须用 HEX 码** — 不用形容词
2. **产品占比数字化** — 填写 `product_coverage_ratio`
3. **必须带 negative_prompt** — 根据图片类型选择对应模板
4. **认证/功效/性能表述必须有依据** — 无证明的写进 `claims_to_avoid`
5. **Prompt 结构标准化** — 主体→场景→光线→构图→质量→负面约束
6. **Style Lock 必须贯穿** — 多张图任务时，所有 Prompt 带入同一份 Style Lock

### Prompt 示例（副图 · 场景生活图）

```
A stainless steel pet water fountain (product body: #1E88E5 blue, 
spout: #FFD700 gold) placed on a light wood floor (#F5DEB3) 
in a modern living room. Natural morning sunlight (#FFF8DC) 
streaming from left, soft shadows. Product positioned right side 
40% frame coverage, vertically centered. Lifestyle photography, 
warm and inviting atmosphere, 8K, photorealistic, 
professional e-commerce.

Negative: no text, no fake logos, no watermark, 
no distorted shape, no unverified claims, no medical claims, 
no celebrity, no extra parts not in package.
```
