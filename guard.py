#!/usr/bin/env python3
"""guard.py: cross-checks a project against the EncoreMed design system handoff (Python 3, standard library only).

This file lives in the handoff directory. Run it against your project (any platform):

    python3 /path/to/handoff/guard.py                  # checks the current folder
    python3 /path/to/handoff/guard.py path/to/project  # checks another folder
    python3 /path/to/handoff/guard.py --strict         # warnings also fail
    python3 /path/to/handoff/guard.py --platform web|other   # default: auto (web if the folder has .css or .html files)

Exit code 0 = PASS, 1 = at least one error. Run it before you hand work back.

The design system is a baseline, not a cage: the products can be web or native apps and may extend it. So the guard stays
in the "ballpark": it reports differences and likely mistakes and only fails on clear breakage.

  ANY PLATFORM (Swift, Kotlin, Dart, XML, JS ... any source file)
    - warning: a colour literal (#RRGGBB, #RGB, 0xRRGGBB, 0xAARRGGBB) that is not in the design palette. It names the closest
      design token when there is one. Use the token's value, or tell the user why you needed a new colour.

  WEB PROJECTS ONLY (the project has .css or .html files)
  ERRORS
    1. tokens.css and components.css exist in the project.
    2. Every var(--token) is defined in tokens.css or app-tokens.css.
    3. No raw colours (hex, rgb(), hsl()...) in components.css, app.css, app-tokens.css or inline style="" attributes.
       Raw colours belong only to the palette and semantic tiers of tokens.css.
    4. The component tier of tokens.css and app-tokens.css contain no raw colours (they alias semantic tokens).
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
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HANDOFF = Path(__file__).resolve().parent
BASELINE = HANDOFF / "web" if (HANDOFF / "web" / "tokens.css").exists() else HANDOFF   # where the baseline tokens.css / components.css live
_pos = [a for a in sys.argv[1:] if not a.startswith("--")]
if "--platform" in sys.argv:   # drop the value that follows --platform from the positional arguments
    _v = sys.argv[sys.argv.index("--platform") + 1:][:1]
    _pos = [a for a in _pos if a not in _v]
PROJECT = Path(_pos[0]).resolve() if _pos else Path.cwd()
SHARED = ("tokens.css", "components.css")
PROJECT_CSS = ("components.css", "app.css", "app-tokens.css")
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
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^\s*(--[\w-]+)\s*:\s*(.*?);", strip_comments(css), re.M | re.S)}


def token_defs():
    defs = {}
    for n in ("tokens.css", "app-tokens.css"):
        t = read(n)
        if t:
            defs.update(defs_of(t))
    return defs


def classes_of(css):
    return set(re.findall(r"\.([A-Za-z_][A-Za-z0-9_-]*)", strip_comments(css)))


# ---------------------------------------------------------------- 1 + baseline comparison
def check_shared():
    for n in SHARED:
        if not (PROJECT / n).exists():
            err(f"{n} is missing from the project: copy it from the handoff directory ({BASELINE})")
    if errors or PROJECT in (HANDOFF, BASELINE):
        return
    strict = "--require-baseline" in sys.argv
    for n in SHARED:
        base, cur = read(n, BASELINE), read(n)
        if base is None or base.replace("\r\n", "\n") == cur.replace("\r\n", "\n"):
            continue
        changed = sum(1 for l in difflib.ndiff(base.splitlines(), cur.splitlines()) if l[:2] in ("+ ", "- "))
        msg = f"{n} differs from the handoff baseline ({changed} line(s) added, removed or changed)"
        (err if strict else note)(msg + (": the shared files must stay unchanged in this mode" if strict else ""))
        if n == "tokens.css":
            b, c = defs_of(base), defs_of(cur)
            for k in sorted(set(b) - set(c)):
                warn(f"tokens.css: token {k} was removed; anything that uses it will break")
            changed_v = [k for k in b if k in c and b[k] != c[k]]
            added = [k for k in c if k not in b]
            if changed_v:
                note(f"tokens.css: {len(changed_v)} token value(s) changed, e.g. {', '.join(changed_v[:4])}")
            if added:
                note(f"tokens.css: {len(added)} token(s) added, e.g. {', '.join(added[:4])}")
        else:
            gone = sorted(classes_of(base) - classes_of(cur))
            new = sorted(classes_of(cur) - classes_of(base))
            if gone:
                warn(f"components.css: class(es) removed: {', '.join('.' + k for k in gone[:8])}{' ...' if len(gone) > 8 else ''}")
            if new:
                note(f"components.css: {len(new)} class(es) added, e.g. {', '.join('.' + k for k in new[:4])}")


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
                err(f"{n}:{line_of(css, m.start())}: var({m.group(1)}) is not defined in tokens.css or app-tokens.css")
        if n == "app-tokens.css":
            continue   # raw colours in app-tokens are checked below, per token
        for m in RAW_COLOUR.finditer(css):
            err(f"{n}:{line_of(css, m.start())}: raw colour '{m.group(0)}...': use a colour token")
        for m in re.finditer(r"(?:^|[;{\s])((?:min-|max-)?height)\s*:\s*([^;}]*)", css):
            val = m.group(2).strip()
            px = re.findall(r"(\d+(?:\.\d+)?)px", val)
            if px and "var(" not in val and max(float(x) for x in px) > 2 and own(m.start(1)):   # 1-2px hairlines and visually-hidden text are fine
                warn(f"{n}:{line_of(css, m.start(1))}: raw pixel {m.group(1)} ({val}): use the control size scale or a token")
        for m in re.finditer(r"!important", css):
            before = css[:m.start()]
            if "prefers-reduced-motion" not in before[before.rfind("@media"):] and own(m.start()):
                warn(f"{n}:{line_of(css, m.start())}: !important")
        for m in re.finditer(r"@import|url\(\s*['\"]?https?:", css):
            if own(m.start()):
                warn(f"{n}:{line_of(css, m.start())}: external stylesheet or URL")


# ---------------------------------------------------------------- 4. raw colours only in palette and semantic tiers
def check_token_tiers():
    t = read("tokens.css")
    if t and "COMPONENT TOKENS" in t:
        tail = strip_comments(t[t.index("COMPONENT TOKENS"):])
        for m in RAW_COLOUR.finditer(tail):
            err(f"tokens.css (component tier): raw colour '{m.group(0)}...': component tokens must alias semantic tokens")
    a = read("app-tokens.css")
    if a:
        css = strip_comments(a)
        for m in RAW_COLOUR.finditer(css):
            err(f"app-tokens.css:{line_of(css, m.start())}: raw colour '{m.group(0)}...': alias a semantic token")


# ---------------------------------------------------------------- 5 + inline styles: html files
def check_html():
    order = ["tokens.css", "app-tokens.css", "components.css", "app.css"]
    for p in sorted(PROJECT.glob("*.html")):
        html = p.read_text()
        names = [Path(l).name for l in re.findall(r'<link[^>]+href="([^"]+\.css)"', html)]
        known = [n for n in names if n in order]
        if known != sorted(known, key=order.index):
            err(f"{p.name}: stylesheets must load in this order: {', '.join(order)} (found: {', '.join(known)})")
        for need in SHARED:
            if need not in names:
                err(f"{p.name}: does not load {need}")
        for m in re.finditer(r'style="([^"]*)"', html):
            if RAW_COLOUR.search(m.group(1)):
                err(f"{p.name}:{line_of(html, m.start())}: inline style with a raw colour: use a token class or a variable")


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


PAIRS = [("--ink-700", "--white"), ("--ink-600", "--white"), ("--ink-500", "--white"), ("--ink-700", "--bg"), ("--ink-600", "--bg"),
         ("--brand-600", "--white"), ("--white", "--brand-600"), ("--brand-800", "--accent-500"), ("--accent-700", "--accent-50")]


def check_contrast(defs):
    for fg, bg in PAIRS:
        a, b = resolve(defs, fg), resolve(defs, bg)
        if not a or not b:
            continue   # a project may rename or drop a token: other checks catch real breakage
        ratio = contrast(a, b)
        if ratio < 4.5:
            err(f"contrast {fg} on {bg} is {ratio:.2f}:1 (needs 4.5:1)")
    ink400, white = resolve(defs, "--ink-400"), resolve(defs, "--white")
    if ink400 and white and contrast(ink400, white) < 4.5:
        note(f"--ink-400 is {contrast(ink400, white):.1f}:1 on white: fine for placeholders and icons only, never for important text")


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
            err("export_tokens.py failed: " + (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ["unknown error"])[-1])
            return
        for out in ("design-tokens.json", "DESIGN-TOKENS.md"):
            if (PROJECT / out).exists() and (PROJECT / out).read_text() != (d / out).read_text():
                err(f"{out} is out of date: run python3 export_tokens.py")


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
        warn(f"colour {hexv} is not in the design palette ({hint}) at {', '.join(where[:3])}{more}")


def detect_web():
    if "--platform" in sys.argv:
        return sys.argv[sys.argv.index("--platform") + 1:][:1] == ["web"]
    return any((PROJECT / n).exists() for n in ("tokens.css", "components.css", "app.css")) or any(PROJECT.glob("*.html"))


def main():
    web = detect_web()
    print(f"guard: project  {PROJECT}  ({'web' if web else 'any platform: colour ballpark check only'})\n       baseline {BASELINE}\n")
    defs = {}
    if web:
        check_shared()
        if not errors:
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
