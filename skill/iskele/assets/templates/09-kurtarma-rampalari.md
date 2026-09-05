# Kurtarma Rampaları

`04-kalite-kapilari.md` işler **yolundayken** ne demek olduğunu söyler. Bu dosya
işler **bozulduğunda** ne yapılacağını söyler. İkisi birlikte çalışır: kapı
"bitti mi?" diye sorar, rampa "bitmiyorsa ne yapacağım?" sorusuna cevap verir.

**Rampa çağrılabilir olsun diye kodludur.** Commit mesajında, stand-up'ta,
görev notunda kodu geçer: `RR-05: park edildi → F2-BE-07`. Kod geçmiyorsa
rampa kullanılmamıştır; paragraf kimse alıntılamaz.

**Kural:** Rampaya girdiğini **yaz**. Sessizce toparlanan bir iş, hata oranı
ölçülemeyen bir iştir — ilerlemeyi veriden hesaplamanın tüm sebebi buydu.

---

## Rampa tablosu

| Kod | Durum | Temel kural | Çıktı |
|---|---|---|---|
| **RR-00** | Kendi işini denetliyorsun | Hakem = yazar; ilan et, yargı iddiasını kanıt sayma | İlan + hangi iddiaların öz-beyan olduğu |
| **RR-01** | Söz verilen artifact üretilemedi | Eksik araç yetenek mi kolaylık mı; düzyazıyı artifact yerine koyma | Kısıt beyanı + atlanan parça kaydı |
| **RR-02** | Görev kapanmıyor | Önce karar: iş mi, görev mi, kriter mi — **kriteri gevşetme** | Kapanan görev / bölünme / tarihli kriter revizyonu |
| **RR-03** | Çizelge ile gerçek uyuşmuyor | Boşluk görevlerin *arasında*; tek örneği değil sınıfı ara | Okuma yüzeyi görevi + aynı fazda tarama |
| **RR-04** | Geçilmiş kapı artık tutmuyor | Önce eski hâle dön; sonra "kimin garantisi, hangi çift?" | Yeni senaryo (bulgudan **önce** yazılan) + düzeltme görevi |
| **RR-05** | Planda olmayan bulgu | Düzeltme değil **asgari kayıt**; ya göreve dönüşür ya gerekçeyle kapanır | Görev veya yazılı kapanış |
| **RR-06** | Tur sınırı aşıldı | DUR, bir seviye yukarı çık: model mi, faz sınırı mı, görev mi | Yalnızca teşhis — kod yok |
| **RR-07** | Faz dışına çıkıldı | Sapma listesi; kapsam dışı satırını **silme** | Park listesi + sahibinin kararı |
| **RR-08** | Niyet değişti | Sırayla güncelle: kısıt → model → faz → backlog → çizelge | ADR + delta listesi + yeniden üretilen tracker |
| **RR-09** | Bağlam bulanıklaştı | Kit hafızadır, sohbet değil; dosyaya yaz ve kes | Devir notu + arşiv + `progress.py` |
| **RR-10** | Belirsizlik / plan-kod çelişkisi | **Varsayma, boş elle de sorma**: öneri + gerekçe | ADR veya işaretlenmiş varsayım |
| **RR-11** | Yayına girmiş işi geri alma | İleri sar, silme: kayıt kalır, kaldırma yeni görevdir | Kaldırma görevi + ADR + düşen ilerleme yüzdesi |
| **RR-12** | Tahmin tutmadı | Veriden yeniden kalibre et; **tek** şeyi değiştir | Yeni ağırlıklar + hangi fazda kalibre edildiği |
| **RR-13** | Kapıdan bir şey kaçtı, plan kıpırdamadı | Önce `Kacan`'a yaz, sonra teşhis et; "hangi kontrol bunu yakalamalıydı?" | `KacanSinifi`: susan kontrolün adı ya da artık var olan kontrol |

---

## Üç rampa uzun hâliyle

Kalanlar tablodaki tek satırla yürür; bu üçü en sık yanlış uygulananlar.

### RR-02 — Görev kapanmıyor

Sırayla sor, **düzenlemeden önce**:

1. **İş** eksik mi? → Bitir.
2. **Görev** çok mu büyük? → Bir görev "kısmen bitmiş" olamaz; böl, kriteri
   bölünmüş parçalara devret.
3. **Kriter** mi yanlış? → Üretim tarafından yazılmışsa **tüketim tarafına**
   çevir ve revizyonu tarihiyle kaydet.

**Yasak:** Yapılana uysun diye kriteri gevşetmek. Bağımlı görev açılsın diye
çizelgede "bitti" işaretlemek. Kriter, iş başlamadan yazılmış bir çürütme
koşuludur; sonuçtan sonra değişen kriter artık önkayıt değildir.

### RR-03 — Çizelge ile gerçek uyuşmuyor

Bir yetenek "bitti" görünüyor ve kullanıcı ona ulaşamıyor. Bu **tek bir görevin
hatası değildir**: boşluk görevlerin *arasında* yaşar, o yüzden hiçbir görevin
kendi kontrol listesi onu göremez.

- Kapanan görevin **tüketen ikizini** ara: okuma yüzeyini getiren görev.
- Yoksa eksik olan kod değil **plandır** — yeni görev açılır, üreten görevin
  kutusuna ID'si yazılır (`→ F3-FE-03`).
- Sonra **aynı fazdaki diğer kapanmış görevleri tara.** Bir örneği tesadüfen
  bulunduysa tarama hiç yapılmamış demektir.

### RR-10 — Belirsizlik: boş elle soru sorulmaz

```
DURUM:    <belirsiz olan, tek cümle>
SEÇENEK:  A <...>  B <...>
ÖNERİM:   A
GEREKÇE:  <kısıta veya alan modeline bağlı — zevke değil>
YANILIRSAM: <A'yı seçip yanılmanın bedeli>
```

Öneri bir kelimeyle reddedilebilir; çıplak soru işi soranın sırtına geri
yükler. **Karar yine sahibinindir: öneri onay değildir, cevapsız öneri rıza
değildir.** Soru turu tektir, en fazla üç soru.

Plan ile kodun çelişmesi ayrıca **bulgudur** — ekip sahip olmadığı bir sistemin
tarifini okuyordur ve bütün tahminler onun üstünde durmaktadır.

---

## Faz kapanışı — süreç çizelgesi

Her kapıda, go/no-go'nun yanında doldurulur. Amaç ekibi notlamak değil,
**planın nereden sızdırdığını** bulmak. Yüksek sayı kötü değildir; gizlenen
sayı kötüdür.

| Ölçüt | Değer | Okuma |
|---|---|---|
| Faz açıldıktan sonraki backlog revizyonu | | Yüksek → faz, girdileri hazır olmadan açıldı |
| Yeniden çalışma turu | | Tek epic'te toplanıyorsa şüphe kişide değil **bölünmede** (RR-06) |
| İşten sonra yeniden yazılan kriter | | Her biri, önkayıt olmaktan çıkmış bir kriterdir |
| Tüketen-ikiz boşluğu | | Kaç tane — **ve kaçı kapıda, kaçı tesadüfen** bulundu. İkinci sayı asıl olan. |
| Senaryo bulgusu: provalı / tesadüfi | / | Hiç bulgu vermeyen liste temiz proje değil, **çalıştırılmamış listedir** |
| Faz dışına çıkma | | RR-07 kaç kez |
| Kullanılan rampalar | | Hangi `RR-nn`. Hiçbiri kullanılmadıysa ya kusursuzdu ya fark edilmedi. |
| **Kaçan** | | Kapıdan sonra bulunan, bu fazın kriterlerinin kapsadığı hata. Dışarıdan gelen tek sayı — içeriden manipüle edilemeyen tek ölçü. |
| **Kaçağın sınıfı** | | Her kaçak için: ateşlemesi gereken kontrol, ya da bu kaçak sayesinde artık var olan kontrol (RR-13). Yanında sınıf olmayan kaçak plana hiçbir şey öğretmemiştir. |

**Çıkarım:** 1–2 cümle. "Faz iyi geçti" değil: bir sonraki fazda ne
değişecek ve **hangi sayı** bunu söylüyor.

> Bu çizelgeyi işi yapan doldurur; yani **hakem = yazar**, öz-beyandır.
> `tracker.xlsx`'in durum sütunu için geçerli olan cümle burada da geçerli.
>
> Doldurma yeri: `tracker.xlsx` → **`Skorkart`** sekmesi, faz başına bir satır.
> `python progress.py` bunu rapora basar. Boş bırakılan hücre "sıfır" değil
> "doldurulmadı" sayılır; `IkizKapida`, `IkizBoslugu`'nun alt kümesidir.

---

## Uyarlama notu

*(Kit üretilirken doldurulur, sonra bu satır silinir.)*

- **Çıkarılan rampalar:** [hangileri, neden — ör. "RR-11: henüz yayına giren
  faz yok"]
- **Eklenen rampalar:** [bu alana özgü olanlar]
- Her rampa bir **çıktı** adlandırır. Çıktısı olmayan rampa tavsiyedir; kit
  tavsiye dokümanı değildir.
