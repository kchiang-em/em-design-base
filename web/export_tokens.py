"""Generate design-tokens.json and DESIGN-TOKENS.md from tokens.css and app-tokens.css (standard library only).

Run:  python3 export_tokens.py

tokens.css (reusable design system) and app-tokens.css (this app's screens) are the source of truth. Both outputs are
generated, so edit those files, then re-run this.

Tiers (in the order they appear):
  palette    the official EncoreMed colours (--em-*)                                              tokens.css
  semantic   roles built from the palette: neutrals, text, brand, accent, status, type, spacing, radius, shadow   tokens.css
  component  per-control tokens for buttons, fields, dropdowns, pagination, etc.                  tokens.css
  app        screen-specific values: login panel, residents table columns, filter bar, list rows  app-tokens.css
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
def _read(name):
    """app-tokens.css and app.css are optional: a new project may start with only tokens.css and components.css."""
    p = HERE / name
    return p.read_text() if p.exists() else ""


SRC = (HERE / "tokens.css").read_text() + "\n" + _read("app-tokens.css")

DECL = re.compile(r"^\s*(--[\w-]+):\s*(.*?);\s*(?:/\*\s*(.*?)\s*\*/)?\s*$")
COMMENT = re.compile(r"^\s*/\*\s*(.*?)\s*\*/\s*$")

tiers = {"palette": {}, "semantic": {}, "component": {}, "app": {}}
order = []          # (tier, group) in file order
tier, group = "semantic", "general"
raw = {}            # name -> (tier, group, value, description)

for line in SRC.splitlines():
    if "Official EncoreMed palette" in line:
        tier, group = "palette", "Official palette"
        continue
    if "Semantic tokens" in line:
        tier, group = "semantic", "Colour: neutrals, text, brand, status"
        continue
    if "COMPONENT TOKENS" in line:
        tier, group = "component", "general"
        continue
    if "APP TOKENS" in line:
        tier, group = "app", "general"
        continue
    m = DECL.match(line)
    if m:
        name, value, desc = m.group(1)[2:], m.group(2).strip(), (m.group(3) or "").strip()
        raw[name] = (tier, group, value, desc)
        if (tier, group) not in order:
            order.append((tier, group))
        continue
    c = COMMENT.match(line)
    if c and not c.group(1).startswith("="):
        label = c.group(1).strip("- ").strip()
        if label:
            group = label

REF = re.compile(r"var\(--([\w-]+)\)")


def resolve(value, seen=()):
    def sub(m):
        n = m.group(1)
        if n in seen or n not in raw:
            return m.group(0)
        return resolve(raw[n][2], seen + (n,))
    return REF.sub(sub, value)


def kind(name, resolved):
    v = resolved.strip()
    if re.match(r"^(#[0-9a-fA-F]{3,8}|rgb\(|color-mix\()", v):
        return "color"
    if name.startswith(("shadow", "focus-ring", "pressed-ring")) or (
            re.match(r"^(inset\s+)?-?\d+(px)?\s+-?\d+(px)?\s", v) and re.search(r"#|rgb|color-mix|hsl", v)):
        return "shadow"
    if name.startswith("font-"):
        return "fontFamily"
    if name.startswith("weight-"):
        return "fontWeight"
    if re.fullmatch(r"-?\d+(\.\d+)?(px|rem|em|%)", v):
        return "dimension"
    if re.fullmatch(r"-?\d*\.?\d+", v):
        return "number"
    if re.fullmatch(r"-?\d+(\.\d+)?ms", v):
        return "duration"
    return "other"


def alias(value):
    return REF.sub(lambda m: "{" + m.group(1) + "}", value)


# Breakpoint tokens are documentation tokens (media queries cannot use custom properties): fail if they drift from components.css/app.css.
_css = _read("components.css") + "\n" + _read("app.css")


def _media_blocks(css):
    """Yield (max-width px, block body) for every @media (max-width: Npx) block, using brace matching."""
    for m in re.finditer(r"@media \(max-width: (\d+)px\)\s*\{", css):
        depth, k = 1, m.end()
        while depth and k < len(css):
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        yield m.group(1), css[m.end():k - 1]


for _name, _needle in (("pager-compact-breakpoint", ".pager__btn--nav span"), ("filters-compact-breakpoint", ".filters {")):
    if _name not in raw:
        continue   # this project does not define the token, so there is nothing to check
    _found = [px for px, body in _media_blocks(_css) if _needle in body]
    _tok = raw.get(_name, (None, None, "", ""))[2]
    if not _found or f"{_found[0]}px" != _tok:
        raise SystemExit(f"--{_name} ({_tok or 'missing'}) does not match the @media query in components.css/app.css ({_found[0] + 'px' if _found else 'not found'})")

out = {"$description": "EncoreMed design tokens, generated from tokens.css and app-tokens.css. Aliases use {token-name}.",
       "palette": {}, "semantic": {}, "component": {}, "app": {}}
for name, (t, g, value, desc) in raw.items():
    res = resolve(value)
    entry = {"$value": alias(value), "$type": kind(name, res), "$group": g}
    if res != value:
        entry["$resolved"] = res
    if desc:
        entry["$description"] = desc
    out[t][name] = entry
(HERE / "design-tokens.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------- DESIGN-TOKENS.md
def table(rows):
    lines = ["| Token | Value | Resolves to |", "|---|---|---|"]
    for name, value, res, desc in rows:
        shown = f"`{value}`"
        res_cell = f"`{res}`" if res != value else ""
        if desc:
            shown += f" <br><sub>{desc}</sub>"
        lines.append(f"| `--{name}` | {shown} | {res_cell} |")
    return "\n".join(lines)


md = ["# Design tokens",
      "",
      "> Generated from `tokens.css` by `export_tokens.py`. Do not edit by hand: change `tokens.css`, then run `python3 export_tokens.py`.",
      "> Machine-readable copy: `design-tokens.json` (aliases written as `{token-name}`, for generating platform constants or importing into design tools).",
      "",
      "## How the tokens are layered",
      "",
      "| Tier | What it holds | Who uses it |",
      "|---|---|---|",
      "| **Palette** | The official EncoreMed colours (`--em-*`), from the official brand guideline (CMYK converted to sRGB) and its colour-blind-safe set. | Only the semantic tier. |",
      "| **Semantic** | Roles built from the palette: neutrals, text, brand, accent, status, type, spacing, radius, shadow. | Component tokens, and layout rules. |",
      "| **Component** | Sizes, colours and states for each control: buttons, fields, dropdowns, pagination, checkbox, toggle, sidebar nav. | Component rules (`components.css`). New components should start here. |",
      "| **App** | Screen-specific values (login panel, residents table columns, filter bar, list rows), in `app-tokens.css`. Not part of the reusable design system. | `app.css` only. |",
      "",
      "## Rules for new components",
      "",
      "1. **No raw colours or pixel heights in a rule.** Use a component token; if none fits, add one to the component tier in `tokens.css` first.",
      "2. **Heights come from the control size scale** (`--control-h-sm` 32, `-md` 36, `-lg` 40, `-xl` 44, `-2xl` 48 px). Do not invent other heights.",
      "3. **Every control has the same states:** default, hover, pressed (amber, `--pressed-*`), disabled, and keyboard focus (`--focus-ring`).",
      "4. **Text colour contrast:** body and secondary text must stay at 4.5:1 or better on their background. The green and mint palette colours are for fills, dots and icons, not text.",
      "5. **Name tokens** `--{component}-{variant?}-{property}-{state?}` (for example `--btn-primary-bg-hover`).",
      ""]
titles = {"palette": "Palette tokens", "semantic": "Semantic tokens", "component": "Component tokens", "app": "App tokens (this app's screens only)"}
for t in ("palette", "semantic", "component", "app"):
    md += [f"## {titles[t]}", ""]
    for (tt, g) in order:
        if tt != t:
            continue
        rows = [(n, v, resolve(v), d) for n, (t2, g2, v, d) in raw.items() if t2 == t and g2 == g]
        if not rows:
            continue
        md += [f"### {g[0].upper() + g[1:] if g == g.lower() else g}", "", table(rows), ""]
(HERE / "DESIGN-TOKENS.md").write_text("\n".join(md))
counts = {k: len(v) for k, v in out.items() if isinstance(v, dict)}
print("wrote design-tokens.json and DESIGN-TOKENS.md:", counts, "| total", sum(counts.values()))
