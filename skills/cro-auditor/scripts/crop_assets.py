#!/usr/bin/env python3
"""Asset helpers for the CRO auditor.

Subcommands
  devices IMAGE...                      Guess whether each screenshot is mobile or desktop (confirm by looking).
  info IMAGE...                         Print size of each image.
  grid IMAGE --out OUT [--step 10]      Save a copy with labelled % gridlines, to read crop boxes off visually.
  crop SPEC.json                        Crop regions into asset files (see SPEC format below).
  palette IMAGE [--box X Y W H] [--n 8] Dominant colours (hex, share %) of an image or a % region of it.
  contrast HEX HEX                      WCAG contrast ratio between two colours.
  markers AUDIT.json --outdir DIR       Draw before.<device>.markers onto each before screenshot to verify placement.

Product imagery is never reused in the proposal (it becomes numbered placeholders). Crop only
the before screenshots (to remove browser chrome) and, if wanted, the brand logo.

SPEC.json for `crop` is a list of:
  {"src": "/mnt/user-data/uploads/shot1.png", "box": [x, y, w, h], "unit": "%",
   "out": "assets/hero.png", "max_width": 900}
`box` is left, top, width, height. unit "%" (default) or "px".
"""
import argparse, json, os, sys
from PIL import Image, ImageDraw, ImageFont


def _font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def classify(w, h):
    r = w / h
    if r >= 1.2:
        return "desktop", "landscape viewport"
    if w <= 1440 and r <= 0.75:
        return "mobile", "narrow portrait"
    if w >= 1600:
        return "desktop", "wide full-page capture"
    return "unclear", "check visually"


def cmd_devices(a):
    seen = {"mobile": 0, "desktop": 0, "unclear": 0}
    for p in a.images:
        w, h = Image.open(p).size
        kind, why = classify(w, h)
        seen[kind] += 1
        print(f"{kind:8s} {w}x{h}  ({why})  {p}")
    print(f"\nmobile: {seen['mobile']}  desktop: {seen['desktop']}  unclear: {seen['unclear']}")
    print("Confirm by looking: a status bar, a single column and a hamburger-only header mean mobile;")
    print("a horizontal nav, side-by-side gallery and buy box mean desktop.")
    if seen["mobile"] == 0 or seen["desktop"] == 0:
        missing = "mobile" if seen["mobile"] == 0 else "desktop"
        print(f"MISSING: no {missing} screenshots. Ask the user for {missing} screenshots before auditing.")


def cmd_info(a):
    for p in a.images:
        im = Image.open(p)
        print(f"{p}: {im.size[0]}x{im.size[1]} {im.mode}")


def cmd_grid(a):
    im = Image.open(a.image).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    f = _font(max(12, W // 60))
    step = a.step
    for pct in range(0, 101, step):
        x = round(W * pct / 100); y = round(H * pct / 100)
        col = (255, 0, 90) if pct % 50 == 0 else (0, 140, 255)
        d.line([(x, 0), (x, H)], fill=col, width=1)
        d.line([(0, y), (W, y)], fill=col, width=1)
        d.text((x + 2, 2), str(pct), fill=col, font=f)
        d.text((2, y + 2), str(pct), fill=col, font=f)
    im.save(a.out)
    print(f"grid saved: {a.out} ({W}x{H}); labels are % of width (top) and height (left)")


def _box_px(im, box, unit):
    W, H = im.size
    x, y, w, h = box
    if unit == "%":
        x, y, w, h = W * x / 100, H * y / 100, W * w / 100, H * h / 100
    l, t = max(0, round(x)), max(0, round(y))
    r, b = min(W, round(x + w)), min(H, round(y + h))
    if r <= l or b <= t:
        raise ValueError(f"empty box {box} on {W}x{H}")
    return (l, t, r, b)


def cmd_crop(a):
    spec = json.load(open(a.spec))
    for s in spec:
        im = Image.open(s["src"])
        c = im.crop(_box_px(im, s["box"], s.get("unit", "%")))
        mw = s.get("max_width")
        if mw and c.size[0] > mw:
            c = c.resize((mw, round(c.size[1] * mw / c.size[0])), Image.LANCZOS)
        os.makedirs(os.path.dirname(os.path.abspath(s["out"])), exist_ok=True)
        if s["out"].lower().endswith((".jpg", ".jpeg")):
            c.convert("RGB").save(s["out"], quality=85)
        else:
            c.save(s["out"])
        print(f"{s['out']}: {c.size[0]}x{c.size[1]}")


def _hex(rgb):
    return "#%02x%02x%02x" % rgb


def _lum(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def ratio(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def parse_hex(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cmd_palette(a):
    im = Image.open(a.image).convert("RGB")
    if a.box:
        im = im.crop(_box_px(im, a.box, "%"))
    im.thumbnail((400, 400))
    q = im.quantize(colors=a.n * 2, method=Image.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    shown = 0
    for c, idx in counts:
        rgb = tuple(pal[idx * 3: idx * 3 + 3])
        share = 100 * c / total
        if share < 0.5:
            continue
        print(f"{_hex(rgb)}  {share:5.1f}%   vs white {ratio(rgb,(255,255,255)):4.1f}:1   vs black {ratio(rgb,(0,0,0)):4.1f}:1")
        shown += 1
        if shown >= a.n:
            break


def cmd_contrast(a):
    r = ratio(parse_hex(a.a), parse_hex(a.b))
    verdict = "passes AA (4.5:1)" if r >= 4.5 else ("large text only (3:1)" if r >= 3 else "fails")
    print(f"{a.a} vs {a.b}: {r:.2f}:1 — {verdict}")


def cmd_markers(a):
    D = json.load(open(a.audit))
    base = os.path.dirname(os.path.abspath(a.audit))
    os.makedirs(a.outdir, exist_ok=True)
    for dev in ("mobile", "desktop"):
        b = D.get("before", {}).get(dev, {})
        for i, s in enumerate(b.get("screenshots", [])):
            name = s.get("src", "")[6:] if s.get("src", "").startswith("asset:") else ""
            path = next((p for p in [os.path.join(base, name), os.path.join(base, "assets", name)] if name and os.path.isfile(p)), None)
            if not path:
                print(f"{dev} screenshot {i}: cannot find {s.get('src','')[:40]}"); continue
            im = Image.open(path).convert("RGB"); W, H = im.size; d = ImageDraw.Draw(im); f = _font(max(12, W // 40))
            for m in b.get("markers", []):
                if m.get("screenshot", 0) != i: continue
                x, y, w, h = m["box"]
                d.rectangle([W*x/100, H*y/100, W*(x+w)/100, H*(y+h)/100], outline=(214, 69, 47), width=max(2, W // 500))
                d.text((W*x/100 + 4, H*y/100 + 2), m.get("change", "!"), fill=(214, 69, 47), font=f)
            out = os.path.join(a.outdir, f"markers-{dev}-{i}.png"); im.thumbnail((1600, 1600)); im.save(out); print(out)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("devices"); s.add_argument("images", nargs="+"); s.set_defaults(f=cmd_devices)
    s = sp.add_parser("info"); s.add_argument("images", nargs="+"); s.set_defaults(f=cmd_info)
    s = sp.add_parser("grid"); s.add_argument("image"); s.add_argument("--out", required=True); s.add_argument("--step", type=int, default=10); s.set_defaults(f=cmd_grid)
    s = sp.add_parser("crop"); s.add_argument("spec"); s.set_defaults(f=cmd_crop)
    s = sp.add_parser("palette"); s.add_argument("image"); s.add_argument("--box", type=float, nargs=4); s.add_argument("--n", type=int, default=8); s.set_defaults(f=cmd_palette)
    s = sp.add_parser("markers"); s.add_argument("audit"); s.add_argument("--outdir", required=True); s.set_defaults(f=cmd_markers)
    s = sp.add_parser("contrast"); s.add_argument("a"); s.add_argument("b"); s.set_defaults(f=cmd_contrast)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
