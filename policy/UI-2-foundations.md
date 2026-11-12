# UI-2 Visual foundations

Draft key: UI-2 · Clause prefix: `FND` · Version 1 (draft, 11 Nov 2026) · Owner: Head of Product

## Purpose

The palette, icons and scales are what make a product recognisably EncoreMed. This policy fixes them, and sets the rules a product's typeface must meet.

## Clauses

**FND-1 Official palette.** *Must.* The EncoreMed palette is these colour codes (sRGB). They derive from the official brand guideline, but the codes below are the reference: nothing depends on the guideline's files.

| Name | Hex | Used for |
|---|---|---|
| navy core | `#023C6E` | primary brand colour: primary buttons, links, selected states; its darker shade (`#012646`) is the navigation background |
| green core | `#16AD85` | brand green: the active navigation edge, the navigation toggle, the logo tile |
| blue | `#16537A` | secondary: active navigation item, gradient highlights; also the information status colour (FND-2) |
| green soft | `#4FAA91` | brand accent: decorative marks on brand surfaces (for example the sign-in panel) |
| grey dark | `#3A3A3C` | body text |
| navy | `#0E4473` | headings |
| slate | `#4C6173` | secondary text and labels |
| green | `#4BA67B` | brand "on" states: switch on, level indicators |
| mint | `#9CD9BC` | light accent on navy (for example badge text) |
| grey light | `#F2F2F2` | page background |

Lighter and darker shades of these colours, used for hover, tinted backgrounds and dark surfaces, are derived from them. The brand greens are brand colours, not status colours (FND-3). A client theme may replace the brand colours (UI-5).

**FND-2 Status and system colours.** *Must.* Five colour families carry a fixed meaning and are not part of the brand palette:

| Family | Meaning | Values |
|---|---|---|
| red | error, destructive action, critical result | `#DC2626` for borders, icons and fills; `#B91C1C` for text |
| amber | warning | `#F59E0B` for fills and the warning triangle; `#854D0E` for text, icon outlines and borders |
| status green | success, positive, connected or live | the classic status green: `#16A34A` for large fills, `#15803D` for dots, icons and text on white, `#166534` for text on a green tint |
| information blue | neutral information | `#16537A`, the brand guideline's secondary blue, with a light tint for backgrounds |

**FND-3 Status colours are universal.** *Must.* Red, amber, status green and information blue mean the same in every product and are never re-themed (THM-3).
- They follow the medical and safety conventions people already know: red for danger and critical (high-priority alarms in IEC 60601-1-8; danger in ISO 3864-1), amber-yellow for caution (medium-priority alarms; warning), green for a safe or successful state.
- Each status also has its own shape, so it is recognised without colour (ACC-7): danger and errors a circle or octagon with "!", warning a triangle (the ISO 3864 warning shape), success a circle with a check, information a circle with "i". The warning triangle is filled amber with a dark outline and glyph.
- Status colours stay distinguishable for the common kinds of colour blindness. Measured with CIEDE2000 under simulated protan, deutan and tritan vision, the main colours of danger, warning and success (`#DC2626`, `#F59E0B`, `#16A34A`) differ by at least 9; their dark text shades are told apart by the icon and words.
- They are never used for decoration.
- The brand green (FND-1) never stands for a status, and the status green is never used as a brand colour.
- Red marks anything that needs attention now: a system error, a destructive action, or a critical clinical result. These are told apart by their icon and wording, never by a second red (ACC-7). A clinical result says what it is ("Critical: potassium 6.8 mmol/L"); a system error says what failed and offers a way forward ("Couldn't save the reading. Retry").

**FND-4 Colour use.** *Must.*
- Brand green and mint are for fills, marks and icons, never for text.
- Status text uses the darker value of its family listed in FND-2, so it meets ACC-6.
- *Should:* the navigation uses a darker shade of the primary navy, so the navy buttons and the page stand apart from it; the page background uses grey light; cards are white with a light border.
- Actions (buttons, links, selected states) are navy, never green, so they are never mistaken for the status green that means success (FND-3). The brand greens and mint stay accents: the active navigation edge, the navigation toggle, the logo tile, switches that are on, and decorative marks.

**FND-5 Typeface.** The typeface is chosen per product. *Should:* use the default, **Public Sans** (open licence; a neo-grotesque close in feel to the brand guideline's Acumin), with Arial on web and the system font on native (SF Pro on Apple platforms, Roboto on Android, Segoe UI on Windows) as the fallback. *May:* use another face, for example Acumin where the company holds a suitable licence, or the face on the company website, and tell the user (SCP-4). *Must:* whatever face a product uses meets these rules:
- One sans-serif family for all interface text, in Regular (400) and Bold (700) only. *May:* a second, display face for large headings on brand surfaces (the sign-in panel, empty-state illustrations), never for body text, labels, controls or data.
- *May:* a monospaced face for codes and identifiers (role codes, serial numbers, tokens), at 13 or larger.
- Characters that are easily confused stay distinct: capital I, lower-case l and the digit 1; capital O and the digit 0. Staff IDs, serial numbers and clinical values depend on it.
- Numbers in tables, readings and anything compared in a column use tabular (equal-width) figures.
- The type scale (FND-7) and the layouts hold with the chosen face and with its fallback.
- The font's licence covers how the product uses it (FND-6).

**FND-6 Font licensing.** *Must.*
- Prefer fonts under an open licence (such as the SIL Open Font License), which may be bundled into apps and committed to repositories. The default, Public Sans, is one; keep its licence file with the font files.
- A commercially licensed font (Acumin is an Adobe font) is used only as its licence allows: never commit its files (`.otf`, `.ttf`, `.woff`, `.woff2`) to a repository, bundle them into an app, or download them from an unofficial site, unless the company confirms a licence that allows it. A desktop or web licence usually does not allow app embedding.

**FND-7 Type scale.** *Must.* Text sizes are 13, 14, 15, 16, 18, 20, 26 and 36. Page titles are 26; section headings 20; labels and buttons 14. Nothing smaller than 13, including the small text that is easiest to forget: badges, counts, captions, tags and tab bar labels. Where 13 does not fit, shorten the text or give it more room.

**FND-8 Spacing.** *Must.* Spacing follows a 4px grid: 2, 4, 8, 12, 16, 20, 24, 32, 48, 64.

**FND-9 Control size scale.** *Must.* Control heights are 32, 36, 40, 44 and 48. No other control height is used. Changing the scale needs the user's agreement first (SCP-5).

**FND-10 Radius scale.** *Must.* Radii are 4, 8 (controls), 12 (cards), 16, pill and circle.

**FND-11 Elevation.** *Must.* Three levels: small (`0 1px 2px`, black at 8%), medium (`0 8px 24px`, navy at 14%), large (`0 20px 48px`, dark navy at 26%). Native platforms map these to their own shadow or elevation at the same three levels.

**FND-12 Icons.** *Must.*
- The icon set is **Lucide** (open source, ISC licence), drawn on a 24px grid with a 1.8px stroke (Lucide's default is 2; set it to 1.8) and round caps and joins, shown at 20px by default and coloured with the text colour of their context.
- **Icons come from an official Lucide release, never from memory.** Use Lucide's published packages or files at a pinned version (see https://lucide.dev), and choose icons by their Lucide name. Do not redraw, retype or approximate an icon's shape from memory, and do not hand-edit an icon's drawing; size, stroke width and colour are set through the package's options or the surrounding style.
- An icon Lucide does not have is first looked for under another Lucide name. Only if there is none, a custom icon is drawn in the same style (24 grid, round caps and joins), kept in the project's own icon folder, and named to the user (SCP-4).
- *May:* native apps use the platform's system symbols (SF Symbols on Apple platforms, Material Symbols on Android) for standard system actions such as share or back. Do not mix two icon sets within one component or toolbar.
- An icon that carries meaning has a text label or an accessible name (ACC-8). Icon-only buttons are kept to actions everyone recognises (close, back, search, more). An icon-only navigation rail is allowed only because it opens with its labels (CMP-11); each rail icon also has an accessible name and a tooltip.

**FND-13 Motion.** *Should.* About 200ms for the sidebar and panels, about 150ms for state changes (hover, pressed), about 120ms for small indicators such as a dropdown chevron. Respect the platform's reduce-motion setting.

**FND-14 Layout targets.** *Must.* Tablet and larger (768px wide and up) use the layouts in UI-4 as designed. Phones (narrower than 768px) follow FND-16. Text that must not reflow (navigation labels, buttons) stays on one line.

**FND-15 Dark mode.** *May.* Dark mode is not defined. A product that needs it derives it from the same roles (text, surfaces, brand, status), keeps contrast at ACC-6, and tells the user.

**FND-16 Phone layouts.** *Must.* On phones, content gets more concise, not smaller:
- **Text keeps its size.** Body text stays at 16 (and text fields at 16 or more on web, so the browser does not zoom in when they gain focus); nothing is smaller than 13 (FND-7). Labels may be shortened; they are not shrunk.
- **One column.** Side-by-side panels stack; filters move into a sheet or a full-screen panel opened from a filter button.
- **Page title:** every screen keeps its title, in short form if needed (CMP-22).
- **Navigation:** a bottom tab bar with up to five destinations, each an icon with a short text label (13 or larger); further destinations go under "More". The last tab is the account (the user's avatar and "Account"): it opens a sheet with the account menu and Sign out, and it is the current tab on screens reached from it. The side navigation (CMP-11) is not used on phones.
- **Lists and tables** become stacked rows or cards that show the two or three most important fields, with the rest one tap away; column titles are hidden. Pagination (CMP-10) becomes a "Load more" button below the list with the "Showing 1–20 of 24" count.
- **Filters:** the search field stays on screen; other filters move into a Filters sheet (CMP-27), as plain lists of radio buttons and checkboxes rather than dropdowns. The Filters button shows how many filters are on, and the sheet's main button says how many results they give ("Show 10 residents").
- **Dialogs** become bottom sheets at full width (CMP-16 behaviour still applies).
- **The main action** of a screen stays reachable at the bottom of the screen.
- Touch targets stay at least 44×44 (ACC-9). Icon-only controls follow FND-12.
- **Safe area:** content and controls stay inside the device's safe area, clear of the status bar, the notch or camera cut-out, the home indicator and rounded corners, in portrait and landscape. Backgrounds (the page header, the tab bar, sheets) may extend under them to the screen edge.

**FND-17 Chart colours.** The chart colours are chosen per project. *Should:* start from this default set, used in this order for categories (series, segments). The set starts from the brand navy and was chosen by measurement: every colour reaches 3:1, none looks like a status colour, and they stay apart for colour-blind readers (the rules below):

| Order | Colour | Hex | On white |
|---|---|---|---|
| 1 | navy core | `#023C6E` | 11.2:1 |
| 2 | royal blue | `#1D1DCD` | 9.9:1 |
| 3 | dark teal | `#256D73` | 6.0:1 |
| 4 | plum | `#A6678C` | 4.3:1 |
| 5 | purple | `#7541AA` | 6.8:1 |
| 6 | teal (darkened) | `#5B92A7` | 3.4:1 |
| 7 | violet | `#8567CC` | 4.4:1 |
| "Other", totals, reference lines | neutral grey | `#737373` | 4.7:1 |

*May:* a project replaces, reorders or adds chart colours to suit its data. *Must:* whatever set a project uses meets these rules:
- A chart may sit on any surface, including a transparent background over the page. Every chart colour reaches 3:1 against what is actually behind it: the card, the page background or a dark panel (ACC-6). The default set is measured on white and also reaches 3:1 on the grey page background. No two default colours are closer than ΔE 7.9 (CIEDE2000) under simulated protan, deutan or tritan vision, and none is close to a status colour.
- The colours stay distinct from each other for the common kinds of colour blindness. Use at most seven categories; group the rest into "Other" in a neutral grey.
- Never rely on colour alone: label series directly, or use a legend together with different markers or line styles (ACC-7).
- Status colours (FND-2), and colours that look like them, appear in a chart only with their status meaning, for example a threshold band or an out-of-range marker, never as a series colour.
- Scales (a value from low to high, or diverging from a midpoint) also use colours chosen per project. *Should:* start from the shades of the primary navy, light to dark. *Must:* the steps are visibly ordered from light to dark and the darkest steps reach 3:1 against what is behind the chart.
- A project that changes the chart colours sets them in its own token file (or theme), keeps the token names `chart-1` to `chart-7` and `chart-other`, sets `chart-surface` to the colour behind its charts, and tells the user what it chose (SCP-4).

**FND-18 Content stays inside its container.** *Must.* At every supported width (phones from 320, tablets from 768, desktops), and with the navigation in each of its states:
- the width that counts is the width left for the content, not the screen's: on a touch screen the navigation opened with its toggle pushes the content over (CMP-11), so a 820-wide tablet with the panel open leaves the content about 570; layouts hold at that width too;
- no element extends beyond its card, table, row, panel or screen, and nothing is cut off by its container;
- the screen never scrolls sideways (WCAG 1.4.10);
- text that does not fit wraps; where it must stay on one line (FND-14) it ends with an ellipsis, and the full text is available (for example in a details view or the accessible name);
- a box may scroll sideways only when that is its purpose (a wide data grid the user pans, or a tab strip on a narrow screen, CMP-24); a list or table never needs to (CMP-9).

**FND-19 Avoid redundancy.** *Should.* Something is redundant when the same screen shows it twice, so the user has to work out whether the two are the same. By default, each of these appears **once per screen**:
- **An action.** One control for each action. Not two "Save" buttons for the same form; not a "View all" link next to a button that opens the same list; not the same command in a toolbar and again in a menu on that screen.
- **A title.** The page title appears once. It is not repeated as a heading in the content (CMP-22); a heading in the content names a part of the page, not the page.
- **A piece of information.** A count, a status, a date or a name appears in one place. Not the same total in a stat card and again in the list header; not the same status as a pill and again as a sentence beside it.
- **A route.** One way to reach a page from the same screen. Not a menu button and a tab bar that open the same navigation.

Repeating one of these is allowed only when the second copy saves the user real effort, for example pagination above and below a long list (CMP-10), or a main action that stays in view while a long form scrolls. When something is repeated on purpose, tell the user what and why (SCP-4).

Two controls that look alike but do different things are not redundant, but each must say what it does: when one screen has two forms that save separately, their buttons name what they save ("Save details", "Save password"), never "Save" twice.
