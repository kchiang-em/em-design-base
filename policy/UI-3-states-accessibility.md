# UI-3 Control states and accessibility

Draft key: UI-3 · Clause prefix: `ACC` · Version 1 (draft, 11 Nov 2026) · Owner: Head of Product

## Purpose

Every control should respond the same way in every EncoreMed product, and every product should be usable by everyone, with any input method.

## Clauses

**ACC-1 Five control states.** *Must.* Every interactive control has five states: default, hover, pressed, disabled and keyboard focus (ACC-2 to ACC-5).

**ACC-2 Hover.** *Must.* On pointer devices only: a darker border or fill. Touch platforms have no hover; the other states still apply.

**ACC-3 Pressed is mint-teal.** *Must.* The pressed state uses the brand accent, so a tap or click reads as registered: background `#E8F7F2`, text and icon `#0B7258` (5.3:1), and a 3px ring of the soft brand green (`#4FAA91` at 55%); on dark surfaces, mint (`#9CD9BC`). A primary button keeps its navy and darkens, with the mint ring. A destructive (red) button darkens to the deeper red, never mint, so it is never read as success. The pressed state never uses the status green (FND-3).

**ACC-4 Disabled.** *Must.* 55% opacity, or the component's own disabled colours. A disabled control is not interactive.

**ACC-5 Keyboard focus.** *Must.* A double ring around the control: a 2px white inner ring and a 2px primary-navy outer ring. The navy ring shows on light surfaces and the white ring on dark ones, so the indicator reaches at least 3:1 on both. It is shown only for keyboard, switch or assistive focus, and no other style of a control (for example the active navigation item) may hide it. Pressed (mint-teal) and focus (navy) are never mixed.

**ACC-6 Contrast.** *Must.*
- **Text:** at least 4.5:1 against its background (WCAG AA). This includes placeholders, helper text, captions, subtitles, table headings, white text on brand colours, and text in the pressed state. Text in a disabled control is exempt.
- **Non-text:** the focus indicator (ACC-5), icons that carry meaning, status dots, and the borders that identify a control (text fields, dropdown triggers, checkboxes) have at least 3:1 against the surface they sit on (WCAG 1.4.11).

**ACC-7 Not colour alone.** *Must.* Status is never conveyed by colour alone: status messages carry an icon and a text label.

**ACC-8 Operable without a pointer.** *Must.* Every control can be reached and operated without a pointer, has an accessible name, and shows a visible focus state.

**ACC-9 Touch targets.** *Must.* On touch platforms, the tappable area of every control is at least 44×44. A control whose visible size is smaller (a 32 compact button, a 32×32 page button, an 18×18 checkbox) extends its tappable area to 44×44 without changing how it looks, and neighbouring tappable areas do not overlap.

**ACC-10 Menus, dropdowns and dialogs.** *Must.* They close on an outside tap and on Escape (or the platform back action), and return focus to the control that opened them.

**ACC-11 WCAG 2.2 Level AA.** *Must.* Every product meets WCAG 2.2 at Level AA. Native and desktop apps apply it as the W3C's guidance on applying WCAG to non-web software (WCAG2ICT) describes. The clauses in this policy are the baseline's way of meeting it; where WCAG asks for more, WCAG applies. Criteria that most often affect these products:
- text resizes to 200% and reflows at a width of 320 CSS pixels without loss of content (1.4.4, 1.4.10);
- status messages such as toasts and saved confirmations are announced to screen readers without taking focus (4.1.3);
- a focused control is never hidden behind a sticky header, footer or panel (2.4.11);
- anything done by dragging can also be done with single taps or clicks (2.5.7);
- sign-in allows pasting and password managers and never asks the user to solve a puzzle or remember a code (3.3.8);
- information the user already entered in a process is filled in or selectable, not asked for again (3.3.7);
- help (contact, support link) is in the same place on every screen that offers it (3.2.6);
- time limits can be turned off, adjusted or extended, and content that moves on its own can be paused (2.2.1, 2.2.2).

**ACC-12 Typing never rebuilds the field; nothing flashes.** *Must.* While the user types into a field, that field stays the same element: it keeps its focus, caret, text selection and focus ring, and the results, counts and lists around it update in place. When a tap, pick or toggle redraws part of the screen, nothing visibly flashes or re-opens: focus returns to the same control with its focus ring already shown, and an open dropdown panel or sheet stays open without replaying its opening animation.
