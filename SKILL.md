---
name: amazon-visual-aplus-generator
description: Amazon product visual strategy and A+ image generation workflow (v2). Template-based, style-locked, prompt-guided. Triggers: plan Amazon images, create A+ content, generate product images, "副图", "A+", "图片策划", amazon visual, listing images, or direct skill name reference. Core rule: NEVER generate images without user confirmation of the visual strategy draft. ALWAYS verify product facts, certifications, and claims before image generation.
agent_created: true
version: "2.0"
---

# Amazon Visual & A+ Generator · v2

## Overview

A 5-phase workflow that takes a product folder through research, visual strategy planning, template-matched scripting, style-locked JSON planning, AI image generation, and size-correct finalization — with a mandatory confirmation gate between strategy and generation.

v2 adds: **template system** (25 image-type JSON templates), **Style Lock** (campaign-wide consistency), **Prompt 铁律** (HEX colors, product ratio, negative_prompt), and **OpenAI-compatible API support**.

This skill does NOT replace a designer. It is a visual-strategy assistant that understands Amazon conversion logic.

---

## When to Use

Trigger when the user:
- Says "plan Amazon images for this product" or equivalent
- Provides a folder path with `product_info.md` and `white_images/`
- Mentions "副图", "A+", "图片策划", "视觉方案", "Amazon visual", "listing images"
- Asks to generate product lifestyle/feature/comparison images for Amazon
- References the skill name directly: `amazon-visual-aplus-generator`

---

## Core Principle: Two-Phase, Confirmation-Gated

The workflow is split by a hard gate. Phase 1 outputs a strategy document — no images. The user must explicitly confirm before Phase 2 begins.

**Why**: Visual direction errors are costly. The gate ensures human judgment on product facts, brand tone, and regulatory claims before any pixel is created.

---

## Workflow

### Phase 0 — Input Validation & Template Matching

#### Step 0.1: Validate Product Folder

```
product-folder/
├── product_info.md        # Required
├── white_images/          # Required: at least one white-background photo
│   ├── main-front.png
│   └── main-side.png
├── brand_assets/          # Optional: logo, brand colors
│   ├── logo.png
│   └── brand-colors.md
└── requirements.md        # Optional: specific requests
```

**Required checks:**
1. Read `product_info.md` — extract: title, five bullets, description, key features, target audience, usage scenarios, verified certifications, forbidden claims.
2. If missing/sparse, prompt user for at minimum: title, 5 bullets, core features, verified certifications.
3. List `white_images/` files. If empty, prompt for at least one white-background photo.
4. If `requirements.md` exists, read for constraints.
5. If `brand_assets/` exists, note available assets.

#### Step 0.2: Match Image Types to Templates

After reading `product_info.md`, match each planned image to a template in `templates/`. Load the matching template JSON to guide Prompt construction.

**Matching reference:**

| Amazon Image | Recommended Template | Template File |
|---|---|---|
| Main image (audit only) | Hero image | `01-hero-image.json` |
| Secondary 1: Core benefit | Hero image / Lifestyle | `01-hero-image.json` / `02-lifestyle-scene.json` |
| Secondary 2: Scene/pain point | Lifestyle scene | `02-lifestyle-scene.json` |
| Secondary 3: Feature breakdown | Infographic / Exploded view | `11-infographic.json` / `17-exploded-view.json` |
| Secondary 4: Dimensions | Size spec | `13-size-spec.json` |
| Secondary 5: Usage steps | Lifestyle / Infographic | `02-lifestyle-scene.json` / `11-infographic.json` |
| Secondary 6: Package contents | Flat lay / Packaging | `03-flat-lay.json` / `10-packaging.json` |
| A+ Module (any) | Infographic | `11-infographic.json` |
| Before/After show | Before-after | `09-before-after.json` |
| Premium/luxury positioning | Luxury atmospherics | `22-luxury-atmospherics.json` |

Load the matched template(s) from `templates/` directory. Use the `prompt_template`, `defaults`, and `category_tips` from the template to construct each image's Prompt.

---

### Phase 1 — Research & Draft Strategy (NO IMAGES)

#### Step 1.1: Market Research

Conduct web research. Use WebSearch to investigate:

| Research area | What to extract |
|---|---|
| Category norms | Common price range, feature expressions, typical image styles |
| Target audience | Who buys, why they buy, what triggers purchase |
| Competitor images | How top listings structure images, which are unique |
| Review pain points | From competitor reviews: complaints that can be addressed visually |
| Regulatory sensitivity | Certifications commonly shown, claims frequently made |

**Output**: A concise research summary (one paragraph per area) included in the strategy draft.

#### Step 1.2: Draft Visual Strategy

Produce a structured strategy document covering:

**A. Main Image Audit**
Check provided white-background image(s) against Amazon requirements:
- Is background pure white (RGB 255,255,255)?
- Does product fill ≥85% of frame?
- Any text, logos, props, or items not in purchase?
- Image ≥1600px on longest side?

**B. Style Lock Draft**

Before detailing each image, propose a **Style Lock** for the entire campaign. Present to user for confirmation:

```json
Style Lock (draft):
  color_palette_hex:
    primary:    [to be determined from product/brand]
    accent:      [to be determined]
    background:  ["#FFFFFF", "#F5F1E8"]
    text:        "#1A1A1A"
  lighting:       [natural morning light / studio / warm indoor]
  layout_logic:  [product right, text left / centered / etc.]
  icon_style:    [outline 2px / filled / etc.]
  font_mood:     [clean sans-serif / elegant serif / etc.]
  negative_prompt_base: [standard list]
```

**C. Secondary Image Plan (6 images recommended)**

For each position, define:
- **Template**: Which `templates/*.json` to use
- **Purpose**: Which purchase anxiety this resolves
- **Visual approach**: Scene, diagram, comparison, lifestyle
- **Key message**: One thing the buyer should understand
- **Product coverage**: Percentage range (see `references/prompt_guidelines.md` 铁律二)

Standard structure template:

| # | Type | Template | Purpose |
|---|---|---|---|
| 1 | Core benefit | `01-hero-image` | One-glance value proposition |
| 2 | Scene/pain point | `02-lifestyle-scene` | Problem it solves, real context |
| 3 | Feature breakdown | `11-infographic` | Structure, materials, technology |
| 4 | Dimensions/compat | `13-size-spec` | Size reference, fit guide |
| 5 | Usage/application | `02-lifestyle-scene` | How to use, scenario |
| 6 | Package contents | `10-packaging` | What's in box, reduce confusion |

**D. A+ Content Plan (7 modules)**

Standard narrative arc:

| Module | Template | Focus |
|---|---|---|
| 1 | `02-lifestyle-scene` | Brand opening / emotional hook |
| 2 | `02-lifestyle-scene` | Pain point / problem scenario |
| 3 | `11-infographic` | Core technology / material |
| 4 | `11-infographic` | Detailed feature showcase |
| 5 | `02-lifestyle-scene` | Usage scenario / lifestyle |
| 6 | `11-infographic` | Comparison / why choose us |
| 7 | `02-lifestyle-scene` | After-sales / brand promise |

Both desktop (1464×600) and mobile (1600×1200) noted for each module. Mobile versions may need different compositions (text larger, product more centered).

**E. Compliance & Risk Notes**

Flag any concerns:
- Claims needing verification
- Certification logos requiring proof
- Regulatory sensitivity (health, safety, environmental)

#### Step 1.3: Present & Wait for Confirmation

Format strategy as a clean, readable plan. End with explicit request for confirmation:

> This is the draft visual strategy. Review and confirm before image generation begins.
> Reply "确认" to proceed, or specify adjustments.

**CRITICAL**: Do NOT proceed to Phase 2 until user explicitly confirms.

---

### Phase 2 — JSON Plan & Image Generation

**Only execute after user confirmation.**

#### Step 2.1: Finalize Style Lock

User confirmed strategy → write finalized `style_lock` object. This object will be referenced by every image entry in the JSON plan.

#### Step 2.2: Generate Detailed JSON Plan

Create `approved_image_plan.json` following the schema in `references/json_schema.md` (v2). Load this reference file for complete field definitions.

**Key rules when building the JSON (v2 additions):**

1. **Every image gets a complete entry** — all fields in the v2 schema.
2. **Match to template** — set `template_id` to the matched template file name (without `.json`).
3. **Apply Style Lock** — set `style_lock_ref` to the confirmed version; set `style_lock_deviation` to `"none"` or explain any reasonable adjustment.
4. **Prompt written in English** — detailed, specific, referencing product white-background photo.
5. **Colors in HEX code** — per 铁律一, no color adjectives.
6. **Product coverage digitized** — set `product_coverage_ratio` per 铁律二.
7. **negative_prompt required** — per 铁律三, include standard negative constraints.
8. **claims_to_avoid non-empty** — always include regulatory-sensitive items.
9. **generation_size respects ÷16 rule** — use size specs from `references/amazon_image_specs.md`.

Load `references/prompt_guidelines.md` when constructing Prompts — follow all 7 铁律.

Size reference:

| Asset type | Final (W×H) | Gen Canvas (W×H) |
|---|---|---|
| secondary_image | 1200 × 1600 | 1200 × 1600 |
| aplus_desktop | 1464 × 600 | 1488 × 608 |
| aplus_mobile | 1600 × 1200 | 1600 × 1200 |

Write JSON to product folder as `approved_image_plan.json`. Present summary table to user.

#### Step 2.3: Generate Images

For each image in the plan, in order:

1. **Load template** — read `templates/{template_id}.json` for `prompt_template`, `examples`, `anti_ai_tips`.
2. **Assemble Prompt** — combine: product description + scene + lighting + composition + quality tags + `negative_prompt`. Follow Prompt 铁律 (see `references/prompt_guidelines.md`).
3. **Call image generation** — two modes available:
   - **API mode**: Use `scripts/generate_image.py` with OpenAI-compatible API
   - **Tool mode**: Use ImageGen tool (if available in current environment)
4. **Save generated image** — save to `product-folder/generated/{image-id}.png`.
5. **Log progress** — report successes and failures.

**Important constraints:**
- Generate sequentially (one at a time).
- If an image fails, retry once with refined prompt.
- **Main image is NEVER generated from scratch** — only audit white-background photo.
- If generated image visibly alters product appearance, flag it.

#### Step 2.4: Finalize Sizes

After all images generated, run size finalization:

```bash
python scripts/visual_size_helper.py batch \
  --manifest approved_image_plan.json \
  --input-dir generated/ \
  --output-dir final/
```

If batch fails for individual images, use single-image command:

```bash
python scripts/visual_size_helper.py finalize \
  --type aplus_desktop \
  --input generated/aplus-desktop-01.png \
  --output final/aplus-desktop-01.jpg
```

#### Step 2.5: Deliver Output

Present user with:

1. **Summary table**: All generated images with type, size, status
2. **Output directory**: `product-folder/final/` containing upload-ready images
3. **Compliance checklist** (from `references/amazon_image_specs.md`):
   - [ ] Product appearance matches reality (AI did not alter it)
   - [ ] No false certifications or unverified claims
   - [ ] All text on images has correct spelling
   - [ ] Mobile thumbnails are readable
   - [ ] Main image meets all Amazon requirements
   - [ ] A+ modules have both desktop and mobile versions
   - [ ] Colors in final images match HEX codes in plan
   - [ ] Style Lock consistency maintained across all images

---

## Bundled Resources

### templates/ (v2 NEW)

25 image-type JSON templates, each containing:
- `prompt_template` — Prompt skeleton
- `defaults` — default parameters
- `variants` — style variants (luxury/fresh/tech/color)
- `category_tips` — per-category customization tips
- `examples` — reference Prompts
- `supports_image_reference` — whether reference image is supported

### scripts/visual_size_helper.py

Handles image sizing and cropping. Three commands: `plan`, `finalize`, `batch`. Requires Pillow.

### scripts/generate_image.py (v2 NEW)

OpenAI-compatible image generation helper. Supports:
- `--prompt-only` — output Prompt without API call (Prompt-only mode)
- `--plan` — batch generate from `approved_image_plan.json`
- `--env-file` — read API config from `.env` file

Configure via environment variables: `IMG_BASE_URL`, `IMG_MODEL`, `IMG_API_KEY`.

### references/amazon_image_specs.md

Complete Amazon image requirements: main image rules, secondary specs, A+ module types and sizes, compliance checklist.

### references/json_schema.md (v2 UPDATED)

Full field-by-field schema for `approved_image_plan.json` (v2). Includes `style_lock`, `negative_prompt`, `product_coverage_ratio`, and all new fields.

### references/prompt_guidelines.md (v2 NEW)

Prompt 铁律 — 7 rules every Prompt must follow: HEX colors, product ratio, negative_prompt, claims verification, Prompt structure, Style Lock, main image rule.

---

## Important Constraints

- **NEVER generate the main (primary) image** from scratch. Must be real product photo on white background. Only audit for compliance.
- **NEVER include unverified claims** in any image prompt. Ask: "Is this verified? Do you have documentation?"
- **ALWAYS write image prompts in English** — image models perform best with English prompts.
- **ALWAYS confirm the draft strategy** before generating any images. Non-negotiable.
- **ALWAYS use HEX codes for colors** — no color adjectives (参考 铁律一).
- **ALWAYS include negative_prompt** — per 铁律三.
- **Mobile A+ images need different compositions** than desktop. Adjust font sizes and layouts.
- **Product in generated images must match white-background photo** in shape, color, and detail. Flag alterations.
- **Style Lock must be consistent** across all images in a campaign. Deviations must be explicitly justified.
