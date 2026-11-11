# UI policies: the rules for EncoreMed product interfaces

This folder holds the **rules**: what every EncoreMed product interface must, should or may do. It contains no code and no implementation detail, and it is written so that each file can become **one Jira policy ticket** without rewriting.

Everything else in this package (the guides, the tokens, the tools, the web reference) **implements** these rules and cites them by clause ID. Nothing outside this folder restates a rule; it points here.

## The policies

| File | Draft key | Title | Clause prefix | Jira key |
|---|---|---|---|---|
| [UI-1-scope.md](UI-1-scope.md) | UI-1 | Scope, strictness and deviations | `SCP` | not yet created |
| [UI-2-foundations.md](UI-2-foundations.md) | UI-2 | Visual foundations: colour, type, spacing, sizes, shape, icons, motion | `FND` | not yet created |
| [UI-3-states-accessibility.md](UI-3-states-accessibility.md) | UI-3 | Control states and accessibility | `ACC` | not yet created |
| [UI-4-components.md](UI-4-components.md) | UI-4 | Component standards | `CMP` | not yet created |
| [UI-5-client-themes.md](UI-5-client-themes.md) | UI-5 | Client colour themes | `THM` | not yet created |
| [UI-6-content.md](UI-6-content.md) | UI-6 | Content: wording, dates, numbers and languages | `CNT` | not yet created |

## How to cite a rule

Cite the **clause ID**, never pasted text: "FND-9", "THM-3". Clause prefixes are unique across the six policies, so a clause ID alone is enough. Once a policy is in Jira, the full citation is the ticket key plus the clause ID (for example "EE-70 THM-3"), the same form the engineering policies already use.

## Levels

Each clause carries a level. The levels are defined in SCP-2:

- **Must:** do not deviate.
- **Should:** follow unless the platform or the product's goal gives a reason not to; say what you did instead.
- **May:** allowed; tell the user what you added and why.

## Clause rules

- A clause ID is never reused or renumbered. A retired clause stays listed with the word "Retired" and the date.
- A change to a clause raises the policy's version line.
- Values that the rules fix (the palette, the scales) are stated in the clause. The design tokens implement them. If a token and a clause disagree, report it; the policy owner decides which one is corrected.

## Moving to Jira (for the dev lead)

1. Create one ticket per file: the ticket title is the policy title; the description is the file's content from "Purpose" down; keep the clause IDs exactly as written.
2. Fill in the "Jira key" column above.
3. Choose what happens to the files in this folder:
   - **Option A (recommended):** replace each file's body with the ticket link, the version line and a list of clause IDs with their one-line titles, so citations still resolve here. Tell AI assistants to read the live ticket (the developer's AI needs Jira access for this).
   - **Option B:** keep the files as a read-only snapshot for developers without Jira access, labelled with the ticket key and version it was copied from. A snapshot can go stale: whenever the ticket version rises, refresh it.
4. Nothing else needs to change: the guides, `AGENTS.md` and the tools cite clause IDs, which stay the same.

## Status

All six policies are drafts (version 1, 11 Nov 2026). **Owner: Head of Product.** Approval of changes and exceptions follows EE-1 (SCP-11). Anything about the interface that the engineering (EE) policies do not define is defined here.

## Decisions taken on 11 Nov 2026

All of these are written into the clauses listed.

| Decision | Where |
|---|---|
| The Head of Product owns the UI policies | every policy header |
| Topics the EE policies cover are not repeated; everything else about the interface is defined here | SCP-11 |
| Brand green and status green are separate; status uses the classic status green | FND-1, FND-2, FND-3 |
| Information blue is the brand guideline's secondary blue `#16537A`, not its navy `#0E4473` (the heading colour), so information messages do not look like headings | FND-2 |
| Borders that identify a control reach 3:1 | ACC-6 |
| Dates and times follow ISO 8601, extended and basic formats | CNT-1, CNT-2 |
| WCAG 2.2 Level AA | ACC-11 |
| Field errors: red border, red alert icon and dark red message below the field; validate on leaving the field or on submit; error summary when a form has more than three errors | CMP-2 |
| One red for errors, destructive actions and critical clinical results, told apart by icon and wording | FND-3 |
| Phone layouts: content gets more concise, not smaller; bottom tab bar with icon and short label; lists as cards; "Load more" instead of pages; dialogs as bottom sheets | FND-16 |
| Toasts stay at least 6 seconds, pause on hover or focus, and are announced to screen readers | CMP-17 |
| Icon set: Lucide at 1.8 stroke; platform system symbols allowed on native for standard actions | FND-12 |
| Wording: sentence case, verb-first buttons, plain error messages, one term per thing | CNT-4 |
| Translation and right-to-left text follow the W3C Internationalization best practices, BCP 47, Unicode CLDR and the Unicode Bidirectional Algorithm | CNT-5, CNT-6 |
| Units follow SI and ISO 80000-1 | CNT-3 |
| The engineering policies are authoritative; the UI policies follow their changes without a separate decision. Policy reviews happen when needed, with no fixed cadence | SCP-11 |
| Every destructive action asks for confirmation in a dialog that starts on Cancel | CMP-21 |
| A client's colours live in the project's own token file (`app-tokens`) as overrides of the brand tokens; there is no separate theme file | THM-1 |
| All chart colours (categories and scales) are chosen per project. The default set (the official palette and the colour-blind-safe set 02, plus three derived colours) is a starting point; any set must reach 3:1 against whatever is behind the chart (charts may be transparent), stay distinct for colour-blind readers and avoid the status colours | FND-17 |

## Open questions for the owner

| # | Question | Affects |
|---|---|---|
| 1 | **Conformance records.** EE-53 asks a repository that adopts engineering policies to keep a conformance table: each clause, how it is met, the evidence and the date, pinned to the policy version. Should each product that adopts the UI policies keep one too? Recommendation: not yet; the conformance checks (SCP-9) and the guard cover the automated part, and a table can be added if products start to diverge. | UI-1 |
