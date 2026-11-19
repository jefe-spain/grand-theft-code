#!/bin/sh
# Capture the demo page for the README with headless Chrome.
# usage: scripts/screenshots.sh   (macOS: needs Google Chrome and the built-in sips)
set -eu
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
WIDTH=1800
HEIGHT=1040
PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE"' EXIT

shot() { # shot <output.png> <query string>
  rm -f "$1"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$PROFILE" \
    --virtual-time-budget=3000 --window-size=$WIDTH,$((HEIGHT + 120)) \
    --screenshot="$PWD/$1" "file://$PWD/docs/index.html$2" >/dev/null 2>&1 &
  pid=$!
  # Headless Chrome can linger after writing the file, so wait for the file, not the process.
  i=0
  while [ ! -s "$1" ] && [ "$i" -lt 60 ]; do sleep 1; i=$((i + 1)); done
  sleep 1
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  [ -s "$1" ] || { echo "failed to render $1" >&2; exit 1; }
  # The headless viewport is shorter than the window, which leaves an empty strip
  # at the bottom. The page is pinned to HEIGHT in shot mode, so crop to it.
  sips --cropOffset 1 1 -c "$HEIGHT" "$WIDTH" "$1" >/dev/null
  echo "wrote $1"
}

shot assets/preview-clean.png "?shot=$HEIGHT&variant=clean"
