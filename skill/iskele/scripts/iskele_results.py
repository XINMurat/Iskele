#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iskele_results.py — tracker.xlsx'te tamamlanan gorevler -> Mizan results[].

iskele_to_registry.py dongunun ilk yarisidir: backlog'u ONKAYIT olarak
Mizan'a tasir. Bu script ikinci yarisidir: `Durum = Tamamlandi` olan her
gorev icin o onkayda bir SONUC ekler. Onsuz registry yalniz niyet tutar ve
hicbir gorevin hukmu kayda gecmez.

NE YAZAR, NE YAZMAZ
-------------------
* Yalniz EKLER. Var olan bir RES-<id> girdisine dokunmaz (R4, append-only);
  ikinci kosum ayni gorevi atlar ve bunu soyler.
* Tier DEGISTIRMEZ. Terfi, R7 geregi yazardan baska birinin onayidir; bu
  script `decision_confirmed_by` alanini BOS birakir.
* `Hakem` sutunu bos olan tamamlanmis gorev, oz-beyandir: sonuc yazilir ama
  karar "tier degismez (hakem author, R8)" olur. Hakemi olan gorevde de terfi
  ONERILMEZ: ikili kabul kriterinin baseline'i yoktur ve Mizan R2 baseline'siz
  bir deneyden K onerisini yasaklar. Script bunu denedi, dogrulayici reddetti.
* `artifact_freshness` (R25) cizelgeden BILINEMEZ: cizelge bir durum tutar,
  hangi build'in gectigini degil. Alan bunu acikca soyleyerek yazilir;
  onaylayan kisi doldurmadan terfi etmemelidir.

Kullanim:
    python iskele_results.py --xlsx tracker.xlsx --registry registry.yaml
    python iskele_results.py ... --out registry.new.yaml   # yerinde yazma yerine
    python iskele_results.py ... --check                   # yazmadan ozet

Cikis kodlari: 0 yazildi/yazilacak bir sey yok · 2 kullanim/veri hatasi.
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from progress import load_config, load_tasks  # noqa: E402

DONE = "Tamamlandi"


def result_for(task, hyp, today):
    tid = task["id"]
    hakem = (task.get("hakem") or "").strip()
    runtime = bool(hakem) or (hyp.get("arbiter") or {}).get("class") == "runtime"
    measured = (f"tracker.xlsx: {tid} Durum={DONE}"
                + (f", Hakem={hakem}" if hakem else ", Hakem sutunu bos")
                + (f", Bitis={task['bitis']}" if task.get("bitis") else ""))
    res = {
        "id": f"RES-{tid}",
        "experiment": f"EXP-{tid}",
        "hypothesis": hyp["id"],
        "date": today,
        "measured": measured,
        "threshold_met": "yes",
        "surprising_positive": False,
        "decision": ("acceptance met by a named arbiter; no tier change proposed "
                     "(R2: a binary acceptance has no baseline)" if runtime else
                     "no tier change: self-reported (arbiter author, R8)"),
        "decision_confirmed_by": "",
        "honesty_annexes": [
            "kaynak cizelgedeki Durum hucresidir; kriterin kosuldugunu bu script dogrulamaz",
            ("hakem cizelgede adlandirildi ama ciktisi buraya tasinmadi" if runtime else
             "hakem yok: gorevi yapan kisi kendi isini tamamlandi isaretledi"),
        ],
    }
    if runtime:
        res["artifact_freshness"] = (
            "BILINMIYOR — tracker.xlsx bir durum tutar, hangi build'in gectigini "
            "degil. Onaylayan kisi hakem ciktisini ve commit'ini buraya yazmadan "
            "terfiyi onaylamamalidir.")
    return res


def experiment_for(task, hyp):
    tid = task["id"]
    return {
        "id": f"EXP-{tid}",
        "hypotheses": [hyp["id"]],
        "design": "gorevin kabul kriteri, gorev tamamlandiginda bir kez kosulur",
        "baseline": {"description": "none",
                     "justification": "kabul kriteri ikili bir hukumdur; karsilastirilacak kol yok"},
        "confound_controls": [
            {"confound": c, "control": "accepted risk -- rationale: cizelge yalniz durumu "
                                       "tasir; onaylayan kisi hakem ciktisina bakar"}
            for c in (hyp.get("confounds") or [])],
        "status": "completed",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", default="tracker.xlsx")
    ap.add_argument("--config", default="iskele.config.json")
    ap.add_argument("--registry", default="registry.yaml",
                    help="iskele_to_registry.py ciktisi")
    ap.add_argument("--out", default=None, help="varsayilan: --registry uzerine")
    ap.add_argument("--check", action="store_true", help="yazma, ozet bas")
    a = ap.parse_args()

    cfg = load_config(a.config)
    tasks, issues = load_tasks(a.xlsx, cfg)
    errors = [m for lvl, m in issues if lvl == "ERROR"]
    for lvl, m in issues:
        print(f"  {'HATA ' if lvl == 'ERROR' else 'UYARI'}: {m}", file=sys.stderr)
    if errors:
        print("cizelgede hata var — sonuc YAZILMADI", file=sys.stderr)
        return 2

    try:
        reg = yaml.safe_load(Path(a.registry).read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        print(f"HATA: {a.registry} okunamadi — {exc}", file=sys.stderr)
        return 2
    if not isinstance(reg, dict) or not isinstance(reg.get("hypotheses"), list):
        print(f"HATA: {a.registry} bir Mizan registry'si degil (hypotheses yok)",
              file=sys.stderr)
        return 2

    hyps = {h.get("id"): h for h in reg["hypotheses"] if isinstance(h, dict)}
    results = reg.setdefault("results", []) or []
    reg["results"] = results
    exps = reg.setdefault("experiments", []) or []
    reg["experiments"] = exps
    have_res = {r.get("id") for r in results if isinstance(r, dict)}
    have_exp = {e.get("id") for e in exps if isinstance(e, dict)}

    today = date.today().isoformat()
    added, skipped, orphan = [], [], []
    for t in tasks:
        if t["durum"] != DONE:
            continue
        hyp = hyps.get(f"H-{t['id']}")
        if hyp is None:
            orphan.append(t["id"])
            continue
        if f"RES-{t['id']}" in have_res:
            skipped.append(t["id"])
            continue
        if f"EXP-{t['id']}" not in have_exp:
            exps.append(experiment_for(t, hyp))
        results.append(result_for(t, hyp, today))
        hyp.setdefault("history", []).append(
            {"date": today, "event": f"RES-{t['id']} eklendi (iskele_results.py); tier degismedi"})
        added.append(t["id"])

    print(f"tamamlanan gorev -> sonuc: {len(added)} eklendi, "
          f"{len(skipped)} zaten kayitli (dokunulmadi)")
    if orphan:
        print(f"  UYARI: registry'de onkaydi olmayan tamamlanmis gorev: "
              f"{', '.join(orphan)} — once iskele_to_registry.py", file=sys.stderr)
    if added and not a.check:
        out = a.out or a.registry
        Path(out).write_text(yaml.safe_dump(reg, allow_unicode=True, sort_keys=False,
                                            width=88), encoding="utf-8")
        print(f"  yazildi: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
