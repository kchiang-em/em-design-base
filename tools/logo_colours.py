#!/usr/bin/env python3
"""logo_colours.py: read a client's logo and list its brand colours (Python 3, standard library only for SVG and PNG).

Use it when the user gives you a logo instead of colour codes. Never guess colours by eye from an image: shades read off a
picture are unreliable (THM-10). Read ../guides/THEMING.md first.

    python3 <handoff>/tools/logo_colours.py path/to/logo.svg
    python3 <handoff>/tools/logo_colours.py path/to/logo.png --json

Formats: SVG and PNG work with no packages. JPEG, WebP and GIF need the Pillow package (pip install pillow); without it, ask the
user for a PNG or SVG of the logo, or for the colour codes.

It prints the candidate brand colours (most prominent first), the neutrals, and a suggested make_theme.py command.
THE SUGGESTION IS ONLY A STARTING POINT: show the colours to the user and get them to confirm which is the primary.
Exit code 0 = colours found, 1 = could not read the file, 2 = the file has no usable brand colour (for example a black and white logo).
"""
import colorsys
import json
import re
import struct
import sys
import zlib
from pathlib import Path

NAMED = {"black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "green": (0, 128, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0),
         "orange": (255, 165, 0), "purple": (128, 0, 128), "gray": (128, 128, 128), "grey": (128, 128, 128), "navy": (0, 0, 128),
         "teal": (0, 128, 128), "maroon": (128, 0, 0), "olive": (128, 128, 0), "lime": (0, 255, 0), "aqua": (0, 255, 255),
         "fuchsia": (255, 0, 255), "silver": (192, 192, 192)}
MAX_PIXELS = 4_000_000


# ------------------------------------------------------------------ reading images
def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def read_svg(path):
    """Every colour used in fill, stroke and gradient stops, weighted by how many shapes use it (SVG has no pixel area)."""
    text = path.read_text(errors="ignore")
    counts = {}
    attr = re.compile(r"""(?:fill|stroke|stop-color|flood-color)\s*[:=]\s*["']?\s*(#[0-9a-fA-F]{3,6}\b|rgb\([^)]*\)|[a-zA-Z]+)""")
    for m in attr.finditer(text):
        v = m.group(1).strip().lower()
        rgb = None
        if v.startswith("#") and len(v) in (4, 7):
            rgb = hex_to_rgb(v)
        elif v.startswith("rgb("):
            nums = re.findall(r"[\d.]+%?", v)[:3]
            if len(nums) == 3:
                rgb = tuple(round(float(n[:-1]) * 2.55) if n.endswith("%") else round(float(n)) for n in nums)
        elif v in NAMED:
            rgb = NAMED[v]
        if rgb:
            counts[rgb] = counts.get(rgb, 0) + 1
    return [(rgb, n) for rgb, n in counts.items()], "SVG: ranked by how many shapes use each colour, not by area"


def read_png(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    pos, idat, plte, trns, ihdr = 8, b"", None, None, None
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            plte = body
        elif kind == b"tRNS":
            trns = body
        elif kind == b"IDAT":
            idat += body
        elif kind == b"IEND":
            break
    w, h, depth, ctype, _, _, interlace = ihdr
    if interlace:
        raise ValueError("interlaced PNG: save it without interlacing, or install Pillow")
    if w * h > MAX_PIXELS:
        raise ValueError(f"image is {w}x{h}: too large for the built-in reader, export a smaller PNG (for example 512 px wide) or install Pillow")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    bits = depth * channels
    stride = (w * bits + 7) // 8
    bpp = max(1, bits // 8)
    raw = zlib.decompress(idat)
    rows, prev = [], bytearray(stride)
    for y in range(h):
        f = raw[y * (stride + 1)]
        cur = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        if f == 1:
            for i in range(bpp, stride):
                cur[i] = (cur[i] + cur[i - bpp]) & 255
        elif f == 2:
            for i in range(stride):
                cur[i] = (cur[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                cur[i] = (cur[i] + (((cur[i - bpp] if i >= bpp else 0) + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = cur[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                cur[i] = (cur[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(cur)
        prev = cur
    step = max(1, int((w * h / 250_000) ** 0.5))   # sample at most about 250,000 pixels
    out = {}
    for y in range(0, h, step):
        row = rows[y]
        for x in range(0, w, step):
            if depth == 8:
                if ctype == 6:
                    r, g, b, a = row[x * 4:x * 4 + 4]
                elif ctype == 2:
                    r, g, b = row[x * 3:x * 3 + 3]; a = 255
                elif ctype == 0:
                    r = g = b = row[x]; a = 255
                elif ctype == 4:
                    r = g = b = row[x * 2]; a = row[x * 2 + 1]
                else:
                    i = row[x]; r, g, b = plte[i * 3:i * 3 + 3]; a = trns[i] if trns and i < len(trns) else 255
            elif depth == 16:
                if ctype == 6:
                    r, g, b, a = row[x * 8], row[x * 8 + 2], row[x * 8 + 4], row[x * 8 + 6]
                elif ctype == 2:
                    r, g, b = row[x * 6], row[x * 6 + 2], row[x * 6 + 4]; a = 255
                elif ctype == 0:
                    r = g = b = row[x * 2]; a = 255
                else:
                    r = g = b = row[x * 4]; a = row[x * 4 + 2]
            else:   # palette or grey at 1, 2 or 4 bits
                per = 8 // depth
                v = (row[x // per] >> (8 - depth * (x % per + 1))) & ((1 << depth) - 1)
                if ctype == 3:
                    r, g, b = plte[v * 3:v * 3 + 3]; a = trns[v] if trns and v < len(trns) else 255
                else:
                    r = g = b = v * 255 // ((1 << depth) - 1); a = 255
            if a < 128:
                continue
            out[(r, g, b)] = out.get((r, g, b), 0) + 1
    return list(out.items()), f"PNG {w}x{h}: ranked by area"


def read_with_pillow(path):
    try:
        from PIL import Image
    except ImportError:
        raise ValueError(f"{path.suffix} needs the Pillow package (pip install pillow). Without it, ask the user for a PNG or SVG of the logo, or for the colour codes")
    im = Image.open(path).convert("RGBA")
    im.thumbnail((500, 500))
    out = {}
    for r, g, b, a in im.getdata():
        if a >= 128:
            out[(r, g, b)] = out.get((r, g, b), 0) + 1
    return list(out.items()), f"{path.suffix.upper().lstrip('.')} via Pillow: ranked by area (compression blur can add a few off-shades)"


def read_logo(path):
    ext = path.suffix.lower()
    if ext == ".svg":
        return read_svg(path)
    if ext == ".png":
        try:
            return read_png(path)
        except ValueError as e:
            if "interlaced" in str(e) or "too large" in str(e):
                try:
                    return read_with_pillow(path)
                except ValueError:
                    pass
            raise
    if ext not in (".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"):
        raise ValueError(f"unsupported file type '{ext}': give a PNG or SVG of the logo")
    return read_with_pillow(path)


# ------------------------------------------------------------------ analysis
def hls(rgb):
    return colorsys.rgb_to_hls(*(v / 255 for v in rgb))


def luminance(rgb):
    c = [v / 255 for v in rgb]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast_white(rgb):
    return 1.05 / (luminance(rgb) + 0.05)


def to_hex(rgb):
    return "#%02x%02x%02x" % tuple(round(v) for v in rgb)


def cluster(colours):
    """merge similar colours (compression blur, anti-aliasing) into groups; each group is weighted by its pixel count."""
    groups = []   # [sum_r, sum_g, sum_b, count, centre]
    for rgb, n in sorted(colours, key=lambda c: -c[1]):
        for g in groups:
            if sum((a - b) ** 2 for a, b in zip(rgb, g[4])) < 40 ** 2:
                for i in range(3):
                    g[i] += rgb[i] * n
                g[3] += n
                break
        else:
            groups.append([rgb[0] * n, rgb[1] * n, rgb[2] * n, n, rgb])
    return [(tuple(g[i] / g[3] for i in range(3)), g[3]) for g in groups]


def analyse(colours):
    clusters = cluster(colours)
    chromatic, neutrals, background = [], [], 0
    for rgb, n in clusters:
        h, l, s = hls(rgb)
        if l > 0.93:
            background += n   # white or near-white (even slightly tinted by anti-aliasing): the logo's background, not a brand colour
        elif s >= 0.25 and 0.10 <= l <= 0.90:
            chromatic.append((rgb, n))
        else:
            neutrals.append((rgb, n))
    total = sum(n for _, n in chromatic) + sum(n for _, n in neutrals) or 1
    # drop tiny clusters: the blended shades along edges (anti-aliasing, JPEG blur) are not brand colours
    chromatic = [c for c in chromatic if c[1] / total >= 0.03]
    neutrals = [c for c in neutrals if c[1] / total >= 0.03]
    chromatic.sort(key=lambda c: -c[1])
    neutrals.sort(key=lambda c: -c[1])
    return chromatic, neutrals, total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 1
    path = Path(args[0])
    if not path.exists():
        print(f"ERROR: {path} does not exist")
        return 1
    try:
        colours, how = read_logo(path)
    except (ValueError, OSError, zlib.error, KeyError, IndexError, struct.error) as e:
        print(f"ERROR: could not read the logo: {e}")
        print("Ask the user for a PNG or SVG file of the logo, or for the brand colour codes.")
        return 1
    chromatic, neutrals, total = analyse(colours)
    result = {"source": how, "brand_candidates": [], "neutrals": []}
    for rgb, n in chromatic[:6]:
        h, l, s = hls(rgb)
        result["brand_candidates"].append({"hex": to_hex(rgb), "share": round(100 * n / total), "hue": round(h * 360),
                                           "white_text_contrast": round(contrast_white(rgb), 2)})
    for rgb, n in neutrals[:3]:
        result["neutrals"].append({"hex": to_hex(rgb), "share": round(100 * n / total), "lightness": round(hls(rgb)[1] * 100)})
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
        return 0 if chromatic else 2

    print(f"Logo: {path.name}  ({how})\n")
    if not chromatic:
        print("No brand colour found: the logo is black, white or grey only.")
        for nb in result["neutrals"]:
            print(f"  neutral {nb['hex']}  {nb['share']}%")
        print("\nA colourless logo gives no brand colour to theme with. Ask the user for the client's brand colour codes.")
        return 2
    print("Brand colour candidates (most prominent first):")
    for i, c in enumerate(result["brand_candidates"], 1):
        ok = "carries white text" if c["white_text_contrast"] >= 4.5 else "too light for white text: usable as an accent or tint, darken it to use as the primary"
        print(f"  {i}. {c['hex']}  {c['share']:>3}% of the logo  white-text contrast {c['white_text_contrast']}:1  ({ok})")
    if result["neutrals"]:
        print("Neutrals in the logo (usually the wordmark or text):")
        for nb in result["neutrals"]:
            print(f"  {nb['hex']}  {nb['share']}%")
    cands = result["brand_candidates"]
    primary = next((c for c in cands if c["white_text_contrast"] >= 4.5), cands[0])
    others = [c for c in cands if c is not primary and min(abs(c["hue"] - primary["hue"]), 360 - abs(c["hue"] - primary["hue"])) >= 25]
    # the secondary colour carries white text (active navigation item), so only a colour that passes can be the secondary;
    # every other logo colour becomes an extra client colour
    secondary = next((c for c in others if c["white_text_contrast"] >= 4.5), None)
    extras = [c for c in cands if c is not primary and c is not secondary][:3]
    cmd = f'python3 {Path(__file__).resolve().parent / "make_theme.py"} --primary "{primary["hex"]}"'
    if secondary:
        cmd += f' --secondary "{secondary["hex"]}"'
    for j, c in enumerate(extras, 1):
        cmd += f' --extra accent{j}="{c["hex"]}"'
    cmd += " --css app-tokens.css"
    print(f"\nSuggested starting point: {cmd}")
    print("CONFIRM WITH THE USER before you run it (THM-10): the most prominent colour is not always the brand colour, and a logo can use "
          "colours that are not meant for the interface. Add --adjust if the primary must be darkened to carry white text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
