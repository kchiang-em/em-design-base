# UI-2 Visual foundations

Draft key: UI-2 · Clause prefix: `FND` · Version 1 (draft, 11 Nov 2026) · Owner: not yet named

## Purpose

The palette, typeface and scales are what make a product recognisably EncoreMed. This policy fixes them.

## Clauses

**FND-1 Official palette.** *Must.* The EncoreMed palette is the core and secondary colours of the official brand guideline (converted from CMYK to sRGB), combined with its colour-blind-safe set:

| Name | Hex | Used for |
|---|---|---|
| navy core | `#023C6E` | primary brand navy: sidebar, primary buttons, links |
| green core | `#16AD85` | primary brand green: live status dots, "captured" marks, active edge |
| blue | `#16537A` | secondary blue: active navigation item, gradient lift |
| green soft | `#4FAA91` | secondary mint-green: login status dot and rings |
| grey dark | `#3A3A3C` | body text |
| navy | `#0E4473` | headings |
| slate | `#4C6173` | secondary text and labels |
| green | `#4BA67B` | switch on, battery bars |
| mint | `#9CD9BC` | badge text on navy, light accents |
| grey light | `#F2F2F2` | page background |

Lighter and darker shades of these colours, used for hover, tinted backgrounds and dark surfaces, are derived from them. A client theme may replace the brand colours (UI-5); the status colours never change (FND-3).

**FND-2 System colours outside the guideline.** *Must.* Three colour families are not in the guideline and are fixed by this system: **red** for errors and destructive actions, **orange** for warnings, and **amber** for the pressed state only (ACC-3).

**FND-3 Status colours are universal.** *Must.* Red means error or destructive, orange means warning, green means positive or live. They mean the same in every product and are never re-themed (THM-3) or used as decoration.

**FND-4 Colour use.** *Must.*
- Green and mint are for fills, dots and icons, never for text (green core on white is only 2.9:1). Text on a green fill uses dark navy.
- *Should:* the sidebar uses the primary navy; the page background uses grey light; cards are white with a light border.

**FND-5 Typeface.** *Must.* Acumin Variable (Concept). Regular (400) and Bold (700) only. Where Acumin is not licensed or not installed, use Arial on web and the system font on native (SF Pro on Apple platforms, Roboto on Android, Segoe UI on Windows). Layouts must hold with the fallback font.

**FND-6 Typeface licensing.** *Must.* Acumin is an Adobe font; its licence controls who may use the font files and how.
- Never commit Acumin font files (`.otf`, `.ttf`, `.woff`, `.woff2`) to a repository, bundle them into an app, or download them from an unofficial site.
- On web, use Acumin only through a company-held web licence (for example an Adobe Fonts web kit).
- In native apps, embed Acumin only if the company confirms a licence that allows app embedding; a desktop or web licence usually does not.
- The owner of the company's Adobe font licence has not been named yet. Until then, ask your team lead or the brand or design team.

**FND-7 Type scale.** *Must.* Text sizes are 13, 14, 15, 16, 18, 20, 26 and 36. Page titles are 26; section headings 20; labels and buttons 14.

**FND-8 Spacing.** *Must.* Spacing follows a 4px grid: 2, 4, 8, 12, 16, 20, 24, 32, 48, 64.

**FND-9 Control size scale.** *Must.* Control heights are 32, 36, 40, 44 and 48. No other control height is used. Changing the scale needs the user's agreement first (SCP-5).

**FND-10 Radius scale.** *Must.* Radii are 4, 8 (controls), 12 (cards), 16, pill and circle.

**FND-11 Elevation.** *Must.* Three levels: small (`0 1px 2px`, black at 8%), medium (`0 8px 24px`, navy at 14%), large (`0 20px 48px`, dark navy at 26%). Native platforms map these to their own shadow or elevation at the same three levels.

**FND-12 Icons.** *Should.* Simple line icons on a 24px grid with a 1.8px stroke and round caps and joins, shown at 20px by default, coloured with the text colour of their context.

**FND-13 Motion.** *Should.* About 200ms for the sidebar and panels, about 150ms for state changes (hover, pressed), about 120ms for small indicators such as a dropdown chevron. Respect the platform's reduce-motion setting.

**FND-14 Layout target.** *Must.* The baseline is designed for tablet and larger (minimum width 768px on web). Phone layouts are not defined yet; derive them from the same components and tokens, and tell the user. Text that must not reflow (navigation labels, buttons) stays on one line.

**FND-15 Dark mode.** *May.* Dark mode is not defined. A product that needs it derives it from the same roles (text, surfaces, brand, status), keeps contrast at 4.5:1 (ACC-6), and tells the user.
