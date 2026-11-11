# Implementation guide: building EncoreMed interfaces on any platform

This guide explains **how** to implement the UI policies in `../policy/` on web and native platforms: where the values live, how to translate them per platform, and the web reference markup. It does not restate the rules: each section cites the clauses it implements (for example FND-9). When a clause and this guide seem to disagree, the clause wins; tell the user about the mismatch (SCP-7).

## 1. What is where

| Folder | What it holds |
|---|---|
| `../policy/` | the rules (UI-1 to UI-6), with clause IDs. Read them first. |
| `../tokens/` | `design-tokens.json`, the portable source of every value; `DESIGN-TOKENS.md`, the same as a readable list |
| `../tools/` | `guard.py` (the conformance checker) and `make_theme.py` (client brand colours). See `../tools/README.md`. |
| `../web/` | the web reference implementation: `tokens.css`, `components.css` and `app.js` (component behaviour) |
| `THEMING.md` | the step-by-step procedure for re-colouring a product for a client (implements UI-5) |

## 2. Setting up a project

**Web.** Copy `web/tokens.css` and `web/components.css` into the project, and download the default font into a `fonts/` folder next to `components.css` (section 4). Every page loads the stylesheets in this order:

1. `tokens.css` (the shared design tokens)
2. `app-tokens.css` (the product's own tokens, optional: its new tokens and its overrides, including a client's brand colours, THM-1)
3. `components.css` (the shared components)
4. `app.css` (the product's own rules)

You may extend or modify the two shared files; add new tokens and classes rather than renaming or deleting existing ones (SCP-4). Use the markup in section 7.

**Native or other.** Generate the platform's constants (colours, spacing, radii, type sizes, durations) from `tokens/design-tokens.json`, with the product's own `app-tokens.json` (format `{"colors": {"name": "#hex"}}`) on top, keeping the token names (SCP-3). Then build screens from the component clauses in `../policy/UI-4-components.md`, using section 5 for the platform mapping.

## 3. Tokens

Tokens come in three tiers, each built from the one before:

| Tier | Examples | Meaning |
|---|---|---|
| Palette | `em-navy-core`, `em-green-core` | the official colours (FND-1) |
| Semantic | `brand-600`, `ink-700`, `accent-500`, `space-lg`, `radius-md`, `text-sm`, `shadow-md` | roles: text, brand, status, spacing, radius, type, elevation |
| Component | `btn-primary-bg-hover`, `field-h`, `dd-option-bg-hover`, `nav-w-expanded` | the values of one control (UI-4) |

- **Naming:** `{component}-{variant?}-{property}-{state?}`, for example `btn-primary-bg-hover`. In CSS they are written `--btn-primary-bg-hover`.
- **`design-tokens.json`** lists every token with its type (`color`, `dimension`, `shadow`, `fontFamily`, `fontWeight`, `number`, `duration`, `other`), its alias (`{brand-600}`) and its resolved value. Generate constants from it, or copy values from `DESIGN-TOKENS.md`.
- **Raw colours** appear only where tokens are defined (SCP-3): the palette and semantic tiers of `tokens.css`, the project's own `app-tokens.css` (project colours such as its chart colours), and a client theme (THM-1). Component tokens and stylesheet rules use tokens.
- **Project colours** go in `app-tokens.css`, not in the shared `tokens.css`, so the shared file stays identical to the baseline. Override a baseline token there (for example `--chart-2`) or add a new one with a project prefix.
- **Computed values:** a few values are written as a colour plus an opacity: white overlays on the navy sidebar (white at 10, 15, 50, 70 and 80%) and the pressed ring (amber `#FFB020` at 55%, 3px, ACC-3).
- **Focus ring (ACC-5):** `focus-ring` is two box shadows, `0 0 0 2px var(--white), 0 0 0 4px var(--brand-600)`. On native platforms draw the same two strokes outside the control. Because it refers to `brand-600`, a client theme recolours it without a separate entry. If a component sets its own `box-shadow` (as the active navigation item does), give it a `:focus-visible` rule that adds the ring, or the ring disappears.

**Where each rule's values live:**

| Clause | Tokens |
|---|---|
| FND-1 palette | `em-*` |
| FND-1 brand greens | `em-green-core`, `em-green-soft`, `em-green`, `em-mint` and `accent-*` (brand uses only: navigation edge and toggle, logo tile, switch on, decorative marks) |
| FND-2, FND-3 status colours | `danger-*` (red; text `danger-700`), `warning-*` (orange; text `warning-700`), `success-*` (status green; dots and icons `success-600`, text on tint `success-700`), `info-*` (information blue; `info-600` on `info-50`) |
| ACC-3 pressed | `amber-*` |
| FND-5 typeface, FND-7 type scale | `font-sans`, `text-*`; weights `weight-medium` (400, Regular), `weight-semibold` and `weight-bold` (both 700, Bold). The names are historical: only 400 and 700 are used. |
| FND-8 spacing | `space-2xs` to `space-5xl` |
| FND-9 control sizes | `control-h-sm` to `control-h-2xl` |
| FND-10 radius | `radius-sm` to `radius-circle` |
| FND-11 elevation | `shadow-sm`, `shadow-md`, `shadow-lg` |
| FND-13 motion | `nav-duration` (200ms), `control-transition` (150ms), `dd-chevron-duration` (120ms) |
| ACC-3 pressed | `pressed-bg`, `pressed-border`, `pressed-fg`, `pressed-on-dark`, `pressed-ring` |
| ACC-4 disabled | `disabled-opacity` and each component's `-disabled` tokens |
| ACC-5 focus | `focus-ring` |
| ACC-6 text greys | `ink-700` to `ink-400`, all at least 4.5:1 on white and on the page background; `ink-300` is for borders and disabled marks only, never text |
| ACC-6 control borders | `border-control` (3:1 on white and on the page background), used by `field-border` and `dd-trigger-border`; `border` stays for cards and dividers, which do not identify a control |
| CMP-2 invalid field | `field-border-error`, `field-error-fg`, `field-error-gap` |
| CMP-17 toast | `toast-duration` (6000ms) |
| CMP-1, CMP-21 danger button | `btn-danger-*` |
| CMP-19 avatar tints | `avatar-tint-1` to `avatar-tint-6` (data colours; store the tint number with the person, not a hex code) |
| FND-17 charts | `chart-1` to `chart-7` in order, `chart-other`; `chart-surface` names what is behind the charts (set it to `var(--bg)` for transparent charts on the page) |
| UI-4 components | `btn-*` (CMP-1), `field-*` (CMP-2), `pw-*` (CMP-3), `clear-btn-*`, `search-*` (CMP-4), `checkbox-*`, `remember-*` (CMP-5), `toggle-*` (CMP-6), `dd-*` (CMP-7), `ms-*` (CMP-8), `card-*` (CMP-9, interactive surfaces), `pager-*` (CMP-10), `nav-*` (CMP-11), `logo-mark-*` (CMP-20) |

## 4. Typeface (FND-5, FND-6)

- **Default: Public Sans** (SIL Open Font License, plus a public-domain dedication for its US-government changes). The font files are not in this package: download them from the official source, https://github.com/uswds/public-sans, and keep its `LICENSE.md` with them.
  - **Web:** download `fonts/webfonts/PublicSans-Regular.woff2` and `fonts/webfonts/PublicSans-Bold.woff2` into a `fonts/` folder next to `components.css`, which declares them with `@font-face`. `--font-sans` lists Public Sans first with Arial as the fallback. The guard warns if the files are missing.
    ```bash
    mkdir -p fonts && for w in Regular Bold; do curl -sL -o fonts/PublicSans-$w.woff2 https://raw.githubusercontent.com/uswds/public-sans/develop/fonts/webfonts/PublicSans-$w.woff2; done
    curl -sL -o fonts/LICENSE.md https://raw.githubusercontent.com/uswds/public-sans/develop/LICENSE.md
    ```
  - **Native:** bundle the Regular and Bold files from the same repository (`fonts/otf/` or `fonts/ttf/`) in the app, with the licence. Fall back to the system font (SF Pro, Roboto, Segoe UI).
- **Another face:** set `--font-sans` in the product's `app-tokens.css` (web), or the font family in its platform constants (native), with the system font as the fallback. Check the face against FND-5: Regular and Bold, distinct I / l / 1 and O / 0, tabular figures, a licence that covers the use. Acumin is allowed where the company holds a suitable licence (FND-6).
- **Tabular figures:** on web, `font-variant-numeric: tabular-nums` (already set on tables, pagination and readings in the reference); on native, the platform's monospaced-digits option.
- Only Regular (400) and Bold (700) are used, and every size comes from the `text-*` tokens, so layouts hold with the fallback.

## 4b. Icons (FND-12)

Use Lucide from an official release. Never draw, type or approximate an icon from memory: install or download it, pinned to one version, and pick icons by their name on https://lucide.dev/icons.
- **Web with a build step:** add Lucide's package for the framework (`lucide-react`, `lucide-vue-next`, `lucide-svelte`, `lucide-angular`, or `lucide` for plain JavaScript) with an exact version, and set its stroke width to 1.8 and size to 20 (24 grid), with the colour from `currentColor`.
- **Web without a build step:** download the SVG files you need from the same published release (the `lucide-static` package, `icons/<name>.svg`) into the project's `icons/` folder, keep Lucide's licence with them, and set `stroke-width="1.8"` on each.
- **Native:** use Lucide's package for the platform where one exists (for example `lucide-react-native`), or import the SVG files from the same release into the platform's asset catalogue as vector assets. Standard system actions may use the platform's own symbols (FND-12).
- Record the Lucide version the project uses (in its dependency file, or a note beside the `icons/` folder), so a later update is deliberate.
- If Lucide has no suitable icon under any name, follow FND-12: draw one in the same style, keep it in the project's `icons/` folder, and tell the user.

## 5. Translating to a platform

| Baseline | Web | iOS (SwiftUI/UIKit) | Android (Compose/Views) | Desktop / cross-platform |
|---|---|---|---|---|
| Colours | CSS variables | an asset catalog or a `Color` extension generated from the tokens | `colors.xml` or a Compose `ColorScheme` | the framework's colour constants |
| Type | `--font-sans` stack (Public Sans) | Public Sans bundled in the app, else SF Pro; sizes from `text-*` | Public Sans bundled in the app, else Roboto | Public Sans, else the system font |
| Spacing, size, radius | `--space-*`, `--control-h-*`, `--radius-*` | constants in points | `dp` values | constants |
| Elevation (FND-11) | box shadows | shadow matching the three levels | `elevation` matching the three levels | same |
| Pressed and focus (ACC-3, ACC-5) | amber pressed, focus ring | amber pressed highlight; focus ring on keyboard focus (iPad, Mac) | amber ripple or pressed state; focus indicator for keyboard | same |
| Motion (FND-13) | 200ms for sidebar and panels, 150ms for state changes | same durations | same durations | same |
| Navigation (CMP-11) | sidebar rail and panel | tab bar or sidebar | navigation rail or drawer | sidebar |

Native apps prefer platform controls restyled with the tokens (SCP-6) and keep touch targets at 44×44 or more (ACC-9).

## 6. Component implementation (UI-4)

The anatomy, sizes and behaviour of each component are set by its clause in `../policy/UI-4-components.md`. The web reference implements them as follows; native products implement the same clause with platform controls.

| Clause | Web classes (`web/components.css`) | Behaviour (`web/app.js`) |
|---|---|---|
| CMP-1 Buttons | `.primary-btn`, `.secondary-btn`, `.danger-btn`, `.icon-button`, `.link-btn`, `.back-btn` | none |
| CMP-2, CMP-3 Text and password field | `.field`, `.filter-field`, `.pw-wrap`, `.pw-toggle` | show/hide password |
| CMP-4 Search field | `.search-wrap`, `.search__clear` | clear button only while there is text |
| CMP-5, CMP-6 Checkbox and switch | `.remember`, `.toggle` | toggles `aria-checked` |
| CMP-7 Dropdown | `.dd`, `.dd--field`, `.dd--sm`, `.dd--up` | open, close, focus, arrow keys, Escape |
| CMP-8 Multi-select | `.ms` | search, multiple picks, clear |
| CMP-9, CMP-10 Table and pagination | `.table-card`, `.table-head`, `.table-foot`, `.pager` | sliding window of five pages |
| CMP-11 Navigation | `.app-shell` (`.nav-expanded`; `.nav-auto` for the mouse overlay), `.sidebar`, `.nav-item`, `.profile`, `.profile-menu` | device detection with `(hover: hover) and (pointer: fine)` and `(any-pointer: coarse)`; hover and focus open the overlay after `--nav-hover-open-delay`, close after `--nav-hover-close-delay`; Escape closes; the toggle (touch) is remembered; staff menu |
| CMP-12 Page header | `.page-header`, `.section-head` | none |
| CMP-13 to CMP-15 Status pill, banner, card | `.status-pill`, `.banner`, `.card` | none |
| CMP-16 Dialog | `.modal-backdrop`, `.modal-card`, `.modal-card--wide` | focus trap; Escape clicks the dialog's `*-cancel` action; initial focus from `data-autofocus` |
| CMP-21 Destructive confirmation | `.modal-card--wide` with `.modal-icon--danger`, `.danger-btn` | opens before the action; focus starts on Cancel; returns to the opening control |
| CMP-17 Toast | `.toast` | removed after `--toast-duration` (6 seconds); the timer pauses while the pointer is over it |
| CMP-18 States | `.state`, `.state--error`, `.spinner`, `.empty-note` | none |
| CMP-20 Logo tile | `.logo`, `.logo__mark` | none |
| CMP-22 App top bar | `.top-bar`, `.top-bar__title`, `.top-bar__tools`, `.context-chip`, `.top-bar__account`, `.account-btn` (add `.has-top-bar` to `.app-shell`) | the account menu; in the reference, `?shell=topbar` switches it on |
| CMP-23 List-detail | `.ld` (`.ld--single` for one pane), `.ld__pane`, `.ld__head`, `.count-badge`, `.ld__search`, `.ld__items`, `.ld-item` (`.selected`), `.ld-item__main`, `.ld-item__delete`, `.ld__detail`, `.ld-detail__head`, `.switch-row` | the list filters in place; on phones one pane at a time (`rolesScreen()` in `web/app.js`) |
| CMP-24 Tabs | `.tabs` (`role="tablist"`), `.tab` (`role="tab"`), `.tab__count`, `.tab-panel` | arrow keys, Home and End; the selected tab kept in view on phones |
| CMP-25 Chips, code labels | `.chip-groups`, `.chip-group`, `.chip-group__label`, `.chips`, `.chip`, `.chip__meta`, `.code-chip` | none |
| CMP-26 Stat card | `.stat-cards`, `.stat-card`, `.stat-card__icon` (`--success`, `--warning`), `.stat-card__value`, `.stat-card__total`, `.stat-card__label` | none |
| CMP-27 to CMP-34 List toolbar, segmented control, data freshness, attention list, masking, defined terms, dashboard panel, long forms | not in the web reference: these are design intents, not fixed layouts. Build them from the clause with the existing tokens and classes (`.filters`, `.search-wrap`, `.card`, `.status-pill`, `.banner`, `.stat-card`, `.code-chip`, `.state`) and tell the user what you added (SCP-4) | each clause's *Must* lines: keyboard use of the segmented control (CMP-28), definitions on hover, focus and tap (CMP-32), the exact update time (CMP-29) |
| FND-16 Phones (narrower than 768px) | one `@media (max-width: 767px)` block at the end of `components.css` (and of `app.css` for screens): the sidebar becomes the tab bar, `.profile__tab-label` and `.profile-menu-item--phone` appear, `.modal-card` becomes a bottom sheet; `.load-more`, `.choice`, `.choice-group`, `.sheet-actions` | `isPhone()` (`matchMedia("(max-width: 767px)")`): no hover or toggle sidebar modes; lists render "Load more" instead of the pager; the Filters sheet |

## 6b. Two rules that are easy to break (ACC-12, FND-18)

**Update in place; never rebuild the field the user is typing in.** A search box that re-renders the whole page on every keystroke destroys and re-creates the field, so the focus ring flashes and the caret can jump.
- Apps that render with `innerHTML`: on input, update only the regions that change (the result list, the count, a clear button) and leave the field alone. The reference does this in `refreshResidents()` and `refreshWardList()` in `web/app.js`; open sheets are updated with `refreshSheet()`, which replaces the sheet's contents, not the sheet.
- React, Vue and similar: keep the field mounted. Do not give it, or a container around it, a `key` that changes with the search text; do not render the field inside the component that is re-created for each result set.
- When a full redraw is unavoidable (paging, for example), give focus back with the ring already shown, not animated in (`focusQuiet()` in `web/app.js`).

**Make columns fit.** Add up the minimum column widths, the gaps between them and the row padding: at the narrowest width that shows the table, the total must not exceed the table's width. If it would, hide lower-priority columns at that width (the reference hides the avatar at 900px and below) or switch to the phone card layout. A row that runs past its table is an FND-18 error; check every table at all three widths (SCP-12).

**Break on the content width, not the screen width.** On a touch tablet the navigation pinned open with its toggle takes 248 of an 820 screen, leaving about 570 for the content (FND-18, CMP-11), and a screen-width `@media` query never notices. Make the content column a size container and switch layouts on its width: the reference sets `container: content / inline-size` on `.main` and uses `@container content (max-width: 720px)` (the `--content-compact-breakpoint` token) to stack the list-detail panes and wrap the top bar. Grids with a minimum column width use `minmax(min(<min>, 100%), 1fr)` so one column can never be wider than its container. Check every screen with the navigation collapsed and expanded (SCP-12).

## 7. Web reference: markup catalogue

The reference markup for **web** products, using the classes in `web/components.css`. Native products implement the clauses in `../policy/UI-4-components.md` with platform controls. Replace `…` with icons or content. Every interactive element is a real `<button>`, `<input>` or `<a>` (ACC-8).

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
<button class="danger-btn">Delete device</button>                 <!-- solid red: only the confirming button of a destructive action -->
<button class="link-btn">Need help?</button>                      <!-- text link -->
<button class="back-btn"><svg>…</svg>Back</button>                <!-- text with arrow -->
```
Modifiers: `.min-160` / `.min-150` set a minimum width.

### Text field, label, password eye
```html
<label><span class="label">Staff ID</span><input class="field" type="email" /></label>

<!-- invalid field (CMP-2): aria-invalid on the field, the message linked with aria-describedby -->
<label><span class="label">Date of birth</span><input class="field" aria-invalid="true" aria-describedby="dob-err" /></label>
<div class="field-error" id="dob-err"><svg>…alert…</svg><span>Enter a date as YYYY-MM-DD, for example 1948-03-07.</span></div>
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

### Phones: Load more, Filters sheet (FND-16)
```html
<!-- below a list, instead of the pager -->
<div class="load-more"><span class="load-more__count" role="status">Showing <strong>1–20</strong> of <strong>24</strong></span>
  <button type="button" class="secondary-btn">Load more</button></div>

<!-- Filters sheet: a .modal-card (a bottom sheet on phones) with plain choice lists -->
<div class="modal-backdrop"><div class="modal-card modal-card--wide" role="dialog" aria-modal="true" aria-labelledby="fs">
  <h2 id="fs">Filters</h2>
  <fieldset class="choice-group" role="radiogroup" aria-label="Zone"><legend>Zone</legend>
    <button type="button" class="choice" role="radio" aria-checked="true"><span class="choice__mark" aria-hidden="true"></span>North Wing</button>
  </fieldset>
  <fieldset class="choice-group"><legend>Care area</legend>
    <button type="button" class="choice" role="checkbox" aria-checked="false"><span class="choice__mark" aria-hidden="true"></span>Memory Care</button>
  </fieldset>
  <div class="sheet-actions"><button type="button" class="secondary-btn">Clear all</button><button type="button" class="primary-btn">Show 10 residents</button></div>
</div></div>
```
**Safe area:** pages that may run full screen on a phone (added to the home screen, or inside a native app's web view) need `viewport-fit=cover` in the viewport tag: `<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">`. The phone rules in `components.css` then pad the page header, content, tab bar, sheets and toasts with `env(safe-area-inset-*)`, so nothing sits under the status bar, notch or home indicator. Native apps use the platform's safe-area layout (SwiftUI safe areas, Android window insets).

The tab bar needs no extra markup: on phones the sidebar markup in "Page shell and sidebar" becomes it. Add `<span class="profile__tab-label">Account</span>` inside `.profile`, and a `.profile-menu-item--phone` Sign out item in the staff menu.

### App top bar, list-detail, tabs, chips, stat cards (CMP-22 to CMP-26)
```html
<!-- top bar: replaces .page-header; add has-top-bar to .app-shell so the sidebar account row is hidden -->
<header class="top-bar">
  <div class="top-bar__title"><h1>Staff roles</h1><p>One-line subtitle</p></div>
  <div class="top-bar__tools">
    <span class="status-pill"><span></span> Gateway connected</span>
    <span class="context-chip"><svg>…</svg><span>Gateway <strong>RSM-GW-1408</strong></span></span>
    <div class="top-bar__account">   <!-- the .profile-menu goes in here while open -->
      <button type="button" class="account-btn" aria-haspopup="menu" aria-expanded="false" aria-label="Staff menu: Name, Role">
        <span class="account-btn__avatar">AM</span><span class="account-btn__who"><strong>Name</strong><small>Role</small></span><svg>…</svg>
      </button></div></div>
</header>

<!-- list-detail -->
<div class="ld">
  <section class="ld__pane" aria-label="Roles">
    <div class="ld__head"><h2>Roles</h2><span class="count-badge">8</span></div>
    <div class="ld__search"><div class="search-wrap"><svg>…</svg><input class="filter-field" placeholder="Search roles…" /></div></div>
    <div class="ld__items">
      <div class="ld-item selected">
        <button type="button" class="ld-item__main" aria-current="true"><span class="ld-item__avatar" aria-hidden="true">CN</span>
          <span class="ld-item__text"><span class="ld-item__name truncate">Charge nurse</span><span class="ld-item__meta truncate">CHARGE_NURSE</span></span><svg>…</svg></button>
        <button type="button" class="icon-button icon-button--danger ld-item__delete" aria-label="Delete the Charge nurse role"><svg>…</svg></button>
      </div>
    </div>
  </section>
  <section class="ld__pane ld__detail" aria-labelledby="t">
    <div class="ld-detail__head"><h2 id="t">Charge nurse</h2><span class="code-chip">CHARGE_NURSE</span>
      <span class="switch-row"><button class="toggle on" role="switch" aria-checked="true" aria-labelledby="a"><span></span></button><span id="a">Active</span></span></div>
    <div class="tabs" role="tablist" aria-label="Role details">
      <button class="tab" role="tab" id="tab-o" aria-selected="true" aria-controls="p" tabindex="0"><svg>…</svg><span>Overview</span></button>
      <button class="tab" role="tab" id="tab-a" aria-selected="false" aria-controls="p" tabindex="-1"><svg>…</svg><span>Actions</span><span class="tab__count">11</span></button>
    </div>
    <div class="tab-panel" role="tabpanel" id="p" aria-labelledby="tab-o">
      <div class="stat-cards">
        <div class="stat-card"><div class="stat-card__icon"><svg>…</svg></div><div><div class="stat-card__value">5<span class="stat-card__total"> / 8</span></div><span class="stat-card__label">Pages in the menu</span></div></div>
      </div>
      <div class="chip-groups"><div class="chip-group"><div class="chip-group__label">Devices</div>
        <div class="chips"><span class="chip">Devices<span class="chip__meta">View · Pair · Unpair</span></span></div></div></div>
    </div>
  </section>
</div>
```
A checkbox set in columns is `.check-grid` holding `.remember` checkbox rows. Success and warning banners add `.banner--success` or `.banner--warning`. The reference screen is `#/roles` (`rolesScreen()` in `web/app.js`); `?show=role-delete` opens its delete confirmation.

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

<!-- destructive confirmation (CMP-21): alertdialog, red icon, Cancel first and focused, red button repeats the verb -->
<div class="modal-backdrop"><div class="modal-card modal-card--wide" role="alertdialog" aria-modal="true" aria-labelledby="m3" aria-describedby="m3d">
  <div class="modal-icon modal-icon--danger"><svg>…trash…</svg></div><h2 id="m3">Delete Scale 07?</h2>
  <p id="m3d">What is lost, what is kept, and how to get it back.</p>
  <div class="modal-actions modal-actions--end"><button class="secondary-btn" data-autofocus>Cancel</button><button class="danger-btn">Delete device</button></div>
</div></div>

<!-- section heading inside page content; add section-head--tight for a smaller subtitle -->
<div class="section-head"><div><h2>Section title</h2><p>Section subtitle.</p></div><!-- optional right-hand content --></div>

<div class="toast" role="status"><span class="toast__check"><svg>…</svg></span>Scan complete</div>   <!-- remove after --toast-duration (6 s); pause while hovered -->

<div class="state" role="status" aria-live="polite"><div class="spinner" aria-hidden="true"></div>Loading…</div>
<div class="state state--error" role="alert"><strong>Couldn't load data.</strong> … <button class="secondary-btn">Retry</button></div>
<div class="empty-note">No results match these filters.</div>
```
Utilities: `.truncate` (single-line ellipsis), `.sr-only` (visually hidden text for screen readers).

## 8. Web behaviour (`web/app.js`)

The markup in section 7 is CSS only. Opening, closing and focus behaviour for the dropdowns, multi-select, sidebar toggle and staff menu live in `web/app.js`: event delegation on `data-action`, one state object, and a `render()` function that rebuilds the page and restores focus. Copy the patterns, not the demo content (SCP-8): the Rossmax Connect product name, the residents, devices, zones and readings, and the staff names are all fictional demo data.

## 9. Known limits

- There is no dark mode (FND-15).
- The checker (`../tools/guard.py`) checks colours on every platform and CSS on web. It cannot judge layout, markup or behaviour, so checking the work against the policies (SCP-9) and the browser check (SCP-12) still apply.
