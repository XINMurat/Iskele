# AGENTS.md — [PROJE]

> Bu dosya **kural deposu değil, yön tabelasıdır.** Kuralların tek gerçek
> kaynağı kit dosyalarıdır. Buradaki bir satır kit ile çelişirse **kit kazanır
> — ve çelişkiyi bildir.** Sessizce birine uymak, ikisini de yanlış yapar.
>
> *(Bu blok kitte kalır; köşeli parantezli alanlar doldurulur.)*

## Proje

**[PROJE]** — [bir cümlelik iş tanımı; teknoloji değil, ne işe yaradığı]

- **Yığın:** [diller, çatılar]
- **Mimari:** [tek cümle] → ayrıntı: `01-mimari-ve-veri-modeli.md`
- **Alan modelinin taşıyıcı ayrımı:** [şemanın üstünde durduğu ayrım]

Ayrımı anlamadan şemaya dokunma — yanlış ayrım iş ortasında çöker ve her faza
yeniden çalışma yükler.

## Nerede ne var

| Aradığın | Dosya |
|---|---|
| Alan modeli, şema, mimari kararlar | `01-mimari-ve-veri-modeli.md` |
| Fazlar, kapılar, bağımlılık zinciri | `02-yol-haritasi.md` |
| Sıradaki görev + kabul kriteri | `03-gorev-listesi.md` |
| Tamamlandı Tanımı, go/no-go, güvenlik | `04-kalite-kapilari.md` |
| Lokal ortam, çalıştırma | `05-gelistirme-kurulumu.md` |
| Risk kaydı + karar gerekçeleri (ADR) | `06-riskler-ve-kararlar.md` |
| Bir şey tutmadığında ne yapılır | `09-kurtarma-rampalari.md` |
| Canlı durum, ilerleme | `tracker.xlsx` → `python progress.py` |

## Komutlar

```bash
[kurulum]
[test]
[çalıştır]
python progress.py      # çizelgeden raporu üret
python check_adr.py     # ADR zincirini doğrula
```

## Çalışma disiplini

1. **Görev listesinden al.** Spec'siz, kabul kriterisiz iş başlamaz.
2. **Kabul kriterini fiilen çalıştır.** Yorumun, butonun, log satırının
   *varlığı* davranışın varlığı değildir.
3. **Ürettiğin her bilginin bir okuma yüzeyi olsun** — ya bu görevin
   kriterinde, ya onu getiren görevin ID'siyle. Üretim tarafı tek başına
   kriteri karşılamaz.
4. **Kapsam kutsaldır.** Faz dışına çıkma; gördüğün ilgisiz sorunu düzeltme,
   **raporla** (`09-kurtarma-rampalari.md` → RR-05).
5. **Boş elle soru sorma.** Belirsizlik getiren önerisini ve gerekçesini de
   getirir; kararı sahibi verir (RR-10).
6. **Çizelgeyi güncelle**, sonra `python progress.py`. İlerleme hesaplanır,
   tahmin edilmez.

## Yasaklar

- ❌ Kabul kriterini yapılana uyacak şekilde gevşetmek
- ❌ Kriteri çalıştırmadan "bitti" demek
- ❌ Kapsam dışı satırını, kendisi engel oldu diye silmek
- ❌ Yürürlükteki bir ADR'yi yerinde düzenlemek — yenisi açılır, eskisinin
  durumu `Yerini aldı → ADR-x` olur
- ❌ Kapanmış görevi, kanıtını silerek yeniden yazmak
- ❌ [projeye özgü: gizli anahtar, para hesabı, modül sınırı ihlali…]

## Bitti ne demek

`04-kalite-kapilari.md`'deki Tamamlandı Tanımı'nın tamamı işaretlenmeden görev
kapanmaz, faz kapısı geçilmeden sonraki faza geçilmez. **Kanıtsız "bitti" yok:**
test çıktısı, ekran görüntüsü ya da tekrar üretim adımları.

---

*Bu kit [iskele](https://github.com/XINMurat/Iskele) ile üretildi. Kitin
haritası ve okuma sırası: `00-BASLA-rehber.md`.*
