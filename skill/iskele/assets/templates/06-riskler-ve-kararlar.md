# Riskler ve Kararlar

İkisi de canlı belgedir: yeni risk/karar çıktıkça eklenir, eskisi silinmez.

## 1. Risk kaydı

Etki/olasılık: D=düşük, O=orta, Y=yüksek.

| # | Risk | Etki | Olas. | Azaltma | Durum |
|---|---|---|---|---|---|
| R1 | [çekirdek varsayım yanlış çıkarsa] | Y | O | [erken test, hangi kapıda] | Açık |
| R2 | [entegrasyon/bağımlılık riski] | O | O | [azaltma] | Açık |

## 2. Mimari Karar Kayıtları (ADR)

Format: **durum → bağlam → değerlendirilen seçenekler → karar → gerekçe → sonuç.**
Kararı değiştirdiğinde eskisini **silme**: yeni ADR açılır, eskisinin durumu
`Yerini aldı → ADR-x` olur. Zincir ileriye doğru gezilebilir kalır.

**Durum sözlüğü** — bu beş değerden biri, başka bir şey değil:

| Durum | Anlamı |
|---|---|
| `Önerildi` | Yazıldı, henüz karar verilmedi |
| `Kabul edildi` | Yürürlükte. **Pratikte değişmez** — değiştirmek yeni ADR açmaktır |
| `Reddedildi` | Değerlendirildi, seçilmedi. Kayıtta kalır: neden seçilmediği de bilgidir |
| `Kullanımdan kalktı` | Artık geçerli değil ve yerini alan bir karar yok |
| `Yerini aldı → ADR-x` | Yerine ADR-x geçti; ileri işaret **zorunlu** |

`Kabul edildi`nin pratikte değişmez olması koleksiyonun tek güvenilirlik
kaynağıdır: yürürlükteki bir ADR sessizce düzenlenebiliyorsa, altı ay sonra
okuyan kişi hangi kararın ne zaman alındığını bilemez.

**Değerlendirilen seçenekler kendi bölümüdür**, gerekçenin içinde bir yan cümle
değil. Sebebi: bir kararın en pahalı kısmı seçilmeyen yoldur, ve "gerekçe"
alanına sıkıştırıldığında ilk kırpılan o olur. **Hiçbir şey yapmama seçeneği de
listeye girer** — çoğu zaman gerçek rakip odur.

### ADR-1 — [karar başlığı]
- **Durum:** Kabul edildi · [YYYY-AA-GG]
- **Bağlam:** [hangi kısıt/problem]
- **Değerlendirilen seçenekler:**
  - A) [seçenek] — [bedeli / neden değil]
  - B) [seçenek] — [bedeli / neden değil]
  - C) Hiçbir şey yapma — [bu neyi kaybettirirdi]
- **Karar:** [ne yapıldı, hangi seçenek]
- **Gerekçe:** [neden bu — kısıta bağlı, zevke değil]
- **Sonuç:** [ne kazanıldı, hangi bedel kabul edildi]

> Zinciri `python check_adr.py` doğrular: durum sözlüğü dışında bir değer,
> çözülmeyen bir `→ ADR-x` işareti, ya da yerini aldığı ADR'nin durumu
> güncellenmemiş bir kayıt hatadır. Düzyazıdaki bir ileri işaret hiçbir şeye
> bağlı değildir; bu onu bağlar.

## 3. Kullanım

- **Karar verirken:** ilgili ADR var mı bak; yeni karar aldıysan ADR ekle.
- **Bir yol tıkandığında:** "denedim, olmadı, çünkü…" diye ADR yaz — negatif bulgu
  kaydedilmezse aynı duvara ikinci kez çarpılır.
- **Faz başında:** risk kaydını gözden geçir.
