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

## How to cite a rule

Cite the **clause ID**, never pasted text: "FND-9", "THM-3". Clause prefixes are unique across the five policies, so a clause ID alone is enough. Once a policy is in Jira, the full citation is the ticket key plus the clause ID (for example "EE-70 THM-3"), the same form the engineering policies already use.

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

All five policies are drafts (version 1, 11 Nov 2026). No policy owner has been named yet.
