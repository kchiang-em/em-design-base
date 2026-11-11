# Instructions for AI assistants using the EncoreMed design baseline

You were pointed at this directory because the user is building a product (web or native) that should look and feel like EncoreMed. This file tells you **what to read and in what order**. It does not contain the rules: they are in `policy/`, and you cite them by clause ID (for example "FND-9").

## 1. Read, in this order

1. **The rules:** `policy/README.md`, then all six policies:
   - `policy/UI-1-scope.md` (SCP): scope, levels (must, should, may), deviations, checking your work
   - `policy/UI-2-foundations.md` (FND): palette, status colours, typeface, scales
   - `policy/UI-3-states-accessibility.md` (ACC): the five control states, contrast, keyboard, touch
   - `policy/UI-4-components.md` (CMP): component anatomy and behaviour
   - `policy/UI-5-client-themes.md` (THM): client colour themes
   - `policy/UI-6-content.md` (CNT): wording, dates and times, numbers and units, translation, right-to-left text
2. **How to build:** `guides/IMPLEMENTATION.md`: setting up a project, the tokens, platform mapping, the web markup.
3. **The values:** `tokens/design-tokens.json` (or `tokens/DESIGN-TOKENS.md`). Never type a value from memory (SCP-3).

If a policy says it has moved to Jira (`policy/README.md` lists the ticket keys), read the live ticket. If you cannot reach Jira, use the copy here and tell the user it may be out of date.

## 2. Special cases

- **The user gives you colour codes or a logo, or asks to re-colour, re-brand or re-theme:** stop and follow `guides/THEMING.md` step by step. Do not edit colours by hand, and do not change `tokens.css` or `components.css`.
- **The user asks for something a Must clause forbids** (for example changing a status colour, THM-3): do not do it. Explain, citing the clause, and offer what is allowed.
- **Sources disagree:** follow SCP-7 and tell the user.
- **The work touches a topic in SCP-11** (decimal rounding, clickable column headers, validating a value on save, policy exceptions): an engineering (EE) policy covers it, and its rules are not copied into this package. Read the live EE ticket. If you cannot reach Jira, tell the user which ticket applies and do not guess what it says.

## 3. Before you say you are done

Follow SCP-9:
1. Run `python3 <this directory>/tools/guard.py <the user's project folder>`. Each message names the clause it checks; `tools/README.md` explains them.
2. Fix every error. Never edit the guard to make it pass (SCP-10).
3. Read every warning and note: fix it, or explain it to the user.
4. Do the hand checks that SCP-9 lists.
5. Report: what you built, what the guard said, and anything you added or changed beyond the baseline, with the clause IDs involved.
