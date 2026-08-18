#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iskele_to_registry.py — backlog markdown -> Mizan registry (onkayit).

NE YAPAR
--------
Her backlog gorevinin KABUL KRITERI, is baslamadan once yazilmis bir curutme
kosuludur. Mizan'in R1 kurali tam olarak bunu ister: esik + curutme, sonuctan
ONCE. Yani backlog zaten bir onkayit kumesidir; bu script onu Mizan'in okudugu
sema haline getirir.

Esleme:
    gorev            -> hypotheses[] girdisi (tier S, status preregistered)
    kabul kriteri    -> refutation (+ threshold.support)
    Bag.:            -> relations.depends_on
    tahmin (S/M/L)   -> cost
    faz/epik/katman  -> origin

HAKEM VARSAYILANI — bilerek rahatsiz edici
------------------------------------------
Varsayilan `arbiter.class` = **author**. Cunku cizelgedeki `Durum` sutununu
isi yapan kisi doldurur; bu bir olcum degil, oz-beyandir. Mizan'in R8'i bu
durumda K'ye terfiyi yasaklar ve kalici bir KKE tasir — dogru davranis budur.

Bir gorevin hakemini yukseltmek icin backlog'a kabul kriterinin yanina
calistirilabilir bir hakem yaz:

    - *Kabul:* Yetkisiz istek 403 alir. **Hakem:** pytest tests/test_authz.py

`**Hakem:**` (veya `**Arbiter:**`) gorulen gorevlerde sinif `runtime` olur ve
K'ye terfi yolu acilir. Yazilmadiginda script bunu SESSIZCE yukseltmez; ozet
satirinda kac gorevin oz-beyanda kaldigini basar.

Kullanim:
    python iskele_to_registry.py --backlog 03-gorev-listesi.md --out registry.yaml
    python iskele_to_registry.py --backlog ... --project "PortalX" --owner "your-org"
    python iskele_to_registry.py --backlog ... --phase F1        # tek faz
"""
import argparse, sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backlog_to_tracker import parse_backlog  # noqa: E402

COST = {"S": "~0.75 is-gunu", "M": "~1.5 is-gunu", "L": "~4 is-gunu"}
ARBITER_KEYS = ("**Hakem:**", "**Arbiter:**", "**Hakem**:", "**Arbiter**:")


def split_arbiter(kabul):
    """'... **Hakem:** pytest x' -> ('...', 'pytest x') | (kabul, None)"""
    for key in ARBITER_KEYS:
        idx = kabul.find(key)
        if idx >= 0:
            return kabul[:idx].strip().rstrip("."), kabul[idx + len(key):].strip()
    return kabul, None


def to_hypothesis(task, today):
    kabul, who = split_arbiter(task.get("kabul", "").strip())
    deps = [d.strip() for d in task["bagimlilik"].replace(";", ",").split(",")
            if d.strip() and d.strip() not in {"—", "-", "–"}]

    if who:
        arbiter = {
            "class": "runtime",
            "who": who,
            "independent_of_author": True,
            "latency": "seconds",
            "calibration": "deterministic pass/fail — esik yok, ikili hukum",
        }
    else:
        # Sessiz varsayim yasak: yukseltmiyoruz, neden yukseltilmedigini yaziyoruz.
        arbiter = {
            "class": "author",
            "who": "gorevi yapan kisi (tracker.xlsx Durum sutunu)",
            "independent_of_author": False,
            "latency": "seconds",
            "calibration": "yok — oz-beyan; kalici KKE, K'ye terfi kapali",
        }

    return {
        "id": f"H-{task['id']}",
        "version": 1,
        "tier": "S",
        "status": "preregistered",
        "preregistered": today,
        "title": task["gorev"],
        "formal": (f"{task['id']} gorevi kabul kriterini saglar: "
                   f"{kabul or 'KABUL KRITERI YAZILMAMIS'}"),
        "origin": f"iskele backlog · faz {task['faz']} · epik {task['epik']} "
                  f"· katman {task['katman'] or '—'}",
        "metric": {
            "name": "acceptance_criterion_met",
            "instrument": who or "elle dogrulama (kayit: tracker.xlsx)",
        },
        "arbiter": arbiter,
        "threshold": {
            "support": "kabul kriteri fiilen kosuldu ve gecti",
            "refute": "kabul kriteri kosuldu ve gecmedi",
            "underpowered": "kriter kosulmadi -> hukum YOK (Durum 'Tamamlandi' olamaz)",
        },
        "refutation": (f"Kabul kriteri saglanmiyor: {kabul}" if kabul else
                       "YAZILMAMIS — kabul kriteri olmayan gorev curutulemez, "
                       "yani onkayit degildir. Backlog'u duzelt."),
        "two_sided": ("Gecerse gorev kapanir; gecmezse ya uygulama ya da kriterin "
                      "kendisi hatalidir — ikisi de bilgi tasir."),
        "informativeness_precondition": (
            "Bagimliliklar tamamlanmis olmali: " + (", ".join(deps) if deps else "yok")),
        "prior_art": [],
        "confounds": ["mutlu-yol girdisi", "kriterin kosulmadan tamamlandi isaretlenmesi"],
        "relations": {"depends_on": [f"H-{d}" for d in deps],
                      "contradicts": [], "refines": []},
        "cost": COST.get(task["tahmin"], task["tahmin"]),
        "history": [{"date": today, "event": f"iskele backlog satir {task['satir']}'den onkayit"}],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backlog", default="03-gorev-listesi.md")
    ap.add_argument("--out", default="registry.yaml")
    ap.add_argument("--project", default="Proje")
    ap.add_argument("--owner", default="")
    ap.add_argument("--phase", default=None, help="yalniz bu fazin gorevleri (or. F1)")
    a = ap.parse_args()

    tasks, problems = parse_backlog(a.backlog)
    for p in problems:
        print(f"  UYARI: {p}", file=sys.stderr)
    if not tasks:
        return 2

    if a.phase:
        tasks = [t for t in tasks if t["faz"] == a.phase]
        if not tasks:
            print(f"  HATA: '{a.phase}' fazinda gorev yok", file=sys.stderr)
            return 2

    today = date.today().isoformat()
    hyps = [to_hypothesis(t, today) for t in tasks]

    missing = [h["id"] for h in hyps if "YAZILMAMIS" in h["refutation"]]
    self_reported = [h["id"] for h in hyps if h["arbiter"]["class"] == "author"]

    registry = {
        "registry": {
            "project": a.project,
            "owner": a.owner,
            "schema_version": "1.2",
            "methodology": "mizan-v2",
            "created": today,
            "notes": (
                "iskele_to_registry.py tarafindan backlog'dan uretildi. Her girdi "
                "bir GOREV onkaydidir, bir arastirma hipotezi degil: iddia 'bu is "
                "kabul kriterini sagliyor'dur. Tier'lar S baslar; terfi, kriterin "
                "fiilen kosulmasiyla ve R7 geregi yazardan baska biri onaylayarak "
                "olur. Bu dosya elle zenginlestirilebilir; yeniden uretim uzerine "
                "yazar, o yuzden zenginlestirdikten sonra kaynagi backlog degil bu "
                "dosya say."),
        },
        "hypotheses": hyps,
        "experiments": [],
        "results": [],
        "bugs": [],
        "features": [],
    }

    Path(a.out).write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False, width=88),
        encoding="utf-8")

    print(f"{len(hyps)} gorev -> onkayit: {a.out}")
    print(f"  hakem 'author' (oz-beyan, K kapali): {len(self_reported)}/{len(hyps)}")
    if missing:
        print(f"  KABUL KRITERI YOK: {', '.join(missing)}", file=sys.stderr)
        print("  Kabul kriteri olmayan gorev curutulemez; backlog'u duzelt.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
