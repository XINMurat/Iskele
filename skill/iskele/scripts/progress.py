#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
progress.py — efor-agirlikli ilerleme ureteci (iskele).

tracker.xlsx (Takip sekmesi) + iskele.config.json  ->  raporun GEN bolgelerini yazar.

Ilke:
  * SAYILAR veriden gelir (xlsx).
  * PROSE yapilandirmadan gelir (iskele.config.json).
  * GEN:...:BEGIN/END disindaki her seye DOKUNULMAZ (elle duzenlenebilir kalir).
  * Bilinmeyen deger SESSIZCE varsayilana dusmez: uyarir ya da yazmaz.

Kullanim:
    python progress.py                       # varsayilan yollar
    python progress.py --check               # yazmadan ozet bas
    python progress.py --xlsx X --html Y --config C
    python progress.py --self-test           # gomulu regresyon testleri

Cikis kodlari: 0 basarili · 2 dogrulama hatasi · 3 degismez ihlali.
Bagimlilik: openpyxl
"""
import argparse, json, re, subprocess, sys, tempfile
import datetime
from datetime import date
from pathlib import Path

from openpyxl import load_workbook

COL = dict(id="ID", faz="Faz", epik="Epik", tahmin="Tahmin", durum="Durum")
# Opsiyonel sutun: eski cizelgelerde yok. YOKSA gosterge hesaplanmaz ve rapora
# "veri yok" yazilir — %0 yazilmaz. Veri yoklugunu sifir olarak gostermek,
# "sessiz varsayim" kirmizi cizgisinin ta kendisidir.
OPT_COL = dict(hakem="Hakem", maliyet="Maliyet",
               baslangic="Baslangic", bitis="Bitis")
# Maliyet: bu gorevi ilerleten oturum(lar)in maliyeti, elle yazilir. Birim
# projeye kalmis (token ya da para) ve rapor birimi BILMEZ -- orani hesaplar,
# tutari yorumlamaz. tools/session_cost.py oturum toplamini olcer; hangi goreve
# yazilacagi bir ATIFTIR ve o hukmu yalnizca oturumu kosan kisi verebilir.
# Gecen sure: Bitis - Baslangic. EFOR DEGILDIR ve rapor onu efor diye
# adlandirmaz -- 5 gun acik duran gorev 2 saatlik is olabilir. Olculen sey
# "isin ne kadar surdugu" degil "gorevin ne kadar acik kaldigi"dir.

# Faz kapanis skorkarti: OPSIYONEL bir sekme, elle doldurulur. Buradaki her
# sayi OZ-BEYANDIR -- hakem = yazar -- ve rapor bunu her seferinde soyler.
# Sekme yoksa gosterge "olculmedi" basar, sifir basmaz. Skorkartin isi
# ekibi notlamak degil, PLANIN nereden sizdirdigini gostermek.
SCORE_SHEET = "Skorkart"
# Cift sekmesi: yeniden birlestirme pasinin kaydi. Backlog'u atomize etmek,
# yalnizca IKI ozellik ayni anda etkinken var olan kusuru yok eden islemdir;
# bu sekme o pasin sonucunun yasadigi yerdir. OPSIYONELDIR -- sekmesi olmayan
# eski bir cizelge hatasiz okunur ve rapor "olculmedi" basar, "0 cift" degil.
PAIR_SHEET = "Cift"
PAIR_COL = dict(faz="Faz", ozellik="Ozellik", garanti="Garanti",
                sira="SiraOnemli", gerekli_sira="GerekliSira",
                sonuc="Sonuc", not_="Not")
# tutuyor  = ozellik etkinken garanti hala gecerli
# kiriliyor = cift garantiyi bozuyor -- bulgu
# bakilmadi = cift listelendi ama sinanmadi; sifir DEGIL, acik is
PAIR_RESULTS = ("tutuyor", "kiriliyor", "bakilmadi")
SCORE_COL = dict(
    faz="Faz",
    revizyon="BacklogRevizyon",           # faz acildiktan sonra degisen gorev
    tur="YenidenTur",                     # birden fazla kez geri donen gorev
    kriter="KriterYenidenYazilan",        # isten SONRA yeniden yazilan kriter
    ikiz="IkizBoslugu",                   # tuketen-ikiz boslugu (RR-03)
    ikiz_kapida="IkizKapida",             # ...kacinin KAPIDA bulundugu
    senaryo="SenaryoProvali",             # senaryo listesinin yakaladigi
    senaryo_tesadufi="SenaryoTesadufi",   # tesaduffen fark edilen
    kapsam="KapsamDisi",                  # faz disina cikma (RR-07)
    rampa="Rampalar",                     # kullanilan RR kodlari (metin)
    kacan="Kacan",                        # kapidan sonra bulunan, kapsanan hata
    cikarim="Cikarim",                    # 1-2 cumle
)
SCORE_NUM = ("revizyon", "tur", "kriter", "ikiz", "ikiz_kapida",
             "senaryo", "senaryo_tesadufi", "kapsam", "kacan")
# OPSIYONEL sutun: eski cizelgelerde yok, ve yoklugu hata degildir -- zorunlu
# yapsaydik her mevcut kit "sekmeyi yeniden uret" hatasiyla kirilirdi. Kacagin
# yanindaki sinif (RR-13): onu yakalamasi gereken kontrol, ya da bu kacak
# sayesinde artik var olan kontrol. Sayi tek basina dongu degildir.
SCORE_COL_OPT = dict(kacan_sinifi="KacanSinifi")

DEFAULTS = {
    "phases": [],
    "effort_weights": {"S": 0.75, "M": 1.5, "L": 4.0},
    "status_credit": {"Tamamlandi": 1.0, "Devam": 0.0,
                      "Bloke": 0.0, "Yapilacak": 0.0},
    "workdays_per_month": 21,
    "phase_meta": {}, "epic_display": {}, "static_steps": [], "flow": [],
}

# Turkce-duyarli katlama: xlsx "Tamamlandi" tutar, insan eli "Tamamlandı" yazar.
_TR_FOLD = str.maketrans("ıİşŞğĞüÜöÖçÇ", "iIsSgGuUoOcC")


def norm(s):
    return str(s or "").strip().translate(_TR_FOLD).lower()


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


def git_short():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                       stderr=subprocess.DEVNULL, text=True).strip() or "—"
    except Exception:
        return "—"


def load_config(path):
    cfg = dict(DEFAULTS)
    if path and Path(path).exists():
        cfg.update(json.loads(Path(path).read_text(encoding="utf-8")))
    return cfg


# ---------------------------------------------------------------- VERI
def load_tasks(xlsx, cfg):
    """xlsx -> (tasks, issues). issues: ('ERROR'|'WARN', mesaj)

    Opsiyonel sutunlarin VARLIGI her gorevin `_cols` alaninda tasinir; bos
    hucre ile hic olmayan sutun ayri seylerdir ve rapor ikisini ayri basar.
    """
    wb = load_workbook(xlsx, data_only=True)
    if "Takip" not in wb.sheetnames:
        sys.exit("HATA: 'Takip' sekmesi yok.")
    ws = wb["Takip"]
    headers = {c.value: i for i, c in enumerate(ws[1])}
    for name in COL.values():
        if name not in headers:
            sys.exit(f"HATA: '{name}' sutunu Takip sekmesinde yok.")

    phases = cfg["phases"]
    st_alias = {norm(k): k for k in cfg["status_credit"]}
    st_alias.update({norm("Tamamlandı"): "Tamamlandi",
                     norm("Yapılacak"): "Yapilacak"})
    ef_alias = {norm(k): k for k in cfg["effort_weights"]}
    ph_alias = {norm(p): p for p in phases}

    tasks, issues, seen = [], [], {}
    for rno, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        tid = row[headers[COL["id"]]]
        if not tid:
            continue
        tid = str(tid).strip()
        if tid in seen:
            issues.append(("ERROR", f"satir {rno}: '{tid}' ID'si mukerrer "
                                    f"(ilk: satir {seen[tid]})"))
        seen[tid] = rno

        raw = {k: str(row[headers[v]] or "").strip() for k, v in COL.items()}
        raw.update({k: (str(row[headers[v]] or "").strip() if v in headers else "")
                    for k, v in OPT_COL.items()})

        faz = ph_alias.get(norm(raw["faz"]))
        if faz is None:
            issues.append(("ERROR", f"satir {rno} [{tid}]: gecersiz Faz "
                                    f"'{raw['faz']}' (beklenen: {'/'.join(phases)})"))
            faz = raw["faz"]

        tahmin = ef_alias.get(norm(raw["tahmin"]))
        if tahmin is None:
            issues.append(("ERROR", f"satir {rno} [{tid}]: gecersiz Tahmin "
                                    f"'{raw['tahmin']}' "
                                    f"(beklenen: {'/'.join(cfg['effort_weights'])})"))
            tahmin = raw["tahmin"]

        if not raw["durum"]:
            durum = "Yapilacak"
            issues.append(("WARN", f"satir {rno} [{tid}]: Durum bos -> 'Yapilacak'"))
        else:
            durum = st_alias.get(norm(raw["durum"]))
            if durum is None:
                issues.append(("ERROR", f"satir {rno} [{tid}]: gecersiz Durum "
                                        f"'{raw['durum']}'"))
                durum = raw["durum"]
            elif durum != raw["durum"]:
                issues.append(("WARN", f"satir {rno} [{tid}]: Durum "
                                       f"'{raw['durum']}' -> '{durum}' normalize edildi"))

        if not raw["epik"]:
            issues.append(("ERROR", f"satir {rno} [{tid}]: Epik bos"))

        tasks.append(dict(id=tid, faz=faz, epik=raw["epik"],
                          tahmin=tahmin, durum=durum, hakem=raw["hakem"],
                          maliyet=raw["maliyet"], baslangic=raw["baslangic"],
                          bitis=raw["bitis"],
                          _cols={k: (v in headers) for k, v in OPT_COL.items()}))

    if not tasks:
        issues.append(("ERROR", "Takip sekmesinde hic gorev satiri yok"))
    return tasks, issues


def load_scorecard(xlsx, cfg):
    """xlsx -> (satirlar | None, issues). None = sekme yok = OLCULMEDI.

    Bos hucre ile hic olmayan sekme ayri seylerdir: bos hucre "bu faz icin
    doldurulmadi" der, olmayan sekme "bu proje skorkart tutmuyor" der. Ikisini
    de sifir basmak, olculmemis seyi olcum gibi gostermek olurdu.
    """
    wb = load_workbook(xlsx, data_only=True)
    if SCORE_SHEET not in wb.sheetnames:
        return None, []
    ws = wb[SCORE_SHEET]
    headers = {c.value: i for i, c in enumerate(ws[1])}
    missing = [v for v in SCORE_COL.values() if v not in headers]
    if missing:
        return None, [("ERROR", f"'{SCORE_SHEET}' sekmesinde eksik sutun: "
                                f"{', '.join(missing)} -- sekmeyi "
                                f"backlog_to_tracker.py ile yeniden uret")]

    ph_alias = {norm(p): p for p in cfg["phases"]}
    rows, issues, seen = [], [], {}
    for rno, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        raw_faz = str(row[headers[SCORE_COL["faz"]]] or "").strip()
        if not raw_faz:
            continue
        faz = ph_alias.get(norm(raw_faz))
        if faz is None:
            # Takip sekmesindeki degismez mantiginin aynisi: tanimsiz faz,
            # tabloda gorunup hicbir toplama girmeyen bir satir uretir.
            issues.append(("ERROR", f"{SCORE_SHEET} satir {rno}: '{raw_faz}' "
                                    f"faz listesinde yok {cfg['phases']}"))
            continue
        if faz in seen:
            issues.append(("ERROR", f"{SCORE_SHEET} satir {rno}: '{faz}' icin "
                                    f"ikinci satir (ilk: satir {seen[faz]})"))
            continue
        seen[faz] = rno

        rec, bad = dict(faz=faz), False
        for key in SCORE_NUM:
            cell = row[headers[SCORE_COL[key]]]
            if cell is None or str(cell).strip() == "":
                rec[key] = None          # doldurulmadi != sifir
                continue
            try:
                val = int(str(cell).strip())
            except ValueError:
                issues.append(("ERROR", f"{SCORE_SHEET} satir {rno}: "
                                        f"{SCORE_COL[key]} sayi degil: {cell!r}"))
                bad = True
                continue
            if val < 0:
                issues.append(("ERROR", f"{SCORE_SHEET} satir {rno}: "
                                        f"{SCORE_COL[key]} negatif: {val}"))
                bad = True
                continue
            rec[key] = val
        for key in ("rampa", "cikarim"):
            rec[key] = str(row[headers[SCORE_COL[key]]] or "").strip()
        for key, col in SCORE_COL_OPT.items():
            rec[key] = (str(row[headers[col]] or "").strip()
                        if col in headers else "")

        # Alt kume kontrolu: kapida bulunanlar, bulunanlarin bir parcasidir.
        # Tersi yalnizca yazim hatasi degil, gostergeyi TERS CEVIRIR: "kapida
        # yakalandi" orani 1'i asar ve tablo iyi haber gibi okunur.
        if (rec.get("ikiz") is not None and rec.get("ikiz_kapida") is not None
                and rec["ikiz_kapida"] > rec["ikiz"]):
            issues.append(("ERROR", f"{SCORE_SHEET} satir {rno}: "
                                    f"{SCORE_COL['ikiz_kapida']} "
                                    f"({rec['ikiz_kapida']}) > "
                                    f"{SCORE_COL['ikiz']} ({rec['ikiz']})"))
            bad = True
        # Faz sutunu cizelge uretilirken ONCEDEN yazilir, cunku bos bir tablo
        # doldurulmaz. Yani "satir var" ile "faz kapandi" ayni sey degildir:
        # hicbir alani doldurulmamis satir, kapanmamis fazdir ve tabloya
        # girmez. Girseydi rapor, olculmemis fazlari "olculdu, hepsi bos"
        # diye basardi.
        if (all(rec.get(k) is None for k in SCORE_NUM)
                and not rec["rampa"] and not rec["cikarim"]
                and not any(rec.get(k) for k in SCORE_COL_OPT)):
            continue
        if not bad:
            rows.append(rec)
    return rows, issues


def score_totals(rows):
    """Doldurulmus alanlarin toplami + kac fazin o alani doldurdugu.

    Sayac ayri tasinir: uc fazdan birinin doldurdugu bir toplam ile ucunun
    doldurdugu ayni toplam farkli seylerdir; rapor ikisini ayri basar.
    """
    out = {}
    for key in SCORE_NUM:
        vals = [r[key] for r in rows if r.get(key) is not None]
        out[key] = (sum(vals), len(vals)) if vals else (None, 0)
    return out


def epic_code(epik):
    parts = str(epik or "").split()
    return parts[0] if parts else "(epik yok)"


def load_pairs(xlsx, cfg):
    """xlsx -> (satirlar | None, issues). None = sekme yok = OLCULMEDI.

    Skorkart ile ayni sozlesme: olmayan sekme "bu proje cift pasi tutmuyor"
    der, bos satir "bu faz icin doldurulmadi" der, ve ikisini de sifir basmak
    olculmemis seyi olcum gibi gostermek olurdu. Sekme opsiyoneldir: zorunlu
    olsaydi sahadaki her cizelge yukseltmede kirilirdi.
    """
    wb = load_workbook(xlsx, data_only=True)
    if PAIR_SHEET not in wb.sheetnames:
        return None, []
    ws = wb[PAIR_SHEET]
    headers = {c.value: i for i, c in enumerate(ws[1])}
    missing = [v for v in PAIR_COL.values() if v not in headers]
    if missing:
        return None, [("ERROR", f"'{PAIR_SHEET}' sekmesinde eksik sutun: "
                                f"{', '.join(missing)} -- sekmeyi "
                                f"backlog_to_tracker.py ile yeniden uret")]

    ph_alias = {norm(p): p for p in cfg["phases"]}
    rows, issues = [], []
    for rno, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        cell = lambda key: str(row[headers[PAIR_COL[key]]] or "").strip()
        raw_faz = cell("faz")
        if not raw_faz:
            continue
        faz = ph_alias.get(norm(raw_faz))
        if faz is None:
            issues.append(("ERROR", f"{PAIR_SHEET} satir {rno}: '{raw_faz}' "
                                    f"faz listesinde yok: {cfg['phases']}"))
            continue
        rec = {k: cell(k) for k in PAIR_COL}
        rec["faz"] = faz
        # Faz sutunu onceden yazilidir, yani "satir var" ile "cift kaydedildi"
        # ayni sey degildir. Hicbir alani dolu olmayan satir atlanir.
        if not any(rec[k] for k in ("ozellik", "garanti", "sonuc", "not_")):
            continue
        if not rec["ozellik"] or not rec["garanti"]:
            issues.append(("ERROR", f"{PAIR_SHEET} satir {rno}: bir cift, "
                                    f"OZELLIK ve dokundugu GARANTI ile tanimlanir; "
                                    f"biri eksik"))
            continue
        sonuc = rec["sonuc"].lower()
        if sonuc not in PAIR_RESULTS:
            issues.append(("ERROR", f"{PAIR_SHEET} satir {rno}: Sonuc "
                                    f"'{rec['sonuc']}' -- gecerli degerler: "
                                    f"{', '.join(PAIR_RESULTS)}"))
            continue
        rec["sonuc"] = sonuc
        # Sira duyarli bir cift guvenli yonu tasimazsa, bulgunun yarisi
        # eksiktir: "bu ikisi tek sirada guvenli" cumlesi, hangi sira oldugunu
        # soylemedikce uygulanabilir degildir.
        if rec["sira"].lower() in ("evet", "true", "1", "x") and not rec["gerekli_sira"]:
            issues.append(("ERROR", f"{PAIR_SHEET} satir {rno}: SiraOnemli "
                                    f"isaretli ama GerekliSira bos -- guvenli "
                                    f"yon bulgunun parcasidir"))
            continue
        # Kirilan bir cift, ne oldugunu soylemeden kayda gecemez.
        if rec["sonuc"] == "kiriliyor" and not rec["not_"]:
            issues.append(("ERROR", f"{PAIR_SHEET} satir {rno}: 'kiriliyor' "
                                    f"ama Not bos -- hangi garantinin nasil "
                                    f"bozuldugu yazilmadan bulgu devredilemez"))
            continue
        rows.append(rec)
    return rows, issues


def pair_totals(rows):
    """Faz basina (toplam, kirik, bakilmadi) -- ve genel toplam."""
    per = {}
    for r in rows or []:
        d = per.setdefault(r["faz"], dict(n=0, kirik=0, bakilmadi=0))
        d["n"] += 1
        if r["sonuc"] == "kiriliyor":
            d["kirik"] += 1
        elif r["sonuc"] == "bakilmadi":
            d["bakilmadi"] += 1
    tot = dict(n=sum(d["n"] for d in per.values()),
               kirik=sum(d["kirik"] for d in per.values()),
               bakilmadi=sum(d["bakilmadi"] for d in per.values()))
    return per, tot


def _as_date(value):
    """Excel tarih hucresi -> date, ya da None. Elle yazilmis metin de kabul."""
    if value is None or value == "":
        return None
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    text = str(value).strip()[:10]
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _as_num(value):
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", "").replace(" ", ""))
    except ValueError:
        return None


def cost_and_duration(tasks, cfg):
    """Maliyet ve gecen sure gostergeleri -- ikisi de OPSIYONEL veriden.

    Uc sey hesaplanir ve ucu de ayri tutulur:

      * gecen sure  : Bitis - Baslangic, TAMAMLANMIS gorevler icin. Efor degil.
      * maliyet     : elle yazilan Maliyet sutununun toplami.
      * birim maliyet: maliyet / tamamlanan efor-gunu. ROI'nin PAYDASI budur --
        payi degil. Getiri, projenin kendi metriginden gelir ve bu script onu
        bilmez; bildigini iddia etseydi uydurmus olurdu.

    Faz faz kirilir, cunku asil bilgi seviyede degil EGIMDE: F1'de birim maliyet
    X, F3'te 0.6X ise proje kendi ic karsilastirma kolunu uretmis olur. Bu,
    "aracsiz ne olurdu" karsi-olgusunun yerini TUTMAZ ama ondan cok daha ucuzdur
    ve elde vardir.
    """
    W, CR, phases = cfg["effort_weights"], cfg["status_credit"], cfg["phases"]
    has_cost = bool(tasks) and tasks[0].get("_cols", {}).get("maliyet", False)
    has_dates = bool(tasks) and (tasks[0].get("_cols", {}).get("baslangic", False)
                                 and tasks[0].get("_cols", {}).get("bitis", False))

    per = {p: dict(cost=0.0, cost_n=0, done_eff=0.0, done_n=0, days=[], est=[])
           for p in phases}
    total = dict(cost=0.0, cost_n=0, done_eff=0.0, done_n=0, days=[], est=[])
    by_size = {}

    for t in tasks:
        faz = t["faz"]
        if faz not in per:
            continue
        done = CR.get(t["durum"], 0.0) >= 1
        eff = W.get(t["tahmin"], 0.0)
        c = _as_num(t.get("maliyet")) if has_cost else None
        if c is not None:
            per[faz]["cost"] += c; per[faz]["cost_n"] += 1
            total["cost"] += c; total["cost_n"] += 1
        if done:
            per[faz]["done_eff"] += eff
            per[faz]["done_n"] += 1
            total["done_eff"] += eff
            total["done_n"] += 1
            if has_dates:
                a, b = _as_date(t.get("baslangic")), _as_date(t.get("bitis"))
                if a and b and b >= a:
                    d = (b - a).days + 1
                    per[faz]["days"].append(d)
                    total["days"].append(d)
                    by_size.setdefault(t["tahmin"], []).append(d)

    def unit(bucket):
        return (bucket["cost"] / bucket["done_eff"]) if bucket["done_eff"] else None

    # Ikinci payda, TAHMINDEN BAGIMSIZ: kapanan gorev SAYISI. Birincisi
    # (efor-gunu) S/M/L agirliklarina dayanir ve o agirliklar yazarin
    # secimiydi -- tahmin yanlissa birim maliyet ayni yonde yanlis olur.
    # Ikisini yan yana basmak, tahminin sayiyi ne kadar tasidigini gorunur
    # kilar: ikisi ayni yone gitmiyorsa guvenilecek olan sayidir, agirlik degil.
    def unit_task(bucket):
        return (bucket["cost"] / bucket["done_n"]) if bucket["done_n"] else None

    return dict(has_cost=has_cost, has_dates=has_dates, per=per, total=total,
                by_size=by_size, unit_total=unit(total),
                unit_task_total=unit_task(total),
                unit_per={p: unit(per[p]) for p in phases},
                unit_task_per={p: unit_task(per[p]) for p in phases})


def compute(tasks, cfg, score_rows=None, pair_rows=None):
    W, CR, phases = cfg["effort_weights"], cfg["status_credit"], cfg["phases"]
    epics = {}
    ph = {p: dict(eff=0.0, done=0.0, n=0, dn=0) for p in phases}
    for t in tasks:
        e = W.get(t["tahmin"], 0.0)
        c = CR.get(t["durum"], 0.0)
        ep = epics.setdefault(epic_code(t["epik"]),
                              dict(eff=0.0, done=0.0, n=0, dn=0))
        ep["eff"] += e; ep["done"] += e * c; ep["n"] += 1; ep["dn"] += (1 if c >= 1 else 0)
        if t["faz"] in ph:
            d = ph[t["faz"]]
            d["eff"] += e; d["done"] += e * c; d["n"] += 1; d["dn"] += (1 if c >= 1 else 0)

    total_eff = sum(p["eff"] for p in ph.values())
    epic_eff = sum(e["eff"] for e in epics.values())
    if abs(epic_eff - total_eff) > 1e-9:
        orphan = sorted({t["faz"] for t in tasks if t["faz"] not in ph})
        raise ValueError(
            f"DEGISMEZ IHLALI: epik efor toplami {epic_eff:g} != faz toplami "
            f"{total_eff:g}. Faz sutunu {phases} disinda deger iceriyor: "
            f"{orphan or '?'} — bu gorevler cubukta gorunur ama toplama girmez.")

    # --- ikinci gosterge: tamamlanan eforun ne kadari oz-beyan? -------------
    # Ilerleme yuzdesi "bitti denen is"i olcer, "dogrulanmis is"i degil. Tek
    # gostergeli rapor, gostergenin olcmedigi seyi sifir degil GORUNMEZ yapar.
    # Burada olculen sey mutevazi ve dogru: tamamlanmis eforun ne kadarinin
    # kabul kriterinde YAZARDAN BASKA bir hakem adi var. Kriterin fiilen
    # kosuldugunu iddia ETMEZ — onu bu script bilemez.
    has_col = bool(tasks) and tasks[0].get("_cols", {}).get("hakem", False)
    arb_done = sum(W.get(t["tahmin"], 0.0) * CR.get(t["durum"], 0.0)
                   for t in tasks if str(t.get("hakem", "")).strip())
    arb_n = sum(1 for t in tasks
                if str(t.get("hakem", "")).strip() and CR.get(t["durum"], 0.0) >= 1)
    total_done = sum(p["done"] for p in ph.values())
    total_dn = sum(p["dn"] for p in ph.values())

    pair_per, pair_tot = pair_totals(pair_rows)
    cd = cost_and_duration(tasks, cfg)
    return dict(epics=epics, phases=ph, total_eff=total_eff, cost=cd,
                pair_rows=pair_rows, pair_per=pair_per, pair_tot=pair_tot,
                score_rows=score_rows,
                score_totals=score_totals(score_rows) if score_rows else None,
                arbiter_col=has_col,
                arbiter_done=arb_done, arbiter_dn=arb_n,
                arbiter_pct=(round(100 * arb_done / total_done)
                             if has_col and total_done else None),
                total_done=total_done,
                total_n=sum(p["n"] for p in ph.values()),
                total_dn=total_dn,
                overall_pct=round(100 * total_done / total_eff) if total_eff else 0)


def active_phase(C, cfg):
    for p in cfg["phases"]:
        d = C["phases"][p]
        if d["eff"] and d["done"] < d["eff"] - 1e-9:
            return p
    return None


# ---------------------------------------------------------------- RENDER
def r_chips(C, cfg):
    ap = active_phase(C, cfg)
    nxt = "tamam"
    if ap:
        meta = cfg["phase_meta"].get(ap, {})
        nxt = f"{meta.get('ms', ap)} — {meta.get('title', ap).split('· ')[-1]}"
    return ('<div class="meta">\n'
            f'      <span class="chip"><span class="dot d-todo"></span>Program '
            f'<b>%{C["overall_pct"]}</b> · {C["total_dn"]}/{C["total_n"]} gorev · '
            f'~{fmt(C["total_eff"])} gun</span>\n'
            f'      <span class="chip"><span class="dot '
            f'{"d-prog" if ap else "d-done"}"></span>Siradaki <b>{esc(nxt)}</b></span>\n'
            f'      <span class="chip">git {git_short()}</span>\n'
            f'      <span class="chip">{date.today().isoformat()}</span>\n'
            '    </div>')


def r_kpi(C, cfg):
    ph, phases = C["phases"], cfg["phases"]
    wpm = cfg["workdays_per_month"] or 21
    out = ['<div class="kpis">']
    cum = 0.0
    for p in phases[:-1]:
        cum += ph[p]["eff"]
        out.append(f'      <div class="kpi"><div class="v num">~{fmt(cum)}</div>'
                   f'<div class="l">{esc(p)} sonuna kadar</div>'
                   f'<div class="l2">~{fmt(round(cum / wpm, 1))} ay</div></div>')
    out.append(f'      <div class="kpi"><div class="v num">~{fmt(C["total_eff"])}</div>'
               f'<div class="l">Tum program</div>'
               f'<div class="l2">~{fmt(round(C["total_eff"] / wpm, 1))} ay</div></div>')
    rem = fmt(C["total_eff"] - C["total_done"])
    out.append('      <div class="kpi" style="border-color:color-mix(in srgb,'
               'var(--accent) 40%,var(--line))">'
               f'<div class="v num">{C["overall_pct"]}<small>%</small></div>'
               f'<div class="l">Program geneli (olculen)</div>'
               f'<div class="l2">{C["total_dn"]}/{C["total_n"]} gorev · '
               f'<b>~{rem} gun kalan</b></div></div>')
    out.append('    </div>')
    return "\n".join(out)


def r_cards(C, cfg):
    ap = active_phase(C, cfg)
    out = ['<div class="cards">']
    for p in cfg["phases"]:
        d = C["phases"][p]
        meta = cfg["phase_meta"].get(p, {})
        pct = round(100 * d["done"] / d["eff"]) if d["eff"] else 0
        if pct >= 100:
            edge, badge = "done", '<span class="status s-done">tamam</span>'
        elif p == ap:
            label = f'siradaki ({meta.get("ms", p)})' if pct == 0 else f'devam (%{pct})'
            edge, badge = "prog", f'<span class="status s-prog">{label}</span>'
        else:
            dep = meta.get("dep") or meta.get("ms", p)
            edge, badge = "todo", f'<span class="status s-wait">{esc(dep)} kapisina bagli</span>'
        out.append(
            f'      <div class="card" style="--edge:var(--{edge})">\n'
            f'        <h2>{esc(meta.get("title", p))} {badge}</h2>\n'
            f'        <div class="repo">{esc(meta.get("repo", ""))}</div>\n'
            f'        <p>{esc(meta.get("desc", ""))}</p>\n'
            f'        <div class="row"><span>Ilerleme</span><b class="num">{pct}%</b></div>\n'
            f'        <span class="track" style="height:6px;margin:6px 0 10px">'
            f'<span class="fill" style="width:{pct}%"></span></span>\n'
            f'        <div class="row"><span>Efor</span>'
            f'<b class="num">~{fmt(d["eff"])} gun</b></div>\n'
            f'        <div class="row"><span>Kalan</span>'
            f'<b class="num">~{fmt(d["eff"] - d["done"])} gun</b></div>\n'
            f'        <div class="row"><span>Gorev</span>'
            f'<b class="num">{d["dn"]}/{d["n"]}</b></div>\n'
            f'        <div class="row"><span>Yigin</span>'
            f'<b>{esc(meta.get("stack", "—"))}</b></div>\n'
            f'      </div>')
    out.append('    </div>')
    return "\n".join(out)


def r_bars(C, cfg):
    items = sorted(C["epics"].items(), key=lambda kv: (-kv[1]["eff"], kv[0]))
    max_eff = max((v["eff"] for _, v in items), default=1) or 1
    out = ['<div class="bars">']
    for code, d in items:
        name = cfg["epic_display"].get(code, code)
        pct = round(100 * d["done"] / d["eff"]) if d["eff"] else 0
        out.append(f'      <div class="bar"><span class="name">{esc(name)}</span>'
                   f'<span class="lane"><span class="track" '
                   f'style="width:{round(d["eff"] / max_eff * 100)}%">'
                   f'<span class="fill" style="width:{pct}%"></span></span></span>'
                   f'<span class="pct">{pct}%</span>'
                   f'<span class="ka">{fmt(d["eff"])}</span>'
                   f'<span class="rem">{fmt(d["eff"] - d["done"])} kalan</span></div>')
    out.append(f'      <div class="bar total"><span class="name">Toplam '
               f'({len(items)} epik)</span><span class="lane"></span>'
               f'<span class="pct">{C["overall_pct"]}%</span>'
               f'<span class="ka">{fmt(C["total_eff"])}</span>'
               f'<span class="rem">{fmt(C["total_eff"] - C["total_done"])} kalan</span></div>')
    out.append('    </div>')
    return "\n".join(out)


def r_timeline(C, cfg):
    ap = active_phase(C, cfg)
    out = ['<div class="tl">']
    for s in cfg["static_steps"]:
        out.append(f'      <div class="step ok"><span class="mk">{esc(s.get("mk", "✓"))}</span>'
                   f'<div><div class="t">{esc(s.get("t", ""))}</div>'
                   f'<div class="m">{esc(s.get("m", ""))}</div></div>'
                   f'<span class="when">tamam</span></div>')
    for step in cfg["flow"]:
        p = step.get("phase")
        d = C["phases"].get(p, dict(eff=0, done=0))
        pct = round(100 * d["done"] / d["eff"]) if d["eff"] else 0
        if step.get("kind") == "gate":
            cls, when = ("step gate ok", "acik") if pct >= 100 else ("step gate", "karar")
        elif pct >= 100:
            cls, when = "step ok", "tamam"
        elif pct > 0:
            cls, when = "step on", "devam"
        elif p == ap:
            cls, when = "step on", "siradaki"
        else:
            cls, when = "step", "—"
        out.append(f'      <div class="{cls}"><span class="mk">{esc(step.get("mk", "▸"))}</span>'
                   f'<div><div class="t">{esc(step.get("t", ""))}</div>'
                   f'<div class="m">{esc(step.get("m", ""))}</div></div>'
                   f'<span class="when">{when}</span></div>')
    out.append('    </div>')
    return "\n".join(out)


def r_hakem(C, cfg):
    """Tamamlanan eforun ne kadari disaridan hakemli — ilerlemenin yaninda,
    ILERLEMENIN ICINDE degil. Bu sayiyi yuzdeye katmak, iki ayri seyi
    (bitti / dogrulandi) tek gostergeye eritirdi."""
    if not C["arbiter_col"]:
        return ('<div class="note">\n'
                '      <b>Hakem gostergesi: veri yok.</b> Cizelgede <code>Hakem</code>\n'
                '      sutunu bulunmuyor (eski surum). Bu <em>%0</em> demek degildir —\n'
                '      olculmedi demektir. Cizelgeyi <code>backlog_to_tracker.py</code>\n'
                '      ile yeniden uret.\n'
                '    </div>')
    if C["total_done"] <= 0:
        return ('<div class="note">\n'
                '      <b>Hakem gostergesi: henuz tamamlanan is yok.</b> Oran, ilk\n'
                '      gorev kapandiginda anlam kazanir.\n'
                '    </div>')

    pct = C["arbiter_pct"]
    self_rep = 100 - pct
    return ('<div class="note">\n'
            f'      <div class="row"><span>Tamamlanan eforun hakemli olani</span>'
            f'<b class="num">%{pct}</b></div>\n'
            f'      <span class="track" style="height:6px;margin:6px 0 10px">'
            f'<span class="fill" style="width:{pct}%"></span></span>\n'
            f'      <div class="row"><span>Oz-beyanda kalan</span>'
            f'<b class="num">%{self_rep}</b></div>\n'
            f'      <div class="row"><span>Hakemli kapanan gorev</span>'
            f'<b class="num">{C["arbiter_dn"]}/{C["total_dn"]}</b></div>\n'
            '      <p class="l2">Olculen sey: kabul kriterinde yazardan baska bir\n'
            '      hakem adi gecen gorevlerin, tamamlanan efor icindeki payi.\n'
            '      Kriterin fiilen kosuldugunu <b>gostermez</b> — bunu hicbir\n'
            '      cizelge bilemez; Tamamlandi Tanimi bilir. Dusuk oran, isin\n'
            '      kotu oldugunu degil, "bitti" hukmunun buyuk olcude isi yapanin\n'
            '      kendi beyanina dayandigini soyler.</p>\n'
            '    </div>')


def r_skorkart(C, cfg):
    """Faz kapanis skorkarti -- surecin nereden sizdirdigi, ilerlemenin YANINDA.

    Ilerleme yuzdesi "ne kadari bitti"yi olcer; bu tablo "plan ne kadar
    tutuyordu"yu. Ikisi ayri gostergedir: bir faz %100 kapanip skorkartinda
    dort yeniden-yazilmis kriter tasiyabilir.
    """
    rows = C.get("score_rows")
    if rows is None:
        return ('<div class="note">\n'
                '      <b>Skorkart: olculmedi.</b> Cizelgede <code>Skorkart</code>\n'
                '      sekmesi yok. Bu <em>sifir</em> demek degildir -- tutulmuyor\n'
                '      demektir. Sekmeyi <code>backlog_to_tracker.py</code> ile\n'
                '      uret, kapida elle doldur.\n'
                '    </div>')
    if not rows:
        return ('<div class="note">\n'
                '      <b>Skorkart: henuz kapanmis faz yok.</b> Tablo ilk kapida\n'
                '      anlam kazanir; faz acilirken doldurulmaz.\n'
                '    </div>')

    T = C["score_totals"]

    def cell(key):
        total, n = T[key]
        if total is None:
            return '<span class="l2">olculmedi</span>'
        suffix = "" if n == len(rows) else f' <span class="l2">({n}/{len(rows)} faz)</span>'
        return f'<b class="num">{total}</b>{suffix}'

    lines = [
        ("Faz acildiktan sonraki backlog revizyonu", "revizyon",
         "Yuksek: faz, girdileri hazir olmadan acildi."),
        ("Yeniden calisma turu", "tur",
         "Tek epikte topluyorsa supheyi kiside degil bolunmede ara."),
        ("Isten sonra yeniden yazilan kriter", "kriter",
         "Her biri, onkayit olmaktan cikmis bir kriterdir."),
        ("Faz disina cikma", "kapsam",
         "Kapsam disi listesinin neyi tutmadigi."),
        ("Kacan", "kacan",
         "Kapidan sonra bulunan, bu fazin kriterlerinin kapsadigi hata. "
         "Surec disindan gelen tek sayi."),
    ]
    body = "".join(
        f'      <div class="row"><span>{lab}</span>{cell(key)}</div>\n'
        f'      <p class="l2">{note}</p>\n'
        for lab, key, note in lines)

    ikiz, _ = T["ikiz"]
    kapida, _ = T["ikiz_kapida"]
    if ikiz is None or kapida is None:
        ratio = ('      <div class="row"><span>Tuketen-ikiz boslugu</span>'
                 '<span class="l2">olculmedi</span></div>\n')
    elif ikiz == 0:
        ratio = ('      <div class="row"><span>Tuketen-ikiz boslugu</span>'
                 '<b class="num">0</b></div>\n'
                 '      <p class="l2">Sifir, taramanin temiz oldugunu degil, bu\n'
                 '      fazda hic bulunmadigini soyler.</p>\n')
    else:
        pct = round(100 * kapida / ikiz)
        ratio = (f'      <div class="row"><span>Tuketen-ikiz boslugu: kapida bulunan</span>'
                 f'<b class="num">{kapida}/{ikiz} (%{pct})</b></div>\n'
                 f'      <p class="l2">Asil sayi bu: kapida degil <em>tesadufen</em>\n'
                 f'      bulunanlar, kapinin o bosluga bakmadigini gosterir.</p>\n')

    prov, _ = T["senaryo"]
    tes, _ = T["senaryo_tesadufi"]
    if prov is None or tes is None:
        senaryo = ('      <div class="row"><span>Senaryo bulgusu: provali / tesadufi</span>'
                   '<span class="l2">olculmedi</span></div>\n')
    else:
        senaryo = (f'      <div class="row"><span>Senaryo bulgusu: provali / tesadufi</span>'
                   f'<b class="num">{prov} / {tes}</b></div>\n'
                   '      <p class="l2">Hic bulgu vermeyen bir prova listesi temiz\n'
                   '      proje degil, calistirilmamis listedir.</p>\n')

    kodlar = sorted({k for row in rows
                     for k in re.findall(r"RR-\d{2}", row.get("rampa", ""))})
    ramp = (f'      <div class="row"><span>Kullanilan rampalar</span>'
            f'<b class="num">{esc(", ".join(kodlar))}</b></div>\n'
            if kodlar else
            '      <div class="row"><span>Kullanilan rampalar</span>'
            '<span class="l2">yok</span></div>\n'
            '      <p class="l2">Hicbiri kullanilmadiysa ya kusursuz gecti ya\n'
            '      da fark edilmedi.</p>\n')

    # Kacan, cizelgenin surec DISINDAN gelen tek sayisi. Sayinin yaninda sinif
    # yoksa dongu kapanmamistir: hata cikti, duzeltme girdi, bir sonraki
    # kapinin neye baktigi degismedi. Rapor bunu ayri basar, cunku "3 kacan"
    # ile "3 kacan, hicbiri siniflanmamis" ayni cizelge degildir (RR-13).
    kc, _ = T["kacan"]
    sinif = " ".join(r.get("kacan_sinifi", "") for r in rows).strip()
    if kc is None:
        kacan_blok = ('      <div class="row"><span>Kacan</span>'
                      '<span class="l2">olculmedi</span></div>\n')
    elif kc == 0:
        kacan_blok = ('      <div class="row"><span>Kacan</span>'
                      '<b class="num">0</b></div>\n'
                      '      <p class="l2">Sifir, kapinin siki oldugunu degil, bu\n'
                      '      fazdan sonra hic bulunmadigini soyler.</p>\n')
    elif sinif:
        kacan_blok = (f'      <div class="row"><span>Kacan / siniflanmis</span>'
                      f'<b class="num">{kc} / var</b></div>\n'
                      f'      <p class="l2">{esc(sinif)}</p>\n')
    else:
        kacan_blok = (f'      <div class="row"><span>Kacan / siniflanmis</span>'
                      f'<b class="num">{kc} / yok</b></div>\n'
                      '      <p class="l2">Sinifsiz kacak: hangi kontrolun bunu\n'
                      '      yakalamasi gerektigi yazilmamis. RR-13 tam olarak bu\n'
                      '      hucre icin var -- sayi, dongu degildir.</p>\n')

    return ('<div class="note">\n'
            f'      <div class="row"><span>Kapanmis faz</span>'
            f'<b class="num">{esc(", ".join(r["faz"] for r in rows))}</b></div>\n'
            + body + ratio + senaryo + ramp + kacan_blok +
            '      <p class="l2"><b>Bu tablodaki her sayi oz-beyandir</b> -- isi\n'
            '      yapan doldurur, hakem = yazar. Olctugu sey ekibin performansi\n'
            '      degil, planin nerede sizdirdigi: yuksek sayi kotu degildir,\n'
            '      gizlenen sayi kotudur.</p>\n'
            '    </div>')


def r_cift(C, cfg):
    """GEN:CIFT -- yeniden birlestirme pasinin sonucu.

    Ilerleme yuzdesi "bitti denen is"i olcer. Bu bolge baska bir seyi olcer:
    parcalara ayrilmis isin YENIDEN BIRLESTIRILIP birlestirilmedigini. Bir faz
    %100 kapanip tek cift bakilmamis olabilir, ve bu bir celiski degil bilgidir
    -- kusur zaten parcalarin arasinda yasar.
    """
    rows = C.get("pair_rows")
    if rows is None:
        return ('<div class="note">\n'
                '      <div class="row"><span>Cift pasi</span>'
                '<span class="l2">olculmedi (&quot;Cift&quot; sekmesi yok)</span></div>\n'
                '      <p class="l2">Sifir cift DEGIL: bu proje pasi tutmuyor.\n'
                '      Sekmeyi backlog_to_tracker.py uretir.</p>\n'
                '    </div>')
    if not rows:
        return ('<div class="note">\n'
                '      <div class="row"><span>Cift pasi</span>'
                '<span class="l2">sekme var, hic cift yazilmamis</span></div>\n'
                '      <p class="l2">Backlog\'i atomize etmek, yalnizca iki\n'
                '      ozellik ayni anda etkinken var olan kusuru yok eder. Bos\n'
                '      bir liste, temiz bir model degil kosulmamis bir pastir.</p>\n'
                '    </div>')

    per, tot = C["pair_per"], C["pair_tot"]
    satirlar = "".join(
        f'      <div class="row"><span>{esc(faz)}</span>'
        f'<b class="num">{d["n"]} cift · {d["kirik"]} kirik'
        + (f' · {d["bakilmadi"]} bakilmadi' if d["bakilmadi"] else '')
        + '</b></div>\n'
        for faz, d in ((p, per[p]) for p in cfg["phases"] if p in per))

    kirik_satir = "".join(
        f'      <p class="l2"><b>{esc(r["faz"])} · {esc(r["ozellik"])}</b> × '
        f'{esc(r["garanti"])}'
        + (f' — sira: {esc(r["gerekli_sira"])}' if r["gerekli_sira"] else '')
        + f'<br>{esc(r["not_"])}</p>\n'
        for r in rows if r["sonuc"] == "kiriliyor")

    if tot["bakilmadi"]:
        acik = (f'      <p class="l2"><b>{tot["bakilmadi"]} cift listelendi ve\n'
                f'      sinanmadi.</b> Bu sifir degil, acik istir: listelenmis ama\n'
                f'      bakilmamis cift, hic listelenmemis cift kadar korur.</p>\n')
    else:
        acik = ''

    return ('<div class="note">\n'
            f'      <div class="row"><span>Cift pasi</span>'
            f'<b class="num">{tot["n"]} cift · {tot["kirik"]} kirik</b></div>\n'
            + satirlar + acik + kirik_satir +
            '      <p class="l2">Her satir elle yazilir: hangi mevcut garantiye\n'
            '      dokunuldugunu backlog\'dan uretmek mumkun degil, modeli bilen\n'
            '      insan bilir. Yesil test paketi burada karsi kanit degildir --\n'
            '      testler ozellik basina yazilir, cift hakkinda susar.</p>\n'
            '    </div>')


def r_maliyet(C, cfg):
    """GEN:MALIYET -- birim maliyet ve gecen sure.

    Bu bolge ROI HESAPLAMAZ ve hesapladigini soylemez. ROI'nin iki terimi var;
    burada olculen yalnizca biri:

      PAYDA  maliyet / tamamlanan efor-gunu. Elle yazilan Maliyet sutunundan
             gelir, birimi projeye aittir, ve bu script birimi yorumlamaz.
      PAY    projenin kendi deger metrigi -- kapanan ticket, cevrim suresi,
             kacan kusur orani. Bu script onu BILMEZ.

    Faz faz basilir, cunku bilgi seviyede degil EGIMDEDIR: her faz bir sonraki
    icin ic karsilastirma kolu olur. "Aracsiz ne olurdu" karsi-olgusunun yerini
    tutmaz -- ama o kol cogu ekipte hic kurulamaz, bu ise elde vardir.
    """
    cd = C["cost"]
    parts = []

    if not cd["has_cost"]:
        parts.append('      <div class="row"><span>Birim maliyet</span>'
                     '<span class="l2">olculmedi (cizelgede &quot;Maliyet&quot; '
                     'sutunu yok)</span></div>\n'
                     '      <p class="l2">%0 DEGIL. Oturum toplamini '
                     'tools/session_cost.py olcer; hangi goreve yazilacagi '
                     'atiftir.</p>\n')
    elif cd["total"]["cost_n"] == 0:
        parts.append('      <div class="row"><span>Birim maliyet</span>'
                     '<span class="l2">sutun var, hic deger yazilmamis</span></div>\n')
    else:
        u, ut = cd["unit_total"], cd["unit_task_total"]
        parts.append(f'      <div class="row"><span>Birim maliyet '
                     f'(maliyet / tamamlanan <b>tahmini</b> efor-gunu)</span>'
                     f'<b class="num">{fmt(u) if u else "—"}</b></div>\n')
        parts.append(f'      <div class="row"><span>...ve tahminden bagimsiz: '
                     f'maliyet / kapanan gorev</span>'
                     f'<b class="num">{fmt(ut) if ut else "—"}</b></div>\n')
        parts.append(f'      <p class="l2">{cd["total"]["cost_n"]} gorevde '
                     f'maliyet yazili · toplam {fmt(cd["total"]["cost"])} · '
                     f'tamamlanan {cd["total"]["done_n"]} gorev / '
                     f'{fmt(cd["total"]["done_eff"])} tahmini efor-gunu. '
                     f'Birim projeye aittir; rapor orani hesaplar, tutari '
                     f'yorumlamaz.</p>\n')
        parts.append('      <p class="l2"><b>Ilk paydanin dayanagi bir '
                     'TAHMINDIR.</b> Efor-gunu S/M/L agirliklarindan gelir ve o '
                     'agirliklar yazarin secimiydi — tahmin yanlissa birim '
                     'maliyet ayni yonde yanlis olur. Ikinci satir bu yuzden var: '
                     'kapanan gorev SAYISI tahminden bagimsizdir. Ikisi ayni yone '
                     'gitmiyorsa agirliga degil sayiya guven, ve asagidaki '
                     'gecen-sure kalibrasyonuna bak.</p>\n')
        rows = [(p, cd["unit_per"][p]) for p in cfg["phases"]
                if cd["unit_per"].get(p) is not None]
        if len(rows) >= 2:
            parts.append('      <div class="row"><span>Faz faz birim maliyet '
                         '(efor-gunu / gorev)</span>'
                         '<b class="num">'
                         + ' · '.join(
                             f'{esc(p)} {fmt(v)}'
                             + (f' / {fmt(cd["unit_task_per"][p])}'
                                if cd["unit_task_per"].get(p) else '')
                             for p, v in rows)
                         + '</b></div>\n')
            first, last = rows[0][1], rows[-1][1]
            if first:
                trend = round(100 * (last - first) / first)
                yon = "dusuyor" if trend < 0 else ("artiyor" if trend > 0 else "sabit")
                parts.append(f'      <p class="l2">Egim: ilk fazdan sona '
                             f'%{abs(trend)} {yon}. <b>Asil bilgi budur</b> — her faz '
                             f'bir sonrakinin ic karsilastirma koludur. Bu, '
                             f'&quot;aracsiz ne olurdu&quot; karsi-olgusunun yerini '
                             f'TUTMAZ.</p>\n')

    if not cd["has_dates"]:
        parts.append('      <div class="row"><span>Gecen sure</span>'
                     '<span class="l2">olculmedi (Baslangic/Bitis bos ya da yok)'
                     '</span></div>\n')
    elif not cd["total"]["days"]:
        parts.append('      <div class="row"><span>Gecen sure</span>'
                     '<span class="l2">tarihli tamamlanmis gorev yok</span></div>\n')
    else:
        days = sorted(cd["total"]["days"])
        med = days[len(days) // 2]
        parts.append(f'      <div class="row"><span>Gecen sure (medyan)</span>'
                     f'<b class="num">{med} gun · {len(days)} gorev</b></div>\n')
        if cd["by_size"]:
            per_size = ' · '.join(
                f'{esc(k)} {sorted(v)[len(v)//2]}g'
                for k, v in sorted(cd["by_size"].items()) if v)
            parts.append(f'      <div class="row"><span>Tahmine gore medyan '
                         f'gecen sure</span><b class="num">{per_size}</b></div>\n')
            parts.append('      <p class="l2">Tahmin kalibrasyonu: S/M/L '
                         'agirliklari yazarin secimiydi, bu ilk gercek veridir '
                         '(RR-12). <b>Gecen sure EFOR DEGILDIR</b> — 5 gun acik '
                         'duran gorev 2 saatlik is olabilir; olculen sey gorevin '
                         'ne kadar ACIK KALDIGIDIR.</p>\n')

    return ('<div class="note">\n' + "".join(parts) +
            '      <p class="l2"><b>Bu bolge ROI degildir.</b> ROI\'nin paydasi '
            'burada; payi projenin kendi deger metriginde. Ve "arac %X '
            'kazandirdi" cumlesi icin ucuncu bir sey gerekir: karsi-olgu. O kol '
            'olmadan atif [KKE]\'dir.</p>\n'
            '    </div>')


RENDERERS = dict(CHIPS=r_chips, KPI=r_kpi, CARDS=r_cards,
                 BARS=r_bars, TIMELINE=r_timeline, HAKEM=r_hakem,
                 SKORKART=r_skorkart, CIFT=r_cift,
                 MALIYET=r_maliyet)


def patch(html, key, block):
    pat = re.compile(r'(<!-- GEN:%s:BEGIN[^>]*-->\n    ).*?(\n<!-- GEN:%s:END -->)'
                     % (key, key), re.S)
    if not pat.search(html):
        return html, False
    return pat.sub(lambda m: m.group(1) + block + m.group(2), html), True


# ---------------------------------------------------------------- SELF-TEST
def self_test():
    """Gomulu regresyon: mutlu yol + uc sessiz-hata vakasi."""
    from openpyxl import Workbook
    cfg = dict(DEFAULTS, phases=["F0", "F1"])
    tmp = Path(tempfile.mkdtemp())
    ok = True

    def make(rows):
        wb = Workbook(); ws = wb.active; ws.title = "Takip"
        ws.append(["ID", "Faz", "Epik", "Tahmin", "Durum"])
        for r in rows:
            ws.append(r)
        p = tmp / "t.xlsx"; wb.save(p); return p

    def check(label, cond):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    # 1) mutlu yol: S+L tamam, M yapilacak -> (0.75+4)/(0.75+4+1.5)=76%
    t, iss = load_tasks(make([
        ["A-1", "F0", "F0.1 Bir", "S", "Tamamlandi"],
        ["A-2", "F0", "F0.1 Bir", "L", "Tamamlandi"],
        ["B-1", "F1", "F1.1 Iki", "M", "Yapilacak"]]), cfg)
    C = compute(t, cfg)
    check("mutlu yol: hata yok", not [m for l, m in iss if l == "ERROR"])
    check("efor toplami 6.25", abs(C["total_eff"] - 6.25) < 1e-9)
    check("ilerleme %76", C["overall_pct"] == 76)
    check("aktif faz F1", active_phase(C, cfg) == "F1")

    # 2) gecersiz tahmin -> ERROR (sessizce M olmaz)
    _, iss = load_tasks(make([["A-1", "F0", "F0.1 Bir", "XL", "Yapilacak"]]), cfg)
    check("gecersiz Tahmin ERROR uretir",
          any(l == "ERROR" and "Tahmin" in m for l, m in iss))

    # 3) Turkce-i 'Tamamlandı' -> normalize + kredi alir
    t, iss = load_tasks(make([["A-1", "F0", "F0.1 Bir", "M", "Tamamlandı"]]), cfg)
    C = compute(t, cfg)
    check("Turkce-i Durum normalize edilir",
          any(l == "WARN" and "normalize" in m for l, m in iss))
    check("Turkce-i Durum kredi alir (%100)", C["overall_pct"] == 100)

    # 4) faz listesi disi -> degismez ihlali
    t, iss = load_tasks(make([
        ["A-1", "F0", "F0.1 Bir", "M", "Yapilacak"],
        ["Z-1", "F9", "F9.9 Hayalet", "L", "Tamamlandi"]]), cfg)
    try:
        compute(t, cfg)
        check("faz disi kayit degismez ihlali uretir", False)
    except ValueError:
        check("faz disi kayit degismez ihlali uretir", True)

    # 5) Hakem sutunu YOKSA gosterge %0 degil "olculmedi" olmali
    t, _ = load_tasks(make([["A-1", "F0", "F0.1 Bir", "M", "Tamamlandi"]]), cfg)
    C = compute(t, cfg)
    check("Hakem sutunu yoksa gosterge None (0 degil)",
          C["arbiter_col"] is False and C["arbiter_pct"] is None)

    # 6) Hakem sutunu varsa oran TAMAMLANAN efor uzerinden hesaplanir.
    #    L(4) hakemli tamam + S(0.75) hakemsiz tamam + M(1.5) hakemli ama
    #    yapilacak -> 4/4.75 = %84. Bitmemis is orana girmemeli: girseydi
    #    "hakem yazdim" demek, dogrulanmis is gibi gorunurdu.
    def make_h(rows):
        wb = Workbook(); ws = wb.active; ws.title = "Takip"
        ws.append(["ID", "Faz", "Epik", "Tahmin", "Durum", "Hakem"])
        for r in rows:
            ws.append(r)
        p = tmp / "th.xlsx"; wb.save(p); return p

    t, _ = load_tasks(make_h([
        ["A-1", "F0", "F0.1 Bir", "L", "Tamamlandi", "pytest tests/a.py"],
        ["A-2", "F0", "F0.1 Bir", "S", "Tamamlandi", ""],
        ["B-1", "F1", "F1.1 Iki", "M", "Yapilacak", "pytest tests/b.py"]]), cfg)
    C = compute(t, cfg)
    check("hakemli oran tamamlanan efor uzerinden (%84)", C["arbiter_pct"] == 84)
    check("hakemli kapanan gorev sayisi 1", C["arbiter_dn"] == 1)
    check("hakem orani ilerleme yuzdesini degistirmez", C["overall_pct"] == 76)

    # ---- Skorkart: opsiyonel sekme, elle doldurulur, her sayisi oz-beyan ----
    def make_s(score_rows, headers=None):
        """Takip + (varsa) Skorkart. headers=None -> hic Skorkart sekmesi yok."""
        wb = Workbook(); ws = wb.active; ws.title = "Takip"
        ws.append(["ID", "Faz", "Epik", "Tahmin", "Durum"])
        ws.append(["A-1", "F0", "F0.1 Bir", "M", "Tamamlandi"])
        if headers is not None:
            wk = wb.create_sheet("Skorkart")
            wk.append(headers)
            for r in score_rows:
                wk.append(r)
        p = tmp / "ts.xlsx"; wb.save(p); return p

    SH = [SCORE_COL[k] for k in ("faz", "revizyon", "tur", "kriter", "ikiz",
                                 "ikiz_kapida", "senaryo", "senaryo_tesadufi",
                                 "kapsam", "rampa", "kacan", "cikarim")]

    # 7) Sekme YOKSA gosterge sifir degil "olculmedi" olmali. Bu, Hakem
    #    sutunuyla ayni kirmizi cizgi: olculmemis seyi sifir basmak, olcum
    #    gibi gorunur ve en pahali sessiz varsayimdir.
    rows, iss = load_scorecard(make_s([], headers=None), cfg)
    check("Skorkart sekmesi yoksa None (bos liste degil)", rows is None)
    check("Skorkart sekmesi yoksa hata da uretmez", not iss)

    # 8) Faz sutunu onceden yazili ama hicbir alan dolu degil -> KAPANMAMIS.
    #    Satir sayilsaydi rapor, acilmamis fazlari "olculdu, hepsi bos" diye
    #    basardi.
    rows, iss = load_scorecard(
        make_s([["F0"] + [None] * 11, ["F1"] + [None] * 11], headers=SH), cfg)
    check("doldurulmamis satir kapanmis faz sayilmaz", rows == [])

    # 9) Mutlu yol: bir faz dolu, toplamlar ve doldurulmus-alan sayaci.
    rows, iss = load_scorecard(
        make_s([["F0", 2, 3, 1, 4, 1, 2, 5, 1, "RR-03, RR-06", 1, "Not"],
                ["F1"] + [None] * 11], headers=SH), cfg)
    T = score_totals(rows)
    check("dolu faz sayisi 1", len(rows) == 1)
    check("yeniden tur toplami 3", T["tur"] == (3, 1))
    check("skorkart hatasiz okunur", not [m for l, m in iss if l == "ERROR"])

    # 10) IkizKapida > IkizBoslugu -> ERROR. Bu yalnizca yazim hatasi degil:
    #     "kapida yakalandi" orani 1'i asar ve tablo iyi haber gibi okunur.
    rows, iss = load_scorecard(
        make_s([["F0", 0, 0, 0, 2, 9, 0, 0, 0, "", 0, ""]], headers=SH), cfg)
    check("IkizKapida > IkizBoslugu ERROR uretir",
          any(l == "ERROR" and "IkizKapida" in m for l, m in iss))

    # 11) Faz listesi disi satir -> ERROR (Takip sekmesindeki degismezle ayni).
    rows, iss = load_scorecard(
        make_s([["F9", 1, 1, 1, 1, 1, 1, 1, 1, "", 1, ""]], headers=SH), cfg)
    check("faz listesi disi skorkart satiri ERROR uretir",
          any(l == "ERROR" and "F9" in m for l, m in iss))

    # 12) Sayi olmayan deger -> ERROR (sessizce 0 sayilmaz).
    rows, iss = load_scorecard(
        make_s([["F0", "cok", 1, 1, 1, 1, 1, 1, 1, "", 1, ""]], headers=SH), cfg)
    check("sayi olmayan skorkart degeri ERROR uretir",
          any(l == "ERROR" and "sayi degil" in m for l, m in iss))

    # 13) Skorkart ilerleme yuzdesine DOKUNMAZ. Iki gosterge ayri kalmali:
    #     bir faz %100 kapanip skorkartinda dort yeniden-yazilmis kriter
    #     tasiyabilir, ve bu bir celiski degil bilgidir.
    t, _ = load_tasks(make_s([], headers=None), cfg)
    rows, _ = load_scorecard(
        make_s([["F0", 9, 9, 9, 9, 9, 9, 9, 9, "RR-02", 9, ""]], headers=SH), cfg)
    check("skorkart ilerleme yuzdesini degistirmez",
          compute(t, cfg, rows)["overall_pct"] == compute(t, cfg)["overall_pct"])

    # 14) KacanSinifi OPSIYONELDIR: sutunu olmayan eski bir cizelge hatasiz
    #     okunur. Zorunlu olsaydi her mevcut kit yukseltmede kirilirdi -- ve
    #     kirilan bir kural, ogrenilecek bir kural degil atlanacak bir kuraldir.
    rows, iss = load_scorecard(
        make_s([["F0", 1, 1, 1, 1, 1, 1, 1, 1, "", 2, "Not"]], headers=SH), cfg)
    check("KacanSinifi sutunu yoksa skorkart yine okunur",
          len(rows) == 1 and not [m for l, m in iss if l == "ERROR"])
    check("sutun yoksa sinif bos string", rows[0]["kacan_sinifi"] == "")

    # 15) Sayi var, sinif yok -> rapor bunu AYRI basar. "3 kacan" ile "3 kacan,
    #     hicbiri siniflanmamis" ayni cizelge degildir: ilki bir olcum, ikincisi
    #     kapanmamis bir dongudur (RR-13).
    SH2 = SH[:-1] + [SCORE_COL_OPT["kacan_sinifi"], SH[-1]]
    rows, _ = load_scorecard(
        make_s([["F0", 0, 0, 0, 0, 0, 0, 0, 0, "", 2, "", "Not"]], headers=SH2), cfg)
    html = r_skorkart(compute(load_tasks(make_s([], headers=None), cfg)[0],
                              cfg, rows), cfg)
    check("sinifsiz kacak raporda isaretlenir", "Sinifsiz kacak" in html)

    # 16) ...ve sinif yazilmissa metni basilir, uyari degil.
    rows, _ = load_scorecard(
        make_s([["F0", 0, 0, 0, 0, 0, 0, 0, 0, "", 2, "DoD: okuma yuzeyi", "Not"]],
               headers=SH2), cfg)
    html = r_skorkart(compute(load_tasks(make_s([], headers=None), cfg)[0],
                              cfg, rows), cfg)
    check("siniflanmis kacak metniyle basilir",
          "DoD: okuma yuzeyi" in html and "Sinifsiz kacak" not in html)

    # ---- Cift sekmesi: yeniden birlestirme pasinin kaydi -------------------
    PH = [PAIR_COL[k] for k in ("faz", "ozellik", "garanti", "sira",
                                "gerekli_sira", "sonuc", "not_")]

    def make_p(rows, headers=PH):
        wb = Workbook(); ws = wb.active; ws.title = "Takip"
        ws.append(["ID", "Epik", "Faz", "Katman", "Tahmin", "Durum"])
        if headers is not None:
            wc = wb.create_sheet(PAIR_SHEET); wc.append(headers)
            for r in rows:
                wc.append(r)
        p = tmp / "tp.xlsx"; wb.save(p); return p

    # 17) Sekme YOKSA gosterge sifir degil "olculmedi". Skorkart ile ayni
    #     kirmizi cizgi: kosulmamis bir pasi "0 kirik cift" diye basmak, en
    #     pahali sessiz varsayimdir -- rapor temiz gorunur.
    rows, iss = load_pairs(make_p([], headers=None), cfg)
    check("Cift sekmesi yoksa None (bos liste degil)", rows is None)
    check("Cift sekmesi yoksa hata da uretmez", not iss)
    html = r_cift(compute(load_tasks(make_p([], headers=None), cfg)[0], cfg,
                          None, None), cfg)
    check("sekme yoksa rapor 'olculmedi' basar", "olculmedi" in html)

    # 18) Faz sutunu onceden yazilidir: hicbir alani dolu olmayan satir
    #     kaydedilmis bir cift degildir.
    rows, iss = load_pairs(make_p([["F0", None, None, None, None, None, None]]), cfg)
    check("bos cift satiri kaydedilmis sayilmaz", rows == [])

    # 19) Bir cift, OZELLIK ve dokundugu GARANTI ile tanimlanir; tek basina
    #     ozellik, ozellik incelemesidir -- pasin tamami budur.
    rows, iss = load_pairs(make_p([["F0", "duraklatma", "", "", "", "tutuyor", ""]]), cfg)
    check("garantisiz cift ERROR uretir",
          any(l == "ERROR" and "GARANTI" in m for l, m in iss))

    # 20) Sonuc sozlugu kapali: "belki" bir sonuc degildir.
    rows, iss = load_pairs(make_p([["F0", "duraklatma", "bayatlama bayragi",
                                    "", "", "belki", ""]]), cfg)
    check("gecersiz Sonuc ERROR uretir",
          any(l == "ERROR" and "Sonuc" in m for l, m in iss))

    # 21) Sira duyarli cift, guvenli yonu tasimazsa bulgunun yarisi eksiktir.
    rows, iss = load_pairs(make_p([["F0", "anonimlestirme", "yeniden atama",
                                    "evet", "", "kiriliyor", "n"]]), cfg)
    check("SiraOnemli ama GerekliSira bos -> ERROR",
          any(l == "ERROR" and "GerekliSira" in m for l, m in iss))

    # 22) Kirilan cift, ne oldugunu soylemeden devredilemez.
    rows, iss = load_pairs(make_p([["F0", "duraklatma", "bayatlama bayragi",
                                    "", "", "kiriliyor", ""]]), cfg)
    check("notsuz 'kiriliyor' ERROR uretir",
          any(l == "ERROR" and "Not bos" in m for l, m in iss))

    # 23) Mutlu yol: sayilar ve raporun ayri bastigi iki sey -- kirik cift ve
    #     LISTELENIP BAKILMAMIS cift. Ikincisi sifir degil acik istir.
    rows, iss = load_pairs(make_p([
        ["F0", "duraklatma", "bayatlama bayragi", "", "", "kiriliyor",
         "Duraklatma, tikanmis isi saklamanin ucuz yolu olur; bayrak gurultuden olur."],
        ["F0", "toplu disa aktarim", "not bazinda gizlilik", "", "", "tutuyor", ""],
        ["F1", "anonimlestirme", "acik islerin yeniden atanmasi", "evet",
         "once yeniden ata, sonra anonimlestir", "bakilmadi", ""],
    ]), cfg)
    check("cift satirlari hatasiz okunur", not [m for l, m in iss if l == "ERROR"])
    per, tot = pair_totals(rows)
    check("cift toplami 3", tot["n"] == 3)
    check("kirik cift 1", tot["kirik"] == 1)
    check("bakilmamis cift 1", tot["bakilmadi"] == 1)
    C = compute(load_tasks(make_s([], headers=None), cfg)[0], cfg, None, rows)
    html = r_cift(C, cfg)
    check("kirik cift raporda metniyle gorunur", "gurultuden olur" in html)
    check("bakilmamis cift ayri basilir", "sinanmadi" in html)

    # 24) Cift pasi ilerleme yuzdesine DOKUNMAZ. Iki gosterge ayri kalmali: bir
    #     faz %100 kapanip tek cift bakilmamis olabilir, ve bu bir celiski
    #     degil bilgidir -- kusur zaten parcalarin arasinda yasar.
    t, _ = load_tasks(make_s([], headers=None), cfg)
    check("cift pasi ilerleme yuzdesini degistirmez",
          compute(t, cfg, None, rows)["overall_pct"] == compute(t, cfg)["overall_pct"])

    # ---- Maliyet ve gecen sure ---------------------------------------------
    import datetime as _dt
    TH = ["ID", "Epik", "Faz", "Katman", "Tahmin", "Durum", "Maliyet",
          "Baslangic", "Bitis"]

    def make_c(rows, headers=TH):
        wb = Workbook(); ws = wb.active; ws.title = "Takip"
        ws.append(headers)
        for r in rows:
            ws.append(r)
        p = tmp / "tc.xlsx"; wb.save(p); return p

    # 25) Sutun YOKSA gosterge %0 degil "olculmedi". Hakem sutunuyla ayni
    #     kirmizi cizgi: olculmemis maliyeti sifir basmak, en pahali sessiz
    #     varsayimdir -- proje bedava gorunur.
    t, _ = load_tasks(make_c([["F0-BE-01", "E1", "F0", "BE", "M", "Tamamlandi"]],
                             headers=TH[:6]), cfg)
    C = compute(t, cfg)
    check("Maliyet sutunu yoksa has_cost False", C["cost"]["has_cost"] is False)
    check("sutun yoksa rapor 'olculmedi' basar", "olculmedi" in r_maliyet(C, cfg))

    # 26) Sutun var, deger yok: yine sifir degil. Bos hucre ile 0 arasindaki
    #     fark, bu dosyadaki her gostergenin uzerine kuruldugu ayrimdir.
    t, _ = load_tasks(make_c([["F0-BE-01", "E1", "F0", "BE", "M", "Tamamlandi",
                               "", "", ""]]), cfg)
    C = compute(t, cfg)
    check("deger yazilmamissa cost_n 0", C["cost"]["total"]["cost_n"] == 0)

    # 27) Birim maliyet = maliyet / TAMAMLANAN efor-gunu. Tamamlanmamis isin
    #     maliyeti paya girer (harcandi), efora girmez (teslim edilmedi) --
    #     tersi, biten isi ucuz gosteren bir bolme olurdu.
    t, _ = load_tasks(make_c([
        ["F0-BE-01", "E1", "F0", "BE", "M", "Tamamlandi", "3000", "", ""],
        ["F0-BE-02", "E1", "F0", "BE", "M", "Devam", "1000", "", ""],
    ]), cfg)
    C = compute(t, cfg)
    # M = 1.5 efor-gunu, tamamlanan tek gorev; toplam maliyet 4000
    check("birim maliyet tamamlanan efora bolunur",
          abs(C["cost"]["unit_total"] - (4000 / 1.5)) < 1e-6)
    # ...ve tahminden bagimsiz ikinci payda: kapanan gorev SAYISI. Ilk payda
    # S/M/L agirliklarina dayanir; agirlik yanlissa birim maliyet ayni yonde
    # yanlis olur, ve bunu gorunur kilan tek sey ikinci sayidir.
    check("gorev basina maliyet tahminden bagimsiz",
          abs(C["cost"]["unit_task_total"] - (4000 / 1)) < 1e-6)
    check("rapor paydanin tahmin oldugunu soyler",
          "TAHMINDIR" in r_maliyet(C, cfg))

    # 28) Gecen sure yalnizca tamamlanmis ve TARIHLI gorevlerden; ve efor diye
    #     adlandirilmaz. Rapor metni bunu her seferinde soyler.
    t, _ = load_tasks(make_c([
        ["F0-BE-01", "E1", "F0", "BE", "S", "Tamamlandi", "100",
         _dt.date(2026, 9, 1), _dt.date(2026, 9, 3)],
        ["F0-BE-02", "E1", "F0", "BE", "S", "Devam", "100",
         _dt.date(2026, 9, 1), _dt.date(2026, 9, 9)],
    ]), cfg)
    C = compute(t, cfg)
    check("gecen sure yalniz tamamlanmis gorevden", C["cost"]["total"]["days"] == [3])
    check("rapor 'EFOR DEGILDIR' der", "EFOR DEGILDIR" in r_maliyet(C, cfg))

    # 29) Faz faz egim: asil bilgi seviyede degil YONDE. Her faz bir sonrakinin
    #     ic karsilastirma koludur -- karsi-olgunun yerini tutmaz, ve rapor
    #     tuttugunu iddia etmez.
    t, _ = load_tasks(make_c([
        ["F0-BE-01", "E1", "F0", "BE", "M", "Tamamlandi", "3000", "", ""],
        ["F1-BE-01", "E1", "F1", "BE", "M", "Tamamlandi", "1500", "", ""],
    ]), cfg)
    C = compute(t, cfg)
    html = r_maliyet(C, cfg)
    check("faz faz birim maliyet basilir", "Faz faz birim maliyet" in html)
    check("egim yonuyle birlikte basilir", "dusuyor" in html)
    check("karsi-olgu uyarisi her zaman var", "TUTMAZ" in html and "[KKE]" in html)

    # 30) Maliyet ilerleme yuzdesine DOKUNMAZ. Ucuncu gosterge de digerleri gibi
    #     ayri kalir: %100 kapanmis bir faz pahali olabilir ve bu celiski degil
    #     bilgidir.
    check("maliyet ilerleme yuzdesini degistirmez",
          compute(t, cfg)["overall_pct"] == compute(t, cfg, None, None)["overall_pct"])

    print("SELF-TEST:", "BASARILI" if ok else "BASARISIZ")
    return 0 if ok else 1


# ---------------------------------------------------------------- MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", default="tracker.xlsx")
    ap.add_argument("--html", default="07-ilerleme-raporu.html")
    ap.add_argument("--config", default="iskele.config.json")
    ap.add_argument("--check", action="store_true", help="yazma, ozet bas")
    ap.add_argument("--force", action="store_true", help="hatalara ragmen yaz (onerilmez)")
    ap.add_argument("--self-test", action="store_true", help="gomulu regresyon testleri")
    a = ap.parse_args()

    if a.self_test:
        sys.exit(self_test())

    cfg = load_config(a.config)
    if not cfg["phases"]:
        sys.exit("HATA: yapilandirmada 'phases' bos "
                 "(iskele.config.json olustur; ornek: assets/iskele.config.example.json)")

    tasks, issues = load_tasks(a.xlsx, cfg)
    score_rows, score_issues = load_scorecard(a.xlsx, cfg)
    pair_rows, pair_issues = load_pairs(a.xlsx, cfg)
    issues = issues + score_issues + pair_issues
    errors = [m for l, m in issues if l == "ERROR"]
    for l, m in issues:
        print(f"  {'HATA ' if l == 'ERROR' else 'UYARI'}: {m}", file=sys.stderr)
    if errors and not a.force:
        print(f"\n{len(errors)} dogrulama hatasi — rapor YAZILMADI. "
              f"Cizelgeyi duzelt ya da --force kullan.", file=sys.stderr)
        sys.exit(2)

    try:
        C = compute(tasks, cfg, score_rows, pair_rows)
    except ValueError as e:
        print(f"\n{e}", file=sys.stderr)
        sys.exit(3)

    print(f"Gorev: {C['total_dn']}/{C['total_n']} · "
          f"Efor: {fmt(C['total_done'])}/{fmt(C['total_eff'])} gun · "
          f"Program %{C['overall_pct']}")
    for p in cfg["phases"]:
        d = C["phases"][p]
        pct = round(100 * d["done"] / d["eff"]) if d["eff"] else 0
        print(f"  {p}: %{pct:>3} · {d['dn']}/{d['n']} gorev · {fmt(d['eff'])} gun")

    if not C["arbiter_col"]:
        print("  Hakem: olculmedi (cizelgede 'Hakem' sutunu yok) — %0 DEGIL")
    elif C["total_done"] <= 0:
        print("  Hakem: henuz tamamlanan is yok")
    else:
        print(f"  Hakem: tamamlanan eforun %{C['arbiter_pct']}'i hakemli · "
              f"%{100 - C['arbiter_pct']}'i oz-beyan "
              f"({C['arbiter_dn']}/{C['total_dn']} gorev)")

    if score_rows is None:
        print("  Skorkart: olculmedi ('Skorkart' sekmesi yok) -- SIFIR DEGIL")
    elif not score_rows:
        print("  Skorkart: henuz kapanmis faz yok")
    else:
        T = C["score_totals"]
        parts = [f"{lab} {T[key][0] if T[key][0] is not None else 'olculmedi'}"
                 for key, lab in (("tur", "yeniden tur"),
                                  ("kriter", "yeniden yazilan kriter"),
                                  ("kacan", "kacan"))]
        print(f"  Skorkart ({len(score_rows)} faz, oz-beyan): "
              + " · ".join(parts))

    if pair_rows is None:
        print("  Cift pasi: olculmedi ('Cift' sekmesi yok) -- SIFIR DEGIL")
    elif not pair_rows:
        print("  Cift pasi: sekme var, hic cift yazilmamis")
    else:
        T = C["pair_tot"]
        print(f"  Cift pasi: {T['n']} cift · {T['kirik']} kirik"
              + (f" · {T['bakilmadi']} bakilmadi" if T["bakilmadi"] else ""))

    cd = C["cost"]
    if not cd["has_cost"]:
        print("  Birim maliyet: olculmedi ('Maliyet' sutunu yok) -- %0 DEGIL")
    elif cd["total"]["cost_n"] == 0:
        print("  Birim maliyet: sutun var, hic deger yazilmamis")
    else:
        u, ut = cd["unit_total"], cd["unit_task_total"]
        print(f"  Birim maliyet: {fmt(u) if u else '—'} / tamamlanan TAHMINI "
              f"efor-gunu · {fmt(ut) if ut else '—'} / kapanan gorev "
              f"({cd['total']['cost_n']} gorevde maliyet yazili)")
    if cd["has_dates"] and cd["total"]["days"]:
        days = sorted(cd["total"]["days"])
        print(f"  Gecen sure: medyan {days[len(days)//2]} gun "
              f"({len(days)} tamamlanmis gorev) -- efor DEGIL, acik kalma suresi")

    if a.check:
        return
    if not Path(a.html).exists():
        sys.exit(f"HATA: rapor bulunamadi: {a.html}")

    html = Path(a.html).read_text(encoding="utf-8")
    applied, missing = [], []
    for key, fn in RENDERERS.items():
        html, done = patch(html, key, fn(C, cfg))
        (applied if done else missing).append(key)
    Path(a.html).write_text(html, encoding="utf-8")
    print(f"Guncellendi: {a.html} (bolgeler: {', '.join(applied) or 'yok'})")
    if missing:
        print(f"  UYARI: raporda bulunmayan GEN bolgeleri: {', '.join(missing)}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
