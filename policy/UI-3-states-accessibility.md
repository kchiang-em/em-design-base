# UI-3 Control states and accessibility

Draft key: UI-3 · Clause prefix: `ACC` · Version 1 (draft, 11 Nov 2026) · Owner: not yet named

## Purpose

Every control should respond the same way in every EncoreMed product, and every product should be usable by everyone, with any input method.

## Clauses

**ACC-1 Five control states.** *Must.* Every interactive control has five states: default, hover, pressed, disabled and keyboard focus (ACC-2 to ACC-5).

**ACC-2 Hover.** *Must.* On pointer devices only: a darker border or fill. Touch platforms have no hover; the other states still apply.

**ACC-3 Pressed is amber.** *Must.* The pressed state is amber: background `#FFF4DC`, text and icon `#B45309`, and a 3px amber ring (`#FFB020` at 55%). Amber is the complement of the logo navy and is used for the pressed state only.

**ACC-4 Disabled.** *Must.* 55% opacity, or the component's own disabled colours. A disabled control is not interactive.

**ACC-5 Keyboard focus.** *Must.* A 3px navy ring at 18% around the control, shown only for keyboard, switch or assistive focus. Pressed (amber) and focus (navy) are never mixed.

**ACC-6 Text contrast.** *Must.* Text has at least 4.5:1 contrast with its background (WCAG AA), including white text on brand colours and text in the pressed state. The soft grey text colour (3.5:1 on white) is for placeholders, helper text and icons only, never for important text.

**ACC-7 Not colour alone.** *Must.* Status is never conveyed by colour alone: status messages carry an icon and a text label.

**ACC-8 Operable without a pointer.** *Must.* Every control can be reached and operated without a pointer, has an accessible name, and shows a visible focus state.

**ACC-9 Touch targets.** *Must.* On touch platforms, touch targets are at least 44×44.

**ACC-10 Menus, dropdowns and dialogs.** *Must.* They close on an outside tap and on Escape (or the platform back action), and return focus to the control that opened them.
