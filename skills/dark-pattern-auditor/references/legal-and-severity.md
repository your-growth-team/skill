# Legal exposure and severity scoring

Use this file to work out three things for each finding:
1. which provisions it likely engages;
2. its severity score;
3. the consequences to write in the report.

Facts here were checked in November 2026. If web search is available and the audit is going to leadership or legal, run one search for "CCPA dark patterns order" and "dark patterns guidelines amendment" to catch newer orders or added patterns. Mention anything new in the report's method section.

## Contents
- Does the regime apply?
- Provisions catalogue
- Consequences ladder
- Severity rubric (scoring)
- Confidence levels
- Enforcement precedents
- Wording rules for findings
- Sources

---

## Does the regime apply?

The Guidelines apply to:
- platforms systematically offering goods or services in India;
- advertisers;
- sellers.

Before the audit, establish whether the product is offered to users in India: pricing in ₹, an Indian app store listing, Indian delivery, or an Indian entity.

- **Offered in India**: frame consequences as real exposure.
- **Not offered in India**: still run the full audit. The 13 patterns are a sound deceptive-design benchmark, and similar rules exist elsewhere (EU DSA and UCPD, US FTC, and others). Label legal consequences as "exposure if offered in India", and say so in the summary.
- **Unknown**: ask once. If there's no answer, assume India and state the assumption.

## Provisions catalogue

Cite these in a finding's `provisions` list. Use the short forms shown.

| Short form | What it is | Engaged by |
|---|---|---|
| Dark Patterns Guidelines 2023, s.4 + Annexure 1 item N | General prohibition plus the specific pattern | Every finding |
| CPA 2019, s.2(47) | Unfair trade practice | Almost every finding |
| CPA 2019, s.2(28) | Misleading advertisement | False urgency, bait and switch, drip pricing, disguised ads, "free" claims |
| CPA 2019, s.2(9) | Consumer rights (to be informed, to choose) | Forced action, subscription trap, interface interference |
| E-Commerce Rules 2020, r.4(3) | E-commerce entities must not adopt unfair trade practices | Any finding on an e-commerce platform |
| E-Commerce Rules 2020, r.4(9) | No automatic recording of consent, including pre-ticked boxes | Basket sneaking, pre-ticked consents, forced action |
| Misleading Ads Guidelines 2022 | Bait ads, free claims, endorsement disclosures | Disguised ads, bait and switch, "free" drip pricing |
| DPDP Act 2023, s.5–6 | Notice, and free, specific, informed, unambiguous consent through clear affirmative action | Pre-ticked or bundled consents, forced data sharing, trick questions on consent. Consent and notice obligations apply from 13 May 2027 (DPDP Rules notified 13–14 Nov 2025). Before then, frame as "upcoming exposure". |
| RBI e-mandate framework | Recurring payments, including pre-debit notification | SaaS billing, subscription trap (check the current circular) |
| IT Act 2000, ss.43, 66 | Unauthorised access and damage, computer offences | Rogue malware |
| ASCI deceptive design guidelines (June 2023) | Self-regulatory code on drip pricing, bait and switch, false urgency, disguised ads | Advertising-side findings (complaint and reputational route) |

## Consequences ladder

The Guidelines have no penalty table of their own. Enforcement runs through the CPA. These are the possible exposures, from mild to severe.

1. **Notice and investigation**: the CCPA can act on complaints or on its own (suo motu) and issue show-cause notices. Since 2025 it has also asked platforms to self-audit and self-declare compliance.
2. **Corrective directions (CPA s.20)**: orders to discontinue the practice, modify the interface, refund or reimburse consumers, or recall goods or withdraw services.
3. **Advertisement directions and penalties (CPA s.21)**: orders to discontinue or modify misleading ads, and penalties of up to ₹10 lakh for a first contravention and up to ₹50 lakh for each subsequent one. Endorsers can be barred from endorsing (up to 1 year, or 3 years for repeat contraventions).
4. **Criminal exposure for false or misleading ads (CPA s.89)**: imprisonment of up to 2 years and a fine of up to ₹10 lakh, rising to 5 years and ₹50 lakh for subsequent offences. Reserve this for clearly false claims, such as fake scarcity or a fake "free" claim.
5. **Non-compliance with CCPA directions (CPA s.88)**: imprisonment of up to 6 months, a fine of up to ₹20 lakh, or both.
6. **Consumer commission complaints and class actions**: individual or class complaints seeking refunds and compensation.
7. **Data protection (DPDP Act, from 13 May 2027)**: penalties of up to ₹50 crore for breaches of general obligations such as consent, and higher caps for security and children's-data failures.
8. **Sector regulators**: IRDAI has told insurers to check for dark patterns, and SEBI has proposed aligning its advertising code. Regulated entities face an extra layer.
9. **Non-legal**: app-store review rejection, press coverage of CCPA orders (they're published and named), loss of user trust, and chargebacks.

Two enforcement facts to state when relevant:
- Published CCPA penalties so far have been modest, roughly ₹1–7 lakh per platform. The CCPA has said that fixing an interface after a notice does not erase the earlier violation. In the PharmEasy order, it called post-notice fixes reactive.
- The penalty factors visible in orders include:
  - the number and nature of patterns;
  - duration and scale;
  - the number of consumers affected;
  - the platform's reach;
  - money linked to the practice;
  - the vulnerability of the consumer group.

  The severity rubric below mirrors these factors on purpose.

## Severity rubric (scoring)

Score every finding on four dimensions. `build_report.py` adds them up and assigns the severity, so the same UI gets the same rating whoever runs the audit. Record the reasoning for each score in the finding.

**Harm (0–4)**: what the user stands to lose.
- 4: money leaves the user without informed, affirmative consent, or the device or data is compromised.
- 3: a money decision is materially steered (purchase, upgrade, renewal, add-on), or the user is blocked from something already paid for.
- 2: a personal-data or consent decision is steered, or the user is misled without a direct charge (for example an unlabelled ad).
- 1: friction, annoyance or wasted time only.
- 0: no consumer detriment. Don't log it as a finding; mention it as a good-practice note if useful.

**Match (0–3)**: how clearly it fits the law.
- 3: mirrors an Annexure 1 illustration, or the facts of a published CCPA order.
- 2: clearly meets the wording of a pattern definition or limb.
- 1: arguable. Depends on facts not visible (the confidence is then usually `needs_verification`).
- 0: doesn't meet any definition. Not a finding.

**Position (0–2)**: where in the journey it happens.
- 2: checkout, payment, renewal, cancellation, or trial-to-paid conversion.
- 1: sign-up, onboarding, consent, permissions, or account settings.
- 0: browsing, content, or marketing pages.

**Amplifiers (+1 each, maximum +3)**:
- `default_for_all`: hits every user by default, rather than an edge case or a single campaign.
- `vulnerable_audience`: children or students, elderly users, health, insurance or credit decisions, financial distress, or first-time digital users.
- `stacked`: combined with another dark pattern on the same screen or step.
- `hard_to_reverse`: non-refundable charge, data shared onward, offline-only reversal, or a recurring charge.

**Total score to severity**

| Score | Severity | Meaning for the team |
|---|---|---|
| 10–12 | Critical | Release-blocking. Fix before the next deploy, or hotfix if live. Highest likelihood of a CCPA notice and penalty. |
| 7–9 | High | Fix in the current sprint. Clear exposure if a complaint or sweep lands. |
| 4–6 | Medium | Schedule for the next release. Real but lower-impact exposure. |
| 1–3 | Low | Backlog, or fix through design-system guidance. Mostly a trust and quality issue. |

**Overrides**: rogue malware is always Critical. Any other override needs an `override_reason` in the finding. Use one sparingly, for example to lift a finding when the CCPA has publicly targeted that exact flow in the same sector.

**Worked calibrations**:
- Paid membership pre-added at checkout for everyone: harm 4 + match 3 + position 2 + default_for_all 1 = **10, Critical**.
- "No, I'll stay unprotected" on an insurance opt-out at checkout: harm 3 + match 3 + position 2 = **8, High**.
- Recurring countdown on a coaching landing page: harm 3 + match 3 + position 0 + vulnerable_audience + default_for_all 2 = **8, High**.
- Cancellation only by emailing support, recurring charge: harm 3 + match 3 + position 2 + hard_to_reverse 1 = **9, High**. Add default_for_all and it becomes **10, Critical**.
- App-install banner returning on every page: harm 1 + match 3 + position 0 = **4, Medium**.
- Pre-ticked marketing consent at sign-up: harm 2 + match 3 + position 1 + default_for_all 1 = **7, High**.

## Confidence levels

Severity is how bad it would be. Confidence is how sure the audit is that it's happening. Keep them separate.

- `confirmed`: directly visible in the evidence, such as copy on screen, a checked box in the DOM, or a timer that resets on reload.
- `likely`: strongly indicated, but one fact is inferred. For example, a Figma default state is "on" but the PRD is silent.
- `needs_verification`: depends on data the audit can't see (inventory, logs, payment behaviour). Say exactly what evidence would settle it and who has it.

The report shows both. A Critical `needs_verification` finding is a priority to verify, not a confirmed breach.

## Enforcement precedents

Published CCPA actions useful as "match = 3" anchors (summarised from orders reported up to September 2026):

| Platform | What the UI did | Pattern(s) | Outcome reported |
|---|---|---|---|
| Zepto | Paid membership auto-added; handling and membership fees appear at checkout | Basket sneaking, drip pricing | Penalty. Later changes didn't absolve past violations. |
| PhysicsWallah | ₹10 donation pre-selected, plus emotional retention copy | Basket sneaking, confirm shaming | Penalty |
| PharmEasy | Membership auto-added | Basket sneaking | Penalty. Post-notice fixes called reactive. |
| BookMyShow | Pre-ticked charity contribution | Basket sneaking | Corrective directions, no disclosed penalty |
| SpiceJet | Pre-ticked loyalty enrolment, default promo consent | Forced action, interface interference | Reported in enforcement summary |
| FirstCry | "Tax-inclusive" prices, GST added at checkout | Drip pricing | Reported in enforcement summary |
| McAfee | "Renew Now" vs "Accept Risk", grey decline vs red renew | Confirm shaming, interface interference | Penalty (reported with PhysicsWallah) |
| IndiGo | "No I will take risk" opt-out | Confirm shaming | Corrective directions; changed to neutral copy |
| Anuj Jindal (coaching) | Recurring 24-hour countdown, "claim your free spot" | False urgency | Reported in enforcement summary |

Context worth citing:
- June 2025: CCPA advisory telling platforms to self-audit within 3 months.
- By November 2025: 26 platforms had filed self-declarations.
- Since then: penalties against 7 platforms and corrective directions to 2, around ₹20 lakh in total.

Don't state a precedent's penalty amount unless the source gives it.

## Wording rules for findings

- Say "likely to be treated as", "risks being found to be", "engages". Avoid "is illegal" or "violates". The CCPA decides.
- Name the limb: "drip pricing, limb (i), fees not revealed upfront", not just "drip pricing".
- Don't invent facts. If you didn't see it, it's `needs_verification`.
- Every report ends with: "This audit is a design-compliance review, not legal advice. Have counsel confirm before relying on it for legal decisions."

## Sources

- Guidelines for Prevention and Regulation of Dark Patterns, 2023, CCPA notification F. No. CCPA-1/1/2023-CCPA (Reg), 30 Nov 2023 (Gazette of India).
- Consumer Protection Act, 2019, ss.2, 18, 20, 21, 88, 89.
- Consumer Protection (E-Commerce) Rules, 2020, r.4.
- Digital Personal Data Protection Act, 2023, and DPDP Rules, 2025 (notified November 2025; consent provisions from 13 May 2027).
- Lex Consult, "From nudge to notice", Bar & Bench, 1 Sep 2026, for the summary of CCPA orders and penalty factors.
- Fox Mandal note on the PhysicsWallah and McAfee orders. Law.asia on the June 2025 self-audit advisory and sector regulators.
