# Design tokens

> Generated from `tokens.css` by `export_tokens.py`. Do not edit by hand: change `tokens.css`, then run `python3 export_tokens.py`.
> Machine-readable copy: `design-tokens.json` (aliases written as `{token-name}`, for generating platform constants or importing into design tools).

## How the tokens are layered

| Tier | What it holds | Who uses it |
|---|---|---|
| **Palette** | The official EncoreMed colours (`--em-*`), from the official brand guideline (CMYK converted to sRGB) and its colour-blind-safe set. | Only the semantic tier. |
| **Semantic** | Roles built from the palette: neutrals, text, brand, accent, status, type, spacing, radius, shadow. | Component tokens, and layout rules. |
| **Component** | Sizes, colours and states for each control: buttons, fields, dropdowns, pagination, checkbox, toggle, sidebar nav. | Component rules (`components.css`). New components should start here. |
| **App** | Screen-specific values (login panel, residents table columns, filter bar, list rows), in `app-tokens.css`. Not part of the reusable design system. | `app.css` only. |

## Rules for new components

1. **No raw colours or pixel heights in a rule.** Use a component token; if none fits, add one to the component tier in `tokens.css` first.
2. **Heights come from the control size scale** (`--control-h-sm` 32, `-md` 36, `-lg` 40, `-xl` 44, `-2xl` 48 px). Do not invent other heights.
3. **Every control has the same states:** default, hover, pressed (amber, `--pressed-*`), disabled, and keyboard focus (`--focus-ring`).
4. **Text colour contrast:** body and secondary text must stay at 4.5:1 or better on their background. The green and mint palette colours are for fills, dots and icons, not text.
5. **Name tokens** `--{component}-{variant?}-{property}-{state?}` (for example `--btn-primary-bg-hover`).

## Palette tokens

### Official palette

| Token | Value | Resolves to |
|---|---|---|
| `--em-navy-core` | `#023c6e` <br><sub>brand core: navy</sub> |  |
| `--em-green-core` | `#16ad85` <br><sub>brand core: green</sub> |  |
| `--em-blue` | `#16537a` <br><sub>brand secondary: blue</sub> |  |
| `--em-green-soft` | `#4faa91` <br><sub>brand secondary: mint-green</sub> |  |
| `--em-grey-dark` | `#3a3a3c` <br><sub>brand secondary: dark grey</sub> |  |
| `--em-navy` | `#0e4473` <br><sub>colour-blind safe: navy</sub> |  |
| `--em-slate` | `#4c6173` <br><sub>colour-blind safe: slate</sub> |  |
| `--em-green` | `#4ba67b` <br><sub>colour-blind safe: green</sub> |  |
| `--em-mint` | `#9cd9bc` <br><sub>colour-blind safe: mint</sub> |  |
| `--em-grey-light` | `#f2f2f2` <br><sub>colour-blind safe: light grey</sub> |  |

## Semantic tokens

### Colour: neutrals, text, brand, status

| Token | Value | Resolves to |
|---|---|---|
| `--white` | `#ffffff` |  |
| `--bg` | `var(--em-grey-light)` | `#f2f2f2` |
| `--surface-subtle` | `#f8f8f8` |  |
| `--surface-muted` | `#edeef0` |  |
| `--border` | `#dcdfe3` |  |
| `--border-strong` | `#c7ccd2` |  |
| `--ink-300` | `#b4bdc6` |  |
| `--ink-400` | `#616f7b` |  |
| `--ink-500` | `#5a6c7d` |  |
| `--ink-600` | `var(--em-slate)` | `#4c6173` |
| `--ink-700` | `var(--em-grey-dark)` | `#3a3a3c` |
| `--ink-900` | `var(--em-navy)` | `#0e4473` |
| `--brand-50` | `#eef4fb` |  |
| `--brand-100` | `#d6e5f5` |  |
| `--brand-300` | `#7fa9d3` |  |
| `--brand-400` | `#3f7ab5` |  |
| `--brand-500` | `var(--em-blue)` | `#16537a` |
| `--brand-600` | `var(--em-navy-core)` | `#023c6e` |
| `--brand-700` | `#01305a` |  |
| `--brand-800` | `#012646` |  |
| `--brand-900` | `#011c34` |  |
| `--brand-950` | `#01121f` |  |

### Amber (complement of the logo navy): pressed / clicked state

| Token | Value | Resolves to |
|---|---|---|
| `--amber-50` | `#fff4dc` |  |
| `--amber-400` | `#ffb020` |  |
| `--amber-600` | `#b45309` |  |

### Accent (logo green): live / positive signals

| Token | Value | Resolves to |
|---|---|---|
| `--accent-50` | `#e8f7f2` |  |
| `--accent-100` | `#c9eee1` |  |
| `--accent-300` | `var(--em-mint)` | `#9cd9bc` |
| `--accent-400` | `var(--em-green-soft)` | `#4faa91` |
| `--accent-500` | `var(--em-green-core)` | `#16ad85` |
| `--accent-600` | `#0f8c6b` |  |
| `--accent-700` | `#0b7258` |  |
| `--danger-600` | `#dc2626` |  |
| `--danger-700` | `#b91c1c` |  |
| `--danger-300` | `#fca5a5` |  |
| `--danger-50` | `#fef2f2` |  |
| `--warning-700` | `#9a5a1f` <br><sub>text (5.5:1 on white, 5.0:1 on the warning tint)</sub> |  |
| `--warning-600` | `#b36b28` <br><sub>icons and borders (4.2:1 on white: not for text)</sub> |  |
| `--warning-400` | `#d78b4c` |  |
| `--warning-50` | `#fff2e4` |  |
| `--info-100` | `#d7e7f7` <br><sub>soft blue tint (also used for avatar tints)</sub> |  |

### Status: positive / success / live. The classic status green, separate from the brand green (accent-*).

| Token | Value | Resolves to |
|---|---|---|
| `--success-50` | `#f0fdf4` |  |
| `--success-500` | `#16a34a` <br><sub>fills only (3.3:1 on white)</sub> |  |
| `--success-600` | `#15803d` <br><sub>dots and icons; text on white (5.0:1)</sub> |  |
| `--success-700` | `#166534` <br><sub>text on the success tint</sub> |  |

### Status: information. The brand guideline's secondary blue, fixed so a client theme does not move it.

| Token | Value | Resolves to |
|---|---|---|
| `--info-50` | `#e3eaef` |  |
| `--info-600` | `#16537a` |  |

### Borders that identify a control (fields, dropdown triggers): at least 3:1 on white and on the page background

| Token | Value | Resolves to |
|---|---|---|
| `--border-control` | `#808c98` |  |
| `--chart-surface` | `var(--white)` <br><sub>what is BEHIND the charts: the card, or the page background when charts are transparent. Contrast is checked against it</sub> | `#ffffff` |
| `--chart-1` | `var(--em-navy-core)` | `#023c6e` |
| `--chart-2` | `#de6872` <br><sub>coral</sub> |  |
| `--chart-3` | `#256d73` <br><sub>dark teal</sub> |  |
| `--chart-4` | `#a6678c` <br><sub>plum</sub> |  |
| `--chart-5` | `#119d78` <br><sub>brand green, darkened to 3.4:1</sub> |  |
| `--chart-6` | `#5b92a7` <br><sub>teal, darkened to 3.4:1</sub> |  |
| `--chart-7` | `#8567cc` <br><sub>violet (4.4:1); mint cannot reach 3:1 without becoming another green</sub> |  |
| `--chart-other` | `#737373` <br><sub>neutral grey for "Other", totals and reference lines (slate looks like chart-3 to colour-blind readers)</sub> |  |

### White overlays (sidebar, login panel)

| Token | Value | Resolves to |
|---|---|---|
| `--white-10` | `rgb(255 255 255 / 10%)` |  |
| `--white-15` | `rgb(255 255 255 / 15%)` |  |
| `--white-50` | `rgb(255 255 255 / 50%)` |  |
| `--white-70` | `rgb(255 255 255 / 70%)` |  |
| `--white-80` | `rgb(255 255 255 / 80%)` |  |

### Type

| Token | Value | Resolves to |
|---|---|---|
| `--font-sans` | `"Acumin Variable Concept", "Acumin Pro", Arial, "Helvetica Neue", Helvetica, sans-serif` |  |
| `--text-xs` | `13px` |  |
| `--text-sm` | `14px` |  |
| `--text-base` | `15px` |  |
| `--text-md` | `16px` |  |
| `--text-lg` | `18px` |  |
| `--text-xl` | `20px` |  |
| `--text-2xl` | `26px` |  |
| `--text-3xl` | `36px` |  |
| `--weight-medium` | `400` |  |
| `--weight-semibold` | `700` |  |
| `--weight-bold` | `700` |  |

### Spacing (4px grid)

| Token | Value | Resolves to |
|---|---|---|
| `--space-2xs` | `2px` |  |
| `--space-xs` | `4px` |  |
| `--space-sm` | `8px` |  |
| `--space-md` | `12px` |  |
| `--space-lg` | `16px` |  |
| `--space-xl` | `20px` |  |
| `--space-2xl` | `24px` |  |
| `--space-3xl` | `32px` |  |
| `--space-4xl` | `48px` |  |
| `--space-5xl` | `64px` |  |

### Radius

| Token | Value | Resolves to |
|---|---|---|
| `--radius-sm` | `4px` |  |
| `--radius-md` | `8px` |  |
| `--radius-lg` | `12px` |  |
| `--radius-xl` | `16px` |  |
| `--radius-pill` | `999px` |  |
| `--radius-circle` | `50%` |  |

### Elevation

| Token | Value | Resolves to |
|---|---|---|
| `--shadow-sm` | `0 1px 2px rgb(0 0 0 / 8%)` |  |
| `--shadow-md` | `0 8px 24px rgb(2 60 110 / 14%)` |  |
| `--shadow-lg` | `0 20px 48px rgb(1 28 52 / 26%)` |  |
| `--shadow-brand` | `0 5px 14px rgb(2 60 110 / 22%)` |  |
| `--focus-ring` | `0 0 0 2px var(--white), 0 0 0 4px var(--brand-600)` <br><sub>double ring: navy shows on light surfaces, white on dark ones</sub> | `0 0 0 2px #ffffff, 0 0 0 4px #023c6e` |

## Component tokens

### Control size scale: every button, field and trigger takes one of these heights

| Token | Value | Resolves to |
|---|---|---|
| `--control-h-sm` | `32px` |  |
| `--control-h-md` | `36px` |  |
| `--control-h-lg` | `40px` |  |
| `--control-h-xl` | `44px` |  |
| `--control-h-2xl` | `48px` |  |
| `--control-radius` | `var(--radius-md)` | `8px` |
| `--control-transition` | `150ms` |  |
| `--toast-duration` | `6000ms` <br><sub>how long a toast stays (CMP-17); it pauses while the pointer is over it</sub> |  |
| `--disabled-opacity` | `.55` |  |

### Pressed (clicked) state, shared by all controls

| Token | Value | Resolves to |
|---|---|---|
| `--pressed-bg` | `var(--amber-50)` | `#fff4dc` |
| `--pressed-border` | `var(--amber-600)` | `#b45309` |
| `--pressed-fg` | `var(--amber-600)` | `#b45309` |
| `--pressed-on-dark` | `var(--amber-400)` | `#ffb020` |
| `--pressed-ring` | `0 0 0 3px color-mix(in srgb, var(--amber-400) 55%, transparent)` | `0 0 0 3px color-mix(in srgb, #ffb020 55%, transparent)` |

### Keyboard focus

| Token | Value | Resolves to |
|---|---|---|
| `--btn-focus-ring` | `var(--focus-ring)` | `0 0 0 2px #ffffff, 0 0 0 4px #023c6e` |

### Text field

| Token | Value | Resolves to |
|---|---|---|
| `--field-h` | `var(--control-h-2xl)` | `48px` |
| `--field-h-compact` | `var(--control-h-xl)` | `44px` |
| `--field-padding-x` | `var(--space-lg)` | `16px` |
| `--field-bg` | `var(--white)` | `#ffffff` |
| `--field-fg` | `var(--ink-700)` | `#3a3a3c` |
| `--field-border` | `var(--border-control)` | `#808c98` |
| `--field-border-hover` | `var(--ink-500)` | `#5a6c7d` |
| `--field-border-error` | `var(--danger-600)` | `#dc2626` |
| `--field-error-fg` | `var(--danger-700)` | `#b91c1c` |
| `--field-error-gap` | `var(--space-xs)` | `4px` |
| `--field-border-focus` | `var(--brand-400)` | `#3f7ab5` |
| `--field-ring-focus` | `var(--focus-ring)` | `0 0 0 2px #ffffff, 0 0 0 4px #023c6e` |
| `--field-bg-disabled` | `var(--bg)` | `#f2f2f2` |
| `--field-fg-disabled` | `var(--ink-400)` | `#616f7b` |

### Button: primary (solid navy)

| Token | Value | Resolves to |
|---|---|---|
| `--btn-primary-h` | `var(--control-h-2xl)` | `48px` |
| `--btn-primary-padding-x` | `var(--space-xl)` | `20px` |
| `--btn-primary-bg` | `var(--brand-600)` | `#023c6e` |
| `--btn-primary-fg` | `var(--white)` | `#ffffff` |
| `--btn-primary-bg-hover` | `var(--brand-700)` | `#01305a` |
| `--btn-primary-bg-disabled` | `var(--ink-300)` | `#b4bdc6` |
| `--btn-primary-shadow` | `var(--shadow-brand)` | `0 5px 14px rgb(2 60 110 / 22%)` |
| `--btn-primary-bg-pressed` | `var(--brand-700)` | `#01305a` |
| `--btn-primary-ring-pressed` | `var(--pressed-ring)` | `0 0 0 3px color-mix(in srgb, #ffb020 55%, transparent)` |
| `--btn-primary-lift` | `-1px` |  |

### Button: secondary (white, tinted border)

| Token | Value | Resolves to |
|---|---|---|
| `--btn-secondary-h` | `var(--control-h-lg)` | `40px` |
| `--btn-secondary-padding-x` | `var(--space-lg)` | `16px` |
| `--btn-secondary-bg` | `var(--white)` | `#ffffff` |
| `--btn-secondary-fg` | `var(--ink-600)` | `#4c6173` |
| `--btn-secondary-border` | `var(--brand-100)` | `#d6e5f5` |
| `--btn-secondary-border-hover` | `var(--ink-300)` | `#b4bdc6` |
| `--btn-secondary-fg-hover` | `var(--brand-600)` | `#023c6e` |
| `--btn-secondary-bg-pressed` | `var(--pressed-bg)` | `#fff4dc` |
| `--btn-secondary-border-pressed` | `var(--pressed-border)` | `#b45309` |
| `--btn-secondary-fg-pressed` | `var(--pressed-fg)` | `#b45309` |

### Button: outline (compact, for rows and cards)

| Token | Value | Resolves to |
|---|---|---|
| `--btn-outline-h` | `var(--control-h-sm)` | `32px` |
| `--btn-outline-fg` | `var(--ink-500)` | `#5a6c7d` |
| `--btn-outline-border` | `var(--border)` | `#dcdfe3` |
| `--btn-outline-border-hover` | `var(--ink-300)` | `#b4bdc6` |
| `--btn-outline-fg-hover` | `var(--brand-600)` | `#023c6e` |
| `--btn-outline-bg-pressed` | `var(--pressed-bg)` | `#fff4dc` |
| `--btn-outline-border-pressed` | `var(--pressed-border)` | `#b45309` |
| `--btn-outline-fg-pressed` | `var(--pressed-fg)` | `#b45309` |

### Button: danger outline (delete)

| Token | Value | Resolves to |
|---|---|---|
| `--btn-danger-outline-fg` | `var(--danger-600)` | `#dc2626` |
| `--btn-danger-outline-border-hover` | `var(--danger-300)` | `#fca5a5` |
| `--btn-danger-outline-bg-hover` | `var(--danger-50)` | `#fef2f2` |

### Button: danger solid (clear all filters)

| Token | Value | Resolves to |
|---|---|---|
| `--btn-danger-h` | `var(--control-h-xl)` | `44px` |
| `--btn-danger-padding-x` | `var(--space-lg)` | `16px` |
| `--btn-danger-bg` | `var(--danger-600)` | `#dc2626` |
| `--btn-danger-fg` | `var(--white)` | `#ffffff` |
| `--btn-danger-bg-hover` | `var(--danger-700)` | `#b91c1c` |
| `--btn-danger-bg-pressed` | `var(--amber-600)` | `#b45309` |
| `--btn-danger-bg-disabled` | `var(--surface-muted)` | `#edeef0` |
| `--btn-danger-fg-disabled` | `var(--ink-300)` | `#b4bdc6` |
| `--btn-danger-gap` | `var(--space-sm)` | `8px` |
| `--btn-danger-font-size` | `var(--text-sm)` | `14px` |
| `--btn-danger-font-weight` | `var(--weight-bold)` | `700` |
| `--btn-danger-icon-size` | `18px` |  |
| `--btn-danger-compact-w` | `var(--btn-danger-h)` <br><sub>icon-only: a square the same size as the button height</sub> | `44px` |

### Button: icon only (square, outlined)

| Token | Value | Resolves to |
|---|---|---|
| `--btn-icon-size` | `var(--control-h-md)` | `36px` |
| `--btn-icon-fg` | `var(--ink-400)` | `#616f7b` |
| `--btn-icon-border` | `var(--border)` | `#dcdfe3` |
| `--btn-icon-border-hover` | `var(--ink-300)` | `#b4bdc6` |
| `--btn-icon-fg-hover` | `var(--brand-600)` | `#023c6e` |
| `--btn-icon-bg-pressed` | `var(--pressed-bg)` | `#fff4dc` |
| `--btn-icon-border-pressed` | `var(--pressed-border)` | `#b45309` |
| `--btn-icon-fg-pressed` | `var(--pressed-fg)` | `#b45309` |

### Button: tinted arrow (resident row action)

| Token | Value | Resolves to |
|---|---|---|
| `--btn-tint-size` | `var(--control-h-md)` | `36px` |
| `--btn-tint-bg` | `var(--brand-50)` | `#eef4fb` |
| `--btn-tint-fg` | `var(--brand-600)` | `#023c6e` |
| `--btn-tint-bg-hover` | `var(--brand-600)` | `#023c6e` |
| `--btn-tint-fg-hover` | `var(--white)` | `#ffffff` |

### Button: inverse (white, on a navy card)

| Token | Value | Resolves to |
|---|---|---|
| `--btn-inverse-size` | `var(--control-h-xl)` | `44px` |
| `--btn-inverse-bg` | `var(--white)` | `#ffffff` |
| `--btn-inverse-fg` | `var(--brand-700)` | `#01305a` |
| `--btn-inverse-bg-hover` | `var(--brand-50)` | `#eef4fb` |
| `--btn-inverse-shadow` | `var(--shadow-sm)` | `0 1px 2px rgb(0 0 0 / 8%)` |
| `--btn-inverse-bg-pressed` | `var(--pressed-bg)` | `#fff4dc` |
| `--btn-inverse-fg-pressed` | `var(--pressed-fg)` | `#b45309` |

### Button: text / link

| Token | Value | Resolves to |
|---|---|---|
| `--btn-link-fg` | `var(--brand-600)` | `#023c6e` |
| `--btn-text-fg` | `var(--ink-400)` | `#616f7b` |
| `--btn-link-fg-pressed` | `var(--pressed-fg)` | `#b45309` |
| `--btn-text-fg-pressed` | `var(--pressed-fg)` | `#b45309` |

### Clear (x) button inside a field

| Token | Value | Resolves to |
|---|---|---|
| `--clear-btn-size` | `24px` |  |
| `--clear-btn-fg` | `var(--ink-700)` | `#3a3a3c` |
| `--clear-btn-bg` | `var(--surface-muted)` | `#edeef0` |
| `--clear-btn-fg-hover` | `var(--ink-900)` | `#0e4473` |
| `--clear-btn-bg-hover` | `var(--border-strong)` | `#c7ccd2` |
| `--clear-btn-radius` | `var(--radius-pill)` | `999px` |
| `--clear-btn-icon-size` | `14px` |  |
| `--search-clear-right` | `12px` |  |
| `--search-input-padding-right-active` | `44px` |  |

### Pagination

| Token | Value | Resolves to |
|---|---|---|
| `--pager-btn-size` | `var(--control-h-sm)` | `32px` |
| `--pager-btn-padding-x` | `var(--space-sm)` | `8px` |
| `--pager-icon-size` | `16px` |  |
| `--pager-gap` | `var(--space-xs)` | `4px` |
| `--pager-bg` | `var(--white)` | `#ffffff` |
| `--pager-fg` | `var(--ink-600)` | `#4c6173` |
| `--pager-border` | `var(--border)` | `#dcdfe3` |
| `--pager-bg-hover` | `var(--brand-50)` | `#eef4fb` |
| `--pager-border-hover` | `var(--ink-300)` | `#b4bdc6` |
| `--pager-fg-hover` | `var(--brand-600)` | `#023c6e` |
| `--pager-current-bg` | `var(--brand-600)` | `#023c6e` |
| `--pager-current-fg` | `var(--white)` | `#ffffff` |
| `--pager-disabled-opacity` | `.45` |  |
| `--pager-bg-pressed` | `var(--pressed-bg)` | `#fff4dc` |
| `--pager-border-pressed` | `var(--pressed-border)` | `#b45309` |
| `--pager-fg-pressed` | `var(--pressed-fg)` | `#b45309` |

### pagination: text variant (labelled First / Previous / Next / Last; icon-only below the compact breakpoint)

| Token | Value | Resolves to |
|---|---|---|
| `--pager-nav-padding-x` | `var(--space-md)` | `12px` |
| `--pager-nav-padding-x-compact` | `var(--space-sm)` | `8px` |
| `--pager-nav-gap` | `var(--space-xs)` | `4px` |
| `--pager-compact-breakpoint` | `1100px` <br><sub>documentation token: CSS media queries cannot read custom properties, so components.css repeats this value (export_tokens.py checks they match)</sub> |  |

### Dropdown (single select) and multi-select

| Token | Value | Resolves to |
|---|---|---|
| `--dd-trigger-h-sm` | `var(--control-h-sm)` | `32px` |
| `--dd-trigger-bg` | `var(--white)` | `#ffffff` |
| `--dd-trigger-fg` | `var(--ink-700)` | `#3a3a3c` |
| `--dd-trigger-border` | `var(--border-control)` | `#808c98` |
| `--dd-trigger-border-hover` | `var(--ink-500)` | `#5a6c7d` |
| `--dd-trigger-border-open` | `var(--brand-400)` | `#3f7ab5` |
| `--dd-chevron-fg` | `var(--ink-400)` | `#616f7b` |
| `--dd-panel-bg` | `var(--white)` | `#ffffff` |
| `--dd-panel-border` | `var(--border)` | `#dcdfe3` |
| `--dd-panel-radius` | `var(--radius-md)` | `8px` |
| `--dd-panel-shadow` | `var(--shadow-md)` | `0 8px 24px rgb(2 60 110 / 14%)` |
| `--dd-panel-z` | `40` |  |
| `--dd-list-max-h` | `200px` |  |
| `--dd-option-fg` | `var(--ink-700)` | `#3a3a3c` |
| `--dd-option-bg-hover` | `var(--surface-muted)` | `#edeef0` |
| `--dd-option-fg-selected` | `var(--brand-600)` | `#023c6e` |
| `--dd-option-check` | `var(--brand-600)` | `#023c6e` |
| `--dd-option-weight-selected` | `var(--weight-semibold)` | `700` |
| `--dd-option-bg-pressed` | `var(--pressed-bg)` | `#fff4dc` |
| `--dd-option-fg-pressed` | `var(--pressed-fg)` | `#b45309` |
| `--dd-trigger-border-pressed` | `var(--pressed-border)` | `#b45309` |
| `--ms-trigger-border-active` | `var(--brand-400)` | `#3f7ab5` |
| `--ms-trigger-padding-right` | `38px` |  |
| `--ms-trigger-padding-right-active` | `62px` |  |
| `--ms-placeholder-fg` | `var(--ink-500)` | `#5a6c7d` |
| `--ms-search-h` | `var(--control-h-md)` | `36px` |
| `--ms-empty-fg` | `var(--ink-400)` | `#616f7b` |

### Dropdown and multi-select: layout and variants (small = rows per page, dark = sidebar zone)

| Token | Value | Resolves to |
|---|---|---|
| `--dd-chevron-right` | `12px` |  |
| `--dd-chevron-size` | `14px` |  |
| `--dd-chevron-duration` | `120ms` |  |
| `--dd-panel-offset` | `var(--space-xs)` | `4px` |
| `--dd-list-gap` | `2px` |  |
| `--dd-list-padding` | `var(--space-xs)` | `4px` |
| `--dd-option-gap` | `var(--space-sm)` | `8px` |
| `--dd-option-padding-y` | `var(--space-sm)` | `8px` |
| `--dd-option-padding-x` | `var(--space-md)` | `12px` |
| `--dd-option-radius` | `var(--radius-sm)` | `4px` |
| `--dd-option-font-size` | `var(--text-xs)` | `13px` |
| `--dd-option-icon-size` | `14px` |  |
| `--dd-sm-min-w` | `68px` |  |
| `--dd-sm-padding-left` | `var(--space-md)` | `12px` |
| `--dd-sm-padding-right` | `var(--space-2xl)` | `24px` |
| `--dd-sm-font-size` | `var(--text-xs)` | `13px` |
| `--dd-sm-font-weight` | `var(--weight-semibold)` | `700` |
| `--dd-sm-chevron-right` | `10px` |  |

### Dropdown: field variant (sits in the filter bar, same height and look as a text field)

| Token | Value | Resolves to |
|---|---|---|
| `--dd-field-h` | `var(--field-h-compact)` | `44px` |
| `--dd-field-padding-left` | `var(--space-md)` | `12px` |
| `--dd-field-padding-right` | `var(--space-3xl)` | `32px` |
| `--dd-field-font-size` | `var(--text-sm)` | `14px` |
| `--dd-field-chevron-right` | `13px` |  |
| `--dd-prefix-fg` | `var(--ink-500)` | `#5a6c7d` |
| `--dd-prefix-gap` | `var(--space-xs)` | `4px` |
| `--dd-footer-padding` | `var(--space-sm) var(--space-md)` | `8px 12px` |
| `--dd-footer-fg` | `var(--ink-500)` | `#5a6c7d` |
| `--dd-footer-font-size` | `var(--text-xs)` | `13px` |
| `--ms-chevron-right` | `13px` |  |
| `--ms-chevron-size` | `16px` |  |
| `--ms-clear-right` | `36px` |  |
| `--ms-search-padding` | `var(--space-sm) var(--space-sm) var(--space-xs)` | `8px 8px 4px` |
| `--ms-search-input-padding-left` | `var(--space-md)` | `12px` |
| `--ms-search-input-padding-right` | `36px` |  |
| `--ms-search-input-font-size` | `var(--text-xs)` | `13px` |
| `--ms-search-icon-right` | `20px` |  |
| `--ms-search-icon-size` | `16px` |  |
| `--ms-check-icon-size` | `12px` |  |
| `--ms-empty-padding` | `var(--space-md)` | `12px` |
| `--ms-empty-font-size` | `var(--text-xs)` | `13px` |

### Checkbox (multi-select option, "remember this device")

| Token | Value | Resolves to |
|---|---|---|
| `--checkbox-size` | `18px` |  |
| `--checkbox-border` | `var(--ink-400)` | `#616f7b` |
| `--checkbox-bg` | `var(--white)` | `#ffffff` |
| `--checkbox-bg-checked` | `var(--brand-600)` | `#023c6e` |
| `--checkbox-fg-checked` | `var(--white)` | `#ffffff` |
| `--checkbox-radius` | `var(--radius-sm)` | `4px` |

### Toggle switch

| Token | Value | Resolves to |
|---|---|---|
| `--toggle-w` | `42px` |  |
| `--toggle-h` | `24px` |  |
| `--toggle-knob` | `18px` |  |
| `--toggle-inset` | `3px` |  |
| `--toggle-travel` | `18px` |  |
| `--toggle-bg-off` | `var(--border-strong)` | `#c7ccd2` |
| `--toggle-bg-on` | `var(--em-green)` | `#4ba67b` |
| `--toggle-knob-bg` | `var(--white)` | `#ffffff` |
| `--toggle-ring-pressed` | `var(--pressed-ring)` | `0 0 0 3px color-mix(in srgb, #ffb020 55%, transparent)` |

### Sidebar navigation item

| Token | Value | Resolves to |
|---|---|---|
| `--nav-item-h` | `var(--control-h-xl)` | `44px` |
| `--nav-fg` | `var(--white-80)` | `rgb(255 255 255 / 80%)` |
| `--nav-fg-hover` | `var(--white)` | `#ffffff` |
| `--nav-bg-hover` | `var(--white-10)` | `rgb(255 255 255 / 10%)` |
| `--nav-bg-active` | `var(--brand-500)` | `#16537a` |
| `--nav-edge-active` | `var(--accent-500)` | `#16ad85` |
| `--nav-edge-width` | `3px` |  |
| `--nav-shadow-active` | `var(--shadow-md)` | `0 8px 24px rgb(2 60 110 / 14%)` |
| `--nav-bg-pressed` | `var(--white-15)` | `rgb(255 255 255 / 15%)` |
| `--nav-edge-pressed` | `var(--pressed-on-dark)` | `#ffb020` |

### Sidebar: collapsed rail, expanded panel, toggle button

| Token | Value | Resolves to |
|---|---|---|
| `--nav-w-collapsed` | `72px` |  |
| `--nav-w-expanded` | `248px` |  |
| `--nav-duration` | `200ms` |  |
| `--nav-icon-size` | `20px` <br><sub>every sidebar icon uses this slot, so icons stay pinned when collapsing</sub> |  |
| `--nav-rail-inset` | `14px` <br><sub>collapsed rail 72 - 2 x 14 = 44: buttons are squares, and the same width rule animates to expanded</sub> |  |
| `--nav-icon-inset` | `12px` |  |
| `--nav-logo-inset` | `16px` |  |
| `--nav-profile-inset` | `5px` |  |
| `--nav-logo-h` | `48px` <br><sub>the logo row is always this tall, collapsed or expanded, so nothing below it moves</sub> |  |
| `--nav-profile-h` | `44px` <br><sub>same for the profile row</sub> |  |
| `--nav-avatar-size` | `34px` |  |
| `--nav-avatar-ring-w` | `2px` |  |
| `--nav-avatar-ring-pressed` | `var(--pressed-on-dark)` | `#ffb020` |
| `--profile-btn-radius` | `var(--control-radius)` | `8px` |
| `--profile-btn-bg-hover` | `var(--white-10)` | `rgb(255 255 255 / 10%)` |
| `--profile-btn-bg-open` | `var(--white-10)` | `rgb(255 255 255 / 10%)` |
| `--profile-btn-bg-pressed` | `var(--white-15)` | `rgb(255 255 255 / 15%)` |
| `--profile-menu-w` | `224px` <br><sub>the sidebar's expanded width minus its side padding; the menu opens to the right of the rail when collapsed</sub> |  |
| `--nav-badge-collapsed-bg` | `var(--accent-500)` | `#16ad85` |
| `--nav-badge-collapsed-fg` | `var(--white)` | `#ffffff` |
| `--nav-badge-min-w` | `18px` |  |
| `--nav-badge-h` | `18px` |  |
| `--nav-toggle-icon-size` | `20px` |  |
| `--nav-toggle-h` | `var(--nav-item-h)` | `44px` |
| `--nav-toggle-bg` | `var(--accent-500)` | `#16ad85` |
| `--nav-toggle-fg` | `var(--brand-800)` | `#012646` |
| `--nav-toggle-bg-hover` | `var(--accent-100)` | `#c9eee1` |
| `--nav-toggle-fg-hover` | `var(--brand-800)` | `#012646` |
| `--nav-toggle-bg-pressed` | `var(--pressed-bg)` | `#fff4dc` |
| `--nav-toggle-fg-pressed` | `var(--pressed-fg)` | `#b45309` |

### Interactive surfaces: list rows, cards, menu items

| Token | Value | Resolves to |
|---|---|---|
| `--card-border-hover` | `var(--border-strong)` | `#c7ccd2` |
| `--card-shadow-hover` | `var(--shadow-md)` | `0 8px 24px rgb(2 60 110 / 14%)` |
| `--card-lift-hover` | `-2px` |  |
| `--menu-item-bg-hover` | `var(--surface-subtle)` | `#f8f8f8` |
| `--menu-item-fg-hover` | `var(--brand-600)` | `#023c6e` |

### Brand mark (the logo tile): a fixed-size square that never shrinks, stretches or reflows

| Token | Value | Resolves to |
|---|---|---|
| `--logo-mark-size` | `40px` |  |
| `--logo-mark-radius` | `var(--radius-lg)` | `12px` |
| `--logo-mark-bg` | `var(--accent-500)` | `#16ad85` |
| `--logo-mark-bg-on-dark` | `var(--white-15)` | `rgb(255 255 255 / 15%)` |
| `--logo-mark-fg` | `var(--white)` | `#ffffff` |

### Password eye (show/hide) button, inside the field

| Token | Value | Resolves to |
|---|---|---|
| `--pw-eye-size` | `var(--control-h-md)` | `36px` |
| `--pw-eye-icon-size` | `20px` |  |
| `--pw-eye-inset` | `var(--space-sm)` <br><sub>gap from the field's right edge</sub> | `8px` |
| `--pw-eye-radius` | `var(--control-radius)` | `8px` |
| `--pw-eye-fg` | `var(--ink-400)` | `#616f7b` |
| `--pw-eye-fg-hover` | `var(--ink-600)` | `#4c6173` |
| `--pw-eye-bg-hover` | `var(--bg)` | `#f2f2f2` |
| `--pw-eye-fg-pressed` | `var(--pressed-fg)` | `#b45309` |
| `--pw-eye-fg-disabled` | `var(--ink-300)` | `#b4bdc6` |
| `--pw-field-padding-right` | `calc(var(--pw-eye-size) + var(--pw-eye-inset) + var(--space-xs))` | `calc(36px + 8px + 4px)` |

### "Remember this device" row (the box uses --checkbox-*)

| Token | Value | Resolves to |
|---|---|---|
| `--remember-gap` | `var(--space-md)` | `12px` |
| `--remember-size` | `var(--text-base)` | `15px` |
| `--remember-weight` | `var(--weight-medium)` | `400` |
| `--remember-fg` | `var(--ink-500)` | `#5a6c7d` |

## App tokens (this app's screens only)
