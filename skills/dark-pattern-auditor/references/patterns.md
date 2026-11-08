# The 13 specified dark patterns: detection and fix playbook

Source: Guidelines for Prevention and Regulation of Dark Patterns, 2023, notified by the Central Consumer Protection Authority (CCPA) on 30 November 2023 under Section 18 of the Consumer Protection Act, 2019 (CPA). Definitions below are plain-language paraphrases. Cite the clause number in findings, and point readers to the Gazette text for the exact wording.

Read the "How to use this file" section first, then go through every pattern in order. Each audit has to say something about all 13, even if it's "no issues seen" or "couldn't verify".

## Contents

- How to use this file
- Framework provisions that apply to every pattern
- 1. False urgency
- 2. Basket sneaking
- 3. Confirm shaming
- 4. Forced action
- 5. Subscription trap
- 6. Interface interference
- 7. Bait and switch
- 8. Drip pricing
- 9. Disguised advertisement
- 10. Nagging
- 11. Trick question
- 12. SaaS billing
- 13. Rogue malware
- Patterns that usually appear together

---

## How to use this file

Each pattern section has the same parts:

- **The rule**: what the Annexure says, broken into its separate limbs. A finding has to fit at least one limb.
- **Official illustrations**: the CCPA's own examples. A UI that mirrors one of these scores the highest "match" in the rubric.
- **Carve-outs**: what the Guidelines say is not this pattern.
- **Website signals** and **Figma / mobile signals**: what to look for in each kind of source.
- **Not a dark pattern when**: legitimate nudges that look similar. Use these to avoid false positives. Over-flagging makes the report noisy and teaches teams to ignore it.
- **To confirm**: facts you usually can't see in a screenshot or mockup. If the finding depends on one, mark the finding `needs_verification` and say exactly what data would settle it.
- **Related provisions**: other laws the same UI is likely to engage.
- **Enforcement record**: published CCPA action, where it exists.
- **Compliant alternative**: the fix pattern, sample copy, and acceptance criteria a developer can test against.

The Guidelines say the illustrations are guidance only. They are not a binding interpretation. Section 7 makes the CCPA's reading final where there is ambiguity. So write findings as "likely to be treated as" or "risks being found to be", not as legal conclusions.

## Framework provisions that apply to every pattern

- **Guidelines s.2(1)(e)**: a dark pattern is a UI/UX practice designed to mislead or trick users into doing something they didn't intend, by subverting their autonomy, decision-making or choice. It must amount to a misleading advertisement, an unfair trade practice, or a violation of consumer rights.
- **Guidelines s.3**: the Guidelines apply to platforms systematically offering goods or services in India, and to advertisers and sellers.
- **Guidelines s.4**: no person, including a platform, may engage in any dark pattern practice.
- **Guidelines s.5**: engaging in any Annexure 1 practice counts as engaging in a dark pattern.
- **Guidelines s.6**: the Guidelines add to other laws; they don't replace them.
- **CPA s.2(9)** consumer rights, **s.2(28)** misleading advertisement, **s.2(47)** unfair trade practice. CCPA orders usually cite these alongside the Guidelines.
- **Consumer Protection (E-Commerce) Rules, 2020**: Rule 4(3) bars unfair trade practices by e-commerce entities. Rule 4(9) bars recording consumer consent automatically, including through pre-ticked boxes.

These ten questions catch most patterns. Ask them of every screen:
1. Is anything chosen for the user that costs money or shares data?
2. Is the price on this screen the price they will pay?
3. Can the user say no as easily and neutrally as yes?
4. Is any claim (stock, viewers, deadline, "free") something the business can prove right now?
5. Does any wording make declining feel shameful, risky or stupid?
6. Is every ad recognisable as an ad?
7. Is the user being asked for something unrelated to what they came to do?
8. Will this prompt come back after the user dismisses it?
9. Is leaving (cancel, unsubscribe, delete, decline) as easy as joining?
10. Does the user know, before money moves, when and how much they'll be charged?

---

## 1. False urgency

**The rule** (Annexure 1, item 1): falsely stating or implying urgency or scarcity to mislead a user into an immediate purchase, or an immediate action that may lead to a purchase. This includes:
- (i) showing false popularity of a product or service;
- (ii) saying stock is more limited than it really is.

**Official illustrations** (paraphrased):
- (a) High-demand claims with no context, for example "only 2 rooms left" combined with "30 others are looking at this".
- (b) Fake time pressure, such as calling a sale exclusive and time-limited for a select group when it isn't.

**Website signals**
- Countdown timers. Reload in a fresh session or incognito: does the timer restart? A timer that resets for each visitor is the clearest evidence.
- "Only N left", "selling fast", "X people viewing", "booked N times today", "last chance", "ends tonight", "exclusive for you".
- Counters that are random or round, never change, or are identical across products.
- Scarcity text hard-coded in HTML or JS rather than driven by inventory APIs. Search the bundle for the literal string or `Math.random`.
- Sale banners that are permanently live, or with an end date that keeps moving.

**Figma / mobile signals**
- Timer components with static placeholder values ("23:59:59") in sale, checkout or paywall frames.
- Badge components such as "Trending", "Hot", "Only 3 left" placed in templates. Check whether the PRD or annotations say they're data-driven.
- Paywall or onboarding frames with "Offer expires in…" and no state showing what happens after expiry.

**Not a dark pattern when**: the claim is true, current and specific. Real stock from inventory, a real sale end date that is honoured, real viewer counts with a time window ("12 bookings in the last 24 hours"). Genuine urgency is allowed. False urgency is not.

**To confirm**: inventory or booking logs behind the scarcity claim; the timer's source and whether the price actually changes at zero; the history of sale end dates. Without this, mark `needs_verification` unless the timer visibly resets.

**Related provisions**: CPA s.2(28) misleading advertisement and s.2(47) unfair trade practice. ASCI Guidelines for Online Deceptive Design Patterns in Advertising (June 2023) also list false urgency.

**Enforcement record**: the CCPA treated a coaching platform's recurring 24-hour countdown, plus "claim your free spot" language, as false urgency. Its position is that urgency and scarcity claims must be backed by verifiable, current evidence.

**Compliant alternative**
- Show scarcity only from live inventory, with a timestamp or window ("3 left in stock as of 2:10 pm").
- Timers: fixed server-side end time, the same for every user. The offer actually ends at zero. No restart on reload.
- Popularity: real counts with a time window, or remove them.
- Acceptance criteria: scarcity strings come from an inventory endpoint, never constants. The timer end is identical across two fresh sessions. When the timer ends, the offer price is no longer purchasable.

**Typical severity**: High. Critical when combined with payment-step pressure or a vulnerable audience (for example students, or exam coaching).

---

## 2. Basket sneaking

**The rule** (Annexure 1, item 2): adding extra items at checkout (products, services, charity or donation payments) without the user's consent, so they pay more than for what they chose.

**Carve-outs**: these are not basket sneaking:
- free samples or complimentary services;
- necessary fees disclosed at the time of purchase, such as delivery, gift-wrapping, government taxes, or other charges explicitly disclosed then.

**Official illustrations** (paraphrased):
- (a) Paid add-ons added automatically, via pre-ticked box or otherwise.
- (b) A one-off salon booking that quietly adds a salon subscription at checkout.
- (c) Travel insurance auto-added to a flight booking.

**Website signals**
- `input[type=checkbox]:checked` or toggles that are on by default next to anything with a price: insurance, protection plans, memberships, donations, tips, "priority", seat selection, extended warranty. Check the live DOM state after JavaScript runs, not just the HTML attribute.
- Cart total higher than the sum of the items the user chose.
- Donation or "round-up" pre-selected.
- Items that appear in the cart between product page and checkout.
- A "remove" control for the add-on that is less visible than the item itself. This overlaps with interface interference.

**Figma / mobile signals**
- Checkout frames where toggles or checkboxes beside paid add-ons are in the "on" variant in the default state.
- Order summary frames listing a membership, donation or protection line the user didn't pick in earlier frames.
- Flows with no frame showing the add-on being deliberately selected.

**Not a dark pattern when**: the add-on is shown unselected and the user opts in with a deliberate action. A necessary fee is clearly disclosed before purchase. A free sample is included.

**To confirm**: whether the add-on is selected by default for all users or only for returning users who chose it before. A remembered choice is defensible if the user can see it.

**Related provisions**: E-Commerce Rules 4(9), which bars pre-ticked consent. CPA s.2(47). The DPDP Act s.6 consent standards also apply where a data-sharing consent is pre-ticked; the consent provisions take effect 13 May 2027.

**Enforcement record**: this is the CCPA's most frequently enforced pattern. Cases include:
- Zepto: paid membership auto-added.
- PhysicsWallah: a ₹10 donation pre-selected.
- PharmEasy: membership auto-added. The CCPA called fixes made after the show-cause notice reactive.
- BookMyShow: pre-ticked charity contribution; corrective directions.

The common principle is that a pre-selected default, without a specific affirmative act by the consumer, is not consent.

**Compliant alternative**
- Every optional paid item starts unselected and is added only by the user's tap or click.
- Show the price next to the opt-in control.
- The cart total updates visibly when the item is added.
- Copy: "Add trip protection for ₹199?" with "Add" / "Don't add" given equal visual weight.
- Acceptance criteria: on a fresh session, the cart total equals the sum of user-chosen items plus disclosed necessary fees. No paid add-on is in the cart unless an explicit user event added it.

**Typical severity**: Critical when money is charged by default. High when the item is visible and removable but pre-selected.

---

## 3. Confirm shaming

**The rule** (Annexure 1, item 3): using a phrase, video, audio or any other means to create fear, shame, ridicule or guilt so the user buys something or keeps a subscription, mainly for commercial gain by subverting their choice.

**Official illustrations** (paraphrased):
- (a) A flight-booking platform whose decline-insurance option says something like "I will stay unsecured".
- (b) A platform that adds charity to the basket and labels the opt-out with something like "charity is for the rich, I don't care".

**Website signals**
- Decline labels that insult or frighten the user: "No thanks, I don't like saving money", "I'll take the risk", "Leave my family unprotected", "I prefer paying full price", "Accept risk", "I don't care about…".
- Cancellation or exit modals using guilt ("You'll lose everything", "Are you sure you want to miss out?") with sad imagery or loss-heavy copy.
- Fear framing on security or insurance upsells, without accurate context.

**Figma / mobile signals**
- Button or link text on decline or cancel paths.
- Illustration choices: crying mascots, broken hearts.
- Retention screens in cancel flows.
- Read every secondary button label across paywall, upsell, cancel and unsubscribe frames.

**Not a dark pattern when**: the copy states a real consequence neutrally, such as "If you cancel, your saved projects will be deleted after 30 days". Accurate information about loss is fine. Emotional pressure on the person is the problem.

**To confirm**: rarely needed. The copy itself is the evidence.

**Related provisions**: CPA s.2(47). It often appears together with interface interference, where the decline is also visually demoted.

**Enforcement record**:
- McAfee's renewal screen offered "Renew Now" and "Accept Risk", with the decline in subdued grey against a prominent red renew button.
- IndiGo used "No I will take risk" as an opt-out. It switched to neutral wording ("No, I will not add it to my trip") after CCPA intervention.
- PhysicsWallah paired a pre-selected donation with emotional retention messages.

**Compliant alternative**
- Neutral, symmetric labels: "Add insurance" / "Continue without insurance". "Keep subscription" / "Cancel subscription".
- State the consequence once, factually, in body text, not in the button.
- Acceptance criteria: the decline label describes the action, not the user. It contains no fear, loss or self-deprecating words. Both options use the same component tier, or the decline is at least a fully legible secondary button.

**Typical severity**: High at checkout, renewal or cancellation. Medium elsewhere.

---

## 4. Forced action

**The rule** (Annexure 1, item 4): forcing the user to take an action to get what they originally intended. Forms include:
- buying additional goods;
- subscribing or signing up to an unrelated service;
- sharing personal information.

**Official illustrations** (paraphrased):
- (a) Blocking continued use of a paid-for service unless the user upgrades.
- (b) Requiring a newsletter subscription to buy a product.
- (c) Requiring a separate, unrelated app download to access a service advertised in the first app.
- (d) Demanding Aadhaar-linked or credit-card details when the purchase doesn't need them.
- (e) Demanding access to contacts or social networks to use a purchased or intended service.
- (f) Making privacy settings hard to understand or change, so users share more than they mean to.

**Website signals**
- Mandatory account creation or login before the price is shown or before guest checkout, where it isn't needed.
- Required fields beyond what fulfilment needs: date of birth, Aadhaar or PAN, phone for a digital-only purchase.
- "Allow contacts" or "Connect social" as a blocking step.
- Newsletter or marketing consent bundled into the "I agree" checkbox needed to proceed.
- Pre-ticked enrolment in loyalty programmes.
- Privacy settings buried several levels deep, defaulting to maximum sharing.

**Figma / mobile signals**
- Onboarding frames requesting permissions (contacts, location, notifications) before value is shown, with no skip.
- Signup forms with required fields marked `*` beyond need.
- A single consent checkbox combining terms with marketing.
- Paywalled frames appearing after the user has already paid.

**Not a dark pattern when**: the data is genuinely needed, such as a delivery address for a physical order or KYC required by regulation (RBI, SEBI or IRDAI rules), and the screen says why. Login is needed because the service is account-based by nature.

**To confirm**: whether a field is legally required (KYC) or simply wanted. The PRD or a backend check can settle this.

**Related provisions**:
- DPDP Act s.6: consent must be free, specific, informed, unconditional and unambiguous, and limited to necessary data. In force from 13 May 2027.
- E-Commerce Rules 4(9).
- CPA s.2(47).

**Enforcement record**: SpiceJet's pre-ticked loyalty-programme enrolment and default consent to promotional communications were treated as forced action and interface interference.

**Compliant alternative**
- Guest checkout where possible.
- Separate, unticked, optional consents for marketing.
- Ask for each field and permission only at the moment it's needed, with a one-line reason.
- Privacy controls reachable within two taps of settings, defaulting to minimum sharing.
- Acceptance criteria: the purchase can be completed with only the fields fulfilment requires. Declining marketing or permissions doesn't block the core task.

**Typical severity**: High when it gates a purchase or collects sensitive identifiers. Medium for bundled marketing consent.

---

## 5. Subscription trap

**The rule** (Annexure 1, item 5) has four separate limbs. Test each one:
- (i) cancelling a paid subscription is impossible, complex or lengthy;
- (ii) the cancellation option is hidden;
- (iii) payment details or auto-debit authorisation are required to get a free subscription;
- (iv) cancellation instructions are ambiguous, latent, confusing or cumbersome.

**Website signals**
- Count the steps from the account home to confirmed cancellation, and compare with the steps to subscribe. "Click to subscribe, call to cancel" is the classic failure.
- Cancellation only by email, chat, phone or store visit.
- "Manage subscription" hidden under unrelated labels.
- Multiple retention screens before the final confirm.
- Free trial pages asking for a card or UPI AutoPay mandate.
- "Cancel anytime" claims with no visible cancel route.

**Figma / mobile signals**
- Is there a cancel flow at all? Missing cancel frames in a subscription product is itself a finding: "not designed" usually means "not built".
- Count the frames in the cancel path compared with the subscribe path.
- Check trial-start frames for payment capture.
- On iOS and Android, check whether the app links to platform subscription management.

**Not a dark pattern when**: cancellation is self-serve and about as quick as signup. A single, optional retention offer is shown once. A trial needs a payment method and the screen clearly says when the first charge happens and how to cancel before it. Even then, flag limb (iii) as a risk: the text targets requiring payment details for a *free* subscription.

**To confirm**: whether cancellation actually stops billing (backend), and whether the confirmation email arrives.

**Related provisions**: CPA s.2(47). RBI's e-mandate framework for recurring payments, which includes pre-debit notification; check the current circular. It also overlaps with SaaS billing.

**Enforcement record**: the CCPA served a notice on Amazon India alleging that consumers were enrolled in Prime without consent through dark patterns. Check for the outcome before citing it in a report. Legal commentary on the CCPA orders treats "leaving should be no harder than joining" as the working compliance benchmark.

**Compliant alternative**
- "Cancel subscription" is visible in account or settings and labelled plainly.
- At most one optional retention offer, then one confirm.
- On-screen and email confirmation with the end date.
- Free trials without payment details. If payment is needed, show a plain-language charge date and amount before the user agrees, and send a reminder before conversion.
- Acceptance criteria: cancellation completes online in no more steps than signup. No step requires contacting support. A confirmation is shown and emailed.

**Typical severity**: Critical when cancellation is offline-only or hidden. High for long or confusing flows, or for payment capture on free trials.

---

## 6. Interface interference

**The rule** (Annexure 1, item 6): a design element that highlights certain information and obscures other relevant information, to misdirect the user from the action they want.

**Official illustrations** (paraphrased):
- (a) A light, faint "No" option on a purchase pop-up; a cancel symbol in tiny font; key symbols changed to mean the opposite.
- (b) An "X" in a pop-up's corner that opens another ad instead of closing.
- (c) The faint "No" again.

**Website signals**
- Contrast and size asymmetry between accept and decline. Measure it: a WCAG contrast below 4.5:1 for the decline text is strong evidence.
- Decline styled as plain grey text while accept is a coloured button.
- Close icons that are tiny, low-contrast, delayed, or that trigger navigation or ads.
- Cookie banners with "Accept all" prominent and "Reject" hidden under "Settings".
- Important terms (auto-renewal, price after promo) in small grey text, far from the CTA.
- Reversed toggle semantics.

**Figma / mobile signals**
- Inspect button variants on modals, paywalls and consent sheets. Check the fill, text colour and size of the decline option.
- Close-icon size below 24×24 or 44×44 pt tap target.
- Disclosure text style (size and colour tokens) next to CTAs.
- Inspect component properties; don't rely on the screenshot alone.

**Not a dark pattern when**: a clear primary/secondary hierarchy exists but the secondary option is fully legible and plainly labelled. Highlighting the recommended choice is normal design. Making the alternative hard to find is the problem.

**To confirm**: measure contrast from the actual colours. Click the close button in the live product to see what it does.

**Related provisions**: CPA s.2(47). DPDP s.6 for consent UIs, in force from 13 May 2027.

**Enforcement record**:
- McAfee: grey decline beside a prominent red renew.
- SpiceJet: default consent to promotional communications, treated as interface interference.

**Compliant alternative**
- Accept and decline with comparable prominence. Both are buttons, or the decline is a clearly legible secondary button with at least 4.5:1 contrast.
- Close icons at least 24×24 visible and 44×44 tap target, and they always close.
- Material terms in body-size text adjacent to the CTA.
- Acceptance criteria: the decline control meets WCAG AA contrast, sits in the same container as accept, and needs the same number of taps.

**Typical severity**: High on purchase, renewal or consent decisions. Medium elsewhere.

---

## 7. Bait and switch

**The rule** (Annexure 1, item 7): advertising one outcome for the user's action, then deceptively serving a different one.

**Official illustrations** (paraphrased):
- (a) A cheap quality product that is "no longer available" at payment, with a similar but pricier product offered instead.
- (b) An out-of-stock item shown as available to lure it into the cart, then revealed as out of stock, with a higher-priced item offered.

**Website signals**
- Ads or listing prices that don't match the product page.
- "In stock" on listing pages but unavailable in the cart.
- Promo codes advertised but rejected at checkout.
- Buttons whose label promises one thing ("Download free") but lead to a paywall or a different product.
- Search results ranking a pricier "similar" item above the searched item.

**Figma / mobile signals**
- Out-of-stock and price-change states. Do they appear before the cart or only at checkout?
- CTA labels compared with the destination frame.
- Banner or ad frames promising an outcome the next frame doesn't deliver.

**Not a dark pattern when**: stock genuinely ran out in between, and the UI says so at the earliest point and shows the original item's status honestly. Substitutes are offered neutrally, not as a forced swap.

**To confirm**: stock history and ad-versus-PDP price data. This is often `needs_verification` from static designs.

**Related provisions**: CPA s.2(28) and s.2(47). The CCPA's 2022 Guidelines for Prevention of Misleading Advertisements cover bait advertising. ASCI also lists bait and switch.

**Compliant alternative**
- Availability checked and shown on listing and product pages.
- If an item becomes unavailable, say so plainly and let the user go back. Don't auto-swap.
- Advertised prices and codes honoured or removed.
- Acceptance criteria: the listing availability flag equals the cart availability at the same timestamp. The advertised price equals the PDP price.

**Typical severity**: High.

---

## 8. Drip pricing

**The rule** (Annexure 1, item 8) has four limbs:
- (i) price elements are not revealed upfront, or are revealed surreptitiously during the journey;
- (ii) the price is revealed after the purchase is confirmed, i.e. the user is charged more than the amount shown at checkout;
- (iii) something is advertised as free without disclosing that continued use needs in-app purchases;
- (iv) the user is blocked from a service already paid for unless they buy something extra.

**Carve-out**: a marketplace isn't liable for price fluctuations caused by third-party sellers or other factors beyond its control.

**Official illustrations** (paraphrased):
- (a) A flight shown at price X at checkout, but a higher Y charged at payment.
- (b) A chess app advertised as free that demands payment after 7 days, with the time limit undisclosed at download.
- (c) A gym membership where the gym can only be used if the member buys special gear from the gym, which wasn't disclosed at sale.

**Website signals**
- Product page price compared with cart compared with checkout compared with payment page. List every line that appears at each step: platform fee, convenience fee, handling, small-cart fee, "taxes extra", surge.
- "Inclusive of all taxes" claims followed by GST added later.
- Fees that appear only after address or payment-method selection.
- "Free" labels on apps or plans that are trials.

**Figma / mobile signals**
- Price components across PDP, cart, checkout and payment frames. Do the totals agree? Where does each fee first appear?
- App-store or landing copy saying "free" while a paywall frame exists in onboarding.

**Not a dark pattern when**: all mandatory fees are shown, or reliably estimated, from the first price display. Taxes are clearly stated as included or excluded. Variable fees such as delivery distance are explained before commitment.

**To confirm**: whether the final charged amount ever exceeds the checkout total (payment logs). Whether fees are dynamic.

**Related provisions**:
- CPA s.2(28) and s.2(47).
- Legal Metrology (Packaged Commodities) Rules on MRP inclusive of taxes, for packaged goods.
- ASCI lists drip pricing.

**Enforcement record**:
- Zepto: lower product-page price, with handling charges and membership fees added at checkout.
- FirstCry: prices shown as tax-inclusive, with GST added at checkout.

The CCPA compares the price that drew the user in with the final amount demanded.

**Compliant alternative**
- Show the all-in price, or a "from ₹X incl. fees" estimate, on the first price display.
- A fee breakdown visible before the payment step.
- "Free" only for genuinely free tiers. Trials labelled with duration and post-trial price.
- Acceptance criteria: for a standard order, PDP price plus disclosed fees equals the payment amount. No new mandatory fee line first appears at or after payment selection.

**Typical severity**: Critical for limbs (ii) and (iv). High for (i) and (iii).

---

## 9. Disguised advertisement

**The rule** (Annexure 1, item 9): passing off ads as other content (user-generated content, news articles) or false ads, designed to blend into the interface so users click.

The explanations add two points:
- (a) this includes misleading advertisements under CPA s.2(28), and the 2022 Misleading Advertisements Guidelines apply;
- (b) for seller or advertiser content on a platform, the seller or advertiser is responsible for disclosing it as an ad. Platforms still need to provide a way to label it.

**Website signals**
- Sponsored products, listings, reviews or articles without a visible "Ad" or "Sponsored" label, or with a label in tiny low-contrast text.
- Native ads styled exactly like editorial or organic results.
- Influencer or "customer story" content that is paid.
- "Recommended for you" carousels that are paid placements.

**Figma / mobile signals**
- Feed and search-result components. Is there a sponsored variant with a label?
- Content cards in templates. Are paid placements distinguishable?

**Not a dark pattern when**: ads are clearly and prominently labelled where the user sees them, before the click.

**To confirm**: whether placements are paid. Ad-server data or commercial agreements settle this.

**Related provisions**:
- CPA s.2(28).
- Guidelines for Prevention of Misleading Advertisements and Endorsements, 2022, including endorsement disclosures.
- ASCI code and influencer guidelines.

**Compliant alternative**
- A consistent "Sponsored" or "Ad" label at the top of every paid unit, at body-text size and contrast.
- Paid units visually distinguishable from organic ones.
- Acceptance criteria: every paid placement from the ad server renders the label component. The label meets WCAG AA contrast.

**Typical severity**: Medium. High when the ad impersonates news, reviews or official notices.

---

## 10. Nagging

**The rule** (Annexure 1, item 10): repeated, persistent requests, information, options or interruptions that disrupt and annoy the user, to push a transaction for commercial gain, unless the user has specifically permitted them.

**Official illustrations** (paraphrased):
- (a) A website repeatedly asking the user to download its app.
- (b) Platforms asking for phone numbers or other personal details, supposedly for security.
- (c) Constant requests to enable notifications or accept cookies with no option to say no.

**Website signals**
- App-install interstitials or banners that return after dismissal, on every page or every visit.
- Notification-permission prompts with only "Allow" / "Later".
- Cookie banners with no reject option.
- Repeated phone or email capture modals.
- Exit-intent pop-ups on every exit.

**Figma / mobile signals**
- Prompt frames with only "Allow" / "Maybe later" (no "No" or "Don't ask again").
- Re-prompt logic in annotations ("show again every session").
- Multiple prompts stacked in onboarding.

**Not a dark pattern when**: a prompt appears once, has a clear "No" or "Don't ask again" that is respected for a reasonable period, or the user opted in.

**To confirm**: frequency logic. Visit twice in the live product, or read the PRD or annotations.

**Related provisions**: CPA s.2(47). DPDP for repeated data requests, in force from 13 May 2027. OS platform guidelines on permission prompts (Apple HIG, Android) are also relevant for app-store review risk.

**Compliant alternative**
- Each prompt has a real "No" / "Don't ask again".
- Respect it, for example no re-ask for at least 90 days or until the user starts the related feature.
- Explain why the permission helps, at the moment of need.
- Acceptance criteria: after "No", the prompt doesn't reappear in the same or the next session. Cookie banners offer "Reject all" at the same level as "Accept all".

**Typical severity**: Medium. High when the nagging seeks sensitive data or blocks use.

---

## 11. Trick question

**The rule** (Annexure 1, item 11): deliberately confusing or vague language (double negatives and similar tricks) used to misdirect the user from the action they want, or to steer them to a particular response.

**Official illustration** (paraphrased): a question asking whether the user wants to opt *out* of updates forever, answered with options like "Yes, I would like to receive updates" and "Not now", instead of a straightforward "Yes".

**Website signals**
- Double negatives ("Uncheck to not receive…").
- Questions whose answers don't match the question.
- Opt-out phrased as opt-in.
- Checkbox labels mixing "don't" and "unsubscribe".
- "Not now" as the only alternative to a permanent choice.
- Toggles where "on" means less.

**Figma / mobile signals**
- Read every consent, preference and unsubscribe screen. Does each answer literally answer the question?
- Check toggle labels against the state they represent.

**Not a dark pattern when**: the question is direct and the answers are "Yes" / "No" or describe the outcome plainly.

**To confirm**: what each option actually does (backend or PRD), if it isn't clear from the UI.

**Related provisions**: CPA s.2(47). DPDP s.6 ("unambiguous"), in force from 13 May 2027.

**Compliant alternative**
- One question, positively phrased ("Send me offers by email?"), with "Yes" / "No" answers.
- No double negatives.
- Acceptance criteria: each option label states the resulting state ("Email me offers" / "Don't email me offers"). A copy review confirms there are no negations stacked in the question and answer.

**Typical severity**: Medium. High when it controls a charge or sensitive data.

---

## 12. SaaS billing

**The rule** (Annexure 1, item 12): generating and collecting recurring payments in a SaaS model by exploiting positive acquisition loops, so money is taken from users as surreptitiously as possible.

**Official illustrations** (paraphrased):
- (a) No notification when a free trial converts to paid.
- (b) Silent recurring debits without notice, or auto-renewing monthly plans without telling users.
- (c) Charging for features or services the customer doesn't use.
- (d) Shady card-authorisation practices.

**Website signals**
- Trial signup with no stated conversion date or price.
- Auto-renew enabled by default and mentioned only in fine print.
- No billing-history or upcoming-charge page.
- Plans that bundle paid add-ons the user didn't select.
- "Authorise ₹1" or ₹2 verification charges with unclear recurring mandates.

**Figma / mobile signals**
- Is there a trial-ending reminder (email, push or in-app frame)?
- Is there a renewal-notice state or a billing-history screen?
- Does the plan picker show the renewal price and frequency next to the CTA?

**Not a dark pattern when**:
- The renewal terms (price, frequency, date) are stated plainly at signup.
- A reminder is sent before trial conversion and before annual renewals.
- Each charge produces a receipt.

**To confirm**: notification and email logs, payment-mandate set-up, and RBI pre-debit notification compliance. Backend evidence is usually needed.

**Related provisions**: CPA s.2(47). RBI e-mandate rules for recurring payments, which require a pre-debit notification; check the current circular. Overlaps with subscription trap.

**Compliant alternative**
- At signup: "Free until 12 Dec, then ₹499/month. We'll remind you on 9 Dec. Cancel anytime in Settings."
- A reminder before conversion or renewal.
- A receipt for every charge.
- A billing page showing the next charge.
- Acceptance criteria: a reminder is sent at least 3 days (and per RBI rules at least 24 hours) before the first paid charge. Every charge triggers a receipt. Renewal price and date are visible in-app.

**Typical severity**: Critical for silent conversion or debits. High for buried auto-renew terms.

---

## 13. Rogue malware

**The rule** (Annexure 1, item 13): using ransomware or scareware to trick users into believing their device has a virus and persuade them to pay for a fake removal tool that actually installs malware.

**Official illustrations** (paraphrased):
- (a) A pirate site promising free content whose link leads to embedded malware.
- (b) Malware-laden ad pop-ups on pirated platforms.
- (c) Ads or auto-redirects that lock the user's files and demand payment.

**Website signals**
- Fake system or virus alerts.
- Fake "scan now" overlays mimicking OS dialogs.
- Auto-downloads.
- Redirect chains to unknown domains from ad slots.
- Ad networks with a poor reputation.

Do not click download links or run anything during an audit. Report the observation and the URL only.

**Figma / mobile signals**
- Rarely relevant to a first-party design. Check fear-based "Your device is at risk" screens in security or cleaner apps that upsell, and ad-slot frames.

**Not a dark pattern when**: a genuine security product reports real, verifiable findings neutrally.

**Related provisions**:
- Information Technology Act, 2000 ss.43 and 66 (criminal exposure).
- Indian Computer Emergency Response Team (CERT-In) reporting.
- CPA s.2(47).

**Compliant alternative**: remove the content. Vet ad networks. Use a strict content-security policy for ad slots. Never imitate system dialogs.

**Typical severity**: always Critical. Escalate to security as well as legal.

---

## Patterns that usually appear together

Look for these clusters. When two patterns stack on one screen, add the "stacked" amplifier in the rubric. Still log each pattern as its own finding, because each has its own fix.

- **Pre-selected add-on + shaming opt-out + grey decline**: basket sneaking + confirm shaming + interface interference. This is the most common enforced combination (PhysicsWallah, McAfee, IndiGo).
- **Low PDP price + fees at checkout + "inclusive of taxes" claim**: drip pricing (Zepto, FirstCry).
- **Free trial needing a card + no reminder + hard cancel**: subscription trap + SaaS billing.
- **Timer + "N people viewing" + "only N left"**: false urgency (several limbs).
- **Repeated app-install prompts + notification ask with no "No"**: nagging.
- **Bundled consent checkbox + pre-ticked marketing**: forced action + interface interference (SpiceJet).
