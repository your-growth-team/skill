# Audit method: how the auditor thinks

Read this in full before auditing. It is the reasoning that every recommendation must come from. The pattern library (`pdp-playbook.md`) and category modules (`category-modules.md`) are tools this method uses; they are not a checklist to apply blindly.

## Contents
1. The auditor's stance
2. The north star: profit, not conversion rate
3. The process (Context → Where → Why → Competitors → How → Guardrails → Output)
4. Triage benchmarks
5. The readiness gate
6. Measurable checks
7. How to order and prioritise recommendations
8. Evidence honesty: observed vs hypothesis

---

## 1. The auditor's stance

- **CRO is not A/B testing.** Testing measures impact; the work is deciding what to change and why. About 80% of the work happens before any test. Never recommend a change without a reason rooted in shopper psychology, evidence, or a measured pattern ("change the button colour" is not a recommendation; "the button shares its colour with five other elements so it doesn't stand out" is).
- **The shopper's doubts drive everything.** Every element on a page either answers a doubt, removes friction, or is in the way. Ask of each element: which doubt does this answer, and is it answered where the doubt arises?
- **Relocate before you invent.** Most strong redesigns move and reformat content the page already has (a stat buried in a paragraph becomes a badge on the hero; a "For dry skin" sentence becomes a pill above the title). Inventory existing assets first. New content is the last resort and must be flagged for the brand to supply.
- **Subtraction is a fix.** Removing a dead selector, a second announcement bar, a share icon or a login icon is often worth more than adding a section.
- **Familiarity beats novelty for fast decisions.** Shoppers expect a standard PDP. Hamburger left, search and cart right, accordions not tabs, title-price-gallery-options-CTA. Unusual layouts must earn their place.
- **Ethical CRO only.** Urgency must be true. Subscriptions must be unmistakable. Nothing is hidden, invented or pre-ticked to trick. The aim is to remove the shopper's real doubts, not to manufacture new pressures.
- **Brand is protected, not flattened.** Condense brand copy, never neutralise its voice. A brand's genuine differentiator (a signature scent, a charity commitment, store pickup, a founder's credential) is protected even when the template has no slot for it.

## 2. The north star: profit, not conversion rate

Profit ≈ traffic × conversion × AOV × margin × repeat rate. Reason in those terms.

- A fix that lifts conversion by deepening discounts can lose money. Discounts are a last resort; when proposed, state the margin cost.
- An upsell that lifts AOV but lowers conversion is judged on **total site revenue per visitor**, not AOV alone.
- **Retention lens:** ask whether the page sets up the second purchase (subscription, supply duration, "most re-ordered", variety pack for trial, loyalty points, community proof). Profitable DTC brands get most sales from repeat and organic customers.
- Traffic mix sets priority. Paid-heavy stores gain most from first-fold clarity and differentiation (every visitor is paid for). Stores with strong organic/repeat traffic gain more from AOV and retention work.

## 3. The process

The three questions that frame everything:
- **Where** did visitors land, what did they see, where did they leave?
- **Why** what did they click and read, and what did they skip?
- **How** what do visitors care about, and is that information accessible?

### Step 0: Device check (always, before anything else)
Classify the screenshots as mobile or desktop (`scripts/crop_assets.py devices`, then confirm by looking). If only one device is present, ask the user for the other device's full-scroll screenshots before auditing, and explain that the page often differs a lot between devices and the audit proposes both. If they can't share them, proceed and say so in the limitations. Every audit delivers both a mobile and a desktop proposal.

### Step 1: Context (always)
Establish, inferring what you can and asking only for what's essential:
- Site type (this skill covers e-commerce) and page type (PDP by default; homepage, collection or landing page if supplied).
- Category, and whether the purchase is **aesthetic** (bought on looks: décor, fashion, jewellery design) or **functional** (bought on what it does: skincare, supplements, chairs).
- **Price tier and decision cycle.** A $30 product is bought in one visit; a $3,000 product over several. High-ticket shifts the readiness gate (see §5).
- **Visitor context.** Traffic source (paid social, search, email, direct), new vs returning, and category crowding. Ad visitors in crowded categories decide in about three seconds and have just seen several near-identical brands.
- **Market/country.** Local conventions matter (India: MRP inclusive of taxes, prepaid vs COD, UPI; US: subscription auto-renewal disclosures, HSA/FSA; AU: TGA claim rules).
- **Positioning.** What makes this brand and this product genuinely different? Ask the user if it isn't obvious. Read the About page if available. This is the step teardown-style audits most often skip, and skipping it is how differentiators get lost.

### Step 2: Where (analytics, if provided)
Top landing pages; bounce and conversion by page; pages with high views and low conversion; add-to-cart rate; buy-to-detail rate by product (find "dark horse" products that convert well but get little exposure). If not provided, say what would help and proceed.

### Step 3: Why (behaviour, if provided)
Scroll maps (what % reach each section and the CTA), click maps, attention maps, session recordings, frequent customer questions (support tickets, reviews, chat logs). Microsoft Clarity is a free source: https://clarity.microsoft.com. If not provided, infer likely leaks from the page and label them as hypotheses.

### Step 4: Competitor scan (when web search is available)
Find 2–4 leading brands in the same category and market. Note the sections they have in common (the expected layout) and current trends. Use this to calibrate what shoppers expect, not to copy. Skip if search is unavailable and say so.

### Step 5: How (the page audit)
1. Category must-knows (`category-modules.md`): can a shopper answer the category's basic questions on this page?
2. The readiness gate (§5) before the add-to-cart.
3. Zone by zone (`pdp-playbook.md`): announcement bar and header, title block, gallery, copy, options, CTA area, below-CTA proof, cross-sell, accordions and depth content.
4. The measurable checks (§6).
5. Internal consistency: every number (price, count, size, rating, review count, savings) matches wherever it appears; selector state matches its label and image; gallery claims match available options.

### Step 6: Guardrails
Check every proposed change against `guardrails.md` before it goes in the prototype.

### Step 7: Output
Changes ordered **structure → copy → design**, with first-fold changes on top-traffic pages first. Each change has a metric and a measurement method. See §7.

## 4. Triage benchmarks

Use when the user shares numbers. Calibrated for repeat-purchase DTC consumables; adjust down for high-ticket and long decision cycles (a $400 chair or $3,000 ring converts lower and that's normal).

| Signal | Reading |
|---|---|
| Site conversion ~1% | Leaky. Start with the first fold of top landing pages. |
| 1.5–2.5% | Typical. Clear room to improve. |
| 2.5–3.5%+ | Healthy. Shift weight toward AOV and retention. |
| PDP bounce > 70% | First fold is failing. |
| Add-to-cart rate < 10% | First fold / readiness failing. |
| Scroll-map drop-off right after the CTA | CTA arrived before readiness. |
| 30%+ drop-off inside a section | Too much copy (description > 2 lines, back-to-back text sections, or a fold > 50% copy). |
| PDP bounce 60–80% | Common; the first fold is where to win. |

## 5. The readiness gate

The add-to-cart CTA should be prominent but not "too early" or "too late". Too early: the shopper can't decide yet. Too late: they've already left. Before the CTA, the shopper should have answers to:

1. **Fit**: is this for me? (concern, skin/hair type, audience, size, use case)
2. **Difference / benefit**: what will it do, and why this one rather than the five similar brands I just saw?
3. **Trust**: why believe it? (proof ladder below)
4. **Value**: is it worth the price? (quantity, duration, per-day/per-use price, savings, specs for high-ticket)

Plus **usability**: can they choose and act without friction?

Judge readiness by **questions answered**, not by components present. Bullets before the CTA are one way to answer "benefit"; a strong description plus proof on the hero image can do the same job.

### Proof ladder (strongest first)
1. Clinical or independent study result (only if the brand has it)
2. Customer-reported result ("80% saw results after first wash")
3. Third-party authority: press badge, award, expert/clinician endorsement, accreditation (OBGYN-formulated, third-party tested)
4. Popularity: best seller, most re-ordered, number of customers
5. Reviews and ratings; UGC video

Use the strongest proof the brand actually has. Flag when a weaker proof sits in a prime slot while a stronger one is buried.

### High-ticket and multi-visit purchases
The gate's weighting shifts:
- **Value** is proven by specs (metal, carat, materials, dimensions, capacity), not per-unit price.
- **Trust** is risk reversal (warranty, returns, trial, resizing) and **access** to a human (consultation, chat, "talk to us").
- Support the return visit: wishlist/save, email details, appointment booking, financing. Don't push aggressive upsells into a considered decision.

## 6. Measurable checks

Check these on each device's first fold and full scroll (mobile ~390 × 844; desktop ~1280 × 900). Mobile targets are listed; on desktop the add-to-cart should be visible in the first screen or close to it.

| Check | Target |
|---|---|
| Announcement bars | One, short height |
| Product title | 2–3 lines, ~24px or less on mobile |
| Description under title | ≤ 2 lines |
| Any paragraph | ≤ 3 lines (half of visitors won't read past 5) |
| Hero image | ≤ 60–70% of the viewport height |
| Price | Near the name, never only after the options |
| Variant selector | On the same screen as the image when variants are visual |
| Add-to-cart | Visible within roughly the first two screen heights |
| Benefit bullets | 3, one line each on mobile, longest to shortest |
| Badges above title | 1–3, 2–3 words each |
| Options shown | 2–4; more than 4 means decompose or use a dropdown |
| CTA colour | Used only on the primary CTA; meets WCAG AA contrast (4.5:1 text) |
| First fold | Contains something to read, something to click, a reason to scroll |
| Gallery | Arrow + sneak peek; thumbnails when the gallery educates; not 30 images |

## 7. How to order and prioritise recommendations

- **Group by layer:** structure (order, placement, what's present) → copy (titles, descriptions, bullets, labels) → design (type size, colour, spacing).
- **Rank by expected profit impact × traffic exposure ÷ effort.** First-fold changes on top landing pages first.
- **One problem at a time.** Recommend a focus order; brands that try to fix seven things at once spread themselves thin.
- **Each change carries:** the doubt or friction it removes, the principle, the primary metric (add-to-cart rate, conversion rate, AOV, revenue per visitor, scroll reach), a guard metric where relevant, and a measurement method.
- **Measurement method by traffic:** A/B test where traffic supports it (rule of thumb: a few hundred conversions per variant per test window); otherwise a before/after comparison over 2–4 weeks with seasonality noted.
- **Structural bets are tests, not verdicts.** Page type (PDP vs dedicated landing page), removing express checkout, removing a large pack, changing the subscription default: recommend testing.
- **Each change says which devices it applies to.** Most apply to both; some are layout-specific (a desktop sticky buy box, a mobile header).
- **Aim for at least 12 ideas** in the backlog when the user wants a test plan (one per week over three months); the prototype shows the highest-priority set.

## 8. Evidence honesty: observed vs hypothesis

Every finding is one of:
- **Observed**: visible on the page or screenshot (missing price near the name, a dropdown hiding 12 options, CTA below the second fold). State confidently.
- **Hypothesis**: a likely cause of drop-off that needs data to confirm. Say which data would confirm it.
- **Needs brand input**: something the page should show but the auditor can't verify or supply (servings per pack, lead time, a real clinical stat, warranty terms).

Never present a hypothesis as observed, and never fill a "needs brand input" gap with invented content.
