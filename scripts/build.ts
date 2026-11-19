/**
 * Build the Grand Theft Code themes for T3 Code from the readable sources in src/.
 *
 *   npm run build   write themes/*.json, docs/index.html and assets/mockup.svg
 *   npm run check   fail if any of those files is out of date
 *
 * T3 Code takes a theme as one JSON file whose CSS cannot load other files, so
 * the animated scene has to travel inside the CSS as a data URI. This script
 * does that packing. It has no dependencies; Node runs the TypeScript directly.
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { renderMockup } from "./mockup.ts";

const ROOT = join(import.meta.dirname, "..");
const SRC = join(ROOT, "src");

/** T3 Code refuses theme CSS longer than this. */
const CSS_LIMIT = 50_000;
const SCENE_PLACEHOLDER = "__SCENE__";
const LOGO_MARKER = /^(?:<!--|\/\*)\s*(\/?)logo\s*(?:-->|\*\/)$/;

export interface Theme {
  version: number;
  name: string;
  appearance: "light" | "dark";
  canvas: string;
  accent: string;
  colors: Record<string, string>;
  css: string;
}

const VARIANTS: Record<string, { name: string; logo: boolean }> = {
  "grand-theft-code": { name: "Grand Theft Code", logo: true },
  "grand-theft-code-clean": { name: "Grand Theft Code Clean", logo: false },
};

const read = (file: string): string => readFileSync(join(SRC, file), "utf8");

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

/** Drop the logo marker lines and, for the Clean variant, what sits between them. */
function withoutLogo(text: string, keepLogo: boolean): string {
  const out: string[] = [];
  let inside = false;
  for (const line of text.split("\n")) {
    const marker = LOGO_MARKER.exec(line.trim());
    if (marker) {
      const closing = marker[1] === "/";
      if (closing !== inside) fail(`unbalanced logo marker: ${line.trim()}`);
      inside = !closing;
      continue;
    }
    if (inside && !keepLogo) continue;
    out.push(line);
  }
  if (inside) fail("logo marker never closed");
  return out.join("\n");
}

/** Join lines with nothing between them, dropping indentation and blank lines. */
const joinLines = (text: string): string =>
  text
    .split("\n")
    .map((line) => line.trim())
    .join("");

/** scene.svg as a data URI that is safe inside a double-quoted CSS url(). */
function buildScene(keepLogo: boolean): string {
  let svg = withoutLogo(read("scene.svg"), keepLogo);
  svg = svg.replace(/<!--.*?-->/gs, "").replace(/\/\*.*?\*\//gs, "");
  svg = joinLines(svg);
  if (svg.includes('"')) fail("scene.svg must use single quotes only");
  return "data:image/svg+xml," + svg.replaceAll("#", "%23");
}

function buildCss(keepLogo: boolean): string {
  const source = read("theme.css").replace(/\/\*.*?\*\//gs, "");
  const css = source
    .split(/\n\s*\n/)
    .map(joinLines)
    .filter(Boolean)
    .join("\n");
  if (css.split(SCENE_PLACEHOLDER).length !== 2) {
    fail(`theme.css must contain ${SCENE_PLACEHOLDER} exactly once`);
  }
  return css.replace(SCENE_PLACEHOLDER, () => buildScene(keepLogo));
}

/** Check the rules T3 Code's theme guide sets for the css field. */
function validate(id: string, css: string): void {
  const problems: string[] = [];
  if (css.length > CSS_LIMIT) problems.push(`css is ${css.length} characters, limit is ${CSS_LIMIT}`);
  for (const banned of ["@import", "image-set("]) {
    if (css.includes(banned)) problems.push(`${banned} is not allowed`);
  }
  for (const [, target] of css.matchAll(/url\(\s*([^)]{0,12})/g)) {
    const bare = target.replace(/^["']+/, "");
    if (!["data:", "#", "%23"].some((prefix) => bare.startsWith(prefix))) {
      problems.push(`url() may only point at data: or #id, found "${target}"`);
    }
  }
  if (problems.length) fail(`${id}: ${problems.join("; ")}`);
}

function buildTheme(id: string): Theme {
  const { name, logo } = VARIANTS[id];
  const theme: Theme = { ...JSON.parse(read("theme.json")), name, css: buildCss(logo) };
  validate(id, theme.css);
  return theme;
}

/** Inline both variants into the mock chat page served by GitHub Pages. */
function buildDemo(themes: Record<string, Theme>): string {
  const page = read("demo.html");
  if (page.split("__THEMES__").length !== 2) fail("demo.html must contain __THEMES__ exactly once");
  const payload = JSON.stringify(themes).replaceAll("</", "<\\/");
  return page.replace("__THEMES__", () => payload);
}

function outputs(): Map<string, string> {
  const themes = Object.fromEntries(Object.keys(VARIANTS).map((id) => [id, buildTheme(id)]));
  const files = new Map<string, string>();
  for (const [id, theme] of Object.entries(themes)) {
    files.set(join(ROOT, "themes", `${id}.json`), JSON.stringify(theme) + "\n");
  }
  files.set(join(ROOT, "docs", "index.html"), buildDemo(themes));
  files.set(join(ROOT, "assets", "mockup.svg"), renderMockup(buildScene(true), themes["grand-theft-code"]));
  return files;
}

function main(): void {
  const check = process.argv.includes("--check");
  const stale: string[] = [];
  for (const [path, content] of outputs()) {
    const name = relative(ROOT, path);
    if (check) {
      if (!existsSync(path) || readFileSync(path, "utf8") !== content) stale.push(name);
      continue;
    }
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, content);
    console.log(`wrote ${name} (${content.length.toLocaleString("en-US")} characters)`);
  }
  if (stale.length) fail(`out of date, run npm run build: ${stale.join(", ")}`);
  if (check) console.log("themes, demo and mock-up are up to date");
}

if (import.meta.main) main();
