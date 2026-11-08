# Guardrails

Check every proposed change against this list before it goes into the prototype. These rules exist because fast teardown-style redesigns repeatedly made the same mistakes: invented claims, changed numbers, removed legal text and lost the brand's real differentiators. A conversion gain that creates legal risk, misleads shoppers or erodes the brand is not a win.

## Three tiers

| Tier | What | Rule |
|---|---|---|
| **Restyle freely** | Order, placement, grouping, spacing, type size, colour within the brand palette, component format (dropdown → tiles, paragraph → bullets, tabs → accordions), removing non-essential UI (share icons, dead selectors, duplicate bars) | Change as the audit requires. |
| **Verify before adding** | Any claim, figure, offer, service promise or proof not visible in the source material: delivery times, free shipping, trials, warranties, free gifts, samples, discounts, pack options and prices, "best seller"/"most re-ordered" labels, stock counts, customer counts, stats | Show it in the prototype only if it's in the source. Otherwise render it as a **needs-input placeholder** (see below) and list it under "Needs brand input". |
| **Never introduce** | Regulated health, medical, disease, weight-loss or drug-like claims not already in the brand's approved materials; escalated claims ("relieves" → "eliminates", "helps" → "cures"); fabricated reviews, endorsements or experts | Don't. If the brand has the claim with substantiation, you may relocate it verbatim with its qualifier. |

## Locked content (relocate or restyle, never delete or alter)

- **Legal and safety notices:** product recalls, safety warnings, age restrictions.
- **Subscription terms:** auto-renewal disclosures, minimum commitments ("2-order minimum"), cancellation terms. Never add "cancel anytime" if a minimum applies.
- **Privacy/consent notices:** chat-recording consent, data notices near forms.
- **Regulatory price displays:** India's MRP / "inclusive of all taxes", "Tax included", unit-price requirements.
- **Claim qualifiers:** asterisks, footnotes, "in a clinical study of n=…", "results may vary". They travel with their claim.
- **Facts:** price, currency, review count, rating, sizes, ingredient lists, nutrition values, specs, certifications. Copy them exactly.

## No fabrication

- Copy in the prototype comes from the source page, screenshots or the brand's other pages. You may rewrite *structure and wording* (shorten, split into bullets, convert to a question), but the substance must trace to the source.
- New microcopy that carries no claim is fine: "Select size:", "Why you'll love it", "What's the difference?", "See nutritional facts".
- **Needs-input placeholders.** When a must-know or a recommended element needs content the source doesn't provide (servings per pack, lead time, a real customer quote, a clinical stat, warranty length), put a clearly marked placeholder in the prototype: `<span class="needs-input">[Servings per pack]</span>`. The template styles these distinctly so nobody mistakes them for real content. Every placeholder is listed in the summary's "Needs brand input" section.
- **Reviews and endorsements:** use only reviews and expert quotes visible in the source. If none are available, use a needs-input placeholder ("[Short verified review mentioning results]").
- **Images:** never reuse, crop or re-host the brand's product photography in the proposal. Every product image, lifestyle shot, comparison card and video is a numbered grey placeholder that states what the shot should be, with a matching `image_plan` entry (see `render-design.md` §5). The logo is the only brand image allowed. Image briefs must not depict results, people or scenes the brand can't truthfully produce, and comparison shots that show another brand's product are flagged for legal review.

## Consistency checks (run on the current page *and* the proposal)

- Every number matches wherever it appears (price, savings %, per-unit maths, review count, sizes).
- Savings and per-unit maths are correct (10% of $32 is $28.80, not $28).
- Option labels stay true across combinations ("Best Value" isn't beaten by another option).
- Selected-state labels match the highlighted swatch/tile and the image.
- Gallery claims match available options (a K-cup icon on the bag requires a K-cup option).
- Variant-dependent content updates with the selection (price, specs, stock).
- Headline price names its purchase option when it isn't the one-time price.

If the current page is internally inconsistent, flag it and ask; never silently pick one value.

## Offers and margin

- Discounts are a last resort. Prefer clarity, proof, sequencing, bundles, thresholds and subscriptions.
- A new or deeper offer is a **recommendation**, never shown as if it already exists. State the margin trade-off.
- Keep the brand's existing offers; tidy competing ones (one leads, others shrink) rather than deleting.

## Ethics (align with dark-pattern rules)

- Urgency only when true: real end dates, real variant-level stock from live inventory.
- No pre-ticked add-ons that land in the cart without a deliberate action. A pre-checked bundle builder that needs a separate "Add 2 items" click is acceptable; flag it for review.
- Subscription and one-time options equally legible; the recurring nature unmistakable; the alternative never greyed out.
- No confirm-shaming, hidden costs or bait pricing.
- If the user has a dark-pattern auditor skill, suggest running the proposal through it.

## Brand fidelity

- Use the brand's own palette, fonts (or the closest available web font), logo treatment, imagery, button shapes and tone of voice. The proposal must read as the same brand, improved.
- Allowed shifts: choosing a CTA colour from within the brand's palette (or a close tint) that isn't overused elsewhere; moving brand colour to the edges; neutralising body text colour; resizing type for hierarchy.
- **Condense brand voice, never neutralise it.** If the brand is irreverent, patriotic, playful or clinical, the rewritten copy keeps that register.
- **Protect differentiators** found in the positioning step (signature scent, founder credential, charity, store pickup, made-to-order craft, origin like K-beauty, a distinctive subscription perk). If the template has no slot, create one.
- **SEO:** when cleaning a keyword-stuffed title, note that keywords should move to the meta title/description so rankings aren't affected.

## Accessibility floor

- CTA text contrast ≥ 4.5:1 (WCAG AA); body text ≥ 4.5:1; large text ≥ 3:1.
- Tap targets ≥ 44px tall on mobile.
- Don't rely on colour alone for selected states (add a border or tick).
