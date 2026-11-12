# UI-4 Component standards

Draft key: UI-4 · Clause prefix: `CMP` · Version 1 (draft, 11 Nov 2026) · Owner: Head of Product

## Purpose

Users move between EncoreMed products. The same component should have the same parts and behave the same way in each, so nothing has to be relearned.

## How to read this policy

- Each clause sets a component's **anatomy** (its parts), its **key sizes** and its **behaviour**. The level of a component clause is **Should** (SCP-2) unless a line says Must; sizes always come from the scales in UI-2, which are Must.
- Sizes are logical pixels: px on web, pt on iOS, dp on Android.
- Every interactive part follows the five control states (ACC-1) and the accessibility rules (UI-3).
- On native platforms, a platform control that does the same job may replace a component (SCP-6), keeping the anatomy and behaviour described here.
- The layout patterns (CMP-22 onwards) describe the design intent: what the pattern is for, the parts it needs and how it should feel. The arrangement, the exact parts and the wording are the product's choice. An example in a clause shows the intent; it is not a layout to copy.

## Clauses

**CMP-1 Buttons.** Radius 8, label 14 bold.
- *Primary:* height 48, side padding 20, navy fill, white label. Hover is a darker navy; disabled is a grey fill.
- *Secondary:* height 40, white fill, 1px light-blue border, slate label.
- *Outline (compact):* height 32, for rows and cards.
- *Icon button:* 36×36, outlined, icon only, with an accessible name (ACC-8). On touch platforms its tappable area is 44×44 (ACC-9).
- *Tinted arrow (list row action):* 36×36, light tint, chevron.
- *Danger:* solid red, height 44; an icon-only 44×44 variant; an outlined variant for delete. Every destructive action asks for confirmation first (CMP-21).
- *Back:* a compact outline button (height 32; a 44×44 tappable area on touch, ACC-9) with a back chevron and the destination in words ("Back to residents", "All roles"), at the top left of the content it leaves.
- *Text or link:* no container, navy bold label. Only for a link inside a sentence or a minor, optional action ("Need help?"). Every other button, including Back, has a visible box, so buttons look like buttons everywhere.

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

**CMP-9 List or table.** A white card (radius 12, 1px border). The header row has small uppercase bold grey titles with wide letter-spacing. Rows have a hover tint and the mint-teal pressed state (ACC-3), and an optional row action arrow (CMP-1). *Must:* column titles never touch; keep a gap of at least 12 to 16 between columns and give each column a minimum width. *Must:* the columns fit the table at every width that shows it (FND-18): the minimum column widths, the gaps and the row padding together never exceed the table's width. Where they would, hide lower-priority columns at that width, or switch to the card layout of FND-16; never let cells or rows run past the table. Clickable column headers follow EE-55, and decimal values in cells follow EE-52 (SCP-11).

**CMP-10 Pagination.** Shown above and below a paged list. Parts: "Showing 1–10 of 24", a "Rows per page" dropdown (5, 10, 20), and the buttons **First, Previous, up to five page numbers, Next, Last**.
- Buttons are 32×32 with a 4 gap; the current page is navy with a white number. On touch platforms each tappable area is 44×44 (ACC-9).
- At most five page numbers show, in a sliding window; First and Last jump to the ends.
- First and Previous are disabled on the first page; Next and Last on the last.
- On narrow screens, the four labelled buttons become icon-only, keeping their accessible names. On phones, pagination follows FND-16.

**CMP-11 Navigation (sidebar).**
- Two states: an icon **rail** (72 wide) and an expanded **panel** (248 wide), animated over about 200ms (FND-13). *Must:* how it opens depends on the input device:
  - **Mouse or trackpad:** it rests as the rail and opens as a panel *over* the page when the pointer rests on it (about 150ms) or keyboard focus moves into it, and closes about 300ms after the pointer leaves, when focus leaves, or on Escape (WCAG 1.4.13). The page content does not move. There is no toggle button.
  - **Touch screen:** the toggle button opens and closes it, never hover, and the page content moves over to make room. The choice is remembered.
  - **Both (a touch laptop):** hovering opens it as on a mouse, and the toggle button pins it open as on touch.
- *Must:* a long list of items scrolls on its own; the logo, the toggle button and the profile row stay in place, so they are always reachable.
- Items are 44 tall (44×44 squares when collapsed) with a 20 icon and a label. The active item is brand blue with a 3 green edge. An item may carry a count badge.
- Top: the logo tile (CMP-20). Above the profile row (touch screens only): the expand/collapse button, full width, green with dark navy text (a brand use of green, FND-3). Bottom (or in the app top bar instead, CMP-22): the profile row (a 34 avatar, the user's name and role) that opens an account menu, and a sign-out item.
- Rows keep the same height in both states, and icons stay in place, so nothing jumps.
- *Sections and groups:* related items may be grouped into sections, and an item may hold sub-pages that open in a submenu. The group shows as active while one of its pages is open. *Must:* a submenu behaves as a menu (ACC-10) and closes once an item is chosen.
- On native apps, the sidebar becomes the platform's navigation pattern (tab bar, navigation rail or drawer), keeping the item order, labels and active-state style. On phones, navigation follows FND-16.

**CMP-12 Page header and section heading.** A header bar (minimum height about 86) with the page title (26) and a one-line subtitle, and an optional status pill and icon button on the right. Section headings are 20 with a 14 subtitle.

**CMP-13 Status pill.** A pill with a 1px border, a 6 status dot (or a status icon) in the status colour (FND-2) and a text label (ACC-7).
- Labels are in sentence case (CNT-4), and the same state has the same label and look everywhere in a product.

**CMP-14 Banner.** A 36×36 tinted icon square, a bold title and one short line. The default banner is informational (information blue, FND-2); success, warning and error banners use the tint and icon colour of their status family.
- A note that warns about a consequence is a banner with its icon, not coloured text alone (ACC-7).
- *Must:* a screen that shows invented or test data (a demo, training or sample patient) says so clearly, in words, so it is never mistaken for real patient data.
- *Must:* a product that runs in more than one environment (production, staging, training) shows which one on every screen, in words, in a fixed place. A non-production environment is marked prominently (for example "Training: changes are not real"), so no one enters real work into it or mistakes it for the live system.

**CMP-15 Card.** White, 1px border, radius 12.

**CMP-16 Dialog (modal).** A centred card (maximum width 390; 430 for the wide variant) with a 48×48 icon, a title (20), a short explanation, an optional field, and two actions.
- *Default variant:* text centred; two equal-width buttons.
- *Wide variant:* text left-aligned; buttons right-aligned (cancel, then the primary action).
- *Must:* the background is dimmed, focus is trapped inside the dialog, and Escape cancels (ACC-10). On phones, a dialog is a full-width bottom sheet (FND-16).

**CMP-17 Toast.** A small card at the bottom right with a status-green check and one line, for confirmations only, never for errors or for anything the user must act on. It stays for at least 6 seconds and pauses while the pointer is over it or it has focus. It is announced to screen readers without taking focus (ACC-11). What it confirms must also be visible elsewhere (the saved item, an updated list), so missing the toast loses nothing.

**CMP-18 Loading, error and empty states.** *Must:* a list or page is never left blank without one of these.
- *Loading:* a spinner with the word "Loading…", in place of the content that is loading. When content already on screen is refreshed, it stays visible; the refresh is shown discreetly, not as a spinner over the content.
- *Error:* one line that says what failed, and a **Retry** button.
- *Empty:* a short message that says what is empty and, where it helps, why and what to do next, with the action that fills it when the user can take one. An icon and a title may be added.
- A detail pane with nothing selected (CMP-23) says what to do ("Select a role to see its permissions").

**CMP-19 Avatar.** A circle with the person's initials on a soft pastel tint. The tints are data colours, not brand colours.

**CMP-20 Logo tile.** The product logo sits in a 40×40 tile with radius 12 at the top of the navigation. *Must:* the logo never shrinks, stretches, reflows or is recoloured. A client logo follows THM-11.

**CMP-21 Confirming destructive actions.** *Must.* Every destructive action asks for confirmation before it happens: deleting, removing, unpairing, revoking, discarding unsaved changes, and anything else that loses data or a connection or cannot be undone in one step.
- The confirmation is a dialog (CMP-16, wide variant) with a red icon. Its title names the action and the thing it acts on ("Delete Scale 07?"). Its text says what will be lost, what is kept, and how to get it back if that is possible.
- Two buttons: **Cancel**, and a solid red button that repeats the action's verb ("Delete device"), never "OK" or "Yes".
- Focus starts on **Cancel**, so pressing Enter by accident does nothing harmful. Escape cancels and focus returns to the control that opened the dialog (ACC-10).
- After the action, a toast confirms it (CMP-17).

**CMP-22 App top bar.** An alternative home for the page title and the account, for products that need a global context. A product uses either the top bar or the sidebar account row (CMP-11), never both.
- Left: the page title (26) and an optional one-line subtitle. Right, in this order: page-level status and actions, the current context (for example the site, ward or gateway) as a chip, notifications if the product has them, and the account button (avatar, name, role, chevron) that opens the account menu with Sign out.
- *May (global bar variant):* a slimmer bar that holds only what is global: the breadcrumb (CMP-35) on the left; on the right, the global search (UX-4), the privacy switch (CMP-31), notifications (CMP-36), the quick action menu (UX-6) and the account. The page title then sits in the page header below it (CMP-12), with the page's own actions. A product uses one variant throughout.
- Global tools keep the same order and place on every screen (UX-3). The global search is the widest of them; the quick action is the only filled button in the bar.
- Minimum height 86, white, with a bottom border; the navigation rail stays on the left. *May:* a more compact bar for dense operational screens; a product uses one height throughout.
- *The context chip* shows where the user is working (hospital, ward, gateway); when the user can work in more than one place, it opens a switcher. A long name is shortened with an ellipsis, with the full name available (FND-18).
- *Should:* the page title appears once, not repeated as a heading in the content (FND-19).
- *Must:* on phones the page title stays visible, in short form if needed (FND-16). Secondary parts (subtitle, the name beside the avatar, the long context name) are hidden; the avatar opens the account menu as a sheet.

**CMP-23 List-detail layout.** For managing a set of items (roles, devices, templates): a list pane beside a detail pane.
- *List pane* (320 wide; 260 on tablets): an uppercase title with a count badge, a search field, and one row per item with an avatar or icon, the name, a secondary line (a code or status) and a chevron. The selected row has a brand tint, a brand border and a filled avatar, and is marked as current for assistive technology. A destructive row action (delete) is a separate button, never part of the row's own button, and confirms first (CMP-21).
- *Detail pane:* the item's name as the pane title (26), its code (CMP-25), an on-off switch with a visible label for its state, then tabs (CMP-24) or sections.
- Searching the list filters it in place (ACC-12).
- *Must:* on phones only one pane shows: the list first, then the detail with a Back link to the list (FND-16).

**CMP-24 Tabs.** For switching between views of one item.
- A row of tabs under the title, 48 high, label 14 bold, an optional icon and an optional count in a small pill. The selected tab is brand-coloured with a 3 underline; the others are grey and darken on hover.
- *Must:* exposed as a tab list with tabs and one tab panel; the selected tab is the only one in the tab order, the left and right arrow keys move between tabs, and Home and End jump to the first and last.
- *Must:* tabs never wrap onto a second row. When they do not fit (on a phone), the row scrolls sideways, the icons are hidden, and the selected tab is kept in view (FND-18).

**CMP-25 Chips and code labels.**
- *Chip:* a rounded label with an optional secondary part in smaller grey text ("Readings · View · Capture"); chips wrap within their area and never run past it. Chips can be grouped under an area heading, beside the chips on wide screens and above them on narrow ones. Chips show information; a chip that does something is a button and follows ACC-1.
- *Filter chip:* a chip that turns a filter on or off, with an optional count of matching items ("Lab 4"). It is a toggle button: its state is exposed as pressed or not, and the selected state is shown by more than colour (a check mark or a filled style with a border, ACC-7). Filter chips that can be combined say so ("Select one or more"). A quick filter ("Pending my actions", "All today") is a filter chip too. The counts follow UX-5.
- *Code label:* a code or identifier in the monospaced face (FND-5) on a light grey tint. *May:* a copy button beside identifiers people copy elsewhere.
- *May:* a small tag after a value that says where it came from ("Pump", "Manual"), so a reader can judge how far to trust it.
- *Must:* chip text, including the secondary part, is 13 or larger (FND-7).

**CMP-26 Stat card.** A card with a 48 x 48 tinted icon tile, a large number (26 bold, tabular figures), an optional "/ total" in smaller grey text, and a one-line label. A stat card that counts items opens them (UX-5). A stat that reports a problem uses the status tint of its meaning (FND-2), with a different icon for the good and the bad state (ACC-7). Stat cards sit in a row that wraps to fewer columns, and to one column on phones.
- *May:* a compact stat strip, several numbers side by side in one card, for the top of a list or a dashboard panel (CMP-33).
- *Should:* the same kind of number looks the same on every screen of a product. A number in a status colour also says what it means in words or with an icon (ACC-7).

**CMP-27 List toolbar.** The controls that act on a list are gathered in one place above it, so the user finds search, filters and the main action in the same spot on every list.
- The search comes first and is the widest control; the main action ("New patient") is set apart from the filters, for example at the far end.
- A short count of what the list shows ("229 patients") sits near the list and updates as the user searches or filters (ACC-12).
- On phones the toolbar follows FND-16: search stays, other filters move into a sheet.

**CMP-28 Segmented control.** A row of joined options for choosing one of a few related views, such as a period or a severity. The selected option is clearly filled. *Must:* it works with the keyboard and announces the selected option, like a radio group or tabs (ACC-8); a shortened label ("7D") has the full words as its accessible name.

**CMP-29 Live data.** A screen whose data changes while it is open, or comes from devices or other systems, tells the user how fresh it is.
- A short line near the data says whether it is live and when it last updated, and offers a way to refresh. When updates stop, it says so, with a warning icon.
- *Must:* the exact time is shown (CNT-2), not only a relative one ("0 s ago").
- A refresh keeps the current content on screen (CMP-18).
- Missing values from a device or system are shown as missing, never silently filled in.

**CMP-30 Attention list.** On an overview or health screen, problems that need someone to act are collected in one prominent list.
- Each item says what happened in plain words, what it affects, and since when; it offers the action that deals with it. Technical detail (codes, counts) is secondary, for support staff.
- The most severe and oldest items come first, and severity is shown by icon and word as well as colour (ACC-7).
- An empty list says that nothing needs attention, rather than disappearing.

**CMP-31 Sensitive data masking.** Where other people may see the screen, patient names and identifiers can be masked.
- Masked values stay distinguishable (for example by keeping initials or the last few characters), so the user can still find the right row.
- The user can reveal one value at a time, and switch masking for the whole screen; the switch says in words whether data is hidden or shown.
- *Must:* every reveal control has an accessible name that says what it reveals (ACC-8). Who may reveal, and whether reveals are recorded, follows the product's privacy requirements.

**CMP-32 Defined terms.** A label or metric that needs explaining is visibly marked and shows a short, plain definition. *Must:* the definition is reachable by hover, keyboard focus and touch, and can be dismissed (WCAG 1.4.13).

**CMP-33 Dashboard panel.** An overview screen is built from cards, one per area. Each has a title, the few numbers or items that matter most, a short status summary when something needs review, and a way into the full list. Panels reflow to one column on phones (FND-16). Filters that apply to several panels are set once, above them.

**CMP-34 Long forms.** A long form is split into titled sections, with related fields side by side on wide screens and stacked on phones.
- *May:* a summary of the key answers beside the form on wide screens.
- The form's actions are easy to find and in a predictable place; the main action is visually first in importance.
- One save action per form (FND-19). When one screen really saves several things separately, each part and its button make clear what is being saved.
- A value with a fixed set of choices is picked, not typed. Required and optional fields follow CMP-2.

**CMP-35 Breadcrumb.** For pages more than one level deep (UX-3): the path from the section to the current page ("LEC Eye Centre › Front office › Visit LEC-001801").
- Every part except the last is a link; the last is the current page, marked as current for assistive technology. The separator is decorative and hidden from assistive technology.
- It sits at the top left, in the top bar (CMP-22) or above the page title, in the same place on every screen.
- *Must:* on narrow screens it shortens from the start, keeping the parent and the current page, and never wraps onto a second row or runs past its container (FND-18). On phones it may be replaced by a Back button to the parent (CMP-1).

**CMP-36 Notifications.** For products that send people messages about their work.
- A bell button in the top bar (CMP-22) with an accessible name that includes the number of unread items ("Notifications, 3 unread"). The badge shows the count (up to "99+") and disappears at zero; its text is 13 or larger (FND-7).
- It opens a panel (a menu on desktop, a sheet on phones, ACC-10) with the newest first. Each item says what happened, to what, and when (CNT-2), and opens the object it is about (UX-5). Opening an item marks it read; "Mark all as read" is at the top.
- Notifications never interrupt (UX-10). Only a critical, time-bound event may also appear as a banner or dialog, and it is still listed here.

**CMP-37 Work queue by stage.** For work that moves through stages in order, such as a clinic visit (front office, triage, assessment, doctor, procedure, pharmacy, billing, completed).
- Stages appear in workflow order, each with the number of items in it and, where it matters, how long the oldest has waited. A stage opens its items (UX-5).
- Each item shows at least two identifiers (UX-4), its current stage and status, and how long it has been in that stage. Moving an item to the next stage is an action on the item (UX-6), and the item moves in place without the list being rebuilt (ACC-12).
- One screen shows the stage counts once (FND-19): as a stage list, as filter chips, or as stat cards, not all three.
