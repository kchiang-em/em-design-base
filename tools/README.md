# Tools: conformance checker and theme helpers

These scripts **implement and check** the UI policies in `../policy/`. They contain no rules of their own: when a rule changes, the policy changes first, then the scripts follow. All three need only Python 3, with no packages.

| Script | What it does | Implements |
|---|---|---|
| `guard.py` | checks a project against the policies and the baseline, and reports what it finds | SCP-9 (the automated part) |
| `make_theme.py` | turns a client's colour codes into brand-colour overrides: derives the shades, checks contrast, and writes them into the project's `app-tokens.css` or `app-tokens.json` (a block it replaces on every run) | UI-5 (THM-1, THM-5, THM-6, THM-9) |
| `logo_colours.py` | measures the colours in a client's logo file (SVG or PNG; JPEG and others with Pillow) and suggests a `make_theme.py` command | THM-10 |

The theme procedure that uses the last two is in `../guides/THEMING.md`.

## guard.py

The baseline is not a cage, so the guard does not stop work: it makes mistakes and changes visible. It takes about a second.

```bash
python3 <handoff>/tools/guard.py                    # check the current folder (your project)
python3 <handoff>/tools/guard.py path/to/project
python3 <handoff>/tools/guard.py --strict           # warnings also fail
python3 <handoff>/tools/guard.py --platform web     # force web or other (default: web if the folder has .css or .html files)
```

It prints `PASS` or `FAIL` and exits with code 1 on any error. **Every message starts with the clause it checks**, for example `[THM-3]`; look the clause up in `../policy/`. Messages about web set-up that no clause covers start with `[web]`.

**If it fails:** fix the line it names. Never edit the guard to make it pass (SCP-10). Extending the baseline is allowed (SCP-4): add rather than rename or remove, and mention it in your summary.

### What it checks, by clause

| Clause | Check | Platforms | Level |
|---|---|---|---|
| FND-1, SCP-3 | colour literals in source files (`#RRGGBB`, `#RGB`, `0xRRGGBB`, `0xAARRGGBB`) that are not in the palette, naming the closest token | any | warning |
| SCP-3 | `tokens.css` and `components.css` are in the project and every page loads them | web | error |
| SCP-3 | every `var(--token)` is defined | web | error |
| SCP-3 | no raw colours in `components.css`, `app.css`, the component tier of `tokens.css`, or inline `style=""`: rules use tokens | web | error |
| SCP-4 | the project's own colours defined in `app-tokens.css` (chart colours, project accents), listed so they stay visible; they count as the project's palette | web | note |
| SCP-4 | a baseline token or class was removed from the project's copy | web | warning |
| SCP-4 | the project's `tokens.css` or `components.css` differs from the baseline: what was added or changed | web | note |
| FND-9 | raw pixel heights on lines the developer wrote or changed | web | warning |
| ACC-6 | text and background token pairs reach 4.5:1 (including the lightest text grey, `ink-400`, and the status text colours), on the project's colours when it overrides any | web; any with `theme.json` | error |
| ACC-6, FND-17 | non-text pairs reach 3:1: control borders on white and on the page background, status dots, red icons, chart colours against `chart-surface` (what is behind the charts) | web; any with `theme.json` | error |
| SCP-3 | an override of a baseline colour is a valid colour or `var()`; a page that does not load an existing `app-tokens.css` | any | error |
| THM-1 | how many baseline colours the project overrides; an old `theme.css` / `theme.json` still in use (warning) | any | note |
| THM-2 | overridden shadows keep their shape and carry a colour | any | error |
| THM-3 | the project overrides a status colour (`danger-*`, `warning-*`, `success-*`, `info-*`) | any | error |
| SCP-5 | the project overrides a baseline size, spacing or other non-colour token | any | warning |
| SCP-4 | a new project token whose name looks like a misspelt baseline token | any | warning |
| THM-5 | the main brand colour changed without its shades | any | warning |
| [web] | stylesheet load order; `!important`, `@import` and external URLs on the developer's lines; stale `design-tokens.json` when `export_tokens.py` is in the project | web | error or warning |

### What it cannot check

Layout, markup, component behaviour, keyboard use, touch target sizes and how the screens look. Those are the hand checks in SCP-9.

## Changing the tools

The rules come first. To change what is checked:
1. change the clause in `../policy/` (or, once the policies are in Jira, ask the policy owner to change the ticket);
2. update the script and the table above to match;
3. run `python3 tools/guard.py .` from the handoff folder: the package must still pass its own check.
