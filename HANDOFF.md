# EncoreMed design system: baseline for developers and their AI assistants

This directory is a **design baseline**, not a framework. Products built from it can be web apps or native apps (iOS, Android, desktop). The baseline fixes the things that make a product look and feel like EncoreMed (colours, type, spacing, sizes, states, how the main components behave), and leaves the rest to the product and the platform. The assistant's job is to **stay within the ballpark**.

Nothing here depends on the brand PDF or JPEG: the official colours and rules are copied in.

## 0. Start here

Give the whole directory to your developer; they point their AI assistant at it. A good first message:

> Use the EncoreMed design baseline in `<path to this directory>`. Read `AGENTS.md`, then `HANDOFF.md`. We are building `<what, and on which platform>`. When you finish, run the guard as `AGENTS.md` describes and report what it says.

`AGENTS.md` is the short rules file the assistant re-reads to cross-check its own work. This file (`HANDOFF.md`) is the full guide.

## 1. What is in this directory

| File | Purpose |
|---|---|
| `AGENTS.md` | rules and the cross-check checklist for the AI assistant |
| `HANDOFF.md` | this guide: brand rules, tokens, component specs, platform mapping |
| `design-tokens.json` | **the portable source of every value** (colours, sizes, spacing, radii, type, shadows, durations), with aliases and resolved values, for any platform |
| `DESIGN-TOKENS.md` | the same tokens as a readable list with resolved values |
| `guard.py` | the checker (section 8). Python 3, no packages. |
| `web/tokens.css`, `web/components.css` | the web reference implementation: CSS variables and component styles |
| `web/app.js` | web reference for component behaviour (dropdown, multi-select, pagination, sidebar, staff menu) |
| `web/export_tokens.py` | optional: if you change `web/tokens.css`, run it in that folder to regenerate the token files there |

Web products copy `web/tokens.css` and `web/components.css` into their project. Native products read `design-tokens.json` (or `DESIGN-TOKENS.md`) and translate the values (section 6).

## 2. How strict to be: must, should, may

| Level | What | Why |
|---|---|---|
| **Must** | the palette colours, the typeface and weights, the 4px spacing grid, the control size scale, the radius scale, the five control states (default, hover, pressed, disabled, focus), 4.5:1 text contrast | these make the product recognisably EncoreMed and keep it accessible |
| **Should** | the component anatomy and behaviour in section 5 (what a dropdown, pagination bar or sidebar contains and how it behaves), the screen patterns, wording style | users already know these patterns from other EncoreMed products |
| **May** | native or platform controls, platform navigation and gestures, dark mode, new components, new colours for a real need | a native app should feel native. Extend the baseline; do not fight the platform |

When you go beyond the baseline (a new colour, a new component, a different pattern), keep to the spirit of it: the same palette family, sizes from the scale, the same five states. Tell the user what you added and why.

## 3. Brand rules (the part that must not drift)

**Colours.** The `em-*` tokens (the `--em-*` variables at the top of `web/tokens.css`) are the official palette: the core and secondary colours from the style guideline PDF (converted from CMYK to sRGB) combined with the colour-blind-safe set.

| Token | Hex | Used for |
|---|---|---|
| `--em-navy-core` | `#023C6E` | primary brand navy: sidebar, primary buttons, links |
| `--em-green-core` | `#16AD85` | primary brand green: live status dots, "captured" marks, active edge |
| `--em-blue` | `#16537A` | secondary blue: active nav item, gradient lift |
| `--em-green-soft` | `#4FAA91` | secondary mint-green: login status dot and rings |
| `--em-grey-dark` | `#3A3A3C` | body text |
| `--em-navy` | `#0E4473` | headings |
| `--em-slate` | `#4C6173` | secondary text and labels |
| `--em-green` | `#4BA67B` | toggle on, battery bars |
| `--em-mint` | `#9CD9BC` | badge text on navy, light accents |
| `--em-grey-light` | `#F2F2F2` | page background |

Not in the guideline, chosen for this system: red (errors, delete), amber (warnings and the pressed state).

**Typeface.** Acumin Variable (Concept), with Arial as the system fallback (`--font-sans`). Regular and Bold only. Acumin is not bundled; it renders only where installed, so everywhere else you get Arial.

**Colour use rules**
- Body and secondary text must stay at **4.5:1** contrast or better on its background. `--ink-700` (11.4:1) and `--ink-600` (6.4:1) are safe on white. The soft grey `--ink-400` is only 3.5:1 on white (3.1:1 on the page background), so use it for placeholders, helper text and icons, not for important text.
- **Green and mint are for fills, dots and icons, not text.** `#16AD85` on white is only 2.9:1. Text on a green fill uses the dark navy `--brand-800`.
- Pressed state is amber; keyboard focus is the navy ring. Do not mix them.
- The sidebar is `--brand-600` (primary navy); the page background is `--bg`; cards are white with `--border`.

## 4. Tokens: the portable source of values

Tokens come in three tiers, each built from the one before:

| Tier | Examples | Meaning |
|---|---|---|
| Palette | `em-navy-core`, `em-green-core` | the official brand colours |
| Semantic | `brand-600`, `ink-700`, `accent-500`, `space-lg`, `radius-md`, `text-sm`, `shadow-md` | roles: text, brand, status, spacing, radius, type, elevation |
| Component | `btn-primary-bg-hover`, `field-h`, `dd-option-bg-hover`, `nav-w-expanded` | the values of one control |

- **Naming:** `{component}-{variant?}-{property}-{state?}`, for example `btn-primary-bg-hover`. (In CSS they are written `--btn-primary-bg-hover`.)
- **`design-tokens.json`** lists every token with its type (`color`, `dimension`, `shadow`, `fontFamily`, `fontWeight`, `number`, `duration`), its alias (`{brand-600}`) and its resolved value. Generate your platform's constants from it, or copy values by hand from `DESIGN-TOKENS.md`. Keep the token names in your code so design and code stay in sync.
- **Scales (the "must" values):**
  - control heights: 32, 36, 40, 44, 48 (`control-h-sm` to `control-h-2xl`). Never invent another control height.
  - spacing (4px grid): 2, 4, 8, 12, 16, 20, 24, 32, 48, 64 (`space-2xs` to `space-5xl`)
  - radius: 4, 8 (controls), 12 (cards), 16, pill, circle (`radius-sm` to `radius-circle`)
  - type sizes: 13, 14, 15, 16, 18, 20, 26, 36 (`text-xs` to `text-3xl`); weights Regular (400) and Bold (700) only
  - elevation: `shadow-sm` (`0 1px 2px` at 8% black), `shadow-md` (`0 8px 24px` navy at 14%), `shadow-lg` (`0 20px 48px` dark navy at 26%)
- **A few values are computed**, so in code they are written as colour + opacity: white overlays on the navy sidebar (white at 10, 15, 50, 70 and 80%), the keyboard focus ring (navy at 18%, 3px) and the pressed ring (amber `#FFB020` at 55%, 3px).

### The five control states (every interactive control)
1. **Default**
2. **Hover** (pointer devices only): a darker border or fill, from the component's `-hover` tokens.
3. **Pressed**: **amber**, from `pressed-bg` `#FFF4DC`, `pressed-border` and `pressed-fg` `#B45309`, and the pressed ring. Amber is the complement of the logo navy and is used for pressed only.
4. **Disabled**: 55% opacity (`disabled-opacity`) or the component's disabled colours; not interactive.
5. **Keyboard / switch focus**: a 3px navy ring at 18% (`focus-ring`) around the control, shown only for keyboard or assistive focus.

On touch platforms there is no hover; pressed and focus still apply.

## 5. Component specs (platform-neutral)

Sizes are in logical pixels (px on web, pt on iOS, dp on Android) and come from tokens. Look up exact colours in `DESIGN-TOKENS.md`. Every control follows the five states in section 4.

**Buttons** (radius 8, label 14 bold)
- *Primary*: height 48, side padding 20, navy fill, white label. Hover is a darker navy. Disabled is a grey fill.
- *Secondary*: height 40, white fill, 1px light-blue border, slate label.
- *Outline (compact)*: height 32, for rows and cards.
- *Icon button*: 36×36, outlined, icon only, with an accessible label.
- *Tinted arrow (list row action)*: 36×36, light tint, chevron.
- *Danger*: solid red, height 44; an icon-only 44×44 variant ("clear all filters"); an outlined variant for delete.
- *Text / link*: no container, navy bold label.

**Text field** (height 48; 44 when compact in a filter bar; radius 8; 1px border; side padding 16)
- Border darkens on hover; on focus the border turns brand blue and the focus ring shows. Disabled uses the page-grey fill.
- *Password field*: a 36×36 show/hide button inside the field, 8px from the right edge.
- *Search field*: a magnifier icon on the left; a 24px round clear (×) button on the right, shown only while there is text.

**Checkbox and switch**
- Checkbox 18×18, radius 4, 1px grey border; checked is a navy fill with a white check.
- Switch 42×24 with a round knob that travels 18px; on is green.

**Dropdown (single select)**
- A trigger shaped like a text field (height 44) or a compact one (height 32, for "rows per page"), with a chevron that rotates when open and an optional prefix label ("Zone:").
- The option panel opens 4px below the trigger (above it near the bottom of the screen), lists options (max height about 200, then scrolls), marks the selected option with a check, and can have a short footer note.
- Behaviour: opens on tap or click or the down arrow; focus moves to the selected option; choosing closes it and returns focus to the trigger; Escape and an outside tap close it. Prefer the platform's native picker on native apps when it fits.

**Multi-select with search**
- Same trigger and panel, plus a search field (height 36) at the top of the panel, a check box before each option, and "No results found" when the search matches nothing.
- It shows "All …" when nothing is selected and the picked names when something is; a clear (×) appears when something is selected. The panel stays open while the user picks several options.

**List or table with pagination**
- A white card (radius 12, 1px border). Header row: small uppercase bold grey titles with wide letter-spacing. Rows have a hover tint and an amber pressed state, and an optional row action arrow.
- Column titles must never touch: keep a gap of at least 12 to 16 between columns and give each column a minimum width.
- *Pagination bar* (shown above and below the list): "Showing 1–10 of 24", a "Rows per page" dropdown (5, 10, 20), and buttons **First, Previous, up to five page numbers, Next, Last**. Buttons are 32×32 with a 4px gap, the current page is navy with a white number, First/Previous are disabled on the first page and Next/Last on the last. On narrow screens the four labelled buttons become icon-only.

**Navigation (sidebar)**
- Two states: an icon **rail** (72 wide) and an expanded **panel** (248 wide), animated over 200ms. It changes **only** from its own toggle button, never on hover, so it works on touch screens.
- Items are 44 tall (44×44 squares when collapsed) with a 20px icon and a label; the active item is brand-blue with a 3px green edge; a count badge can sit on an item.
- Top: the logo mark (40×40, radius 12), which never shrinks, stretches or reflows. Above the profile row: the expand/collapse button, a full-width green button with dark navy text. Bottom: the profile row (a 34px avatar, name and role) that opens a staff menu, and a sign-out item. Rows keep the same height in both states so nothing jumps.

**Page header and sections**: a header bar (min height about 86) with the page title (26) and a one-line subtitle, and optional status pill and icon button on the right. Section headings are 20 with a 14 subtitle.

**Status pill, banner, card**
- *Status pill*: a pill with a 1px border and a 6px green dot.
- *Banner*: a 36×36 tinted icon square, a bold title and one short line.
- *Card*: white, 1px border, radius 12.

**Dialog (modal)**: a centred card (max width 390; 430 for the wide variant) with a 48×48 icon, title (20), a short explanation, an optional field, and two actions. The default variant centres the text and shows two equal-width buttons; the wide variant left-aligns text and right-aligns the buttons (cancel, then the primary action). Dim the background; trap focus; Escape cancels.

**Toast**: a small card at the bottom right with a green check and one line, dismissed after about 2 seconds. Use it for confirmations, not errors.

**States**: *loading* is a 28px spinner with the word "Loading…"; *error* says what failed in one line and offers a **Retry** button; *empty* is one centred sentence. Never leave a list blank without one of these.

**Avatar and initials**: a circle with the person's initials on a soft pastel tint. The tint colours are data, not brand colours.

## 6. Translating the baseline to a platform

| Baseline | Web | iOS (SwiftUI/UIKit) | Android (Compose/Views) | Desktop / cross-platform |
|---|---|---|---|---|
| Colours | CSS variables | an asset catalog or a `Color` extension generated from the tokens | `colors.xml` or a Compose `ColorScheme` | a theme file |
| Type | `--font-sans` stack | Acumin if licensed, else SF Pro; sizes from `text-*` | Acumin if licensed, else Roboto | system font fallback |
| Spacing, size, radius | `--space-*`, `--control-h-*`, `--radius-*` | constants in points | `dp` values | constants |
| Elevation | box shadows | shadow or elevation matching the three levels | `elevation` matching the three levels | same |
| Pressed and focus | amber pressed, focus ring | amber pressed highlight; focus ring on keyboard focus (iPad, Mac) | amber ripple / pressed state; focus indicator for keyboard | same |
| Motion | 200ms for sidebar and panels, about 130ms for hover | same durations | same durations | same |

Rules for native apps:
- **Prefer native controls** (pickers, sheets, navigation bars, the platform back gesture) and restyle them with the tokens. Keep the baseline's *look*: palette, type, spacing, radii, states. Do not rebuild a native control only to copy the web version.
- Keep touch targets at least 44×44.
- The sidebar becomes a platform navigation pattern (tab bar, navigation rail or drawer); keep the item order, labels and active-state style.
- Dark mode is not defined in the baseline. If the product needs it, derive it from the semantic tokens and tell the user; keep contrast at 4.5:1.
- Do not copy this demo's fictional data or names (Rossmax, residents, devices).

## 7. Behaviour rules

- **Layout:** the baseline is designed for tablet and larger (minimum width 768px on web). Phone layouts are not defined; derive them from the same components and tokens.
- **Text that must not reflow** (navigation labels, buttons) stays on one line.
- **Menus, dropdowns and dialogs** close on an outside tap and on Escape (or the platform back action) and return focus to what opened them.
- **Icons** are simple line icons: 24px grid, 1.8px stroke, round caps and joins, 20px by default, coloured by the text colour of their context.
- **Accessibility:** every control is reachable and operable without a pointer, has an accessible name, and shows a clear focus state. Status is never conveyed by colour alone.


## 8. Safeguards: `guard.py`

The baseline is not a cage, so `guard.py` does not stop you. It cross-checks your project, so that mistakes and changes are visible. It needs only Python 3 and takes about a second.

```bash
python3 <this directory>/guard.py                # check the current folder (your project)
python3 <this directory>/guard.py path/to/project
python3 <this directory>/guard.py --strict       # warnings also fail
```

It prints `PASS` or `FAIL` and exits with code 1 on any error.

**On any platform:** it scans your source files (Swift, Kotlin, Dart, XML, JS and others) for colour literals (`#RRGGBB`, `#RGB`, `0xRRGGBB`, `0xAARRGGBB`) that are not in the design palette, and warns, naming the closest token. Fix it by using the token's value, or tell the user why a new colour was needed.

**On web projects** (the folder has `.css` or `.html` files) it also checks:

| Check | What it prevents |
|---|---|
| `tokens.css` and `components.css` are in the project | a project missing the design system (error) |
| Every `var(--token)` is defined | typos and invented tokens that render as nothing (error) |
| No raw colours in `components.css`, `app.css`, `app-tokens.css` or inline `style=""` | off-brand colours; every colour comes from a token (error) |
| Component and app tokens alias other tokens | raw colours hidden inside component tokens (error) |
| Stylesheets load in this order: `tokens.css`, `app-tokens.css`, `components.css`, `app.css` | components styled before their tokens exist (error) |
| Text and background pairs reach 4.5:1 contrast | unreadable text from a changed colour token (error) |
| A baseline token or class was removed from your copy | breakage elsewhere (warning) |
| Raw pixel `height`, `!important`, external URLs on lines you wrote or changed | drift from the size scale (warning) |
| Your `tokens.css` or `components.css` differs from the baseline | information only: what you added or changed (note) |

**If it fails:** edit the line it names. Do not edit `guard.py` to make it pass. Extending the baseline is allowed: add rather than rename or remove, and mention it in your summary.

## 9. Web reference: markup catalogue

This is the reference implementation for **web** products (the CSS classes in `web/components.css`). Native products use sections 4 to 7 and take the values from `design-tokens.json`. Replace `…` with icons or content. Every interactive element is a real `<button>`, `<input>` or `<a>`.

### Page shell and sidebar
```html
<div class="app-shell nav-expanded">            <!-- remove "nav-expanded" for the collapsed rail -->
  <aside class="sidebar">
    <div class="sidebar__logo">
      <div class="logo logo--light">
        <div class="logo__mark"><svg>…</svg></div>
        <div class="logo__text"><div class="logo__name">Product</div><div class="logo__sub">Subtitle</div></div>
      </div>
    </div>
    <nav class="sidebar__nav" aria-label="Main">
      <button class="nav-item active" title="Residents" aria-label="Residents" aria-current="page">
        <svg>…</svg><span class="nav-label">Residents</span>
      </button>
      <button class="nav-item" title="Devices" aria-label="Devices"><svg>…</svg><span class="nav-label">Devices</span><span class="nav-badge">4</span></button>
    </nav>
    <div class="sidebar__toggle-row">
      <button class="nav-item sidebar__toggle" aria-expanded="true" aria-label="Collapse navigation" title="Collapse navigation">
        <svg>…</svg><span class="nav-label">Collapse menu</span>
      </button>
    </div>
    <div class="sidebar__foot">
      <!-- staff menu popup, shown only while open: <div class="profile-menu"> <div class="profile-menu__head">Staff menu</div> <button class="profile-menu-item">…</button> </div> -->
      <button class="profile" aria-haspopup="menu" aria-expanded="false" aria-label="Staff menu: Name, Role">
        <span class="profile__avatar">AM</span>
        <span class="profile__who"><span class="profile__name truncate">Name</span><span class="profile__role">Role</span></span>
      </button>
      <button class="nav-item" title="Sign out" aria-label="Sign out"><svg>…</svg><span class="nav-label">Sign out</span></button>
    </div>
  </aside>
  <main class="main">
    <header class="page-header"><div><h1>Title</h1><p>Subtitle</p></div>
      <div class="header-actions"><span class="status-pill"><span></span> Connected</span><button class="icon-button" aria-label="…"><svg>…</svg></button></div>
    </header>
    <div class="content-scroll"> … page content … </div>
  </main>
</div>
```
Add `class="open"` to `.profile` while its menu is open.

### Buttons
```html
<button class="primary-btn">Save</button>                         <!-- solid navy; add disabled -->
<button class="secondary-btn"><svg>…</svg>Cancel</button>        <!-- white, tinted border -->
<button class="icon-button" aria-label="…"><svg>…</svg></button> <!-- square, outlined -->
<button class="link-btn">Need help?</button>                      <!-- text link -->
<button class="back-btn"><svg>…</svg>Back</button>                <!-- text with arrow -->
```
Modifiers: `.min-160` / `.min-150` set a minimum width.

### Text field, label, password eye
```html
<label><span class="label">Staff ID</span><input class="field" type="email" /></label>
<div class="pw-wrap">
  <input class="field" type="password" />
  <button type="button" class="pw-toggle" aria-label="Show password"><svg>…</svg></button>
</div>
```
`.field--mono` gives a monospace field. Compact fields in a filter bar use `.filter-field`.

### Checkbox row and switch
```html
<button type="button" class="remember on" role="checkbox" aria-checked="true"><span class="remember__box"><svg>…</svg></span>Remember this device</button>
<button class="toggle on" role="switch" aria-checked="true" aria-label="…"><span></span></button>
```

### Search box with clear (×)
```html
<div class="search-wrap"><svg>…</svg>
  <input class="filter-field" type="text" placeholder="Search…" />
  <button type="button" class="search__clear" aria-label="Clear search"><svg>…</svg></button>   <!-- only while there is text -->
</div>
```

### Dropdown (single select)
Variants: `dd--field` (looks like a text field, with an optional `.dd__prefix`), `dd--sm` (compact, for rows per page), `dd--up` (opens upward). Add `open` while open. Opening is state you manage (re-render or toggle the class).
```html
<div class="dd dd--field open" data-dd="zone">
  <button type="button" class="dd__trigger" aria-haspopup="listbox" aria-expanded="true" aria-label="Zone: North Wing">
    <span class="dd__label"><span class="dd__prefix">Zone:</span> North Wing</span>
  </button>
  <svg class="dd__chevron">…</svg>
  <div class="dd__panel">
    <div class="dd__list" role="listbox" aria-label="Zone">
      <button type="button" class="dd__option selected" role="option" aria-selected="true"><span>North Wing</span><svg>…check…</svg></button>
      <button type="button" class="dd__option" role="option" aria-selected="false"><span>East Wing</span></button>
    </div>
    <div class="dd__footer">Optional footer note.</div>
  </div>
</div>
```
Behaviour to implement: opens on click or ArrowDown, moves focus to the selected option, closes on pick (focus back to the trigger), on Escape and on outside click.

### Multi-select with search
```html
<div class="ms open has-value" data-dd="ward">            <!-- has-value when something is picked -->
  <button type="button" class="ms__trigger filter-field" aria-haspopup="listbox" aria-expanded="true"><span class="ms__label">Memory Care</span></button>
  <button type="button" class="ms__clear" aria-label="Clear"><svg>…</svg></button>   <!-- only when has-value -->
  <svg class="ms__chevron">…</svg>
  <div class="ms__panel">
    <div class="ms__search"><input class="ms__search-input" type="text" role="searchbox" aria-label="Search" /><svg>…</svg></div>
    <div class="ms__list" role="listbox" aria-multiselectable="true">
      <button type="button" class="ms__option selected" role="option" aria-selected="true"><span class="ms__check"><svg>…check…</svg></span><span>Memory Care</span></button>
    </div>
    <!-- no matches: <div class="ms__empty">No results found</div> -->
  </div>
</div>
```
Use `ms__label placeholder` for the "All …" placeholder text. The panel stays open while picking several options.

### Table with pagination
```html
<div class="table-card">
  <div class="table-foot table-foot--top">            <!-- optional pager above; use a plain .table-foot below the table -->
    <div class="table-foot__left">
      <span>Showing <strong>1–10</strong> of <strong>24</strong></span>
      <div class="rows-select"><span>Rows per page</span> …a .dd.dd--sm dropdown… </div>
    </div>
    <nav class="pager" aria-label="Pagination">
      <button class="pager__btn pager__btn--nav" aria-label="First page" disabled><svg>…</svg><span>First</span></button>
      <button class="pager__btn pager__btn--nav" aria-label="Previous page" disabled><svg>…</svg><span>Previous</span></button>
      <button class="pager__btn current" aria-label="Page 1" aria-current="page">1</button>
      <button class="pager__btn" aria-label="Page 2">2</button>
      <button class="pager__btn pager__btn--nav" aria-label="Next page"><span>Next</span><svg>…</svg></button>
      <button class="pager__btn pager__btn--nav" aria-label="Last page"><span>Last</span><svg>…</svg></button>
    </nav>
  </div>
  <div class="table-head my-columns"> column titles </div>     <!-- "my-columns" and "my-row" are classes YOU define in app.css (a CSS grid) -->
  <button class="my-row my-columns"> row cells </button>
</div>
```
Show at most **5 page numbers** in a sliding window (`First` and `Last` jump to the ends). Table column grids are screen-specific: define your own grid class in `app.css`.

### Status, banner, cards, modal, toast, loading
```html
<span class="status-pill"><span></span> Gateway connected</span>
<div class="banner"><div class="banner__icon"><svg>…</svg></div><div><strong>Title</strong><small>One short line.</small></div></div>
<div class="card"> … </div>

<div class="modal-backdrop"><div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="m1">
  <div class="modal-icon"><svg>…</svg></div><h2 id="m1">Title</h2><p>Short explanation.</p>
  <label class="modal-label"><span class="label">Field label</span><input class="field" /></label>   <!-- optional input -->
  <div class="modal-actions"><button class="secondary-btn">Cancel</button><button class="primary-btn">Confirm</button></div>   <!-- two equal columns -->
</div></div>

<!-- wide variant: left-aligned text, warning icon, right-aligned actions -->
<div class="modal-backdrop"><div class="modal-card modal-card--wide" role="dialog" aria-modal="true" aria-labelledby="m2">
  <div class="modal-icon modal-icon--warn"><svg>…</svg></div><h2 id="m2">Apply changes?</h2><p>Longer explanation.</p>
  <div class="modal-actions modal-actions--end"><button class="secondary-btn">Keep current</button><button class="primary-btn">Apply</button></div>
</div></div>

<!-- section heading inside page content; add section-head--tight for a smaller subtitle -->
<div class="section-head"><div><h2>Section title</h2><p>Section subtitle.</p></div><!-- optional right-hand content --></div>

<div class="toast" role="status"><span class="toast__check"><svg>…</svg></span>Scan complete</div>   <!-- remove after about 2 seconds -->

<div class="state" role="status" aria-live="polite"><div class="spinner" aria-hidden="true"></div>Loading…</div>
<div class="state state--error" role="alert"><strong>Couldn't load data.</strong> … <button class="secondary-btn">Retry</button></div>
<div class="empty-note">No results match these filters.</div>
```
Utilities: `.truncate` (single-line ellipsis), `.sr-only` (visually hidden text for screen readers).

## 10. Known limits
- **Acumin Variable is not bundled.** Without a licence, use Arial on web and the system font on native (SF Pro, Roboto).
- **The web markup catalogue (section 9) is CSS only.** Opening, closing and focus behaviour for the dropdowns, multi-select, sidebar toggle and staff menu live in `web/app.js` (event delegation on `data-action`, a state object and a `render()` function). Native products implement the behaviour in section 5 with platform controls.
- **The soft grey `ink-400` is below 4.5:1 on white** (3.5:1). Use it for placeholders, helper text and icons, never for important text.
- **Tablet and larger is the design target.** There is no defined phone layout; derive one from the same components and tokens.
- **No dark mode** is defined.
- **The guard checks colours and (on web) CSS.** It cannot judge layout, markup or behaviour, so use the self-check list in `AGENTS.md` too.
