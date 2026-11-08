#!/usr/bin/env python3
"""Screenshot every view of a built CRO report and both proposals at true size, for visual QA.

Usage
  python qa_render.py REPORT.html OUTDIR [--fonts DIR]

--fonts DIR: a folder of .woff2 files (for example from `npm install @fontsource/<family>`) to inject
as @font-face, because sandboxes often can't reach Google Fonts. File names must start with the
family slug (archivo-..., hanken-grotesk-...); weight is read from the name. Variable files ('-wdth-'
or '-wght-') are registered with the full weight and width range.
Prints where the add-to-cart lands, in screens, on each device.
"""
import argparse, base64, glob, os, re
from playwright.sync_api import sync_playwright


def font_css(d):
    css = ""
    for p in sorted(glob.glob(os.path.join(d, "**", "*.woff2"), recursive=True)):
        n = os.path.basename(p)
        if "italic" in n or "latin-ext" in n or not "-latin-" in n:
            continue
        fam = n.split("-latin-")[0].replace("-", " ").title()
        m = re.search(r"-(\d{3})-normal", n)
        w = m.group(1) if m else "100 900"
        st = "62% 125%" if ("-wdth-" in n or "-full-" in n) else "100%"
        b = base64.b64encode(open(p, "rb").read()).decode()
        css += f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b}) format('woff2');font-weight:{w};font-stretch:{st};}}"
    return css


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("report"); ap.add_argument("outdir"); ap.add_argument("--fonts")
    a = ap.parse_args(); os.makedirs(a.outdir, exist_ok=True)
    css = font_css(a.fonts) if a.fonts else ""
    html = open(a.report, encoding="utf-8").read().replace("</head>", "<style>" + css + "</style></head>")
    tmp = os.path.join(a.outdir, "_qa.html"); open(tmp, "w", encoding="utf-8").write(html)
    o = lambda n: os.path.join(a.outdir, n)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 960})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + os.path.abspath(tmp)); pg.wait_for_timeout(900)
        pg.click("button[data-dev=mobile]"); pg.wait_for_timeout(300); pg.screenshot(path=o("mobile-after.png"))
        pg.click("#hl"); pg.wait_for_timeout(300); pg.click("[data-v=compare]"); pg.wait_for_timeout(400); pg.screenshot(path=o("mobile-compare-hl.png"))
        pg.click("button[data-dev=desktop]"); pg.wait_for_timeout(600); pg.screenshot(path=o("desktop-compare-hl.png"))
        pg.click("#hl"); pg.click("[data-v=after]"); pg.wait_for_timeout(500); pg.screenshot(path=o("desktop-after.png"))
        pg.click("#sumBtn"); pg.wait_for_timeout(400); pg.screenshot(path=o("summary.png"), full_page=True)
        for dev, host, w, vh in (("mobile", "hostAm", 390, 844), ("desktop", "hostAd", 1280, 900)):
            inner = pg.evaluate(f"()=>{{const sr=document.getElementById('{host}').shadowRoot;return '<style>'+sr.querySelector('style').textContent+'</style>'+sr.querySelector('.proto').outerHTML}}")
            q = b.new_page(viewport={"width": w, "height": vh})
            q.set_content("<html><head><style>" + css + "body{margin:0}</style></head><body>" + inner + "</body></html>"); q.wait_for_timeout(600)
            top = q.evaluate("()=>{const c=document.querySelector('.cta');return c?c.getBoundingClientRect().top:null}")
            print(f"{dev}: add-to-cart at {top:.0f}px = {top/vh:.2f} screens" if top is not None else f"{dev}: no .cta element found")
            q.screenshot(path=o(f"{dev}-full.png"), full_page=True)
        print("page errors:", errs or "none"); b.close()
    os.remove(tmp)


if __name__ == "__main__":
    main()
