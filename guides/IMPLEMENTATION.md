# Implementation guide: building EncoreMed interfaces on any platform

This guide explains **how** to implement the UI policies in `../policy/` on web and native platforms: where the values live, how to translate them per platform, and the web reference markup. It does not restate the rules: each section cites the clauses it implements (for example FND-9). When a clause and this guide seem to disagree, the clause wins; tell the user about the mismatch (SCP-7).

## 1. What is where

| Folder | What it holds |
|---|---|
| `../policy/` | the rules (UI-1 to UI-5), with clause IDs. Read them first. |
| `../tokens/` | `design-tokens.json`, the portable source of every value; `DESIGN-TOKENS.md`, the same as a readable list; `theme.example.css` and `theme.example.json`, client theme templates (UI-5) |
| `../tools/` | `guard.py` (the conformance checker), `make_theme.py` and `logo_colours.py` (client themes). See `../tools/README.md`. |
| `../web/` | the web reference implementation: `tokens.css`, `components.css`, `app.js` (component behaviour) and `export_tokens.py` |
| `THEMING.md` | the step-by-step procedure for re-colouring a product for a client (implements UI-5) |

## 2. Setting up a project

**Web.** Copy `web/tokens.css` and `web/components.css` into the project. Every page loads the stylesheets in this order:

1. `tokens.css` (the design tokens)
2. `theme.css` (a client's colours, optional, THM-1)
3. `app-tokens.css` (the product's own tokens, optional)
4. `components.css` (the shared components)
5. `app.css` (the product's own rules)

You may extend or modify the two shared files; add new tokens and classes rather than renaming or deleting existing ones (SCP-4). Use the markup in section 7.

**Native or other.** Generate the platform's constants (colours, spacing, radii, type sizes, durations) from `tokens/design-tokens.json`, keeping the token names (SCP-3). Then build screens from the component clauses in `../policy/UI-4-components.md`, using section 5 for the platform mapping.

## 3. Tokens

Tokens come in three tiers, each built from the one before:

| Tier | Examples | Meaning |
|---|---|---|
| Palette | `em-navy-core`, `em-green-core` | the official colours (FND-1) |
| Semantic | `brand-600`, `ink-700`, `accent-500`, `space-lg`, `radius-md`, `text-sm`, `shadow-md` | roles: text, brand, status, spacing, radius, type, elevation |
| Component | `btn-primary-bg-hover`, `field-h`, `dd-option-bg-hover`, `nav-w-expanded` | the values of one control (UI-4) |

- **Naming:** `{component}-{variant?}-{property}-{state?}`, for example `btn-primary-bg-hover`. In CSS they are written `--btn-primary-bg-hover`.
- **`design-tokens.json`** lists every token with its type (`color`, `dimension`, `shadow`, `fontFamily`, `fontWeight`, `number`, `duration`, `other`), its alias (`{brand-600}`) and its resolved value. Generate constants from it, or copy values from `DESIGN-TOKENS.md`.
- **Raw colours** appear only in the palette and semantic tiers of `tokens.css` and in a client theme (SCP-3, THM-1). Component tokens alias semantic tokens.
- **Computed values:** a few values are written as a colour plus an opacity: white overlays on the navy sidebar (white at 10, 15, 50, 70 and 80%), the keyboard focus ring (navy at 18%, 3px, ACC-5) and the pressed ring (amber `#FFB020` at 55%, 3px, ACC-3).

**Where each rule's values live:**

| Clause | Tokens |
|---|---|
| FND-1 palette | `em-*` |
| FND-2, FND-3 system and status colours | `danger-*` (red), `warning-*` (orange), `accent-*` and `em-green*`, `em-mint` (green), `amber-*` (pressed) |
| FND-5 typeface, FND-7 type scale | `font-sans`, `text-*`; weights `weight-medium` (400, Regular), `weight-semibold` and `weight-bold` (both 700, Bold). The names are historical: only 400 and 700 are used. |
| FND-8 spacing | `space-2xs` to `space-5xl` |
| FND-9 control sizes | `control-h-sm` to `control-h-2xl` |
| FND-10 radius | `radius-sm` to `radius-circle` |
| FND-11 elevation | `shadow-sm`, `shadow-md`, `shadow-lg` |
| FND-13 motion | `nav-duration` (200ms), `control-transition` (150ms), `dd-chevron-duration` (120ms) |
| ACC-3 pressed | `pressed-bg`, `pressed-border`, `pressed-fg`, `pressed-on-dark`, `pressed-ring` |
| ACC-4 disabled | `disabled-opacity` and each component's `-disabled` tokens |
| ACC-5 focus | `focus-ring` |
| ACC-6 soft grey | `ink-400` (placeholders, helper text and icons only) |
| UI-4 components | `btn-*` (CMP-1), `field-*` (CMP-2), `pw-*` (CMP-3), `clear-btn-*`, `search-*` (CMP-4), `checkbox-*`, `remember-*` (CMP-5), `toggle-*` (CMP-6), `dd-*` (CMP-7), `ms-*` (CMP-8), `card-*` (CMP-9, interactive surfaces), `pager-*` (CMP-10), `nav-*` (CMP-11), `logo-mark-*` (CMP-20) |

## 4. Typeface (FND-5, FND-6)

- **Web:** `--font-sans` lists Acumin first and Arial after. If the company has an Adobe Fonts web kit with Acumin, load the kit and keep `--font-sans` as it is; otherwise Arial is used automatically.
- **Native:** use the system font (SF Pro, Roboto, Segoe UI) unless the company confirms a licence that allows embedding Acumin in an app.
- Only Regular (400) and Bold (700) are used, and every size comes from the `text-*` tokens, so layouts hold with the fallback.

## 5. Translating to a platform

| Baseline | Web | iOS (SwiftUI/UIKit) | Android (Compose/Views) | Desktop / cross-platform |
|---|---|---|---|---|
| Colours | CSS variables | an asset catalog or a `Color` extension generated from the tokens | `colors.xml` or a Compose `ColorScheme` | a theme file |
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
| CMP-1 Buttons | `.primary-btn`, `.secondary-btn`, `.icon-button`, `.link-btn`, `.back-btn` | none |
| CMP-2, CMP-3 Text and password field | `.field`, `.filter-field`, `.pw-wrap`, `.pw-toggle` | show/hide password |
| CMP-4 Search field | `.search-wrap`, `.search__clear` | clear button only while there is text |
| CMP-5, CMP-6 Checkbox and switch | `.remember`, `.toggle` | toggles `aria-checked` |
| CMP-7 Dropdown | `.dd`, `.dd--field`, `.dd--sm`, `.dd--up` | open, close, focus, arrow keys, Escape |
| CMP-8 Multi-select | `.ms` | search, multiple picks, clear |
| CMP-9, CMP-10 Table and pagination | `.table-card`, `.table-head`, `.table-foot`, `.pager` | sliding window of five pages |
| CMP-11 Navigation | `.app-shell`, `.sidebar`, `.nav-item`, `.profile`, `.profile-menu` | collapse and expand, staff menu |
| CMP-12 Page header | `.page-header`, `.section-head` | none |
| CMP-13 to CMP-15 Status pill, banner, card | `.status-pill`, `.banner`, `.card` | none |
| CMP-16 Dialog | `.modal-backdrop`, `.modal-card`, `.modal-card--wide` | **not in the reference:** add the focus trap and Escape-to-cancel that CMP-16 requires |
| CMP-17 Toast | `.toast` | removed after about 2 seconds |
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

## 8. Web behaviour (`web/app.js`)

The markup in section 7 is CSS only. Opening, closing and focus behaviour for the dropdowns, multi-select, sidebar toggle and staff menu live in `web/app.js`: event delegation on `data-action`, one state object, and a `render()` function that rebuilds the page and restores focus. Copy the patterns, not the demo content (SCP-8). The reference does not yet implement the dialog's focus trap and Escape-to-cancel (CMP-16); add them.

## 9. Known limits

- The typeface is not bundled (FND-6).
- There is no phone layout (FND-14) and no dark mode (FND-15).
- The soft grey `ink-400` is 3.5:1 on white: placeholders, helper text and icons only (ACC-6).
- The checker (`../tools/guard.py`) checks colours on every platform and CSS on web. It cannot judge layout, markup or behaviour, so the hand checks in SCP-9 still apply.
