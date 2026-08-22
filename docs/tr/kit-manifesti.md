# Kit manifesti — her parça ne içerir, neden var

> **Türkçe asıl.** `skill/iskele/references/kit-manifest.md`'nin Türkçe
> aslıdır; paketlenen sürüm İngilizcedir. Ana metin:
> [`metodoloji.md`](metodoloji.md)


Şablonlar `assets/templates/` altında. Bu belge her parçanın **amacını** ve
**doldurma kurallarını** verir; şablonlar iskeleti.

Küçük projede parça atlayabilirsin — ama atladığını ve nedenini `00`'da yaz.

---

## 00 — Rehber (`00-BASLA-rehber.md`) · zorunlu

Kitin haritası. İçerir: dosya tablosu (hangi dosya ne işe yarar, ne zaman
kullanılır), önerilen kullanım sırası, çalışma disiplini kuralları.

Disiplin maddeleri (en az bunlar):
- Faz atlama yok.
- Görev = tek atomik iş; "kısmen bitti" yok.
- Kanıt olmadan "done" yok.
- Negatif bulguyu kaydet (sessizce başka yola sapma).

---

## 01 — Mimari ve veri modeli · zorunlu

Bkz. `domain-model.md`. İçerir: alan ayrımı + gerekçesi, varlıklar/ilişkiler
(tercihen DDL), teknoloji seçimleri ve **neden** seçildiği, bilinçli ödünleşimler.

Kural: her teknoloji seçimi bir kısıta bağlanmalı ("on-prem + AD zorunlu olduğu
için ..."). Kısıta bağlanamayan seçim tercihtir; öyle işaretle.

---

## 02 — Yol haritası · zorunlu

Fazlar, kapılar, bağımlılık zinciri.

Her faz için: amaç, kapsam, **kapsam dışı (açık)**, çıkış kriteri, kaba efor.
Her kapı için: kilometre taşı adı + go/no-go'ya işaret.

Kural: fazlar takvim değil bağımlılık sırasıdır. "Bir sonraki fazın kaydedecek
verisi bir öncekinden gelir" testini uygula.

Efor verirken: tabanı söyle (bottom-up görev toplamı mı, top-down tahmin mi),
kalibresiz olduğunu işaretle, ilk faz sonrası yeniden kalibre edeceğini yaz.

---

## 03 — Görev listesi (backlog) · zorunlu

Format (üreteç buna bağlı — bkz. `tracking.md`):

```markdown
### Epik F1.2 — Süreç & adım
- [ ] **F1-BE-04** (M) Süreç CRUD API. **Bağ.:** F1-BE-02, F1-BE-03
  - *Kabul:* Süreç oluşturma/düzenleme yetki kontrolüyle çalışır; taslak başlar.
```

Zorunlu alanlar: ID, tahmin `(S|M|L)`, başlık, bağımlılık, **kabul kriteri**.

Kabul kriteri testi: *bunu çalıştırarak doğrulayabilir miyim?* Hayırsa yeniden yaz.

| Kötü | İyi |
|---|---|
| "Arama iyi çalışır" | "Başlıkta geçen kelimeyle arama sonuç döner; yetkisiz birim sonuçları gelmez" |
| "Güvenlik eklenir" | "Yetkisiz istek 403 alır; token'sız istek 401 alır" |

Tahmin ölçeği (varsayılan): `S≈0.75`, `M≈1.5`, `L≈4` iş-günü. Projeye göre
değiştirilebilir ama **çizelge, rapor ve üreteçte aynı olmalı**.

---

## 04 — Kalite kapıları · zorunlu

İki bölüm:

**Tamamlandı Tanımı (DoD)** — her görevde geçerli. Çekirdek maddeler:
- Kabul kriteri **fiilen çalıştırıldı** (göz kararı değil).
- Değişiklik ana dala girdi.
- Davranış değiştiyse otomatik test var.
- Yeni arayüz ise yetki kontrolü var.
- Çizelge güncellendi.
- Tıkanma/negatif bulgu kayda geçti.

**Faz go/no-go** — kapı başına somut, tek tek işaretlenebilir maddeler. Her
kapıda alan modelinin kritik değişmezi (ör. donma testi) yer almalı.

---

## 05 — Geliştirme kurulumu · opsiyonel (ama çoğu projede gerekli)

Ön gereksinimler (sürümlerle), klasör yapısı, adım adım kurulum komutları,
doğrulama komutu ("şunu çalıştır, şunu görmelisin"), sık sorunlar.

---

## 06 — Riskler ve kararlar · zorunlu

**Risk kaydı:** risk, etki, olasılık, azaltma, durum. Proje boyunca canlı.

**ADR (karar kaydı):** her mimari karar için bağlam → karar → gerekçe → sonuç.
Kararı değiştirdiğinde eskisini silme, "değiştirildi (→ ADR-x)" diye işaretle.
Bir yol tıkandığında "denedim, olmadı, çünkü…" diye ADR yaz — negatif bulgu
kaydedilmezse aynı duvara ikinci kez çarpılır.

---

## 07 — İlerleme raporu (`.html`) · zorunlu

Üst düzey görünüm. Sayısal bölgeler `GEN:...:BEGIN/END` işaretleri arasında;
üreteç yalnız oraya dokunur. Bölümler: özet göstergeler, faz kartları,
efor-ağırlıklı epik çubukları, kapı/faz zaman çizelgesi, riskler, ADR listesi.

Kural: **rapor çizelgenin türevidir.** Çelişki varsa çizelge doğrudur, rapor
düzeltilir. Rapordaki her sayı ya hesaplanır ya "tahmin" diye işaretlenir.

---

## 08 — Takip çizelgesi (`tracker.xlsx`) · zorunlu

Backlog'un satır satır hâli + Durum/Sorumlu/Tarih/Not. `Ozet` sekmesi formülle
hesaplar (elle sayı girme). Şema: `tracking.md`.

---

## 09 — Onboarding (`08-onboarding.md`) · opsiyonel

Yeni katılan için 15 dakikalık bağlam: ne yapıyoruz, anlaşılması gereken tek
en önemli fikir (alan ayrımı), yığın, kritik kurallar, okuma sırası, "hangi soru
hangi dosyada" tablosu.

---

## Kalite kontrol — kit teslim edilmeden önce

- [ ] Her sayı üç yerde aynı mı? (backlog ↔ çizelge ↔ rapor)
- [ ] Her görevin kabul kriteri çalıştırılabilir mi?
- [ ] Her fazın "kapsam dışı"ı yazılı mı?
- [ ] Efor tabanı ve kalibresizlik işaretli mi?
- [ ] Üreteç bozuk veriyle denendi mi? (yalnız mutlu yol değil)
- [ ] Atlanan parçalar ve nedeni `00`'da yazılı mı?
