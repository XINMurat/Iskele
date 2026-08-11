# Yol Haritası

Fazlar bağımlılık zinciridir, takvim değil. Her fazın çıkışında bir **kapı** vardır;
kapı geçilmeden sonraki faza geçilmez.

## Faz haritası

| Faz | Ad | Amaç | Kaba efor | Çıkış kriteri (kapı) |
|---|---|---|---|---|
| F0 | Kurulum & Altyapı | Çalışan iskelet | ~X gün | M0 — dikey dilim çalışıyor |
| F1 | Çekirdek | İlk kullanılabilir sürüm | ~X gün | M1 — çekirdek akış uçtan uca |
| F2 | Genişletme | İkincil akışlar, sertleştirme | ~X gün | M2 — yayına hazır |

> Efor tabanı: görev tahminlerinin bottom-up toplamı (`progress.py --check`).
> **Kalibresizdir** — ilk faz gerçekleşince yeniden kalibre et.

## Bağımlılık zinciri

```
F0 (iskelet) ──► F1 (çekirdek) ──► F2 (genişletme)
     │                │
     │  F0 olmadan    │  F1 olmadan F2'nin
     │  F1 çalışamaz  │  genişleteceği şey yok
```

## Faz kapsamları

**F0 —** [kapsam]
*Kapsam dışı (bilinçli):* [ne yapılmayacak — kapsam sürüklenmesini bu önler]

**F1 —** [kapsam]
*Kapsam dışı:* [...]

**F2 —** [kapsam]
*Kapsam dışı:* [...]

## Kilometre taşları

- **M0 —** [somut, gözlenebilir çıkış durumu]
- **M1 —** [...]
- **M2 —** [...]

Her kilometre taşında `04-kalite-kapilari.md` içindeki go/no-go listesi çalıştırılır.

## Öneri: nasıl ilerlemeli

F0'ı **dikey bir dilimle** bitir — tek bir akışı DB'den ekrana kadar çalıştır.
Katmanları ayrı ayrı "bitirip" entegrasyonda sürprizle karşılaşmak en pahalı
rework kaynağıdır.
