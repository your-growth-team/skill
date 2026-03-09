---
name: forensic-accounting
description: Perform forensic accounting analysis on a company's financials. Use this whenever a user uploads financial statements, spreadsheets, or ledgers and asks about fraud detection, earnings manipulation, red flags, audit concerns, suspicious patterns, or financial irregularities. Also trigger for questions about Benford's Law analysis, ratio-based anomaly detection, or any request to "check the books" of a company.
---

# Forensic Accounting Skill

## Workflow

1. **Ingest** — Ask the user for financial statements (3+ years preferred). Accept CSV, Excel, or PDF.
2. **Statistical Tests** — Run Benford's Law on transaction data. Flag digit distribution anomalies. See `references/benfords-law.md` for methodology.
3. **Ratio Analysis** — Compute the forensic ratios in `references/red-flag-ratios.md` and flag any outside normal ranges.
4. **Narrative Review** — Scan for qualitative red flags using `references/qualitative-checklist.md`.
5. **Classify Findings** — Rate each finding: High / Medium / Low risk.
6. **Produce Report** — Executive Summary → Findings Table → Recommended Next Steps.

## Hard Rules
- Never give a legal conclusion — frame all findings as "indicators warranting further investigation"
- Always caveat that this is not a substitute for a licensed forensic auditor
- If data is insufficient for a finding, say so explicitly rather than speculating
