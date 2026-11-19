#!/usr/bin/env python3
"""Build the Grand Theft Code themes for T3 Code from the readable sources in src/.

    python3 build.py           write themes/*.json and docs/index.html
    python3 build.py --check   fail if the committed files are out of date

No dependencies beyond the Python 3.9+ standard library.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

# T3 Code refuses theme CSS longer than this.
CSS_LIMIT = 50_000
SCENE_PLACEHOLDER = "__SCENE__"
LOGO_MARKER = re.compile(r"^(?:<!--|/\*)\s*(/?)logo\s*(?:-->|\*/)$")

VARIANTS = {
    # theme id: (display name, include the VI badge)
    "grand-theft-code": ("Grand Theft Code", True),
    "grand-theft-code-clean": ("Grand Theft Code Clean", False),
}


def without_logo(text: str, keep_logo: bool) -> str:
    """Drop the logo marker lines and, for the Clean variant, what sits between them."""
    out, inside = [], False
    for line in text.splitlines():
        marker = LOGO_MARKER.match(line.strip())
        if marker:
            closing = marker.group(1) == "/"
            if closing != inside:
                raise SystemExit(f"unbalanced logo marker: {line.strip()}")
            inside = not closing
            continue
        if inside and not keep_logo:
            continue
        out.append(line)
    if inside:
        raise SystemExit("logo marker never closed")
    return "\n".join(out)


def join_lines(text: str) -> str:
    """Join lines with nothing between them, dropping indentation and blank lines."""
    return "".join(line.strip() for line in text.splitlines())


def build_scene(keep_logo: bool) -> str:
    """Return scene.svg as a data URI that is safe inside a double-quoted CSS url()."""
    svg = without_logo((SRC / "scene.svg").read_text(), keep_logo)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"/\*.*?\*/", "", svg, flags=re.S)
    svg = join_lines(svg)
    if '"' in svg:
        raise SystemExit("scene.svg must use single quotes only")
    return "data:image/svg+xml," + svg.replace("#", "%23")


def build_css(keep_logo: bool) -> str:
    css = re.sub(r"/\*.*?\*/", "", (SRC / "theme.css").read_text(), flags=re.S)
    rules = [join_lines(block) for block in re.split(r"\n\s*\n", css)]
    css = "\n".join(rule for rule in rules if rule)
    if css.count(SCENE_PLACEHOLDER) != 1:
        raise SystemExit(f"theme.css must contain {SCENE_PLACEHOLDER} exactly once")
    return css.replace(SCENE_PLACEHOLDER, build_scene(keep_logo))


def validate(theme_id: str, css: str) -> None:
    """Check the rules T3 Code's theme guide sets for the css field."""
    problems = []
    if len(css) > CSS_LIMIT:
        problems.append(f"css is {len(css)} characters, limit is {CSS_LIMIT}")
    for banned in ("@import", "image-set("):
        if banned in css:
            problems.append(f"{banned} is not allowed")
    for target in re.findall(r"url\(\s*([^)]{0,12})", css):
        if not target.lstrip("\"'").startswith(("data:", "#", "%23")):
            problems.append(f"url() may only point at data: or #id, found {target!r}")
    if problems:
        raise SystemExit(f"{theme_id}: " + "; ".join(problems))


def build_theme(theme_id: str) -> dict:
    name, keep_logo = VARIANTS[theme_id]
    theme = json.loads((SRC / "theme.json").read_text())
    theme["name"] = name
    theme["css"] = build_css(keep_logo)
    validate(theme_id, theme["css"])
    return theme


def build_demo(themes: dict[str, dict]) -> str:
    """Inline both variants into the mock chat page served by GitHub Pages."""
    payload = json.dumps(themes, ensure_ascii=False).replace("</", "<\\/")
    page = (SRC / "demo.html").read_text()
    if page.count("__THEMES__") != 1:
        raise SystemExit("demo.html must contain __THEMES__ exactly once")
    return page.replace("__THEMES__", payload)


def outputs() -> dict[pathlib.Path, str]:
    themes = {theme_id: build_theme(theme_id) for theme_id in VARIANTS}
    files = {
        ROOT / "themes" / f"{theme_id}.json": json.dumps(theme, ensure_ascii=False) + "\n"
        for theme_id, theme in themes.items()
    }
    files[ROOT / "docs" / "index.html"] = build_demo(themes)
    return files


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for path, content in outputs().items():
        rel = path.relative_to(ROOT)
        if check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(rel))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"wrote {rel} ({len(content):,} characters)")
    if stale:
        print("out of date, run python3 build.py: " + ", ".join(stale), file=sys.stderr)
        return 1
    if check:
        print("themes and demo are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
