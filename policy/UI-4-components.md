# UI-4 Component standards

Draft key: UI-4 · Clause prefix: `CMP` · Version 1 (draft, 11 Nov 2026) · Owner: not yet named

## Purpose

Users move between EncoreMed products. The same component should have the same parts and behave the same way in each, so nothing has to be relearned.

## How to read this policy

- Each clause sets a component's **anatomy** (its parts), its **key sizes** and its **behaviour**. The level of a component clause is **Should** (SCP-2) unless a line says Must; sizes always come from the scales in UI-2, which are Must.
- Sizes are logical pixels: px on web, pt on iOS, dp on Android.
- Every interactive part follows the five control states (ACC-1) and the accessibility rules (UI-3).
- On native platforms, a platform control that does the same job may replace a component (SCP-6), keeping the anatomy and behaviour described here.

## Clauses

**CMP-1 Buttons.** Radius 8, label 14 bold.
- *Primary:* height 48, side padding 20, navy fill, white label. Hover is a darker navy; disabled is a grey fill.
- *Secondary:* height 40, white fill, 1px light-blue border, slate label.
- *Outline (compact):* height 32, for rows and cards.
- *Icon button:* 36×36, outlined, icon only, with an accessible name (ACC-8).
- *Tinted arrow (list row action):* 36×36, light tint, chevron.
- *Danger:* solid red, height 44; an icon-only 44×44 variant (for example "clear all filters"); an outlined variant for delete.
- *Text or link:* no container, navy bold label.

**CMP-2 Text field.** Height 48 (44 when compact in a filter bar), radius 8, 1px border, side padding 16. The border darkens on hover; on focus the border turns brand blue and the focus ring shows (ACC-5). Disabled uses the page-grey fill. A label sits above the field.

**CMP-3 Password field.** A text field (CMP-2) with a 36×36 show/hide button inside it, 8 from the right edge, with an accessible name that says what it does ("Show password").

**CMP-4 Search field.** A magnifier icon on the left; a 24 round clear (×) button on the right, shown only while there is text.

**CMP-5 Checkbox.** 18×18, radius 4, 1px grey border. Checked is a navy fill with a white check. The label is part of the touch target.

**CMP-6 Switch.** 42×24 with a round knob that travels 18. On is green.

**CMP-7 Dropdown (single select).**
- *Trigger:* shaped like a text field (height 44), or compact (height 32, for example "rows per page"), with a chevron that rotates when open and an optional prefix label ("Zone:").
- *Panel:* opens 4 below the trigger (above it near the bottom of the screen); lists options up to a height of about 200, then scrolls; marks the selected option with a check; may end with a short footer note.
- *Behaviour:* opens on tap, click or the down-arrow key; focus moves to the selected option; choosing an option closes the panel and returns focus to the trigger; Escape and an outside tap close it (ACC-10). On native apps, prefer the platform picker when it fits (SCP-6).

**CMP-8 Multi-select with search.** The dropdown's trigger and panel (CMP-7), plus:
- a search field (height 36) at the top of the panel, a checkbox before each option, and "No results found" when the search matches nothing;
- the trigger shows "All …" when nothing is selected and the selected names when something is; a clear (×) button appears when something is selected;
- the panel stays open while the user picks several options.

**CMP-9 List or table.** A white card (radius 12, 1px border). The header row has small uppercase bold grey titles with wide letter-spacing. Rows have a hover tint and the amber pressed state (ACC-3), and an optional row action arrow (CMP-1). *Must:* column titles never touch; keep a gap of at least 12 to 16 between columns and give each column a minimum width.

**CMP-10 Pagination.** Shown above and below a paged list. Parts: "Showing 1–10 of 24", a "Rows per page" dropdown (5, 10, 20), and the buttons **First, Previous, up to five page numbers, Next, Last**.
- Buttons are 32×32 with a 4 gap; the current page is navy with a white number.
- At most five page numbers show, in a sliding window; First and Last jump to the ends.
- First and Previous are disabled on the first page; Next and Last on the last.
- On narrow screens, the four labelled buttons become icon-only, keeping their accessible names.

**CMP-11 Navigation (sidebar).**
- Two states: an icon **rail** (72 wide) and an expanded **panel** (248 wide), animated over about 200ms (FND-13). *Must:* it changes only from its own toggle button, never on hover, so it works on touch screens.
- Items are 44 tall (44×44 squares when collapsed) with a 20 icon and a label. The active item is brand blue with a 3 green edge. An item may carry a count badge.
- Top: the logo tile (CMP-20). Above the profile row: the expand/collapse button, full width, green with dark navy text. Bottom: the profile row (a 34 avatar, name and role) that opens a staff menu, and a sign-out item.
- Rows keep the same height in both states, and icons stay in place, so nothing jumps.
- On native apps, the sidebar becomes the platform's navigation pattern (tab bar, navigation rail or drawer), keeping the item order, labels and active-state style.

**CMP-12 Page header and section heading.** A header bar (minimum height about 86) with the page title (26) and a one-line subtitle, and an optional status pill and icon button on the right. Section headings are 20 with a 14 subtitle.

**CMP-13 Status pill.** A pill with a 1px border, a 6 status dot in the status colour (FND-3) and a text label (ACC-7).

**CMP-14 Banner.** A 36×36 tinted icon square, a bold title and one short line.

**CMP-15 Card.** White, 1px border, radius 12.

**CMP-16 Dialog (modal).** A centred card (maximum width 390; 430 for the wide variant) with a 48×48 icon, a title (20), a short explanation, an optional field, and two actions.
- *Default variant:* text centred; two equal-width buttons.
- *Wide variant:* text left-aligned; buttons right-aligned (cancel, then the primary action).
- *Must:* the background is dimmed, focus is trapped inside the dialog, and Escape cancels (ACC-10).

**CMP-17 Toast.** A small card at the bottom right with a green check and one line, dismissed after about 2 seconds. For confirmations only, never for errors.

**CMP-18 Loading, error and empty states.** *Must:* a list or page is never left blank without one of these.
- *Loading:* a 28 spinner with the word "Loading…".
- *Error:* one line that says what failed, and a **Retry** button.
- *Empty:* one centred sentence.

**CMP-19 Avatar.** A circle with the person's initials on a soft pastel tint. The tints are data colours, not brand colours.

**CMP-20 Logo tile.** The product logo sits in a 40×40 tile with radius 12 at the top of the navigation. *Must:* the logo never shrinks, stretches, reflows or is recoloured. A client logo follows THM-11.
