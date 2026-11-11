# UI-1 Scope, strictness and deviations

Draft key: UI-1 · Clause prefix: `SCP` · Version 1 (draft, 11 Nov 2026) · Owner: not yet named

## Purpose

EncoreMed products should look and behave like one family, whatever platform they run on, while each product stays free to meet its own needs. This policy sets what the UI policies apply to, how strictly, and how a product may go beyond them.

## Clauses

**SCP-1 Scope.** *Must.* The UI policies (UI-1 to UI-5) apply to every EncoreMed product interface: web apps and native apps (iOS, Android, desktop). They are a baseline, not a framework: they fix what makes a product recognisably EncoreMed (colour, type, spacing, sizes, control states, how the main components behave) and leave the rest to the product and its platform.

**SCP-2 Levels.** *Must.* Every clause has a level:
- **Must:** do not deviate.
- **Should:** follow unless the platform or the product's goal gives a reason not to. When you do not follow it, say what you did instead and why.
- **May:** allowed. Tell the user what you added and why.

**SCP-3 Values come from the design tokens.** *Must.* Every colour, size, spacing, radius, type size, shadow and duration in a product comes from a design token. Do not type a value from memory or invent one. Keep the token names in the code so design and code stay traceable. Raw colour values appear only where the tokens themselves are defined and in a client theme file (THM-1).

**SCP-4 Extending the baseline.** *May.* A product may add components, use platform controls and navigation, add dark mode, and add a colour for a real need. When it does:
- keep the spirit of the baseline: the same palette family, sizes from the scales (UI-2), the five control states (ACC-1);
- add rather than rename or remove shared tokens and components;
- tell the user what was added or changed and why.

**SCP-5 Ask first.** *Must.* Ask the user before changing the control size scale (FND-9) or the typeface (FND-5), or before removing a baseline token or component.

**SCP-6 Native apps feel native.** *Should.* Native apps prefer the platform's own controls and navigation (pickers, sheets, navigation bars, back gestures) and restyle them with the tokens, keeping the baseline's look: palette, type, spacing, radii and states. Do not rebuild a native control only to copy the web version.

**SCP-7 When sources disagree.** *Must.* The UI policies decide the rules. The design tokens are the implemented values. The user's request decides what to build. When two of them disagree, do not silently follow whichever is easier: tell the user about the mismatch and what you chose.

**SCP-8 No demo content.** *Must.* Do not copy the reference implementation's demo data or names (Rossmax, residents, devices) into a product.

**SCP-9 Check before calling work done.** *Must.* Before work is reported as done:
1. run the conformance checks that the implementation provides, and fix every error;
2. read every warning and note, and either fix it or explain it to the user;
3. check by hand what a script cannot see: every value traces to a token (SCP-3); every interactive control has the five states (ACC-1); keyboard and assistive use works (ACC-8); contrast (ACC-6); touch targets (ACC-9); the screens at tablet width and at a large width, and the navigation in both of its states (CMP-11); components behave as UI-4 describes;
4. report what was built, what the checks said, and anything added or changed beyond the baseline.

**SCP-10 Never weaken a check.** *Must.* Do not edit, disable or bypass a conformance check to make it pass. Fix the work, or explain the deviation to the user.
