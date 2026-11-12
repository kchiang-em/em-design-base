# UI-1 Scope, strictness and deviations

Draft key: UI-1 · Clause prefix: `SCP` · Version 1 (draft, 11 Nov 2026) · Owner: Head of Product

## Purpose

EncoreMed products should look and behave like one family, whatever platform they run on, while each product stays free to meet its own needs. This policy sets what the UI policies apply to, how strictly, and how a product may go beyond them.

## Clauses

**SCP-1 Scope.** *Must.* The UI policies (UI-1 to UI-7) apply to every EncoreMed product interface: web apps and native apps (iOS, Android, desktop). They are a baseline, not a framework: they fix what makes a product recognisably EncoreMed (colour, type, spacing, sizes, control states, how the main components behave) and leave the rest to the product and its platform.

**SCP-2 Levels.** *Must.* Every clause has a level:
- **Must:** do not deviate.
- **Should:** follow unless the platform or the product's goal gives a reason not to. When you do not follow it, say what you did instead and why.
- **May:** allowed. Tell the user what you added and why.

**SCP-3 Values come from the design tokens.** *Must.* Every colour, size, spacing, radius, type size, shadow and duration in a product comes from a design token. Do not type a value from memory or invent one. Keep the token names in the code so design and code stay traceable. Raw colour values appear only where tokens are defined: the shared token file and the project's own token file, which also holds a client's colours (THM-1). Stylesheet rules and component code use tokens.

**SCP-4 Extending the baseline.** *May.* A product may add components, use platform controls and navigation, add dark mode, and add a colour for a real need. When it does:
- keep the spirit of the baseline: the same palette family, sizes from the scales (UI-2), the five control states (ACC-1);
- add rather than rename or remove shared tokens and components;
- tell the user what was added or changed and why.

**SCP-5 Ask first.** *Must.* Ask the user before changing the control size scale (FND-9) or the type scale (FND-7), or before removing a baseline token or component.

**SCP-6 Native apps feel native.** *Should.* Native apps prefer the platform's own controls and navigation (pickers, sheets, navigation bars, back gestures) and restyle them with the tokens, keeping the baseline's look: palette, type, spacing, radii and states. Do not rebuild a native control only to copy the web version.

**SCP-7 When sources disagree.** *Must.* The UI policies decide the rules. The design tokens are the implemented values. The user's request decides what to build. When two of them disagree, do not silently follow whichever is easier: tell the user about the mismatch and what you chose.

**SCP-8 The reference is an example, not a template.** The reference implementation (the screens and behaviour in `web/`) shows one way to meet the policies. It is a source to learn from, not a layout to reproduce.
- *May:* design a product's own layouts, screens and flows as its users and content need, as long as the result complies with the policies. A layout that differs from the reference is not a deviation; a layout that breaks a clause is.
- *Must:* the shared values and component styles (the design tokens and `components.css`, or their native equivalents) are still used (SCP-3). Only the arrangement is free; the look comes from the baseline.
- *Must:* do not copy the demo data, names or screens of a reference implementation into a product. Reference implementations show patterns, not content.

**SCP-9 Check the work against the policies before calling it done.** *Must.* Before work is reported as done:
1. go through the policies (UI-1 to UI-7, and the engineering policies listed in SCP-11) and check the work against **every clause that applies** to the screens and components that were built or changed, by any method (reading the screens, the code or their text, or a script of one's own). A clause applies when the work contains what it governs: a table edit brings in the table, text, colour, content and accessibility clauses, not the sign-in or theming ones;
2. fix anything that does not meet a *Must*; for a *Should* that is not met, fix it or tell the user why;
3. run the code check that the implementation provides and the browser check (SCP-12) as part of this, and fix every error; read every warning and note, and fix it or explain it;
4. report which policies were checked, what the checks found, any clause not met and why, and anything added or changed beyond the baseline.

Clauses that are easy to miss (examples, not the scope): dates and times in the ISO default or the user's chosen setting (CNT-1, CNT-2); singular and plural forms, never "(s)" (CNT-4); redundancy (FND-19); text under 13 (FND-7); a field rebuilt or a focus ring flashing while typing (ACC-12); content running past its container (FND-18); every value from a token (SCP-3); the five control states (ACC-1); keyboard use (ACC-8); contrast (ACC-6); confirmation before a destructive action (CMP-21); icons taken from an official Lucide release, not drawn from memory (FND-12); every stat, count, badge and banner opens the items it refers to (UX-5); Back returns to the same place with its filters kept (UX-3); two patient identifiers wherever a patient is acted on (UX-4); key tasks within their step budget (UX-2).

**SCP-10 Never weaken a check.** *Must.* Do not edit, disable or bypass a conformance check to make it pass. Fix the work, or explain the deviation to the user.

**SCP-11 Engineering policies are not repeated here.** *Must.* Where an engineering policy (project EE, label `ee-policy`) covers a topic, that policy applies and the UI policies do not restate it. Read the live ticket. Everything about the interface that the engineering policies do not define is defined in the UI policies. The engineering policies that cover interface topics include:

| Topic | Policy |
|---|---|
| Who approves policy changes and exceptions | EE-1 |
| Rounding of decimal values | EE-52 |
| Linking, no redundant policies, conformance records | EE-53 |
| Clickable column headers | EE-55 |
| Validating a configurable display value when it is saved | EE-56 |

The engineering policies are authoritative. When one changes, the UI policies follow it without a separate decision; if a UI clause and an engineering policy ever disagree, the engineering policy wins and the UI clause is corrected.

**SCP-12 Browser check after every edit.** *Must.* After every edit that changes what a screen shows or how it behaves, and before reporting it, run the screens the edit touched in a real browser (or on a device or simulator for native apps) at phone, tablet and desktop width, with the navigation both collapsed and expanded (on a touch tablet, opened with its toggle so it pushes the content over, CMP-11), and confirm that:
- nothing extends beyond its container, is cut off, or makes the screen scroll sideways (FND-18);
- typing into each field keeps that field, its focus and its caret (ACC-12);
- there are no script errors and every file the screen needs loads;
- text is 13 or larger (FND-7) and, at phone width, every control's tap area is at least 44 x 44 (ACC-9).
Use whatever tooling suits the project (a browser's device mode, an automated browser test, a device or simulator). Fix every error before moving on: a defect found later costs more than one found now.

**SCP-13 Every defect becomes a rule and a check.** *Must.* When a defect is found in review or testing that the rules and checks did not catch, add or sharpen a clause that forbids it and extend the checks to detect it, so it cannot come back unnoticed. Changes to the clauses follow EE-1 (SCP-11).
