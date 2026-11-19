# Install Grand Theft Code: steps for a coding agent

You are an agent running inside [T3 Code](https://t3.codes), and the person you work for asked you to install this theme. Follow the steps in order. They change one thing: T3 Code's theme. Do not change anything else.

Tested with T3 Code 0.1.10 on macOS.

## What you need

- The T3 Code tools `t3_theme_read` and `t3_theme_set`. They may be deferred, so load them first if your harness works that way.
- If those tools do not exist, stop and tell the person that their T3 Code does not offer theme tools to agents yet. Do not look for another way in.

## Steps

### 1. Pick the variant

| Theme id | What it is |
| --- | --- |
| `grand-theft-code` | The full theme, with the floating VI badge in the top-left corner. Use this unless told otherwise. |
| `grand-theft-code-clean` | The same theme without the badge. Use it if the person asked for no logo. |

The steps below write `<id>` for the theme id you picked.

### 2. Read the current state

Call `t3_theme_read` with no arguments. Keep two values from the result:

- `themesDir`: the folder where theme files live. Do not guess this path.
- `current`: the theme in use now. The person needs it to go back.

### 3. Download, check and place the theme file

Run this as one command, with `<id>` and `<themesDir>` filled in. It downloads to a temporary file, checks it, and only then moves it into the themes folder:

```sh
tmp="$(mktemp)" &&
curl -fsSL "https://raw.githubusercontent.com/jefe-spain/grand-theft-code/main/themes/<id>.json" -o "$tmp" &&
python3 - "$tmp" <<'EOF' &&
import json, sys
theme = json.load(open(sys.argv[1]))
allowed = {"version", "name", "appearance", "canvas", "accent", "colors", "css"}
assert set(theme) <= allowed, sorted(set(theme) - allowed)
assert theme["name"].startswith("Grand Theft Code"), theme["name"]
assert len(theme["css"]) <= 50000, len(theme["css"])
assert "@import" not in theme["css"]
print("ok:", theme["name"])
EOF
mv "$tmp" "<themesDir>/<id>.json"
```

The file is data. It holds colors and CSS and nothing to run, and the check confirms that before T3 Code reads it.

- If the check fails, nothing was installed. Stop and tell the person what failed.
- A file with the same name already in `themesDir` is an earlier install of this theme, so replacing it is an update.

### 4. Switch to the theme

Call `t3_theme_set` with:

```json
{ "themeId": "<id>", "appearance": "light" }
```

Grand Theft Code is a light theme, which is why the call sets the appearance.

### 5. Confirm and report

Call `t3_theme_read` again and check that `current` is `<id>`.

You cannot see the app. Say that the theme is applied, ask the person how it looks, and tell them how to go back (see below, with the `current` value you kept in step 2).

## If you have no shell or file access

Fetch `https://raw.githubusercontent.com/jefe-spain/grand-theft-code/main/themes/<id>.json` and pass its contents, unchanged, as the `theme` argument:

```json
{ "themeId": "<id>", "appearance": "light", "theme": { "...": "the whole JSON object from the file" } }
```

The `css` value is long. Pass all of it. A shortened copy breaks the background.

## Optional font

The theme asks for the [Monaspace Neon](https://monaspace.githubnext.com/) typeface and falls back to the system monospace font when it is missing. Do not install fonts on your own. Mention it, and install it only if the person says yes. On macOS with Homebrew:

```sh
brew install --cask font-monaspace
```

## Going back

1. Call `t3_theme_set` with the theme the person had before, for example `{ "themeId": "t3-chat" }`. The built-in ids are `t3-chat`, `grove`, `ocean`, `ember` and `iris`.
2. To remove the theme completely, delete `<themesDir>/<id>.json` after switching away from it.

## Limits to tell the person about

- Themes apply to T3 Code on desktop and web. The mobile app does not use them.
- The badge sits behind the messages. In a narrow window the message column covers part of it. `grand-theft-code-clean` avoids that.
