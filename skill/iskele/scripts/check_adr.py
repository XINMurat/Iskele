#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ADR zincirini dogrula: durum sozlugu, ileri isaretler, supersede tutarliligi.

NEDEN VAR
---------
ADR kaydinin tek isi alti ay sonra okunmaktir. O yuzden iki seyi ayni anda
tasimasi gerekir: bugun hangi kararin yururlukte oldugunu, ve degistirilen bir
kararin nereye gittigini. Ikisi de duzyazida yasarsa hicbir seye bagli degildir
-- "degistirildi (-> ADR-7)" yazan bir satir, ADR-7 hic yazilmamis olsa bile
ayni derecede ikna edicidir. Bu script onu baglar.

Kontrol ettikleri:

  1. Her ADR'nin bir **Durum** satiri var ve degeri sozlukten.
  2. `Yerini aldi -> ADR-x` diyen her kayitta x **cozuluyor** (o ADR var).
  3. Yerini alan ADR **geriye dogru** tutarli: yeni karar yururlukte
     (`Onerildi` ya da `Kabul edildi`), eskisi degil. Ikisi birden yururlukte
     ise ekip iki celiskili karari ayni anda uyguluyor demektir.
  4. Dongu yok: A, B'nin yerini alip B de A'nin yerini alamaz.
  5. Her ADR'de **Degerlendirilen secenekler** bolumu var ve en az iki secenek
     listeliyor. Tek secenekli bir karar, karar degil kayittir.

Kontrol ETMEDIGI sey: kararin dogru olup olmadigi. Bunu hicbir script bilemez.

KULLANIM
--------
    python check_adr.py                       # 06-riskler-ve-kararlar.md
    python check_adr.py --file <yol>
    python check_adr.py --quiet               # yalniz hatalari bas

Cikis: 0 temiz · 1 zincir hatasi · 2 dosya okunamadi.
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

DEFAULT_FILE = "06-riskler-ve-kararlar.md"

# Durum sozlugu. Sabit tutulur: acik uclu bir alan, bir sure sonra herkesin
# kendi kelimesini yazdigi ve hicbir seyin karsilastirilamadigi bir alandir.
LIVE = {"onerildi", "kabul edildi"}
DEAD = {"reddedildi", "kullanimdan kalkti"}
SUPERSEDED = "yerini aldi"
VOCAB = sorted(LIVE | DEAD | {SUPERSEDED})

RE_HEADING = re.compile(r"^#{2,4}\s*ADR-(\d+)\s*[—\-–]\s*(.+?)\s*$", re.M)
RE_STATUS = re.compile(r"^\s*[-*]\s*\*\*Durum:?\*\*\s*(.+?)\s*$", re.M)
RE_OPTIONS = re.compile(r"^\s*[-*]\s*\*\*De[gğ]erlendirilen se[cç]enekler:?\*\*",
                        re.M | re.I)
RE_FORWARD = re.compile(r"ADR-(\d+)")

# Turkce katlama: dosyaya "Yerini aldı" yazilir, karsilastirma ASCII yapilir.
_FOLD = str.maketrans("ıİşŞğĞüÜöÖçÇâÂîÎ", "iIsSgGuUoOcCaAiI")


def fold(s: str) -> str:
    return s.translate(_FOLD).strip().lower()


def status_of(raw: str) -> str:
    """Durum satirindan sozluk degerini cikar.

    Satir "Yerini aldi -> ADR-2 - 2026-03-01" gibi ok, numara ve tarih tasir.
    Ilk hali bunlari desenle ayiklamaya calisiyordu ve U+2192 okunu desene
    koymayi unuttugum icin TEMIZ bir dosyada kirmizi verdi -- pozitif kontrolun
    yakaladigi ilk sey oydu. Sozlukten one dogru eslemek daha saglam: yeni bir
    ayrac ya da tarih bicimi eklendiginde bozulmaz.
    """
    f = fold(raw)
    for v in (SUPERSEDED, "kullanimdan kalkti", "kabul edildi", "reddedildi",
              "onerildi"):
        if f.startswith(v):
            return v
    return f


def parse(text: str) -> list[dict]:
    """Her ADR icin: numara, baslik, ham durum, ileri isaret, secenek var mi."""
    heads = list(RE_HEADING.finditer(text))
    out = []
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[start:end]
        st = RE_STATUS.search(body)
        raw = st.group(1).strip() if st else ""
        # Ileri isaret yalniz DURUM satirindan okunur. Govdedeki serbest bir
        # "ADR-3'te tartisildi" atfi supersede degildir; ikisini karistiran bir
        # checker, her capraz atfi zincir sanip gurultu uretir.
        fwd = RE_FORWARD.search(raw)
        out.append(dict(
            no=int(m.group(1)),
            title=m.group(2).strip(),
            raw_status=raw,
            status=status_of(raw),
            supersedes=int(fwd.group(1)) if fwd else None,
            has_options=bool(RE_OPTIONS.search(body)),
            option_count=len(re.findall(r"^\s{2,}[-*]\s+\S", body, re.M)),
        ))
    return out


def check(adrs: list[dict]) -> list[str]:
    problems: list[str] = []
    by_no = {a["no"]: a for a in adrs}

    for a in adrs:
        tag = f"ADR-{a['no']}"

        if not a["raw_status"]:
            problems.append(f"{tag}: Durum satiri yok. Yururlukte mi, degil mi?")
            continue
        if a["status"] not in VOCAB:
            problems.append(
                f"{tag}: '{a['raw_status']}' durum sozlugunde yok "
                f"({', '.join(VOCAB)})")

        if a["status"] == SUPERSEDED:
            if a["supersedes"] is None:
                problems.append(
                    f"{tag}: '{SUPERSEDED}' diyor ama hangi ADR'nin yerini "
                    f"aldigini soylemiyor. Ileri isaret zorunlu.")
            elif a["supersedes"] not in by_no:
                problems.append(
                    f"{tag}: ADR-{a['supersedes']}'e isaret ediyor, o ADR yok")
            else:
                nxt = by_no[a["supersedes"]]
                if nxt["status"] in DEAD:
                    problems.append(
                        f"{tag}: yerini ADR-{nxt['no']} aldi ama o da "
                        f"'{nxt['raw_status']}' — yururlukte hicbir karar yok")
                if nxt["supersedes"] == a["no"]:
                    problems.append(
                        f"{tag} ile ADR-{nxt['no']} birbirinin yerini almis "
                        f"(dongu); zincir ileri gitmiyor")
        elif a["supersedes"] is not None:
            problems.append(
                f"{tag}: durumu '{a['raw_status']}' ama ileri isaret tasiyor. "
                f"Isaret varsa durum '{SUPERSEDED}' olmali.")

        if not a["has_options"]:
            problems.append(
                f"{tag}: 'Degerlendirilen secenekler' bolumu yok. Secilmeyen "
                f"yol, kararin en pahali parcasidir.")
        elif a["option_count"] < 2:
            problems.append(
                f"{tag}: tek secenek listelenmis. Iki secenegi olmayan bir "
                f"karar, karar degil kayittir (hicbir sey yapmama da bir secenek).")

    return problems


def main() -> int:
    # Windows konsolu varsayilan olarak cp1254/cp857 kullanir ve dosyadan
    # okunan Turkce durum metnini bozar. Hatayi okunamaz basan bir checker,
    # hatayi bulmayi zorlastirir.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=DEFAULT_FILE)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if not os.path.isfile(a.file):
        print(f"HATA: dosya yok: {a.file}", file=sys.stderr)
        return 2
    text = io.open(a.file, encoding="utf-8", errors="replace").read()

    adrs = parse(text)
    if not adrs:
        print(f"HATA: {a.file} icinde ADR basligi bulunamadi "
              f"(beklenen bicim: '### ADR-1 — baslik')", file=sys.stderr)
        return 2

    problems = check(adrs)
    if problems:
        print("ADR zinciri tutmuyor:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        print("\nDurum sozlugu ve zincir kurali: sablonun 2. bolumu.",
              file=sys.stderr)
        return 1

    if not a.quiet:
        live = [f"ADR-{x['no']}" for x in adrs if x["status"] in LIVE]
        sup = [f"ADR-{x['no']}->ADR-{x['supersedes']}"
               for x in adrs if x["status"] == SUPERSEDED]
        print(f"ok  {len(adrs)} ADR · yururlukte: {', '.join(live) or 'yok'}"
              + (f" · zincir: {', '.join(sup)}" if sup else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
