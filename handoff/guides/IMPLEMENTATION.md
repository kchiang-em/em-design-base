# Implementation guide: building EncoreMed interfaces on any platform

This guide explains **how** to implement the UI policies in `../policy/` on web and native platforms: where the values live, how to translate them per platform, and the web reference markup. It does not restate the rules: each section cites the clauses it implements (for example FND-9). When a clause and this guide seem to disagree, the clause wins; tell the user about the mismatch (SCP-7).

## 1. What is where

| Folder | What it holds |
|---|---|
| `../policy/` | the rules (UI-1 to UI-6), with clause IDs. Read them first. |
| `../tokens/` | `design-tokens.json`, the portable source of every value; `DESIGN-TOKENS.md`, the same as a readable list |
| `../tools/` | `guard.py` (the conformance checker), `make_theme.py` and `logo_colours.py` (client themes). See `../tools/README.md`. |
| `../web/` | the web reference implementation: `tokens.css`, `components.css`, `app.js` (component behaviour) and `export_tokens.py` |
| `THEMING.md` | the step-by-step procedure for re-colouring a product for a client (implements UI-5) |

## 2. Setting up a project

**Web.** Copy `web/tokens.css` and `web/components.css` into the project. Every page loads the stylesheets in this order:

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
| FND-17 charts | `chart-1` to `chart-7` in order, `chart-other`; `chart-surface` names what is behind the charts (set it to `var(--bg)` for transparent charts on the page) |
| UI-4 components | `btn-*` (CMP-1), `field-*` (CMP-2), `pw-*` (CMP-3), `clear-btn-*`, `search-*` (CMP-4), `checkbox-*`, `remember-*` (CMP-5), `toggle-*` (CMP-6), `dd-*` (CMP-7), `ms-*` (CMP-8), `card-*` (CMP-9, interactive surfaces), `pager-*` (CMP-10), `nav-*` (CMP-11), `logo-mark-*` (CMP-20) |

## 4. Typeface (FND-5, FND-6)

- **Web:** `--font-sans` lists Acumin first and Arial after. If the company has an Adobe Fonts web kit with Acumin, load the kit and keep `--font-sans` as it is; otherwise Arial is used automatically.
- **Native:** use the system font (SF Pro, Roboto, Segoe UI) unless the company confirms a licence that allows embedding Acumin in an app.
- Only Regular (400) and Bold (700) are used, and every size comes from the `text-*` tokens, so layouts hold with the fallback.

## 5. Translating to a platform

| Baseline | Web | iOS (SwiftUI/UIKit) | Android (Compose/Views) | Desktop / cross-platform |
|---|---|---|---|---|
| Colours | CSS variables | an asset catalog or a `Color` extension generated from the tokens | `colors.xml` or a Compose `ColorScheme` | the framework's colour constants |
| Type | `--font-sans` stack | Acumin if licensed, else SF Pro; sizes from `text-*` | Acumin if licensed, else Roboto | system font fallback |
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
| CMP-11 Navigation | `.app-shell`, `.sidebar`, `.nav-item`, `.profile`, `.profile-menu` | collapse and expand, staff menu |
| CMP-12 Page header | `.page-header`, `.section-head` | none |
| CMP-13 to CMP-15 Status pill, banner, card | `.status-pill`, `.banner`, `.card` | none |
| CMP-16 Dialog | `.modal-backdrop`, `.modal-card`, `.modal-card--wide` | focus trap; Escape clicks the dialog's `*-cancel` action; initial focus from `data-autofocus` |
| CMP-21 Destructive confirmation | `.modal-card--wide` with `.modal-icon--danger`, `.danger-btn` | opens before the action; focus starts on Cancel; returns to the opening control |
| CMP-17 Toast | `.toast` | removed after `--toast-duration` (6 seconds); the timer pauses while the pointer is over it |
| CMP-18 States | `.state`, `.state--error`, `.spinner`, `.empty-note` | none |
| CMP-20 Logo tile | `.logo`, `.logo__mark` | none |

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

- The typeface is not bundled (FND-6).
- Phone layouts (FND-16) are defined as rules but not implemented in the web reference. There is no dark mode (FND-15).
- The web reference does not show every UI-6 rule: its demo data uses relative times such as "Yesterday, 16:42" (CNT-2 allows relative times only within 24 hours).
- The checker (`../tools/guard.py`) checks colours on every platform and CSS on web. It cannot judge layout, markup or behaviour, so the hand checks in SCP-9 still apply.
