#!/usr/bin/env python3
"""Validate an audit JSON, compute severities, inline images, and render the HTML report.

Usage:
  python build_report.py audit.json --out dark-pattern-audit.html [--check]

--check  validate and print the scoring table only (no HTML written)

audit.json shape (see SKILL.md "Audit data format" for field meanings):
{
  "meta": {"title", "target_name", "target", "target_type": "website|figma|screenshots",
           "audited_on", "auditor", "scope": [..], "applicability"},
  "summary": {"verdict", "overview", "top_actions": [..]},
  "screens": [{"id", "name", "device": "mobile|desktop", "source", "image": "path/to.png (optional)",
               "current_html", "compliant_html", "notes"}],
  "findings": [{"id": "F1", "title", "pattern": "<pattern id>", "limb", "screen_id", "boxes": [{"x","y","w","h"}],
                "evidence", "why", "provisions": [..], "confidence": "confirmed|likely|needs_verification",
                "verify", "score": {"harm", "match", "position", "amplifiers": [..], "rationale"},
                "severity_override", "override_reason", "consequences", "precedent",
                "fix": {"summary", "copy_before", "copy_after", "acceptance_criteria": [..], "dev_notes", "owners": [..]}}],
  "coverage": {"<pattern id>": {"status": "clear|not_verifiable|not_assessed", "note"}},
  "method": {"capture", "limitations": [..], "sources": [..]},
  "disclaimer": "optional override"
}
"""
import argparse
import base64
from html import escape
import datetime as dt
import io
import json
import mimetypes
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
SEVERITIES = ["critical", "high", "medium", "low"]
AMPLIFIERS = {"default_for_all", "vulnerable_audience", "stacked", "hard_to_reverse"}
CONFIDENCE = {"confirmed", "likely", "needs_verification"}
COVERAGE_STATUS = {"clear", "not_verifiable", "not_assessed", "found"}


def severity_for(total):
    if total >= 10:
        return "critical"
    if total >= 7:
        return "high"
    if total >= 4:
        return "medium"
    return "low"


def inline_image(path_str, base_dir, max_width=1400):
    if not path_str or path_str.startswith("data:"):
        return path_str
    p = Path(path_str)
    if not p.is_absolute():
        p = (base_dir / p).resolve()
    if not p.exists():
        raise FileNotFoundError(f"image not found: {p}")
    try:
        from PIL import Image
        im = Image.open(p)
        im = im.convert("RGB")
        if im.width > max_width:
            im = im.resize((max_width, int(im.height * max_width / im.width)))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=78, optimize=True)
        data, mime = buf.getvalue(), "image/jpeg"
    except ImportError:
        data, mime = p.read_bytes(), mimetypes.guess_type(str(p))[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(data).decode()


def validate_and_score(audit, pattern_ids):
    errors, warnings = [], []
    screens = audit.get("screens") or []
    screen_ids = {s.get("id") for s in screens}
    for s in screens:
        if not s.get("id") or not s.get("name"):
            errors.append(f"screen missing id/name: {s}")
        if not (s.get("current_html") or s.get("image")):
            warnings.append(f"screen {s.get('id')}: no current_html or image — nothing to show")
        if s.get("current_html") and not s.get("compliant_html"):
            warnings.append(f"screen {s.get('id')}: no compliant_html — the fix won't be shown in context")
        if s.get("device") not in (None, "mobile", "desktop"):
            errors.append(f"screen {s.get('id')}: device must be mobile or desktop")

    ids = set()
    for f in audit.get("findings") or []:
        fid = f.get("id", "?")
        if fid in ids:
            errors.append(f"duplicate finding id {fid}")
        ids.add(fid)
        for k in ("title", "pattern", "evidence", "why", "confidence", "score", "fix"):
            if not f.get(k):
                errors.append(f"{fid}: missing '{k}'")
        if f.get("pattern") and f["pattern"] not in pattern_ids:
            errors.append(f"{fid}: unknown pattern '{f['pattern']}' (use one of {sorted(pattern_ids)})")
        if f.get("confidence") and f["confidence"] not in CONFIDENCE:
            errors.append(f"{fid}: confidence must be one of {sorted(CONFIDENCE)}")
        if f.get("confidence") == "needs_verification" and not f.get("verify"):
            warnings.append(f"{fid}: needs_verification but no 'verify' note saying what evidence would settle it")
        if f.get("screen_id") and f["screen_id"] not in screen_ids:
            errors.append(f"{fid}: screen_id '{f['screen_id']}' not in screens")
        if not f.get("provisions"):
            warnings.append(f"{fid}: no provisions listed")
        fix = f.get("fix") or {}
        if not fix.get("acceptance_criteria"):
            warnings.append(f"{fid}: fix has no acceptance_criteria — developers need testable criteria")
        for b in f.get("boxes") or []:
            if not all(k in b for k in ("x", "y", "w", "h")):
                errors.append(f"{fid}: box needs x,y,w,h percentages")

        sc = f.get("score") or {}
        try:
            harm, match, pos = int(sc.get("harm")), int(sc.get("match")), int(sc.get("position"))
        except (TypeError, ValueError):
            errors.append(f"{fid}: score needs integer harm, match, position")
            continue
        if not (0 <= harm <= 4 and 0 <= match <= 3 and 0 <= pos <= 2):
            errors.append(f"{fid}: score out of range (harm 0-4, match 0-3, position 0-2)")
        if harm == 0 or match == 0:
            errors.append(f"{fid}: harm or match is 0 — per the rubric this is not a finding")
        amps = sc.get("amplifiers") or []
        bad = [a for a in amps if a not in AMPLIFIERS]
        if bad:
            errors.append(f"{fid}: unknown amplifiers {bad} (use {sorted(AMPLIFIERS)})")
        total = harm + match + pos + min(len(set(amps)), 3)
        f["score_total"] = total
        sev = severity_for(total)
        if f.get("pattern") == "rogue_malware":
            sev = "critical"
        ov = f.get("severity_override")
        if ov:
            if ov not in SEVERITIES:
                errors.append(f"{fid}: severity_override must be one of {SEVERITIES}")
            elif not f.get("override_reason"):
                errors.append(f"{fid}: severity_override requires override_reason")
            else:
                sev = ov
        if f.get("severity") and f["severity"] != sev and not ov:
            warnings.append(f"{fid}: severity '{f['severity']}' replaced by computed '{sev}' (score {total})")
        f["severity"] = sev

    # data-dp references in screens should point at real findings
    for s in screens:
        for attr in ("data-dp", "data-fix"):
            for m in re.finditer(attr + r'="([^"]+)"', s.get("current_html", "") + s.get("compliant_html", "")):
                for ref in m.group(1).split():
                    if ref not in ids:
                        warnings.append(f"screen {s.get('id')}: {attr} references unknown finding {ref}")
    referenced = set()
    for s in screens:
        referenced |= set(" ".join(re.findall(r'data-dp="([^"]+)"', s.get("current_html", ""))).split())
    for f in audit.get("findings") or []:
        if f.get("screen_id") and f["id"] not in referenced and not f.get("boxes"):
            warnings.append(f"{f['id']}: not marked on its screen (no data-dp in current_html and no boxes)")

    # coverage: all 13 should be addressed
    cov = audit.setdefault("coverage", {})
    found = {f.get("pattern") for f in audit.get("findings") or []}
    for pid in pattern_ids:
        entry = cov.get(pid)
        if pid in found:
            continue
        if not entry or entry.get("status") not in COVERAGE_STATUS - {"found"}:
            warnings.append(f"coverage: '{pid}' has no finding and no clear/not_verifiable status — marked not_assessed")
            cov[pid] = {"status": "not_assessed", "note": (entry or {}).get("note", "")}
        elif entry.get("status") == "not_verifiable" and not entry.get("note"):
            warnings.append(f"coverage: '{pid}' not_verifiable without a note on what's needed")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audit")
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    audit_path = Path(args.audit).resolve()
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    patterns = json.loads((ASSETS / "patterns.json").read_text(encoding="utf-8"))
    pattern_ids = [p["id"] for p in patterns["patterns"]]

    errors, warnings = validate_and_score(audit, pattern_ids)
    print("Findings:")
    for f in sorted(audit.get("findings") or [], key=lambda f: (SEVERITIES.index(f.get("severity", "low")), -f.get("score_total", 0))):
        sc = f.get("score", {})
        print(f"  {f.get('id'):>4}  {f.get('severity','?'):<8} {f.get('score_total','?'):>2}/12  "
              f"(h{sc.get('harm')} m{sc.get('match')} p{sc.get('position')} +{len(sc.get('amplifiers') or [])})  "
              f"{f.get('pattern')}: {f.get('title')}")
    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        sys.exit(1)
    if args.check:
        return
    if not args.out:
        ap.error("--out is required unless --check")

    for s in audit.get("screens") or []:
        if s.get("image"):
            s["image"] = inline_image(s["image"], audit_path.parent)
    audit.setdefault("meta", {})["generated_at"] = dt.date.today().isoformat()

    def js(obj):
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

    html = (ASSETS / "report-template.html").read_text(encoding="utf-8")
    html = html.replace("/*__AUDIT_JSON__*/null", js(audit)).replace("/*__PATTERNS_JSON__*/null", js(patterns))
    title = audit["meta"].get("title") or "Dark pattern audit"
    html = html.replace("<title>Dark pattern audit</title>", f"<title>{escape(title)}</title>", 1)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    size = out.stat().st_size / 1e6
    print(f"Wrote {out} ({size:.2f} MB)")
    if size > 15:
        print("WARNING: over 15 MB — downscale or drop evidence images before publishing (16 MB limit).")


if __name__ == "__main__":
    main()
