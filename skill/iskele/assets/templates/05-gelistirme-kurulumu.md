# Geliştirme Kurulumu

## Ön gereksinimler

| Araç | Sürüm | Ne için |
|---|---|---|
| [araç] | [sürüm] | [amaç] |

## Klasör yapısı

```
proje-kok/
├─ [servis]/
├─ infra/
└─ docs/        # bu kit
```

## Adım adım

### 1. Repo ve ortam
```bash
git clone <repo-url> && cd proje-kok
cp infra/.env.example infra/.env   # parolaları değiştir
```

### 2. Altyapı
```bash
cd infra && docker compose up -d && docker compose ps
```

### 3. Servisler
```bash
# [derleme/çalıştırma komutları]
```

**Doğrulama:** [şunu çalıştır → şunu görmelisin]

## Sık sorunlar
- **Port çakışması:** [çözüm]
- **Bağlantı hatası:** [çözüm]

## Durdurma
```bash
docker compose down       # veriler kalır
docker compose down -v    # volume siler — DİKKAT
```
