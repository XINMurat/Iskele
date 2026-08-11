#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kiyas_to_backlog.py — Kiyas tohum partisi -> iskele backlog markdown'i.

NE YAPAR
--------
Kiyas'in urettigi her tohum zaten "en ucuz curutme" tasir: onu oldurecek en
kucuk test. Bir backlog gorevinin kabul kriterinden istedigi sey de tam olarak
budur — calistirilabilir bir hukum. Esleme bu yuzden zorlama degil:

    seed.claim                    -> gorev basligi
    seed.cheapest_refutation.test -> *Kabul:* (kriter)
    seed.cost                     -> tahmin (S/M/L)
    seed.arbiter.who              -> **Hakem:** (iskele_to_registry.py bunu okur)
    seed.id                       -> gorevin izi (yorumda kalir)

TIER FILTRESI — sessizce is'e cevirmiyoruz
------------------------------------------
Yalniz `H-aday` tohumlar goreve donusur. Gerekce: `S` (spekulatif) bir tohum
henuz is degil, arastirma sorusudur; onu backlog'a gorev diye koymak, hakemi
olmayan bir seyi planlanmis is gibi gostermek olur. `S` / `NK` / `GB` tohumlar
dosyanin sonunda **yorum blogu** olarak listelenir: gorunur kalirlar ama efora
sayilmazlar. `handoff.status: declined` olanlar tamamen atlanir.

Tahmin de sessizce varsayilmaz: `cost` alani S/M/L'ye cozulemezse gorev `(M)`
alir ve satirin sonuna `<!-- TAHMIN: kalibresiz -->` isareti dusulur.

Kullanim:
    python kiyas_to_backlog.py --seeds seeds.yaml --phase F2 --layer X --out yeni.md
    python kiyas_to_backlog.py --seeds seeds.yaml --start-no 7 --append 03-gorev-listesi.md
"""
import argparse, re, sys
from pathlib import Path

import yaml

WORK_TIERS = {"H-aday"}
SIZE_HINT = [
    (re.compile(r'\b(kucuk|small|hours?|saat|yarim gun|half[- ]day)\b', re.I), "S"),
    (re.compile(r'\b(orta|medium|1-2\s*g[uü]n|days?)\b', re.I), "M"),
    (re.compile(r'\b(buyuk|large|hafta|weeks?|3-5\s*g[uü]n)\b', re.I), "L"),
]


def size_of(cost):
    """cost serbest metnini S/M/L'ye cozer; cozemezse (None) doner."""
    if not cost:
        return None
    c = str(cost).strip()
    if c.upper() in {"S", "M", "L"}:
        return c.upper()
    for rx, size in SIZE_HINT:
        if rx.search(c):
            return size
    return None


def one_line(text):
    return " ".join(str(text or "").split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", required=True, help="kiyas-seed.yaml partisi")
    ap.add_argument("--phase", default="F2", help="hedef faz kodu (or. F2)")
    ap.add_argument("--layer", default="X", help="katman kodu (INF/BE/FE/X)")
    ap.add_argument("--epic", default=None, help="epik basligi (varsayilan: batch.problem)")
    ap.add_argument("--start-no", type=int, default=1, help="ilk gorev numarasi")
    ap.add_argument("--out", default=None, help="dosyaya yaz (varsayilan: stdout)")
    a = ap.parse_args()

    data = yaml.safe_load(Path(a.seeds).read_text(encoding="utf-8")) or {}
    batch = data.get("batch") or {}
    seeds = data.get("seeds") or []
    if not seeds:
        print("  HATA: 'seeds' bos veya yok", file=sys.stderr)
        return 2

    work, parked, declined = [], [], 0
    for s in seeds:
        if (s.get("handoff") or {}).get("status") == "declined":
            declined += 1
            continue
        (work if s.get("tier") in WORK_TIERS else parked).append(s)

    epic_code = f"{a.phase}.K"
    epic_name = a.epic or one_line(batch.get("problem")) or "Kiyas devri"
    out = [f"### Epik {epic_code} — {epic_name[:80]}", ""]

    uncalibrated = 0
    for i, s in enumerate(work, start=a.start_no):
        tid = f"{a.phase}-{a.layer}-{i:02d}"
        size = size_of(s.get("cost"))
        if size is None:
            size, uncalibrated = "M", uncalibrated + 1
        title = one_line(s.get("claim")) or f"(basliksiz tohum {s.get('id')})"

        test = one_line((s.get("cheapest_refutation") or {}).get("test"))
        arb = (s.get("arbiter") or {})
        who = one_line(arb.get("who"))
        kabul = test or "EKSIK — tohumda cheapest_refutation.test yok"
        if who and arb.get("class") in {"runtime", "instrument", "third_party"}:
            kabul += f" **Hakem:** {who}"

        mark = "  <!-- TAHMIN: kalibresiz -->" if size_of(s.get("cost")) is None else ""
        out.append(f"- [ ] **{tid}** ({size}) {title} **Bağ.:** —{mark}")
        out.append(f"  - *Kabul:* {kabul}")
        out.append(f"  - <!-- kiyas: {s.get('id')} · illet: {one_line(s.get('illet'))[:120]} -->")
        out.append("")

    if parked:
        out += ["<!-- ================================================================",
                "     GOREV DEGIL — henuz is olmayan tohumlar. Gorunur birakiliyor ki",
                "     sessizce kaybolmasinlar; efora SAYILMIYORLAR. Bir tohum ancak",
                "     hakemi ve kirilma noktasi netlestiginde (tier H-aday) goreve",
                "     donusur.",
                "     ---------------------------------------------------------------"]
        for s in parked:
            out.append(f"     [{s.get('tier')}] {s.get('id')} — {one_line(s.get('claim'))[:100]}")
        out += ["     ================================================================ -->", ""]

    text = "\n".join(out)
    if a.out:
        Path(a.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    print(f"{len(work)} gorev · {len(parked)} park edildi (is degil) · "
          f"{declined} reddedilmis atlandi", file=sys.stderr)
    if uncalibrated:
        print(f"  UYARI: {uncalibrated} gorevin tahmini kalibresiz — (M) verildi, "
              f"satirlar isaretlendi. Efor toplamina guvenmeden once elle gozden gecir.",
              file=sys.stderr)
    if not work:
        print("  UYARI: hicbir tohum H-aday degil — backlog'a gorev girmedi.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
