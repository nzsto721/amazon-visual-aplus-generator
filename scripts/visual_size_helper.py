#!/usr/bin/env python3
"""
Amazon Visual Size Helper — handles image sizing for Amazon listing images.

Usage:
    # Plan mode: given a final target, suggest generation canvas size
    python visual_size_helper.py plan

    # Plan mode for a specific type
    python visual_size_helper.py plan --type aplus_desktop

    # Finalize mode: resize/crop an image to final Amazon upload size
    python visual_size_helper.py finalize --type aplus_desktop --input raw/aplus-01.png --output final/aplus-01.jpg

    # Batch finalize from a manifest
    python visual_size_helper.py finalize --manifest image_plan.json --input-dir raw/ --output-dir final/
"""

import argparse
import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Amazon official size specs + recommended generation canvas
# Generation size is chosen to be divisible by 16 (model-friendly)
# while keeping the safe area accurate.
# ---------------------------------------------------------------------------
SIZE_SPECS = {
    "secondary": {
        "final":       (1200, 1600),
        "generation":  (1200, 1600),  # 1200÷16=75, 1600÷16=100 — valid for GPT Image 2
        "description": "Secondary / lifestyle images for the image block"
    },
    "aplus_desktop": {
        "final":       (1464, 600),
        "generation":  (1488, 608),   # 1488÷16=93, 608÷16=38 — gen-safe then crop
        "description": "A+ Content desktop module image (7 modules max)",
        "note": "1464 and 600 are NOT divisible by 16 (GPT Image 2 constraint). Generate at 1488x608 then center-crop."
    },
    "aplus_mobile": {
        "final":       (1600, 1200),
        "generation":  (1600, 1200),  # 1600÷16=100, 1200÷16=75 — valid for GPT Image 2
        "description": "A+ Content mobile module image (7 modules max)"
    },
    "brand_story_desktop": {
        "final":       (1464, 600),
        "generation":  (1488, 608),
        "description": "Brand story desktop module",
        "note": "Same ÷16 constraint as A+ desktop."
    },
    "brand_story_mobile": {
        "final":       (1600, 1200),
        "generation":  (1600, 1200),
        "description": "Brand story mobile module"
    },
}

# Safe area: how much of the generation canvas is "safe" (content won't be cropped)
SAFE_AREA_RATIO = 0.86  # keep key elements inside center 86%


def plan(args):
    """Print size plan — recommended generation size vs final upload size."""
    if args.type:
        specs = [SIZE_SPECS[args.type]]
    else:
        specs = list(SIZE_SPECS.values())

    print(f"{'Type':<22} {'Final (W×H)':<16} {'Gen Canvas (W×H)':<18} {'Safe Area':<12}")
    print("-" * 68)
    for spec in specs:
        fw, fh = spec["final"]
        gw, gh = spec["generation"]
        safe_w = int(gw * SAFE_AREA_RATIO)
        safe_h = int(gh * SAFE_AREA_RATIO)
        name = [k for k, v in SIZE_SPECS.items() if v is spec][0]
        print(f"{name:<22} {fw}×{fh:<10} {gw}×{gh:<12} {safe_w}×{safe_h}")
        if spec.get("note"):
            print(f"  >> {spec['note']}")


def finalize_single(args):
    """Resize and crop a single image to final Amazon size."""
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow is required. Install with: pip install Pillow")
        sys.exit(1)

    spec = SIZE_SPECS.get(args.type)
    if not spec:
        print(f"ERROR: Unknown type '{args.type}'. Valid types: {list(SIZE_SPECS.keys())}")
        sys.exit(1)

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.open(input_path).convert("RGB")
    orig_w, orig_h = img.size
    target_w, target_h = spec["final"]

    print(f"Input:  {orig_w}×{orig_h} → Target: {target_w}×{target_h} ({args.type})")

    # Strategy: scale so the SHORTER dimension matches target, then crop the longer one
    target_ratio = target_w / target_h
    img_ratio = orig_w / orig_h

    if img_ratio > target_ratio:
        # Image is wider than target — scale by height
        new_h = target_h
        new_w = int(target_h * img_ratio)
    else:
        # Image is taller than target — scale by width
        new_w = target_w
        new_h = int(target_w / img_ratio)

    img = img.resize((new_w, new_h), Image.LANCZOS)

    # Center crop
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))

    # Save as high-quality JPEG
    img.save(str(output_path), "JPEG", quality=95)
    print(f"Output: {output_path} ({target_w}×{target_h})")


def finalize_batch(args):
    """Batch finalize from an image_plan.json manifest."""
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow is required. Install with: pip install Pillow")
        sys.exit(1)

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found: {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        plan_data = json.load(f)

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    images = plan_data.get("images", [])
    if not images:
        print("No images found in manifest.")
        return

    success = 0
    for img_entry in images:
        img_id = img_entry.get("id", "unknown")
        asset_type = img_entry.get("asset_type", "secondary_image")

        # Map asset_type to size spec
        type_map = {
            "secondary_image": "secondary",
            "aplus_desktop": "aplus_desktop",
            "aplus_mobile": "aplus_mobile",
            "brand_story_desktop": "brand_story_desktop",
            "brand_story_mobile": "brand_story_mobile",
        }
        spec_key = type_map.get(asset_type)
        if not spec_key:
            print(f"  SKIP {img_id}: unknown asset_type '{asset_type}'")
            continue

        spec = SIZE_SPECS[spec_key]
        input_file = input_dir / f"{img_id}.png"
        output_file = output_dir / f"{img_id}.jpg"

        if not input_file.exists():
            input_file = input_dir / f"{img_id}.jpg"
        if not input_file.exists():
            print(f"  SKIP {img_id}: input file not found")
            continue

        try:
            img = Image.open(input_file).convert("RGB")
            orig_w, orig_h = img.size
            target_w, target_h = spec["final"]

            target_ratio = target_w / target_h
            img_ratio = orig_w / orig_h

            if img_ratio > target_ratio:
                new_h = target_h
                new_w = int(target_h * img_ratio)
            else:
                new_w = target_w
                new_h = int(target_w / img_ratio)

            img = img.resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - target_w) // 2
            top = (new_h - target_h) // 2
            img = img.crop((left, top, left + target_w, top + target_h))
            img.save(str(output_file), "JPEG", quality=95)

            print(f"  OK   {img_id}: {orig_w}×{orig_h} → {target_w}×{target_h} ({spec_key})")
            success += 1
        except Exception as e:
            print(f"  FAIL {img_id}: {e}")

    print(f"\nDone: {success}/{len(images)} images processed.")


def main():
    parser = argparse.ArgumentParser(
        description="Amazon Visual Size Helper — plan and finalize image sizes"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Plan command
    plan_parser = subparsers.add_parser("plan", help="Show recommended generation canvas sizes")
    plan_parser.add_argument("--type", choices=list(SIZE_SPECS.keys()),
                             help="Show only one type (omit for all)")

    # Finalize command (single)
    finalize_parser = subparsers.add_parser("finalize", help="Crop/resize one image to final size")
    finalize_parser.add_argument("--type", required=True, choices=list(SIZE_SPECS.keys()))
    finalize_parser.add_argument("--input", required=True, help="Path to generated image")
    finalize_parser.add_argument("--output", required=True, help="Output path for sized image")

    # Batch finalize
    batch_parser = subparsers.add_parser("batch", help="Batch finalize from image_plan.json")
    batch_parser.add_argument("--manifest", required=True, help="Path to image_plan.json")
    batch_parser.add_argument("--input-dir", required=True, help="Directory containing generated images")
    batch_parser.add_argument("--output-dir", required=True, help="Output directory for sized images")

    args = parser.parse_args()

    if args.command == "plan":
        plan(args)
    elif args.command == "finalize":
        finalize_single(args)
    elif args.command == "batch":
        finalize_batch(args)


if __name__ == "__main__":
    main()
