# Kurtarma — iş bozulduğunda, ve kitin devrettiği rampalar

> **Türkçe asıl.** `skill/iskele/references/recovery.md`'nin Türkçe aslıdır;
> paketlenen sürüm İngilizcedir. Ana metin:
> [`metodoloji.md`](metodoloji.md)

Bir koşu davranmayı bıraktığında oku: söz verilen artifact üretilmedi, görev
kapanmıyor, çizelge ile gerçek uyuşmuyor, niyet kaydı, oturum bulanıklaştı.

Bu skill'in geri kalanı kitin **kurulmasını** anlatır. Bu dosyanın iki işi var
ve ikisi farklı:

1. **Kiti üreten koşu için rampalar** — aşağıdaki `RR-00`…`RR-13`.
2. **Kitin devrettiği rampa kataloğu** — manifestin `09` parçası, şablonu
   `assets/templates/09-kurtarma-rampalari.md`. Adım 3 ve 5, işler **yolunda
   giderken** ne demek olduğunu üretir. Kitte hiçbir şey bozulduğunda ne
   yapılacağını söylemiyordu; o boşluğu planı **uygulayan** herkes miras alır.

İkinci iş, **üretken** bir skill'e özgü olan. Mizan ve ux-mizan rampalarını
kendileri için taşır; iskele hem kendisi için taşır **hem de projeye bir kopya
gönderir** — çünkü proje, onu planlayan oturumdan uzun yaşar.

## Rampanın biçimi

```
DURUM        az önce ne gözledin
İLK HAMLE    her şeyden önce ne yapılır
YASAK        arızayı düzeltmek yerine görünmez kılan kestirme
ÇIKTI        elinde ne kalır -- asla "hallettim" değil
DAYANAK      atlarsan seni yakalayan adım, kırmızı çizgi veya script
```

**Girdiğin rampayı yaz.** Sessizce toparlanan bir kit, hata oranı ölçülemeyen
bir kittir — ilerlemeyi veriden hesaplamanın bütün sebebi buydu.

---

## Bu rampaların var olma sebebi: hata sınıfları

Rampalar çare; bunlar hastalık. Proje kazası değil **model hata modları** —
host'tan host'a tekrar ederler, çünkü hem üretip hem yargılayan bir tarafın,
işe yarar görünme baskısı altındaki davranışıdır.

| Sınıf | Kit kurulurken nasıl görünür | Rampa |
|---|---|---|
| **Üretim tarafında kapatma** | Uç yazıldı, testler geçti, kullanıcı hiçbir şeye ulaşamıyor. Çizelgede "bitti". | RR-03 |
| **İyimser raporlama** | "Kuruldu", "takibe alındı", "doğrulandı" — arkasında artifact yok | RR-01 |
| **Kriter yumuşatma** | Kriter tutmadı, tutana kadar yeniden yazıldı | RR-02 |
| **Sessiz boşluk doldurma** | Kısıt cevaplanmadı, makul bir tanesi varsayıldı, şema onun üstüne kuruldu | RR-10 |
| **Görev enflasyonu** | Kırk görev, çünkü kırk plan gibi duruyor; tahminler "düşünülmüş" görünsün diye şişirilir | RR-06 |
| **Kapsam kayması** | Faz dışına çıkıldı, çünkü sapma ilginçti | RR-07 |
| **Plan esareti** | Niyet değişti, backlog yamandı, alan modeli eski bölünmeyi korudu | RR-08 |
| **Kendi kitini onaylama** | Kabul kriterlerini yazan koşu, karşılanıp karşılanmadığına da karar veriyor | RR-00 |
| **Sahte kesinlik** | Kalibre edilmemiş ağırlıklardan "~78,5 gün", takvim gibi sunulur | RR-12 |
| **Sınıfsız kaçak** | Kaçtı, düzeltme girdi, bir sonraki kapının neye baktığı değişmedi. Çizelge sayar; sayı döngü değildir | RR-13 |
| **Bağlam çürümesi** | Üçüncü saat: görev üretilmeye devam ediyor, modele karşı kontrol edilmiyor | RR-09 |

---

## RR-00 — Kendi kitini yargılamak üzeresin

**DURUM.** Sıradaki iş, aynı koşuda daha önce ürettiğin bir şeyi doğrulamak,
onaylamak veya denetlemek: kendi kabul kriterlerin, kendi kapı listen, kendi
senaryo listen.

**İLK HAMLE.** Geçişi tek satırla ilan et ve iddianın tavanını koy:

```
ROL DEĞİŞİMİ: üretici -> kendi kitimin denetçisi. Hakem: yazar.
Yargı iddiaları öz-beyandır, ölçüm değildir.
```

Sonra ya ayrı bir koşuya devret (adım 7'deki mizan devri **tam bunun için**),
ya da tavanı beyan ederek devam et.

**YASAK.** Senaryo prova listesini kendin yazıp sonucu kapsam saymak —
uydurulmuş makul senaryo, kanıt etiketi takmış kurgudur. İş bitmiş göründüğü
için görevin hakem sınıfını yükseltmek.

**ÇIKTI.** İlan, ve hangi iddiaların öz-beyan olduğu. Burada ayrı bir koşu
mümkün değilse bunu söyle — olmuş gibi ima etme.

**DAYANAK.** *Kendi işini denetlemek* kırmızı çizgisi; adım 7 ("hakem varsayılan
olarak `author`'dır ve öyle kalmalıdır"); adım 5'in senaryo kuralı.

---

## RR-01 — Söz verilen artifact üretilemedi

**DURUM.** openpyxl yok, kabuk yok, alt-ajan yok; ya da
`backlog_to_tracker.py` / `progress.py` hata verdi.

**İLK HAMLE.** İkame etmeden önce teşhis. Eksik araç bir **yetenek** mi
götürüyor yoksa bir **kolaylık** mı? openpyxl yoksa çizelge yoktur, çizelge
yoksa hesaplanan ilerleme de yoktur — adım 6 **olmamıştır**. Alt-ajanın
yokluğu yalnızca tarama hızına mal olur.

**YASAK.** Çizelgeyi üretmek yerine "tablo şöyle görünürdü" yazmak. Bu,
planlayıcının işlediği bir **üretim tarafı iddiasıdır**: altıncı adım yapılmış
*görünür*, ortada takip edilebilir hiçbir şey yoktur.

**ÇIKTI.** Kısıt, kite yazılmış olarak: hangi parça üretilemedi, kit bunun
sonucunda neyi iddia edemez, ve açıkça önerilen alternatif (CSV çizelge, ya da
kurulumu bekleyip backlog'la devam). Ayrıca atlanan parça olarak kaydet —
manifest kuralı zaten "sessizce atlama" diyor.

**DAYANAK.** İşletim varsayımları (*aracı varsaymadan önce kontrol et*),
manifestin "hangi parçayı neden atladığını söyle" kuralı.

---

## RR-02 — Görev kapanmıyor

**DURUM.** İş bitmiş görünüyor ve kabul kriteri tutmuyor — ya da yalnızca
cömert okunursa tutuyor.

**İLK HAMLE.** Hiçbir şeyi **düzenlemeden önce** üçünden hangisinin yanlış
olduğuna karar ver:

1. **İş** — eksik. Bitir.
2. **Görev** — çok büyük; "kısmen bitmiş" durumda, ki backlog kuralı bunu
   imkânsız sayar. Böl, kriteri parçalara devret.
3. **Kriter** — üretim tarafından yazılmış veya yazıldığı hâliyle ölçülemez.
   **Tüketim tarafına** çevir ve revizyonu kaydet: sonucu gördükten sonra
   değişen kriter artık bir önkayıt değildir — ve adım 7 bu backlog'u mizan'a
   tam olarak önkayıt seti diye devretmişti.

**YASAK.** Yapılana uysun diye kriteri gevşetmek. Kriter "kullanıcı ulaşır"
derken "uç veriyi döndürüyor" ile kapatmak. Bağımlı görevi açmak için çizelgede
"bitti" işaretlemek.

**ÇIKTI.** Ya kriteri fiilen çalıştırılmış kapanmış bir görev, ya bir bölünme,
ya da gerekçesiyle tarihli bir kriter revizyonu. Üçü de ilerlemedir; yalnızca
ilki "bitti"dir.

**DAYANAK.** Adım 4 (atomik görev, tüketim tarafı kriter), DoD'nin *kabul
kriteri fiilen çalıştırıldı* maddesi, *mutlu yol doğrulaması* kırmızı çizgisi.

---

## RR-03 — Çizelge ile gerçek uyuşmuyor

**DURUM.** Bir yetenek "bitti" işaretli ve ulaşılamıyor. Ya da var olmayan bir
yüzey için test var.

**İLK HAMLE.** Backlog kurallarının doğduğu arıza budur ve **asla tek bir
görevin hatası değildir**: boşluk görevlerin *arasında* yaşar, orada hiçbir
görevin kendi kontrol listesi onu göremez. O yüzden hatayı değil **çifti** ara.
Kapanmış görevin **tüketen ikizini** bul — okuma yüzeyini getiren görev. Böyle
bir görev yoksa eksik olan yapı değil **plandır**.

**YASAK.** Kapanmış görevin içinde sessizce düzeltip devam etmek. Bu, tek
örneği onarır, sınıfı bırakır: bu kuralı doğuran projede aynı boşluk **dört
kez** tekrarladı ve dördü de plandan çıkmadı.

**ÇIKTI.** Eksik okuma yüzeyi için yeni backlog görevi, üreten görevin kutusuna
yazılan ID (`→ F3-FE-03`), ve risk dosyasına sınıfın notu. Sonra aynı fazın
diğer kapanmış görevlerini **aynı biçim için tara** — bir örneği tesadüfen
bulunduysa tarama hiç yapılmamış demektir.

**DAYANAK.** Adım 4 (üreten görev tüketen ikizini adlandırır), DoD'nin okuma
yüzeyi maddesi.

---

## RR-04 — Geçilmiş bir kapı artık tutmuyor

**DURUM.** Son kapıda çalışan bir şey artık çalışmıyor ve mevcut fazdaki
hiçbir görev onunla ilgili değildi.

**İLK HAMLE.** Önce eski hâle dön, sonra teşhis et — incelenmekte olan bir
regresyon, hâlâ yayında olan bir regresyondur. Sonra hata ayıklama sorusunu
değil **kapının kendi sorusunu** sor: *kimin garantisi bozuldu, hangi çift
bozdu?* Adım 5'te adlandırılan iki kırılgan biçim: **türetilmiş sinyal** (bir
yokluktan hesaplanan her şey — "3 gündür dokunulmadı", "atanmamış" — yeni bir
durum var olduğu anda anlamı sessizce değişir) ve **çağrı yeri çağrı yeri
uygulanan garanti** (beş yerde doğru, altıncı toplu yüzeyde toptan delinir).

**YASAK.** Yeşil test paketini karşı kanıt saymak. Testler özellik başına
yazılır; parçalar hakkında konuşur, **çift** hakkında susarlar — senaryo
provasının ayrı bir seviye olmasının sebebi tam olarak budur.

**ÇIKTI.** Geri alınmış durum, fazın prova listesine eklenen yeni senaryo
(**bir sonraki bulgudan önce** yazılan, bunun ardından değil) ve gerçek
düzeltme için bir görev. Çift, prova listesinde olması gereken bir çiftse bunu
söyle: bu, **plan hakkında** bir bulgudur ve düzeltmeden değerlidir.

**DAYANAK.** Adım 5 senaryo provası, adım 3 (kapılar), *faz atlama* kırmızı
çizgisi.

---

## RR-05 — Planda olmayan bir bulgu

**DURUM.** İş sırasında gerçek bir sorun görüyorsun — ölü kod, eksik kontrol,
tutulmamış bir söz — ve hiçbir görev onu kapsamıyor.

**İLK HAMLE.** Düzeltme yok, görevi genişletme yok. **Asgari kaydı** üret:
hangi dosya, hangi davranış, neyin gösterebileceği. Sonra yönlendir:

- **Gösterilebiliyor** → kabul kriteri olan bir backlog görevi, bir faza
  yerleştirilmiş. Plana girer; mevcut göreve girmez.
- **Gösterilemiyor** → risk dosyasında, neden sabitlenemediği yazılarak
  kapanır. Kapanmış bir gözlem kayıttır; backlog'daki sabitlenmemiş bir endişe,
  sonraki okuyucunun işten ayıramayacağı gürültüdür.

**YASAK.** Küçük diye sessizce düzeltmek. Her sessiz düzeltme, tüm iddiası
"ilerleme veriden hesaplanır" olan bir planda takip edilmeyen bir değişikliktir.

**ÇIKTI.** Bir görev ya da yazılı bir kapanış — ve her hâlükârda mevcut görev
kendi kriteriyle, değişmemiş hâlde kapanır.

**DAYANAK.** Adım 3'ün açık kapsam-dışı listeleri, tıkanma ve negatif bulgunun
adresi olarak `06-riskler-ve-kararlar`.

---

## RR-06 — Turlar tek görevde birikiyor

**DURUM.** Aynı görev üç veya daha fazla kez geri döndü; ya da backlog büyürken
hiçbir şey kapanmıyor.

**İLK HAMLE.** **Görevi çalışmayı bırak ve bir seviye yukarı çık.** Tekrar eden
turlardan sonra kapanmayan görev genellikle zor bir görev değildir; **yanlış
bölünmenin üstünde duran** bir görevdir. Adım 2'nin sorusunu yeniden oku —
burada ayrı yaşam döngüsü olan iki şey birbirine mi karışıyor? — ve faz
sınırının veriyi kapının yanlış tarafına koyup koymadığına bak.

**YASAK.** Aynı çerçeveyle dördüncü deneme. Pano hareket etsin diye görev
eklemek. Tur sayısı makul görünsün diye tahmin şişirmek.

**ÇIKTI.** Yazılı bir teşhis — model, faz sınırı ya da görev — ve *yalnızca*
teşhis. Bu rampada kod yok. Sorun modeldeyse ADR kaydı revizyonu alır ve
etkilenen görevler yeniden türetilir; o RR-08'dir.

**DAYANAK.** Adım 2 (ayrım bulunmadan şema yazma), adım 3 (sonraki fazın verisi
öncekinden gelir).

---

## RR-07 — İş faz dışına çıktı

**DURUM.** Yapılan şey bu fazın kapsamında değil, ya da açık kapsam-dışı
listesinde.

**İLK HAMLE.** Sapmayı listele: hangi değişiklikler dışarıdaydı ve her biri
gerekli miydi yoksa yalnızca yakın mıydı. Sonra ait oldukları faza görev olarak
park et.

**YASAK.** Sapmayı mevcut görevin diff'ine katmak. İşine gelmediği ortaya
çıktığı için kapsam-dışı satırını silmek — o satır kapsam kaymasını önleyen
şeydir, sonradan düzenlenmesi kaymanın kendisidir.

**ÇIKTI.** Karar için geri verilen park listesi: faz sınırı taşınsın mı, yoksa
iş parkta mı kalsın. Bu, kurucunun değil **sahibinin** kararıdır.

**DAYANAK.** Adım 3 (faz başına açık kapsam-dışı), *kapsam kayması* kırmızı
çizgisi.

---

## RR-08 — Niyet kaydı

**DURUM.** Sahip, projenin ne için olduğunu değiştiriyor ya da adım 1'de
cevaplanmış bir kısıt yanlış çıkıyor — backlog var olduktan **sonra**.

**İLK HAMLE.** **Döngünün kendi sırasıyla** güncelle: kısıtlar → alan modeli →
fazlar → backlog → çizelge. Sonra bir **delta listesi** üret: hangi görevler
değişti, hangileri düştü, hangileri yeni.

**YASAK.** Yalnız backlog'u yamamak. Değişmemiş bir modelden yeniden türetilen
backlog eski bölünmeyi sessizce miras alır ve adım 2 yanlış bölünmenin ne
yaptığını zaten söylüyor: iş ortasında çöker ve her faza yeniden çalışma
yükler. Ayrıca kapanmış görevleri hep böyle yazılmış gibi göstermek için
düzenleme — kapanmış backlog, ADR kaydıyla aynı sebeple ekleme-yalnız.

**ÇIKTI.** Niyet değişikliği için tarihli bir ADR, delta listesi ve
`backlog_to_tracker.py`'nin yeniden koşturulması — çizelge, planın hatırasına
değil planın kendisine uysun diye.

**DAYANAK.** Yedi adımın sırası ("sırayı bozma"), ADR ve kapanmış backlog için
ekleme-yalnız kuralı.

---

## RR-09 — Oturum bulanıklaştı

**DURUM.** Uzun koşu. Görev üretilmeye devam ediyor ama artık modele karşı
kontrol edilmiyor; hangi kararların kaydedildiğini hatırlamıyorsun.

**İLK HAMLE.** Durumu dosyalara yaz ve kes. Bu skill'de hamle zaten var —
**devir, bağlam kesme noktasıdır**. Backlog'u boşalt, ADR indeksini yeniden
üret, kapanmış fazları arşivle, `progress.py`'yi koştur, devir notunu yaz.
Sonraki faz taze bir oturumda başlar.

**YASAK.** Faz neredeyse kapandı diye devam etmek — son görevler koşunun en
kötü koşullarında yazılır ve ilk koşullarında yazılmış gibi okunur. Kararı
ADR'yi açmak yerine hatırlamak.

**ÇIKTI.** Yazılmış kit ve açık bir sınır beyanı. Beklentiyi de dürüst tut:
okuma yüzeyini küçültmek **yön** olarak gerçek bir kazanç, bayt sayısının ima
ettiği token kazancı değil.

**DAYANAK.** Adım 7 (devir bir bağlam kesme noktasıdır), okuma yüzeyi bölümü.

---

## RR-10 — Belirsizlik, ya da plan ile kod çelişiyor

**DURUM.** Bir kısıtın iki okuması da savunulabilir; ya da backlog, ADR kaydı ve
uygulama neyin kararlaştırıldığı konusunda ayrışıyor.

**İLK HAMLE.** Varsayma — ve **boş elle de sorma**.

```
DURUM:      <belirsiz olan, tek cümle>
SEÇENEK:    A <...>  B <...>
ÖNERİM:     A
GEREKÇE:    <kısıta veya alan modeline bağlı, zevke değil>
YANILIRSAM: <A'yı seçip yanılmanın bedeli>
```

Öneri bir kelimeyle reddedilebilir; çıplak soru, plan için gelen kişinin
sırtına işi geri yükler. Karar yine onundur — **öneri onay değildir, cevapsız
öneri rıza değildir.** Adım 1'in kuralı sormaya da geçerlidir: tek tur, en
fazla üç soru.

Plan-kod çelişkisi ayrıca **bir bulgudur**: ekip, sahip olmadığı bir sistemin
tarifini okumaktadır ve bütün alt tahminler onun üstünde durur.

**YASAK.** Planı derli toplu gösteren okumayı seçmek. Kendi çıkarımını
kararlaşmış kısıt diye kaydetmek — belgelenmemiş boşluk her zaman karar
verilmiş sınırdan kötüdür, **uydurulmuş** sınır ikisinden de kötüdür.

**ÇIKTI.** ADR olarak kaydedilmiş bir karar; ya da sahibin açık bıraktığı bir
soruda, varsayım olarak işaretlenmiş bir varsayılan ve ona dayanan görevlerin
adları.

**DAYANAK.** Adım 1 (sor, varsayma), adım 5'in sınır kuralı, *sessiz varsayım*
kırmızı çizgisi.

---

## RR-11 — Yayına girmiş işi geri alma

**DURUM.** Bir fazın çıktısı geri çıkmak zorunda — kapı hatayla geçildi ya da
yaklaşım yanlıştı.

**İLK HAMLE.** İleri sar, geri değil: geri alma, işin silinmesi değil **yeni ve
kayıtlı bir olaydır**. Görevler kanıtlarıyla kapalı kalır; kaldırmayı yeni bir
görev taşır, gerekçeyi bir ADR taşır.

**YASAK.** Görevleri, kriterlerini ya da yaklaşımı savunan ADR'yi silmek. ADR
kaydı, altı ay sonrası için yazılan tek belgedir ve orada bulunacak en yararlı
karar türü, **geri alınmış** olandır.

**ÇIKTI.** Kaldırma görevi, tetikleyicisiyle birlikte geri alma ADR'si ve
yeniden hesaplanmış ilerleme. İlerlemenin **düşmesi** doğru bir çıktıdır;
yalnızca yükselen bir yüzde, duygular hakkında bir rapordur.

**DAYANAK.** Ekleme-yalnız ADR kaydı, adım 6 (ilerleme çizelgeden hesaplanır,
iddia edilmez).

---

## RR-12 — Tahmin tutmadı

**DURUM.** Faz aştı ya da efor ağırlıklı sayı olanla örtüşmeyi bıraktı.

**İLK HAMLE.** Duyguyla değil **veriyle** yeniden kalibre et. S/M/L ağırlıkları
yazarın seçimiydi ve kalibre değildi; kapanan ilk faz, bu projenin sahip olduğu
ilk gerçek hız verisidir. **Tek** şeyi değiştir — ağırlıkları — ve yeniden
türet; ağırlık ile kapsamı birlikte değiştirmek tek sayı ve sıfır atıf üretir.

**YASAK.** Toplam olması gereken yere insin diye kalan görevleri elle yeniden
tahmin etmek. Dayanağın değiştiğini söylemeden yeni sayıyı sunmak. Ondalığı
hak edilmiş gibi "~78,5 gün" raporlamak.

**ÇIKTI.** Yeni ağırlıklar, hangi fazda kalibre edildikleri ve o fazın ötesi
için kalibre olmadığını söyleyen yeniden ifade edilmiş bir tahmin.

**DAYANAK.** *Sahte kesinlik* ve *uydurma sayı* kırmızı çizgileri, adım 6 (efor
ağırlıklı ilerleme).

---

## RR-13 — Kapıdan bir şey kaçtı, plan kıpırdamadı

**DURUM.** Kapı kapandıktan sonra bir kusur ortaya çıktı — kullanıcı çarptı,
üretimde patladı, bir sonraki faz üstüne bastı — ve durduğu zemin bu fazın
kriterlerinin kapsadığı zemin. Sessiz hâli de aynı rampayı tetikler: "bir
dahaki sefere DoD'ye eklemeli" diye yazılmış, hiçbir listeye girmemiş bir ders.

**İLK HAMLE.** Teşhis etmeden **önce** çizelgedeki `Kacan` hücresine yaz.
Çekim, hatayı düzeltip devam etmektir; düzeltme ürüne, kaçak plana aittir ve
ikisinden yalnızca birincisi normalde bir yere yazılır.

Sonra tek soruyu `KacanSinifi` hücresinde yazılı olarak cevapla: **bunu hangi
kontrol yakalamalıydı?**

- **Kontrol var ve ateşlemedi.** Adını yaz — bir DoD maddesi, bir go/no-go
  satırı, bir kabul kriteri, bir prova senaryosu. O zaman bulgu bu faz
  hakkındadır, kit hakkında değil: madde atlandı, kapsam dışı bırakıldı ya da
  koşulup yanlış okundu. *"Bu fazda aynı-adımda-iki-kişi senaryosunu hiç prova
  etmedik"* gerçek bir cevaptır ve kimsenin ihtiyaç duymadığı yeni bir kuraldan
  iyidir.
- **Hiçbir kontrol kapsamıyor.** O zaman artık kapsayanı yaz — bir sonraki
  kapının sorabileceği bir soru olarak, bu hatanın tarifi olarak değil. *"Aynı
  adımda iki kişi çalışabilir mi?"* bir senaryodur; *"eşzamanlılığı düşünmek
  lazım"* bir ruh hâlidir. Yeni senaryolar **açılan** fazın listesine girer
  (adım 5), kapanmış olana geriye dönük yazılmaz.

**YASAK.** Kaçağı yalnız düzeltmeyle kapatmak. `Kacan`'ı doldurup
`KacanSinifi`'ni boş bırakmak — sayı, bu rampa tarafından tüketilmek için var,
seyredilmek için değil. Yeni senaryoyu, onu kaçıran fazın içine geriye dönük
yazmak: kaçak, o fazın kapsam iddiasının yanlış olduğunun kanıtıdır ve bunu
açıkça söylemek dürüst hamledir.

**ÇIKTI.** Yanında sınıfıyla kaydedilmiş bir kaçak, ve sınıf yeniyse — şu an
açık olan faza eklenmiş DoD maddesi, go/no-go satırı ya da senaryo.

**NEDEN BURADA HER YERDEN ÖNEMLİ.** Kitin diğer bütün ölçüleri planın
içinden gelir: plana uyulup uyulmadığına plan karar verir. Bu tek sayı
dışarıdan gelir; çizelgenin onu "içeriden manipüle edilemeyen tek ölçü" diye
adlandırmasının sebebi bu. Adım 5'teki iki senaryo sınıfı da birer kaçaktan
doğdu — tüketen-ikiz boşluğu dört kez, bileşim kusuru beş kez tesadüfen fark
edildi, ve ancak ondan sonra sınıf olarak yazıldı. Bu rampanın hem kanıtı hem
iddianamesi budur.

**DAYANAK.** Çizelgenin `Kacan` / `KacanSinifi` çifti, adım 5 (DoD, go/no-go,
senaryo provası), RR-03 (tüketen-ikiz boşluğu), `SenaryoProvali` /
`SenaryoTesadufi` oranı — provalı, tesadüfiyi yener; kaçak ise o oranın
göremediği üçüncü kategoridir.

---

## Faz kapanışı — süreç çizelgesi

Her kapıda, go/no-go'nun yanında doldurulur. Ekibi notlamaz; **planın nereden
sızdırdığını** bulur. Yüksek sayı kötü değildir, gizlenen sayı kötüdür.

| Ölçüt | Değer | Okuma |
|---|---|---|
| Faz açıldıktan sonraki backlog revizyonu | | Yüksek → faz, girdileri hazır olmadan açıldı |
| Yeniden çalışma turu | | Tek epic'te toplanıyorsa şüphe kişide değil **bölünmede** (RR-06) |
| İşten sonra yeniden yazılan kriter | | Her biri, önkayıt olmaktan çıkmış bir kriter. Sıfır ulaşılabilir; incelenmemiş olan değil. |
| Tüketen-ikiz boşluğu | | Kaç tane — **ve kaçı kapıda, kaçı tesadüfen** bulundu. İkinci sayı asıl olan. |
| Senaryo bulgusu: provalı / tesadüfi | / | Hiç bulgu vermeyen liste temiz proje değil, **çalıştırılmamış listedir** |
| Faz dışına çıkma | | RR-07 kaç kez |
| Kullanılan rampalar | | Hangi `RR-nn`. Hiçbiri kullanılmadıysa ya kusursuzdu ya fark edilmedi. |
| **Kaçan** | | Kapıdan sonra bulunan, bu fazın kriterlerinin kapsadığı hata. Süreç dışından gelen tek sayı ve içeriden manipüle edilemeyen tek ölçü. |
| **Kaçağın sınıfı** | | Her kaçak için: ateşlemesi gereken kontrol, ya da bu kaçak sayesinde artık var olan kontrol (RR-13). Yanında sınıf olmayan kaçak plana hiçbir şey öğretmemiştir. |
| **Bakılan / kırılan çift** | / | Çizelgenin `Cift` sekmesinden: kapı kaç özellik × garanti çiftini gerçekten geri birleştirdi, kaçı kırıldı. Sıfır çiftli faz pası koşmamıştır — backlog'u atomize etmek tam olarak bu sınıfı yok eder, yani planda başka hiçbir şey onu bulamaz. |

**Çıkarım:** 1–2 cümle. "Faz iyi geçti" değil: sonraki fazda ne değişecek ve
**hangi sayı** bunu söylüyor.

**Çizelgede bir yeri var.** `backlog_to_tracker.py` faz başına bir satırlık
`Skorkart` sekmesi üretir; `progress.py` onu okuyup ilerleme çubuklarının
yanında basar (`GEN:SKORKART`). Böylece skorkart, kimsenin bir daha açmadığı bir
belgede değil, işin takip edildiği yerde doldurulur. Üreteç, onu yalancı yapacak
iki hatayı reddeder: sekme yoksa *tutulmuyor* yazar, sıfır yazmaz; ve
`IkizKapida > IkizBoslugu` bir doğrulama hatasıdır — kümesinden büyük bir alt
küme göstergeyi bozmakla kalmaz, ters çevirir. Şema: [`takip.md`](takip.md).

Çizelge de bir iddiadır. İşi yapan doldurduğunda hakem `author`'dır ve
öz-beyandır. Söyle; adım 7'nin çizelgenin durum sütunu için kurduğu cümle
burada da geçerlidir.

---

## Rampaları kitle birlikte göndermek

`09` parçası (`09-kurtarma-rampalari.md`) projenin kendi kopyasını tuttuğu yer.
Adım 5'te, kalite kapılarının yanında üretilir — kapılar "bitti"nin ne demek
olduğunu söyler, rampalar bitmediğinde ne yapılacağını.

- **Uyarla, yapıştırma.** Burada oluşamayacak rampaları çıkar (henüz yayına
  giren faz yoksa RR-11 yok), bu alanın zorladıklarını ekle. Hangilerini
  çıkardığını dosyaya yaz.
- **Her rampa kanıtını adlandırır.** Çıktısı olmayan rampa tavsiyedir; kit
  tavsiye dokümanı değildir.
- **Katalog, uygulayan içindir** — insan ya da ajan. Projenin dilinde yaz ve
  her rampaya bir kod ver: kod, rampayı commit mesajında veya stand-up'ta
  **alıntılanabilir** yapan şeydir (`RR-05: park edildi → F2-BE-07`); paragrafı
  kimse alıntılamaz.
