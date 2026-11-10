# Rules for AI assistants using the EncoreMed design baseline

You were pointed at this directory because the user is building a product (web or native) that should look and feel like EncoreMed. This directory is a **baseline**, not a framework: your job is to **stay within the ballpark** of it. Read this file first, then `HANDOFF.md`. Re-read the checklist at the bottom before you tell the user you are done.

## If the user gives you colour codes
If the user pastes colours or a logo, or asks you to change, re-brand or re-theme the colours (for a client, for example), **stop and read `THEMING.md` first, then follow it step by step.** Do not edit colours by hand in the project's files, and do not change `tokens.css` or `components.css`. In short: run `make_theme.py` with the pasted colours (for a logo, first run `logo_colours.py` to read its colours and confirm them with the user; never estimate colours by eye), load the resulting theme file, run `guard.py`, and report what you set. Red, orange and green (the status colours) never change.

## What is here
- `HANDOFF.md`: the full guide: brand rules, tokens, platform-neutral component specs, how to translate to each platform.
- `design-tokens.json`: every value (colours, sizes, spacing, radii, type, shadows, durations), the portable source. `DESIGN-TOKENS.md`: the same, readable.
- `THEMING.md`: the step-by-step playbook for changing colours (read it whenever colours are mentioned). `make_theme.py`: creates the theme file from the colours the user pasted. `logo_colours.py`: reads the colours of a client's logo (SVG or PNG). `theme.example.css` and `theme.example.json`: theme templates.
- `guard.py`: the checker. Run it against the user's project.
- `web/`: the web reference implementation (CSS, and JS for behaviour). Only for web products.

## Stay within the ballpark: must, should, may
- **Must** (do not deviate): the status colours (red, orange, green); the palette colours (EncoreMed's by default; see client themes below); the typeface and weights; the 4px spacing grid; the control size scale (32, 36, 40, 44, 48); the radius scale; the five control states (default, hover, pressed in amber, disabled, keyboard focus); 4.5:1 text contrast.
- **Should** (follow unless the platform or the user's goal says otherwise): the component anatomy and behaviour in `HANDOFF.md` section 5; the screen patterns; the wording style.
- **May**: use native or platform controls and navigation, add new components, add dark mode, add a colour for a real need. A native app should feel native: restyle the platform's controls with the tokens instead of rebuilding them to copy the web version.
- When you go beyond the baseline, keep its spirit (same palette family, sizes from the scale, the five states) and **tell the user what you added and why**.
- **Client themes:** if the product is for a client with its own brand colours, put them in a **theme file** (`theme.css` on web, `theme.json` on any platform), created with `make_theme.py` as described in `THEMING.md`. Raw colours are allowed there and nowhere else. You may change brand colours, shades, text, surface and pressed colours. You may **not** change the status colours (red, orange, green) or any non-colour token. Change the main brand colour and its shades together and keep 4.5:1 contrast. You do not need to ask first, but tell the user which colours you themed.
- **Ask the user first** before changing the control size scale or the typeface, or before removing a baseline token or class.

## How to build
1. Take every colour, size, spacing and radius from the tokens (`design-tokens.json`). Do not type a colour or a control height from memory or invent one. Keep the token names in your code.
2. **Web:** copy `web/tokens.css` and `web/components.css` into the project and use the markup in `HANDOFF.md` section 9. Load order: `tokens.css`, `theme.css` (a client's colours, if any), `app-tokens.css` (the project's own), `components.css`, `app.css` (the project's own). You may extend or modify the two shared files; add new tokens and classes rather than renaming or deleting existing ones.
3. **Native or other:** generate constants from `design-tokens.json` (colours, spacing, radii, type sizes, durations) in the platform's idiom (see `HANDOFF.md` section 6), then build screens from the component specs in section 5.
4. Do not copy this demo's fictional data or names (Rossmax, residents, devices) into the new product.

## When sources disagree
If `HANDOFF.md`, the tokens and the user's request disagree: the tokens are the truth for values; the user's request decides what to build. Do not silently follow whichever is easier. Tell the user about the mismatch and what you chose.

## Cross-check: do this before you say you are done
1. Run `python3 <this directory>/guard.py <the user's project folder>`.
2. Fix every `ERROR` (web projects). Do not edit `guard.py` to make it pass.
3. Read every `warning` and `note`. A warning about a colour that is not in the palette means you typed or invented a colour: use the nearest token it names, put it in the client theme if it is a client brand colour, or explain to the user why a new colour was needed. A theme error about a status colour means you tried to change red, orange or green: do not. Notes describe how a web project's `tokens.css` and `components.css` differ from the baseline; make sure each difference is something you meant and told the user about.
4. Check by hand (the script cannot see these):
   - Do all colours, sizes, spacing and radii trace back to a token?
   - Does every interactive control have all five states, with amber for pressed?
   - Is every control usable without a pointer, with an accessible name and a visible focus state?
   - Is text at least 4.5:1 contrast? Are green and mint used only for fills, dots and icons, never for text?
   - Are touch targets at least 44×44 on touch platforms?
   - Did I check the screen at tablet width and at a large width, and (if there is a sidebar or navigation) in both its states?
   - Did the components I built behave like their specs in `HANDOFF.md` section 5 (for example, pagination shows First, Previous, five numbers, Next, Last)?
5. Report to the user: what you built, what the guard said, and anything you added or changed beyond the baseline.
