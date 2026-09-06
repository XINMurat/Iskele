# Adım 6 — Takip ve üreteç

> **Türkçe asıl.** `skill/iskele/references/tracking.md`'nin Türkçe
> aslıdır; paketlenen sürüm İngilizcedir. Ana metin:
> [`metodoloji.md`](metodoloji.md)


Amaç: ilerlemeyi *tahmin etmek* değil *hesaplamak*. Rapor, çizelgenin türevidir.

## Zincir

```
03-gorev-listesi.md ──backlog_to_tracker.py──> tracker.xlsx ──progress.py──> 07-ilerleme-raporu.html
        (kaynak)                                  (canlı durum)                 (GEN bölgeleri)
```

Backlog "ne yapılacak"ın kaynağıdır; çizelge günlük durumu taşır; rapor okunur
görünümdür. İkisini elle senkron tutma — üreteci çalıştır.

## Çizelge şeması (`tracker.xlsx`)

**Sekme `Takip`** — sütunlar (bu adlar üreteç tarafından aranır):

| Sütun | Üretilen mi | Değerler |
|---|---|---|
| `ID` | ✓ backlog'dan | benzersiz |
| `Faz` | ✓ | yapılandırmadaki faz kodları |
| `Epik` | ✓ | `F1.2 Baslik` (ilk kelime epik kodu) |
| `Gorev` | ✓ | başlık |
| `Katman` | ✓ | ID'den türetilir |
| `Tahmin` | ✓ | `S` / `M` / `L` |
| `Bagimlilik` | ✓ | ID listesi |
| `Durum` | **elle** | `Yapilacak` / `Devam` / `Bloke` / `Tamamlandi` |
| `Sorumlu` `Baslangic` `Bitis` `Not` | **elle** | serbest |
| `Hakem` | ✓ kabul kriterinden | boş olabilir |
| `Maliyet` | — | **elle**, opsiyonel: bu görevi ilerleten oturum(lar)ın maliyeti. Birim serbest ama tutarlı olsun — rapor oranı hesaplar, tutarı yorumlamaz. İKİ ayrı paydaya bölünür: tamamlanan **tahmini** efor-günü (çubukların kullandığı S/M/L ağırlıkları) ve kapanan görev **sayısı**. İlki tahmin hatasını miras alır, ikincisi almaz; ikisini birden basmak bunu görünür kılar |
| `GercekEfor` | — | **elle**, opsiyonel: görevin gerçekten aldığı efor (gün). Geçen süre DEĞİLDİR — geçen süre görevin ne kadar açık kaldığını, bu ne kadar çalışıldığını ölçer. Tahminle birlikte **beklenti sapmasını** verir (gerçek / tahmini efor) ve o sapmanın ne olarak adlandırılabileceğine config'teki `estimate_basis` karar verir |

> `Hakem` sütunu **sona** eklenir, araya değil: `Durum` H sütununda kalmalı,
> çünkü `Ozet` formülleri ve açılır liste doğrulaması ona bağlı.

## Hakem sütunu ve ikinci gösterge

Kabul kriterine `**Hakem:** pytest tests/test_authz.py` yazarsan üreteç bunu
`Hakem` sütununa taşır. Yazmazsan sütun boş kalır — bu normaldir ve
**uydurulmaz**.

Rapor bunu ayrı bir bölge olarak basar (`GEN:HAKEM`): *tamamlanan eforun ne
kadarında yazardan başka bir hakem adı geçiyor.* İki şeye dikkat:

- **İlerleme yüzdesini değiştirmez.** "Bitti" ile "doğrulandı" iki ayrı şeydir;
  tek göstergeye eritmek ikisini de okunamaz yapar.
- **Kriterin fiilen koşulduğunu göstermez.** Bunu hiçbir çizelge bilemez; onu
  Tamamlandı Tanımı bilir. Gösterge yalnızca "bitti" hükmünün ne kadarının işi
  yapanın kendi beyanına dayandığını söyler.

`Hakem` sütunu olmayan eski çizelgelerde gösterge **%0 değil "ölçülmedi"**
basar. Ölçülmemiş bir şeyi sıfır göstermek, sessiz varsayımın en pahalı türüdür:
ölçüm gibi görünür.

**Sekme `Ozet`** — `COUNTIF`/`COUNTIFS` formülleriyle durum ve faz kırılımı.
Elle sayı girme; formül bozulur.

**`Skorkart` sekmesi** — faz kapanış skorkartı. **Opsiyonel, elle doldurulur ve
içindeki her sayı öz-beyandır.** Faz başına bir satır; kapıda, go/no-go'nun
yanında yazılır.

| Sütun | Dolduran | Anlamı |
|---|---|---|
| `Faz` | ✓ önceden yazılı | yapılandırmadaki faz kodları |
| `BacklogRevizyon` | **elle** | faz açıldıktan sonra değişen görev sayısı |
| `YenidenTur` | **elle** | birden fazla kez geri dönen görev |
| `KriterYenidenYazilan` | **elle** | işten **sonra** yeniden yazılan kabul kriteri |
| `IkizBoslugu` | **elle** | tüketen-ikiz boşlukları (RR-03) |
| `IkizKapida` | **elle** | bunların kaçı **kapıda** yakalandı |
| `SenaryoProvali` / `SenaryoTesadufi` | **elle** | senaryo bulgusu: provalı / tesadüfi |
| `KapsamDisi` | **elle** | faz dışına çıkma sayısı (RR-07) |
| `Rampalar` | **elle** | hangi `RR-nn` kullanıldı, serbest metin |
| `Kacan` | **elle** | kapıdan sonra bulunan, bu fazın kriterlerinin kapsadığı hata |
| `KacanSinifi` | **elle**, opsiyonel | her kaçak için: ateşlemesi gereken kontrol ya da bu kaçak sayesinde artık var olan kontrol (RR-13). Opsiyonel, çünkü mevcut çizelgeler kırılmadan okunmaya devam etmeli; sayı dolu ve bu hücre boşsa rapor *sınıfsız kaçak* basar — döngü kapanmamıştır |
| `Cikarim` | **elle** | bir iki cümle |

Hiçbiri backlog'dan üretilemez, ve mesele de bu: ölçülen şey işin kendisi değil
**planın nereden sızdırdığı** — bunu yalnızca kapıda duran insan bilir.

**Üretecin zorladığı üç kural:**

- **Sekme yok ≠ sıfır.** Sekmesi olmayan bir çizelge *"ölçülmedi"* basar.
  Sıfırlar dizisi, mümkün olan en pohpohlayıcı yalan olurdu: yeniden çalışma
  yok, yeniden yazılan kriter yok, kaçan yok.
- **Boş hücre ≠ sıfır.** `Faz` sütunu önceden yazılır ki tablo boş değil yarım
  dolu olsun; yani "satır var" ile "faz kapandı" aynı şey değildir. Hiçbir alanı
  doldurulmamış satır atlanır, kısmen doldurulmuş bir sütun ise kaç fazın
  cevapladığını basar (`3 (2/4 faz)`).
- **`IkizKapida` ≤ `IkizBoslugu`.** Bu bir alt kümedir: bulunanların kaçı kapıda
  yakalandı. Ters yazıldığında "kapıda yakalandı" oranı 1'i aşar ve tablo iyi
  haber gibi okunur — gösterge yanlışlaşmakla kalmaz, **ters döner**. Bu bir
  doğrulama hatasıdır (çıkış 2), sayı değil.

**İlerleme yüzdesine dokunmaz.** Bir faz %100 kapanıp skorkartında dört yeniden
yazılmış kriter taşıyabilir; bu çelişki değil, bilginin ta kendisidir. İkisini
tek göstergeye eritmek ikisini de okunmaz yapardı — `Hakem` sütunuyla aynı
gerekçe.

Rapor bunu kendi bölgesi olarak basar (`GEN:SKORKART`) ve her üretimde sayıların
öz-beyan olduğunu yazar. Skorkart da bir iddiadır: işi yapan doldurur, hakem =
yazar.

Ölçütlerin nereden geldiği ve nasıl okunduğu:
[`kurtarma.md`](kurtarma.md) — faz kapanış çizelgesi.

**Sekme `Cift`** — çift pası; her satır bir çift, **elle** doldurulur.

| sütun | dolduran | ne tutar |
|---|---|---|
| `Faz` | önceden yazılı | çiftin ait olduğu kapının fazı |
| `Ozellik` | **elle** | sınanan özellik (ya da görev ID'si) |
| `Garanti` | **elle** | onun dokunabildiği MEVCUT garanti |
| `SiraOnemli` | **elle** | çift yalnız tek yönde güvenliyse `evet` |
| `GerekliSira` | **elle** | o yön, açıkça yazılmış. `SiraOnemli` işaretliyse zorunlu — tek yönde güvenli bir çift, hangi yön olduğu yazılmadan bulgu değildir |
| `Sonuc` | **elle** | `tutuyor` · `kiriliyor` · `bakilmadi` |
| `Not` | **elle** | `kiriliyor` için zorunlu: hangi garanti, nasıl bozuluyor |

**Neden üretilemez.** Backlog'u atomize etmek (adım 4) tam olarak, yalnızca
**iki** özellik aynı anda etkinken var olan kusuru yok eden işlemdir. Onları
geri birleştiren pas, adım 5'in ikinci sorusudur ve bu sekme var olana kadar
hiçbir iz bırakmıyordu: pası koşan fazla atlayan faz birbirinin aynı çizelgeyi
üretiyordu. Yeni bir özelliğin hangi mevcut garantiye dokunabildiği görev
listesinden türetilemez; yalnızca modeli bilen insan bilir.

`bakilmadi` sıfır değildir. Listelenip hiç sınanmamış bir çift, kimsenin
listelemediği bir çift kadar korur; rapor bu yüzden iki sayıyı ayrı basar.
**Sekme opsiyoneldir**: o yokken üretilmiş bir çizelge değişmeden okunur ve
rapor `0` değil *ölçülmedi* basar.

Rapor bunu kendi bölgesi olarak basar (`GEN:CIFT`).

**Sekme `Aciklama`** — hangi sütun elle doldurulur, hangisi üretilir.

> ASCII not: sekme ve sütun adlarını ASCII tut (`Aciklama`, `Gorev`). Türkçe
> karakter, dosya/sütun eşleşmesinde platformlar arası sürtünme yaratır. Hücre
> *içeriği* Türkçe olabilir — üreteç `ı/i` katlamasını yapar.

## Efor-ağırlıklı ilerleme

```
ilerleme % = Σ(tamamlanan görevlerin eforu) / Σ(tüm görevlerin eforu)
```

Görev sayısı değil **efor** ağırlıklı: 4 günlük bir görev, 0.75 günlük bir görevle
aynı ağırlıkta sayılmamalı.

Varsayılan ağırlıklar `S=0.75 · M=1.5 · L=4` (iş-günü). Değiştireceksen üç yerde
birden değiştir: backlog ölçeği, `iskele.config.json`, rapor dipnotu.

**Kredi kuralı.** Varsayılan ikili: yalnız `Tamamlandi` kredi alır. `Devam`a kısmi
kredi (ör. 0.5) vermek ilerlemeyi şişirir ve "neredeyse bitti" yanılsaması üretir;
vereceksen bilinçli yap ve rapora yaz.

## GEN işaretleri

Rapor HTML'inde üretilecek her bölge şu çiftle sarılır:

```html
<!-- GEN:BARS:BEGIN (progress.py uretir; kaynak: tracker.xlsx) -->
    <div class="bars">...</div>
<!-- GEN:BARS:END -->
```

Üreteç **yalnız** bu bölgelerin içini değiştirir. Dışarısı (yorumlar, riskler, ADR
listesi, dipnot) elle düzenlenebilir ve korunur. Bu ayrım önemli: rapor hem
otomatik hem yazılabilir kalır.

Varsayılan bölge anahtarları: `CHIPS` (üst rozetler), `KPI` (özet göstergeler),
`CARDS` (faz kartları), `BARS` (epik çubukları), `TIMELINE` (kapı/faz akışı),
`HAKEM` (tamamlanan eforun ne kadarı yazardan başka bir hakem adı taşıyor),
`SKORKART` (faz kapanış çizelgesi), `CIFT` (çift pası — parçalara ayrılan iş
geri birleştirildi mi) ve `MALIYET` (birim maliyet ve geçen süre — ROI'nin
PAYDASI, ROI'nin kendisi değil).

`tools/check_doc_claims.py` bu listeyi üretecin `RENDERERS` sözlüğüne bağlar:
iki kez bayatladı — önce `HAKEM`, sonra `SKORKART` eklendi, bu cümle iki dilde
de beş demeye devam etti.

## Yapılandırma (`iskele.config.json`)

Üreteci projeye bağlayan tek dosya. Şablon: `assets/iskele.config.example.json`.

```jsonc
{
  "phases": ["F0", "F1"],
  "effort_weights": {"S": 0.75, "M": 1.5, "L": 4.0},
  "status_credit": {"Tamamlandi": 1.0, "Devam": 0.0,
                    "Bloke": 0.0, "Yapilacak": 0.0},
  "workdays_per_month": 21,
  "phase_meta": {
    "F0": {"title": "F0 · Kurulum", "repo": "faz/f0", "stack": "Docker",
           "ms": "M0", "dep": null, "desc": "..."}
  },
  "epic_display": {"F0.1": "F0.1 Proje iskeleti"},
  "static_steps": [{"t": "Mimari onaylandı", "m": "01-...md"}],
  "flow": [{"kind": "phase", "phase": "F0", "mk": "M0",
            "t": "M0 — İskelet", "m": "..."},
           {"kind": "gate", "phase": "F0", "mk": "◆",
            "t": "Kapı M0", "m": "go/no-go"}]
}
```

`phase_meta`/`epic_display`/`flow` **küratörlüdür** (insan yazar); sayılar
çizelgeden gelir. Bu ayrımı koru: prose yapılandırmada, sayı veride.

## Girdi doğrulama — sessiz varsayım yasak

Üreteç bilinmeyen bir değeri sessizce varsayılana düşürmemeli. Sahada görülmüş
üç hata ve kuralı:

| Hata | Sessiz davranış (yanlış) | Doğru davranış |
|---|---|---|
| Geçersiz `Tahmin` (`XL`) | sessizce `M` ağırlık | HATA, yazma |
| Yerelleştirilmiş `Durum` (`Tamamlandı` vs `Tamamlandi`) | sessizce 0 kredi → ilerleme eksik | normalize et + UYARI |
| Faz listesi dışı `Faz` (`F9`) | epik çubuğunda görünür, toplama girmez | **değişmez ihlali** → HATA |

**Değişmez:** `Σ epik eforu == Σ faz eforu`. Iraksama, bir görevin tanımlı fazların
dışına düşmesi demektir ve gösterge sessizce yanlışlanır. Üreteç bunu kontrol eder
ve ihlalde durur.

`progress.py` çıkış kodları: `0` başarılı · `2` doğrulama hatası (rapor yazılmadı)
· `3` değişmez ihlali. `--force` hatayı geçer (önerilmez), `--check` yazmadan özet
basar.

## Haftalık akış

1. Çizelgede `Durum` sütununu güncelle.
2. `python progress.py` çalıştır.
3. Uyarı/hata çıkarsa çizelgeyi düzelt (raporu değil).
4. Raporun elle yazılan bölümlerini (risk, "bu hafta odağı") tazele.
