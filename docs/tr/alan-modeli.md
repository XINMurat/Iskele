# Adım 2 — Alan modelini bulmak

> **Türkçe asıl.** `skill/iskele/references/domain-model.md`'nin Türkçe
> aslıdır; paketlenen sürüm İngilizcedir. Ana metin:
> [`metodoloji.md`](metodoloji.md)


Bu, kitin mekanikleştirilemeyen tek adımı. Iskele senin yerine ayrımı *bulmaz*;
aramanı zorlar ve bulduktan sonrasını mekanikleştirir. Buradaki dürüstlük önemli:
kalan altı adım şablon işidir, bu adım muhakemedir.

## Aranan soru

> Bu alanda birbirine karıştırılan ama **ayrı yaşam döngüsüne** sahip iki şey var mı?

Ayrı yaşam döngüsü testi: A değiştiğinde B de zorunlu değişiyor mu? Cevap **hayır**
ise ikisi ayrı varlıktır ve ayrı tablolarda durmalıdır.

## Sık karşılaşılan ayrım kalıpları

| Kalıp | A (yavaş değişen) | B (hızlı üretilen) | Örnek alan |
|---|---|---|---|
| **Tanım / Örnek** | Şablon, prosedür, tarif | O şablonun bir çalıştırması | Süreç yönetimi, iş akışı, sınav, checklist |
| **Katalog / Sipariş** | Ürün tanımı, fiyat listesi | Verilmiş sipariş satırı | E-ticaret, satın alma |
| **Kural / Değerlendirme** | Politika, formül, tarife | Bir olaya uygulanmış sonuç | Sigorta, faturalama, puanlama |
| **Plan / Gerçekleşen** | Bütçe, program, rota | Fiili harcama, kayıt, iz | Proje yönetimi, lojistik |
| **Kimlik / Olay** | Kişi, varlık, hesap | O varlığa olan şey | CRM, muhasebe, IoT |
| **Sürüm / Anlık görüntü** | Canlı belge | Yayınlanmış donmuş kopya | Doküman, sözleşme, mevzuat |

Bir alan birden fazla kalıp taşıyabilir. Hepsini isimlendir.

## Ayrımı bulmanın üç sorusu

1. **Geçmişe bakma sorusu:** "Altı ay sonra 'bunu o zaman nasıl yapıyorduk?' diye
   sorulacak mı?" Evet ise, geçmişi koruyan bir *donmuş kopya* mekanizması gerekir;
   canlı kaydı geçmişe yansıtmak bu cevabı yok eder.
2. **Çoğalma sorusu:** "Hangi kayıt bir kere yazılır, hangisi her kullanımda yeniden
   üretilir?" Farklı çoğalma hızları = farklı varlık.
3. **Sahiplik sorusu:** "Bunu kim değiştirebilir, kim yalnız kullanır?" Farklı yetki
   sınıfları çoğu zaman farklı varlığa işaret eder.

## Ayrım bulunduktan sonra — üç zorunlu karar

**a) Donma (freezing).** B, A'nın hangi hâlinden üretildi? Referans mı tutuyor,
kopya mı? Referans tutarsa A değişince B'nin geçmişi bozulur. Geçmiş önemliyse
**kopyala ve dondur** (snapshot), sadece işaret etme.

**b) Kimlik izlenebilirliği.** Donmuş kopya, canlı kayda geri izlenebilmeli
(`source_id` + `version`), ama ona *bağımlı* olmamalı.

**c) Yetki asimetrisi.** Genelde A'yı düzenlemek dar yetki, B'yi üretmek geniş
yetkidir. Bunu baştan modelle; sonradan eklemek acı verir.

## Anti-kalıplar

- **Tek tablo cazibesi.** "İkisi de adım, tek tabloda tutayım" → iki yaşam döngüsü
  tek yere sıkışır, sorgular ve yetkiler birbirine girer.
- **Polimorfik sahiplik.** `owner_type` + `owner_id` ile tek tabloda çok tip
  sahiplik pratiktir ama **yabancı anahtar zorlanamaz** (yetim kayıt riski). Küçük
  ölçekte kabul edilebilir; bilinçli ödünleşim olarak **yaz ve işaretle**, sessizce
  yapma.
- **Erken genelleştirme.** Henüz doğrulanmamış bir model üzerine dallanma/kural
  motoru kurma. Önce düz hâlini çalıştır (bkz. dikey dilim).

## Çıktı: ne yazılmalı

`01-mimari-ve-veri-modeli.md` içinde:

1. Bulunan ayrım(lar) ve **neden ayrı tutulduğu** (bir paragraf).
2. Varlık listesi + ilişkiler (tercihen çalıştırılabilir DDL).
3. Donma mekanizması varsa yapısı ve doğrulama testi:
   *"A'yı değiştir → eski B değişmemeli"*. Bu test kapıya (go/no-go) girer.
4. Bilinçli ödünleşimler (ne kaybediyoruz, ne zaman geri döneceğiz).

## Dikey dilim kuralı

Model kurulduktan sonra ilk inşa görevi **dikey dilim** olmalı: tek bir küçük akışı
veritabanından ekrana kadar uçtan uca çalıştır. Katmanları ayrı ayrı "bitirip"
sonra entegrasyonda sürprizle karşılaşmak, en pahalı rework kaynağıdır. Dikey dilim
çalışmıyorsa model veya altyapı gerçekten bağlı değildir.
