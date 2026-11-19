#!/usr/bin/env python3
"""Draw assets/mockup.svg: an animated mock-up of T3 Code wearing the theme.

    python3 tools/mockup.py           write assets/mockup.svg
    python3 tools/mockup.py --check   fail if the committed file is out of date

The picture is one self-contained SVG with no scripts, fonts or images inside,
so it plays in a README. The background is the real scene from src/scene.svg;
the window around it is drawn here, modelled on T3 Code's layout. Every name,
thread and message in it is invented.

A 24 second loop: the prompt is typed, sent, the agent works, the reply lands.
With reduced motion the finished conversation is shown and nothing moves.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (the theme build lives next to this folder)

OUT = ROOT / "assets" / "mockup.svg"
COLORS = json.loads((ROOT / "src" / "theme.json").read_text())["colors"]

# Window and layout, in px.
W, H = 1360, 800
SIDEBAR = 224
HEADER = 36
AREA_X, AREA_Y, AREA_W, AREA_H = SIDEBAR, HEADER, W - SIDEBAR, H - HEADER
COL_W = 600
COL_X = AREA_X + (AREA_W - COL_W) // 2
COL_R = COL_X + COL_W

# Monospace advance. Every text gets an explicit textLength from this, so the
# layout holds whichever monospace font the viewer has.
ADVANCE = 0.6
FONT = "'Monaspace Neon',ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

INK = COLORS["text"]
MUTED = COLORS["textMuted"]
FAINT = "#9a86b8"
PINK = "#ff2e97"
CYAN = "#00d5ff"
VIOLET = "#8a3ffc"

# Timeline of the loop, in seconds.
LOOP = 24.0
T_TYPE, T_SEND, T_WORK, T_TOOL1, T_TOOL2, T_REPLY, T_CLEAR = 0.7, 3.4, 3.9, 4.7, 5.7, 6.8, 21.6
FADE = 0.35
PROMPT = "Install the theme from jefe-spain/grand-theft-code"

ICONS = {
    "search": "<circle cx='11' cy='11' r='8'/><path d='m21 21-4.3-4.3'/>",
    "panel-left": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M9 3v18'/>",
    "panel-right": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M15 3v18'/>",
    "panel-bottom": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M3 15h18'/>",
    "panel-details": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M8 9h8M8 13h8'/>",
    "arrow-left": "<path d='m12 19-7-7 7-7M19 12H5'/>",
    "arrow-right": "<path d='M5 12h14m-7-7 7 7-7 7'/>",
    "arrow-up": "<path d='m5 12 7-7 7 7M12 19V5'/>",
    "list-filter": "<path d='M3 6h18M7 12h10M10 18h4'/>",
    "folder": "<path d='M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z'/>",
    "folder-plus": "<path d='M12 10v6M9 13h6M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z'/>",
    "square-pen": "<path d='M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7'/><path d='M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z'/>",
    "square-dashed": "<rect x='3' y='3' width='18' height='18' rx='2' stroke-dasharray='4 3.2'/>",
    "settings": "<circle cx='12' cy='12' r='3'/><circle cx='12' cy='12' r='8.5' stroke-dasharray='3.2 3.47'/>",
    "git-branch": "<path d='M6 3v12'/><circle cx='18' cy='6' r='3'/><circle cx='6' cy='18' r='3'/><path d='M18 9a9 9 0 0 1-9 9'/>",
    "chart": "<path d='M6 20v-6M12 20V8M18 20V4'/>",
    "refresh": "<path d='M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8'/><path d='M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16'/><path d='M8 16H3v5'/>",
    "paperclip": "<path d='m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48'/>",
    "mic": "<path d='M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z'/><path d='M19 10v2a7 7 0 0 1-14 0v-2M12 19v3'/>",
    "chevron-down": "<path d='m6 9 6 6 6-6'/>",
    "chevron-right": "<path d='m9 18 6-6-6-6'/>",
    "terminal": "<path d='m4 17 6-6-6-6M12 19h8'/>",
    "wrench": "<path d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z'/>",
    "laptop": "<path d='M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16'/>",
    "code": "<path d='m16 18 6-6-6-6M8 6l-6 6 6 6'/>",
    "plus": "<path d='M5 12h14M12 5v14'/>",
    "copy": "<rect x='8' y='8' width='14' height='14' rx='2'/><path d='M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2'/>",
    "reply": "<path d='M9 14 4 9l5-5'/><path d='M4 9h10.5a5.5 5.5 0 0 1 0 11H11'/>",
    "spark": "<path d='M12 3v18M3 12h18M5.6 5.6l12.8 12.8M18.4 5.6 5.6 18.4'/>",
    "loader": "<circle cx='12' cy='12' r='9' stroke-dasharray='4.2 3.87'/>",
}


def icon(name: str, x: float, y: float, size: float = 12, color: str = MUTED, cls: str = "", width: float = 1.75) -> str:
    """A 24-unit line icon with its top-left corner at x, y."""
    attr = f" class='{cls}'" if cls else ""
    return (
        f"<svg{attr} x='{x}' y='{y}' width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' "
        f"stroke='{color}' stroke-width='{width}' stroke-linecap='round' stroke-linejoin='round'>{ICONS[name]}</svg>"
    )


def text_width(content: str, size: float, spacing: float = 0) -> float:
    return round(len(content) * (size * ADVANCE + spacing), 1)


def text(x: float, y: float, content: str, size: float = 12, fill: str = INK, weight: int = 400,
         anchor: str = "start", cls: str = "", extra: str = "", spacing: float = 0) -> str:
    attrs = f"x='{x}' y='{y}' font-size='{size}' fill='{fill}' textLength='{text_width(content, size, spacing)}'"
    if weight != 400:
        attrs += f" font-weight='{weight}'"
    if anchor != "start":
        attrs += f" text-anchor='{anchor}'"
    if cls:
        attrs += f" class='{cls}'"
    if extra:
        attrs += " " + extra
    return f"<text {attrs}>{escape(content)}</text>"


class Timeline:
    """Collects the opacity keyframes for elements that come and go during the loop."""

    def __init__(self) -> None:
        self.rules: list[str] = []
        self.count = 0

    @staticmethod
    def pct(seconds: float) -> str:
        return f"{seconds / LOOP * 100:.2f}".rstrip("0").rstrip(".") + "%"

    def _add(self, frames: str, resting_visible: bool) -> str:
        self.count += 1
        name = f"u-k{self.count}"
        self.rules.append(f"@keyframes {name}{{{frames}}}")
        self.rules.append(f".{name}{{animation:{name} {LOOP:g}s linear infinite}}")
        return name if resting_visible else f"{name} u-gone"

    def show(self, start: float, end: float = T_CLEAR, resting_visible: bool = True, fade: float = FADE) -> str:
        """Visible from start to end. resting_visible is the state without animation."""
        p = self.pct
        return self._add(
            f"0%,{p(start)}{{opacity:0}}{p(start + fade)},{p(end)}{{opacity:1}}{p(end + fade)},100%{{opacity:0}}",
            resting_visible,
        )

    def hide(self, start: float, end: float) -> str:
        """Visible except from start to end."""
        p = self.pct
        return self._add(
            f"0%,{p(start)}{{opacity:1}}{p(start + FADE)},{p(end)}{{opacity:0}}{p(end + FADE)},100%{{opacity:1}}",
            True,
        )


def scene() -> tuple[str, str]:
    """The theme's own background scene, resized from viewport units to this window."""
    svg = build.build_scene(keep_logo=True).split(",", 1)[1].replace("%23", "#")

    def to_px(match: re.Match) -> str:
        unit = AREA_W if match.group(2) == "w" else AREA_H
        return f"{float(match.group(1)) * unit / 100:g}px"

    svg = re.sub(r"(\d*\.?\d+)v([wh])\b", to_px, svg)
    style = re.search(r"<style>(.*?)</style>", svg, flags=re.S).group(1)
    svg = re.sub(r"<style>.*?</style>", "", svg, flags=re.S)
    opening = "<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'>"
    assert svg.startswith(opening), svg[:80]
    svg = f"<svg x='{AREA_X}' y='{AREA_Y}' width='{AREA_W}' height='{AREA_H}'>" + svg[len(opening):]
    return style, svg


def sky() -> str:
    """The CSS layers under the scene: sky gradient, grid lines, striped sun."""
    cx, bottom = AREA_X + AREA_W / 2, H
    stripes = "".join(
        f"<rect x='{cx - 320}' y='{bottom - 300 + 22 + 30 * i}' width='640' height='8'/>" for i in range(10)
    )
    return (
        f"<rect x='{AREA_X}' y='{AREA_Y}' width='{AREA_W}' height='{AREA_H}' fill='url(#u-sky)'/>"
        f"<rect x='{AREA_X}' y='{AREA_Y}' width='{AREA_W}' height='{AREA_H}' fill='url(#u-grid)'/>"
        f"<g clip-path='url(#u-sunbox)'><circle cx='{cx}' cy='{bottom}' r='452.5' fill='url(#u-sun)'/></g>"
        f"<g fill='#ffd6e0' opacity='.95'>{stripes}</g>"
    )


def sidebar(tl: Timeline) -> str:
    out = [
        f"<rect width='{SIDEBAR}' height='{H}' fill='url(#u-side)'/>",
        # Window controls and app title.
        "<circle cx='17' cy='18' r='5.5' fill='#ff5f57'/><circle cx='35' cy='18' r='5.5' fill='#febc2e'/>"
        "<circle cx='53' cy='18' r='5.5' fill='#28c840'/>",
        icon("panel-left", 70, 11.5, 13),
        text(92, 22, "T3", 12, INK, 800),
        text(109, 22, "Code", 12, MUTED),
        icon("arrow-left", 144, 12, 12, FAINT),
        icon("arrow-right", 164, 12, 12, FAINT),
        # Search row.
        icon("search", 12, 44, 13),
        text(32, 54.5, "Search", 12, MUTED, 600),
        icon("list-filter", 164, 44.5, 12),
        icon("folder-plus", 183, 44.5, 12),
        icon("square-pen", 202, 44.5, 12),
    ]

    def thread(y: float, project: str, age: str, title: str, branch: str = "", project_icon: str = "folder") -> None:
        out.append(icon(project_icon, 12, y - 8.5, 10, FAINT))
        out.append(text(27, y, project, 10, FAINT))
        out.append(text(212, y, age, 10, FAINT, anchor="end"))
        out.append(text(12, y + 17, title, 12, MUTED))
        if branch:
            out.append(text(12, y + 31, branch, 10, FAINT))

    thread(84, "acme-web", "12m", "Fix flaky checkout test", "main")
    thread(140, "No project", "40m", "Plan the team offsite", project_icon="square-dashed")
    thread(182, "billing-api", "2h", "Refactor webhook retries", "retry-queue")

    # Lower groups: the open thread, then the settled ones.
    out += [
        text(12, 652, "Working", 10.5, MUTED, 600),
        text(196, 652, "1", 10.5, MUTED, anchor="end"),
        icon("chevron-down", 201, 643, 10, FAINT),
        f"<rect x='6' y='664' width='{SIDEBAR - 14}' height='44' rx='8' fill='{COLORS['sidebarRowActive']}'/>",
        icon("square-dashed", 12, 670.5, 10, FAINT),
        text(27, 679, "No project", 10, FAINT),
        text(12, 697, "Install a sunset theme", 12, INK, 600),
    ]
    busy = tl.show(T_SEND, T_REPLY, resting_visible=False)
    idle = tl.hide(T_SEND, T_REPLY)
    out += [
        f"<g class='{busy}'>"
        f"<g transform='translate(143 675.5)'><g class='u-spin'>{icon('loader', -5, -5, 10, '#3b5bff', width=2.4)}</g></g>"
        + text(212, 679, "Working", 10, "#3b5bff", 700, anchor="end")
        + "</g>",
        text(212, 679, "now", 10, FAINT, anchor="end", cls=idle),
        text(12, 734, "Settled", 10.5, MUTED, 600),
        text(196, 734, "3", 10.5, MUTED, anchor="end"),
        icon("chevron-right", 201, 725, 10, FAINT),
        icon("settings", 12, 772, 13),
        icon("git-branch", 36, 772, 13),
        icon("chart", 60, 772, 13),
        icon("refresh", 199, 772, 13),
        # Violet edge with a soft glow.
        f"<rect x='{SIDEBAR - 8}' width='8' height='{H}' fill='url(#u-edge)'/>",
        f"<rect x='{SIDEBAR - 2}' width='2' height='{H}' fill='{VIOLET}'/>",
    ]
    return "".join(out)


def header() -> str:
    x = SIDEBAR
    return "".join([
        f"<rect x='{x}' width='{W - x}' height='{HEADER}' fill='#fff' fill-opacity='.86'/>",
        f"<rect x='{x}' y='{HEADER - 2}' width='{W - x}' height='8' fill='url(#u-hglow)'/>",
        f"<rect x='{x}' y='{HEADER - 2}' width='{W - x}' height='2' fill='{PINK}'/>",
        icon("square-dashed", x + 14, 11, 11, FAINT),
        text(x + 31, 21.5, "No project", 11.5, FAINT),
        text(x + 109, 21.5, "/", 11.5, FAINT),
        text(x + 125, 21.5, "Install a sunset theme", 11.5, INK, 600),
        f"<rect x='{W - 80}' y='7' width='20' height='20' rx='5' fill='#ffd0e8'/>",
        icon("panel-details", W - 76, 11, 12, INK),
        icon("panel-bottom", W - 52, 11, 12),
        icon("panel-right", W - 28, 11, 12),
    ])


def details() -> str:
    """The thread details card on the right."""
    x, y, w = W - 186, HEADER + 10, 176
    out = [
        f"<rect x='{x}' y='{y}' width='{w}' height='152' rx='12' fill='#fad7e6' fill-opacity='.9' stroke='#f3bfd9'/>",
        icon("laptop", x + 12, y + 12, 12),
        text(x + 32, y + 22, "Studio Mac", 11, INK, 600),
        icon("code", x + 12, y + 32, 12, INK),
        text(x + 32, y + 42, "Open in editor", 11, INK, 600),
        icon("chevron-down", x + w - 22, y + 33, 10),
        icon("plus", x + 12, y + 52, 12),
        text(x + 32, y + 62, "Add project script", 11, INK, 600),
    ]

    def meter(row_y: float, label: str, share: float, value: str, bar_x: float = 76, bar_w: float = 58) -> None:
        out.append(text(x + 12, row_y, label, 9.5, FAINT))
        out.append(f"<rect x='{x + bar_x}' y='{row_y - 4}' width='{bar_w}' height='2' rx='1' fill='#d9c4dd'/>")
        out.append(f"<rect x='{x + bar_x}' y='{row_y - 4}' width='{bar_w * share:g}' height='2' rx='1' fill='#5d3f86'/>")
        out.append(text(x + w - 12, row_y, value, 9.5, MUTED, anchor="end"))

    meter(y + 90, "Session", 0.38, "38%")
    meter(y + 106, "Weekly", 0.12, "12%")
    meter(y + 136, "Context", 0.12, "24k / 200k", bar_x=62, bar_w=40)
    return "".join(out)


def conversation(tl: Timeline) -> str:
    out = []

    # User message, right-aligned.
    bubble_w = text_width(PROMPT, 12) + 32
    bx = COL_R - bubble_w
    out.append(
        f"<g class='{tl.show(T_SEND)}'>"
        f"<rect x='{bx + 2}' y='72' width='{bubble_w - 4}' height='34' rx='16' fill='{PINK}' opacity='.35' filter='url(#u-blur6)'/>"
        f"<path d='M{bx + 18} 62H{COL_R - 18}a18 18 0 0 1 18 18v12a4 4 0 0 1-4 4H{bx + 18}a18 18 0 0 1-18-18a18 18 0 0 1 18-18Z' fill='url(#u-bubble)'/>"
        + text(bx + 16, 83.5, PROMPT, 12, INK)
        + "</g>"
    )

    # Work log.
    x = COL_X
    out.append(text(x, 132, "Working for 3s", 11, FAINT, cls=tl.show(T_WORK, T_REPLY, resting_visible=False)))
    out.append(
        f"<g class='{tl.show(T_REPLY)}'>" + text(x, 132, "Worked for 3s", 11, FAINT)
        + icon("chevron-right", x + text_width("Worked for 3s", 11) + 5, 123, 10, FAINT) + "</g>"
    )
    out.append(f"<g class='{tl.show(T_TOOL1)}'>" + icon("terminal", x, 145, 11, FAINT) + text(x + 18, 154.5, "Ran 2 commands", 11, FAINT) + "</g>")
    out.append(f"<g class='{tl.show(T_TOOL2)}'>" + icon("wrench", x, 167, 11, FAINT) + text(x + 18, 176.5, "Set the theme", 11, FAINT) + "</g>")

    # Assistant reply card.
    cy, ch = 192, 208
    tx = x + 22
    card = [
        f"<rect x='{x + 14}' y='{cy + 26}' width='{COL_W - 28}' height='{ch - 20}' rx='16' fill='{VIOLET}' opacity='.4' filter='url(#u-blur10)'/>",
        f"<rect x='{x - 4}' y='{cy - 4}' width='{COL_W + 8}' height='{ch + 8}' rx='20' fill='#fff' opacity='.45'/>",
        f"<rect x='{x}' y='{cy}' width='{COL_W}' height='{ch}' rx='16' fill='#fff' fill-opacity='.96' stroke='#f1c4e1'/>",
    ]

    def line(delay: float, body: str) -> None:
        card.append(f"<g class='{tl.show(T_REPLY + delay)}'>{body}</g>")

    title = "GRAND THEFT CODE IS ON"
    title_attrs = "font-style='italic'"
    line(0.2,
         text(tx, cy + 33, title, 14, PINK, 800, extra=title_attrs + " filter='url(#u-blur4)' opacity='.75'", spacing=1.1, cls="u-tube")
         + text(tx, cy + 33, title, 14, PINK, 800, extra=title_attrs, spacing=1.1))
    first = "The theme file is in your themes folder and T3 Code has switched to it."
    line(0.5, text(tx, cy + 60, first, 12, INK) + text(tx, cy + 80, "Nothing else was changed.", 12, "#c4006a", 700))
    bullet_1 = "Palms sway, clouds drift and a plane crosses the sky every 75 seconds."
    line(0.8, f"<circle cx='{tx + 3}' cy='{cy + 104}' r='1.7' fill='{INK}'/>" + text(tx + 14, cy + 108, bullet_1, 12, INK))
    # Second bullet holds an inline code chip.
    before, chip, after = "The ", "VI", " badge floats in the corner. Ask for the clean variant to drop it."
    chip_x = tx + 14 + text_width(before, 12)
    chip_w = text_width(chip, 12) + 10
    line(1.1,
         f"<circle cx='{tx + 3}' cy='{cy + 126}' r='1.7' fill='{INK}'/>"
         + text(tx + 14, cy + 130, before.rstrip(), 12, INK)
         + f"<rect x='{chip_x - 2}' y='{cy + 118}' width='{chip_w}' height='17' rx='6' fill='{INK}'/>"
         + text(chip_x + 3, cy + 130, chip, 12, "#7df3ff")
         + text(chip_x + chip_w + 2, cy + 130, after.strip(), 12, INK))
    code = 't3_theme_set({ themeId: "grand-theft-code", appearance: "light" })'
    line(1.4,
         f"<rect x='{tx}' y='{cy + 148}' width='{COL_W - 44}' height='40' rx='12' fill='{CYAN}' opacity='.5' filter='url(#u-blur6)'/>"
         f"<rect x='{tx}' y='{cy + 148}' width='{COL_W - 44}' height='40' rx='12' fill='{COLORS['codeBackground']}' stroke='{CYAN}' stroke-width='2'/>"
         + text(tx + 16, cy + 172, code, 11.5, INK))
    out.append(f"<g class='{tl.show(T_REPLY)}'>{''.join(card)}</g>")

    # Message actions under the reply.
    my = cy + ch + 12
    out.append(
        f"<g class='{tl.show(T_REPLY + 1.7)}'>" + icon("copy", x + 4, my, 11, FAINT) + icon("git-branch", x + 28, my, 11, FAINT)
        + icon("reply", x + 52, my, 11, FAINT) + text(x + 76, my + 9.5, "09:41", 10, FAINT) + "</g>"
    )
    return "".join(out)


def composer(tl: Timeline) -> tuple[str, list[str]]:
    x, y, w, h = COL_X, 712, COL_W, 70
    out = [
        # Cyan offset shadow, pink glow, white ring, then the card.
        f"<rect x='{x + 10}' y='{y + 12}' width='{w - 4}' height='{h - 4}' rx='15' fill='{CYAN}' opacity='.55'/>",
        f"<rect x='{x - 2}' y='{y - 2}' width='{w + 4}' height='{h + 4}' rx='18' fill='{PINK}' opacity='.75' filter='url(#u-blur10)'/>",
        f"<rect x='{x - 4}' y='{y - 4}' width='{w + 8}' height='{h + 8}' rx='19' fill='#fff' opacity='.9'/>",
        f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='15' fill='#fff' fill-opacity='.94' stroke='{PINK}' stroke-width='2'/>",
        text(x + 16, y + 25, "Ask anything. @ files, $ skills, / commands", 12, FAINT, cls=tl.hide(T_TYPE - 0.2, T_SEND)),
        icon("paperclip", x + 14, y + h - 24, 12),
        icon("spark", x + w - 162, y + h - 24, 12, "#e2733d", width=2),
        text(x + w - 145, y + h - 14, "Fable 5.2", 11, INK, 600),
        text(x + w - 80, y + h - 14, "High", 11, MUTED),
        icon("mic", x + w - 46, y + h - 24, 12),
    ]
    # Send button: an arrow at rest, a stop square while the agent works.
    bx, by = x + w - 20, y + h - 18
    out.append(f"<circle cx='{bx}' cy='{by}' r='10' fill='{PINK}'/>")
    out.append(f"<g class='{tl.hide(T_SEND, T_REPLY)}'>{icon('arrow-up', bx - 6, by - 6, 12, '#fff', width=2.4)}</g>")
    out.append(f"<rect class='{tl.show(T_SEND, T_REPLY, resting_visible=False)}' x='{bx - 3.5}' y='{by - 3.5}' width='7' height='7' rx='1.5' fill='#fff'/>")

    # The prompt is typed one character at a time, then cleared when it is sent.
    typing_rules = []
    step = (T_SEND - 0.5 - T_TYPE) / len(PROMPT)
    p = Timeline.pct
    chars = []
    for i, char in enumerate(PROMPT):
        if char == " ":
            continue
        at = T_TYPE + i * step
        typing_rules.append(
            f"@keyframes u-c{i}{{0%,{p(at)}{{opacity:0}}{p(at + 0.02)},{p(T_SEND)}{{opacity:1}}{p(T_SEND + 0.15)},100%{{opacity:0}}}}"
            f".u-c{i}{{animation:u-c{i} {LOOP:g}s linear infinite}}"
        )
        chars.append(f"<text class='u-c{i} u-gone' x='{x + 16 + i * 12 * ADVANCE:g}' y='{y + 25}'>{escape(char)}</text>")
    out.append(f"<g font-size='12' fill='{INK}'>{''.join(chars)}</g>")
    return "".join(out), typing_rules


def render() -> str:
    tl = Timeline()
    scene_style, scene_svg = scene()
    side = sidebar(tl)
    talk = conversation(tl)
    box, typing_rules = composer(tl)
    cx = AREA_X + AREA_W / 2

    defs = (
        f"<clipPath id='u-win'><rect width='{W}' height='{H}' rx='12'/></clipPath>"
        f"<clipPath id='u-sunbox'><rect x='{cx - 320}' y='{H - 320}' width='640' height='320'/></clipPath>"
        "<linearGradient id='u-side' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#efe4ff'/>"
        "<stop offset='.55' stop-color='#ffe3f3'/><stop offset='1' stop-color='#ffe9c9'/></linearGradient>"
        "<linearGradient id='u-sky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#efe4ff'/>"
        "<stop offset='.4' stop-color='#ffe3f3'/><stop offset='.72' stop-color='#ffd9de'/><stop offset='1' stop-color='#ffe9c9'/></linearGradient>"
        f"<pattern id='u-grid' x='{AREA_X}' y='0' width='44' height='44' patternUnits='userSpaceOnUse'>"
        f"<rect width='1' height='44' fill='{VIOLET}' opacity='.1'/></pattern>"
        f"<radialGradient id='u-sun' gradientUnits='userSpaceOnUse' cx='{cx}' cy='{H}' r='452.5'>"
        "<stop offset='0' stop-color='#ffe25c' stop-opacity='.85'/><stop offset='.45' stop-color='#ff8a4c' stop-opacity='.75'/>"
        "<stop offset='.7' stop-color='#ff2e97' stop-opacity='.7'/><stop offset='.705' stop-color='#ff2e97' stop-opacity='0'/></radialGradient>"
        "<linearGradient id='u-bubble' x1='0' y1='0' x2='1' y2='.35'><stop offset='0' stop-color='#ffe45c'/>"
        "<stop offset='.5' stop-color='#ffa26b'/><stop offset='1' stop-color='#ff6fb5'/></linearGradient>"
        f"<linearGradient id='u-edge'><stop offset='0' stop-color='{VIOLET}' stop-opacity='0'/><stop offset='1' stop-color='{VIOLET}' stop-opacity='.35'/></linearGradient>"
        f"<linearGradient id='u-hglow' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{PINK}' stop-opacity='.45'/><stop offset='1' stop-color='{PINK}' stop-opacity='0'/></linearGradient>"
        "<filter id='u-blur4' x='-20%' y='-60%' width='140%' height='220%'><feGaussianBlur stdDeviation='3'/></filter>"
        "<filter id='u-blur6' x='-10%' y='-40%' width='120%' height='180%'><feGaussianBlur stdDeviation='6'/></filter>"
        "<filter id='u-blur10' x='-10%' y='-40%' width='120%' height='180%'><feGaussianBlur stdDeviation='10'/></filter>"
    )
    style = (
        f"text{{font-family:{FONT};white-space:pre}}"
        ".u-gone{opacity:0}"
        ".u-spin{animation:u-spin 1.6s linear infinite}@keyframes u-spin{to{rotate:360deg}}"
        ".u-tube{animation:u-tube 3.2s ease-in-out infinite}@keyframes u-tube{50%{opacity:.25}}"
        + "".join(tl.rules) + "".join(typing_rules)
        # The scene's own rules come last: they end with the reduced-motion switch for everything.
        + scene_style
    )
    title = "Grand Theft Code theme in T3 Code"
    desc = (
        "Animated mock-up of the T3 Code window with the Grand Theft Code theme: a sidebar of threads, "
        "a chat where an agent installs the theme, and a sunset background with palms and a VI badge."
    )
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}' role='img' aria-labelledby='u-title u-desc'>"
        f"<title id='u-title'>{title}</title><desc id='u-desc'>{desc}</desc>"
        f"<style>{style}</style><defs>{defs}</defs>"
        "<g clip-path='url(#u-win)'>"
        f"<rect width='{W}' height='{H}' fill='{json.loads((ROOT / 'src' / 'theme.json').read_text())['canvas']}'/>"
        + sky() + scene_svg + talk + box + details() + header() + side
        + "</g>"
        f"<rect x='.5' y='.5' width='{W - 1}' height='{H - 1}' rx='12' fill='none' stroke='#2a1050' stroke-opacity='.25'/>"
        "</svg>\n"
    )


def main() -> int:
    svg = render()
    if "--check" in sys.argv[1:]:
        if not OUT.exists() or OUT.read_text() != svg:
            print("assets/mockup.svg is out of date, run python3 tools/mockup.py", file=sys.stderr)
            return 1
        print("mock-up is up to date")
        return 0
    OUT.write_text(svg)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(svg):,} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
