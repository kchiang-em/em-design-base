# Theming procedure: re-colouring a product for a client

**For AI assistants.** This procedure implements the client theme policy, UI-5 (`../policy/UI-5-client-themes.md`). Read that policy first: it says what a theme may and may not change; this file says how to do it. Follow this when the user gives you colour codes **or a logo**, or asks to change, re-brand or re-theme the colours of a product built on the EncoreMed design baseline. Typical requests:

> "Change the colours to the client's: primary #AABBCC, secondary #DDEEFF."
> "Here are the brand colours for ACME: …"
> "Make the app use our blue instead of the navy."
> "Here is the client's logo: match the app to it." (see section 3b)

Do **not** search the project and replace colours by hand. Use the steps below: they keep the result consistent, accessible, and valid for the guard.

## 1. The rules this procedure follows

The rules are in UI-5; this list only names them. Cite them by ID when you report.

| Clause | Subject |
|---|---|
| THM-1 | client colours live in the project's own token file |
| THM-2 | what a theme may change |
| THM-3 | status colours never change |
| THM-4 | only colours are themed |
| THM-5 | the main colour and its shades change together |
| THM-6 | contrast holds (ACC-6) |
| THM-7 | extra client colours |
| THM-8 | the pressed state stays amber |
| THM-9 | a primary close to a status colour |
| THM-10 | where theme colours come from (codes, logos) |
| THM-11 | the client logo is an asset |
| THM-12 | out of a theme's scope |
| THM-13 | report the theme |

In practice: use `make_theme.py` to derive the colours (THM-5), never invent shades by hand, and finish by running `guard.py` and reporting (section 6).

## 2. Step by step

**Step 1. Understand what was pasted** (section 3). Convert every colour to hex first (`rgb(122,31,61)` becomes `#7A1F3D`). If the user gives a colour **name** ("burgundy") or a brand name, ask for the hex code; do not guess (THM-10). If the user gives a **logo**, go to section 3b first and come back to step 2 with the confirmed colours.

**Step 2. Run the tool** from the project folder (needs Python 3, no packages):

```bash
python3 <handoff directory>/tools/make_theme.py --primary "<hex>" [options] --css app-tokens.css    # web
python3 <handoff directory>/tools/make_theme.py --primary "<hex>" [options] --json app-tokens.json  # native or any platform
```

| Option | Use it for | Becomes |
|---|---|---|
| `--primary` (required) | the client's main brand colour: buttons, sidebar, links | `em-navy-core` and all the brand shades |
| `--secondary` | a second brand colour: active navigation item, gradient lift | `em-blue` (default: a slightly lighter primary) |
| `--heading` | the colour of headings | `em-navy` (default: the primary) |
| `--text` | body text | `em-grey-dark` (default: unchanged) |
| `--muted-text` | secondary text and labels | `em-slate` (default: unchanged) |
| `--background` | page background | `em-grey-light` (default: unchanged) |
| `--accent` | the client's accent colour, replacing the EncoreMed brand green: navigation edge and toggle, logo tile, switch on, level bars. Never a status colour | `em-green-core` and the accent shades (default: unchanged) |
| `--extra name=hex` | another client colour with no EncoreMed role (repeat as needed) | a new token `--client-<name>` |
| `--adjust` | primary is too light for white text: darken it until it passes (otherwise the tool stops and suggests a colour) | |

The tool derives the rest of the brand scale from the primary colour (hover shade, dark surfaces, light tints), re-tints the shadows (the focus ring follows the primary by itself), checks contrast, and prints a table of what it set. **Keep that table: it is the core of your report.**

**Step 3. Read the tool's messages.**
- `ERROR ... contrast`: do not ship it. Ask the user for a darker or lighter colour, or confirm the tool's suggested colour (then run again with `--adjust`).
- `NOTE: primary hue is close to a status colour`: it is allowed, but tell the user (THM-9). Because the status colours cannot change, errors, warnings and success messages can look like the brand. Keep an icon and a text label on every status message; never rely on colour alone.
- `NOTE: ... sidebar toggle label ... darkened`: normal. The label sits on the EncoreMed brand green, so the tool darkened only that label.

The tool writes the colours into the project's own token file as one marked "brand colours" block (CSS) or as `colors` entries (JSON), creating the file if needed. Running it again replaces that block and leaves the project's other tokens alone. Do not edit inside the block: run the tool again.

**Step 4. Apply the theme.**
- **Web:** make sure every page loads `app-tokens.css` right after `tokens.css`: `tokens.css`, `app-tokens.css`, `components.css`, `app.css`. The component styles follow automatically. No other CSS change is needed.
- **Native or other:** generate your platform's colour constants from `design-tokens.json` with `app-tokens.json` on top. For every colour token in `design-tokens.json`: if `app-tokens.json` has that name, use its value; otherwise, if the token is an alias such as `{brand-600}`, resolve it using the *themed* values; otherwise use its own value. Keep the token names in your code. Then follow `IMPLEMENTATION.md` section 5 for the platform.

**Step 5. Remove hard-coded EncoreMed colours from the project's own code.** The old navy and blue may be written directly in the project's files. Search for them and replace each with the matching token (web: `var(--brand-600)`, `var(--brand-500)`; native: your generated constant):

```bash
grep -rniE "023c6e|16537a|0e4473|01305a|012646|011c34|01121f|2 60 110" <project folder> --include=* --exclude-dir=node_modules --exclude-dir=.git
```

Colours that are not in the palette at all will be reported by the guard in step 6. Do not paste a client colour into the project's own code: add it to the token file (with `--extra`) and refer to the token.

**Step 6. Run the guard** and fix everything it reports:

```bash
python3 <handoff directory>/tools/guard.py <project folder>
```

**Step 7. Check the screens** (look at them if you can run the product; otherwise say you could not). Verify on each: the primary button (default, hover, pressed in amber, disabled), the navigation or sidebar and its active item, a text field in focus (the focus ring), a table or list with hover, a dropdown open, a modal, the login or splash screen, and status pills or messages (they must still be red, orange, status green or information blue). Check that nothing is unreadable.

**Step 8. Report** (section 6).

## 3. Interpreting what the user pastes

| The user gives you | What you do |
|---|---|
| one colour | it is the **primary** |
| two colours, labelled "primary" and "secondary" | use the labels |
| two unlabelled colours | the darker or more saturated one is the primary, the other is the secondary. **Say which you assumed.** |
| three or more colours | very light neutral becomes `--background`; dark neutral becomes `--text`; the main brand colour is the primary; a second brand colour is the secondary; a bright or light brand colour that suits highlights (the role EncoreMed's green plays) can be the `--accent`; **every other colour becomes an `--extra`**. Do not invent roles for them. |
| "accent" or "highlight" colour | `--extra`, used for decoration or brand emphasis only. Never for a status. |
| a colour for "success", "error" or "warning" | do not apply it. Explain that status colours are universal (THM-3). |
| a colour for a specific part ("sidebar blue", "link colour") | the sidebar and links are the primary; a different sidebar colour is a design change, so ask the user. |
| a logo (SVG or PNG file) instead of colour codes | go to section 3b: measure the colours from the file, confirm them with the user, then continue |
| a gradient, illustration or photo | out of scope for a theme (THM-12): imagery is an asset the client supplies. Tell the user. |
| a typeface | not part of a colour theme (THM-12). A product may choose its typeface within FND-5: check it against those rules and tell the user. |
| a request for dark mode | not defined by the baseline (FND-15, THM-12); tell the user it is a separate piece of work. |

When something is genuinely ambiguous (which of two colours is the primary), pick the most likely one, state it, and make it easy to swap by running the tool again.

## 3b. When the user gives a logo instead of colour codes

A logo is a reliable source of the brand colours, **if you measure them from the file and not by eye**. Colours judged from how an image looks are unreliable (anti-aliasing, JPEG blur, screen colour). Never write a hex code you only estimated (THM-10).

1. **Get the file.** You need the logo as a file you can read, ideally **SVG** (exact colours) or **PNG**. If the user pasted or attached the image in the chat, first check whether your tool saved it to disk (look for a file path in the attachment information, a temporary or attachments folder, or ask your tool): if there is a path, use it. If the image exists only in the conversation and there is no file, you can see it but you cannot measure it, so ask the user to save it and give you the path, or to give you the colour codes. You may look at the image to sanity-check your measurement, but never use your own visual estimate as the colour value. Screenshots of a logo are a weaker source than the logo file itself (they are often recompressed or colour-shifted).
2. **Measure the colours with a short script you write** (any language; in Python, the standard library can read SVG, and Pillow, if installed, reads PNG and JPEG). It must:
   - **SVG:** collect the `fill` and `stroke` colours (hex, `rgb()`, named colours) from attributes and `style`, and count how many shapes use each;
   - **PNG or JPEG:** count the colours of the opaque pixels;
   - set aside the background and neutrals: transparent pixels, near-white (lightness above about 93%) and low-saturation greys and blacks (report the neutrals separately; they are usually the wordmark);
   - merge near-identical colours (anti-aliased edges and JPEG noise are shades of the real colour), and drop groups under about 3% of the coloured pixels;
   - list the remaining colours, most prominent first, with their hex code, their share of the logo, and the contrast of white text on them (4.5:1 or more means it can be a primary).
3. **Confirm with the user before applying** (THM-10). The most prominent colour is not always the brand colour, and a logo can contain colours that are not meant for an interface. Show the candidates and your proposed roles in one short message, for example: "Your logo uses #7A1F3D (about 70%) and #F2A900 (about 20%). I plan to use #7A1F3D as the primary and keep #F2A900 as an extra accent colour, because it is too light for white text. Is that right?" If the user said to just use the logo, go ahead, state the assumption, and make it easy to change.
4. **Run `make_theme.py` with the confirmed colours** and continue with step 3 onwards in section 2. A colour too light for white text can be the `--accent`, or an `--extra`.

Cases:

| Situation | What to do |
|---|---|
| the logo is black, white or grey only (the tool exits with "no brand colour") | there is no colour to theme with: ask the user for the client's brand colour codes |
| the main logo colour is too light for white text (a yellow or light blue logo) | it cannot be the primary as is. Offer a darker version of the same hue (`make_theme.py --adjust` finds the nearest one), or use it as an `--extra` accent and ask for a darker primary. Tell the user which you did |
| the logo has several colours | the largest dark colour is usually the primary; one more colour that carries white text may be the secondary; every other colour becomes an `--extra`. Do not try to use them all |
| a gradient logo | the tool reports the dominant shades; ask the user which one is the brand colour |
| an SVG | shares are by number of shapes, not area; treat the ranking as approximate |
| a JPEG, or a low-resolution PNG | colours can be slightly off from compression; round to the obvious brand value if the user confirms it |
| several logo variants (colour, white, black) | use the colour version for extraction |

**The logo itself is an asset, not a token (THM-11).** Extracting its colours does not place it in the product. If the user also wants the client's logo in the interface, that is a separate task: put the file where the product keeps its logo (on web, the sidebar and login panel; on native, the asset catalogue), keep its proportions and clear space, never recolour or stretch it, and say if its shape (a wide wordmark) does not fit the fixed logo tile and needs a design decision.

## 4. Which tokens a theme touches (THM-2 to THM-4)

| Changes with a theme | Never changes |
|---|---|
| primary and its shades (buttons, sidebar, links, focus, hover, dark surfaces, tints) | status colours: red `danger-*`, orange `warning-*`, status green `success-*`, information blue `info-*` |
| the brand greens (`em-green*`, `em-mint`, `accent-*`), when the client has an accent colour: `make_theme.py --accent` | |
| secondary (active navigation item, gradients) | sizes, spacing, radii, type scale |
| headings, text, secondary text, page background (only if the user gave them) | the five control states and their structure |
| the shadow tints (the focus ring follows the primary automatically) | the amber **pressed** colour, unless the user asks (see below) |
| extra client colours (`--client-<name>`) | |

**Pressed state (THM-8):** it stays amber by default. If the client's brand is itself amber, orange or yellow, the pressed state becomes hard to tell from normal; tell the user, and only change the `amber-*` colours if they ask, keeping the pressed text readable (4.5:1).

**Extra client colours** (`--client-<name>`, THM-7): use them as `var(--client-<name>)` in the product's own CSS, or as a generated constant natively. Keep them out of status messages, and keep text on them at 4.5:1.

## 5. If you cannot run the tool

Write the theme by hand with these rules (they are what the tool does). `p` is the primary colour in HSL:

| Token | How to get it |
|---|---|
| `em-navy-core` | the primary |
| `brand-700` (hover) | the primary with its lightness multiplied by 0.82 |
| `brand-800` | lightness × 0.64 |
| `brand-900` | lightness × 0.48 |
| `brand-950` | lightness × 0.27 |
| `brand-50`, `-100`, `-300`, `-400` | the primary mixed with white, keeping 6%, 16%, 45% and 70% of the primary |
| `em-blue` | the secondary, or the primary with lightness + 0.06 (it must still carry white text at 4.5:1) |
| `em-navy` | the heading colour, or the primary |
| `shadow-md`, `shadow-brand` | keep the shape, replace the rgb colour with the primary at the same opacity (14%, 22%). The focus ring needs no entry: it is drawn from `brand-600`. |
| `shadow-lg` | the same, using `brand-900` at 26% |

Check: white on the primary, on `brand-700` and on `em-blue` all at least 4.5:1; headings on white at least 4.5:1; and `nav-toggle-fg` (default `brand-800`) on the brand green `#16AD85` at least 4.5:1, otherwise set `nav-toggle-fg` and `nav-toggle-fg-hover` to a darker colour. Then run the guard.

## 6. What to tell the user (THM-13)

Report in this order, briefly:
1. **What you set:** the mapping table the tool printed (role, token, value), and which colour you treated as primary and secondary if the user did not say.
2. **What you did not change, and why:** status colours (universal), sizes and states.
3. **If you worked from a logo:** the colours you extracted, which you treated as primary, secondary and extras, and whether the user confirmed them.
4. **Warnings you raised:** a primary close to a status colour, a colour you darkened or adjusted (with the before and after), anything you could not do (logo, fonts, dark mode, imagery).
5. **The guard result**, and what you replaced in the project's own code.
6. **What you could not verify** (for example, you did not run the product to look at the screens).

## 7. Mistakes to avoid
- Typing a client hex code anywhere except the project's token file.
- Estimating colours by eye from a logo or screenshot instead of measuring them from the file (section 3b).
- Editing `tokens.css` or `components.css` to change colours, or editing inside the generated block by hand. Run `make_theme.py`.
- Overriding a status colour because it "looks off" next to the brand colour.
- Skipping the shades: changing only the primary leaves EncoreMed navy in hover and tinted states (the guard warns about this).
- Shipping a primary colour that fails contrast with white text.
- Using green or mint for text, or an `--extra` colour for a status.
- Reporting "done" without running the guard.

## 8. If the guard or tool complains

Guard messages start with the clause they check, for example `[THM-3]`.

| Message | Meaning and fix |
|---|---|
| `[THM-3] --x is a status colour ... cannot change it` | remove the override from the token file |
| `[SCP-4] project token --x ... looks like --y: a typo?` | a misspelt token name: fix it, or ignore it if it really is a new token |
| `[SCP-3] --x must be a colour` | the override's value is not a hex, `rgb()`, `hsl()` or `var()` colour |
| `[THM-5] the brand colours were changed but these related shades were not` | run `make_theme.py` instead of editing by hand |
| `[THM-1] theme.css is from an older package` | move its contents into `app-tokens.css` (or `theme.json` into `app-tokens.json`), or simply run `make_theme.py` again |
| `contrast ... needs 4.5:1` | pick a darker or lighter colour; the message names the pair |
| `colour #xxxxxx is not in the design palette` | a colour in the project's code that is not a token: use the token it names, or add the colour to the token file with `--extra` |
| `the project has an app-tokens.css but this page does not load it` | add the `<link>` right after `tokens.css` |
| `raw colour ... project colours go in app-tokens.css` | move the colour into the token file and use the token |
