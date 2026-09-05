# Kalite Kapıları

İki seviye: her **görev** için Tamamlandı Tanımı (DoD), her **faz** için go/no-go.
Kutu tam dolmadan ilerleme yok.

## 1. Tamamlandı Tanımı (DoD) — her görev

- [ ] Kabul kriteri **fiilen çalıştırıldı** (endpoint çağrıldı / ekran açıldı), göz kararı değil.
- [ ] Değişiklik ana dala girdi.
- [ ] Davranış değiştiyse **otomatik test** kabul kriterini doğruluyor.
- [ ] Yeni arayüz ise yetki kontrolü var (yetkisiz istek reddediliyor).
- [ ] Veri değiştiren işlemse denetim izi (audit) yazılıyor.
- [ ] **Kullanıcının göreceği bir bilgi üretiyorsa: o bilgiyi okuyabileceği bir yüzey
      var ve fiilen açıldı** — ya da aynı fazda o yüzeyi getiren görev listede ve bu
      görevin kutusunda ID'si yazılı. *Üretim tarafı bir kriteri tek başına karşılamaz.*
- [ ] `tracker.xlsx`'te durum güncellendi.
- [ ] Tıkanma/negatif bulgu `06-riskler-ve-kararlar.md`'ye yazıldı.

**"üretiyor" tuzağı:** *"Sistem X üretiyor"* ile *"kullanıcı X'e ulaşıyor"* farklı iki
cümledir; ilki ikincisini ima etmez. Uç yazıldı, tablo doldu, olay yayımlandı — hiçbiri
kullanıcıya ulaşan bir yetenek demek değildir. Kriteri kullanıcının **yapabildiği** şeyle
yaz. Bu boşluk görevlerin *arasında* yaşadığı için tek bir görevin kontrol listesi onu
göremez; bu yüzden DoD'de ayrı madde.

**"mış gibi" testi:** Yorum satırı, log mesajı veya buton *varlığı* davranış kanıtı
değildir. Kabul kriterini gerçek veriyle bir kez daha çalıştırmadan done deme.

## 2. Go/No-Go — faz geçişi

**Her kapıda, listedeki maddelerden önce: çift pası.** DoD ve go/no-go
*yazılmış olanı* denetler. Yalnızca **iki özellik aynı anda etkinken** var olan
kusuru ikisi de göremez — çünkü backlog'u atomize etmek tam olarak o kusuru yok
eden işlemdir. Bu yüzden kapıda bilerek geri birleştirilir: bu fazın her yeni
özelliği için, dokunabildiği mevcut garantiler; ve her çift için tek soru —
*bu garanti, o özellik etkinken hâlâ geçerli mi?*

En kırılgan iki sınıf: bir **yokluktan** hesaplanan sinyaller ("3 gündür
dokunulmadı", "atanmamış") ve tek tek çağrı yerinde uygulanan garantiler (beş
ekranda doğru uygulanan kural, altıncı toplu yüzeyle toptan geçersizleşir).
**Sıra da sayılır:** bazı çiftler yalnız tek yönde güvenlidir ve o yön bulgunun
parçasıdır. Yeşil test paketi burada karşı kanıt değildir.

- [ ] Bu fazın çiftleri çizelgenin `Cift` sekmesine yazıldı.
- [ ] `bakilmadi` kalan çift yok — ya da kalanı kapıda **açıkça** kabul edildi
      ve gerekçesi yazıldı. (Listelenip sınanmamış çift, kimsenin listelemediği
      çift kadar korur; bu yüzden rapor iki sayıyı ayrı basar.)
- [ ] `kiriliyor` çıkan her çift ya kapatıldı ya da bir görev olarak backlog'a
      girdi.


### M0 — F0 → F1
- [ ] Altyapı servisleri healthy.
- [ ] **Dikey dilim:** tek akış DB'den ekrana çalışıyor.
- [ ] [projeye özgü maddeler]

> Dikey dilim eksikse katmanlar gerçekten bağlı değildir — F1'e geçme.

### M1 — F1 → F2
- [ ] Alan modelinin **kritik değişmezi** doğrulandı (ör. donma/izolasyon testi).
- [ ] Çekirdek akış uçtan uca çalışıyor.
- [ ] Yetki kontrolü zorlanıyor.

### M2 — Yayına alma öncesi
- [ ] Güvenlik listesi geçiyor.
- [ ] Yük hedefi karşılanıyor.
- [ ] Yedekleme/geri yükleme tatbikatı yapıldı.

## 3. Güvenlik listesi

- [ ] Her endpoint yetkiyi zorluyor (yatay/dikey yetki aşımı yok).
- [ ] Girdi doğrulama ve parametreli sorgular.
- [ ] Dosya yükleme: tip/boyut doğrulaması.
- [ ] Secret'lar repoda değil.
- [ ] Hata mesajları iç detay sızdırmıyor.
