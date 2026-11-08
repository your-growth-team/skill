#!/usr/bin/env python3
"""Scan saved HTML or text for dark-pattern *leads*.

These are leads, not findings: every hit needs human/Claude judgement against
references/patterns.md before it goes into the report.

Usage:
  python scan_signals.py page.html [more.html|.txt|.md ...] [--json out.json]
  python scan_signals.py capture_dir/            # scans every .html/.txt/.md inside

Prints a Markdown summary grouped by pattern; --json also writes machine-readable output.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup  # optional; falls back to regex-only text scanning
except ImportError:  # pragma: no cover
    BeautifulSoup = None

# (pattern_id, signal_name, regex). Case-insensitive. Keep regexes specific to limit noise.
PHRASES = [
    # False urgency
    ("false_urgency", "scarcity claim", r"\bonly\s+\d+\s+(left|remaining|seats?|rooms?|items?|spots?)\b"),
    ("false_urgency", "popularity claim", r"\b\d+\s+(people|others|users|shoppers)\s+(are\s+)?(viewing|looking|watching|bought|booked)"),
    ("false_urgency", "popularity claim", r"\bbooked\s+\d+\s+times\b|\bselling\s+fast\b|\bin\s+high\s+demand\b"),
    ("false_urgency", "time pressure", r"\b(hurry|last\s+chance|ends?\s+(soon|today|tonight|in)|offer\s+expires|limited[-\s]time|today\s+only|don'?t\s+miss\s+out)\b"),
    ("false_urgency", "timer text", r"\b\d{1,2}\s*[:h]\s*\d{2}\s*[:m]\s*\d{2}\s*s?\b"),
    # Confirm shaming
    ("confirm_shaming", "shaming decline copy", r"\bno\s+thanks?,?\s+i\s+(don'?t|do\s+not|prefer|like|want|will|'?ll)\b"),
    ("confirm_shaming", "risk/fear decline copy", r"\b(i'?ll|i\s+will)\s+(take\s+the\s+risk|stay\s+(unsecured|unprotected))|\baccept\s+risk\b|\btake\s+(the\s+)?risk\b"),
    ("confirm_shaming", "guilt copy", r"\b(i\s+don'?t\s+care|leave\s+(me|my\s+\w+)\s+unprotected|miss\s+out|you'?ll\s+lose\s+everything|charity\s+is\s+for)\b"),
    # Basket sneaking / drip pricing
    ("drip_pricing", "fee line", r"\b(convenience|platform|handling|service|processing|booking|small[-\s]cart|packaging|surge)\s+(fee|charge)s?\b"),
    ("drip_pricing", "taxes-extra language", r"\b(\+\s*taxes|taxes\s+extra|excl(\.|uding)?\s+(of\s+)?(gst|tax(es)?))\b"),
    ("drip_pricing", "inclusive-of-taxes claim (check final total)", r"\b(inclusive\s+of\s+all\s+taxes|incl\.?\s+of\s+all\s+taxes|mrp\s+incl)\b"),
    ("drip_pricing", "'free' claim (check trial / IAP disclosure)", r"\b(free\s+forever|100%\s+free|play\s+for\s+free|download\s+free|totally\s+free)\b"),
    ("basket_sneaking", "add-on / donation language", r"\b(donat(e|ion)|round[-\s]?up|protection\s+plan|insurance|extended\s+warranty|membership|tip\s+(your|the))\b"),
    # Subscription trap / SaaS billing
    ("subscription_trap", "free trial", r"\bfree\s+trial\b"),
    ("subscription_trap", "cancel-by-contact instruction", r"\bto\s+cancel,?\s+(please\s+)?(call|email|contact|write|visit)\b"),
    ("saas_billing", "auto-renew language", r"\bauto[-\s]?renew(s|al|ing)?\b|\brenews\s+automatically\b|\bautopay\b|\be-?mandate\b"),
    # Forced action
    ("forced_action", "gated access", r"\b(sign\s*up|log\s*in|register)\s+to\s+(continue|view|see|buy|checkout|unlock)\b"),
    ("forced_action", "sensitive identifier request", r"\baadhaa?r\b|\bpan\s+(card|number)\b"),
    ("forced_action", "contacts / social access", r"\b(access|sync|import|allow)\s+(your\s+)?contacts\b|\bconnect\s+(with\s+)?(facebook|google|social)\b"),
    # Nagging
    ("nagging", "app-install prompt", r"\b(download|get|open\s+in|install)\s+(the|our)?\s*app\b|\bcontinue\s+in\s+app\b|\bopen\s+app\b"),
    ("nagging", "notification ask", r"\b(turn\s+on|enable|allow)\s+(push\s+)?notifications\b"),
    ("nagging", "deferral-only option", r"\b(maybe\s+later|not\s+now|remind\s+me\s+later)\b"),
    # Trick question
    ("trick_question", "negated consent wording", r"\b(uncheck|untick)\s+(this|the\s+box)?\s*(if|to)\b|\bdo\s+not\s+(un)?subscribe\b|\bopt\s+out\s+of\s+not\b|\bdon'?t\s+(not|un)"),
    ("trick_question", "opt-out question", r"\bopt\s+out\s+of\s+(receiving|getting)\b"),
    # Disguised ads
    ("disguised_advertisement", "ad label present (check prominence & coverage)", r"\b(sponsored|promoted|advertisement|paid\s+partnership)\b"),
    # Rogue malware
    ("rogue_malware", "scareware language", r"\b(virus|malware|trojan)s?\s+(detected|found)\b|\byour\s+(device|phone|computer|pc)\s+(is|may\s+be)\s+(infected|at\s+risk)\b|\bscan\s+now\b"),
]
COMPILED = [(p, s, re.compile(r, re.I)) for p, s, r in PHRASES]



def snippet(text, start, end, pad=60):
    a, b = max(0, start - pad), min(len(text), end + pad)
    return re.sub(r"\s+", " ", text[a:b]).strip()


def scan_text(text, source):
    hits = []
    for pattern, signal, rx in COMPILED:
        for m in rx.finditer(text):
            hits.append({
                "pattern": pattern,
                "signal": signal,
                "match": m.group(0),
                "context": snippet(text, m.start(), m.end()),
                "source": source,
            })
    return hits


def label_for(inp, soup):
    """Best-effort label text for an input."""
    if inp.get("id"):
        lab = soup.find("label", attrs={"for": inp["id"]})
        if lab:
            return lab.get_text(" ", strip=True)
    parent = inp.find_parent("label")
    if parent:
        return parent.get_text(" ", strip=True)
    sib = inp.find_next(string=True)
    return (sib or "").strip()[:160]


def scan_html(html, source):
    hits = []
    if BeautifulSoup is None:
        text = re.sub(r"<[^>]+>", " ", html)
        return scan_text(text, source)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Pre-checked inputs (static attribute; live state is captured by capture_site.py)
    for inp in soup.find_all("input"):
        typ = (inp.get("type") or "").lower()
        if typ in ("checkbox", "radio") and inp.has_attr("checked"):
            lab = label_for(inp, soup)
            if re.search(r"₹|\brs\.?\s?\d|\$|\binsur|\bdonat|\bmember|\bprotect|\bwarranty|\btip\b", lab, re.I):
                pattern, kind = "basket_sneaking", " (looks like a paid add-on)"
            elif re.search(r"offer|update|newsletter|marketing|promot|whatsapp|\bsms\b|email me|loyalty|partners?", lab, re.I):
                pattern, kind = "forced_action", " (looks like a marketing/data consent; E-Commerce Rule 4(9))"
            else:
                pattern, kind = "forced_action", ""
            hits.append({
                "pattern": pattern,
                "signal": "pre-checked %s%s" % (typ, kind),
                "match": lab[:120],
                "context": lab[:200],
                "source": source,
            })
    # Toggle-like elements marked on
    for el in soup.select('[aria-checked="true"], [role="switch"][aria-checked="true"]'):
        lab = el.get("aria-label") or el.get_text(" ", strip=True)
        hits.append({"pattern": "basket_sneaking", "signal": "toggle on by default (aria-checked)",
                     "match": lab[:120], "context": lab[:200], "source": source})
    # Timer-ish elements by class/id
    for el in soup.find_all(attrs={"class": re.compile(r"countdown|timer|clock", re.I)}):
        hits.append({"pattern": "false_urgency", "signal": "timer element (class)",
                     "match": el.get_text(" ", strip=True)[:80], "context": str(el.get("class")), "source": source})
    # Required sensitive fields
    for inp in soup.find_all("input", required=True):
        name = " ".join(filter(None, [inp.get("name"), inp.get("id"), inp.get("placeholder"), inp.get("autocomplete")]))
        if re.search(r"aadha|pan\b|dob|birth|contact", name, re.I):
            hits.append({"pattern": "forced_action", "signal": "required sensitive field",
                         "match": name[:80], "context": name[:160], "source": source})

    text = soup.get_text(" ", strip=True)
    hits.extend(scan_text(text, source))
    # Absence check: subscription language but no cancel wording at all
    if re.search(r"subscri|membership|free\s+trial|auto[-\s]?renew", text, re.I) and not re.search(r"\bcancel", text, re.I):
        hits.append({"pattern": "subscription_trap", "signal": "subscription language but no 'cancel' anywhere on page",
                     "match": "", "context": "", "source": source})
    return hits


def dedupe(hits):
    seen, out = set(), []
    for h in hits:
        key = (h["pattern"], h["signal"], h["match"].lower(), h["source"])
        if key not in seen:
            seen.add(key)
            out.append(h)
    return out


def collect(paths):
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files += sorted([f for f in p.rglob("*") if f.suffix.lower() in (".html", ".htm", ".txt", ".md")])
        elif p.exists():
            files.append(p)
        else:
            print(f"warning: {p} not found", file=sys.stderr)
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", help="write hits to this JSON file")
    args = ap.parse_args()

    hits = []
    for f in collect(args.paths):
        raw = f.read_text(encoding="utf-8", errors="ignore")
        if f.suffix.lower() in (".html", ".htm") or "<html" in raw[:500].lower():
            hits += scan_html(raw, f.name)
        else:
            hits += scan_text(raw, f.name)
    hits = dedupe(hits)

    by_pattern = {}
    for h in hits:
        by_pattern.setdefault(h["pattern"], []).append(h)
    print(f"# Dark-pattern signal scan: {len(hits)} leads (verify each one)\n")
    for pattern, items in sorted(by_pattern.items()):
        print(f"## {pattern} ({len(items)})")
        for h in items[:25]:
            ctx = f" | …{h['context']}…" if h["context"] and h["context"] != h["match"] else ""
            print(f"- [{h['source']}] {h['signal']}: \"{h['match']}\"{ctx}")
        if len(items) > 25:
            print(f"- … {len(items) - 25} more in JSON output")
        print()
    if args.json:
        Path(args.json).write_text(json.dumps(hits, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"JSON written to {args.json}")


if __name__ == "__main__":
    main()
