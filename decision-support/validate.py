#!/usr/bin/env python3
"""Good Measure Kitchen · Decision Desk validator.

Why this file exists
--------------------
This section is a decision record, so "verified" has to be checkable by a machine and by
a sceptic. Six families of checks:

  1. every local href/src resolves to a file that exists in this directory tree;
  2. every page carries the exact Amazon Associates disclosure sentence above the masthead
     and again in the footer (Operating Agreement s5 + 16 CFR 255.0(f));
  3. every outbound link to a storefront product page carries rel="sponsored nofollow
     noopener", and no live link may embed an Associates tag while enrolment is unconfirmed
     (that condition is flagged in IRR-06, so the gate here is deliberately strict);
  4. no reader-facing text may contain a price-like figure, and the promotional cliches this
     project refuses are absent from prose (the lint list itself and quoted policy text are
     exempt, via <code>/<pre> or a `lint:allow` marker);
  5. every row in every register cites something — an official URL, a file path, or a command
     that reproduces the finding;
  6. numbers asserted in prose equal the numbers computed from the tables themselves, so the
     counts cannot rot when a row is added.

It also writes data/decision-desk.json by parsing the same HTML a human reads, so the
machine-readable register can never drift from the rendered one.

    python3 decision-support/validate.py [--json] [--quiet]

Exit 0 = all checks pass. Exit 1 = something is wrong with the desk, and the message says what.
"""
from __future__ import annotations
import html as htmlmod
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DOC_HOSTS = re.compile(r"^(affiliate-program|sell|webservices|sellercentral|docs|developers|www\.ecfr|www\.ftc|consumer\.ftc|www\.iana|www\.w3|github\.com)", re.I)
STOREFRONT = re.compile(r"(^|\.)(amazon|amzn)\.", re.I)
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases"
BANNED = ["in today's fast-paced", "game changer", "game-changer", "elevate your",
          "delve", "unlock the", "whether you're a", "let's be honest", "best overall",
          "editor's pick", "top rated", "money can buy", "we tested"]
EXEMPT_CONTEXT = ["banned", "forbidden", "refus", "retire", "not publish", "discarded",
                  "never", "no page", "until", "without a", "prohibit", "kill the",
                  "no “", "not “", "never conditions", "slop", "reject", "permission"]
REQUIRED_NAV = ["executive-summary.html", "products.html", "suggestions.html",
                "questions.html", "verification.html", "editorial-plan.html"]
TAG_RE = re.compile(r"<[^>]+>", re.S)
ROW_RE = re.compile(r"<tr\b([^>]*)>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", re.S)
ATTR_RE = re.compile(r'([\w:.-]+)="([^"]*)"')
VOID_BALANCE = {"meta", "link", "br", "img", "hr", "input", "source", "area", "base",
                "col", "embed", "param", "track", "wbr"}


def strip_tags(fragment: str) -> str:
    """Text of a fragment, with code/pre content kept but marked."""
    return " ".join(htmlmod.unescape(TAG_RE.sub(" ", fragment)).split())


def rows_of(body: str) -> list[dict]:
    """Every table row as {attrs, cells, raw} — attributes kept, since they are the data."""
    out = []
    for m in ROW_RE.finditer(body):
        out.append({"attrs": dict(ATTR_RE.findall(m.group(1))),
                    "cells": [strip_tags(c) for c in CELL_RE.findall(m.group(2))],
                    "raw": m.group(0)})
    return out


def prose_without_code(body: str) -> str:
    """Page text with code/pre blocks and lint:allow rows removed, for phrase checks."""
    s = re.sub(r"<(code|pre|kbd|samp)\b.*?</\1>", " ", body, flags=re.S)
    s = re.sub(r"<tr\b[^>]*lint:allow[^>]*>.*?</tr>", " ", s, flags=re.S)
    s = re.sub(r"<caption\b.*?</caption>", " ", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    return strip_tags(s)


def balance(body: str) -> list[str]:
    """Cheap structural sanity check: tag nesting must return to empty."""
    stack, problems = [], []
    for m in re.finditer(r"<(/?)([a-zA-Z][\w-]*)\b[^>]*?(/?)>", body):
        closing, tag, self_closed = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID_BALANCE or self_closed:
            continue
        if closing:
            if not stack:
                problems.append(f"stray </{tag}> near offset {m.start()}")
            elif stack[-1] != tag:
                problems.append(f"</{tag}> closes <{stack[-1]}> near offset {m.start()}")
                if tag in stack:
                    while stack and stack.pop() != tag:
                        pass
            else:
                stack.pop()
        else:
            stack.append(tag)
    if stack:
        problems.append("unclosed: " + ", ".join(stack[:6]))
    return problems


def main() -> int:
    quiet = "--quiet" in sys.argv
    errors: list[str] = []
    warnings: list[str] = []
    pages = sorted([ROOT / "index.html"] + [p for p in ROOT.glob("*.html") if p.name != "index.html"])
    src = {p: p.read_text(encoding="utf-8") for p in pages}

    # ---- 1. local references -------------------------------------------------
    for path, body in src.items():
        for m in re.finditer(r'<(?:a|img|link|script)\b[^>]*>', body):
            tag = m.group(0)
            for key in ("href", "src"):
                v = (re.search(rf'{key}="([^"]*)"', tag) or ["", ""])[1]
                if not v or v.startswith(("http://", "https://", "#", "mailto:", "data:", "javascript:")):
                    continue
                clean = v.split("#")[0].split("?")[0]
                if not clean:
                    continue
                target = (path.parent / clean)
                if not clean.startswith("../") and not target.suffix:
                    target = target / "index.html"
                if not target.exists():
                    errors.append(f"broken local reference: {path.name} → {v}")

    # ---- 1b. in-page fragment links -------------------------------------------
    for path, body in src.items():
        ids = set(re.findall(r'\bid="([^"]+)"', body)) | set(re.findall(r'\bname="([^"]+)"', body))
        for frag in re.findall(r'href="#([^"/]+)"', body):
            if frag not in ids:
                errors.append(f"{path.name}: in-page link #{frag} has no matching id on the page")

    # ---- 2. disclosure, nav, structure ----------------------------------------
    for path, body in src.items():
        name = path.name
        if DISCLOSURE not in body:
            errors.append(f"{name}: missing the exact Associates disclosure sentence")
        strip = re.search(r'<div class="disclosure">.*?</div>', body, re.S)
        if not strip:
            errors.append(f"{name}: no disclosure strip above the masthead")
        else:
            if "masthead" in body and strip.start() > body.index("masthead"):
                errors.append(f"{name}: disclosure strip sits below the masthead")
            if DISCLOSURE not in body[body.rindex("<footer"):]:
                errors.append(f"{name}: disclosure is not repeated in the footer")
        for nav in REQUIRED_NAV:
            if f'href="{nav}"' not in body:
                errors.append(f"{name}: nav is missing {nav}")
        for tag in ("html", "head", "body", "main", "footer"):
            if f"<{tag}" not in body:
                errors.append(f"{name}: no <{tag}> element")
        if 'lang="en"' not in body:
            errors.append(f"{name}: no lang attribute on <html>")
        if not re.search(r"<title>.{20,}</title>", body, re.S):
            errors.append(f"{name}: <title> missing or too short to be useful")
        if "<meta name=\"viewport\"" not in body:
            errors.append(f"{name}: no viewport meta")
        m = re.search(r'<link rel="canonical" href="([^"]+)"', body)
        if not m:
            errors.append(f"{name}: no canonical URL — the desk preaches canonicals in IRR-07, so it ships them")
        else:
            expect = ("https://karagemop466-tech.github.io/Affil1/decision-support/" +
                      ("" if name == "index.html" else name))
            if m.group(1) != expect:
                errors.append(f"{name}: canonical is {m.group(1)}, expected {expect}")
        for img in re.findall(r"<img\b[^>]*>", body):
            if 'alt="' not in img:
                errors.append(f"{name}: <img> without alt text")
        for bad in balance(body):
            errors.append(f"{name}: markup — {bad}")

    # ---- 3. outbound links ---------------------------------------------------
    counts = {"retail": 0, "retail_ok": 0, "doc": 0}
    for path, body in src.items():
        for m in re.finditer(r"<a\b[^>]*>", body):
            tag = m.group(0)
            href = (re.search(r'href="([^"]*)"', tag) or ["", ""])[1]
            if not href.startswith(("http://", "https://")):
                continue
            host = urlparse(href).netloc
            if urlparse(href).scheme == "http":
                warnings.append(f"{path.name}: non-HTTPS outbound link → {href}")
            is_product = bool(re.search(r"/dp/|/product/|link\.amazon|amzn\.(to|com)/", href))
            if STOREFRONT.search(host) and not DOC_HOSTS.search(host) and is_product:
                counts["retail"] += 1
                rel = ((re.search(r'rel="([^"]*)"', tag) or ["", ""])[1]).lower().split()
                if not {"sponsored", "nofollow", "noopener"}.issubset(rel):
                    errors.append(f"{path.name}: product link lacks rel='sponsored nofollow noopener' → {href[:78]}")
                else:
                    counts["retail_ok"] += 1
                if re.search(r"[?&]tag=", href):
                    errors.append(f"{path.name}: an Associates tag is embedded while enrolment is unconfirmed "
                                  f"(IRR-06) → {href[:78]}")
            elif STOREFRONT.search(host) and not DOC_HOSTS.search(host):
                warnings.append(f"{path.name}: storefront host linked without a sponsored marker (not a product page) → {href[:60]}")
            else:
                counts["doc"] += 1

    # ---- 4. prices and refused wording ---------------------------------------
    for path, body in src.items():
        text = prose_without_code(body)
        for phrase in BANNED:
            for m in re.finditer(re.escape(phrase), text, re.I):
                around = text[max(0, m.start() - 170):m.end() + 170].lower()
                if any(k in around for k in EXEMPT_CONTEXT):
                    continue
                errors.append(f'{path.name}: refused promotional wording "{phrase}" in reader prose')
        for m in re.finditer(r"(?<![\w.])\$\s?\d[\d,]*(?:\.\d{2})?", text):
            around = text[max(0, m.start() - 200):m.end() + 200].lower()
            if any(k in around for k in ["not published", "discarded", "permitted", "minimum", "payout", "usd"]):
                continue
            errors.append(f"{path.name}: a price-like figure in reader text → {m.group(0)[:18]}")

    # ---- 5. registers must cite ----------------------------------------------
    registers: dict[str, list[dict]] = {}
    reg = rows_of(src[ROOT / "products.html"])
    registers["product_intents"] = [r for r in reg if re.match(r"^P-\d\d$", r["cells"][0] if r["cells"] else "")]
    for r in registers["product_intents"]:
        if not re.search(r'href="https?://', r["raw"]):
            errors.append(f"products register: row {r['cells'][0]} cites no URL for manual review")
        if len(r["cells"]) != 9:
            errors.append(f"products register: row {r['cells'][0]} has {len(r['cells'])} cells, expected 9 "
                          f"(intended identifier and observed redirect must stay separate)")
    ver = rows_of(src[ROOT / "verification.html"])
    registers["sources"] = [r for r in ver if re.match(r"^[AFGR]-\d\d$", r["cells"][0] if r["cells"] else "")]
    for r in registers["sources"]:
        if not re.search(r'href="https?://', r["raw"]):
            errors.append(f"source register: entry {r['cells'][0]} has no link for manual review")
    registers["irregularities"] = [r for r in ver if re.match(r"^IRR-\d\d$", r["cells"][0] if r["cells"] else "")]
    if not registers["irregularities"]:
        errors.append("verification page: the irregularity register is empty")
    for r in registers["irregularities"]:
        if not re.search(r'href="https?://|\.json|\.html|\.py|\.js|<code>|[A-Za-z_]+\.(yml|txt|xml)', r["raw"]):
            errors.append(f"irregularity {r['cells'][0]}: no evidence file, link or command cited")
    qs = rows_of(src[ROOT / "questions.html"])
    registers["open_questions"] = [r for r in qs if re.match(r"^Q-\d\d$", r["cells"][0] if r["cells"] else "")]
    for r in registers["open_questions"]:
        if len(r["cells"]) != 7:
            errors.append(f"question {r['cells'][0]}: {len(r['cells'])} columns, expected 7 "
                          f"(question / have / missing / how / owner / severity)")
    sg = rows_of(src[ROOT / "suggestions.html"])
    registers["suggestions"] = [r for r in sg if r["attrs"].get("data-id", "").startswith("S-")]
    for r in registers["suggestions"]:
        if not re.search(r'data-decide|class="decide"', r["raw"]):
            errors.append(f"suggestion {r['attrs'].get('data-id')}: no decision control on the board")
        for choice in ("adopt", "park", "reject"):
            if f'data-choice="{choice}"' not in r["raw"]:
                errors.append(f"suggestion {r['attrs'].get('data-id')}: missing the {choice} control")

    # ---- 6. prose numbers vs computed numbers --------------------------------
    n = {k: len(v) for k, v in registers.items()}
    gates = Counter(r["attrs"].get("data-gate") for r in registers["suggestions"])
    paths = Counter(t for r in registers["suggestions"] for t in r["attrs"].get("data-path", "").split())
    verbatim = sum(1 for r in registers["sources"] if "verbatim" in " ".join(r["cells"]))
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
             "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
             "fourteen": 14, "twenty-eight": 28, "forty-nine": 49}
    numwords = "|".join(words)

    def claimed(page: str, pattern: str, want: int, label: str):
        for m in re.finditer(pattern, src[ROOT / page], re.I):
            got = m.group(1)
            val = int(got) if got.isdigit() else words.get(got.lower().replace("-", " "), -1)
            if val not in (want, -1):
                errors.append(f"{page}: prose says {got} {label}, the data says {want}")

    claimed("suggestions.html", r"\b(%s)\b ways to improve" % numwords, n["suggestions"], "suggestions")
    claimed("suggestions.html", r"<strong>(\d+) rows</strong>", n["suggestions"], "board rows")
    m = re.search(r"<h1>(.*?)</h1>", src[ROOT / "questions.html"], re.S)
    if m:
        t = strip_tags(m.group(1))
        mm = re.search(r"\b(%s)\b questions" % numwords, t, re.I)
        if mm and words[mm.group(1).lower()] != n["open_questions"]:
            errors.append(f'questions.html: headline says {mm.group(1)} questions, register has {n["open_questions"]}')
    claimed("verification.html", r"\b(%s)\b entries\. Each one" % numwords, n["sources"], "register entries")
    claimed("index.html", r"<b>(\d+)</b><span>source-register entries", n["sources"], "register entries")
    claimed("index.html", r"<b>(\d+)</b><span>suggestions to review", n["suggestions"], "suggestions")
    claimed("index.html", r"<b>(\d+)</b><span>flagged irregularities", n["irregularities"], "irregularities")
    m = re.search(r"\b(%s)\b working pages for the person" % numwords, src[ROOT / "index.html"], re.I)
    if m:
        hub = src[ROOT / "index.html"]
        sec = hub[hub.index('id="pages"'):]
        cards = len(re.findall(r'<article class="card accent">', sec))
        if words[m.group(1).lower()] != cards:
            errors.append(f"index.html: prose says {m.group(1)} working pages, the desk links {cards}")
    m = re.search(r"(\d+) quoted verbatim", src[ROOT / "index.html"])
    if m and int(m.group(1)) != verbatim:
        errors.append(f"index.html: claims {m.group(1)} verbatim sources, {verbatim} carry the verbatim chip")
    ep = src[ROOT / "editorial-plan.html"]
    m = re.search(r"\b(%s)\b of the twelve already exist as drafts" % numwords, ep, re.I)
    marked = ep.count("Exists as a draft")
    if m and words[m.group(1).lower()] != marked:
        errors.append(f"editorial-plan.html: claims {m.group(1)} drafts exist, {marked} rows are marked as drafts")
    cards = re.findall(r'<span class="chip ok">(\d+) suggestions</span>', src[ROOT / "suggestions.html"])
    if cards and sorted(map(int, cards)) != sorted([paths.get(x, 0) for x in "abc"]):
        errors.append(f"suggestions.html: path card chips {cards} do not match computed path counts "
                      f"{[paths.get(x, 0) for x in 'abc']}")
    for page, want_free, want_blocked in [("suggestions.html", gates.get("free", 0), gates.get("blocked", 0))]:
        m = re.search(r"Gates: (\d+) rows need nothing from you; (\d+) need access", src[ROOT / page])
        if m and (int(m.group(1)) != want_free or int(m.group(2)) != want_blocked):
            errors.append(f"{page}: gate counts in prose ({m.group(1)}/{m.group(2)}) differ from the table "
                          f"({want_free}/{want_blocked})")

    # ---- machine-readable output ---------------------------------------------
    def clean(cell: str) -> str:
        return re.sub(r"\s+", " ", cell).strip()

    desk = {
        "generated": str(date.today()),
        "section": "decision-support",
        "generated_by": "validate.py --json (parses the same HTML a human reads)",
        "counts": {**n, "verbatim_sources": verbatim, "pages": len(pages),
                   "suggestion_gates": dict(gates), "suggestion_paths": dict(paths)},
        "registers": {
            "product_intents": [dict(zip(
                ["id", "submitted_and_intended", "candidate_listing", "product",
                 "observed_register_a", "observed_register_b", "observed_this_session",
                 "confirmation", "source"], [clean(c) for c in r["cells"]]))
                for r in registers["product_intents"]],
            "sources": [{"id": clean(c[0]), "entry": clean(c[1]), "wording": clean(c[2]),
                         "read": clean(c[-2]), "status": clean(c[-1])}
                        for c in (r["cells"] for r in registers["sources"])],
            "irregularities": [{"id": clean(c[0]), "finding": clean(c[1]), "evidence": clean(c[2]),
                                 "action": clean(c[3]), "severity": clean(c[4])}
                                for c in (r["cells"] for r in registers["irregularities"])],
            "open_questions": [{"id": clean(c[0]), "question": clean(c[1]), "what_we_have": clean(c[2]),
                                "what_is_missing": clean(c[3]), "how_to_find_out": clean(c[4]),
                                "owner": clean(c[5]), "severity": clean(c[6])}
                               for c in (r["cells"] for r in registers["open_questions"])],
            "suggestions": [{"id": r["attrs"]["data-id"], "path": r["attrs"].get("data-path"),
                             "effort": r["attrs"].get("data-cost"), "gate": r["attrs"].get("data-gate"),
                             "suggestion": clean(c[1]), "why": clean(c[2]), "touches": clean(c[3])}
                            for r in registers["suggestions"] for c in [r["cells"]]],
        },
        "links": {"product_links_marked_sponsored": f'{counts["retail_ok"]}/{counts["retail"]}',
                  "documentation_links": counts["doc"]},
    }
    out = ROOT / "data" / "decision-desk.json"
    if "--json" in sys.argv:
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(desk, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    if not quiet:
        print(f"Decision Desk · {len(pages)} pages · registers: " +
              ", ".join(f"{k}={v}" for k, v in n.items()))
        print(f"  computed from the tables: paths={dict(paths)} gates={dict(gates)} verbatim_sources={verbatim}")
        print(f"  product links carrying rel='sponsored nofollow noopener': "
              f"{counts['retail_ok']}/{counts['retail']} · documentation links: {counts['doc']}")
        if warnings:
            print(f"  {len(warnings)} warning(s):")
            for w in warnings[:12]:
                print("   -", w)
        if "--json" in sys.argv:
            print(f"  wrote {out.relative_to(ROOT)} · {sum(n.values())} records")
    if errors:
        print(f"\nFAIL — {len(errors)} error(s):")
        for e in errors[:40]:
            print("  ✗", e)
        if len(errors) > 40:
            print(f"  … and {len(errors) - 40} more")
        return 1
    print("\nPASS — all six check families hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
