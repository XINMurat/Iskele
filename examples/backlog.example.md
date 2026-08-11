# Görev Listesi (Backlog)

Görevler faz → epik → görev hiyerarşisinde. Her görev tek atomik iştir.

**ID şeması:** `F{faz}-{katman}-{no}` · Katman: `INF`=altyapı, `BE`=backend, `FE`=frontend, `X`=kesişen.
**Tahmin:** S ≈ ½–1 gün · M ≈ 1–2 gün · L ≈ 3–5 gün.
**Bağ.:** önce tamamlanması gereken görev(ler).
`[ ]` yapılacak · `[~]` devam · `[x]` tamamlandı (kabul kriteri doğrulandı).

> Bu dosya "ne yapılacak"ın kaynağıdır; günlük durum `tracker.xlsx`'te yürür.
> Çizelgeyi elle doldurma: `python backlog_to_tracker.py --backlog 03-gorev-listesi.md`

---

## F0 — Kurulum & Altyapı

### Epik F0.1 — Proje iskeleti
- [ ] **F0-INF-01** (S) Repo yapısı ve dizin düzeni. **Bağ.:** —
  - *Kabul:* Klasör yapısı standart; README kökte.
- [ ] **F0-INF-02** (M) Altyapı servisleri konteynerle ayağa kalkıyor. **Bağ.:** F0-INF-01
  - *Kabul:* `docker compose up` sonrası tüm servisler healthy.

### Epik F0.2 — Dikey dilim
- [ ] **F0-X-01** (M) Uçtan uca tek akış (DB → API → ekran). **Bağ.:** F0-INF-02
  - *Kabul:* Elle eklenen bir kayıt, API'den çekilip ekranda görünüyor. **→ M0**

---

## F1 — Çekirdek

### Epik F1.1 — Çekirdek model
- [ ] **F1-BE-01** (L) Alan modelinin tabloları ve migration'ları. **Bağ.:** F0-X-01
  - *Kabul:* Migration uygulanınca şemadaki tüm tablo/kısıtlar mevcut.
- [ ] **F1-BE-02** (M) Çekirdek CRUD API + yetki kontrolü. **Bağ.:** F1-BE-01
  - *Kabul:* Yetkisiz istek 403 alır; yetkili istek kaydı oluşturur.

<!-- Her görev: ID, tahmin (S/M/L), başlık, Bağ., Kabul. Kabul kriteri
     ÇALIŞTIRILABILIR olmalı — "iyi çalışır" kabul kriteri değildir. -->

---

## Özet sayım

| Faz | Görev sayısı | Kaba yük |
|---|---|---|
| F0 | 3 | ~3.75 gün |
| F1 | 2 | ~5.5 gün |

> Sayımı elle güncelleme — `progress.py --check` doğrusunu basar.
