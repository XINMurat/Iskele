# [PROJE] — Teslim Kiti Rehberi

Bu kit, projeyi uçtan uca geliştirip yürütmek için gereken planlama dokümanlarını
ve takip araçlarını içerir.

## Kit içeriği

| # | Dosya | Ne işe yarar | Ne zaman |
|---|---|---|---|
| 00 | `00-BASLA-rehber.md` | Bu dosya — kitin haritası | İlk |
| 01 | `01-mimari-ve-veri-modeli.md` | Alan modeli, şema, kararlar | Referans — temel |
| 02 | `02-yol-haritasi.md` | Fazlar, kapılar, bağımlılıklar | Planlama |
| 03 | `03-gorev-listesi.md` | Atomik backlog + kabul kriterleri | Günlük geliştirme |
| 04 | `04-kalite-kapilari.md` | DoD + go/no-go | Görev/faz kapanışında |
| 05 | `05-gelistirme-kurulumu.md` | Lokal ortam kurulumu | Başta, bir kez |
| 06 | `06-riskler-ve-kararlar.md` | Risk kaydı + ADR | Karar verirken |
| 07 | `07-ilerleme-raporu.html` | Üst düzey rapor | Haftalık |
| 08 | `tracker.xlsx` | Canlı takip çizelgesi | Her gün |

*Atlanan parçalar:* [hangileri, neden]

## Kullanım sırası

1. Mimari ve veri modelini oku (`01`) — modeli içselleştir.
2. Yol haritasını gözden geçir (`02`) — faz sınırlarını anla.
3. Ortamı kur (`05`).
4. `03`'ten sıradaki görevi al (F0'dan başla).
5. `tracker.xlsx`'i güncelle → `python progress.py`.
6. Kalite kapılarını uygula (`04`).
7. Risk/karar dosyasını canlı tut (`06`).

## Çalışma disiplini

- **Faz atlama yok.** Kapı geçilmeden sonraki faza geçme.
- **Görev = tek atomik iş.** "Kısmen bitti" yoksa görev doğru boyutlanmış demektir.
- **Kanıt olmadan "done" yok.** Kabul kriterini fiilen çalıştır.
- **Negatif bulguyu kaydet.** Tıkandıysan `06`'ya yaz, sessizce sapma.
- **Rapor çizelgenin türevidir.** Çelişkide çizelge doğrudur.
