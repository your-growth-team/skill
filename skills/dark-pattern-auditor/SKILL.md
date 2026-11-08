---
name: dark-pattern-auditor
description: Audit a live website URL, screenshots, or a Figma file (mobile or web mockups) for dark patterns under India's CCPA Guidelines for Prevention and Regulation of Dark Patterns, 2023, covering all 13 specified patterns (false urgency, basket sneaking, confirm shaming, forced action, subscription trap, interface interference, bait and switch, drip pricing, disguised ads, nagging, trick questions, SaaS billing, rogue malware). Produces an interactive HTML report that marks each problem on recreated screens, scores severity, maps the likely breach and Consumer Protection Act consequences, and shows a compliant fix with copy and acceptance criteria. Use whenever someone wants a site, app, checkout, paywall, onboarding, consent or cancellation flow, or Figma design checked for dark patterns, deceptive or manipulative UX, or CCPA or consumer-protection compliance, including when a URL or figma.com link is shared with "could this get us in trouble", even without the words "dark pattern".
---

# Dark pattern auditor

This skill turns a URL or a Figma link into a dark-pattern audit that product managers, designers and developers can act on. The output is one self-contained HTML report containing:
- a verdict and the fixes to do first;
- each finding, scored for severity, mapped to the clause it likely breaches, with consequences and a fix;
- recreated screens with the problems outlined, and a switch to a compliant version (the "prototype" of the fix);
- a coverage table showing what was found, cleared or unverifiable for all 13 patterns;
- method, limitations and a disclaimer.

The audience is product people, not lawyers. Be precise about the law, plain in the language, and honest about what the evidence does and doesn't show.

## Files in this skill

| File | Read it when |
|---|---|
| `references/patterns.md` | Always, in full, before judging anything. It holds the definitions, signals, false-positive guards, fixes and precedents for all 13 patterns. |
| `references/legal-and-severity.md` | Always, before scoring. It holds provisions, the consequences ladder, the scoring rubric and enforcement precedents. |
| `references/capture.md` | Before capturing evidence. It covers website capture modes, the Figma playbook, journeys to cover, and how to write the HTML recreations. |
| `scripts/capture_site.py` | Live sites, when a browser can reach the site (Claude Code or Cowork). Screenshots, rendered DOM, live checked boxes, ticking or resetting timers, button contrast. |
| `scripts/scan_signals.py` | On any captured HTML or text. A quick list of leads by pattern. |
| `scripts/build_report.py` | To validate the audit JSON, compute severity, inline images and render the report. |
| `assets/example-audit.json` | Before writing your own audit JSON: a complete worked example (10 findings, 2 screens, recreations, coverage) showing the expected depth and tone. |
| `assets/report-template.html`, `assets/patterns.json` | Used by the builder. Don't hand-edit the report HTML. Change the JSON and rebuild. |

## Workflow

### 1. Scope

Work out four things. Don't interrogate the user. Infer what you can, and ask at most one short question if something essential is missing (usually the link itself).

- **Target**: a URL, a Figma link (file, page, section or frame), or uploaded screenshots.
- **Journeys in scope**: default to every journey in `capture.md` that exists in the product. If the user named one ("just the checkout"), audit that one, list the others as out of scope, and still note anything glaring you saw in passing.
- **India applicability**: is the product offered to users in India? If unclear, assume yes and say so. See "Does the regime apply?" in `legal-and-severity.md`.
- **Requester's role** (PM, design, dev), if obvious. The report has role filters, so this only shapes your chat summary.

### 2. Capture evidence

Follow `references/capture.md`. Pick the strongest mode available and note which one you used:
- **Live site with a browser** (Claude Code, Cowork, Claude in Chrome): run `capture_site.py` or walk the journeys.
- **Live site, fetch only** (claude.ai): `web_fetch` the pages, run `scan_signals.py` on the saved text, and ask once for screenshots of flows you can't reach.
- **Figma**: map frames with `get_metadata`, view them with `get_screenshot`, and read copy and properties where needed.

Never complete payments, start paid trials or submit real personal data while capturing.

### 3. Review all 13 patterns

Read `references/patterns.md` in full. Then go screen by screen, and for each screen walk through the ten screening questions and the signals for every pattern. Scanner output is a list of leads, not findings: confirm or discard each lead against the pattern's definition and its "Not a dark pattern when" section.

For every pattern, end with one of four outcomes:
- one or more **findings**;
- **clear** (you looked and saw no issue);
- **not_verifiable** (the evidence needed isn't available; say what is needed);
- **not_assessed** (out of scope; say why).

The coverage table is what makes the audit trustworthy. A blank pattern looks like it was forgotten.

One UI element can carry several findings. For example, a pre-ticked donation with a shaming opt-out is basket sneaking and confirm shaming. Log each pattern as its own finding with its own fix, and add the `stacked` amplifier.

### 4. Score each finding

Use the rubric in `references/legal-and-severity.md`:
- harm 0–4;
- match 0–3;
- position 0–2;
- up to three amplifiers.

Write a one-sentence rationale. Set confidence separately (`confirmed`, `likely` or `needs_verification`). Give every `needs_verification` finding a `verify` note: what data settles it, and who has it. Don't set severity yourself; the builder computes it from the score so ratings are consistent across auditors.

### 5. Write the fix

For each finding, write:
- a one-paragraph fix summary;
- before and after copy, where copy is involved;
- testable acceptance criteria a developer or QA can check (two to four bullets);
- owners (`PM`, `Design`, `Dev`, `Legal`).

Base fixes on the "Compliant alternative" in `patterns.md`, adapted to this product's actual UI. A good fix keeps the business goal where it can. Offering an add-on is fine; pre-selecting it isn't.

### 6. Recreate the screens

For each screen with findings, write `current_html` (the problem elements carry `data-dp="F1"`) and `compliant_html` (the fixed elements carry `data-fix="F1"`), following "Recreating screens in HTML" in `capture.md`. Keep each one short and faithful to real copy, prices and visual hierarchy. If you have a real screenshot file, also set `image` and give findings `boxes` (percent coordinates; `capture_site.py` outputs these).

### 7. Build and deliver

Write `audit.json` (format below), then run:

```bash
python <skill-dir>/scripts/build_report.py audit.json --check     # scoring table and warnings
python <skill-dir>/scripts/build_report.py audit.json --out dark-pattern-audit-<target>-<YYYY-MM-DD>.html
```

Fix every ERROR. Read every WARNING and fix the ones that matter, such as an unmarked finding, missing acceptance criteria, or a not_verifiable pattern without a note.

Deliver:
- **claude.ai with the Artifact tool**: save the HTML under `/mnt/user-data/outputs/` and publish it. It's self-contained and theme-aware, so the user gets a shareable link.
- **Otherwise**: save it to the outputs or working folder and present the file.

In chat, keep it short:
- the verdict;
- the counts by severity;
- the top 3 fixes;
- the biggest limitation, if any;
- a pointer to the report.

Don't repeat the whole report in chat.

Optional follow-ups, only when the user asks: write findings into Figma as annotations (see `capture.md`), or turn findings into tickets in their tracker, one per finding, with severity, fix and acceptance criteria.

## Audit data format

```json
{
  "meta": {
    "title": "Dark pattern audit: Checkout and subscriptions",
    "target_name": "Acme Grocery",
    "target": "https://acme.example",
    "target_type": "website",
    "audited_on": "2026-11-02",
    "auditor": "Claude for Vaastav",
    "scope": ["Product page", "Cart", "Checkout review", "Membership cancel"],
    "applicability": "Acme sells to consumers in India, so the CCPA Guidelines apply."
  },
  "summary": {
    "verdict": "Checkout adds a paid membership by default and reveals fees late. Both are patterns the CCPA has already penalised.",
    "overview": "Six findings across four screens. Cancellation is reachable online but takes five steps.",
    "top_actions": ["Untick the membership and donation by default", "Show all fees on the product page", "Cut cancellation to two steps"]
  },
  "screens": [{
    "id": "S1", "name": "Checkout review", "device": "mobile", "source": "https://acme.example/checkout",
    "image": "capture/03-checkout.jpg",
    "current_html": "<div data-dp=\"F1\"><label><input type=checkbox checked> Acme Plus ₹99/mo</label></div>",
    "compliant_html": "<div data-fix=\"F1\"><label><input type=checkbox> Add Acme Plus for ₹99/mo</label></div>"
  }],
  "findings": [{
    "id": "F1",
    "title": "Paid membership pre-selected at checkout",
    "pattern": "basket_sneaking",
    "limb": "paid add-on added without consent",
    "screen_id": "S1",
    "boxes": [{"x": 4, "y": 52, "w": 92, "h": 7}],
    "evidence": "Acme Plus (₹99/month) is ticked by default on the checkout review screen. The order total includes it.",
    "why": "A paid item the user didn't choose is in the basket by default. The Guidelines treat a pre-ticked paid add-on as basket sneaking, and pre-ticked consent is barred by E-Commerce Rule 4(9).",
    "provisions": ["Dark Patterns Guidelines 2023, s.4 + Annexure 1 item 2", "CPA 2019, s.2(47)", "E-Commerce Rules 2020, r.4(9)"],
    "confidence": "confirmed",
    "score": {"harm": 4, "match": 3, "position": 2, "amplifiers": ["default_for_all"], "rationale": "Money is charged by default at payment for every user; mirrors illustration (a) and the Zepto and PharmEasy orders."},
    "consequences": "Optional: a product-specific consequence. The template adds the standard consequence for the severity.",
    "precedent": "Zepto, PharmEasy (membership auto-added); BookMyShow (pre-ticked contribution).",
    "fix": {
      "summary": "Show Acme Plus as an unticked offer with its price. Add it only when the user ticks it, and update the total visibly.",
      "copy_before": "Acme Plus ₹99/mo (ticked)",
      "copy_after": "Add Acme Plus for ₹99/month? Free delivery on every order. (unticked)",
      "acceptance_criteria": [
        "On a fresh session, the checkout total equals the chosen items plus disclosed fees",
        "Acme Plus enters the cart only through an explicit user tap",
        "The membership checkbox renders unchecked in all checkout entry points"
      ],
      "dev_notes": "Remove the defaultChecked prop; drop the server-side auto-attach in the cart service.",
      "owners": ["PM", "Design", "Dev"]
    }
  }],
  "coverage": {
    "false_urgency": {"status": "clear", "note": "No timers or scarcity claims on audited pages."},
    "saas_billing": {"status": "not_verifiable", "note": "Need renewal-reminder emails and billing logs to confirm pre-debit notice."}
  },
  "method": {
    "capture": "Live site captured with capture_site.py on mobile emulation, 2 Nov 2026; fresh-session timer check run.",
    "limitations": ["Logged-in account pages not audited.", "Payment page not reached (no test card)."],
    "sources": ["CCPA Dark Patterns Guidelines 2023", "Consumer Protection Act 2019"]
  }
}
```

Notes on the fields:
- Pattern ids are the `id`s in `assets/patterns.json`.
- Amplifier ids: `default_for_all`, `vulnerable_audience`, `stacked`, `hard_to_reverse`.
- Finding ids run F1, F2, and so on. Screen ids run S1, S2, and so on.
- A finding without a `screen_id` is allowed for journey-level issues, such as "no cancel flow exists in the designs".
- In JSON strings, escape the double quotes inside HTML attributes, or use single quotes in the HTML.

## Judgement guardrails

- **Evidence first.** Every finding names what was seen and where. If it depends on data you couldn't see (real stock, billing logs, what a button does), mark it `needs_verification` and say what's needed. Don't round up suspicion into a confirmed breach.
- **Avoid false positives.** Highlighting a recommended plan, a genuine sale end date, a clearly labelled ad, or a necessary disclosed fee isn't a dark pattern. Check each pattern's "Not a dark pattern when" section. A report that flags everything teaches teams to ignore it.
- **Use legal language carefully.** Say "likely to be treated as", "risks", "engages". Never say "illegal". The CCPA's interpretation is final, and the Guidelines call their illustrations guidance. End with the disclaimer.
- **Missing designs count.** In Figma audits, a subscription product with no cancel flow, or a trial with no reminder state, is a finding (confidence `likely`) because the pattern turns on it.
- **Stay current.** If web search is available and the report is going to leadership or legal, search once for newer CCPA dark-pattern orders or amendments (see `legal-and-severity.md`). Add anything material to the method section.
- **Audit any target the same way.** Competitors' public pages can be audited too. Keep the tone factual and never fabricate evidence.
