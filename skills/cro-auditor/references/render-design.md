# Designing the proposed page (mobile and desktop)

The prototype is what the client sees first, so it has to look like a page a senior designer at their brand would ship. A generic, kit-styled mockup undermines every recommendation in the audit. This guide turns the two bundled design skills into rules for this job.

## Contents
1. Read the bundled design skills
2. Resolve the tension: distinctive vs. on-brand vs. conventional
3. Write the design plan
4. Tokens and the foundation the template gives you
5. Image placeholders and the image brief
6. Mobile layout pattern
7. Desktop layout pattern
8. Quality bar (check before building, and again from screenshots)
9. Visual QA

---

## 1. Read the bundled design skills

Before writing any proposal HTML, read:
- `bundled/frontend-design/frontend-design.md`: aesthetic direction, typography, colour, spatial composition, and what makes a design read as generic.
- `bundled/ui-ux-pro-max/ui-ux-pro-max.md`: the Quick Reference §1–§7 (accessibility, touch, performance, style, layout and responsive, typography and colour, animation), "Common Rules for Professional UI", and the pre-delivery checklist.

If a full UI/UX Pro Max install with `scripts/search.py` exists in the environment (for example under `/mnt/skills/plugins/ui-ux-pro-max/scripts/`), you may run `--design-system` or `--domain typography` for font-pairing ideas. The bundled copy has the rules only.

## 2. Resolve the tension: distinctive vs. on-brand vs. conventional

The three sources pull in different directions:
- **Frontend Design** says commit to a bold, characterful direction and avoid generic fonts and templates.
- **Brand fidelity** (from `guardrails.md`) says the page must read as the same brand, improved.
- **The CRO playbook** says familiar layouts win for fast purchases.

Resolve it this way:
- **The brand decides** the palette, logo, voice, and the *character* of the type (heavy grotesk, elegant serif, rounded, condensed…).
- **Convention decides** the page structure: the PDP sequence, header pattern, where the gallery, options and button go.
- **Distinctiveness goes into one signature element** derived from the brand: the product-name treatment, a spec bar, a scent pyramid, an ingredient spotlight, a bold price block. Make that element memorable and keep everything around it quiet and disciplined.
- **Typefaces:** pick Google Fonts that match the brand's type character. Avoid the generic defaults (Inter, Roboto, Arial, plain system stacks) unless the brand genuinely uses them. Pair one display face with one body face.
- **Avoid the generic AI looks** named in Frontend Design (purple gradients on white, identical rounded cards everywhere, one radius and one soft shadow on everything, cream plus terracotta by default). Use them only if the brand itself does.

## 3. Write the design plan

Record it in `audit.json` as `design_plan`, before writing HTML:

```json
"design_plan": {
  "direction": "One or two sentences: the aesthetic idea, where brand colour lives, and the signature element.",
  "type": "Display and body faces and their roles; the mobile and desktop type scales; body size on mobile.",
  "color": "Token roles: ink, surface, brand, accent, the CTA colour and why it is reserved.",
  "layout": "Mobile gutters and spacing rhythm; desktop container, grid ratio and gap.",
  "checks": "The quality-bar items you will verify."
}
```

Then review the plan against the brand. If any part would look the same for any other store in the category, change that part.

## 4. Tokens and the foundation the template gives you

Set `brand.tokens` (each becomes a CSS variable on `.proto`). Required: `bg`, `ink`, `cta`, `on-cta`, `f-display`, `f-body`. Add whatever else the design needs (`surface`, `ink-2`, `muted`, `line`, `brand`, `brand-tint`, `accent`, `ph`…). Add Google Fonts stylesheet URLs to `brand.font_links`.

The template gives every render a small foundation, nothing more:
- `.proto` is the root, with a reset (box-sizing, margins, list styles, buttons), so your CSS starts clean. It carries `data-dev="mobile"` or `"desktop"` for device-specific rules.
- `.ph` image placeholders (see §5).
- Icons: write `<i data-icon="name" class="s"></i>` and the builder swaps in an inline SVG from one consistent family (1.6 stroke). Available: menu, search, bag, user, heart, chevron-left, chevron-right, chevron-down, plus, minus, check, arrow-right, sparkle, flask, layers, tag, truck, chat, clock, wind, moon, gift, shield, box, info, image, star (filled), play (filled). Class `s` = 16px. Never use emoji as icons.
- `.needs-input` for inline placeholders the brand must fill.
- The highlight layer for `data-change`.

Everything visual is yours. Write it in `after.css` (shared by both devices) plus `after.mobile.css` and `after.desktop.css`, every selector scoped under `.proto`. See the example in `assets/example/audit.json`.

## 5. Image placeholders and the image brief

Product imagery is never reused or cropped from screenshots. Our job is the page and the brief for the images, not the photography. Every product image, lifestyle shot, comparison card and video in the proposal is a grey placeholder that says what should go there.

```html
<div class="ph"><span class="ph-n">Image 1</span><span class="ph-t">Hero bottle, night mood</span><span class="ph-d">Bottle on a dark backdrop, warm amber rim light</span></div>
<div class="ph mini on"><span class="ph-n">1</span></div>          <!-- thumbnail -->
<div class="ph vid"><span class="ph-n">Video 1</span><i data-icon="play" class="play"></i><span class="ph-t">First-spray reaction</span></div>
```

Control shape with `--ph-ar` (aspect ratio, default 1/1) and colour with `--ph-bg` (or the `ph` token).

Write a matching `image_plan` entry for every numbered image, in gallery order:

```json
{"n": "1", "slot": "Hero", "show": "What the shot is, composition and mood", "overlay": "Any on-image text, or None", "why": "Which shopper doubt it answers"}
```

Plan the gallery from the category module and the shopper's doubts: hero (answers the top doubt), proof or comparison, performance or specs, ingredients or notes, scale, in-use or lifestyle, packaging or gift, and video. Usually 5–7 images plus 2–4 videos. The summary prints the plan as the client's shoot list.

The brand logo may be an image (`<img class="logo" src="asset:logo.png">`), cropped from a screenshot, or a styled wordmark.

## 6. Mobile layout pattern (390 px)

One column, 16px gutters, an 8px spacing rhythm, section gaps of 20–32px. Typical order (follow the audit, not this list blindly):

1. One short announcement bar (36px).
2. Header (56px): menu left, logo centre, search and bag right; 44px tap targets.
3. Title block: identity tag or badges, product name (the display face), one-line descriptor, two-line description, rating, price with value context, tax/legal line.
4. Gallery: main placeholder at ~80% width with a peek of image 2, arrow button, then numbered thumbnails.
5. The signature element (spec bar, scent pyramid…), if it belongs in the decision zone.
6. Options with "Select X: value" labels and tiles; risk-reducing help at the selector.
7. Offers and add-ons, compact.
8. Buy row: quantity inline with one primary button (52px); express checkout as an outlined secondary.
9. Reassurance list under the button.
10. Proof, depth content and question accordions; cross-sell; video row.

Body text 16px; secondary 13–14px; nothing under 12px. The add-to-cart should land within about two screen heights.

## 7. Desktop layout pattern (1280 px)

- Announcement bar; header (72px) with search, logo and icons; a one-line text navigation if the store has one.
- **Main:** a 1200px container, 40px side padding, two columns at roughly 1.1 : 1 with a 48–64px gap.
  - **Left:** the gallery as a grid (hero spanning both columns, then a 2-column grid), all placeholders.
  - **Right:** the buy box (`position: sticky; top: 24px`) carrying the same decision sequence as mobile, with larger type (product name 64–96px if it's the signature element; body 17px).
- **Below:** a two-column section for depth (scent or ingredients card beside the question accordions), then a 4-up video or UGC row, then cross-sell.
- The add-to-cart should be visible in the first screen or close to it.

Desktop is not a stretched mobile page: use the width for side-by-side gallery and decision, and keep line lengths at 60–75 characters.

## 8. Quality bar

From UI/UX Pro Max and Frontend Design, applied to PDPs:

- **Hierarchy** is carried by size, weight and spacing, not colour alone; one type scale per device; tabular figures for prices.
- **One primary CTA** per screen, in a colour used nowhere else on the page, with at least 4.5:1 text contrast. Secondary actions are outlined or text.
- **Touch targets** are at least 44 × 44px, with 8px or more between them.
- **Body text** is at least 16px on mobile, with line-height 1.4–1.6.
- **Contrast** is 4.5:1 for text and 3:1 for large text and UI glyphs.
- **Spacing** follows a consistent 4/8 rhythm, with section spacing in tiers (16 / 24 / 32 / 48 / 72).
- **Consistency:** one icon family and stroke, a small radius scale, and a restrained shadow scale (often none).
- **Placeholders** are clearly placeholders and numbered.
- **Brand:** logo, palette, voice and type character are recognisable at a glance. Brand colour sits on the edges and selected states; the decision zone stays neutral.
- **One signature element**, executed precisely; nothing decorative elsewhere.
- **Interactions:** `details` accordions with an animated chevron (150–300ms, respecting reduced motion), visible selected states that don't rely on colour alone, and no layout shift on state change.

## 9. Visual QA

Always look at the result before delivering:

```bash
python scripts/qa_render.py /mnt/user-data/outputs/<report>.html /home/claude/cro-work/<brand>/qa [--fonts /tmp/qa-fonts]
```

The script saves both proposals at true size (390px and 1280px, full page), the mobile and desktop Compare views with highlights, and the summary. It also prints where the add-to-cart lands in screens.

The sandbox often can't reach Google Fonts, so a render without them is not what the client will see. For accurate QA, fetch the same families from npm and pass the folder:

```bash
mkdir -p /tmp/f && cd /tmp/f && npm init -y >/dev/null && npm install @fontsource/<body-family> @fontsource-variable/<display-family>
mkdir -p /tmp/qa-fonts && cp node_modules/@fontsource*/*/files/*-latin-*normal.woff2 /tmp/qa-fonts/
```

Fontsource packages: https://fontsource.org (npm: https://www.npmjs.com/search?q=%40fontsource).

Then view the images and check:
- the first screen on each device matches the plan;
- the signature element lands;
- the CTA is the strongest thing in its colour;
- nothing overlaps or clips;
- every badge sits on its element;
- placeholders read as a shoot list.

Iterate until it looks like the brand's best page.
