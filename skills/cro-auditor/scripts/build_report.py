#!/usr/bin/env python3
"""Validate a CRO audit JSON (v2: mobile + desktop) and render the self-contained report.

Usage
  python build_report.py audit.json --check
  python build_report.py audit.json --out /mnt/user-data/outputs/cro-audit-<brand>-<date>.html [--assets DIR] [--force]

Only the user's screenshots (before views) and the brand logo may be images. Product imagery in the
proposal must be `.ph` placeholders described in `image_plan`. Images are referenced as "asset:<file>"
and inlined as data URIs.
"""
import argparse, base64, io, json, os, re, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "report-template.html")
LAYERS = {"structure", "copy", "design"}
KINDS = {"added", "moved", "reformatted", "removed", "restyled"}
STATUSES = {"pass", "partial", "fail", "na"}
DEVICES = ("mobile", "desktop")


ICONS = {
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "search": '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
 "bag": '<path d="M6 8h12l-1 12H7L6 8z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
 "user": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c1.2-3.5 4-5 7-5s5.8 1.5 7 5"/>',
 "heart": '<path d="M12 20s-7-4.3-7-9.6A3.9 3.9 0 0 1 12 8a3.9 3.9 0 0 1 7 2.4C19 15.7 12 20 12 20z"/>',
 "chevron-left": '<path d="M15 6l-6 6 6 6"/>', "chevron-right": '<path d="M9 6l6 6-6 6"/>',
 "chevron-down": '<path d="M6 9l6 6 6-6"/>', "plus": '<path d="M12 5v14M5 12h14"/>', "minus": '<path d="M5 12h14"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>', "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
 "flask": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 15h9"/>',
 "layers": '<path d="M12 4l9 5-9 5-9-5 9-5z"/><path d="M3 14l9 5 9-5"/>',
 "tag": '<path d="M3 12V4h8l9 9-8 8-9-9z"/><circle cx="7.5" cy="8" r="1.3"/>',
 "truck": '<path d="M2 6h11v10H2zM13 10h4l4 3.5V16h-8"/><circle cx="6" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/>', "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 "wind": '<path d="M3 9h11a3 3 0 1 0-3-3M3 13h15a3 3 0 1 1-3 3M3 17h7"/>',
 "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
 "gift": '<path d="M4 10h16v4H4zM5.5 14h13v7h-13zM12 10v11"/><path d="M12 10c-1.8-3.7-6-3.7-6-1.2S10.2 10 12 10zM12 10c1.8-3.7 6-3.7 6-1.2S13.8 10 12 10z"/>',
 "shield": '<path d="M12 3l7 3v5.5c0 4.5-3 7.8-7 9.5-4-1.7-7-5-7-9.5V6z"/>',
 "box": '<path d="M3.5 7.5L12 3l8.5 4.5v9L12 21l-8.5-4.5z"/><path d="M3.5 7.5L12 12l8.5-4.5M12 12v9"/>',
 "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5M12 8h.01"/>',
 "image": '<rect x="3.5" y="4.5" width="17" height="15" rx="1.5"/><circle cx="9" cy="10" r="1.6"/><path d="M20.5 16l-5-5-8 8.5"/>',
 "star": ('f', '<path d="M12 3.2l2.7 5.6 6.1.8-4.5 4.2 1.1 6-5.4-2.9-5.4 2.9 1.1-6-4.5-4.2 6.1-.8z"/>'),
 "play": ('f', '<path d="M8 5.5v13l10.5-6.5z"/>'),
}


def expand_icons(html, E):
    def rep(m):
        name, extra = m.group(1), (m.group(2) or "").strip()
        v = ICONS.get(name)
        if v is None:
            E.append(f"unknown icon '{name}' (available: {', '.join(sorted(ICONS))})"); return ""
        fill, paths = (v if isinstance(v, tuple) else ("", v))
        cls = "i" + (" f" if fill else "") + (" " + extra if extra else "")
        return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{paths}</svg>'
    return re.sub(r'<i data-icon="([a-z\-]+)"(?:\s+class="([^"]*)")?\s*></i>', rep, html or "")


def _lum(h):
    h = h.strip().lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h): return None
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    if la is None or lb is None: return None
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def encode(path, max_w):
    if path.lower().endswith(".svg"):
        return "data:image/svg+xml;base64," + base64.b64encode(open(path, "rb").read()).decode()
    im = Image.open(path)
    alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    if im.size[0] > max_w:
        im = im.resize((max_w, round(im.size[1] * max_w / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    if alpha:
        im.save(buf, "PNG", optimize=True); mime = "image/png"
    else:
        im.convert("RGB").save(buf, "JPEG", quality=80, optimize=True); mime = "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()


def css_rules(css):
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        yield m.group(1).strip(), m.group(2)


def validate(D):
    E, W = [], []
    meta = D.get("meta", {})
    for k in ("brand", "page_title", "verdict"):
        if not meta.get(k): E.append(f"meta.{k} is missing")

    tok = D.get("brand", {}).get("tokens", {})
    for k in ("bg", "ink", "cta", "on-cta", "f-display", "f-body"):
        if k not in tok: E.append(f"brand.tokens.{k} is missing")
    r = contrast(tok.get("cta", ""), tok.get("on-cta", "#ffffff"))
    if r is not None and r < 4.5:
        E.append(f"CTA text contrast {r:.2f}:1 is below WCAG AA 4.5:1")
    r = contrast(tok.get("ink", ""), tok.get("bg", ""))
    if r is not None and r < 4.5:
        E.append(f"Body text contrast {r:.2f}:1 is below 4.5:1")
    for link in D.get("brand", {}).get("font_links", []):
        if not link.startswith("https://fonts.googleapis.com/"):
            E.append(f"font link not allowed (only fonts.googleapis.com works when published): {link}")

    A = D.get("after", {})
    all_css = A.get("css", "") + "".join(A.get(d, {}).get("css", "") for d in DEVICES)
    leaks = sorted({sel[:60] for sel, body in css_rules(all_css) if "var(--cta)" in body and "cta" not in sel.lower() and "buy" not in sel.lower()})
    if leaks:
        W.append("CTA colour used outside CTA selectors (keep it scarce): " + " | ".join(leaks[:6]))
    if re.search(r"url\(\s*['\"]?https?://", all_css):
        E.append("CSS references remote files")

    html = {}
    for d in DEVICES:
        h = A.get(d, {}).get("html", "")
        html[d] = h
        if not h.strip():
            E.append(f"after.{d}.html is empty: every audit renders both a mobile and a desktop proposal")
        if re.search(r"<script", h, re.I): E.append(f"after.{d}.html must not contain <script>")
        if re.search(r"""(src|href)\s*=\s*["']https?://""", h): E.append(f"after.{d}.html references remote files")
        for m in re.finditer(r"<img\b[^>]*>", h, re.I):
            if not re.search(r'class\s*=\s*"[^"]*\blogo\b', m.group(0)):
                E.append(f"after.{d}.html has an <img> that isn't the logo. Product imagery must be .ph placeholders with an image_plan entry: {m.group(0)[:70]}")

    B = D.get("before", {})
    have = [d for d in DEVICES if B.get(d, {}).get("screenshots")]
    if not have:
        E.append("before has no screenshots for either device")
    for d in DEVICES:
        if d not in have and not B.get(d, {}).get("note"):
            W.append(f"no {d} screenshots: the workflow asks the user for them first; if they declined, set before.{d}.note explaining why")
        for s in B.get(d, {}).get("screenshots", []):
            if not s.get("src", "").startswith(("asset:", "data:")):
                E.append(f"before.{d} screenshot src must be asset:<file>")

    changes = D.get("changes", [])
    ids = [c.get("id") for c in changes]
    if len(ids) != len(set(ids)): E.append("change ids must be unique")
    if len(changes) < 6: W.append(f"only {len(changes)} changes; a full audit usually has 10–18")
    if len(changes) > 22: W.append(f"{len(changes)} changes; move lower-priority ideas into next_tests")
    ids_in = {d: set() for d in DEVICES}
    for d in DEVICES:
        for m in re.finditer(r'data-change\s*=\s*"([^"]+)"', html[d]):
            ids_in[d].update(m.group(1).split())
    marked = {m.get("change") for d in DEVICES for m in B.get(d, {}).get("markers", []) if m.get("change")}
    for c in changes:
        cid = c.get("id", "?")
        for k in ("title", "what", "why", "zone", "metric"):
            if not c.get(k): E.append(f"{cid}: '{k}' is missing")
        if c.get("layer") not in LAYERS: E.append(f"{cid}: layer must be one of {sorted(LAYERS)}")
        if c.get("kind") not in KINDS: E.append(f"{cid}: kind must be one of {sorted(KINDS)}")
        devs = c.get("devices") or list(DEVICES)
        if c.get("kind") == "removed":
            if cid not in marked: W.append(f"{cid}: removed element has no before marker, so it can't be shown")
            continue
        for d in devs:
            if cid not in ids_in[d]:
                E.append(f"{cid}: no element in after.{d}.html carries data-change=\"{cid}\" (set devices if it only applies to one)")
    for d in DEVICES:
        for x in ids_in[d] - set(ids): W.append(f"after.{d}.html has data-change=\"{x}\" with no change entry")

    n_ph = sum(len(re.findall(r'class="[^"]*\bph\b', html[d])) for d in DEVICES)
    plan = D.get("image_plan", [])
    if n_ph and not plan: E.append(f"{n_ph} image placeholders but image_plan is empty")
    if plan and len(plan) < 3: W.append("image_plan has fewer than 3 shots; most PDP galleries need 5–7")
    for p in plan:
        for k in ("n", "slot", "show", "why"):
            if not p.get(k): E.append(f"image_plan entry {p.get('n','?')}: '{k}' is missing")
    if any("needs-input" in html[d] for d in DEVICES) and not D.get("needs_input"):
        E.append("placeholders marked needs-input but needs_input is empty")
    for row in D.get("scorecard", []) + D.get("checks", []):
        for k in ("before", "after"):
            if row.get(k) not in STATUSES: E.append(f"'{row.get('question') or row.get('check')}': {k} must be one of {sorted(STATUSES)}")
    if not D.get("scorecard"): W.append("scorecard is empty")
    if not D.get("design_plan"): W.append("design_plan is missing: record the direction, type and token choices (see render-design.md)")
    return E, W


def inline(D, dirs, E):
    def find(name):
        for d in dirs:
            p = os.path.join(d, name)
            if os.path.isfile(p): return p
        return None
    cache = {}
    def res(name, w):
        if (name, w) not in cache:
            p = find(name)
            if not p: E.append(f"asset not found: {name}"); cache[(name, w)] = ""
            else: cache[(name, w)] = encode(p, w)
        return cache[(name, w)]
    for d, w in (("mobile", 1000), ("desktop", 1700)):
        for s in D.get("before", {}).get(d, {}).get("screenshots", []):
            if s.get("src", "").startswith("asset:"): s["src"] = res(s["src"][6:], w)
    A = D.get("after", {})
    sub = lambda t: re.sub(r"asset:([A-Za-z0-9._\-/]+)", lambda m: res(m.group(1), 600), t or "")
    A["css"] = sub(A.get("css", ""))
    for d in DEVICES:
        if d in A:
            A[d]["html"] = sub(A[d].get("html", "")); A[d]["css"] = sub(A[d].get("css", ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audit"); ap.add_argument("--out"); ap.add_argument("--assets")
    ap.add_argument("--check", action="store_true"); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    D = json.load(open(a.audit))
    base = os.path.dirname(os.path.abspath(a.audit))
    pre = []
    for d in DEVICES:
        if d in D.get("after", {}):
            D["after"][d]["html"] = expand_icons(D["after"][d].get("html", ""), pre)
    E, W = validate(D)
    E = pre + E
    ch = D.get("changes", [])
    print(f"Changes: {len(ch)}  " + "  ".join(f"{l}: {sum(1 for c in ch if c.get('layer')==l)}" for l in ("structure", "copy", "design"))
          + f"   Image plan: {len(D.get('image_plan', []))}   Needs input: {len(D.get('needs_input', []))}")
    for e in E: print("ERROR  ", e)
    for w in W: print("WARNING", w)
    if a.check and not a.out: sys.exit(1 if E else 0)
    if not a.out: print("pass --out to render"); sys.exit(1)
    inline(D, [x for x in [a.assets, base, os.path.join(base, "assets")] if x], E)
    if E and not a.force:
        print(f"\n{len(E)} error(s); fix them or pass --force"); sys.exit(1)
    tpl = open(TEMPLATE, encoding="utf-8").read()
    meta = D.get("meta", {})
    links = "".join(f'<link rel="stylesheet" href="{l}">' for l in D.get("brand", {}).get("font_links", []))
    out = (tpl.replace("__TITLE__", f"CRO audit: {meta.get('brand','')} – {meta.get('page_title','')}".replace("<", "&lt;"))
              .replace("<!--__FONT_LINKS__-->", links)
              .replace("/*__AUDIT_JSON__*/", json.dumps(D, ensure_ascii=False).replace("<", "\\u003c")))
    open(a.out, "w", encoding="utf-8").write(out)
    mb = os.path.getsize(a.out) / 1e6
    print(f"\nwrote {a.out} ({mb:.1f} MB)")
    if mb > 16: print("ERROR   over the 16 MB publish limit")


if __name__ == "__main__":
    main()
