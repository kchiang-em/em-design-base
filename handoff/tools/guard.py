#!/usr/bin/env python3
"""guard.py: cross-checks a project against the EncoreMed design system handoff (Python 3, standard library only).

This file lives in the handoff directory's tools/ folder. Run it against your project (any platform):

    python3 /path/to/handoff/tools/guard.py                  # checks the current folder
    python3 /path/to/handoff/tools/guard.py path/to/project  # checks another folder
    python3 /path/to/handoff/tools/guard.py --strict         # warnings also fail
    python3 /path/to/handoff/tools/guard.py --platform web|other   # default: auto (web if the folder has .css or .html files)

Exit code 0 = PASS, 1 = at least one error. Run it before you hand work back (SCP-9).

The rules live in ../policy/ (UI-1 to UI-5). Every message starts with the clause it checks, for example [THM-3];
messages about web set-up that no clause covers start with [web].

The design system is a baseline, not a cage: the products can be web or native apps and may extend it. So the guard stays
in the "ballpark": it reports differences and likely mistakes and only fails on clear breakage.

  PROJECT TOKENS AND CLIENT COLOURS
    The project's own tokens live in ONE file at the project root:  app-tokens.css  (web)  or  app-tokens.json  (any platform,
    {"colors": {"name": "#hex"}}). It holds the project's new tokens AND its overrides of baseline tokens, such as a client's
    brand colours (make_theme.py writes those). Raw colours are allowed there.
    - Overriding a status colour is an error: red (danger-*), orange (warning-*), green (success-*), information blue (info-*).
    - Overriding the main brand colour without its lighter and darker shades is a warning.
    - Overriding a baseline token that is not a colour (sizes, spacing, radii) is a warning.
    - Contrast is checked on the project's colours; its colours count as the project's palette.
    - theme.css / theme.json (older packages) still work, with a warning to move them into app-tokens.

  ANY PLATFORM (Swift, Kotlin, Dart, XML, JS ... any source file)
    - warning: a colour literal (#RRGGBB, #RGB, 0xRRGGBB, 0xAARRGGBB) that is not in the design palette. It names the closest
      design token when there is one. Use the token's value, or tell the user why you needed a new colour.

  WEB PROJECTS ONLY (the project has .css or .html files)
  ERRORS
    1. tokens.css and components.css exist in the project.
    2. Every var(--token) is defined in tokens.css or app-tokens.css.
    3. No raw colours (hex, rgb(), hsl()...) in components.css, app.css or inline style="" attributes: rules use tokens.
       Raw colours belong only to the palette and semantic tiers of tokens.css.
    4. The component tier of tokens.css contains no raw colours (component tokens alias semantic tokens).
       app-tokens.css MAY define the project's own colours (chart colours, project accents): they are listed in a note.
    5. Stylesheets load in this order in every .html file: tokens, app-tokens, components, app.
    6. Text and background token pairs meet 4.5:1 contrast (WCAG AA).
    7. design-tokens.json / DESIGN-TOKENS.md are not stale (only if export_tokens.py is in the project).
  WARNINGS (fix, or explain in your summary)
    - a token or a class that exists in the handoff baseline was removed from the project's shared files
      (web: tokens.css / components.css)
    - raw pixel height / min-height / max-height (use the control size scale or a token)
    - !important (except in prefers-reduced-motion), @import or external URLs
  NOTES (information, not a problem)
    - the project's tokens.css / components.css differ from the handoff baseline (what was added or changed)
"""
import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HANDOFF = Path(__file__).resolve().parent.parent   # this file is in <handoff>/tools/
BASELINE = HANDOFF / "web"                          # where the baseline tokens.css / components.css live
_pos = [a for a in sys.argv[1:] if not a.startswith("--")]
if "--platform" in sys.argv:   # drop the value that follows --platform from the positional arguments
    _v = sys.argv[sys.argv.index("--platform") + 1:][:1]
    _pos = [a for a in _pos if a not in _v]
PROJECT = Path(_pos[0]).resolve() if _pos else Path.cwd()
SHARED = ("tokens.css", "components.css")
APP_CSS, APP_JSON = "app-tokens.css", "app-tokens.json"
LEGACY = {"theme.css": APP_CSS, "theme.json": APP_JSON}   # older packages kept client colours in a separate theme file
# Status colours are universal: a project may not change them (red, orange, green, information blue). FND-3, THM-3.
LOCKED_EXACT = set()
LOCKED_PREFIX = ("--danger-", "--warning-", "--success-", "--info-")
# Shadows (and, in older baselines, the focus ring) are tinted with the brand colour, so a theme may restyle them too.
TINTED_EFFECTS = {"--focus-ring", "--shadow-md", "--shadow-lg", "--shadow-brand"}


def is_locked(name):
    return name in LOCKED_EXACT or name.startswith(LOCKED_PREFIX)
PROJECT_CSS = ("components.css", "app.css", "app-tokens.css")
THEME = {}   # the project's token entries (app-tokens.css / app-tokens.json): token -> value, filled by load_theme()
errors, warnings, notes = [], [], []


def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)
def note(msg): notes.append(msg)


def read(name, base=None):
    p = (base or PROJECT) / name
    return p.read_text() if p.exists() else None


def strip_comments(css):
    # keep newlines so line numbers still match the original
    return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css, flags=re.S)


def line_of(text, index):
    return text.count("\n", 0, index) + 1


RAW_COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgb|rgba|hsl|hsla|hwb|lab|lch|oklab|oklch)\(")


def defs_of(css):
    # custom property declarations anywhere in the text (one per line, or several on one line)
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"(?<![\w-])(--[\w-]+)\s*:\s*([^;{}]+?)\s*(?:;|(?=\}))", strip_comments(css))}


def token_defs():
    defs = defs_of(read("tokens.css") or "")
    defs.update(THEME)   # the project's tokens, after check_theme() dropped the rejected overrides
    return defs


def baseline_defs():
    t = read("tokens.css", BASELINE)
    return defs_of(t) if t else {}


# ---------------------------------------------------------------- client theme
HEX_COLOUR = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\Z")
BRAND_ROOTS = {"--em-navy-core", "--em-blue", "--em-navy", "--brand-500", "--brand-600"}
BRAND_SHADES = ["--brand-50", "--brand-100", "--brand-400", "--brand-700", "--brand-800"]
INK_ROOTS = {"--em-slate", "--em-grey-dark", "--ink-600", "--ink-700"}
INK_SHADES = ["--ink-300", "--ink-400", "--ink-500", "--border", "--surface-muted"]


def load_theme():
    THEME.clear()
    for old, new in LEGACY.items():
        if read(old) is not None:
            warn(f"[THM-1] {old} is from an older package: move its contents into {new} (it is still read for now)")
    for name in ("theme.css", APP_CSS):
        css = read(name)
        if css:
            THEME.update(defs_of(css))
    for name in ("theme.json", APP_JSON):
        js = read(name)
        if not js:
            continue
        try:
            data = json.loads(js)
        except json.JSONDecodeError as e:
            err(f"[THM-1] {name} is not valid JSON: {e}")
            continue
        colours = data.get("colors", data) if isinstance(data, dict) else {}
        for k, v in colours.items():
            if isinstance(v, str) and not k.startswith(("$", "note", "_")):
                THEME[k if k.startswith("--") else "--" + k] = v.strip()


def is_colour_token(base, name, depth=0):
    v = base.get(name)
    if v is None or depth > 10:
        return False
    m = re.fullmatch(r"var\((--[\w-]+)\)", v)
    if m:
        return is_colour_token(base, m.group(1), depth + 1)
    if re.search(r"\d+px", v):
        return False
    return bool(HEX_COLOUR.match(v) or RAW_COLOUR.search(v) or "color-mix(" in v)


def check_theme():
    """Checks the project's overrides of baseline tokens (a client's brand colours, for example). New tokens are the project's own."""
    if not THEME:
        return
    base = baseline_defs()
    known = set(base) | set(defs_of(read("tokens.css") or ""))
    rejected = set()   # overrides that are errors are ignored by every other check, so one mistake is reported once
    colour_overrides = 0
    for name, val in list(THEME.items()):
        if name not in known:   # the project's own token
            close = difflib.get_close_matches(name, sorted(known), n=1, cutoff=0.92)
            if close:
                warn(f"[SCP-4] project token {name} is not in the baseline but looks like {close[0]}: a typo?")
            continue
        if base.get(name) == val:
            continue
        if is_locked(name):
            err(f"[THM-3] {name} is a status colour (red, orange, green or information blue) and is universal: a project cannot change it")
            rejected.add(name)
            continue
        if name in TINTED_EFFECTS:
            if not re.search(r"rgba?\(|#[0-9a-fA-F]{3,8}|var\(--", val):
                err(f"[THM-2] {name} must keep its shape and carry a colour, e.g. '0 8px 24px rgb(R G B / 14%)', found '{val}'")
                rejected.add(name)
            continue
        if not is_colour_token(base, name):
            warn(f"[SCP-5] {name} overrides a baseline size, spacing or other non-colour token: allowed for a real need, tell the user")
            continue
        alias = re.fullmatch(r"var\((--[\w-]+)\)", val)
        if alias:
            if alias.group(1) not in known | set(THEME):
                err(f"[SCP-3] {name} refers to {alias.group(1)}, which is not defined")
                rejected.add(name)
                continue
        elif not (HEX_COLOUR.match(val) or re.match(r"(?:rgba?|hsla?)\(", val)):
            err(f"[SCP-3] {name} must be a colour (hex, rgb() or hsl()) or a var(), found '{val}'")
            rejected.add(name)
            continue
        colour_overrides += 1
    for name in rejected:
        THEME.pop(name, None)
    # the main colours changed but their lighter and darker shades did not
    changed = {k for k in THEME if k in known and base.get(k) != THEME[k]}
    for roots, shades, label in ((BRAND_ROOTS, BRAND_SHADES, "brand"), (INK_ROOTS, INK_SHADES, "text and surface")):
        if roots & changed:
            missing = [x for x in shades if x not in changed]
            if len(missing) >= len(shades) - 2:
                warn(f"[THM-5] the {label} colours were changed but these related shades were not: {', '.join(missing)}. "
                     f"They still show the EncoreMed colours in hover, tinted and border states (use make_theme.py)")
    if colour_overrides:
        note(f"[THM-1] the project overrides {colour_overrides} baseline colour(s), for example a client's brand colours")


def classes_of(css):
    return set(re.findall(r"\.([A-Za-z_][A-Za-z0-9_-]*)", strip_comments(css)))


# ---------------------------------------------------------------- 1 + baseline comparison
def check_shared():
    for n in SHARED:
        if not (PROJECT / n).exists():
            err(f"[SCP-3] {n} is missing from the project: copy it from the handoff directory ({BASELINE})")
    if errors or PROJECT in (HANDOFF, BASELINE):
        return
    strict = "--require-baseline" in sys.argv
    for n in SHARED:
        base, cur = read(n, BASELINE), read(n)
        if base is None or base.replace("\r\n", "\n") == cur.replace("\r\n", "\n"):
            continue
        changed = sum(1 for l in difflib.ndiff(base.splitlines(), cur.splitlines()) if l[:2] in ("+ ", "- "))
        msg = f"[SCP-4] {n} differs from the handoff baseline ({changed} line(s) added, removed or changed)"
        (err if strict else note)(msg + (": the shared files must stay unchanged in this mode" if strict else ""))
        if n == "tokens.css":
            b, c = defs_of(base), defs_of(cur)
            for k in sorted(set(b) - set(c)):
                warn(f"[SCP-4] tokens.css: token {k} was removed; anything that uses it will break")
            changed_v = [k for k in b if k in c and b[k] != c[k]]
            added = [k for k in c if k not in b]
            if changed_v:
                note(f"[SCP-4] tokens.css: {len(changed_v)} token value(s) changed, e.g. {', '.join(changed_v[:4])}")
            if added:
                note(f"[SCP-4] tokens.css: {len(added)} token(s) added, e.g. {', '.join(added[:4])}")
        else:
            gone = sorted(classes_of(base) - classes_of(cur))
            new = sorted(classes_of(cur) - classes_of(base))
            if gone:
                warn(f"[SCP-4] components.css: class(es) removed: {', '.join('.' + k for k in gone[:8])}{' ...' if len(gone) > 8 else ''}")
            if new:
                note(f"[SCP-4] components.css: {len(new)} class(es) added, e.g. {', '.join('.' + k for k in new[:4])}")


# ---------------------------------------------------------------- 2, 3, warnings: stylesheets
def check_css(defs):
    for n in PROJECT_CSS:
        raw = read(n)
        if raw is None:
            continue
        css = strip_comments(raw)
        # lines that are identical to the handoff baseline are not the developer's: do not warn about them
        base_text = read(n, BASELINE) if n in SHARED and PROJECT not in (HANDOFF, BASELINE) else None
        base_lines = {l.strip() for l in strip_comments(base_text).splitlines()} if base_text else set()
        css_lines = css.splitlines()
        own = lambda idx: css_lines[line_of(css, idx) - 1].strip() not in base_lines
        for m in re.finditer(r"var\((--[\w-]+)", css):
            if m.group(1) not in defs:
                err(f"[SCP-3] {n}:{line_of(css, m.start())}: var({m.group(1)}) is not defined in tokens.css or app-tokens.css")
        if n == "app-tokens.css":
            continue   # app-tokens may define project colours: listed in check_token_tiers()
        for m in RAW_COLOUR.finditer(css):
            err(f"[SCP-3] {n}:{line_of(css, m.start())}: raw colour '{m.group(0)}...': use a colour token (project colours go in app-tokens.css, a client's brand colours in theme.css)")
        for m in re.finditer(r"(?:^|[;{\s])((?:min-|max-)?height)\s*:\s*([^;}]*)", css):
            val = m.group(2).strip()
            px = re.findall(r"(\d+(?:\.\d+)?)px", val)
            if px and "var(" not in val and max(float(x) for x in px) > 2 and own(m.start(1)):   # 1-2px hairlines and visually-hidden text are fine
                warn(f"[FND-9] {n}:{line_of(css, m.start(1))}: raw pixel {m.group(1)} ({val}): use the control size scale or a token")
        for m in re.finditer(r"!important", css):
            before = css[:m.start()]
            if "prefers-reduced-motion" not in before[before.rfind("@media"):] and own(m.start()):
                warn(f"[web] {n}:{line_of(css, m.start())}: !important")
        for m in re.finditer(r"@import|url\(\s*['\"]?https?:", css):
            if own(m.start()):
                warn(f"[web] {n}:{line_of(css, m.start())}: external stylesheet or URL")


# ---------------------------------------------------------------- 4. raw colours only in palette and semantic tiers
def check_token_tiers():
    t = read("tokens.css")
    if t and "COMPONENT TOKENS" in t:
        tail = strip_comments(t[t.index("COMPONENT TOKENS"):])
        for m in RAW_COLOUR.finditer(tail):
            err(f"[SCP-3] tokens.css (component tier): raw colour '{m.group(0)}...': component tokens must alias semantic tokens")
    a = read("app-tokens.css")
    if a:   # the project's own colours belong here (SCP-3, SCP-4): allowed, and listed so they stay visible
        base = baseline_defs()
        own = {k: v for k, v in defs_of(a).items() if RAW_COLOUR.search(v) and k not in base}
        if own:
            note(f"[SCP-4] app-tokens.css defines {len(own)} project colour(s): " + ", ".join(f"{k} {v}" for k, v in list(own.items())[:6]) + (" ..." if len(own) > 6 else ""))


# ---------------------------------------------------------------- 5 + inline styles: html files
def check_html():
    order = ["tokens.css", "theme.css", "app-tokens.css", "components.css", "app.css"]   # theme.css: older packages
    for p in sorted(PROJECT.glob("*.html")):
        html = p.read_text()
        names = [Path(l).name for l in re.findall(r'<link[^>]+href="([^"]+\.css)"', html)]
        known = [n for n in names if n in order]
        if known != sorted(known, key=order.index):
            err(f"[web] {p.name}: stylesheets must load in this order: {', '.join(n for n in order if n != 'theme.css')} (found: {', '.join(known)})")
        for need in SHARED:
            if need not in names:
                err(f"[SCP-3] {p.name}: does not load {need}")
        if (PROJECT / APP_CSS).exists() and APP_CSS not in names:
            err(f"[SCP-3] {p.name}: the project has an {APP_CSS} but this page does not load it (right after tokens.css)")
        for m in re.finditer(r'style="([^"]*)"', html):
            if RAW_COLOUR.search(m.group(1)):
                err(f"[SCP-3] {p.name}:{line_of(html, m.start())}: inline style with a raw colour: use a token class or a variable")


# ---------------------------------------------------------------- 6. contrast
def resolve(defs, name, depth=0):
    v = defs.get(name)
    if v is None or depth > 10:
        return None
    m = re.fullmatch(r"var\((--[\w-]+)\)", v)
    if m:
        return resolve(defs, m.group(1), depth + 1)
    return v if re.fullmatch(r"#[0-9a-fA-F]{6}", v) else None


def luminance(hex6):
    c = [int(hex6[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


PAIRS = [("--pressed-fg", "--pressed-bg"), ("--ink-700", "--white"), ("--ink-600", "--white"), ("--ink-500", "--white"), ("--ink-400", "--white"),
         ("--ink-700", "--bg"), ("--ink-600", "--bg"), ("--ink-400", "--bg"),
         ("--brand-600", "--white"), ("--white", "--brand-600"), ("--nav-toggle-fg", "--nav-toggle-bg"),
         ("--success-700", "--success-50"), ("--success-600", "--white"), ("--info-600", "--white"), ("--info-600", "--info-50"),
         ("--danger-700", "--white"), ("--field-error-fg", "--white"), ("--warning-700", "--white"), ("--warning-700", "--warning-50")]
# non-text contrast (WCAG 1.4.11): borders that identify a control, status dots and icons need 3:1
PAIRS_NONTEXT = [("--border-control", "--white"), ("--border-control", "--bg"), ("--field-border", "--white"), ("--dd-trigger-border", "--white"),
                 ("--success-600", "--bg"), ("--danger-600", "--white")] + [(f"--chart-{i}", "--chart-surface") for i in (1, 2, 3, 4, 5, 6, 7)] + [("--chart-other", "--chart-surface")]   # FND-17: against what is behind the charts


def check_contrast(defs):
    for fg, bg in PAIRS:
        a, b = resolve(defs, fg), resolve(defs, bg)
        if not a or not b:
            continue   # a project may rename or drop a token: other checks catch real breakage
        ratio = contrast(a, b)
        if ratio < 4.5:
            err(f"[ACC-6] contrast {fg} on {bg} is {ratio:.2f}:1 (needs 4.5:1)")
    for fg, bg in PAIRS_NONTEXT:
        a, b = resolve(defs, fg), resolve(defs, bg)
        if a and b and contrast(a, b) < 3:
            err(f"[ACC-6] non-text contrast {fg} on {bg} is {contrast(a, b):.2f}:1 (needs 3:1)")


# ---------------------------------------------------------------- 7. generated files are current
def check_generated():
    if not (PROJECT / "export_tokens.py").exists() or not (PROJECT / "design-tokens.json").exists():
        return
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for n in ("export_tokens.py", "tokens.css", "components.css", "app-tokens.css", "app.css"):
            if (PROJECT / n).exists():
                shutil.copy(PROJECT / n, d / n)
        r = subprocess.run([sys.executable, "-I", str(d / "export_tokens.py")], capture_output=True, text=True, cwd=d)
        if r.returncode != 0:
            err("[web] export_tokens.py failed: " + (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ["unknown error"])[-1])
            return
        for out in ("design-tokens.json", "DESIGN-TOKENS.md"):
            if (PROJECT / out).exists() and (PROJECT / out).read_text() != (d / out).read_text():
                err(f"[web] {out} is out of date: run python3 export_tokens.py")


# ---------------------------------------------------------------- any platform: colours must stay in the ballpark
SOURCE_EXT = {".swift", ".m", ".h", ".kt", ".java", ".xml", ".dart", ".cs", ".xaml", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte",
              ".html", ".css", ".scss", ".less", ".json5", ".qml", ".rs", ".py", ".gd"}
SKIP_DIRS = {".git", "node_modules", "build", "dist", "Pods", "DerivedData", ".gradle", ".idea", ".dart_tool", "__pycache__", "venv", ".venv", "Carthage"}
HEX = re.compile(r"(?<![\w&])(?:#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![\w])|0[xX]([0-9a-fA-F]{8}|[0-9a-fA-F]{6})(?![\w]))")


def palette():
    """hex -> token name, for every baseline token that resolves to a plain colour."""
    base = read("tokens.css", BASELINE)
    if base is None:
        return {}
    d = defs_of(base)
    if PROJECT not in (HANDOFF, BASELINE) and read("tokens.css"):
        d.update(defs_of(read("tokens.css")))   # colours the project changed in its own tokens.css count as its palette
    if read("app-tokens.css"):
        d.update(defs_of(read("app-tokens.css")))   # so do the project's own colours
    d.update(THEME)                              # so do the colours of a client theme
    out = {}
    for name in d:
        h = resolve(d, name)
        if h:
            out.setdefault(h.lower(), name)
    return out


def norm_hex(code):
    """candidate #rrggbb values for a literal (an 8-digit code can be #RRGGBBAA or 0xAARRGGBB)."""
    code = code.lower()
    if len(code) == 3:
        return ["#" + "".join(c * 2 for c in code)]
    if len(code) == 6:
        return ["#" + code]
    return ["#" + code[:6], "#" + code[2:]]


def check_ballpark(web):
    pal = palette()
    if not pal:
        return
    skip_css = web   # in a web project, .css files are checked more strictly by the checks above
    seen = {}
    for p in PROJECT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in SOURCE_EXT or any(part in SKIP_DIRS for part in p.relative_to(PROJECT).parts):
            continue
        if p.resolve() == Path(__file__).resolve() or (skip_css and p.suffix.lower() in (".css", ".scss", ".less")):
            continue
        try:
            text = p.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for m in HEX.finditer(line):
                code = m.group(1) or m.group(2)
                cands = norm_hex(code)
                if any(c in pal for c in cands):
                    continue
                key = cands[0]
                seen.setdefault(key, []).append(f"{p.relative_to(PROJECT)}:{i}")
    for hexv, where in sorted(seen.items(), key=lambda kv: -len(kv[1])):
        rgb = tuple(int(hexv[i:i + 2], 16) for i in (1, 3, 5))
        best = min(pal.items(), key=lambda kv: sum((int(kv[0][i:i + 2], 16) - rgb[j]) ** 2 for j, i in enumerate((1, 3, 5))))
        dist = sum((int(best[0][i:i + 2], 16) - rgb[j]) ** 2 for j, i in enumerate((1, 3, 5))) ** 0.5
        hint = f"closest token: {best[1]} {best[0]}" if dist <= 60 else "no close token"
        more = f" (+{len(where) - 3} more)" if len(where) > 3 else ""
        warn(f"[FND-1] colour {hexv} is not in the design palette ({hint}) at {', '.join(where[:3])}{more}")


def detect_web():
    if "--platform" in sys.argv:
        return sys.argv[sys.argv.index("--platform") + 1:][:1] == ["web"]
    return any((PROJECT / n).exists() for n in ("tokens.css", "components.css", "app.css", APP_CSS, "theme.css")) or any(PROJECT.glob("*.html"))


def main():
    web = detect_web()
    load_theme()
    print(f"guard: project  {PROJECT}  ({'web' if web else 'any platform: colour ballpark check'}{', project tokens' if THEME else ''})\n       baseline {BASELINE}\n")
    defs = {}
    if not web and THEME:
        check_theme()
        merged = baseline_defs()
        merged.update(THEME)
        check_contrast(merged)
    if web:
        check_shared()
        if not errors:
            check_theme()
            defs = token_defs()
            check_css(defs)
            check_token_tiers()
            check_html()
            check_contrast(defs)
            check_generated()
    check_ballpark(web)
    if "--strict" in sys.argv:
        errors.extend(f"(strict) {w}" for w in warnings)
        warnings.clear()
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("warning", w)
    for n in notes:
        print("note   ", n)
    print(f"\n{'FAIL' if errors else 'PASS'}: {len(errors)} error(s), {len(warnings)} warning(s), {len(notes)} note(s)" + (f", {len(defs)} tokens checked" if web else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
