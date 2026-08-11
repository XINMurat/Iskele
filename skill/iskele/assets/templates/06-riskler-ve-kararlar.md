# Riskler ve Kararlar

İkisi de canlı belgedir: yeni risk/karar çıktıkça eklenir, eskisi silinmez.

## 1. Risk kaydı

Etki/olasılık: D=düşük, O=orta, Y=yüksek.

| # | Risk | Etki | Olas. | Azaltma | Durum |
|---|---|---|---|---|---|
| R1 | [çekirdek varsayım yanlış çıkarsa] | Y | O | [erken test, hangi kapıda] | Açık |
| R2 | [entegrasyon/bağımlılık riski] | O | O | [azaltma] | Açık |

## 2. Mimari Karar Kayıtları (ADR)

Format: bağlam → karar → gerekçe → sonuç. Kararı değiştirdiğinde eskisini silme,
"değiştirildi (→ ADR-x)" diye işaretle.

### ADR-1 — [karar başlığı]
- **Bağlam:** [hangi kısıt/problem]
- **Karar:** [ne yapıldı]
- **Gerekçe:** [neden bu, alternatif neden değil]
- **Sonuç:** [ne kazanıldı, hangi bedel kabul edildi]

## 3. Kullanım

- **Karar verirken:** ilgili ADR var mı bak; yeni karar aldıysan ADR ekle.
- **Bir yol tıkandığında:** "denedim, olmadı, çünkü…" diye ADR yaz — negatif bulgu
  kaydedilmezse aynı duvara ikinci kez çarpılır.
- **Faz başında:** risk kaydını gözden geçir.
