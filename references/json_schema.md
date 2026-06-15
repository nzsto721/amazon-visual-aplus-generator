# Image Plan JSON Schema

This document defines the JSON structure for `approved_image_plan.json`, the master plan file that maps every image to its visual script, generation parameters, and final sizing instructions.

## Top-Level Structure

```json
{
  "product_name": "Product name as in listing",
  "asin": "B0XXXXXXXXX (optional, for reference)",
  "generated_at": "ISO 8601 datetime",
  "images": [
    { "...": "image entry, see below" }
  ]
}
```

## Image Entry Schema

Each image in the `images` array follows this structure. All fields except `notes` are required.

```json
{
  "id": "secondary-01",
  "asset_type": "secondary_image",
  "module_position": 1,
  "final_size": {
    "width": 1200,
    "height": 1600
  },
  "generation_size": {
    "width": 1200,
    "height": 1600
  },
  "safe_area": "keep key text and product inside center 86% of generation canvas",
  "crop_strategy": "direct generation — 1200x1600 is already valid for GPT Image 2 (both dimensions ÷16)",
  "source_product_images": ["white_images/main-front.png"],
  "visual_goal": "explain the core benefit in one glance",
  "headline": "More Space, Less Mess",
  "subheadline": "Organize your kitchen in minutes",
  "icon_labels": ["No drilling", "Strong hold", "Easy clean"],
  "scene_description": "bright modern kitchen countertop, morning light",
  "composition": "product positioned right 40%, before/after scene on left, three icon badges at bottom",
  "tone_and_style": "modern clean, warm neutral tones, natural lighting",
  "text_placement": "headline top-left, subheadline below headline, icons bottom strip",
  "claims_to_avoid": ["unverified weight capacity", "medical-grade"],
  "prompt": "Full English image-generation prompt with all visual details",
  "notes": "Optional: any special instructions or context"
}
```

### Field-by-Field Reference

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique identifier for this image, e.g. `secondary-01`, `aplus-desktop-03` |
| `asset_type` | string | One of: `secondary_image`, `aplus_desktop`, `aplus_mobile`, `brand_story_desktop`, `brand_story_mobile` |
| `module_position` | int | Position in the module sequence (1-based) |
| `final_size` | object | `{width, height}` — Amazon upload size after cropping |
| `generation_size` | object | `{width, height}` — Canvas size passed to the image model |
| `safe_area` | string | Description of which area is safe from cropping |
| `crop_strategy` | string | How the generation output is cropped to final size |
| `source_product_images` | array | Paths to product white-background photos used as visual reference |
| `visual_goal` | string | One-line summary of what this image must communicate |
| `headline` | string | Main title text for the image (keep ≤5 words recommended) |
| `subheadline` | string | Supporting text below headline (≤10 words) |
| `icon_labels` | array | Short labels for icon badges (3-5 items) |
| `scene_description` | string | Full scene description: setting, lighting, mood, context |
| `composition` | string | Layout description: where things are positioned |
| `tone_and_style` | string | Visual style direction: color palette, photography style, mood |
| `text_placement` | string | Where text elements sit on the image |
| `claims_to_avoid` | array | Claims that must NOT appear in the image (unverified certs, health claims, etc.) |
| `prompt` | string | The complete image-generation prompt in English |
| `notes` | string | Optional: extra context for the reviewer |

## asset_type Values

| Value | Final Size | Module Limit | Description |
|---|---|---|---|
| `secondary_image` | 1200 × 1600 | Up to 6-9 images | Listing image block below main image |
| `aplus_desktop` | 1464 × 600 | 7 per page | A+ Content desktop module |
| `aplus_mobile` | 1600 × 1200 | 7 per page | A+ Content mobile module |
| `brand_story_desktop` | 1464 × 600 | 19 cards max | Brand story carousel desktop |
| `brand_story_mobile` | 1600 × 1200 | 19 cards max | Brand story carousel mobile |

## Standard Image Plan Template

A typical Amazon listing image plan:

| ID | asset_type | Purpose |
|---|---|---|
| `secondary-01` | secondary_image | Core benefit / hero proposition |
| `secondary-02` | secondary_image | Scene / pain point illustration |
| `secondary-03` | secondary_image | Feature breakdown / structure diagram |
| `secondary-04` | secondary_image | Dimensions / compatibility guide |
| `secondary-05` | secondary_image | Usage steps / application |
| `secondary-06` | secondary_image | What's in the box / accessories |
| `aplus-desktop-01` | aplus_desktop | Brand opening / emotional hook |
| `aplus-desktop-02` | aplus_desktop | Pain point / problem scenario |
| `aplus-desktop-03` | aplus_desktop | Core technology / material |
| `aplus-desktop-04` | aplus_desktop | Detailed feature showcase |
| `aplus-desktop-05` | aplus_desktop | Usage scenario / lifestyle |
| `aplus-desktop-06` | aplus_desktop | Comparison / why choose us |
| `aplus-desktop-07` | aplus_desktop | After-sales / brand promise |
| `aplus-mobile-01` | aplus_mobile | (same narrative, mobile-optimized) |
| ... | ... | (repeat for all 7 mobile modules) |

## Prompt Writing Guidelines

The `prompt` field should be a complete, detailed image-generation prompt in English. Follow these rules:

1. **Open with the product context**: Describe the product and its environment
2. **Specify the composition**: Mention positioning, layout, and visual hierarchy
3. **Include text elements**: If the image model supports text, specify exact headline/copy
4. **Define lighting and style**: Natural light vs studio, warm vs cool, lifestyle vs diagrammatic
5. **State what NOT to include**: Refer to `claims_to_avoid` for forbidden content
6. **End with technical parameters**: aspect ratio, resolution hint, output constraints

Example (abbreviated):
```
A clean kitchen countertop scene showing [product] on the right side 
in soft morning light. Left side shows a cluttered before-state with 
disorganized items. Three icon badges at bottom: drill-free installation, 
strong adhesive hold, easy to clean. Studio photography, warm natural 
tones, 3:4 portrait orientation. Product must match the reference 
white-background photo exactly. No unverified weight capacity claims, 
no medical-grade language.
```
