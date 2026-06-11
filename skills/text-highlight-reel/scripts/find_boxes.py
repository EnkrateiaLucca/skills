# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Find pixel rectangles for a quoted phrase inside an image, using macOS Vision OCR.

Usage:
    uv run find_boxes.py <image> "<quote>"

Output (stdout, JSON):
    {"lines": [{"x":N,"y":N,"w":N,"h":N}, ...]}

Strategy: OCR every word with its pixel box, then find the longest contiguous
run of OCR words whose normalized text matches the normalized quote. Group the
matched words by line (similar y-center) and emit one rectangle per line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SWIFT_SCRIPT = HERE / "vision_ocr.swift"


def normalize(s: str) -> str:
    # lowercase, strip punctuation, collapse whitespace
    s = s.lower()
    s = re.sub(r"[‘’“”]", "'", s)
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def ocr(image_path: str):
    out = subprocess.check_output(
        ["swift", str(SWIFT_SCRIPT), image_path],
        stderr=subprocess.PIPE,
    )
    return json.loads(out)


def find_quote_run(words, quote):
    qtoks = normalize(quote).split()
    if not qtoks:
        return []
    wtoks = [normalize(w["text"]) for w in words]
    # Slide a window over the word list
    n, m = len(wtoks), len(qtoks)
    best = None  # (start, length, miss_count)
    for i in range(n):
        j = 0  # quote pointer
        k = i  # word pointer
        misses = 0
        while j < m and k < n:
            if wtoks[k] == qtoks[j]:
                j += 1
                k += 1
            elif wtoks[k] == "":
                k += 1
            else:
                # allow a small number of OCR mismatches by skipping one word
                misses += 1
                if misses > 2:
                    break
                k += 1
        if j == m:
            length = k - i
            cand = (i, length, misses)
            if best is None or misses < best[2] or (misses == best[2] and length < best[1]):
                best = cand
    if not best:
        return []
    i, length, _ = best
    return words[i : i + length]


def group_lines(matched_words):
    """Group words by line based on vertical overlap, then build one bbox per line."""
    if not matched_words:
        return []
    # Sort by y then x
    ws = sorted(matched_words, key=lambda w: (w["y"], w["x"]))
    lines = []
    current = [ws[0]]
    for w in ws[1:]:
        ref = current[-1]
        ref_center = ref["y"] + ref["h"] / 2
        w_center = w["y"] + w["h"] / 2
        # Same line if vertical centers within ~60% of line height
        if abs(w_center - ref_center) < max(ref["h"], w["h"]) * 0.6:
            current.append(w)
        else:
            lines.append(current)
            current = [w]
    lines.append(current)

    rects = []
    for line in lines:
        x1 = min(w["x"] for w in line)
        y1 = min(w["y"] for w in line)
        x2 = max(w["x"] + w["w"] for w in line)
        y2 = max(w["y"] + w["h"] for w in line)
        # small horizontal padding so the highlight covers letter bowls
        rects.append({"x": x1 - 4, "y": y1 - 4, "w": (x2 - x1) + 8, "h": (y2 - y1) + 8})
    # Sort top to bottom by y
    rects.sort(key=lambda r: r["y"])
    return rects


def main():
    if len(sys.argv) < 3:
        print("usage: find_boxes.py <image> <quote>", file=sys.stderr)
        sys.exit(2)
    image, quote = sys.argv[1], sys.argv[2]
    words = ocr(image)
    matched = find_quote_run(words, quote)
    if not matched:
        print(json.dumps({"lines": [], "error": "quote not found in OCR text"}), file=sys.stdout)
        sys.exit(1)
    lines = group_lines(matched)
    print(json.dumps({"lines": lines}))


if __name__ == "__main__":
    main()
