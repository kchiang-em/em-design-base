# UI-4 Component standards

Draft key: UI-4 · Clause prefix: `CMP` · Version 1 (draft, 11 Nov 2026) · Owner: Head of Product

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
- *Icon button:* 36×36, outlined, icon only, with an accessible name (ACC-8). On touch platforms its tappable area is 44×44 (ACC-9).
- *Tinted arrow (list row action):* 36×36, light tint, chevron.
- *Danger:* solid red, height 44; an icon-only 44×44 variant; an outlined variant for delete. Every destructive action asks for confirmation first (CMP-21).
- *Text or link:* no container, navy bold label.

**CMP-2 Text field.** Height 48 (44 when compact in a filter bar), radius 8, 1px border, side padding 16. The border darkens on hover; on focus the border turns brand blue and the focus ring shows (ACC-5). Disabled uses the page-grey fill. A label sits above the field. Validating a configurable value when it is saved follows EE-56 (SCP-11).
- *Invalid state:* the border turns red, and an error message appears directly below the field: a red alert icon and dark red text (FND-2) that say what is wrong and how to fix it ("Enter a date as YYYY-MM-DD, for example 2026-11-11"), never a code alone. The message is linked to the field as its description, and the field is marked invalid for assistive technology. The focus ring (ACC-5) still shows on an invalid field.
- *When to validate:* when the user leaves the field or submits, not on every keystroke. Keep what the user typed. On submit, move focus to the first invalid field; when a form has more than three errors, also show a short summary at the top that links to each field.
- *Helper text* (a format hint) sits between the label and the field, or below the field when there is no error, in secondary text that meets ACC-6.
- *Required fields:* mark the optional ones ("Optional") when most fields are required, or the required ones ("Required") when most are optional, in words, not by colour or an asterisk alone.

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

**CMP-9 List or table.** A white card (radius 12, 1px border). The header row has small uppercase bold grey titles with wide letter-spacing. Rows have a hover tint and the amber pressed state (ACC-3), and an optional row action arrow (CMP-1). *Must:* column titles never touch; keep a gap of at least 12 to 16 between columns and give each column a minimum width. Clickable column headers follow EE-55, and decimal values in cells follow EE-52 (SCP-11).

**CMP-10 Pagination.** Shown above and below a paged list. Parts: "Showing 1–10 of 24", a "Rows per page" dropdown (5, 10, 20), and the buttons **First, Previous, up to five page numbers, Next, Last**.
- Buttons are 32×32 with a 4 gap; the current page is navy with a white number. On touch platforms each tappable area is 44×44 (ACC-9).
- At most five page numbers show, in a sliding window; First and Last jump to the ends.
- First and Previous are disabled on the first page; Next and Last on the last.
- On narrow screens, the four labelled buttons become icon-only, keeping their accessible names. On phones, pagination follows FND-16.

**CMP-11 Navigation (sidebar).**
- Two states: an icon **rail** (72 wide) and an expanded **panel** (248 wide), animated over about 200ms (FND-13). *Must:* it changes only from its own toggle button, never on hover, so it works on touch screens.
- Items are 44 tall (44×44 squares when collapsed) with a 20 icon and a label. The active item is brand blue with a 3 green edge. An item may carry a count badge.
- Top: the logo tile (CMP-20). Above the profile row: the expand/collapse button, full width, green with dark navy text (a brand use of green, FND-3). Bottom: the profile row (a 34 avatar, the user's name and role) that opens an account menu, and a sign-out item.
- Rows keep the same height in both states, and icons stay in place, so nothing jumps.
- On native apps, the sidebar becomes the platform's navigation pattern (tab bar, navigation rail or drawer), keeping the item order, labels and active-state style. On phones, navigation follows FND-16.

**CMP-12 Page header and section heading.** A header bar (minimum height about 86) with the page title (26) and a one-line subtitle, and an optional status pill and icon button on the right. Section headings are 20 with a 14 subtitle.

**CMP-13 Status pill.** A pill with a 1px border, a 6 status dot in the status colour (FND-2) and a text label (ACC-7).

**CMP-14 Banner.** A 36×36 tinted icon square, a bold title and one short line. The default banner is informational (information blue, FND-2); success, warning and error banners use the tint and icon colour of their status family.

**CMP-15 Card.** White, 1px border, radius 12.

**CMP-16 Dialog (modal).** A centred card (maximum width 390; 430 for the wide variant) with a 48×48 icon, a title (20), a short explanation, an optional field, and two actions.
- *Default variant:* text centred; two equal-width buttons.
- *Wide variant:* text left-aligned; buttons right-aligned (cancel, then the primary action).
- *Must:* the background is dimmed, focus is trapped inside the dialog, and Escape cancels (ACC-10). On phones, a dialog is a full-width bottom sheet (FND-16).

**CMP-17 Toast.** A small card at the bottom right with a status-green check and one line, for confirmations only, never for errors or for anything the user must act on. It stays for at least 6 seconds and pauses while the pointer is over it or it has focus. It is announced to screen readers without taking focus (ACC-11). What it confirms must also be visible elsewhere (the saved item, an updated list), so missing the toast loses nothing.

**CMP-18 Loading, error and empty states.** *Must:* a list or page is never left blank without one of these.
- *Loading:* a 28 spinner with the word "Loading…".
- *Error:* one line that says what failed, and a **Retry** button.
- *Empty:* one centred sentence.

**CMP-19 Avatar.** A circle with the person's initials on a soft pastel tint. The tints are data colours, not brand colours.

**CMP-20 Logo tile.** The product logo sits in a 40×40 tile with radius 12 at the top of the navigation. *Must:* the logo never shrinks, stretches, reflows or is recoloured. A client logo follows THM-11.

**CMP-21 Confirming destructive actions.** *Must.* Every destructive action asks for confirmation before it happens: deleting, removing, unpairing, revoking, discarding unsaved changes, and anything else that loses data or a connection or cannot be undone in one step.
- The confirmation is a dialog (CMP-16, wide variant) with a red icon. Its title names the action and the thing it acts on ("Delete Scale 07?"). Its text says what will be lost, what is kept, and how to get it back if that is possible.
- Two buttons: **Cancel**, and a solid red button that repeats the action's verb ("Delete device"), never "OK" or "Yes".
- Focus starts on **Cancel**, so pressing Enter by accident does nothing harmful. Escape cancels and focus returns to the control that opened the dialog (ACC-10).
- After the action, a toast confirms it (CMP-17).
