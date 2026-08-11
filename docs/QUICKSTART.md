# Quickstart / Hızlı Başlangıç

## English

### 1. Install the skill

```bash
cp iskele.skill ~/.claude/skills/
```

Then simply describe what you want to build. İskele triggers on intents like
"plan this project", "give me a roadmap", "turn this into a backlog", or "I
don't know where to start".

### 2. Answer the constraint questions

İskele asks at most three: where it runs, scale and identity, and what output
you want now (plan, prototype, or both). Constraints determine the
architecture — preferences do not.

### 3. Take delivery of the kit

Ten pieces, seven of them mandatory. See
[`skill/iskele/references/kit-manifest.md`](../skill/iskele/references/kit-manifest.md)
for what each contains.

| # | File | Required |
|---|---|---|
| 00 | `00-BASLA-rehber.md` | ✓ |
| 01 | `01-mimari-ve-veri-modeli.md` | ✓ |
| 02 | `02-yol-haritasi.md` | ✓ |
| 03 | `03-gorev-listesi.md` | ✓ |
| 04 | `04-kalite-kapilari.md` | ✓ |
| 05 | `05-gelistirme-kurulumu.md` | — |
| 06 | `06-riskler-ve-kararlar.md` | ✓ |
| 07 | `07-ilerleme-raporu.html` | ✓ |
| 08 | `tracker.xlsx` | ✓ |
| 09 | `08-onboarding.md` | — |

If a piece is skipped, the skill must say **which one and why** — never
silently.

### 4. Wire up tracking

```bash
pip install -r skill/iskele/scripts/requirements.txt
python skill/iskele/scripts/backlog_to_tracker.py --backlog 03-gorev-listesi.md --out tracker.xlsx
```

Fill in `Durum` / `Sorumlu` / dates by hand as work proceeds. Everything else in
the tracker is generated — do not hand-edit it, and never type numbers into the
`Ozet` sheet (they are formulas).

### 5. Regenerate the report

```bash
python skill/iskele/scripts/progress.py --xlsx tracker.xlsx --html 07-ilerleme-raporu.html --config iskele.config.json
```

Add `--check` to print the summary without writing. The script touches only the
`GEN:...:BEGIN`/`:END` regions; the rest of the report is yours.

### 6. Hand off

- **[Mizan](https://github.com/XINMurat/Mizan)** — audit the kit's own claims.
  Every sentence that says "verified" goes through a counter-example sweep.
- **[Kıyas](https://github.com/XINMurat/Kiyas)** — generate missing features and
  risks; they re-enter the backlog as tasks.

Both directions have an adapter, so the handoff moves files rather than
intentions:

```bash
python skill/iskele/scripts/iskele_to_registry.py --backlog 03-gorev-listesi.md --out registry.yaml
python skill/iskele/scripts/kiyas_to_backlog.py --seeds seeds.yaml --phase F2 --out new-tasks.md
```

Expect the registry to come back with every task at `arbiter: author` — that is
correct, not a bug. A status column filled in by whoever did the work is
self-report. Name a real judge in the backlog to change it:

```markdown
- *Kabul:* An unauthorized request gets 403. **Hakem:** pytest tests/test_authz.py
```

---

## Türkçe

### 1. Skill'i kur

```bash
cp iskele.skill ~/.claude/skills/
```

Sonra ne inşa etmek istediğini anlat. İskele "bu projeyi planla", "yol haritası
çıkar", "backlog çıkar", "nereden başlayacağımı bilmiyorum" gibi niyetlerde
devreye girer.

### 2. Kısıt sorularını cevapla

İskele en fazla üç soru sorar: nerede çalışacak, ölçek ve kimlik, şimdi hangi
çıktı isteniyor (plan, prototip, ikisi). Mimariyi kısıtlar belirler, tercihler
değil.

### 3. Kiti teslim al

On parça, yedisi zorunlu. Her parçanın içeriği için bkz.
[`skill/iskele/references/kit-manifest.md`](../skill/iskele/references/kit-manifest.md).
Bir parça atlanıyorsa skill **hangisini ve neden** atladığını söylemek
zorundadır — sessizce atlamaz.

### 4. Takibi kur

```bash
pip install -r skill/iskele/scripts/requirements.txt
python skill/iskele/scripts/backlog_to_tracker.py --backlog 03-gorev-listesi.md --out tracker.xlsx
```

İş ilerledikçe `Durum` / `Sorumlu` / tarihleri elle doldur. Çizelgedeki diğer
her şey üretilir — elle düzenleme, `Ozet` sekmesine sayı yazma (orası formül).

### 5. Raporu yeniden üret

```bash
python skill/iskele/scripts/progress.py --xlsx tracker.xlsx --html 07-ilerleme-raporu.html --config iskele.config.json
```

`--check` yazmadan özeti basar. Script yalnız `GEN:...:BEGIN`/`:END`
bölgelerine dokunur; raporun gerisi senindir.

### 6. Devret

- **[Mizan](https://github.com/XINMurat/Mizan)** — kitin kendi iddialarını
  denetle; "doğrulandı" diyen her cümleyi karşı-örnek taramasına sok.
- **[Kıyas](https://github.com/XINMurat/Kiyas)** — eksik özellik ve risk
  adaylarını üret; backlog'a görev olarak geri girerler.

İki yönün de adaptörü var; devir niyet değil dosya taşır:

```bash
python skill/iskele/scripts/iskele_to_registry.py --backlog 03-gorev-listesi.md --out registry.yaml
python skill/iskele/scripts/kiyas_to_backlog.py --seeds tohumlar.yaml --phase F2 --out yeni.md
```

Registry'de her görevin `arbiter: author` gelmesi hata değil, doğru davranış:
işi yapanın doldurduğu durum sütunu öz-beyandır. Değiştirmek için backlog'da
gerçek hakemi adlandır:

```markdown
- *Kabul:* Yetkisiz istek 403 alır. **Hakem:** pytest tests/test_authz.py
```
