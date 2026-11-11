# UI-6 Content: wording, dates, numbers and languages

Draft key: UI-6 · Clause prefix: `CNT` · Version 1 (draft, 11 Nov 2026) · Owner: Head of Product

## Purpose

People read EncoreMed products quickly, often under pressure, and sometimes in another language. The same thing should be written the same way everywhere, and a date or a value should never be open to two readings.

## Clauses

**CNT-1 Dates.** *Must.* Dates follow ISO 8601 by default.
- **Extended format** wherever people read a date: `2026-11-11`.
- **Basic format** only where separators cannot be used, such as file names and compact identifiers: `20261111`.
- Months and days always have two digits, and years four.
- *May:* a user or app setting offers **day-month-year** for display: `11-11-2026` (DD-MM-YYYY, with hyphens). *Must:* ISO is the default until someone changes the setting; the setting changes only how dates are shown on screen, and every date on every screen follows it; data exchange, files, exports and logs always stay ISO. No other format is offered: never slashes or month-first forms (`11/12/2026`), which read differently from country to country.

**CNT-2 Times.** *Must.* Times follow ISO 8601 and the 24-hour clock by default.
- *May:* a user or app setting offers the **12-hour clock** for display: `2:30 PM`, always with AM or PM. As with dates (CNT-1), the 24-hour clock is the default, the setting changes only what is shown on screen, and data exchange, files, exports and logs keep the 24-hour ISO form.
- **Extended format** on screen (with the default setting): `14:30`, with seconds only when they matter (`14:30:05`). **Basic format** (`143005`) only in compact identifiers.
- **Date and time together:** in data exchange, files and logs, the full form with a time-zone offset: `2026-11-11T14:30:00+08:00` (basic: `20261111T143000+0800`). On screen, date and time may be separated by a space for readability: `2026-11-11 14:30`.
- Show the time zone or offset when the people reading a time may be in different time zones.
- *May:* relative times ("2 min ago") for events in the last 24 hours, always shown together with the exact time: "2 min ago · 15:08", with the date added when it is not today ("3 h ago · 2026-11-10 23:50"). The exact time is visible, not only on hover: hover does not exist on touch screens or for keyboard users.

**CNT-3 Numbers and units.** *Must.* Rounding of decimal values follows EE-52 (SCP-11). Units follow the SI and ISO 80000-1 conventions: a space between the number and the unit symbol (`120 mmHg`, `36.8 °C`, `72 kg`), and the unit's official symbol, never an invented abbreviation.

**CNT-4 Wording.** *Should.*
- Sentence case for titles, labels, buttons, menu items, tabs and status labels ("Pair a new device", not "Pair A New Device"). Capitals are for codes and abbreviations ("ICU"); uppercase styling of a short heading (CMP-9) is a visual style, not wording.
- Counts agree with their number: "1 ward", "4 wards", "8 actions required". Avoid mixed forms that are neither singular nor plural, such as "ward(s)" or "8 action required".
- Buttons start with a verb that says what happens ("Save readings", "Unpair"), not "OK" or "Submit".
- Error messages say what happened and what to do next, in plain words, without blaming the user and never as a code alone (CMP-2, FND-3).
- One term per thing: once a product calls someone a "patient", it never calls them a "client" or a "user" elsewhere.
- Short: one idea per sentence, no jargon or internal names.

**CNT-5 Translation.** *Must* for a product that ships in more than one language; *Should* for every other product, so it can be translated later. It follows the W3C Internationalization best practices:
- All text people see lives outside the code, in a string file per language; text is never built by joining fragments ("Showing " + n + " of " + m), because word order changes between languages.
- Layouts hold when text grows: allow at least 40% more length for sentences and up to 100% more for short labels; no text inside images.
- Each screen declares its language, and any passage in another language declares its own, using BCP 47 language tags (WCAG 3.1.1, 3.1.2).
- Numbers and units follow the language's conventions from the Unicode CLDR, except dates and times, which always follow CNT-1 and CNT-2.
- Text with a count uses the language's plural forms from the Unicode CLDR plural rules (one string per form, for example ICU MessageFormat), never "(s)".

**CNT-6 Right-to-left languages.** *Must* for a product that ships in a right-to-left language (Arabic, Hebrew, Persian, Urdu). It follows the Unicode Bidirectional Algorithm (UAX #9) and the W3C guidance on right-to-left text:
- The layout mirrors: navigation, alignment, the order of buttons and the direction of progress all flip. Build layouts with start and end, never left and right, so mirroring is automatic.
- Icons that show direction mirror (back and forward arrows, chevrons, the sidebar toggle); icons that do not (check, search, clock, media playback, logos) stay as they are.
- Numbers, ISO dates and times, codes, serial numbers and units stay left to right inside right-to-left text, isolated so they do not reorder.
- Test every screen with a right-to-left language before release.
