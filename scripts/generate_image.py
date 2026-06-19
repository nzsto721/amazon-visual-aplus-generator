#!/usr/bin/env python3
"""OpenAI-compatible image generation helper for amazon-visual-aplus-generator.

支持 OpenAI / gpt-image / 任意 OpenAI 兼容 API（国内大模型网关等）。

配置方式（优先级从高到低）：
1. 环境变量
2. .env 文件（脚本同级目录或 --env-file 指定）

环境变量：
  IMG_BASE_URL   API 基础地址，默认 https://api.openai.com/v1
  IMG_MODEL       模型名称，默认 gpt-image-1.5
  IMG_API_KEY     API Key（必填，除非使用 Prompt-only 模式）
  IMG_SIZE        生成尺寸，默认 1:1（也可用 1200x1600 等）
  IMG_QUALITY     质量，默认 auto（可选 low/medium/high）

使用方式：
  # Prompt-only 模式（不配置 API，只输出 Prompt 文本）
  python generate_image.py --prompt-only --prompt-file prompt.txt

  # API 模式：生成单张图
  python generate_image.py --prompt-file prompt.txt --output-dir outputs/

  # API 模式：批量从 JSON Plan 读取并生成
  python generate_image.py --plan approved_image_plan.json --output-dir outputs/
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def load_env_file(path: str | None) -> None:
    if not path:
        return
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8").strip()
    if args.prompt:
        return args.prompt.strip()
    raise SystemExit("请提供 --prompt 或 --prompt-file")


def generate_single(prompt: str, args: argparse.Namespace) -> str | None:
    """调用图像生成 API，返回本地文件路径或 None。"""
    base_url = os.getenv("IMG_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
    model = os.getenv("IMG_MODEL") or os.getenv("OPENAI_IMAGE_MODEL") or "gpt-image-1.5"
    api_key = os.getenv("IMG_API_KEY") or os.getenv("OPENAI_API_KEY")
    size = os.getenv("IMG_SIZE") or args.size or "1:1"
    quality = os.getenv("IMG_QUALITY") or args.quality or "auto"

    if not api_key:
        print("⚠️  未配置 IMG_API_KEY，跳过 API 调用。Prompt 已输出到控制台。")
        print(f"\n[Prompt]\n{prompt}\n")
        return None

    endpoint = base_url.rstrip("/") + "/images/generations"
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": 1,
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_text = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"图像 API 请求失败: {exc.code}\n{error_text}") from exc

    item = (data.get("data") or [{}])[0]
    b64 = item.get("b64_json")
    url = item.get("url")

    output_dir = Path(args.output_dir or "outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    if b64:
        out = output_dir / f"{args.output_name or 'image'}.png"
        out.write_bytes(base64.b64decode(b64))
        print(f"✅ 图像已保存: {out}")
        return str(out)

    if url:
        out = output_dir / f"{(args.output_name or 'image')}-url.txt"
        out.write_text(url, encoding="utf-8")
        print(f"✅ 图像 URL 已保存: {out}")
        return str(out)

    # 未知返回格式，保存原始响应
    out = output_dir / "response.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"⚠️  未知返回格式，原始响应已保存: {out}")
    return None


def generate_from_plan(plan_path: str, args: argparse.Namespace) -> None:
    """从 approved_image_plan.json 批量生成图片。"""
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    images = plan.get("images") or []
    if not images:
        raise SystemExit("JSON Plan 中未找到 images 字段")

    output_dir = Path(args.output_dir or "outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📋 从 Plan 读取 {len(images)} 张图片任务\n")

    for i, img in enumerate(images, 1):
        img_id = img.get("id", f"img-{i:02d}")
        prompt = img.get("prompt", "")
        negative = img.get("negative_prompt", "")
        size = img.get("generation_size", {})
        size_str = f"{size.get('width', 1024)}x{size.get('height', 1024)}" if size else "1:1"

        print(f"[{i}/{len(images)}] 生成: {img_id}")
        print(f"  Size: {size_str}")

        full_prompt = prompt
        if negative:
            full_prompt += f"\nNegative: {negative}"

        args_passthrough = argparse.Namespace(
            prompt=full_prompt,
            prompt_file=None,
            output_dir=str(output_dir),
            output_name=img_id,
            size=size_str,
            quality=args.quality or "auto",
            env_file=args.env_file,
            plan=None,
        )

        result = generate_single(full_prompt, args_passthrough)
        if result:
            print(f"  ✅ {result}")
        else:
            # API 未配置，把 Prompt 写到文件
            prompt_file = output_dir / f"{img_id}-prompt.txt"
            prompt_file.write_text(full_prompt, encoding="utf-8")
            print(f"  📝 Prompt 已保存（未调用 API）: {prompt_file}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Amazon 视觉策划 · 图像生成助手（支持 OpenAI 兼容 API）"
    )
    parser.add_argument("--prompt", help="图像 Prompt 文本")
    parser.add_argument("--prompt-file", help="包含 Prompt 的文本文件路径")
    parser.add_argument("--prompt-only", action="store_true", help="只输出 Prompt，不调用 API")
    parser.add_argument("--plan", help="从 approved_image_plan.json 批量生成")
    parser.add_argument("--output-dir", default="outputs", help="输出目录")
    parser.add_argument("--output-name", help="输出文件名（不含扩展名）")
    parser.add_argument("--env-file", default=".env", help=".env 文件路径")
    parser.add_argument("--size", default="1:1", help="生成尺寸（如 1200x1600 或 1:1）")
    parser.add_argument("--quality", default="auto", help="图像质量（low/medium/high/auto）")
    args = parser.parse_args()

    load_env_file(args.env_file)

    # Prompt-only 模式
    if args.prompt_only:
        prompt = read_prompt(args)
        print("=" * 60)
        print("📝 图像生成 Prompt（Prompt-only 模式）")
        print("=" * 60)
        print(prompt)
        print("=" * 60)
        print("\n将此 Prompt 复制到支持的图像生成工具即可。")
        return 0

    # 从 Plan 批量生成
    if args.plan:
        generate_from_plan(args.plan, args)
        return 0

    # 单张生成
    prompt = read_prompt(args)
    result = generate_single(prompt, args)
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
