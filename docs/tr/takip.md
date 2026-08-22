# Adım 6 — Takip ve üreteç

> **Türkçe asıl.** `skill/iskele/references/tracking.md`'nin Türkçe
> aslıdır; paketlenen sürüm İngilizcedir. Ana metin:
> [`metodoloji.md`](metodoloji.md)


Amaç: ilerlemeyi *tahmin etmek* değil *hesaplamak*. Rapor, çizelgenin türevidir.

## Zincir

```
03-gorev-listesi.md ──backlog_to_tracker.py──> tracker.xlsx ──progress.py──> 07-ilerleme-raporu.html
        (kaynak)                                  (canlı durum)                 (GEN bölgeleri)
```

Backlog "ne yapılacak"ın kaynağıdır; çizelge günlük durumu taşır; rapor okunur
görünümdür. İkisini elle senkron tutma — üreteci çalıştır.

## Çizelge şeması (`tracker.xlsx`)

**Sekme `Takip`** — sütunlar (bu adlar üreteç tarafından aranır):

| Sütun | Üretilen mi | Değerler |
|---|---|---|
| `ID` | ✓ backlog'dan | benzersiz |
| `Faz` | ✓ | yapılandırmadaki faz kodları |
| `Epik` | ✓ | `F1.2 Baslik` (ilk kelime epik kodu) |
| `Gorev` | ✓ | başlık |
| `Katman` | ✓ | ID'den türetilir |
| `Tahmin` | ✓ | `S` / `M` / `L` |
| `Bagimlilik` | ✓ | ID listesi |
| `Durum` | **elle** | `Yapilacak` / `Devam` / `Bloke` / `Tamamlandi` |
| `Sorumlu` `Baslangic` `Bitis` `Not` | **elle** | serbest |
| `Hakem` | ✓ kabul kriterinden | boş olabilir |

> `Hakem` sütunu **sona** eklenir, araya değil: `Durum` H sütununda kalmalı,
> çünkü `Ozet` formülleri ve açılır liste doğrulaması ona bağlı.

## Hakem sütunu ve ikinci gösterge

Kabul kriterine `**Hakem:** pytest tests/test_authz.py` yazarsan üreteç bunu
`Hakem` sütununa taşır. Yazmazsan sütun boş kalır — bu normaldir ve
**uydurulmaz**.

Rapor bunu ayrı bir bölge olarak basar (`GEN:HAKEM`): *tamamlanan eforun ne
kadarında yazardan başka bir hakem adı geçiyor.* İki şeye dikkat:

- **İlerleme yüzdesini değiştirmez.** "Bitti" ile "doğrulandı" iki ayrı şeydir;
  tek göstergeye eritmek ikisini de okunamaz yapar.
- **Kriterin fiilen koşulduğunu göstermez.** Bunu hiçbir çizelge bilemez; onu
  Tamamlandı Tanımı bilir. Gösterge yalnızca "bitti" hükmünün ne kadarının işi
  yapanın kendi beyanına dayandığını söyler.

`Hakem` sütunu olmayan eski çizelgelerde gösterge **%0 değil "ölçülmedi"**
basar. Ölçülmemiş bir şeyi sıfır göstermek, sessiz varsayımın en pahalı türüdür:
ölçüm gibi görünür.

**Sekme `Ozet`** — `COUNTIF`/`COUNTIFS` formülleriyle durum ve faz kırılımı.
Elle sayı girme; formül bozulur.

**Sekme `Aciklama`** — hangi sütun elle doldurulur, hangisi üretilir.

> ASCII not: sekme ve sütun adlarını ASCII tut (`Aciklama`, `Gorev`). Türkçe
> karakter, dosya/sütun eşleşmesinde platformlar arası sürtünme yaratır. Hücre
> *içeriği* Türkçe olabilir — üreteç `ı/i` katlamasını yapar.

## Efor-ağırlıklı ilerleme

```
ilerleme % = Σ(tamamlanan görevlerin eforu) / Σ(tüm görevlerin eforu)
```

Görev sayısı değil **efor** ağırlıklı: 4 günlük bir görev, 0.75 günlük bir görevle
aynı ağırlıkta sayılmamalı.

Varsayılan ağırlıklar `S=0.75 · M=1.5 · L=4` (iş-günü). Değiştireceksen üç yerde
birden değiştir: backlog ölçeği, `iskele.config.json`, rapor dipnotu.

**Kredi kuralı.** Varsayılan ikili: yalnız `Tamamlandi` kredi alır. `Devam`a kısmi
kredi (ör. 0.5) vermek ilerlemeyi şişirir ve "neredeyse bitti" yanılsaması üretir;
vereceksen bilinçli yap ve rapora yaz.

## GEN işaretleri

Rapor HTML'inde üretilecek her bölge şu çiftle sarılır:

```html
<!-- GEN:BARS:BEGIN (progress.py uretir; kaynak: tracker.xlsx) -->
    <div class="bars">...</div>
<!-- GEN:BARS:END -->
```

Üreteç **yalnız** bu bölgelerin içini değiştirir. Dışarısı (yorumlar, riskler, ADR
listesi, dipnot) elle düzenlenebilir ve korunur. Bu ayrım önemli: rapor hem
otomatik hem yazılabilir kalır.

Varsayılan bölge anahtarları: `CHIPS` (üst rozetler), `KPI` (özet göstergeler),
`CARDS` (faz kartları), `BARS` (epik çubukları), `TIMELINE` (kapı/faz akışı).

## Yapılandırma (`iskele.config.json`)

Üreteci projeye bağlayan tek dosya. Şablon: `assets/iskele.config.example.json`.

```jsonc
{
  "phases": ["F0", "F1"],
  "effort_weights": {"S": 0.75, "M": 1.5, "L": 4.0},
  "status_credit": {"Tamamlandi": 1.0, "Devam": 0.0,
                    "Bloke": 0.0, "Yapilacak": 0.0},
  "workdays_per_month": 21,
  "phase_meta": {
    "F0": {"title": "F0 · Kurulum", "repo": "faz/f0", "stack": "Docker",
           "ms": "M0", "dep": null, "desc": "..."}
  },
  "epic_display": {"F0.1": "F0.1 Proje iskeleti"},
  "static_steps": [{"t": "Mimari onaylandı", "m": "01-...md"}],
  "flow": [{"kind": "phase", "phase": "F0", "mk": "M0",
            "t": "M0 — İskelet", "m": "..."},
           {"kind": "gate", "phase": "F0", "mk": "◆",
            "t": "Kapı M0", "m": "go/no-go"}]
}
```

`phase_meta`/`epic_display`/`flow` **küratörlüdür** (insan yazar); sayılar
çizelgeden gelir. Bu ayrımı koru: prose yapılandırmada, sayı veride.

## Girdi doğrulama — sessiz varsayım yasak

Üreteç bilinmeyen bir değeri sessizce varsayılana düşürmemeli. Sahada görülmüş
üç hata ve kuralı:

| Hata | Sessiz davranış (yanlış) | Doğru davranış |
|---|---|---|
| Geçersiz `Tahmin` (`XL`) | sessizce `M` ağırlık | HATA, yazma |
| Yerelleştirilmiş `Durum` (`Tamamlandı` vs `Tamamlandi`) | sessizce 0 kredi → ilerleme eksik | normalize et + UYARI |
| Faz listesi dışı `Faz` (`F9`) | epik çubuğunda görünür, toplama girmez | **değişmez ihlali** → HATA |

**Değişmez:** `Σ epik eforu == Σ faz eforu`. Iraksama, bir görevin tanımlı fazların
dışına düşmesi demektir ve gösterge sessizce yanlışlanır. Üreteç bunu kontrol eder
ve ihlalde durur.

`progress.py` çıkış kodları: `0` başarılı · `2` doğrulama hatası (rapor yazılmadı)
· `3` değişmez ihlali. `--force` hatayı geçer (önerilmez), `--check` yazmadan özet
basar.

## Haftalık akış

1. Çizelgede `Durum` sütununu güncelle.
2. `python progress.py` çalıştır.
3. Uyarı/hata çıkarsa çizelgeyi düzelt (raporu değil).
4. Raporun elle yazılan bölümlerini (risk, "bu hafta odağı") tazele.
