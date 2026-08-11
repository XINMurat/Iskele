# İskele — Kullanım Kılavuzu (TR)

Bu kılavuz, skill'in yedi adımlı döngüsünün Türkçe anlatımıdır. Normatif kaynak
skill'in kendisidir: [`skill/iskele/SKILL.md`](../../skill/iskele/SKILL.md).
İngilizce karşılığı: [`../en/usage-guide.md`](../en/usage-guide.md).

## Kurulum

```bash
cp iskele.skill ~/.claude/skills/
pip install -r skill/iskele/scripts/requirements.txt
```

## Yedi adım — özet

| Adım | Ne yapılır | Nerede anlatılır |
|---|---|---|
| 1 | Kısıtları çıkar (tek turda, en fazla üç soru) | SKILL.md §1 |
| 2 | Alan ayrımını bul — şemadan **önce** | `references/domain-model.md` |
| 3 | Fazları ve kapıları kur (bağımlılık zinciri, takvim değil) | SKILL.md §3 |
| 4 | Backlog'u atomize et (ID · tahmin · bağ. · kabul) | `assets/templates/03-*.md` |
| 5 | Kalite kapılarını yaz (DoD + go/no-go) | `assets/templates/04-*.md` |
| 6 | Takip + üreteci kur | `references/tracking.md` |
| 7 | Devret (mizan / kiyas) | SKILL.md §7 |

## Zinciri kurmak

### Çizelgeyi üret

```bash
python skill/iskele/scripts/backlog_to_tracker.py \
  --backlog 03-gorev-listesi.md --out tracker.xlsx --config iskele.config.json
```

Backlog satır formatı (parser bunu arar):

```markdown
### Epik F1.2 — Süreç & adım
- [ ] **F1-BE-04** (M) Süreç CRUD API. **Bağ.:** F1-BE-02, F1-BE-03
  - *Kabul:* Yetki kontrolüyle çalışır; yetkisiz istek 403 alır.
```

Kurallar:
- `ID` benzersiz olmalı — mükerrer ID uyarı üretir.
- Tahmin `(S)`, `(M)` veya `(L)`.
- `Bağ.:` yoksa `—` yaz; boş bırakma.
- Kabul kriteri **koşulabilir** olmalı.

### Çizelgede ne elle doldurulur

| Sütun | Kim doldurur |
|---|---|
| `ID` `Faz` `Epik` `Gorev` `Katman` `Tahmin` `Bagimlilik` | üreteç |
| `Durum` `Sorumlu` `Baslangic` `Bitis` `Not` | elle |

`Ozet` sekmesi `COUNTIF`/`COUNTIFS` formülleriyle çalışır — oraya elle sayı
yazma, formülü bozarsın.

### Raporu yeniden üret

```bash
python skill/iskele/scripts/progress.py \
  --xlsx tracker.xlsx --html 07-ilerleme-raporu.html --config iskele.config.json
```

- `--check` — yazmaz, hesaplanan özeti basar.
- `--self-test` — gömülü regresyon testlerini koşar.
- `--force` — hatalara rağmen yazar (önerilmez; sessiz yanlış gösterge üretir).

Script yalnız `GEN:...:BEGIN` / `GEN:...:END` arasını yeniden yazar. Raporun
gerisini rahatça elle düzenleyebilirsin.

## Efor-ağırlıklı ilerleme

```
ilerleme % = Σ(tamamlanan görevlerin eforu) / Σ(tüm görevlerin eforu)
```

Varsayılan ağırlıklar `S=0.75 · M=1.5 · L=4` (iş-günü). Değiştireceksen üç yerde
birden değiştir: backlog ölçeği, `iskele.config.json`, rapor dipnotu.

**Kredi kuralı.** Varsayılan ikilidir: yalnız `Tamamlandi` kredi alır. `Devam`a
kısmi kredi vermek ilerlemeyi şişirir ve "neredeyse bitti" yanılsaması üretir;
vereceksen bilinçli yap ve rapora yaz.

## Kırmızı çizgiler

- **Sahte kesinlik.** Tahmini hassas sayı gibi sunma; tabanını ve kalibresiz
  olduğunu söyle, ilk faz gerçekleşince yeniden kalibre et.
- **Mutlu-yol doğrulaması.** "Doğruladım" demeden önce *hangi girdiyle* sorusunu
  cevapla; en az bir kenar durum dene.
- **Sessiz varsayım.** Üreteç bilinmeyen değeri sessizce varsayılana düşürmesin;
  görünür uyarı ver ya da yazma.
- **Faz atlama ve kapsam sürüklenmesi.** Kapı geçilmeden sonraki faza geçme;
  "kapsam dışı"nı açıkça yaz.
- **Kendi işini denetleme.** Kiti sen ürettiysen denetimi de sen yapıyorsan
  hakem = yazar; bunu beyan et.
- **Uydurma sayı.** Rapordaki her sayı ya hesaplanmıştır ya tahmin olarak
  işaretlidir.

## Sık karşılaşılan tuzaklar

**`ı`/`i` katlaması.** Karışık Türkçe/İngilizce veride büyük/küçük harf
dönüşümü platforma göre değişir. Yapısal adları (sekme, sütun, ID) ASCII tut;
hücre içeriği Türkçe olabilir.

**"Kısmen bitti" görevler.** Bir görev kısmen bitebiliyorsa fazla büyüktür; böl.
Aksi hâlde çizelge bir yalanı taşır ve rapor onu yüzdeye çevirir.

**Çizelgeyi elle senkron tutmak.** Backlog değiştiyse üreteci koştur. İki
kaynağı elle eşit tutma girişimi hep sapmayla biter.
