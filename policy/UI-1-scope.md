# UI-1 Scope, strictness and deviations

Draft key: UI-1 · Clause prefix: `SCP` · Version 1 (draft, 11 Nov 2026) · Owner: Head of Product

## Purpose

EncoreMed products should look and behave like one family, whatever platform they run on, while each product stays free to meet its own needs. This policy sets what the UI policies apply to, how strictly, and how a product may go beyond them.

## Clauses

**SCP-1 Scope.** *Must.* The UI policies (UI-1 to UI-6) apply to every EncoreMed product interface: web apps and native apps (iOS, Android, desktop). They are a baseline, not a framework: they fix what makes a product recognisably EncoreMed (colour, type, spacing, sizes, control states, how the main components behave) and leave the rest to the product and its platform.

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

**SCP-8 No demo content.** *Must.* Do not copy the demo data, names or screens of a reference implementation into a product. Reference implementations show patterns, not content.

**SCP-9 Check before calling work done.** *Must.* Before work is reported as done:
1. run the conformance checks that the implementation provides, and fix every error;
2. read every warning and note, and either fix it or explain it to the user;
3. check by hand what a script cannot see: every value traces to a token (SCP-3); every interactive control has the five states (ACC-1); keyboard and assistive use works (ACC-8); contrast (ACC-6); touch targets (ACC-9); the screens at tablet width and at a large width, and the navigation in both of its states (CMP-11); components behave as UI-4 describes;
4. report what was built, what the checks said, and anything added or changed beyond the baseline.

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
