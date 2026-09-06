#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What an AI-assisted stretch of work actually cost, measured rather than felt.

WHY THIS EXISTS
---------------
Teams cannot answer "what did the AI cost us, and against what return?" and the
usual diagnosis is that the data does not exist. For the cost half that is
simply false: a Claude Code session writes its real usage to the transcript on
disk -- input, output, cache-write, cache-read and thinking tokens, per message,
with the model name. Nobody totals it. This totals it.

It reads ONLY local files, sends nothing anywhere, and needs no API key.

WHAT IT GIVES YOU, AND WHAT IT DOES NOT
---------------------------------------
GIVES  exact token counts per session, per day, per project, split by the four
       rates that actually bill differently. Cache reads are an order of
       magnitude cheaper than fresh input, so a total that adds them together
       is not a cost, it is a number.

DOES NOT  attribute cost to a task. A session is a stretch of wall-clock time;
       which backlog item it advanced is a judgement only the person who ran it
       can make. The tracker's `Maliyet` column is where that judgement is
       recorded, and it is [H] by construction -- this tool refuses to invent
       the attribution, because a fabricated denominator is worse than a
       missing one.

DOES NOT  convert to money by default. Rates depend on the plan and change; pass
       --rates to supply them and the arithmetic is yours, stated, not guessed
       by this script.

USAGE
-----
    python tools/session_cost.py                       # all projects, by day
    python tools/session_cost.py --project C--TRAE-x   # one project
    python tools/session_cost.py --since 2026-09-01
    python tools/session_cost.py --by session
    python tools/session_cost.py --rates rates.json    # {"model": {"input":3,
                                                       #  "output":15,
                                                       #  "cache_write":3.75,
                                                       #  "cache_read":0.3}}
                                                       # (per million tokens)
    python tools/session_cost.py --json
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import glob
import json
import os
import sys

FIELDS = ("input", "output", "cache_write", "cache_read", "thinking")


def transcript_root() -> str:
    return os.path.join(os.path.expanduser("~"), ".claude", "projects")


def iter_records(paths: list[str]):
    for path in paths:
        project = os.path.basename(os.path.dirname(path))
        session = os.path.splitext(os.path.basename(path))[0]
        try:
            fh = open(path, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = rec.get("message")
                if not isinstance(msg, dict):
                    continue
                usage = msg.get("usage")
                if not isinstance(usage, dict):
                    continue
                yield project, session, rec.get("timestamp", ""), msg.get("model", "?"), usage


def totals(usage: dict) -> dict:
    details = usage.get("output_tokens_details") or {}
    return {
        "input": usage.get("input_tokens", 0) or 0,
        "output": usage.get("output_tokens", 0) or 0,
        "cache_write": usage.get("cache_creation_input_tokens", 0) or 0,
        "cache_read": usage.get("cache_read_input_tokens", 0) or 0,
        "thinking": details.get("thinking_tokens", 0) or 0,
    }


def money(bucket: dict, model: str, rates: dict) -> float | None:
    """Cost in the rates' currency, or None when no rate covers this model.

    A missing rate prints as "-", never as 0.0. Zero is a measurement; a
    missing rate is an absence, and printing one as the other is the mistake
    this whole family exists to refuse.
    """
    table = rates.get(model) or rates.get("default")
    if not table:
        return None
    per_m = lambda key: (bucket.get(key, 0) / 1_000_000) * table.get(key, 0)
    return per_m("input") + per_m("output") + per_m("cache_write") + per_m("cache_read")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Token cost of local Claude Code sessions")
    ap.add_argument("--root", default=transcript_root())
    ap.add_argument("--project", help="project directory name, substring match")
    ap.add_argument("--since", help="YYYY-MM-DD (inclusive)")
    ap.add_argument("--until", help="YYYY-MM-DD (inclusive)")
    ap.add_argument("--by", choices=["day", "session", "project", "model"], default="day")
    ap.add_argument("--rates", help="JSON file of per-million rates by model")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except (AttributeError, ValueError):
            pass

    paths = sorted(glob.glob(os.path.join(args.root, "*", "*.jsonl")))
    if args.project:
        paths = [p for p in paths if args.project in os.path.basename(os.path.dirname(p))]
    if not paths:
        print(f"transkript bulunamadi: {args.root}", file=sys.stderr)
        return 2

    rates = {}
    if args.rates:
        try:
            with open(args.rates, encoding="utf-8") as fh:
                rates = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"rates okunamadi: {exc}", file=sys.stderr)
            return 2

    groups: dict[str, dict] = collections.defaultdict(
        lambda: {k: 0 for k in FIELDS} | {"calls": 0, "models": collections.Counter()})
    grand = {k: 0 for k in FIELDS}
    calls = 0

    for project, session, ts, model, usage in iter_records(paths):
        day = (ts or "")[:10]
        if args.since and day and day < args.since:
            continue
        if args.until and day and day > args.until:
            continue
        key = {"day": day or "?", "session": f"{project}/{session[:8]}",
               "project": project, "model": model}[args.by]
        bucket = groups[key]
        t = totals(usage)
        for f in FIELDS:
            bucket[f] += t[f]
            grand[f] += t[f]
        bucket["calls"] += 1
        bucket["models"][model] += 1
        calls += 1

    if args.json:
        print(json.dumps({"grand": grand, "calls": calls,
                          "groups": {k: {f: v[f] for f in FIELDS} | {"calls": v["calls"]}
                                     for k, v in groups.items()}}, indent=2))
        return 0

    print(f"kaynak: {args.root}  ·  {len(paths)} transkript  ·  {calls} model cagrisi")
    print(f"\n{args.by:<24} {'taze':>10} {'cache-yaz':>12} {'cache-oku':>13} "
          f"{'cikti':>10}" + (f" {'ucret':>10}" if rates else ""))
    for key in sorted(groups):
        b = groups[key]
        line = (f"{key[:24]:<24} {b['input']:>10,} {b['cache_write']:>12,} "
                f"{b['cache_read']:>13,} {b['output']:>10,}")
        if rates:
            model = b["models"].most_common(1)[0][0] if b["models"] else "?"
            cost = money(b, model, rates)
            line += f" {('%.2f' % cost) if cost is not None else '-':>10}"
        print(line)

    print(f"\n{'TOPLAM':<24} {grand['input']:>10,} {grand['cache_write']:>12,} "
          f"{grand['cache_read']:>13,} {grand['output']:>10,}")
    print(f"  cikti icinde dusunme: {grand['thinking']:,}")
    eff = grand["input"] + grand["cache_write"] * 1.25 + grand["cache_read"] * 0.10
    print(f"  fiyat-agirlikli girdi esdegeri: {eff:,.0f} token")
    print("    (cache YAZMA ~1.25x, cache OKUMA ~0.1x taze girdi. Oranlar "
          "saglayicinin fiyat yapisindan gelir; kesin tutar icin --rates ver.)")
    if rates:
        total_cost = sum(
            (money(b, b["models"].most_common(1)[0][0] if b["models"] else "?", rates) or 0)
            for b in groups.values())
        print(f"  ucret toplami: {total_cost:.2f}")
    else:
        print("  ucret: HESAPLANMADI -- oran verilmedi. Sifir degil, yok.")

    print("\nBu sayilar maliyet tarafidir ve OLCUMDUR. Getiri tarafi burada yok:")
    print("  * bir oturumun hangi gorevi ilerlettigi, yalnizca onu kosan kisinin")
    print("    verebilecegi bir hukumdur -- cizelgedeki Maliyet sutunu o hukmun")
    print("    yeridir ve yapisi geregi [H]'dir;")
    print("  * 'AI %X kazandirdi' cumlesi icin karsi-olgu gerekir: ayni isin")
    print("    aracsiz maliyeti. O kol olmadan atif [KKE]'dir, sonuc degil.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
