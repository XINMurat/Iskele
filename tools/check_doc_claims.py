#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refuse to publish a claim about the code that the code does not support.

WHY THIS EXISTS
---------------
`check_counts.py` binds numbers that describe the REPOSITORY (how many pieces,
how many references). This binds sentences that describe the CODE: which report
regions the generator writes, what the default effort weights are, which columns
it reads out of the tracker. Those sentences are the ones a reader trusts most
and nothing was checking any of them.

They go stale the ordinary way. The region list said five keys through two
additions -- `HAKEM` shipped, then `SKORKART` shipped, and the documentation
kept saying five in both languages. Nothing failed, because a list in prose is
not connected to the dict it describes.

HOW IT DIFFERS FROM A DRIFT DETECTOR
------------------------------------
Tools like fiberplane/drift anchor a doc to a symbol and warn when the symbol's
AST changes. That answers "did the code move?", which is useful and is not the
question here. This asks the stronger one: **does the sentence still state the
truth?** A change alarm goes off on a rename that broke nothing and stays quiet
when someone adds a seventh key to a list of five -- exactly the case that
actually happened. Binding the claim to the VALUE rather than to the diff costs
one comparison and catches the class the diff misses.

It also means a clean run says something: not "nothing moved" but "these four
sentences are true right now".

WHAT IT CHECKS
--------------
  1. Report region keys, EN and TR, against `RENDERERS` in progress.py.
  2. Default effort weights against `DEFAULTS["effort_weights"]`.
  3. Every column the scripts read is named in the tracker schema table.
  4. Documented exit codes exist in the script.

WHAT IT DOES NOT CHECK: whether the prose around the value is a good
explanation. No script knows that.

USAGE
-----
    python tools/check_doc_claims.py            # exit 1 on any false claim
    python tools/check_doc_claims.py --verbose  # print what was derived
"""
from __future__ import annotations

import argparse
import ast
import io
import os
import re
import sys

PROGRESS = "skill/iskele/scripts/progress.py"
TRACKER = "skill/iskele/scripts/backlog_to_tracker.py"
DOC_EN = "skill/iskele/references/tracking.md"
DOC_TR = "docs/tr/takip.md"

# A paragraph break, written as a constant so no escape has to survive a
# round trip through a shell heredoc to get this file edited.
BLANK_LINE = chr(10) + chr(10)


def read(path: str) -> str:
    with io.open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def literal_at(src: str, name: str):
    """The value of a module-level assignment, without importing the module.

    Parsed rather than imported on purpose: importing progress.py would need
    openpyxl, and a documentation check that fails when an optional dependency
    is missing would be turned off on the first CI machine that lacks it.
    """
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except ValueError:
                        # dict(...) call form -- read the keywords instead.
                        if isinstance(node.value, ast.Call):
                            out = {}
                            for kw in node.value.keywords:
                                try:
                                    out[kw.arg] = ast.literal_eval(kw.value)
                                except ValueError:
                                    out[kw.arg] = None
                            return out
                        return None
    return None


def renderer_keys(src: str) -> set[str]:
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "RENDERERS":
                    return {kw.arg for kw in node.value.keywords if kw.arg}
    return set()


def documented_regions(text: str) -> tuple[set[str], int] | None:
    """The backticked keys on the 'region keys' line, with its line number."""
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"(region keys|bölge anahtarları)", line, re.I):
            # The sentence wraps, so read to the end of the PARAGRAPH -- which
            # is what this comment always claimed and the code did not do: it
            # took a fixed four-line window, so the ninth key landed outside
            # it and the guard reported a stale list that was not stale. A
            # checker that goes wrong as the thing it checks grows is the
            # drift it exists to catch, one level up.
            rest = []
            for nxt in text.splitlines()[i - 1:]:
                if not nxt.strip():
                    break
                rest.append(nxt)
            blob = " ".join(rest)
            keys = set(re.findall(r"`([A-Z][A-Z0-9_]+)`", blob))
            return keys, i
    return None


def check(verbose: bool) -> list[str]:
    problems: list[str] = []
    prog = read(PROGRESS)
    notes = []

    # 1 — report regions, both languages
    actual = renderer_keys(prog)
    notes.append(f"RENDERERS: {', '.join(sorted(actual))}")
    for label, path in (("EN", DOC_EN), ("TR", DOC_TR)):
        if not os.path.isfile(path):
            problems.append(f"{path}: swept but missing")
            continue
        found = documented_regions(read(path))
        if not found:
            problems.append(f"{path}: no 'region keys' sentence found — the "
                            f"claim this check binds has disappeared")
            continue
        claimed, lineno = found
        missing = actual - claimed
        extra = claimed - actual
        if missing:
            problems.append(
                f"{path}:{lineno} ({label}) lists {len(claimed)} report regions "
                f"and the generator writes {len(actual)}; not documented: "
                f"{', '.join(sorted(missing))}")
        if extra:
            problems.append(
                f"{path}:{lineno} ({label}) documents regions the generator "
                f"does not write: {', '.join(sorted(extra))}")

    # 2 — default effort weights
    defaults = literal_at(prog, "DEFAULTS") or {}
    weights = defaults.get("effort_weights") or {}
    notes.append("effort_weights: " + ", ".join(f"{k}={v:g}" for k, v in weights.items()))
    en = read(DOC_EN)
    m = re.search(r"Default weights\s*`([^`]+)`", en)
    if not m:
        problems.append(f"{DOC_EN}: the 'Default weights' claim is gone")
    else:
        claimed = dict(re.findall(r"([SML])\s*=\s*([0-9.]+)", m.group(1)))
        for k, v in weights.items():
            if k not in claimed:
                problems.append(f"{DOC_EN}: default weight {k} is not documented")
            elif abs(float(claimed[k]) - float(v)) > 1e-9:
                problems.append(
                    f"{DOC_EN}: documents {k}={claimed[k]}, the code uses {v:g}")

    # 3 — every column the scripts read is named in the docs
    cols = {}
    for name in ("COL", "OPT_COL", "SCORE_COL"):
        cols.update(literal_at(prog, name) or {})
    notes.append(f"columns read: {len(cols)}")
    doc_blob = en + read(DOC_TR) if os.path.isfile(DOC_TR) else en
    for key, header in cols.items():
        if f"`{header}`" not in doc_blob:
            problems.append(
                f"the scripts read a column `{header}` that the tracker schema "
                f"table does not mention — a reader filling the sheet by hand "
                f"has no way to know it matters")

    # 4 — documented exit codes exist in the script
    actual_codes = {0} | {int(n) for n in re.findall(r"sys\.exit\((\d+)\)", prog)}
    # The sentence wraps, and a single-line match silently saw two of the
    # three codes. A check that under-reports reads exactly like a clean
    # result, which is the failure this file exists to prevent -- so the
    # paragraph is sliced by hand rather than matched with an escape that
    # is easy to get subtly wrong.
    blob = None
    if "exit codes:" in en:
        tail = en.split("exit codes:", 1)[1]
        blob = tail.split(BLANK_LINE, 1)[0]
    if blob is not None:
        claimed_codes = {int(n) for n in re.findall(r"`(\d+)`", blob)}
        notes.append(f"exit codes: doc {sorted(claimed_codes)} / code {sorted(actual_codes)}")
        for c in sorted(claimed_codes - actual_codes):
            problems.append(
                f"{DOC_EN}: documents exit code {c}, which progress.py never returns")

    if verbose:
        for n in notes:
            print(" ", n)
    return problems


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    problems = check(a.verbose)
    if problems:
        print("FAIL: a document states something the code does not:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        print("\nThe code is the source of truth. Fix the sentence, not this check.",
              file=sys.stderr)
        return 1
    print("ok  every documented claim about the generator matches the code")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
