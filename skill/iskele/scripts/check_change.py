#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refuse a change a reviewer cannot actually read.

WHY THIS EXISTS
---------------
The kit's gates audit whether a task is DONE. None of them asks whether the
change that closed it can be REVIEWED. With a fast author -- a model, or a
person in a hurry -- that gap decides everything: one commit closes eight
tasks, a file grows past three thousand lines, and "reviewed" quietly comes to
mean "approved without reading". A rule that says "keep changes small" in
prose is negotiable by whoever is in a hurry; this script is the same rule in
the form that travels (SKILL.md, "the scripted part is the part that travels").

WHAT IT CHECKS
--------------
Over the commits in `<base>..HEAD` (merges skipped):
  KIMLIKSIZ          the message names no task ID
  COK_AMACLI         the message names more than one task ID
  BUYUK_DEGISIKLIK   added+deleted lines in source files exceed the budget
Over the source files as they are now:
  BUYUK_DOSYA        more lines than the file budget
  UZUN_SATIR         lines longer than the line budget
And, as information rather than a failure:
  INSAN_ONAYI        the range touches a path the project declared critical
                     (money, authorisation, migrations ...): a named person
                     reads it, whatever else passed.

THE RATCHET
-----------
An existing project already has files over the budget. Failing on them forever
teaches everyone to ignore the check; exempting them forever lets them grow.
So `--write-baseline` records what is over budget today, and from then on a
recorded file may not get WORSE (more lines, more over-long lines). A file not
in the baseline gets no allowance. Shrinking is reported so the baseline can be
tightened; it is never loosened by this script on its own.

NO SILENT DEFAULTS
------------------
Every threshold comes from the `review` block of the kit config. A key that is
absent is reported as `olculmedi` and the run exits 2: a gate asked to pass
without a threshold has measured nothing. A key set to null is a decision
("this project does not budget line length") and is printed as `kapali`.

EXIT CODES
----------
  0  measured, nothing over budget
  1  at least one finding
  2  something could not be measured (missing config block or key, no git,
     unresolvable base)

USAGE
-----
    python check_change.py --config iskele.config.json --base main
    python check_change.py --config iskele.config.json --files-only
    python check_change.py --config iskele.config.json --write-baseline
    python check_change.py --self-test
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tempfile

KEYS = ("id_pattern", "max_changed_lines", "max_file_lines", "max_line_length",
        "source_globs", "critical_globs")
MISSING = object()


# --------------------------------------------------------------------------
# small pure helpers (everything the self-test exercises lives here)
# --------------------------------------------------------------------------
def glob_to_regex(pattern: str) -> "re.Pattern[str]":
    """`**/` spans directories, `*` and `?` stay inside one path segment."""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?"); i += 3
        elif pattern.startswith("**", i):
            out.append(".*"); i += 2
        elif pattern[i] == "*":
            out.append("[^/]*"); i += 1
        elif pattern[i] == "?":
            out.append("[^/]"); i += 1
        else:
            out.append(re.escape(pattern[i])); i += 1
    return re.compile("^" + "".join(out) + "$")


def matches(path: str, globs) -> bool:
    path = path.replace("\\", "/")
    return any(glob_to_regex(g).match(path) for g in (globs or []))


def read_review(config: dict):
    """-> (settings, unmeasured[]). Absent key = unmeasured; null = switched off."""
    block = config.get("review", MISSING)
    if block is MISSING or not isinstance(block, dict):
        return None, ["review blogu yok: hicbir esik tanimli degil"]
    settings, unmeasured = {}, []
    for key in KEYS:
        value = block.get(key, MISSING)
        if value is MISSING:
            unmeasured.append(f"{key} verilmedi")
        settings[key] = None if value is MISSING else value
    for key in ("max_changed_lines", "max_file_lines", "max_line_length"):
        v = settings[key]
        if v is not None and (isinstance(v, bool) or not isinstance(v, int) or v <= 0):
            unmeasured.append(f"{key} pozitif tamsayi degil: {v!r}")
            settings[key] = None
    if settings["id_pattern"] is not None:
        try:
            re.compile(settings["id_pattern"])
        except (re.error, TypeError) as e:
            unmeasured.append(f"id_pattern derlenemedi: {e}")
            settings["id_pattern"] = None
    settings["exclude_globs"] = block.get("exclude_globs") or []
    settings["exempt_message_pattern"] = block.get("exempt_message_pattern")
    settings["baseline"] = block.get("baseline")
    return settings, unmeasured


def judge_commit(sha: str, message: str, numstat, s: dict):
    """numstat: [(added, deleted, path)] -> findings [(code, where, detail)]."""
    found = []
    subject = (message.strip().splitlines() or [""])[0]
    exempt = s.get("exempt_message_pattern")
    if exempt and re.search(exempt, subject):
        return found
    if s["id_pattern"]:
        ids = sorted(set(re.findall(s["id_pattern"], message)))
        if not ids:
            found.append(("KIMLIKSIZ", sha[:8], f"gorev ID'si yok: {subject[:70]}"))
        elif len(ids) > 1:
            found.append(("COK_AMACLI", sha[:8], f"{len(ids)} gorev tek degisiklikte: {', '.join(ids)}"))
    if s["max_changed_lines"] and s["source_globs"]:
        total = sum(a + d for a, d, p in numstat
                    if matches(p, s["source_globs"]) and not matches(p, s["exclude_globs"]))
        if total > s["max_changed_lines"]:
            found.append(("BUYUK_DEGISIKLIK", sha[:8], f"{total} satir > {s['max_changed_lines']}"))
    return found


def judge_file(path: str, text: str, s: dict, baseline: dict):
    """-> (findings, measured) where measured = {"lines": n, "long_lines": n}."""
    lines = text.splitlines()
    n = len(lines)
    longn = sum(1 for ln in lines if s["max_line_length"] and len(ln) > s["max_line_length"])
    measured = {"lines": n, "long_lines": longn}
    allowed = (baseline or {}).get(path, {})
    found = []
    if s["max_file_lines"] and n > s["max_file_lines"]:
        cap = allowed.get("lines")
        if cap is None:
            found.append(("BUYUK_DOSYA", path, f"{n} satir > {s['max_file_lines']}"))
        elif n > cap:
            found.append(("BUYUK_DOSYA", path, f"{n} satir; taban cizgisi {cap} idi, buyudu"))
    if s["max_line_length"] and longn:
        cap = allowed.get("long_lines")
        if cap is None:
            found.append(("UZUN_SATIR", path, f"{longn} satir > {s['max_line_length']} karakter"))
        elif longn > cap:
            found.append(("UZUN_SATIR", path, f"{longn} uzun satir; taban cizgisi {cap} idi, artti"))
    return found, measured


def over_budget(measured: dict, s: dict) -> bool:
    return bool((s["max_file_lines"] and measured["lines"] > s["max_file_lines"]) or measured["long_lines"])


# --------------------------------------------------------------------------
# git and the file system
# --------------------------------------------------------------------------
def git(repo: str, *args: str) -> str:
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "replace").strip() or "git basarisiz")
    return r.stdout.decode("utf-8", "replace")


def commits(repo: str, base: str):
    for sha in git(repo, "rev-list", "--no-merges", "--reverse", f"{base}..HEAD").split():
        message = git(repo, "show", "-s", "--format=%B", sha)
        numstat = []
        for row in git(repo, "show", "--numstat", "--format=", sha).splitlines():
            parts = row.split("\t")
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():   # "-" = binary
                numstat.append((int(parts[0]), int(parts[1]), parts[2]))
        yield sha, message, numstat


def tracked_sources(repo: str, s: dict):
    for path in git(repo, "ls-files").splitlines():
        if matches(path, s["source_globs"]) and not matches(path, s["exclude_globs"]):
            yield path


def run(repo: str, config_path: str, base, files_only: bool, write_baseline: bool, out=sys.stdout) -> int:
    def say(*a):
        print(*a, file=out)

    try:
        with io.open(config_path, encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, ValueError) as e:
        say(f"olculmedi: config okunamadi ({e})")
        return 2
    s, unmeasured = read_review(config)
    if s is None:
        say("olculmedi: " + unmeasured[0])
        return 2
    for key in KEYS:
        if s[key] is None and not any(u.startswith(key) for u in unmeasured):
            say(f"kapali: {key} (config'te null: bilincli karar)")

    baseline_path = os.path.join(os.path.dirname(os.path.abspath(config_path)), s["baseline"]) if s["baseline"] else None
    baseline = {}
    if baseline_path and os.path.exists(baseline_path) and not write_baseline:
        with io.open(baseline_path, encoding="utf-8") as f:
            baseline = json.load(f).get("files", {})

    findings, human, shrunk, new_baseline = [], [], [], {}
    try:
        if s["source_globs"]:
            for path in tracked_sources(repo, s):
                try:
                    with io.open(os.path.join(repo, path), encoding="utf-8", errors="replace") as f:
                        text = f.read()
                except OSError:
                    continue
                found, measured = judge_file(path, text, s, baseline)
                findings += found
                if over_budget(measured, s):
                    new_baseline[path] = measured
                old = baseline.get(path)
                if old and (measured["lines"] < old.get("lines", 0) or measured["long_lines"] < old.get("long_lines", 0)):
                    shrunk.append(path)
        if not files_only and not write_baseline:
            if not base:
                unmeasured.append("--base verilmedi: degisiklik araligi olculmedi (--files-only bilincli atlar)")
            else:
                for sha, message, numstat in commits(repo, base):
                    findings += judge_commit(sha, message, numstat, s)
                    touched = sorted({p for _, _, p in numstat if matches(p, s["critical_globs"])})
                    if touched:
                        human.append((sha[:8], touched))
    except RuntimeError as e:
        say(f"olculmedi: git ({e})")
        return 2

    if write_baseline:
        if not baseline_path:
            say("olculmedi: review.baseline verilmedi; taban cizgisi yazilacak yer yok")
            return 2
        with io.open(baseline_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_note": "check_change.py --write-baseline. Butceyi asan dosyalarin bugunku hali; "
                                "buradaki bir dosya kotulesemez, burada olmayan dosyaya pay yok.",
                       "files": dict(sorted(new_baseline.items()))}, f, ensure_ascii=False, indent=2)
            f.write("\n")
        say(f"taban cizgisi yazildi: {len(new_baseline)} dosya -> {baseline_path}")
        return 0

    for code, where, detail in findings:
        say(f"{code:<17} {where}  {detail}")
    for sha, touched in human:
        say(f"{'INSAN_ONAYI':<17} {sha}  kritik yol: {', '.join(touched)}")
    for path in shrunk:
        say(f"kuculdu           {path}  (taban cizgisi sikilastirilabilir: --write-baseline)")
    for u in unmeasured:
        say(f"olculmedi: {u}")
    say(f"\n{len(findings)} bulgu, {len(human)} degisiklik insan onayi bekliyor, "
        f"{len(unmeasured)} olculmedi, taban cizgisinde {len(baseline)} dosya")
    return 1 if findings else (2 if unmeasured else 0)


# --------------------------------------------------------------------------
# self-test: every check is shown to fire, and to stay quiet when it should
# --------------------------------------------------------------------------
def self_test() -> int:
    results = []

    def check(name, ok):
        results.append(ok)
        print(("ok   " if ok else "FAIL ") + name)

    s, un = read_review({"review": {"id_pattern": r"F\d+-[A-Z]+-\d+", "max_changed_lines": 100, "max_file_lines": 50,
                                    "max_line_length": 20, "source_globs": ["src/**/*.py"], "critical_globs": ["src/para/**"]}})
    check("tam config: olculmeyen yok", un == [])
    check("glob: ** dizin asar", matches("src/a/b/x.py", ["src/**/*.py"]) and matches("src/x.py", ["src/**/*.py"]))
    check("glob: * dizin asmaz", not matches("src/a/x.py", ["src/*.py"]))
    check("glob: ters egik cizgi normalize", matches("src\\a\\x.py", ["src/**/*.py"]))

    def codes(found):
        return [c for c, _, _ in found]

    check("tek ID, kucuk degisiklik: temiz", judge_commit("a" * 40, "F1-BE-01: limit", [(10, 5, "src/x.py")], s) == [])
    check("ID yok -> KIMLIKSIZ", codes(judge_commit("a" * 40, "duzeltmeler", [], s)) == ["KIMLIKSIZ"])
    check("iki ID -> COK_AMACLI", codes(judge_commit("a" * 40, "F1-BE-01 ve F2-QA-03", [], s)) == ["COK_AMACLI"])
    check("ayni ID iki kez: tek sayilir", judge_commit("a" * 40, "F1-BE-01 ... F1-BE-01 eki", [], s) == [])
    check("butce asimi -> BUYUK_DEGISIKLIK",
          codes(judge_commit("a" * 40, "F1-BE-01", [(80, 30, "src/x.py")], s)) == ["BUYUK_DEGISIKLIK"])
    check("kaynak disi satirlar sayilmaz", judge_commit("a" * 40, "F1-BE-01", [(900, 0, "docs/x.md")], s) == [])
    s2 = dict(s, exempt_message_pattern=r"^release:")
    check("muaf desen: yargilanmaz", judge_commit("a" * 40, "release: v1", [(900, 0, "src/x.py")], s2) == [])

    big = "\n".join("x" for _ in range(60))
    check("buyuk dosya, taban yok -> BUYUK_DOSYA", codes(judge_file("src/x.py", big, s, {})[0]) == ["BUYUK_DOSYA"])
    check("tabandaki dosya ayni boyda: temiz", judge_file("src/x.py", big, s, {"src/x.py": {"lines": 60, "long_lines": 0}})[0] == [])
    check("tabandaki dosya buyudu -> BUYUK_DOSYA",
          codes(judge_file("src/x.py", big + "\nx", s, {"src/x.py": {"lines": 60, "long_lines": 0}})[0]) == ["BUYUK_DOSYA"])
    check("uzun satir -> UZUN_SATIR", codes(judge_file("src/x.py", "y" * 30, s, {})[0]) == ["UZUN_SATIR"])
    check("sinirdaki satir uzun degil", judge_file("src/x.py", "y" * 20, s, {})[0] == [])

    _, un = read_review({})
    check("review blogu yok -> olculmedi", len(un) == 1)
    s3, un = read_review({"review": {"id_pattern": None, "max_changed_lines": 100, "max_file_lines": 50,
                                     "max_line_length": None, "source_globs": [], "critical_globs": []}})
    check("null = bilincli kapali, olculmedi degil", un == [] and s3["max_line_length"] is None)
    _, un = read_review({"review": {"max_changed_lines": 100}})
    check("eksik anahtar -> olculmedi", len(un) == len(KEYS) - 1)
    _, un = read_review({"review": dict.fromkeys(KEYS, None) | {"max_file_lines": "600"}})
    check("metin esik reddedilir (sessizce cevrilmez)", any("max_file_lines" in u for u in un))
    _, un = read_review({"review": dict.fromkeys(KEYS, None) | {"max_file_lines": True}})
    check("bool esik reddedilir", any("max_file_lines" in u for u in un))

    # end to end on a throw-away repository: the gate must be able to FAIL
    with tempfile.TemporaryDirectory() as d:
        def g(*a):
            subprocess.run(["git", "-C", d, *a], check=True, capture_output=True)
        try:
            g("init", "-q"); g("config", "user.email", "t@example.invalid"); g("config", "user.name", "t")
            g("config", "commit.gpgsign", "false")
            os.makedirs(os.path.join(d, "src", "para"))
            cfg = os.path.join(d, "iskele.config.json")
            with io.open(cfg, "w", encoding="utf-8") as f:
                json.dump({"review": {"id_pattern": r"F\d+-[A-Z]+-\d+", "max_changed_lines": 10, "max_file_lines": 5,
                                      "max_line_length": 40, "source_globs": ["src/**/*.py"],
                                      "critical_globs": ["src/para/**"], "baseline": "review-baseline.json"}}, f)
            def write(rel, n):
                with io.open(os.path.join(d, rel), "w", encoding="utf-8", newline="\n") as f:
                    f.write("".join(f"satir {i}\n" for i in range(n)))
            write("src/eski.py", 30)
            g("add", "-A"); g("commit", "-q", "-m", "F0-BE-01: baslangic")
            base = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            buf = io.StringIO()
            check("uctan uca: tabansiz eski dosya dusurur", run(d, cfg, None, True, False, buf) == 1)
            check("uctan uca: taban cizgisi yazilir", run(d, cfg, None, False, True, io.StringIO()) == 0)
            check("uctan uca: tabanla temiz", run(d, cfg, None, True, False, io.StringIO()) == 0)
            write("src/para/hesap.py", 3)
            g("add", "-A"); g("commit", "-q", "-m", "F1-BE-02: hesap")
            buf = io.StringIO()
            check("uctan uca: kucuk tek amacli degisiklik gecer", run(d, cfg, base, False, False, buf) == 0)
            check("uctan uca: kritik yol INSAN_ONAYI basar", "INSAN_ONAYI" in buf.getvalue())
            write("src/eski.py", 31)
            g("add", "-A"); g("commit", "-q", "-m", "toparlama")
            buf = io.StringIO()
            rc = run(d, cfg, base, False, False, buf)
            check("uctan uca: buyuyen eski dosya + kimliksiz commit dusurur",
                  rc == 1 and "BUYUK_DOSYA" in buf.getvalue() and "KIMLIKSIZ" in buf.getvalue())
            check("uctan uca: cozulmeyen taban -> 2", run(d, cfg, "yok-boyle-dal", False, False, io.StringIO()) == 2)
        except (OSError, subprocess.CalledProcessError) as e:
            check(f"uctan uca: git calistirilamadi ({e})", False)

    print(f"\n{sum(results)}/{len(results)} gecti")
    return 0 if all(results) else 1


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--config", help="kit config (review blogu)")
    p.add_argument("--repo", default=".", help="git deposu (varsayilan: bulunulan dizin)")
    p.add_argument("--base", help="karsilastirma tabani: <base>..HEAD araligindaki commit'ler yargilanir")
    p.add_argument("--files-only", action="store_true", help="yalniz dosya butceleri; degisiklik araligi bilincli atlanir")
    p.add_argument("--write-baseline", action="store_true", help="butceyi asan dosyalarin bugunku halini kaydet")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        return self_test()
    if not a.config:
        p.error("--config gerekli")
    return run(a.repo, a.config, a.base, a.files_only, a.write_baseline)


if __name__ == "__main__":
    sys.exit(main())
