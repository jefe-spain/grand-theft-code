#!/usr/bin/env python3
"""Convert lines of text to one SVG path, so the badge needs no font at runtime.

The path in src/scene.svg (id='wm') was made with Pricedown Black by Typodermic
Fonts, which is free to download from https://typodermicfonts.com/pricedown/.
The font is not part of this repository. Get your own copy to change the text:

    pip install fonttools
    python3 tools/wordmark.py "Pricedown Bl.otf" \\
        grand:50:70:.072 theft:72:120:.065 code:72:170:.065

Each line is text:x:baseline:scale, in the badge's 293 x 200 unit space. The
script prints the path data, one closed shape per line, ready to paste into the
d attribute of the wm path.
"""
from __future__ import annotations

import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

# Font units removed between letters; Pricedown looks better set tight.
TRACKING = -14


def number(value: float) -> str:
    """Format with one decimal and no padding: 12.0 -> 12, 0.5 -> .5, -0.5 -> -.5."""
    text = ("%.1f" % value).rstrip("0").rstrip(".")
    if text in ("-0", ""):
        return "0"
    if text.startswith("-0."):
        return "-" + text[2:]
    if text.startswith("0."):
        return text[1:]
    return text


def outline(font_path: str, lines: list[str]) -> str:
    font = TTFont(font_path)
    glyphs, cmap, advances = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    pen = SVGPathPen(glyphs, ntos=number)
    for spec in lines:
        text, x0, baseline, scale = spec.rsplit(":", 3)
        x0, baseline, scale = float(x0), float(baseline), float(scale)
        cursor = 0
        for char in text:
            glyph = cmap[ord(char)]
            # Font y grows upwards and SVG y grows downwards, hence the negative scale.
            glyphs[glyph].draw(TransformPen(pen, (scale, 0, 0, -scale, x0 + cursor * scale, baseline)))
            cursor += advances[glyph][0] + TRACKING
    return pen.getCommands()


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    path = outline(sys.argv[1], sys.argv[2:])
    print(path.replace("Z", "Z\n").rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
