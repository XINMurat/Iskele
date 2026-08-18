---
name: iskele
description: Turns a vague project intent into an executable delivery kit — domain model, phased roadmap with gates, atomic backlog with acceptance criteria, Definition-of-Done quality gates, a tracking spreadsheet, and a progress report that regenerates itself from the tracker. Use this skill whenever someone wants to plan, scope, structure, or kick off a software project or major feature — including "proje planla", "yol haritası çıkar", "task listesi / backlog çıkar", "nereden başlayacağımı bilmiyorum", "bu projeyi nasıl kurarım", "geliştirme planı", "kit oluştur", "sprint planı", "MVP kapsamı", "ilerleme raporu / takip çizelgesi kur" — and also when a user merely describes an app or system they want to build and clearly needs structure rather than code. Use it too when an existing project has a roadmap but no tracking, no acceptance criteria, or no way to see progress. Generative sibling of mizan (audits claims) and kiyas (generates ideas); iskele builds the structure they operate on.
---

# Iskele

Bir projeyi *kurar*: belirsiz niyeti, yürütülebilir ve izlenebilir bir iş sistemine çevirir.

Üçlünün fiilleri ayrıdır — **iskele kurar, mizan tartar, kiyas üretir.** Karıştırma:
denetim/kanıt sorusu geldiyse mizan'a, fikir/tıkanma sorusu geldiyse kiyas'a geç.

## Neden bu skill var

Planlama çıktıları iki tipik şekilde başarısız olur:

1. **Yürütülemez plan** — güzel bir yol haritası var ama "bugün ne yapacağım" belirsiz;
   görevler atomik değil, kabul kriteri yok, bitip bitmediği tartışmaya açık.
2. **İzlenemez plan** — görev listesi var ama ilerleme el yordamıyla tahmin ediliyor;
   rapor gerçeği değil, yazarın hissini yansıtıyor.

Iskele bu ikisini kapatır: her görev atomik ve kabul kriterli, ilerleme veriden
*hesaplanır*, rapor çizelgenin türevi olur.

## Ne zaman kullan, ne zaman kullanma

**Kullan:** yeni proje/ürün/büyük özellik planlanacaksa; mevcut projede backlog,
takip veya kabul kriteri yoksa; "nereden başlasam" sorusu varsa.

**Kullanma:** tek bir dosya/fonksiyon işi (doğrudan yap); yalnız fikir aranıyorsa
(kiyas); yalnız mevcut iddialar denetlenecekse (mizan); acil bug (önce düzelt).

## Çekirdek döngü — yedi adım

Sırayı bozma. Her adım bir öncekinin çıktısını girdi alır; atlanan adım sonraki
adımda çöker.

### 1. Kısıtları çıkar (soru sor, varsayma)

Mimariyi kısıtlar belirler, tercihler değil. En az şunları netleştir:

- **Nerede çalışacak?** (on-prem / bulut / masaüstü / mobil)
- **Ölçek ve kimlik?** (kaç kullanıcı, SSO zorunlu mu, çok kiracılı mı)
- **Şimdi hangi çıktı isteniyor?** (plan mı, prototip mi, ikisi mi)
- **Sert kısıtlar?** (mevcut yığın, mevzuat, teslim tarihi, ekip büyüklüğü)

Cevap belirsizse **tek turda sor**; üçten fazla soru sorma. Kullanıcı zaten
söylediyse tekrar sorma — konuşmadan çıkar.

### 2. Alan modelini bul — ayrımı ara (en kritik adım)

Bu adım mekanikleştirilemez; ama **aranacak soru sabittir**: *bu alanda birbirine
karıştırılan ama ayrı yaşam döngüsüne sahip iki şey var mı?*

Ayrım bulunmadan şema yazma. Yanlış ayrımla kurulan şema, inşanın ortasında çöker
ve tüm fazlara rework yükler.

Ayrım kalıpları ve nasıl aranacağı için: **`references/domain-model.md`** oku.

Çıktı: varlıklar, ilişkiler, ve *ayrımın neden ayrı tutulduğunun* gerekçesi.

### 3. Fazla ve kapıları kur

Fazlar bağımlılık zinciridir, takvim değil. Her fazın çıkışına bir **kapı**
(kilometre taşı + go/no-go) koy. Kural: bir sonraki fazın *kaydedecek verisi*
bir öncekinden gelmeli.

Her faz için: amaç, kapsam, **açık kapsam dışı** (kapsam sürüklenmesini bu önler),
çıkış kriteri.

### 4. Backlog'u atomize et

Her görev: `ID` · epik · katman · **tahmin (S/M/L)** · **bağımlılık** · **kabul kriteri**.

- ID şeması sabit olsun (ör. `F{faz}-{katman}-{no}`) — çizelge, rapor ve üreteç
  buna bağlanır.
- Kabul kriteri **çalıştırılabilir** olmalı: "endpoint 200 döner", "yetkisiz istek
  403 alır". "İyi çalışır" kabul kriteri değildir.
- Kabul kriteri **tüketim tarafından** yazılır: *"kullanıcı X'e ulaşıyor"*, *"sistem
  X üretiyor"* değil. İkisi farklı cümledir ve ilki ikincisini **ima etmez**.
  Üretim taraflı bir kriter, üretim doğru yapıldığında geçer — ulaşılamayan bir
  yetenek geride kalsa bile.
- **Üreten görev, tüketen eşini adlandırır.** Kullanıcının göreceği bir bilgi üreten
  her görevin kabul kriterinde ya okuma yüzeyi vardır ya da o yüzeyi getiren görevin
  ID'si yazılıdır (`→ F3-FE-03`). Backlog'u katman ekseninde (BE/FE) kesmek bu
  boşluğu **varsayılan hâle getirir**: boşluk görevlerin arasında yaşar, hiçbir
  görevin kendi listesi onu göremez.
- Bir görev "kısmen bitti" olamaz; olabiliyorsa görev fazla büyüktür, böl.

> **Somut hata (bu kuralı doğuran):** bir bildirim görevi *"ilgili olay bildirim
> üretiyor"* kriteriyle kapandı. Uçlar ve on iki test yerindeydi; ön yüzde tek bir
> bildirim çağrısı yoktu — kullanıcı hiçbir bildirimi göremiyordu. Testlerden biri
> `read_all_clears_the_badge` adını taşıyordu: **var olmayan bir rozeti** sınıyordu.
> Aynı sınıf o projede dört kez tekrarladı (denetim izi, ek silme, parola, bildirim)
> ve **hiçbiri plandan çıkmadı** — dördü de tesadüfen fark edildi.

### 5. Kalite kapılarını yaz

İki seviye:

- **Tamamlandı Tanımı (DoD)** — her görev için ortak kontrol listesi.
  Zorunlu iki madde: *kabul kriterini fiilen çalıştır* (yorumun, butonun, log
  satırının varlığı davranışın varlığı değildir) ve *üretilen her bilginin bir
  okuma yüzeyi vardır* (üretim tarafı tek başına yetmez).
- **Faz go/no-go** — kapıda tek tek doğrulanacak somut maddeler.

- **Senaryo provası** — üçüncü seviye, ve kapıların en çok atlanan maddesi.
  DoD ile go/no-go, *yazılmış olanı* denetler: kabul kriteri tuttu mu, uç
  ulaşılabilir mi. İkisi de **hiç yazılmamış olanı** göremez. İki soru sınıfı
  yalnız burada yakalanır:

  1. **Alanın gerçeği modelde ifade edilebiliyor mu?** Sahada rutin olarak
     olan durumları listele ve tek tek dene. Üç sonuç: ifade edilebiliyor
     (tamam) · edilemiyor **ama bilinçli sınır olarak yazılı** (tamam, bu bir
     karardır) · edilemiyor **ve hiçbir yerde yazılı değil** (bulgu).
     *Belgesiz boşluk, karar verilmiş sınırdan her zaman kötüdür.*
  2. **İki özellik aynı anda geçerliyken hangisinin güvencesi kırılıyor?**
     Backlog'u atomize etmek (adım 4) tam da bu kusuru yok eder: parçalara
     ayırınca yalnız *kesişimde* var olan hata görünmez olur. Bu yüzden
     kapıda bilerek geri toplanır. Her yeni özellik için, dokunabileceği
     mevcut güvenceleri listele ve *"bu özellik etkinken o güvence hâlâ
     geçerli mi?"* diye sor. En kırılgan ikisi: **türetilmiş sinyaller**
     (bir yokluktan hesaplanan her şey — "3 gündür dokunulmadı",
     "atanmamış" — yeni bir durum eklenince sessizce anlam değiştirir) ve
     **çağrı yeri yeri uygulanan güvenceler** (beş yerde doğru uygulanan bir
     gizlilik kuralını, altıncı bir toplu yüzey tek hamlede deler).
     **Sıra da sayılır:** bazı çiftler yalnız tek yönde güvenlidir.

  **Listeyi tek başına yazamazsın ve yazıyormuş gibi yapma.** Alanı bilen
  kişiye sor; uydurulmuş makul senaryolar, kanıt etiketi takılmış kurgudur.
  **Ve senaryolar bulgudan ÖNCE yazılır:** sonradan yazılan senaryo, kendi
  bulduğu şeyi bulmuş olur ve kapsam hakkında hiçbir şey kanıtlamaz (HARKing).
  Bu yüzden kural listenin kendisinden önemlidir: **her yeni faz, kendi
  senaryolarını faz açılırken ekler**, kapıya gelince değil.

  Yeşil test süiti burada karşı-kanıt değildir: testler özellik başına
  yazılır, yani parçalar hakkında konuşur ve çift hakkında susar.

### 6. Takip + üreteci kur

- **Çizelge** (`tracker.xlsx`): backlog'un satır satır hâli + Durum/Sorumluluk/Tarih.
  `scripts/backlog_to_tracker.py` bunu backlog markdown'ından üretir.
- **Rapor** (`report.html`): çizelgenin türevi. Sayısal bölgeler `GEN:...:BEGIN/END`
  işaretleri arasında; **script yalnız oraya dokunur**, gerisi elle düzenlenebilir.
- **Üreteç** (`scripts/progress.py`): çizelgeyi okur, **efor-ağırlıklı** ilerlemeyi
  hesaplar, raporun işaretli bölgelerini yeniden üretir.

Kurulum ve sözleşmeler: **`references/tracking.md`** oku.

### 7. Devret

Kit tamamlanınca:

- **mizan** → kitin kendi iddialarını denetle (kanıt katmanları, Gap Map).
  Özellikle "doğrulandı" diyen her cümleyi karşı-örnek taramasına sok.
- **kiyas** → eksik özellik/risk adaylarını üret; adaylar backlog'a görev olarak
  geri girer.

Devir düzyazı değil, dosya. İki adaptör bunu taşır:

```bash
python scripts/iskele_to_registry.py --backlog 03-gorev-listesi.md --out registry.yaml
python scripts/kiyas_to_backlog.py --seeds tohumlar.yaml --phase F2 --out yeni.md
```

Her kabul kriteri, iş başlamadan önce yazılmış bir çürütme koşuludur — Mizan'ın
R1'inin istediği şeyin ta kendisi. Bu yüzden backlog zaten bir önkayıt kümesidir;
adaptör onu Mizan'ın okuduğu şemaya çevirir, tersi yönde de Kıyas'ın "en ucuz
çürütme"si doğrudan kabul kriteri olur.

**Hakem varsayılanı `author`'dır ve öyle kalmalıdır.** Çizelgedeki `Durum`'u işi
yapan doldurur; bu ölçüm değil öz-beyandır, Mizan K'ye terfiyi kapatır. Görevin
hakemi gerçekten çalıştırılabilirse backlog'da adını ver:

```markdown
- *Kabul:* Yetkisiz istek 403 alır. **Hakem:** pytest tests/test_authz.py
```

Bunu sen yazmadıkça adaptör sınıfı yükseltmez — sessiz terfi, sessiz varsayımın
en pahalı türüdür.

**Devir aynı zamanda bir bağlam kesme noktasıdır.** Uzun oturumda her tur,
konuşmanın tamamını yeniden taşır: maliyet bulgunun değil transkriptin
boyutuyla büyür. Kit dosyaya yazıldığı anda o yükü taşımanın bir sebebi
kalmaz — bir sonraki faz **taze bir oturumda** başlayabilir, çünkü ihtiyacı
olan her şey (backlog, ADR günlüğü, çizelge, devir notu) diskte durur.
Bunu faz sınırında açıkça söyle; alışkanlıktan geçmiş bütün geçmişi ileri
taşımak, kitin var oluş sebebini boşa çıkarır.

Aynı ilkenin gündelik hâli: **dosyayı değil aralığı oku** (önce ara, sonra
gereken satırları aç), **geniş taramayı alt ajana ver** (ham çıktı değil sonuç
dönsün), ve **bulguyu üretildiği anda dosyaya yaz** — sona saklanan bulgu, hem
her turda bedelini ödetir hem ilk bağlam sıfırlamasında kaybolur.

Döngü kapanır: **iskele kurar → mizan tartar → kiyas üretir → iskele'ye geri girer.**

## Çıktı manifesti

Tam kit on parçadır. Küçük projede kısaltabilirsin ama **hangi parçayı neden
atladığını söyle** — sessizce atlama.

| # | Dosya | Zorunlu? | İşlev |
|---|---|---|---|
| 00 | `00-BASLA-rehber.md` | ✓ | Kitin haritası, kullanım sırası, çalışma disiplini |
| 01 | `01-mimari-ve-veri-modeli.md` | ✓ | Alan modeli, şema, mimari kararlar |
| 02 | `02-yol-haritasi.md` | ✓ | Fazlar, kapılar, bağımlılık zinciri |
| 03 | `03-gorev-listesi.md` | ✓ | Atomik backlog, kabul kriterleri |
| 04 | `04-kalite-kapilari.md` | ✓ | DoD + go/no-go + güvenlik listesi |
| 05 | `05-gelistirme-kurulumu.md` | — | Lokal ortam, çalıştırma adımları |
| 06 | `06-riskler-ve-kararlar.md` | ✓ | Risk kaydı + ADR (karar gerekçeleri) |
| 07 | `07-ilerleme-raporu.html` | ✓ | Üst düzey rapor (GEN işaretli) |
| 08 | `tracker.xlsx` | ✓ | Canlı takip çizelgesi |
| 09 | `08-onboarding.md` | — | Ekip için tek sayfalık bağlam |

Şablonlar: `assets/templates/`. Parça listesinin gerekçeleri ve her dosyanın
içeriği: **`references/kit-manifest.md`**.

## Kırmızı çizgiler

Bunlar gerçek başarısızlık kalıplarıdır; her biri sahada görüldü.

**Sahte kesinlik.** Tahminleri hassas sayı gibi sunma. "~78.5 gün" aritmetik olarak
doğru olsa bile *süre tahmini* olarak spekülatiftir: ağırlıklar yazar seçimidir, hız
verisi yoktur. Efor sayılarını verirken tabanını ve kalibresiz olduğunu söyle;
ilk faz gerçekleşince yeniden kalibre et.

**Mutlu-yol doğrulaması.** "Doğruladım" demeden önce sor: *hangi girdiyle?* İyi huylu
veriyle koşan doğrulama, girdi doğrulamasını hiç test etmez. En az bir kenar durum
(geçersiz değer, boş kayıt, yerelleştirilmiş metin) dene.

**Sessiz varsayım.** Üreteç bilinmeyen bir değeri sessizce varsayılana düşürmemeli;
görünür uyarı ver ya da yaz-ma. Sessizce yanlış bir gösterge, eksik göstergeden
kötüdür. (Türkçe/İngilizce karışık veride `ı/i` katlaması klasik tuzaktır.)

**Faz atlama ve kapsam sürüklenmesi.** Kapı geçilmeden sonraki faza geçme; her fazın
"kapsam dışı" listesini açıkça yaz.

**Kendi işini denetleme.** Kiti sen ürettiysen denetimi de sen yapıyorsan, hakem =
yazar. Bunu açıkça beyan et; yargı iddialarını kanıtlanmış saymayı bırak.

**Uydurma sayı.** Rapordaki her sayı ya veriden hesaplanmalı ya da tahmin olduğu
işaretlenmeli. İkisi de değilse yazma.

## Referanslar

- `references/domain-model.md` — Adım 2: ayrımı bulma kalıpları ve sorular
- `references/kit-manifest.md` — Adım 1–5: her dosyanın içeriği ve gerekçesi
- `references/tracking.md` — Adım 6: çizelge şeması, GEN işaretleri, üreteç kurulumu
- `assets/templates/` — doldurulacak şablonlar
- `scripts/backlog_to_tracker.py` — backlog markdown → `tracker.xlsx`
- `scripts/progress.py` — `tracker.xlsx` → raporun GEN bölgelerini güncelle
- `scripts/iskele_to_registry.py` — Adım 7: backlog → Mizan registry (önkayıt)
- `scripts/kiyas_to_backlog.py` — Adım 7: Kıyas tohumları → backlog görevleri
