# EncoreMed design baseline

A small, platform-neutral design baseline for EncoreMed products: the brand colours, type, spacing, sizes, component states and component behaviour that make a product look and feel like EncoreMed. It works for web and native apps, and it is written so an **AI coding assistant** can read it and prototype within the design.

It is a baseline, not a framework. Extend it when your product needs more; the guard only reports differences and clear mistakes.

## Quick start

1. **Give your AI assistant this directory** and start with:

   > Use the EncoreMed design baseline in `<path to this directory>`. Read `AGENTS.md`, then `HANDOFF.md`. We are building `<what, and on which platform>`. When you finish, run the guard as `AGENTS.md` describes and report what it says.

2. **Web product:** copy `web/tokens.css` and `web/components.css` into your project and load them in this order: `tokens.css`, your own `app-tokens.css` (optional), `components.css`, your own `app.css`. Use the markup in `HANDOFF.md` section 9.
3. **Native or other product:** generate your platform's constants (colours, spacing, radii, type sizes, durations) from `design-tokens.json`, then build screens from the component specs in `HANDOFF.md` section 5. Section 6 maps the baseline to iOS, Android and desktop.
4. **Check your work** (needs Python 3, no packages):

   ```bash
   python3 guard.py path/to/your/project
   ```

   Any platform: it warns about colours that are not in the design palette and names the closest token. Web projects also get checks for undefined tokens, raw colours, stylesheet order and text contrast.

## What is in this directory

| File | What it is |
|---|---|
| `README.md` | this file |
| `AGENTS.md` | the short rules file the AI assistant follows and re-reads to cross-check its work |
| `HANDOFF.md` | the full guide: brand rules, tokens, component specs, platform mapping, the guard, the web markup catalogue |
| `design-tokens.json` | every value (356 tokens), the portable source for any platform; aliases and resolved values |
| `DESIGN-TOKENS.md` | the same tokens as a readable list |
| `guard.py` | the checker |
| `web/tokens.css`, `web/components.css` | the web reference implementation |
| `web/app.js` | web reference for how the components behave (dropdown, multi-select, pagination, sidebar, staff menu). It contains demo content (Rossmax residents and devices); copy the patterns, not the content. |
| `web/export_tokens.py` | optional: regenerates the token files from `web/tokens.css` if you change it |

## How strict it is

- **Must:** the palette, the typeface, the 4px spacing grid, the control size scale, the radius scale, the five control states (default, hover, pressed in amber, disabled, keyboard focus) and 4.5:1 text contrast.
- **Should:** the component anatomy and behaviour in `HANDOFF.md` section 5.
- **May:** native controls and navigation, new components, dark mode, a new colour for a real need. Tell the user what you added and why.

## Known limits

- The typeface, Acumin Variable, is not included. Without a licence use Arial on web and the system font on native.
- There is no phone layout and no dark mode defined; derive them from the same tokens and components.
- The guard checks colours (every platform) and CSS (web). It cannot judge layout, markup or behaviour; use the hand-check list in `AGENTS.md`.
- The soft grey `ink-400` is only 3.5:1 on white. Use it for placeholders and icons, not for important text.

## For maintainers

`web/tokens.css`, `web/components.css`, `web/app.js`, `web/export_tokens.py`, `design-tokens.json` and `DESIGN-TOKENS.md` are generated copies from the source design-system project. Change them there, rebuild the package, and copy the result here, so the web files and the token files never drift apart. `README.md`, `AGENTS.md`, `HANDOFF.md` and `guard.py` are edited directly in this directory (or, for `AGENTS.md` and `HANDOFF.md`, in the source project, which copies them in).
