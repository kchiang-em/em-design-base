# Theming playbook: re-colouring a product for a client

**For AI assistants.** Follow this when the user gives you colour codes **or a logo**, or asks to change, re-brand or re-theme the colours of a product built on the EncoreMed design baseline. Typical requests:

> "Change the colours to the client's: primary #AABBCC, secondary #DDEEFF."
> "Here are the brand colours for ACME: …"
> "Make the app use our blue instead of the navy."
> "Here is the client's logo: match the app to it." (see section 3b)

Do **not** search the project and replace colours by hand. Use the steps below: they keep the result consistent, accessible, and valid for the guard.

## 1. The rules, in one minute

1. All client colours go in **one theme file**: `theme.css` (web) or `theme.json` (any platform). Raw colour codes are allowed there and **nowhere else**. Everywhere else, use tokens.
2. **Status colours never change:** red (errors), orange (warnings) and green (positive, live). They mean the same in every product. If the user asks to change them, say no and explain.
3. Only **colours** are themed. Sizes, spacing, radii, type scale and the five control states do not change.
4. Text must keep **4.5:1 contrast**, including white text on the new primary colour.
5. Use `make_theme.py` to derive the colours. Do not invent shades by hand.
6. Finish by running `guard.py` and reporting to the user (section 6).

## 2. Step by step

**Step 1. Understand what was pasted** (section 3). Convert every colour to hex first (`rgb(122,31,61)` becomes `#7A1F3D`). If the user gives a colour **name** ("burgundy") or a brand name, ask for the hex code; do not guess. If the user gives a **logo**, go to section 3b first and come back to step 2 with the confirmed colours.

**Step 2. Run the tool** from the project folder (needs Python 3, no packages):

```bash
python3 <handoff directory>/make_theme.py --primary "<hex>" [options] --css theme.css      # web
python3 <handoff directory>/make_theme.py --primary "<hex>" [options] --json theme.json   # native or any platform
```

| Option | Use it for | Becomes |
|---|---|---|
| `--primary` (required) | the client's main brand colour: buttons, sidebar, links | `em-navy-core` and all the brand shades |
| `--secondary` | a second brand colour: active navigation item, gradient lift | `em-blue` (default: a slightly lighter primary) |
| `--heading` | the colour of headings | `em-navy` (default: the primary) |
| `--text` | body text | `em-grey-dark` (default: unchanged) |
| `--muted-text` | secondary text and labels | `em-slate` (default: unchanged) |
| `--background` | page background | `em-grey-light` (default: unchanged) |
| `--extra name=hex` | another client colour with no EncoreMed role (repeat as needed) | a new token `--client-<name>` |
| `--adjust` | primary is too light for white text: darken it until it passes (otherwise the tool stops and suggests a colour) | |

The tool derives the rest of the brand scale from the primary colour (hover shade, dark surfaces, light tints), re-tints the keyboard focus ring and the shadows, checks contrast, and prints a table of what it set. **Keep that table: it is the core of your report.**

**Step 3. Read the tool's messages.**
- `ERROR ... contrast`: do not ship it. Ask the user for a darker or lighter colour, or confirm the tool's suggested colour (then run again with `--adjust`).
- `NOTE: primary hue is close to a status colour`: it is allowed, but tell the user. Because red, orange and green cannot change, errors and warnings can look like the brand. Keep an icon and a text label on every status message; never rely on colour alone.
- `NOTE: ... sidebar toggle label ... darkened`: normal. The label sits on the fixed status green, so the tool darkened only that label.

**Step 4. Apply the theme.**
- **Web:** make sure every page loads `theme.css` right after `tokens.css`: `tokens.css`, `theme.css`, `app-tokens.css`, `components.css`, `app.css`. The component styles follow automatically. No other CSS change is needed.
- **Native or other:** generate your platform's colour constants from `design-tokens.json` with the theme on top. For every colour token in `design-tokens.json`: if `theme.json` has that name, use its value; otherwise, if the token is an alias such as `{brand-600}`, resolve it using the *themed* values; otherwise use its own value. Keep the token names in your code. Then follow `HANDOFF.md` section 6 for the platform.

**Step 5. Remove hard-coded EncoreMed colours from the project's own code.** The old navy and blue may be written directly in the project's files. Search for them and replace each with the matching token (web: `var(--brand-600)`, `var(--brand-500)`; native: your generated constant):

```bash
grep -rniE "023c6e|16537a|0e4473|01305a|012646|011c34|01121f|2 60 110" <project folder> --include=* --exclude-dir=node_modules --exclude-dir=.git
```

Colours that are not in the palette at all will be reported by the guard in step 6. Do not paste a client colour into the project's own code: add it to the theme (as `--extra`) and refer to the token.

**Step 6. Run the guard** and fix everything it reports:

```bash
python3 <handoff directory>/guard.py <project folder>
```

**Step 7. Check the screens** (look at them if you can run the product; otherwise say you could not). Verify on each: the primary button (default, hover, pressed in amber, disabled), the navigation or sidebar and its active item, a text field in focus (the focus ring), a table or list with hover, a dropdown open, a modal, the login or splash screen, and status pills or messages (they must still be red, orange or green). Check that nothing is unreadable.

**Step 8. Report** (section 6).

## 3. Interpreting what the user pastes

| The user gives you | What you do |
|---|---|
| one colour | it is the **primary** |
| two colours, labelled "primary" and "secondary" | use the labels |
| two unlabelled colours | the darker or more saturated one is the primary, the other is the secondary. **Say which you assumed.** |
| three or more colours | very light neutral becomes `--background`; dark neutral becomes `--text`; the main brand colour is the primary; a second brand colour is the secondary; **every other colour becomes an `--extra`**. Do not invent roles for them. |
| "accent" or "highlight" colour | `--extra`, used for decoration or brand emphasis only. Never for a status. |
| a colour for "success", "error" or "warning" | do not apply it. Explain that status colours are universal. |
| a colour for a specific part ("sidebar blue", "link colour") | the sidebar and links are the primary; a different sidebar colour is a design change, so ask the user. |
| a logo (SVG or PNG file) instead of colour codes | go to section 3b: extract the colours with `logo_colours.py`, confirm them with the user, then continue |
| a gradient, illustration or photo | out of scope for tokens: imagery is an asset the client supplies. Tell the user. |
| a typeface | not part of the colour theme: ask the user (`HANDOFF.md` section 3 for the baseline typeface). |
| a request for dark mode | not defined by the baseline; tell the user it is a separate piece of work. |

When something is genuinely ambiguous (which of two colours is the primary), pick the most likely one, state it, and make it easy to swap by running the tool again.

## 3b. When the user gives a logo instead of colour codes

A logo is a reliable source of the brand colours, **if you read it with the tool and not by eye**. Colours judged from how an image looks are unreliable (anti-aliasing, JPEG blur, screen colour). Never write a hex code you only estimated.

1. **Get the file.** You need the logo as a file you can run the tool on, ideally **SVG** (exact colours) or **PNG**. If the user pasted or attached the image in the chat, first check whether your tool saved it to disk (look for a file path in the attachment information, a temporary or attachments folder, or ask your tool): if there is a path, use it. If the image exists only in the conversation and there is no file, you can see it but you cannot measure it, so ask the user to save it and give you the path, or to give you the colour codes. You may look at the image to sanity-check the tool's result, but never use your own visual estimate as the colour value. JPEG, WebP and GIF work only if the Pillow package is installed; otherwise ask for a PNG or SVG. Screenshots of a logo are a weaker source than the logo file itself (they are often recompressed or colour-shifted).
2. **Run the extractor** from the project folder:
   ```bash
   python3 <handoff directory>/logo_colours.py path/to/logo.svg
   ```
   It lists the brand colours (most prominent first, with how much of the logo each covers and whether white text is readable on it), the neutrals, and a suggested `make_theme.py` command.
3. **Confirm with the user before applying.** The most prominent colour is not always the brand colour, and a logo can contain colours that are not meant for an interface. Show the candidates and your proposed roles in one short message, for example: "Your logo uses #7A1F3D (about 70%) and #F2A900 (about 20%). I plan to use #7A1F3D as the primary and keep #F2A900 as an extra accent colour, because it is too light for white text. Is that right?" If the user said to just use the logo, go ahead, state the assumption, and make it easy to change.
4. **Run `make_theme.py` with the confirmed colours** and continue with step 3 onwards in section 2.

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

**The logo itself is an asset, not a token.** Extracting its colours does not place it in the product. If the user also wants the client's logo in the interface, that is a separate task: put the file where the product keeps its logo (on web, the sidebar and login panel; on native, the asset catalogue), keep its proportions and clear space, never recolour or stretch it, and say if its shape (a wide wordmark) does not fit the fixed logo tile and needs a design decision.

## 4. What changes and what does not

| Changes with a theme | Never changes |
|---|---|
| primary and its shades (buttons, sidebar, links, focus, hover, dark surfaces, tints) | status colours: red `danger-*`, orange `warning-*`, green `accent-*`, `em-green`, `em-green-core`, `em-green-soft`, `em-mint` |
| secondary (active navigation item, gradients) | sizes, spacing, radii, type scale |
| headings, text, secondary text, page background (only if the user gave them) | the five control states and their structure |
| the focus ring and shadow tints | the amber **pressed** colour, unless the user asks (see below) |
| extra client colours (`--client-<name>`) | |

**Pressed state:** it stays amber by default. If the client's brand is itself amber, orange or yellow, the pressed state becomes hard to tell from normal; tell the user, and only change the `amber-*` colours if they ask, keeping the pressed text readable (4.5:1).

**Extra client colours** (`--client-<name>`): use them as `var(--client-<name>)` in the product's own CSS, or as a generated constant natively. Keep them out of status messages, and keep text on them at 4.5:1.

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
| `focus-ring`, `shadow-md`, `shadow-brand` | keep the shape, replace the rgb colour with the primary at the same opacity (18%, 14%, 22%) |
| `shadow-lg` | the same, using `brand-900` at 26% |

Check: white on the primary, on `brand-700` and on `em-blue` all at least 4.5:1; headings on white at least 4.5:1; and `nav-toggle-fg` (default `brand-800`) on the status green `#16AD85` at least 4.5:1, otherwise set `nav-toggle-fg` and `nav-toggle-fg-hover` to a darker colour. Then run the guard.

## 6. What to tell the user

Report in this order, briefly:
1. **What you set:** the mapping table the tool printed (role, token, value), and which colour you treated as primary and secondary if the user did not say.
2. **What you did not change, and why:** status colours (universal), sizes and states.
3. **If you worked from a logo:** the colours you extracted, which you treated as primary, secondary and extras, and whether the user confirmed them.
4. **Warnings you raised:** a primary close to a status colour, a colour you darkened or adjusted (with the before and after), anything you could not do (logo, fonts, dark mode, imagery).
5. **The guard result**, and what you replaced in the project's own code.
6. **What you could not verify** (for example, you did not run the product to look at the screens).

## 7. Mistakes to avoid
- Typing a client hex code anywhere except the theme file.
- Estimating colours by eye from a logo or screenshot instead of running `logo_colours.py`.
- Editing `tokens.css` or `components.css` to change colours. Use the theme.
- Overriding a status colour because it "looks off" next to the brand colour.
- Skipping the shades: changing only the primary leaves EncoreMed navy in hover and tinted states (the guard warns about this).
- Shipping a primary colour that fails contrast with white text.
- Using green or mint for text, or an `--extra` colour for a status.
- Reporting "done" without running the guard.

## 8. If the guard or tool complains

| Message | Meaning and fix |
|---|---|
| `theme: --x is a status colour ... cannot change it` | remove it from the theme |
| `theme: --x is not a design token (did you mean ...)` | a typo in a token name; fix it, or if it is a new client colour name it `--client-<name>` |
| `theme: --x must be a colour` | the value is not a hex, `rgb()` or `hsl()` colour |
| `theme: the brand colours were changed but these related shades were not` | run `make_theme.py` instead of editing by hand, or set the listed shades |
| `contrast ... needs 4.5:1` | pick a darker or lighter colour; the message names the pair |
| `colour #xxxxxx is not in the design palette` | a colour in the project's code that is not a token: use the token it names, or add the colour to the theme as an `--extra` |
| `the project has a theme.css but this page does not load it` | add the `<link>` right after `tokens.css` |
| `raw colour ... a client's brand colours go in theme.css` | move the colour into the theme and use the token |
