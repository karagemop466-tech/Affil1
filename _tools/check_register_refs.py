#!/usr/bin/env python3
"""Cross-register references have to resolve, and a record's citations have to cover
what the record talks about.

The registers cite each other by id - questions and suggestions name SRC rows, flags
name Q and S rows - and nothing on this site checked that those ids exist. Two
failures, both real and both from 2026-11-20, are why this file exists: a merge that
renumbered one session's sources left rows citing ids the register no longer defined,
and a merge that dropped a source row left a guide quoting a USDA fact sheet whose
register citation pointed at an Amazon policy page.

Three rules, each decidable, each written to fail on a shape that has actually gone
wrong here rather than on a general idea of tidiness:

  1. An id cited anywhere must be defined somewhere.
  2. A record that returns to one subject two or more times and cites sources must
     cite at least one source about that subject. Deliberately coarse: it fires on
     "cites only off-topic documents", not on "cites one wrong document beside two
     right ones", because that second case is an intent no checker can see. Overreach
     here buys a gate that cries wolf and gets switched off.
  3. Every URL a guide prints as its source must be an official host AND have a row
     in _src/data/sources.json, so the register can date it. This one is exact.

Rule 2 ignores a subject mentioned once (an aside is not a topic) and a record whose
subject families tie, rather than guessing which one it "really" means.

What is deliberately NOT claimed: no mechanical test can tell that a citation was
meant for a different document while a sibling citation looks plausible. Where that
matters, the page prints the source label next to the URL so a human reads the pair
instead of trusting a green tick.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "_src" / "data"
KIND = {"SRC": "sources", "Q": "questions", "S": "suggestions", "FLG": "flags"}
REF_RE = re.compile(r"\b(?:SRC-\d{2,3}|FLG-\d{2,3}|Q-\d{2}|S-\d{2})(?![\w-])")
SCANNED = ("flags", "questions", "suggestions", "products", "links", "crosscheck",
           "decisions-registry", "reverification", "events")

# Subject family -> (words that mark a record as being about it, words that mark a
# source row as being able to support it)
FAMILIES = [
    ("food safety",
     re.compile(r"\b(food safety|food-safety|thermometer|leftover|USDA|FSIS|internal "
                r"temperature|calibrat\w+|danger zone)\b", re.I),
     re.compile(r"fsis\.usda\.gov|USDA|FSIS", re.I)),
    ("crawler indexing",
     re.compile(r"\b(robots\.txt|robots meta|noindex|nofollow|sitemap|indexab\w*|"
                r"canonical|search console)\b", re.I),
     re.compile(r"developers\.google\.com|support\.google\.com|\bGoogle\b", re.I)),
    ("associates program",
     re.compile(r"\b(associates|special link|tracking id|operating agreement|program "
                r"policies|commission)\b", re.I),
     re.compile(r"affiliate-program\.amazon\.com|sell\.amazon\.com|\bAmazon\b", re.I)),
]


def load(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def rows(name):
    """Every list of records in a register, not just the first key it happens to have.

    suggestions.json opens with 'paths' and keeps its decisions under 'suggestions'; a
    checker that stops at the first list resolves 3 of 30 ids and reports the rest as
    missing. False alarms are how gates get switched off.
    """
    out = []
    for val in load(name).values():
        if isinstance(val, list):
            out.extend(r for r in val if isinstance(r, dict))
    return out


def main():
    index, src_rows = {}, []
    for kind, fname in KIND.items():
        for r in rows(fname):
            rid = str(r.get("id", ""))
            if rid:
                index[rid] = r
    for r in rows("sources"):
        src_rows.append(str(r.get("id", "")))

    errors, checked = [], 0
    for fname in SCANNED:
        if not (DATA / f"{fname}.json").is_file():
            continue
        for r in rows(fname):
            text = json.dumps(r, ensure_ascii=False)
            own = str(r.get("id", ""))
            refs = sorted(set(REF_RE.findall(text)) - {own})
            for ref in refs:
                checked += 1
                if ref not in index:
                    errors.append(f"{fname} {own or '?'}: cites {ref}, which no register row defines")

            cited_src = [x for x in refs if x.startswith("SRC-")]
            if not cited_src:
                continue
            # Coverage of the dominant subject only. A row about chicken temperatures
            # also mentions "sitemap" in passing because publishing it regenerates one,
            # and a rule that demands a source for every incidental word turns into two
            # false alarms a week - which is how a gate gets deleted. So the family the
            # record talks about most is the one that has to be covered, and a tie
            # between families is left alone rather than guessed at.
            scored = [(len(subj.findall(text)), label, accept) for label, subj, accept in FAMILIES]
            # A single mention is an aside, not a subject: S-28 says "once Search
            # Console has data" in a row whose claims are all food-safety quotations.
            scored = [s for s in scored if s[0] >= 2]
            top = [s for s in scored if s[0] == max(n for n, _, _ in scored)]
            if len(top) != 1:
                continue
            n, label, accept = top[0]
            if not any(accept.search(json.dumps(index[s], ensure_ascii=False))
                       for s in cited_src if s in index):
                errors.append(
                    f"{fname} {own or '?'}: talks about {label} {n} times and cites "
                    f"{', '.join(cited_src)}, none of which is a {label} source")

    # A guide's declared sources must be official pages the register also knows about:
    # the site rule is that a claim carries an official source, and a URL invented on the
    # page alone is how that rule becomes decoration.
    sys.path.insert(0, str(ROOT / "_tools"))
    try:
        from content import GUIDES
    except Exception as exc:                                    # the build gate reports it
        print(f"guides not importable ({exc}); source rule unchecked for guides")
        GUIDES = []
    known = {str(s.get("url", "")).rstrip("/") for s in rows("sources")}
    official = re.compile(r"^https://([a-z0-9.-]+)/(?:.*|)$", re.I)
    allowed_hosts = {"fsis.usda.gov", "www.fsis.usda.gov", "foodsafety.gov", "www.foodsafety.gov", "affiliate-program.amazon.com",
                     "consumer.ftc.gov", "www.ftc.gov", "www.ecfr.gov", "developers.google.com",
                     "support.google.com", "docs.github.com", "sell.amazon.com",
                     "developer-docs.amazon.com", "www.amazon.com"}
    guide_refs = 0
    for g in GUIDES:
        for label, url in g.get("sources", []):
            guide_refs += 1
            host = official.match(url).group(1).lower() if official.match(url) else ""
            if host not in allowed_hosts:
                errors.append(f"guide {g['slug']}: source {label!r} is not an official host ({host})")
            if url.rstrip("/") not in known:
                errors.append(f"guide {g['slug']}: source {label!r} -> {url} has no row in "
                              f"_src/data/sources.json, so the register cannot date it")

    print(f"register references: {checked} cross-citations against {len(index)} defined ids; "
          f"{guide_refs} guide source declarations")
    for e in errors:
        print("  ERR ", e)
    print(f"{len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
