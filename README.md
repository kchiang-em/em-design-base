# EncoreMed design baseline

A small, platform-neutral design baseline for EncoreMed products: the rules, values and reference code that make a product look and feel like EncoreMed, for web and native apps. It is written so an **AI coding assistant** can read it and prototype within the design.

It is a baseline, not a framework. Extend it when your product needs more; the checker reports differences and clear mistakes, and does not block you.

## How it is organised

The package separates **rules** from **implementation**:

| Folder | Holds | Changes when |
|---|---|---|
| `policy/` | **the rules**: six policies (UI-1 to UI-6) with numbered clauses such as FND-9 or THM-3. No code. Each file is written to become one Jira policy ticket. | the policy owner changes a rule |
| `guides/` | **how to build**: the implementation guide and the client theming procedure. They cite clause IDs and do not restate the rules. | the way of implementing changes |
| `tokens/` | **the values**: `design-tokens.json` (every value, for any platform) and a readable copy. A product keeps its own tokens, including a client's colours, in its own `app-tokens.css` or `app-tokens.json` | a value changes |
| `tools/` | **the scripts**: the conformance checker (`guard.py`) and the theme helpers. Their messages cite clause IDs. | a check or helper changes |
| `web/` | **the web reference implementation**: CSS and the JS behaviour patterns | the web reference changes |

`AGENTS.md` tells an AI assistant what to read, in what order.

## Quick start

1. **Give your AI assistant this directory** and start with:

   > Use the EncoreMed design baseline in `<path to this directory>`. Read `AGENTS.md` and follow it. We are building `<what, and on which platform>`. When you finish, run the guard as `AGENTS.md` describes and report what it says.

2. **Web product:** copy `web/tokens.css` and `web/components.css` into your project and download the default font, Public Sans (`guides/IMPLEMENTATION.md` section 4) (`guides/IMPLEMENTATION.md` section 2 has the stylesheet order and section 7 the markup).
3. **Native or other product:** generate your platform's constants from `tokens/design-tokens.json`, then build screens from the component clauses in `policy/UI-4-components.md` (`guides/IMPLEMENTATION.md` section 5 maps them to iOS, Android and desktop).
4. **Changing colours for a client?** Give your assistant the client's colour codes (or the logo file) and tell it to follow `guides/THEMING.md`. Status colours (red, orange, status green, information blue) never change (THM-3).
5. **Check your work** (needs Python 3, no packages):

   ```bash
   python3 tools/guard.py path/to/your/project                     # reads the code
   ```

   Run it after every edit that changes a screen, and check those screens in a browser at phone, tablet and desktop width (SCP-12).

## Moving the rules to Jira

`policy/README.md` explains how to turn each policy file into a Jira ticket and what to do with the files afterwards. The guides, tools and `AGENTS.md` cite clause IDs only, so they keep working after the move.

## Known limits

- There is no dark mode (FND-15).
- The checker covers colours (every platform) and CSS (web). Everything else is covered by checking the work against the policies (SCP-9) and the browser check (SCP-12).

## For maintainers

`web/` and `tokens/` are generated from the source design-system project: change them there, rebuild the package, and copy the result here, so the web files and the token files never drift apart. `policy/`, `guides/`, `tools/`, `README.md` and `AGENTS.md` are edited directly in this directory.
