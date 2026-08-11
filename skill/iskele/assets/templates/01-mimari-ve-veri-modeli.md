# Mimari ve Veri Modeli

## 1. Kısıtlar (mimariyi bunlar belirledi)

| Konu | Kısıt | Kaynak |
|---|---|---|
| Dağıtım | [on-prem / bulut] | [kullanıcı beyanı] |
| Ölçek & kimlik | [kaç kullanıcı, SSO] | [...] |
| Sert kısıtlar | [mevcut yığın, mevzuat, tarih] | [...] |

> Her teknoloji seçimi bir kısıta bağlanmalı. Bağlanamayan seçim *tercihtir* — öyle işaretle.

## 2. Alan modeli — çekirdek ayrım

**Ayrım:** [A] ile [B] farklı yaşam döngüsüne sahiptir.
- **[A]** — [ne, ne sıklıkla değişir, kim değiştirir]
- **[B]** — [ne, ne sıklıkla üretilir, kim üretir]

**Neden ayrı tutuluyor:** [A değiştiğinde B'nin zorunlu değişmemesi; geçmişin korunması]

**Farklılaştırıcı mekanizma:** [sistemi benzerlerinden ayıran şey]

## 3. Kararlar

| Konu | Karar | Gerekçe |
|---|---|---|
| [katman] | [teknoloji] | [hangi kısıt gerektirdi] |

## 4. Varlıklar ve şema

```sql
-- Çalıştırılabilir DDL yaz; sözle anlatma.
CREATE TABLE ... ;
```

## 5. Kritik tasarım kararları

**1. [Donma / izolasyon mekanizması].** [Nasıl çalışır.]
**Neden önemli:** [hangi soruyu koruyor]
**Doğrulama testi:** [A'yı değiştir → eski B değişmemeli] → go/no-go'ya girer.

**2. [Bilinçli ödünleşim].** [Ne kazanıldı, ne kaybedildi, ne zaman geri dönülecek.]

## 6. API yüzeyi (özet)

```
GET/POST /...
```

## 7. Fazlama önerisi

| Faz | Kapsam | Çıktı |
|---|---|---|
| F0 | [iskelet + dikey dilim] | [...] |
