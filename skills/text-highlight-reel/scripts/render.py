# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""Render a highlight-reel video given an image and either a quote or explicit line rectangles.

Usage:
    uv run render.py --image /path/to/source.png --quote "the sentence to highlight" \
                     --out /path/to/out.mp4 [--duration 6]

    uv run render.py --image /path/to/source.png \
                     --lines '[{"x":40,"y":430,"w":1440,"h":50}]' \
                     --out /path/to/out.mp4

Requires: node/npm, Swift (preinstalled on macOS) when using --quote.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "remotion-project"
CACHE_DIR = Path.home() / ".cache" / "text-highlight-reel-project"


def ensure_project():
    """Copy the template to a stable cache dir and install deps once."""
    if not CACHE_DIR.exists():
        shutil.copytree(TEMPLATE_DIR, CACHE_DIR)
    else:
        # Refresh source files in case the skill was updated
        for sub in ("src", "remotion.config.ts", "tsconfig.json", "package.json"):
            s = TEMPLATE_DIR / sub
            d = CACHE_DIR / sub
            if s.is_dir():
                shutil.rmtree(d, ignore_errors=True)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
    (CACHE_DIR / "public").mkdir(exist_ok=True)
    if not (CACHE_DIR / "node_modules").exists():
        print("installing remotion dependencies (first run only)…", file=sys.stderr)
        subprocess.check_call(["npm", "install", "--silent"], cwd=CACHE_DIR)


def get_lines(args) -> list[dict]:
    if args.lines:
        return json.loads(args.lines)
    if args.quote:
        out = subprocess.check_output(
            ["uv", "run", str(SKILL_DIR / "scripts" / "find_boxes.py"),
             args.image, args.quote],
        )
        data = json.loads(out)
        if not data.get("lines"):
            raise SystemExit(f"could not locate quote in image: {data.get('error')}")
        return data["lines"]
    raise SystemExit("provide either --quote or --lines")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--quote", help="phrase to highlight (OCR will locate it)")
    ap.add_argument("--lines", help="JSON list of {x,y,w,h} rectangles")
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=6.0)
    ap.add_argument("--blur-radius", type=float, default=10)
    args = ap.parse_args()

    image = Path(args.image).expanduser().resolve()
    if not image.exists():
        raise SystemExit(f"image not found: {image}")
    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    ensure_project()

    # Copy image into public/ with a deterministic name to keep cache stable
    img_dest = CACHE_DIR / "public" / "source.png"
    shutil.copy2(image, img_dest)

    lines = get_lines(args)
    print(f"highlighting {len(lines)} line(s): {lines}", file=sys.stderr)

    from PIL import Image as _Img
    with _Img.open(img_dest) as im:
        iw, ih = im.size

    props = {
        "imageSrc": "source.png",
        "imageWidth": iw,
        "imageHeight": ih,
        "lines": lines,
        "durationSeconds": args.duration,
        "blurRadius": args.blur_radius,
    }

    cmd = [
        "npx", "remotion", "render",
        "src/index.ts", "Highlight", str(out),
        "--props", json.dumps(props),
    ]
    subprocess.check_call(cmd, cwd=CACHE_DIR)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
