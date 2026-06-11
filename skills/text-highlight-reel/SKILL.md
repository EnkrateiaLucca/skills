---
name: text-highlight-reel
description: Render a short MP4/GIF that takes a screenshot of a page of text (PDF screenshot, article screenshot, book scan, etc.) and animates a yellow marker-style highlight over a specific quote while blurring the surrounding text. Built on Remotion (CSS blur + mix-blend-mode multiply marker + feathered sharp reveal). Use this skill whenever the user wants to "highlight this quote in the image as a video", "make a reel that highlights this sentence", "animate a marker sweep over this passage", "blur everything except this sentence and record it", or hands over a screenshot of text along with a quote they want emphasized for social media / lecture slides. Also trigger on phrases like "highlight reel of this paragraph", "animated highlighter", "marker animation on this screenshot", or any request that combines a text-image and a target quote with the intent of producing a short video.
---

# Text Highlight Reel

Turn a screenshot of text + a target quote into a short animated MP4 where the rest of the page blurs out and a yellow marker sweeps across the quote.

## When to use

The user gives you (or refers to) two things:
1. **An image of text** — a screenshot, PDF page render, scanned document, blog excerpt, etc.
2. **A quote inside that image** — the specific sentence/phrase they want highlighted.

…and they want a short video/GIF that draws attention to that quote. Common phrasings: "highlight this sentence and make it a video", "animate a marker over this", "blur everything except…", "make me an Instagram-style highlight of this paragraph."

If the user only has a PDF, render a page to PNG first (e.g. with `pdftoppm` or Chrome screenshot) and then proceed.

## Inputs

You need three things from the user — gather them if they're missing:

| Input | Required | How to obtain |
| --- | --- | --- |
| Image path | yes | Ask, or use the most recent screenshot they shared |
| The exact quote | yes | Copy from their message; punctuation/case do not need to be exact — OCR matching is fuzzy |
| Output path | recommended | Default to the cwd as `highlight_<slug>.mp4` |

Optional knobs: `--duration` (seconds, default 6), `--blur-radius` (default 10).

If OCR fails to locate the quote (e.g. handwriting, weird font, the quote spans a hyphenated line break), fall back to **manual rectangles**: ask the user to look at the image and give you `(x, y, width, height)` per line, or compute them yourself by inspecting a crop of the image. Then call `render.py` with `--lines '[...]'` instead of `--quote`.

## How to run it

The skill ships a Remotion project and two helper scripts:

```
text-highlight-reel/
├── SKILL.md                              (this file)
├── scripts/
│   ├── render.py                         orchestrator — call this
│   ├── find_boxes.py                     quote → pixel rectangles (OCR)
│   └── vision_ocr.swift                  macOS Vision word-box dumper
└── assets/remotion-project/              the parameterized Remotion app
```

### Path 1: OCR-located quote (preferred)

```bash
uv run "$SKILL_DIR/scripts/render.py" \
  --image /abs/path/to/screenshot.png \
  --quote "the sentence the user wants highlighted" \
  --out   /abs/path/to/output.mp4
```

This OCRs the image with macOS Vision, finds the quote, computes one rectangle per visible line, and renders.

### Path 2: Manual rectangles (fallback)

Use this when OCR can't find the quote or the user wants pixel-perfect control.
Inspect the image (`PIL.Image.crop` around suspected y-ranges, then `Read` the crop) to estimate `(x, y, w, h)` for each line of the quote. Then:

```bash
uv run "$SKILL_DIR/scripts/render.py" \
  --image /abs/path/to/screenshot.png \
  --lines '[{"x":1820,"y":365,"w":165,"h":50},{"x":40,"y":430,"w":1440,"h":50}]' \
  --out   /abs/path/to/output.mp4
```

Each line of the quote gets its own rectangle. A multi-line sentence where the first line starts mid-paragraph gets a small rect at the right end of the upper line plus a full-width rect on the next line — match what's actually visible.

### First run

The first invocation copies the Remotion project to `~/.cache/text-highlight-reel-project/` and runs `npm install` once (~30s, ~250MB). Subsequent renders reuse it and take seconds.

### Output

A `.mp4` at the path you specified, matching the image's exact pixel dimensions (rounded to even for H.264). If the user asked for a GIF, transcode after rendering:

```bash
ffmpeg -i output.mp4 -vf "fps=20,scale=900:-1:flags=lanczos" output.gif
```

## Animation timeline (defaults)

- **0.0–0.5s** — hold sharp original
- **0.5–1.5s** — blur ramps in, surrounding text dims, the sharp window over the quote fades in
- **1.6–4.6s** — yellow marker sweeps left-to-right across each line of the quote
- **4.6–end**  — hold final frame

To change pacing, edit `assets/remotion-project/src/HighlightSweep.tsx` — the schema fields `blurStart`, `blurEnd`, `sweepStart`, `sweepEnd` are all overridable via `--props` if you want to expose them through `render.py` (currently only `durationSeconds` and `blurRadius` are wired through; extend the orchestrator if needed).

## Why this design

The naive approach — Gaussian-blur the whole image in PIL and paste a clear crop on top — works but produces a hard rectangular boundary around the sharp region and a flat yellow rectangle that obscures the text. Three choices make this version look like a real highlighter:

1. **`filter: blur(Npx)` on the `<Img>`** rather than a pre-blurred raster. The browser samples each frame at full resolution, so the blur stays smooth at any composition size and animates continuously instead of stepping.
2. **`mix-blend-mode: multiply` for the yellow overlay**. A solid opaque rectangle would cover the letters; multiplying yellow against the page lets the dark text show through, exactly like a real marker.
3. **Radial-gradient mask on the sharp window**. The "kept sharp" region is feathered instead of a hard rect, so the transition from blurred → sharp around the highlighted line reads as a soft halo rather than a cutout.

## Tips for picking the quote string

OCR matching is normalized (lowercase, punctuation stripped, whitespace collapsed) and tolerates up to two mismatched words, so don't worry about getting quotation marks or curly apostrophes right. Do include enough words to be unambiguous — if the same 3-word phrase appears twice on the page, give 6–10 words so the matcher locks onto the right occurrence.

## Failure modes & quick fixes

- **"quote not found in OCR text"** — try a shorter, less ambiguous chunk; or fall back to manual rectangles.
- **Highlight overshoots the period** — pass a tighter quote (omit trailing words) or supply explicit `--lines`.
- **Highlight looks too tall/short** — Vision word boxes can be loose; tweak the rectangle heights via `--lines`.
- **Render fails on `npm install`** — check Node ≥18; clear `~/.cache/text-highlight-reel-project/node_modules` and retry.
