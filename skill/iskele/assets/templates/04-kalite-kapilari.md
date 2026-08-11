# Kalite Kapıları

İki seviye: her **görev** için Tamamlandı Tanımı (DoD), her **faz** için go/no-go.
Kutu tam dolmadan ilerleme yok.

## 1. Tamamlandı Tanımı (DoD) — her görev

- [ ] Kabul kriteri **fiilen çalıştırıldı** (endpoint çağrıldı / ekran açıldı), göz kararı değil.
- [ ] Değişiklik ana dala girdi.
- [ ] Davranış değiştiyse **otomatik test** kabul kriterini doğruluyor.
- [ ] Yeni arayüz ise yetki kontrolü var (yetkisiz istek reddediliyor).
- [ ] Veri değiştiren işlemse denetim izi (audit) yazılıyor.
- [ ] `tracker.xlsx`'te durum güncellendi.
- [ ] Tıkanma/negatif bulgu `06-riskler-ve-kararlar.md`'ye yazıldı.

**"mış gibi" testi:** Yorum satırı, log mesajı veya buton *varlığı* davranış kanıtı
değildir. Kabul kriterini gerçek veriyle bir kez daha çalıştırmadan done deme.

## 2. Go/No-Go — faz geçişi

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
