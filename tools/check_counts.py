#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refuse to publish a count that no longer matches what is being counted.

WHY THIS EXISTS
---------------
The manifest is described in five places and three languages. Every one of them
states a number -- "the full kit is eleven pieces", "on bir parça, dokuzu
zorunlu", "the four references" -- and until this file existed, none of those
numbers was connected to anything. So they went wrong quietly: a tenth piece
shipped and four documents still said ten, and `docs/QUICKSTART.md` claimed
"yedisi zorunlu" while the table two lines above it showed eight ✓. Nothing
failed, because a number in prose is not a check.

This is the counting counterpart of the rule-range guard the sibling
repositories run over "R1-RN" claims. Same argument, same shape: pick the
artifact that cannot lie (the files on disk, the table that lists them), derive
the number from it, and fail on any document that claims a different one.

WHAT IS AUTHORITATIVE
---------------------
- **The manifest table in `skill/iskele/SKILL.md`.** It is the skill body: the
  piece list a host actually loads. Every other manifest table must agree with
  it on the piece ids, the file names and which pieces are required.
- **`skill/iskele/references/*.md` on disk.** The reference count is whatever
  is in the directory; no document gets to claim a different one.

Only tables carrying a Required/Zorunlu column are compared. The guide
template's table is a project-facing reading list rather than the manifest and
deliberately omits optional pieces, so it has no such column and is skipped --
by shape, not by an exception list that would go stale the same way the numbers
did.

NUMBER WORDS
------------
The prose says "eleven" and "on bir", not 11. So the check carries a small
word->int table for both languages. A number word it does not know is reported
as unreadable rather than passed over: an unparsed claim is exactly the
silently-wrong claim this file exists to catch.

USAGE
-----
    python tools/check_counts.py            # sweep; exit 1 on any mismatch
    python tools/check_counts.py --verbose  # also print what was derived
"""
from __future__ import annotations

import argparse
import glob
import io
import os
import re
import sys

SKILL_MANIFEST = "skill/iskele/SKILL.md"
REFERENCE_GLOB = "skill/iskele/references/*.md"

# Files whose prose or tables make manifest/reference claims.
SWEPT = [
    "skill/iskele/SKILL.md",
    "skill/iskele/references/kit-manifest.md",
    "docs/QUICKSTART.md",
    "docs/index.md",
    "docs/tr/metodoloji.md",
    "docs/tr/kit-manifesti.md",
    "README.md",
]

EN_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
}
TR_WORDS = {
    "bir": 1, "iki": 2, "üç": 3, "uc": 3, "dört": 4, "dort": 4, "beş": 5,
    "bes": 5, "altı": 6, "alti": 6, "yedi": 7, "sekiz": 8, "dokuz": 9,
    "on": 10, "on bir": 11, "on iki": 12, "on üç": 13, "on uc": 13,
    "on dört": 14, "on dort": 14, "on beş": 15, "on bes": 15,
    "yirmi": 20,
}


def to_int(word: str) -> int | None:
    """A number as digits or as an English/Turkish word. None = unreadable."""
    w = word.strip().lower()
    if w.isdigit():
        return int(w)
    return EN_WORDS.get(w) or TR_WORDS.get(w)


def read(path: str) -> str:
    with io.open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def manifest_tables(text: str) -> list[list[tuple[str, str, bool]]]:
    """Every markdown table that lists pieces AND marks which are required.

    Returns one list of (id, filename, required) per table. A table without a
    Required/Zorunlu column is not a manifest -- it is a reading list -- and is
    not returned.
    """
    tables = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] != "#":
            continue
        if not re.match(r"(file|dosya)$", cells[1], re.I):
            continue
        if not re.match(r"(required|zorunlu)", cells[2], re.I):
            continue
        rows = []
        for row in lines[i + 2:]:
            if not row.strip().startswith("|"):
                break
            c = [x.strip() for x in row.strip().strip("|").split("|")]
            if len(c) < 3 or not re.match(r"^\d+$", c[0]):
                break
            name = c[1].strip("`")
            rows.append((c[0], name, "✓" in c[2]))
        if rows:
            tables.append(rows)
    return tables


def check() -> tuple[list[str], list[str]]:
    problems: list[str] = []
    notes: list[str] = []

    truth_tables = manifest_tables(read(SKILL_MANIFEST))
    if not truth_tables:
        return ([f"{SKILL_MANIFEST}: no manifest table found -- this check has "
                 f"nothing to stand on"], notes)
    truth = truth_tables[0]
    total, required = len(truth), sum(1 for r in truth if r[2])
    refs = sorted(os.path.basename(p) for p in glob.glob(REFERENCE_GLOB))
    notes.append(f"manifest: {total} pieces, {required} required")
    notes.append(f"references on disk: {len(refs)} ({', '.join(refs)})")

    for path in SWEPT:
        if not os.path.isfile(path):
            problems.append(f"{path}: swept but missing")
            continue
        text = read(path)

        # 1. Every other manifest table must match the skill body's, row for row.
        for t_no, table in enumerate(manifest_tables(text)):
            if path == SKILL_MANIFEST and t_no == 0:
                continue
            if len(table) != total:
                problems.append(
                    f"{path}: a manifest table lists {len(table)} pieces, "
                    f"{SKILL_MANIFEST} lists {total}")
                continue
            for (ai, an, ar), (bi, bn, br) in zip(table, truth):
                if ai != bi or an != bn:
                    problems.append(
                        f"{path}: piece {ai} is `{an}`, {SKILL_MANIFEST} has "
                        f"{bi} `{bn}`")
                elif ar != br:
                    problems.append(
                        f"{path}: piece {ai} is marked "
                        f"{'required' if ar else 'optional'}, "
                        f"{SKILL_MANIFEST} marks it "
                        f"{'required' if br else 'optional'}")

        # 2. Prose counts. The claim carries a number; the number must be the
        #    one derived above, and a number word nobody can parse is a finding
        #    rather than a pass.
        claims = [
            (r"kit is ([\w-]+) pieces", total, "pieces"),
            (r"kit ((?:on|yirmi) [\w]+|[\w]+) par[çc]a", total, "parça"),
            (r"((?:on|yirmi) [\w]+|[\w]+) par[çc]a, ([\w]+?)[sşuü]*[ıi]? zorunlu", None, "parça+zorunlu"),
            (r"([\w-]+) pieces, ([\w-]+) required", None, "pieces+required"),
            (r"the ([\w-]+) references", len(refs), "references"),
            (r"((?:on|yirmi) [\w]+|[\w]+) referans[ıi]n", len(refs), "referans"),
            (r"([\w-]+) kit files", total, "kit files"),
            # Turkish compounds two number words ("on bir"), so the capture has
            # to reach for the pair before settling for the single word --
            # otherwise "On bir kit dosyası" reads as a claim of one.
            (r"((?:on|yirmi) [\w]+|[\w]+) kit dosyas", total, "kit dosyası"),
        ]
        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern, expect, label in claims:
                for m in re.finditer(pattern, line, re.I):
                    words = list(m.groups())
                    wanted = [expect] if expect is not None else [total, required]
                    for word, exp in zip(words, wanted):
                        got = to_int(word)
                        if got is None:
                            problems.append(
                                f"{path}:{lineno}: cannot read the number in "
                                f"{label} claim: {word!r}")
                        elif got != exp:
                            problems.append(
                                f"{path}:{lineno}: claims {word!r} ({got}) "
                                f"{label}, the truth is {exp}")
    return problems, notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    problems, notes = check()
    if args.verbose:
        for n in notes:
            print(n)
    if problems:
        print("FAIL: a document claims a count the repository does not have:",
              file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        print("\nThe manifest table in skill/iskele/SKILL.md and the files in\n"
              "skill/iskele/references/ are the source of truth. Fix the prose,\n"
              "not this check.", file=sys.stderr)
        return 1
    print(f"ok  every manifest and reference count agrees "
          f"({notes[0].split(': ')[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
