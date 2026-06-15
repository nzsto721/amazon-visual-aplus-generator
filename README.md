# Amazon Visual & A+ Generator — WorkBuddy Skill

一套 Codex Skill 跑完亚马逊副图 + A+ 全流程：从市场调研、视觉策划、JSON 脚本到生图裁切。

## 它做什么

| 阶段 | 说明 |
|---|---|
| ① 输入验证 | 检查产品文件夹（product_info.md + 白底图）是否齐全 |
| ② 联网调研 | 调研类目、人群、竞品图片、评论痛点 |
| ③ 策划方案 | 输出副图 + A+ 策划草案，**等你确认才生图** |
| ④ JSON 细化 | 把每张图拆成标题、副标题、图标、构图、尺寸、Prompt |
| ⑤ 生图 + 裁切 | 调用图像模型生成，裁切为 Amazon 合规尺寸 |

## 核心原则

- **主图绝不凭空生成** — 只审计白底图合规性
- **确认闸门** — 策划方案必须等你确认后才生图
- **所有认证/功效/性能表述必须有依据** — 没验证的不写进 Prompt

## 需要你准备什么

```
my-product/
├── product_info.md        # 标题、五点、描述、认证（必填）
├── white_images/          # 产品白底图（必填，至少 1 张）
│   ├── main-front.png
│   └── main-side.png
├── brand_assets/          # 品牌 Logo + 色板（选填）
└── requirements.md        # 特殊需求（选填）
```

## 怎么用

在 WorkBuddy 中把 Skill 放到 `~/.workbuddy/skills/amazon-visual-aplus-generator/`，然后：

```
用 amazon-visual-aplus-generator 给这个产品策划副图和 A+：C:\my-product
```

## 输出尺寸

| 类型 | 最终尺寸 | 生成画布 |
|---|---|---|
| 副图 (Secondary) | 1200 × 1600 | 1200 × 1600 |
| A+ 桌面版 | 1464 × 600 | 1488 × 608 |
| A+ 移动版 | 1600 × 1200 | 1600 × 1200 |

## 文件结构

```
amazon-visual-aplus-generator/
├── SKILL.md                          # WorkBuddy Skill 主文件
├── README.md                         # 本文件
├── .gitignore
├── scripts/
│   └── visual_size_helper.py         # 尺寸处理脚本 (plan / finalize / batch)
└── references/
    ├── amazon_image_specs.md          # Amazon 图片规范参考（含 GPT Image 2 约束）
    └── json_schema.md                 # approved_image_plan.json Schema 定义
```

## 依赖

`visual_size_helper.py` 需要 Pillow：

```bash
pip install Pillow
```

## 许可证

MIT
