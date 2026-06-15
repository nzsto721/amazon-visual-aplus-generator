---
name: amazon-visual-aplus-generator
description: Amazon product visual strategy and A+ image generation workflow. This skill should be used when the user needs to plan secondary images and A+ content for an Amazon listing, generate detailed visual scripts, and produce sized images. Triggers include: planning Amazon images, creating A+ content, generating product lifestyle images, Amazon visual strategy, or when the user provides a product folder with product_info.md and white_images. Key principle: NEVER generate images without user confirmation of the visual strategy draft. ALWAYS require the user to verify product facts, certifications, and claims before image generation.
agent_created: true
---

# Amazon Visual & A+ Generator

## Overview

A 5-phase workflow that takes a product folder (product info + white-background photos) through research, visual strategy planning, execution-ready JSON scripting, AI image generation, and size-correct finalization — with a mandatory confirmation gate between strategy and generation.

This skill does NOT replace a designer. It acts as a visual-strategy assistant that understands Amazon conversion logic: which purchase anxieties each image should resolve, how to structure a 6-secondary-image + 7-module-A+ narrative, and how to produce size-compliant final assets.

## When to Use

Trigger when the user:

- Says "plan Amazon images for this product"
- Provides a folder path with `product_info.md` and `white_images/`
- Mentions "副图", "A+", "图片策划", "视觉方案", "Amazon visual", "listing images"
- Asks to generate product lifestyle/feature/comparison images for Amazon
- References the skill name directly: `amazon-visual-aplus-generator`

## Core Principle: Two-Phase, Confirmation-Gated

The workflow is split by a hard gate. Phase 1 outputs a strategy document — no images. The user must explicitly confirm (e.g., "确认", "approved", "go ahead") before Phase 2 begins.

**Why**: Visual direction errors are costly. Generating 20 images on a wrong strategy wastes time and API calls. The gate ensures human judgment on product facts, brand tone, and regulatory claims before any pixel is created.

## Workflow

### Phase 0 — Input Validation

Before anything else, validate the product folder structure:

```
product-folder/
├── product_info.md        # Required: title, bullets, description, features, certifications
├── white_images/          # Required: at least one product white-background photo
│   ├── main-front.png
│   └── main-side.png
├── brand_assets/          # Optional: logo, brand colors, style guide
│   ├── logo.png
│   └── brand-colors.md
└── requirements.md        # Optional: user's specific requests or constraints
```

**Required checks:**

1. Read `product_info.md` — extract: title, five bullet points, product description, key features, target audience, usage scenarios, verified certifications, and any forbidden claims.
2. If `product_info.md` is missing or sparse, prompt the user to provide at minimum: title, 5 bullets, core features, and any verified certifications.
3. List the files in `white_images/`. If empty, prompt for at least one product white-background photo.
4. If `requirements.md` exists, read it for user-specified constraints (specific scenes, must-include features, forbidden imagery).
5. If `brand_assets/` exists, note available brand assets.

### Phase 1 — Research & Draft Strategy (NO IMAGES)

#### Step 1: Market Research

Conduct web research to understand the product's category context. Use WebSearch to investigate:

| Research area | What to extract |
|---|---|
| Category norms | Common price range, feature expressions, typical image styles |
| Target audience | Who buys, why they buy, what triggers purchase |
| Competitor images | How top listings structure their images, which images are reused patterns, which are unique |
| Review pain points | From competitor reviews: what do buyers complain about? Can these be addressed visually? |
| Regulatory sensitivity | Any certifications commonly shown (but possibly unverified), any claims frequently made |

**Output**: A concise research summary (one paragraph per area above) included in the strategy draft.

#### Step 2: Draft Visual Strategy

Produce a structured strategy document covering:

**A. Main Image Audit**
Check the provided white-background image(s) against Amazon requirements:
- Is the background pure white (RGB 255,255,255)?
- Does the product fill ≥85% of the frame?
- Are there any text, logos, props, or items not in the purchase?
- Is the image ≥1600px on the longest side for zoom?

**B. Secondary Image Plan (6 images recommended)**

For each position, define:
- **Purpose**: Which purchase anxiety or question does this image resolve?
- **Visual approach**: Scene, diagram, comparison, or lifestyle
- **Key message**: The one thing the buyer should understand

Standard structure template:

| # | Type | Purpose |
|---|---|---|
| 1 | Core benefit | One-glance value proposition — what makes this product worth buying |
| 2 | Scene / pain point | The problem it solves, shown in real context |
| 3 | Feature breakdown | Structure, materials, technology, key specs |
| 4 | Dimensions / compatibility | Size reference, fit guide, compatibility chart |
| 5 | Usage / application | How to use it, step-by-step or scenario |
| 6 | Package contents | What's in the box, accessories, to reduce post-purchase confusion |

**C. A+ Content Plan (7 modules)**

Standard narrative arc:

| Module | Focus |
|---|---|
| 1 | Brand opening / emotional hook — why this brand exists |
| 2 | Pain point / problem — the situation before the product |
| 3 | Core technology / material — what makes it different |
| 4 | Detailed feature showcase — zoom into specific advantages |
| 5 | Usage scenario / lifestyle — the product in daily life |
| 6 | Comparison / why choose us — vs alternatives or old ways |
| 7 | After-sales / brand promise — warranty, support, trust signals |

Both desktop (1464×600) and mobile (1600×1200) versions noted for each module.

**D. Compliance & Risk Notes**

Flag any concerns:
- Claims that would need verification before being used in images
- Certification logos that must be proven
- Regulatory sensitivity (health, safety, environmental claims)

#### Step 3: Present & Wait for Confirmation

Format the strategy as a clean, readable plan. End with an explicit request for confirmation:

> This is the draft visual strategy. Review and confirm before image generation begins.
> Reply "确认" to proceed, or specify adjustments (e.g., "Change image 3 to focus on installation, not materials").

**CRITICAL**: Do NOT proceed to Phase 2 until the user explicitly confirms. If the user requests changes, revise the strategy and present again.

### Phase 2 — JSON Plan & Image Generation

**Only execute after user confirmation.**

#### Step 4: Generate Detailed JSON Plan

Create `approved_image_plan.json` following the schema in `references/json_schema.md`. Load this reference file for the complete field definitions.

Key rules when building the JSON:

1. **Every image gets a complete entry** — headline, subheadline, icon_labels, scene, composition, tone, claims_to_avoid, and prompt.
2. **prompt is written in English** — detailed, specific, referencing the product white-background photo as visual reference.
3. **claims_to_avoid must be non-empty** — always include regulatory-sensitive items even if not applicable (e.g., "unverified medical claims", "unverified certifications").
4. **generation_size respects the ÷16 rule** — use size specs from `references/amazon_image_specs.md`:

| Asset type | Final (W×H) | Gen Canvas (W×H) |
|---|---|---|
| secondary_image | 1200 × 1600 | 1200 × 1600 |
| aplus_desktop | 1464 × 600 | 1488 × 608 |
| aplus_mobile | 1600 × 1200 | 1600 × 1200 |

Write the JSON to the product folder as `approved_image_plan.json`. Present a summary table of all images to the user for final review.

#### Step 5: Generate Images

For each image in the plan, in order:

1. **Load the ImageGen tool schema**: Use ToolSearch with `tool_names: ["ImageGen"]`.
2. **Call ImageGen**: Use DeferExecuteTool with the `prompt` field from the JSON entry.
3. **Save the generated image**: Save to `product-folder/generated/{image-id}.png`.
4. **Log progress**: Report successes and any failures.

**Important constraints:**
- Generate images sequentially (one at a time) to maintain quality control.
- If an image fails (tool error, quality issue), retry once with a refined prompt.
- Main image (primary) is NEVER generated from scratch — only audit the white-background photo.
- If a generated image visibly alters the product appearance (wrong shape, color, details), flag it for the user.

#### Step 6: Finalize Sizes

After all images are generated, run the size finalization script:

```bash
python scripts/visual_size_helper.py batch \
  --manifest approved_image_plan.json \
  --input-dir generated/ \
  --output-dir final/
```

This crops and resizes each image to Amazon's exact upload dimensions.

If the batch script fails for individual images, use the single-image command for each:

```bash
python scripts/visual_size_helper.py finalize \
  --type aplus_desktop \
  --input generated/aplus-desktop-01.png \
  --output final/aplus-desktop-01.jpg
```

#### Step 7: Deliver Output

Present the user with:

1. **Summary table**: All generated images with their type, size, and status
2. **Output directory**: `product-folder/final/` containing sized images ready for upload
3. **Compliance checklist**: Remind the user of pre-upload checks (reference `references/amazon_image_specs.md`):

- [ ] Product appearance matches reality (AI did not alter it)
- [ ] No false certifications or unverified claims
- [ ] All text on images has correct spelling and grammar
- [ ] Mobile thumbnails are readable
- [ ] Main image meets all Amazon requirements
- [ ] A+ modules have both desktop and mobile versions

## Bundled Resources

### scripts/visual_size_helper.py

Handles image sizing and cropping. Three commands:

- `plan` — Show generation canvas vs final upload size for all Amazon image types
- `finalize` — Resize and crop one image to a specific Amazon size
- `batch` — Batch process all images from an `approved_image_plan.json` manifest

Requires Pillow (`pip install Pillow`).

### references/amazon_image_specs.md

Complete reference for Amazon image requirements: main image rules, secondary image specs, A+ module types and sizes, compliance checklist. Load when checking image compliance or when the user asks about Amazon image rules.

### references/json_schema.md

Full field-by-field schema for `approved_image_plan.json`. Load when building the detailed image plan in Phase 2. Includes standard image plan templates and prompt writing guidelines.

## Important Constraints

- **NEVER generate the main (primary) image** from scratch. The main image must be a real product photo on white background. Only audit it for compliance.
- **NEVER include unverified claims** in any image prompt. If the user mentions a certification, efficacy claim, or performance metric, ask: "Is this verified? Do you have documentation?"
- **ALWAYS write image prompts in English**, as image generation models perform best with English prompts.
- **ALWAYS confirm the draft strategy** before generating any images. This is non-negotiable.
- **Mobile A+ images may need different compositions** than desktop versions. Text that is readable at 1464×600 may be unreadable at phone width. Adjust font sizes and layouts accordingly.
- **The product in generated images must match the white-background photo** as closely as possible in shape, color, and detail. If the model alters the product, flag it.
