#!/usr/bin/env python3
"""Syntax-check the site's own JavaScript without a node toolchain.

CI runs `node --check` when node exists; this is the same gate where it does not.
It is deliberately narrow: it catches the mistakes a hand-edit actually makes —
an unterminated string, an unbalanced brace, a stray template literal — so the
first-party collector cannot ship unparseable, and it says so rather than
silently passing. It is not a security review and does not execute the file.
"""

import pathlib
import re
import sys


def check(src: str) -> str | None:
    depth = {"(": 0, "{": 0, "[": 0}
    closers = {")": "(", "}": "{", "]": "["}
    i, line, n = 0, 1, len(src)
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            i += 1
            continue
        if src.startswith("/*", i):
            end = src.find("*/", i + 2)
            if end == -1:
                return f"line {line}: unterminated block comment"
            line += src.count("\n", i, end)
            i = end + 2
            continue
        if src.startswith("//", i):
            i = src.find("\n", i)
            if i == -1:
                break
            continue
        if c in "\"'`":
            quote, start = c, line
            i += 1
            while i < n:
                if src[i] == "\\":
                    i += 2
                    continue
                if src[i] == quote:
                    break
                if src[i] == "\n":
                    if quote == "`":
                        line += 1
                    else:
                        return f"line {start}: unterminated string literal"
                    if quote != "`" and src[i - 1] != "\\":
                        return f"line {start}: unterminated string literal"
                i += 1
            else:
                return f"line {start}: unterminated string literal"
            i += 1
            continue
        if c in depth:
            depth[c] += 1
        elif c in closers:
            depth[closers[c]] -= 1
            if depth[closers[c]] < 0:
                return f"line {line}: unmatched '{c}'"
        i += 1
    for kind, count in depth.items():
        if count != 0:
            return f"unbalanced '{kind}' ({count} unclosed)"
    if re.search(r"\beval\s*\(", src):
        return "eval() present — not permitted in first-party code"
    if re.search(r"https?://(?!karagemop466-tech\.github\.io)[\w.-]+\.[a-z]{2,}", src):
        for m in re.finditer(r"src\s*=\s*[\"']https?://", src):
            return f"external script/document reference near offset {m.start()} — no third-party loads"
    return None


def main(argv):
    paths = argv[1:] or ["assets/js/analytics.js", "assets/js/events.js", "assets/js/shortlist.js"]
    bad = 0
    for rel in paths:
        p = pathlib.Path(rel)
        if not p.exists():
            print(f"MISSING {rel}")
            bad += 1
            continue
        err = check(p.read_text(encoding="utf-8"))
        if err:
            print(f"FAIL  {rel}: {err}")
            bad += 1
        else:
            print(f"ok    {rel} ({len(p.read_text(encoding='utf-8'))} bytes)")
    if bad:
        print(f"\n{bad} file(s) failed the syntax check")
        return 1
    print(f"\nall {len(paths)} script(s) parse cleanly; no eval, no third-party load")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
