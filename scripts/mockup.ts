/**
 * Draw assets/mockup.svg: an animated mock-up of T3 Code wearing the theme.
 *
 * The picture is one self-contained SVG with no scripts, fonts or images
 * inside, so it plays in a README. The background is the theme's real scene;
 * the window around it is drawn here, modelled on T3 Code's layout. Every
 * name, thread and message in it is invented.
 *
 * A 24 second loop: the prompt is typed, sent, the agent works, the reply
 * lands. With reduced motion the finished conversation is shown, still.
 */
import type { Theme } from "./build.ts";

// Window and layout, in px.
const W = 1360;
const H = 800;
const SIDEBAR = 224;
const HEADER = 36;
const AREA = { x: SIDEBAR, y: HEADER, w: W - SIDEBAR, h: H - HEADER };
const COL_W = 600;
const COL_X = AREA.x + (AREA.w - COL_W) / 2;
const COL_R = COL_X + COL_W;

// Monospace advance. Every text gets an explicit textLength from this, so the
// layout holds whichever monospace font the viewer has.
const ADVANCE = 0.6;
const FONT =
  "'Monaspace Neon',ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace";

const FAINT = "#9a86b8";
const PINK = "#ff2e97";
const CYAN = "#00d5ff";
const VIOLET = "#8a3ffc";

// Timeline of the loop, in seconds.
const LOOP = 24;
const T = { type: 0.7, send: 3.4, work: 3.9, tool1: 4.7, tool2: 5.7, reply: 6.8, clear: 21.6 };
const FADE = 0.35;
const PROMPT = "Install the theme from jefe-spain/grand-theft-code";

const ICONS = {
  search: "<circle cx='11' cy='11' r='8'/><path d='m21 21-4.3-4.3'/>",
  "panel-left": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M9 3v18'/>",
  "panel-right": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M15 3v18'/>",
  "panel-bottom": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M3 15h18'/>",
  "panel-details": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M8 9h8M8 13h8'/>",
  "arrow-left": "<path d='m12 19-7-7 7-7M19 12H5'/>",
  "arrow-right": "<path d='M5 12h14m-7-7 7 7-7 7'/>",
  "arrow-up": "<path d='m5 12 7-7 7 7M12 19V5'/>",
  "list-filter": "<path d='M3 6h18M7 12h10M10 18h4'/>",
  folder:
    "<path d='M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z'/>",
  "folder-plus":
    "<path d='M12 10v6M9 13h6M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z'/>",
  "square-pen":
    "<path d='M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7'/><path d='M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z'/>",
  "square-dashed": "<rect x='3' y='3' width='18' height='18' rx='2' stroke-dasharray='4 3.2'/>",
  settings: "<circle cx='12' cy='12' r='3'/><circle cx='12' cy='12' r='8.5' stroke-dasharray='3.2 3.47'/>",
  "git-branch":
    "<path d='M6 3v12'/><circle cx='18' cy='6' r='3'/><circle cx='6' cy='18' r='3'/><path d='M18 9a9 9 0 0 1-9 9'/>",
  chart: "<path d='M6 20v-6M12 20V8M18 20V4'/>",
  refresh:
    "<path d='M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8'/><path d='M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16'/><path d='M8 16H3v5'/>",
  paperclip:
    "<path d='m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48'/>",
  mic: "<path d='M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z'/><path d='M19 10v2a7 7 0 0 1-14 0v-2M12 19v3'/>",
  "chevron-down": "<path d='m6 9 6 6 6-6'/>",
  "chevron-right": "<path d='m9 18 6-6-6-6'/>",
  terminal: "<path d='m4 17 6-6-6-6M12 19h8'/>",
  wrench:
    "<path d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z'/>",
  laptop:
    "<path d='M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16'/>",
  code: "<path d='m16 18 6-6-6-6M8 6l-6 6 6 6'/>",
  plus: "<path d='M5 12h14M12 5v14'/>",
  copy: "<rect x='8' y='8' width='14' height='14' rx='2'/><path d='M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2'/>",
  reply: "<path d='M9 14 4 9l5-5'/><path d='M4 9h10.5a5.5 5.5 0 0 1 0 11H11'/>",
  spark: "<path d='M12 3v18M3 12h18M5.6 5.6l12.8 12.8M18.4 5.6 5.6 18.4'/>",
  loader: "<circle cx='12' cy='12' r='9' stroke-dasharray='4.2 3.87'/>",
} as const;

type IconName = keyof typeof ICONS;

const escapeXml = (s: string): string => s.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");

/** Round to one decimal, which is all the precision the layout needs. */
const r1 = (n: number): number => Math.round(n * 10) / 10;

/** A 24-unit line icon with its top-left corner at x, y. */
function icon(name: IconName, x: number, y: number, size = 12, color = "", opts: { cls?: string; width?: number } = {}): string {
  const cls = opts.cls ? ` class='${opts.cls}'` : "";
  return (
    `<svg${cls} x='${r1(x)}' y='${r1(y)}' width='${size}' height='${size}' viewBox='0 0 24 24' fill='none' ` +
    `stroke='${color}' stroke-width='${opts.width ?? 1.75}' stroke-linecap='round' stroke-linejoin='round'>${ICONS[name]}</svg>`
  );
}

const textWidth = (content: string, size: number, spacing = 0): number => r1(content.length * (size * ADVANCE + spacing));

interface TextOptions {
  size?: number;
  fill?: string;
  weight?: number;
  anchor?: "start" | "end";
  cls?: string;
  extra?: string;
  spacing?: number;
}

function text(x: number, y: number, content: string, opts: TextOptions = {}): string {
  const { size = 12, fill = "", weight = 400, anchor = "start", cls, extra, spacing = 0 } = opts;
  let attrs = `x='${r1(x)}' y='${r1(y)}' font-size='${size}' fill='${fill}' textLength='${textWidth(content, size, spacing)}'`;
  if (weight !== 400) attrs += ` font-weight='${weight}'`;
  if (anchor !== "start") attrs += ` text-anchor='${anchor}'`;
  if (cls) attrs += ` class='${cls}'`;
  if (extra) attrs += ` ${extra}`;
  return `<text ${attrs}>${escapeXml(content)}</text>`;
}

/** Seconds into the loop, as a keyframe percentage. */
const pct = (seconds: number): string => `${Number(((seconds / LOOP) * 100).toFixed(2))}%`;

/** Collects the opacity keyframes for elements that come and go during the loop. */
class Timeline {
  rules: string[] = [];

  private add(frames: string, restingVisible: boolean): string {
    const name = `u-k${this.rules.length / 2 + 1}`;
    this.rules.push(`@keyframes ${name}{${frames}}`, `.${name}{animation:${name} ${LOOP}s linear infinite}`);
    return restingVisible ? name : `${name} u-gone`;
  }

  /** Visible from start to end. restingVisible is the state without animation. */
  show(start: number, end = T.clear, restingVisible = true): string {
    return this.add(
      `0%,${pct(start)}{opacity:0}${pct(start + FADE)},${pct(end)}{opacity:1}${pct(end + FADE)},100%{opacity:0}`,
      restingVisible,
    );
  }

  /** Visible except from start to end. */
  hide(start: number, end: number): string {
    return this.add(
      `0%,${pct(start)}{opacity:1}${pct(start + FADE)},${pct(end)}{opacity:0}${pct(end + FADE)},100%{opacity:1}`,
      true,
    );
  }
}

/** The theme's own background scene, resized from viewport units to this window. */
function scene(dataUri: string): { style: string; svg: string } {
  let svg = dataUri.slice(dataUri.indexOf(",") + 1).replaceAll("%23", "#");
  svg = svg.replace(/(\d*\.?\d+)v([wh])\b/g, (_, value: string, axis: string) => {
    const px = (Number(value) * (axis === "w" ? AREA.w : AREA.h)) / 100;
    return `${Number(px.toPrecision(6))}px`;
  });
  const style = /<style>(.*?)<\/style>/s.exec(svg)?.[1] ?? "";
  svg = svg.replace(/<style>.*?<\/style>/s, "");
  const opening = "<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'>";
  if (!svg.startsWith(opening)) throw new Error("scene.svg no longer starts with the expected <svg> tag");
  return { style, svg: `<svg x='${AREA.x}' y='${AREA.y}' width='${AREA.w}' height='${AREA.h}'>` + svg.slice(opening.length) };
}

export function renderMockup(sceneDataUri: string, theme: Theme): string {
  const ink = theme.colors.text;
  const muted = theme.colors.textMuted;
  const tl = new Timeline();
  const cx = AREA.x + AREA.w / 2;

  /** The CSS layers under the scene: sky gradient, grid lines, striped sun. */
  const sky = (): string => {
    const stripes = Array.from(
      { length: 10 },
      (_, i) => `<rect x='${cx - 320}' y='${H - 300 + 22 + 30 * i}' width='640' height='8'/>`,
    ).join("");
    return (
      `<rect x='${AREA.x}' y='${AREA.y}' width='${AREA.w}' height='${AREA.h}' fill='url(#u-sky)'/>` +
      `<rect x='${AREA.x}' y='${AREA.y}' width='${AREA.w}' height='${AREA.h}' fill='url(#u-grid)'/>` +
      `<g clip-path='url(#u-sunbox)'><circle cx='${cx}' cy='${H}' r='452.5' fill='url(#u-sun)'/></g>` +
      `<g fill='#ffd6e0' opacity='.95'>${stripes}</g>`
    );
  };

  const sidebar = (): string => {
    const out = [
      `<rect width='${SIDEBAR}' height='${H}' fill='url(#u-side)'/>`,
      // Window controls and app title.
      "<circle cx='17' cy='18' r='5.5' fill='#ff5f57'/><circle cx='35' cy='18' r='5.5' fill='#febc2e'/>" +
        "<circle cx='53' cy='18' r='5.5' fill='#28c840'/>",
      icon("panel-left", 70, 11.5, 13, muted),
      text(92, 22, "T3", { fill: ink, weight: 800 }),
      text(109, 22, "Code", { fill: muted }),
      icon("arrow-left", 144, 12, 12, FAINT),
      icon("arrow-right", 164, 12, 12, FAINT),
      // Search row.
      icon("search", 12, 44, 13, muted),
      text(32, 54.5, "Search", { fill: muted, weight: 600 }),
      icon("list-filter", 164, 44.5, 12, muted),
      icon("folder-plus", 183, 44.5, 12, muted),
      icon("square-pen", 202, 44.5, 12, muted),
    ];

    const thread = (y: number, project: string, age: string, title: string, branch = "", projectIcon: IconName = "folder") => {
      out.push(icon(projectIcon, 12, y - 8.5, 10, FAINT));
      out.push(text(27, y, project, { size: 10, fill: FAINT }));
      out.push(text(212, y, age, { size: 10, fill: FAINT, anchor: "end" }));
      out.push(text(12, y + 17, title, { fill: muted }));
      if (branch) out.push(text(12, y + 31, branch, { size: 10, fill: FAINT }));
    };
    thread(84, "acme-web", "12m", "Fix flaky checkout test", "main");
    thread(140, "No project", "40m", "Plan the team offsite", "", "square-dashed");
    thread(182, "billing-api", "2h", "Refactor webhook retries", "retry-queue");

    // Lower groups: the open thread, then the settled ones.
    const busy = tl.show(T.send, T.reply, false);
    const idle = tl.hide(T.send, T.reply);
    out.push(
      text(12, 652, "Working", { size: 10.5, fill: muted, weight: 600 }),
      text(196, 652, "1", { size: 10.5, fill: muted, anchor: "end" }),
      icon("chevron-down", 201, 643, 10, FAINT),
      `<rect x='6' y='664' width='${SIDEBAR - 14}' height='44' rx='8' fill='${theme.colors.sidebarRowActive}'/>`,
      icon("square-dashed", 12, 670.5, 10, FAINT),
      text(27, 679, "No project", { size: 10, fill: FAINT }),
      text(12, 697, "Install a sunset theme", { fill: ink, weight: 600 }),
      `<g class='${busy}'>` +
        `<g transform='translate(143 675.5)'><g class='u-spin'>${icon("loader", -5, -5, 10, "#3b5bff", { width: 2.4 })}</g></g>` +
        text(212, 679, "Working", { size: 10, fill: "#3b5bff", weight: 700, anchor: "end" }) +
        "</g>",
      text(212, 679, "now", { size: 10, fill: FAINT, anchor: "end", cls: idle }),
      text(12, 734, "Settled", { size: 10.5, fill: muted, weight: 600 }),
      text(196, 734, "3", { size: 10.5, fill: muted, anchor: "end" }),
      icon("chevron-right", 201, 725, 10, FAINT),
      icon("settings", 12, 772, 13, muted),
      icon("git-branch", 36, 772, 13, muted),
      icon("chart", 60, 772, 13, muted),
      icon("refresh", 199, 772, 13, muted),
      // Violet edge with a soft glow.
      `<rect x='${SIDEBAR - 8}' width='8' height='${H}' fill='url(#u-edge)'/>`,
      `<rect x='${SIDEBAR - 2}' width='2' height='${H}' fill='${VIOLET}'/>`,
    );
    return out.join("");
  };

  const header = (): string => {
    const x = SIDEBAR;
    return [
      `<rect x='${x}' width='${W - x}' height='${HEADER}' fill='#fff' fill-opacity='.86'/>`,
      `<rect x='${x}' y='${HEADER - 2}' width='${W - x}' height='8' fill='url(#u-hglow)'/>`,
      `<rect x='${x}' y='${HEADER - 2}' width='${W - x}' height='2' fill='${PINK}'/>`,
      icon("square-dashed", x + 14, 11, 11, FAINT),
      text(x + 31, 21.5, "No project", { size: 11.5, fill: FAINT }),
      text(x + 109, 21.5, "/", { size: 11.5, fill: FAINT }),
      text(x + 125, 21.5, "Install a sunset theme", { size: 11.5, fill: ink, weight: 600 }),
      `<rect x='${W - 80}' y='7' width='20' height='20' rx='5' fill='#ffd0e8'/>`,
      icon("panel-details", W - 76, 11, 12, ink),
      icon("panel-bottom", W - 52, 11, 12, muted),
      icon("panel-right", W - 28, 11, 12, muted),
    ].join("");
  };

  /** The thread details card on the right. */
  const details = (): string => {
    const x = W - 186;
    const y = HEADER + 10;
    const w = 176;
    const out = [
      `<rect x='${x}' y='${y}' width='${w}' height='152' rx='12' fill='#fad7e6' fill-opacity='.9' stroke='#f3bfd9'/>`,
      icon("laptop", x + 12, y + 12, 12, muted),
      text(x + 32, y + 22, "Studio Mac", { size: 11, fill: ink, weight: 600 }),
      icon("code", x + 12, y + 32, 12, ink),
      text(x + 32, y + 42, "Open in editor", { size: 11, fill: ink, weight: 600 }),
      icon("chevron-down", x + w - 22, y + 33, 10, muted),
      icon("plus", x + 12, y + 52, 12, muted),
      text(x + 32, y + 62, "Add project script", { size: 11, fill: ink, weight: 600 }),
    ];
    const meter = (rowY: number, label: string, share: number, value: string, barX = 76, barW = 58) => {
      out.push(text(x + 12, rowY, label, { size: 9.5, fill: FAINT }));
      out.push(`<rect x='${x + barX}' y='${rowY - 4}' width='${barW}' height='2' rx='1' fill='#d9c4dd'/>`);
      out.push(`<rect x='${x + barX}' y='${rowY - 4}' width='${r1(barW * share)}' height='2' rx='1' fill='#5d3f86'/>`);
      out.push(text(x + w - 12, rowY, value, { size: 9.5, fill: muted, anchor: "end" }));
    };
    meter(y + 90, "Session", 0.38, "38%");
    meter(y + 106, "Weekly", 0.12, "12%");
    meter(y + 136, "Context", 0.12, "24k / 200k", 62, 40);
    return out.join("");
  };

  const conversation = (): string => {
    const out: string[] = [];
    const x = COL_X;

    // User message, right-aligned.
    const bubbleW = textWidth(PROMPT, 12) + 32;
    const bx = COL_R - bubbleW;
    out.push(
      `<g class='${tl.show(T.send)}'>` +
        `<rect x='${bx + 2}' y='72' width='${bubbleW - 4}' height='34' rx='16' fill='${PINK}' opacity='.35' filter='url(#u-blur6)'/>` +
        `<path d='M${bx + 18} 62H${COL_R - 18}a18 18 0 0 1 18 18v12a4 4 0 0 1-4 4H${bx + 18}a18 18 0 0 1-18-18a18 18 0 0 1 18-18Z' fill='url(#u-bubble)'/>` +
        text(bx + 16, 83.5, PROMPT, { fill: ink }) +
        "</g>",
    );

    // Work log, indented to line up with the text inside the reply card.
    const small = { size: 11, fill: FAINT };
    const wx = x + 22;
    out.push(text(wx, 132, "Working for 3s", { ...small, cls: tl.show(T.work, T.reply, false) }));
    out.push(
      `<g class='${tl.show(T.reply)}'>` +
        text(wx, 132, "Worked for 3s", small) +
        icon("chevron-right", wx + textWidth("Worked for 3s", 11) + 5, 123, 10, FAINT) +
        "</g>",
    );
    out.push(`<g class='${tl.show(T.tool1)}'>${icon("terminal", wx, 145, 11, FAINT)}${text(wx + 18, 154.5, "Ran 2 commands", small)}</g>`);
    out.push(`<g class='${tl.show(T.tool2)}'>${icon("wrench", wx, 167, 11, FAINT)}${text(wx + 18, 176.5, "Set the theme", small)}</g>`);

    // Assistant reply card. Its parts are revealed one after another.
    const cy = 192;
    const ch = 208;
    const tx = x + 22;
    const card = [
      `<rect x='${x + 14}' y='${cy + 26}' width='${COL_W - 28}' height='${ch - 20}' rx='16' fill='${VIOLET}' opacity='.4' filter='url(#u-blur10)'/>`,
      `<rect x='${x - 4}' y='${cy - 4}' width='${COL_W + 8}' height='${ch + 8}' rx='20' fill='#fff' opacity='.45'/>`,
      `<rect x='${x}' y='${cy}' width='${COL_W}' height='${ch}' rx='16' fill='#fff' fill-opacity='.96' stroke='#f1c4e1'/>`,
    ];
    const line = (delay: number, body: string) => card.push(`<g class='${tl.show(T.reply + delay)}'>${body}</g>`);

    const title = { size: 14, fill: PINK, weight: 800, spacing: 1.1 };
    line(
      0.2,
      text(tx, cy + 33, "GRAND THEFT CODE IS ON", { ...title, cls: "u-tube", extra: "font-style='italic' filter='url(#u-blur4)' opacity='.75'" }) +
        text(tx, cy + 33, "GRAND THEFT CODE IS ON", { ...title, extra: "font-style='italic'" }),
    );
    line(
      0.5,
      text(tx, cy + 60, "The theme file is in your themes folder and T3 Code has switched to it.", { fill: ink }) +
        text(tx, cy + 80, "Nothing else was changed.", { fill: "#c4006a", weight: 700 }),
    );
    line(
      0.8,
      `<circle cx='${tx + 3}' cy='${cy + 104}' r='1.7' fill='${ink}'/>` +
        text(tx + 14, cy + 108, "Palms sway, clouds drift and a plane crosses the sky every 75 seconds.", { fill: ink }),
    );
    // The second bullet holds an inline code chip.
    const chipX = tx + 14 + textWidth("The ", 12);
    const chipW = textWidth("VI", 12) + 10;
    line(
      1.1,
      `<circle cx='${tx + 3}' cy='${cy + 126}' r='1.7' fill='${ink}'/>` +
        text(tx + 14, cy + 130, "The", { fill: ink }) +
        `<rect x='${r1(chipX - 2)}' y='${cy + 118}' width='${r1(chipW)}' height='17' rx='6' fill='${ink}'/>` +
        text(chipX + 3, cy + 130, "VI", { fill: "#7df3ff" }) +
        text(chipX + chipW + 2, cy + 130, "badge floats in the corner. Ask for the clean variant to drop it.", { fill: ink }),
    );
    line(
      1.4,
      `<rect x='${tx}' y='${cy + 148}' width='${COL_W - 44}' height='40' rx='12' fill='${CYAN}' opacity='.5' filter='url(#u-blur6)'/>` +
        `<rect x='${tx}' y='${cy + 148}' width='${COL_W - 44}' height='40' rx='12' fill='${theme.colors.codeBackground}' stroke='${CYAN}' stroke-width='2'/>` +
        text(tx + 16, cy + 172, 't3_theme_set({ themeId: "grand-theft-code", appearance: "light" })', { size: 11.5, fill: ink }),
    );
    out.push(`<g class='${tl.show(T.reply)}'>${card.join("")}</g>`);

    // Message actions under the reply.
    const my = cy + ch + 12;
    out.push(
      `<g class='${tl.show(T.reply + 1.7)}'>` +
        icon("copy", x + 4, my, 11, FAINT) +
        icon("git-branch", x + 28, my, 11, FAINT) +
        icon("reply", x + 52, my, 11, FAINT) +
        text(x + 76, my + 9.5, "09:41", { size: 10, fill: FAINT }) +
        "</g>",
    );
    return out.join("");
  };

  const composer = (): { svg: string; typingRules: string[] } => {
    const x = COL_X;
    const y = 712;
    const w = COL_W;
    const h = 70;
    const bx = x + w - 20;
    const by = y + h - 18;
    const out = [
      // Cyan offset shadow, pink glow, white ring, then the card.
      `<rect x='${x + 10}' y='${y + 12}' width='${w - 4}' height='${h - 4}' rx='15' fill='${CYAN}' opacity='.55'/>`,
      `<rect x='${x - 2}' y='${y - 2}' width='${w + 4}' height='${h + 4}' rx='18' fill='${PINK}' opacity='.75' filter='url(#u-blur10)'/>`,
      `<rect x='${x - 4}' y='${y - 4}' width='${w + 8}' height='${h + 8}' rx='19' fill='#fff' opacity='.9'/>`,
      `<rect x='${x}' y='${y}' width='${w}' height='${h}' rx='15' fill='#fff' fill-opacity='.94' stroke='${PINK}' stroke-width='2'/>`,
      text(x + 16, y + 25, "Ask anything. @ files, $ skills, / commands", { fill: FAINT, cls: tl.hide(T.type - 0.2, T.send) }),
      icon("paperclip", x + 14, y + h - 24, 12, muted),
      icon("spark", x + w - 162, y + h - 24, 12, "#e2733d", { width: 2 }),
      text(x + w - 145, y + h - 14, "Fable 5.2", { size: 11, fill: ink, weight: 600 }),
      text(x + w - 80, y + h - 14, "High", { size: 11, fill: muted }),
      icon("mic", x + w - 46, y + h - 24, 12, muted),
      // Send button: an arrow at rest, a stop square while the agent works.
      `<circle cx='${bx}' cy='${by}' r='10' fill='${PINK}'/>`,
      `<g class='${tl.hide(T.send, T.reply)}'>${icon("arrow-up", bx - 6, by - 6, 12, "#fff", { width: 2.4 })}</g>`,
      `<rect class='${tl.show(T.send, T.reply, false)}' x='${bx - 3.5}' y='${by - 3.5}' width='7' height='7' rx='1.5' fill='#fff'/>`,
    ];

    // The prompt is typed one character at a time, then cleared when it is sent.
    const typingRules: string[] = [];
    const chars: string[] = [];
    const step = (T.send - 0.5 - T.type) / PROMPT.length;
    [...PROMPT].forEach((char, i) => {
      if (char === " ") return;
      const at = T.type + i * step;
      typingRules.push(
        `@keyframes u-c${i}{0%,${pct(at)}{opacity:0}${pct(at + 0.02)},${pct(T.send)}{opacity:1}${pct(T.send + 0.15)},100%{opacity:0}}` +
          `.u-c${i}{animation:u-c${i} ${LOOP}s linear infinite}`,
      );
      chars.push(`<text class='u-c${i} u-gone' x='${r1(x + 16 + i * 12 * ADVANCE)}' y='${y + 25}'>${escapeXml(char)}</text>`);
    });
    out.push(`<g font-size='12' fill='${ink}'>${chars.join("")}</g>`);
    return { svg: out.join(""), typingRules };
  };

  const background = scene(sceneDataUri);
  // Order matters: each call registers its keyframes on the shared timeline.
  const side = sidebar();
  const talk = conversation();
  const box = composer();

  const defs =
    `<clipPath id='u-win'><rect width='${W}' height='${H}' rx='12'/></clipPath>` +
    `<clipPath id='u-sunbox'><rect x='${cx - 320}' y='${H - 320}' width='640' height='320'/></clipPath>` +
    "<linearGradient id='u-side' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#efe4ff'/>" +
    "<stop offset='.55' stop-color='#ffe3f3'/><stop offset='1' stop-color='#ffe9c9'/></linearGradient>" +
    "<linearGradient id='u-sky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#efe4ff'/>" +
    "<stop offset='.4' stop-color='#ffe3f3'/><stop offset='.72' stop-color='#ffd9de'/><stop offset='1' stop-color='#ffe9c9'/></linearGradient>" +
    `<pattern id='u-grid' x='${AREA.x}' y='0' width='44' height='44' patternUnits='userSpaceOnUse'>` +
    `<rect width='1' height='44' fill='${VIOLET}' opacity='.1'/></pattern>` +
    `<radialGradient id='u-sun' gradientUnits='userSpaceOnUse' cx='${cx}' cy='${H}' r='452.5'>` +
    "<stop offset='0' stop-color='#ffe25c' stop-opacity='.85'/><stop offset='.45' stop-color='#ff8a4c' stop-opacity='.75'/>" +
    "<stop offset='.7' stop-color='#ff2e97' stop-opacity='.7'/><stop offset='.705' stop-color='#ff2e97' stop-opacity='0'/></radialGradient>" +
    "<linearGradient id='u-bubble' x1='0' y1='0' x2='1' y2='.35'><stop offset='0' stop-color='#ffe45c'/>" +
    "<stop offset='.5' stop-color='#ffa26b'/><stop offset='1' stop-color='#ff6fb5'/></linearGradient>" +
    `<linearGradient id='u-edge'><stop offset='0' stop-color='${VIOLET}' stop-opacity='0'/><stop offset='1' stop-color='${VIOLET}' stop-opacity='.35'/></linearGradient>` +
    `<linearGradient id='u-hglow' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='${PINK}' stop-opacity='.45'/><stop offset='1' stop-color='${PINK}' stop-opacity='0'/></linearGradient>` +
    "<filter id='u-blur4' x='-20%' y='-60%' width='140%' height='220%'><feGaussianBlur stdDeviation='3'/></filter>" +
    "<filter id='u-blur6' x='-10%' y='-40%' width='120%' height='180%'><feGaussianBlur stdDeviation='6'/></filter>" +
    "<filter id='u-blur10' x='-10%' y='-40%' width='120%' height='180%'><feGaussianBlur stdDeviation='10'/></filter>";

  const style =
    `text{font-family:${FONT};white-space:pre}` +
    ".u-gone{opacity:0}" +
    ".u-spin{animation:u-spin 1.6s linear infinite}@keyframes u-spin{to{rotate:360deg}}" +
    ".u-tube{animation:u-tube 3.2s ease-in-out infinite}@keyframes u-tube{50%{opacity:.25}}" +
    tl.rules.join("") +
    box.typingRules.join("") +
    // The scene's own rules come last: they end with the reduced-motion switch for everything.
    background.style;

  const desc =
    "Animated mock-up of the T3 Code window with the Grand Theft Code theme: a sidebar of threads, " +
    "a chat where an agent installs the theme, and a sunset background with palms and a VI badge.";

  return (
    `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 ${W} ${H}' width='${W}' height='${H}' role='img' aria-labelledby='u-title u-desc'>` +
    `<title id='u-title'>Grand Theft Code theme in T3 Code</title><desc id='u-desc'>${desc}</desc>` +
    `<style>${style}</style><defs>${defs}</defs>` +
    "<g clip-path='url(#u-win)'>" +
    `<rect width='${W}' height='${H}' fill='${theme.canvas}'/>` +
    sky() +
    background.svg +
    talk +
    box.svg +
    details() +
    header() +
    side +
    "</g>" +
    `<rect x='.5' y='.5' width='${W - 1}' height='${H - 1}' rx='12' fill='none' stroke='#2a1050' stroke-opacity='.25'/>` +
    "</svg>\n"
  );
}
