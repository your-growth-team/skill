# Capturing evidence: live websites and Figma files

The audit is only as good as its evidence. Pick the strongest capture mode the environment allows, and record which one you used. The report's method section states it, so readers know what was and wasn't checkable.

## Journeys to cover

Most dark patterns live in a handful of flows. Walk (or find frames for) each flow that exists in the product, and list skipped ones in the report's limitations.

1. Landing and listing pages: banners, timers, badges, sponsored units, pop-ups on entry.
2. Product or service detail page: price display, stock and popularity claims, add-on offers.
3. Cart: items and totals compared with what was chosen; pre-selected extras.
4. Checkout and payment, up to the final review screen: fees, insurance, donations, consents, price changes.
5. Sign-up, login and onboarding: required fields, permissions, bundled consents, forced account creation.
6. Consent surfaces: cookies, notifications, marketing preferences, privacy settings.
7. Free trial and subscription start: payment capture, auto-renew disclosure, renewal price.
8. Renewal and billing: reminders, receipts, billing history.
9. Cancellation, unsubscribe and account deletion: step count, retention screens, decline copy.
10. Exit intent and in-session prompts: app-install nags, re-prompts, exit pop-ups.

## Safety rules for live capture

- Never complete a payment, place an order, start a paid trial, or submit real personal or payment data. Stop at the final review or payment-method screen and capture it.
- Use obviously fake test data only where a field must be filled to proceed (for example a test email), and only on the user's own product or a staging environment.
- Don't download files or click suspicious ads or "scan" prompts. For rogue-malware signals, record the URL and screenshot only.
- Respect logins: audit logged-in areas only with credentials the user provides for their own product.

---

## Website capture modes (best first)

### Mode A: real browser (Claude Code, Cowork, or Claude in Chrome)

Use this when you can run a browser that reaches the site.

- **With `scripts/capture_site.py`** (needs Python and Playwright; network access to the site):

  ```bash
  pip install playwright && playwright install chromium   # first time only
  python scripts/capture_site.py --url https://example.com/product/123 --out capture/ --device mobile
  python scripts/capture_site.py --steps journey.json --out capture/ --device desktop
  ```

  For each step the script saves:
  - a screenshot (`NN-name.jpg`);
  - the rendered DOM (`NN-name.html`);
  - `signals.json`, which contains:
    - elements checked by default, with their bounding boxes as percentages;
    - timer-like text and whether it changed over a few seconds;
    - fixed overlays and modals;
    - urgency, shaming and fee phrases;
    - a reset check that reloads the page in a fresh browser context and compares timer values.

  The `journey.json` format is described at the top of the script. Bounding boxes from `signals.json` can go straight into a finding's `boxes`.

- **With Claude in Chrome or another browser tool**: walk the journeys manually. Screenshot each step. Note which boxes are checked, what each close or decline button does, and whether timers restart in a new tab or private window.

### Mode B: fetch only (claude.ai, where the sandbox can't reach external sites)

`web_fetch` returns the page's text, not its rendered state. It can show:
- copy (urgency, shaming, fee words, "free" claims, ad labels);
- link structure (is there a cancel or unsubscribe page?);
- sometimes static markup.

It cannot reliably show:
- visual hierarchy, colours or contrast;
- whether boxes are pre-ticked after JavaScript;
- timer behaviour;
- pop-ups;
- anything behind a login or deep in the checkout.

So in Mode B:
1. Fetch the URL(s) the user gave, and follow obvious links (pricing, cart, subscription, help or cancellation page) that appear in the fetched content.
2. Save fetched text into the workspace and run `scripts/scan_signals.py` on it for leads.
3. Ask the user, once, for screenshots of the flows you can't reach, typically product page, cart, checkout review, any pop-ups, and the cancel flow. A screen recording's frames also work. Give them the journey list above so they know what to capture.
4. If they can't provide them, finish the audit anyway. Mark those patterns `not_verifiable` in coverage with a note on what is needed. Don't guess.

### Mode C: screenshots only

The user uploads screenshots or a PDF of screens. Treat each image as a screen.
1. Read the visible text and layout carefully.
2. Note checkbox and toggle states, button hierarchy and fine print.
3. Estimate highlight boxes as percentages of the image.

Contrast can be estimated from pixel colours. If the image files are in the workspace, use Pillow to sample the foreground and background colours and compute the WCAG ratio.

---

## Figma capture

Works for mobile and web mockups. The Figma connector tools need to be loaded first (`tool_search` for "figma screenshot metadata"). If the Figma connector isn't available, ask the user to connect it or to export the frames as PNG.

1. **Parse the link.** `figma.com/design/<fileKey>/...?node-id=<a>-<b>`. The node id uses `:` in API calls (`a:b`). If the link points to a page or section, audit all top-level frames inside it.
2. **Map the structure.** Call `get_metadata` on the page or section node to list frames with names and sizes.
   - Group frames into journeys using names and positions: rows of frames are usually a flow.
   - Identify states and variants: empty, filled, error, success, default and selected.
   - Dark patterns often hide in states, for example a toggle's default variant.
3. **See each frame.** Call `get_screenshot` per frame (or per row for large files). Look at the image the way a user would.
4. **Read the text and properties.** For frames with consent, pricing, upsell, paywall or cancel content, extract the exact copy and component properties.
   - `get_design_context` returns text, styles and variants.
   - The Figma plugin requires loading the `figma:figma-design-to-code` skill before the first `get_design_context` call. Read it, then call the tool for inspection only. Don't generate code.
   - Use `get_variable_defs` when you need exact colour tokens for contrast.
5. **Check what's missing.** For subscription products, is there a cancel flow? For trials, is there a reminder or conversion state? For permission prompts, is there a "No" state? A missing state is a finding when the pattern definition depends on it. Phrase it as "the designs contain no…", with confidence `likely`.
6. **Record sources.** For each screen, keep the frame name and a link `https://www.figma.com/design/<fileKey>/?node-id=<a>-<b>` for the report.

**Getting images into the report**: if a Figma tool can save the frame render into the workspace (for example `download_assets` writing a PNG), use it as the screen's `image`. If renders only come back as images in the conversation and not as files, skip `image`. The HTML recreation (`current_html`) becomes the visual evidence, and the Figma link gives the source.

**Optional, only if the user asks**: write findings back into the Figma file as annotations so designers see them in place. Load `figma:figma-use` first. Use an annotation category such as "Dark pattern audit", with one annotation per finding giving the ID, pattern, severity and fix.

---

## Recreating screens in HTML (all modes)

The report shows each audited screen as a lightweight HTML recreation in two versions:
- **Current**: the problem elements marked with `data-dp="F1"`. Use space-separated IDs if one element carries several findings.
- **Compliant**: the fixed elements marked with `data-fix="F1"`.

This is the "prototype" part of the report. It lets designers and developers see the exact fix in context, even when no screenshot file is available.

Guidelines for recreations:
- Recreate only the relevant part of the screen: header, the problematic module, the CTAs. Don't rebuild the whole page. Aim for 15–60 lines of HTML per version.
- Keep the real copy, prices, labels and the visual hierarchy that matters: colours, sizes and weights of the accept and decline buttons, fine-print size, checked states. Use inline styles and simple elements. No scripts, external images or fonts.
- Mark checked states with real `checked` attributes on inputs, so the recreation is honest.
- In the compliant version, change only what the fix requires, so the before and after comparison is clear.
- `device` is `mobile` (renders in a 375px frame) or `desktop` (renders full width up to 960px).
