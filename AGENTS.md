# Instructions for AI assistants using the EncoreMed design baseline

You were pointed at this directory because the user is building a product (web or native) that should look and feel like EncoreMed. This file tells you **what to read and in what order**. It does not contain the rules: they are in `policy/`, and you cite them by clause ID (for example "FND-9").

## 1. Read, in this order

1. **The rules:** `policy/README.md`, then all six policies:
   - `policy/UI-1-scope.md` (SCP): scope, levels (must, should, may), deviations, checking your work
   - `policy/UI-2-foundations.md` (FND): palette, status colours, typeface rules, scales
   - `policy/UI-3-states-accessibility.md` (ACC): the five control states, contrast, keyboard, touch
   - `policy/UI-4-components.md` (CMP): component anatomy and behaviour
   - `policy/UI-5-client-themes.md` (THM): client colour themes
   - `policy/UI-6-content.md` (CNT): wording, dates and times, numbers and units, translation, right-to-left text
2. **How to build:** `guides/IMPLEMENTATION.md`: setting up a project, the tokens, platform mapping, the web markup.
3. **The values:** `tokens/design-tokens.json` (or `tokens/DESIGN-TOKENS.md`). Never type a value from memory (SCP-3).
4. **Icons:** install or download Lucide from an official release at a pinned version (`guides/IMPLEMENTATION.md` section 4b). Never draw or retype an icon from memory (FND-12).

If a policy says it has moved to Jira (`policy/README.md` lists the ticket keys), read the live ticket. If you cannot reach Jira, use the copy here and tell the user it may be out of date.

**About `web/`:** `tokens.css` and `components.css` are the shared baseline: use them. The screens in `app.js` are only a reference: they show one way to meet the policies. Design the user's layouts as their product needs; any layout is fine as long as it complies with the policies (SCP-8). Never copy the demo's data or names.

## 2. Special cases

- **The user gives you colour codes or a logo, or asks to re-colour, re-brand or re-theme:** stop and follow `guides/THEMING.md` step by step. Do not edit colours by hand, and do not change `tokens.css` or `components.css`.
- **The user asks for something a Must clause forbids** (for example changing a status colour, THM-3): do not do it. Explain, citing the clause, and offer what is allowed.
- **Sources disagree:** follow SCP-7 and tell the user.
- **The work touches a topic in SCP-11** (decimal rounding, clickable column headers, validating a value on save, policy exceptions): an engineering (EE) policy covers it, and its rules are not copied into this package. Read the live EE ticket. If you cannot reach Jira, tell the user which ticket applies and do not guess what it says.

## 3. After every edit that changes a screen (SCP-12)

Treat this like running the tests: do it after **each** edit, not once at the end.
1. **Code check:** `python3 <this directory>/tools/guard.py <the user's project folder>`.
2. **Browser check** on the screens you touched: open each one, and each state you changed (a dialog, a sheet, an error state), in a real browser at phone, tablet and desktop width, and confirm what SCP-12 lists: nothing overflows or is cut off (FND-18), typing keeps the field and its focus (ACC-12), no script errors, no text under 13 (FND-7), tap areas of 44 x 44 on phones (ACC-9). Use the project's own tooling; for a native app, use a device or simulator.
3. **Fix every problem before your next edit.** Never edit a check to make it pass (SCP-10). Read every warning: fix it or explain it.
4. **If the user or a reviewer finds a defect the checks missed,** fix it, then tell the user which clause should forbid it and how a check could catch it (SCP-13).

## 4. Before you say you are done

Follow SCP-9:
1. **Check the work against the policies.** Go through `policy/` (and the EE policies in SCP-11) and check every clause that applies to what you built or changed, by any method you like. Fix every *Must* that is not met; for a *Should*, fix it or tell the user why. SCP-9 lists clauses that are easy to miss.
2. Both checks above (code and browser) pass, on every screen you built or changed.
3. Report: which policies you checked, what the checks found, any clause not met and why, and anything you added or changed beyond the baseline, with the clause IDs involved. If a check could not be done (for example no browser available), say so: that is not a pass.
