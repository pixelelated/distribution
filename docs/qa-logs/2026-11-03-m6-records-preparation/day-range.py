#!/usr/bin/env python3
"""Select T46 documentary ranges; stdin is data, never executed or echoed."""
import argparse
import json
import re
import sys

TIMESTAMP = re.compile(
    r"^(?:\[[^\]\n]+\]\s+)?(?:\d{4}[-_]\d{2}[-_]\d{2}[ T])?"
    r"(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?"
    r"(?:\s+UTC|Z|\+00:00)?(?=\s|$|[—–-])"
)


def select(text):
    lines = text.splitlines()
    heads = []
    fence = None
    for number, line in enumerate(lines, 1):
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*", line):
                fence = None
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if opening:
            marker, tail = opening.groups()
            if marker[0] != "`" or "`" not in tail:
                fence = (marker[0], len(marker))
                continue
        heading = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line)
        if heading:
            title = re.sub(r"[ \t]+#+[ \t]*$", "", heading[2]).strip()
            heads.append((number, len(heading[1]), title))
    candidates = [(n, level) for n, level, title in heads if level >= 2 and TIMESTAMP.match(title)]
    if not candidates:
        return {"selection": "no-supported-timestamp", "start_inclusive": 1,
                "end_exclusive": min(len(lines) + 1, 41), "logical_lines": len(lines),
                "last_entry_claim": False, "unclosed_fence": fence is not None}
    start, level = candidates[-1]  # File order, never clock order.
    boundary = next((n for n, lev, _ in heads if n > start and lev <= level), len(lines) + 1)
    return {"selection": "last-supported-heading-in-file-order", "start_inclusive": start,
            "end_exclusive": min(boundary, start + 120), "section_end_exclusive": boundary,
            "truncated": boundary > start + 120, "logical_lines": len(lines),
            "last_entry_claim": True, "unclosed_fence": fence is not None}


def self_test():
    fixture = ("# Day\n\n## 16:00 UTC — earlier in file\nfirst\n"
               "## 09:00 UTC — later in file\nlast\n### Details\nnested\n## Appendix\nend\n")
    r = select(fixture)
    assert (r["start_inclusive"], r["end_exclusive"]) == (5, 9)
    r = select("# Day\n## 10:00 UTC — real\na\n```\n## 23:59 UTC — fake\n```\nz\n")
    assert (r["start_inclusive"], r["end_exclusive"]) == (2, 8)
    r = select("# Day\n~~~\n## 23:59 UTC — fake\n")
    assert r["selection"] == "no-supported-timestamp" and r["unclosed_fence"]
    r = select("# Day\n## 25:61 UTC — invalid\n" + "x\n" * 50)
    assert not r["last_entry_claim"] and r["end_exclusive"] == 41
    r = select("# Day\n## [A] 2026-11-03T11:02:03Z — valid\nx\n")
    assert (r["start_inclusive"], r["end_exclusive"]) == (2, 4)
    r = select("# Day\n## 10:00 UTC — long\n" + "x\n" * 140)
    assert r["end_exclusive"] == 122 and r["truncated"]
    assert select("")["end_exclusive"] == 1
    print("PASS T46 day ranges: 7 synthetic cases; no historical bodies read")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--stdin", action="store_true")
    group.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
    else:
        print(json.dumps(select(sys.stdin.read()), sort_keys=True))


if __name__ == "__main__":
    main()
