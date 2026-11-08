#!/usr/bin/env python3
"""Capture live-site evidence for a dark-pattern audit (needs Playwright + network access).

Setup (first time):
  pip install playwright && playwright install chromium

Single pages:
  python capture_site.py --url https://shop.example/p/1 --url https://shop.example/cart --out capture/ --device mobile

A journey (clicks through a flow and snapshots where you ask):
  python capture_site.py --steps journey.json --out capture/ --device desktop

journey.json:
  {
    "steps": [
      {"goto": "https://shop.example/p/1"},
      {"snap": "product"},
      {"click": "text=Add to cart"},           # any Playwright selector
      {"wait": 1500},                           # milliseconds
      {"goto": "https://shop.example/cart"},
      {"snap": "cart"},
      {"fill": ["#email", "audit-test@example.com"]},
      {"click": "button:has-text('Continue')"},
      {"snap": "checkout-review"}
    ]
  }

SAFETY: never script a payment, an order, a paid-trial start or real personal data.
Stop at the final review / payment-method screen.

Output (in --out):
  NN-name.jpg   full-page screenshot
  NN-name.html  rendered DOM after JavaScript
  signals.json  live signals per snapshot, with element boxes as % of the page:
                checked-by-default inputs, ticking timers, overlays, buttons with
                colours/contrast, plus a fresh-session timer reset check
  Then run scan_signals.py on the folder for text leads.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright is not installed. Run: pip install playwright && playwright install chromium")

LIVE_JS = r"""
() => {
  const W = Math.max(document.documentElement.scrollWidth, document.body ? document.body.scrollWidth : 0, 1);
  const H = Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0, 1);
  const box = el => { const r = el.getBoundingClientRect();
    return {x: +((r.left + scrollX) / W * 100).toFixed(2), y: +((r.top + scrollY) / H * 100).toFixed(2),
            w: +(r.width / W * 100).toFixed(2), h: +(r.height / H * 100).toFixed(2)}; };
  const visible = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const labelOf = el => {
    if (el.id) { const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`); if (l) return l.innerText.trim(); }
    const p = el.closest('label'); if (p) return p.innerText.trim();
    if (el.getAttribute('aria-label')) return el.getAttribute('aria-label');
    const par = el.parentElement; return par ? par.innerText.trim().slice(0, 160) : '';
  };
  const parseRGB = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(Number); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const effectiveBg = el => { let e = el; while (e) { const c = parseRGB(getComputedStyle(e).backgroundColor);
      if (c && c.a > 0.5) return c; e = e.parentElement; } return {r: 255, g: 255, b: 255, a: 1}; };
  const contrast = el => { const fg = parseRGB(getComputedStyle(el).color); if (!fg) return null;
    const bg = effectiveBg(el); const a = lum(fg), b = lum(bg);
    return +((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)).toFixed(2); };

  const checked = [...document.querySelectorAll('input[type=checkbox], input[type=radio], [role=switch], [aria-checked]')]
    .filter(el => (el.checked === true || el.getAttribute('aria-checked') === 'true'))
    .map(el => ({label: labelOf(el).slice(0, 200), type: el.type || el.getAttribute('role') || 'aria', box: box(el.closest('label') || el), visible: visible(el)}));

  const timerRx = /\b\d{1,2}\s*[:h]\s*\d{2}(\s*[:m]\s*\d{2})?\b/;
  const timers = [];
  document.querySelectorAll('body *').forEach(el => {
    if (el.children.length > 3 || !visible(el)) return;
    const t = (el.innerText || '').trim();
    if (t.length < 60 && timerRx.test(t) && !el.closest('script,style')) {
      if (!timers.some(x => x.el && x.el.contains(el))) timers.push({el, text: t});
    }
  });
  window.__dpTimers = timers.map(t => t.el);

  const overlays = [...document.querySelectorAll('body *')].filter(el => {
    const s = getComputedStyle(el); if (!(s.position === 'fixed' || s.position === 'sticky') || !visible(el)) return false;
    const r = el.getBoundingClientRect(); return (r.width * r.height) > (innerWidth * innerHeight * 0.12);
  }).slice(0, 10).map(el => ({text: (el.innerText || '').trim().slice(0, 300), box: box(el), position: getComputedStyle(el).position}));

  const buttons = [...document.querySelectorAll('button, a, [role=button], input[type=submit], input[type=button]')]
    .filter(visible).map(el => { const s = getComputedStyle(el); const t = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim();
      return {text: t.slice(0, 80), color: s.color, background: s.backgroundColor, fontSize: s.fontSize, fontWeight: s.fontWeight,
              contrast: contrast(el), box: box(el)}; })
    .filter(b => b.text).slice(0, 120);

  return {url: location.href, title: document.title, page: {width: W, height: H},
          checked, timers: timers.map(t => ({text: t.text, box: box(t.el)})), overlays, buttons};
}
"""

REREAD_TIMERS_JS = "() => (window.__dpTimers || []).map(el => (el.innerText || '').trim())"


def to_seconds(text):
    m = re.search(r"(\d{1,2})\s*[:h]\s*(\d{2})(?:\s*[:m]\s*(\d{2}))?", text)
    if not m:
        return None
    a, b, c = m.group(1), m.group(2), m.group(3)
    return int(a) * 3600 + int(b) * 60 + int(c) if c else int(a) * 60 + int(b)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "page"


def new_context(browser, device, playwright):
    if device == "mobile":
        return browser.new_context(**playwright.devices["iPhone 13"], locale="en-IN")
    return browser.new_context(viewport={"width": 1366, "height": 900}, locale="en-IN")


def snapshot(page, out, idx, name, results):
    base = f"{idx:02d}-{slug(name)}"
    page.wait_for_timeout(1200)
    page.screenshot(path=str(out / f"{base}.jpg"), full_page=True, type="jpeg", quality=70)
    (out / f"{base}.html").write_text(page.content(), encoding="utf-8")
    data = page.evaluate(LIVE_JS)
    first = [t["text"] for t in data["timers"]]
    if first:
        page.wait_for_timeout(3000)
        second = page.evaluate(REREAD_TIMERS_JS)
        for t, a, b in zip(data["timers"], first, second):
            t["ticking"] = a != b
            t["seconds_at_capture"] = to_seconds(a)
    data.update({"name": name, "screenshot": f"{base}.jpg", "dom": f"{base}.html"})
    results.append(data)
    print(f"  snapped {base}: {len(data['checked'])} checked, {len(data['timers'])} timers, {len(data['overlays'])} overlays")


def reset_check(browser, device, playwright, results):
    """Reload pages with ticking timers in a fresh context; a countdown that is not lower = restarts per session."""
    for r in results:
        ticking = [t for t in r.get("timers", []) if t.get("ticking") and t.get("seconds_at_capture")]
        if not ticking:
            continue
        time.sleep(5)
        ctx = new_context(browser, device, playwright)
        pg = ctx.new_page()
        try:
            pg.goto(r["url"], wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(1500)
            pg.evaluate(LIVE_JS)
            fresh = [to_seconds(x) for x in pg.evaluate(REREAD_TIMERS_JS)]
            for t in ticking:
                later = [s for s in fresh if s is not None]
                t["fresh_session_seconds"] = later[0] if later else None
                if later and later[0] >= t["seconds_at_capture"]:
                    t["resets_in_fresh_session"] = True
        except Exception as e:  # keep going; note the failure
            r.setdefault("errors", []).append(f"reset check failed: {e}")
        finally:
            ctx.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", action="append", default=[], help="page to snapshot (repeatable)")
    ap.add_argument("--steps", help="journey JSON file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", choices=["mobile", "desktop"], default="desktop")
    ap.add_argument("--no-reset-check", action="store_true")
    args = ap.parse_args()
    if not args.url and not args.steps:
        ap.error("give --url or --steps")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    steps = []
    for u in args.url:
        steps += [{"goto": u}, {"snap": slug(u.split('//')[-1])}]
    if args.steps:
        steps += json.loads(Path(args.steps).read_text())["steps"]

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = new_context(browser, args.device, p)
        page = ctx.new_page()
        idx = 1
        skip_until_goto = False
        for st in steps:
            if skip_until_goto and "goto" not in st:
                print(f"  skipping {st} (previous navigation failed)", file=sys.stderr)
                continue
            try:
                if "goto" in st:
                    skip_until_goto = False
                    print(f"goto {st['goto']}")
                    page.goto(st["goto"], wait_until="networkidle", timeout=45000)
                elif "click" in st:
                    page.click(st["click"], timeout=15000)
                elif "fill" in st:
                    page.fill(st["fill"][0], st["fill"][1], timeout=15000)
                elif "wait" in st:
                    page.wait_for_timeout(int(st["wait"]))
                elif "snap" in st:
                    snapshot(page, out, idx, st["snap"], results)
                    idx += 1
            except Exception as e:
                print(f"  step {st} failed: {e}", file=sys.stderr)
                results.append({"step": st, "error": str(e).splitlines()[0]})
                if "goto" in st:
                    skip_until_goto = True
        if not args.no_reset_check:
            reset_check(browser, args.device, p, [r for r in results if "url" in r])
        browser.close()

    (out / "signals.json").write_text(json.dumps({"device": args.device, "snapshots": results}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out/'signals.json'}. Next: python scan_signals.py {out}")


if __name__ == "__main__":
    main()
