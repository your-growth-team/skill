# Report format and build

The deliverable is one self-contained HTML report:
- a **Mobile / Desktop** device switch;
- **Before / After / Compare** views;
- a **Highlight changes** switch that outlines and numbers every change on both devices;
- a change panel with what, why and the metric for each change;
- a printable **Summary** with the readiness scorecard, every change, the image brief, measurable checks, brand inputs, data requests, next tests and limitations.

You write `audit.json`; the builder validates it and renders the report.

## Contents
1. Folder layout
2. Before screenshots and markers
3. audit.json reference
4. Build, check, QA, deliver

---

## 1. Folder layout

```
/home/claude/cro-work/<brand>/
  audit.json
  assets/
    before-m-1.jpg, before-m-2.jpg …   mobile screenshots (browser/status chrome cropped off if needed)
    before-d-1.jpg, before-d-2.jpg …   desktop screenshots
    logo.png                            optional: the brand logo
```

`assets/example/` in this skill holds a complete run (UFF! DESIRED, a fragrance PDP) to copy from.

## 2. Before screenshots and markers

- **Detect devices first:** `python scripts/crop_assets.py devices <screenshots…>`, then confirm by looking.
- **Crop** browser or OS chrome off the top if it isn't part of the page: `crop_assets.py crop spec.json` with `{"src", "box": [x, y, w, h] (%), "out"}`.
- **Mark the problems.** Add markers for every removed element and for the main problem behind moved or reformatted ones: `{"screenshot": 0, "box": [x, y, w, h], "change": "C4", "label": "Countdown disagrees with the cart"}`. Boxes are in % of that screenshot file.
- **Read the boxes off a grid** of the exact file you'll use: `crop_assets.py grid assets/before-d-1.jpg --out grid.png`. Upscale small images first.
- **Verify:** `crop_assets.py markers audit.json --outdir chk`, then view the result. Every box must sit on its element.
- **Missing device:** if the user didn't share one device and chose to proceed anyway, leave that device's `screenshots` empty and set its `note`. The report shows a clear empty state in Before for that device.

## 3. audit.json reference

```json
{
  "meta": {
    "brand": "UFF! Perfumes", "page_title": "DESIRED", "page_url": "uffco.com/products/desired",
    "date": "YYYY-MM-DD", "category": "Fragrance", "market": "India", "price_tier": "₹399–1,299 · blind buy",
    "decision_type": "Sensory purchase", "traffic": "Assumed paid social",
    "verdict": "2–4 sentences: why the page under-converts and what the proposal does about it.",
    "start_device": "mobile"
  },
  "brand": {
    "tokens": {"bg": "#ffffff", "ink": "#141212", "cta": "#141212", "on-cta": "#ffffff",
               "f-display": "'Archivo', sans-serif", "f-body": "'Hanken Grotesk', sans-serif",
               "surface": "#f6f4f1", "brand": "#872824", "ph": "#e8e5e0"},
    "font_links": ["https://fonts.googleapis.com/css2?family=…&display=swap"]
  },
  "design_plan": {"direction": "…", "type": "…", "color": "…", "layout": "…", "checks": "…"},
  "before": {
    "mobile":  {"screenshots": [{"src": "asset:before-m-1.jpg", "caption": "…"}], "markers": [ … ]},
    "desktop": {"screenshots": [{"src": "asset:before-d-1.jpg", "caption": "…"}], "markers": [ … ], "note": "only if screenshots are missing"}
  },
  "after": {
    "css": "shared CSS for both devices, every selector under .proto",
    "mobile":  {"html": "…", "css": "…"},
    "desktop": {"html": "…", "css": "…"}
  },
  "changes": [
    {"id": "C1", "zone": "Announcement bar", "layer": "structure", "kind": "reformatted", "source": "relocated",
     "devices": ["mobile", "desktop"],
     "title": "…", "what": "…", "why": "…", "metric": "AOV", "impact": "Guard: conversion rate", "needs_input": false}
  ],
  "image_plan": [{"n": "1", "slot": "Hero", "show": "…", "overlay": "None", "why": "…"}],
  "scorecard": [{"question": "Fit: is it for me?", "before": "partial", "after": "pass", "note": "…"}],
  "checks": [{"check": "Add-to-cart within the first two mobile screens", "before": "fail", "after": "pass", "note": "…"}],
  "needs_input": [{"item": "…", "why": "…"}],
  "data_requests": ["…"],
  "next_tests": [{"idea": "…", "metric": "…", "why": "…"}],
  "summary": {"measurement": "…", "protected": ["…"], "limitations": ["…"]}
}
```

Field notes:
- **Numbering.** Changes are numbered in array order, so list them top to bottom as they appear on the page. Mobile order wins; desktop-only changes go where they appear.
- **`devices`** defaults to both. Every non-removed change must carry `data-change="C#"` in each device's HTML it applies to. To mark one element with two changes, separate the ids with a space: `data-change="C3 C7"`.
- **`layer`**: structure | copy | design. **`kind`**: added | moved | reformatted | removed | restyled. **`source`**: relocated | reformatted | removed | microcopy | needs-input | brand-supplied | restyled.
- **Statuses** for scorecard and checks: pass | partial | fail | na.
- **The proposal HTML** may contain no `<script>`, no remote URLs, and no `<img>` except the logo (`class="logo"`). Product imagery is `.ph` placeholders, each described in `image_plan`.
- **Icons:** `<i data-icon="name" class="s"></i>` (see `render-design.md` §4).

## 4. Build, check, QA, deliver

```bash
python scripts/build_report.py audit.json --check
python scripts/build_report.py audit.json --out /mnt/user-data/outputs/cro-audit-<brand>-<YYYY-MM-DD>.html
python scripts/qa_render.py /mnt/user-data/outputs/cro-audit-<brand>-<YYYY-MM-DD>.html qa --fonts /tmp/qa-fonts
```

The builder **errors** on:
- a missing device render;
- product `<img>` tags;
- placeholders without an image plan;
- CTA contrast below 4.5:1;
- remote files;
- changes not marked in their device HTML;
- missing required fields.

It **warns** when the CTA colour is used outside CTA selectors, a device's screenshots are missing without a note, or the design plan is missing. Fix every error, and read every warning.

**Deliver:**
- **On claude.ai with the Artifact tool:** publish the HTML. It is self-contained; fonts come from Google Fonts and images are data URIs.
- **Otherwise:** present the file.
