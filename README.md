# İskele — From Vague Intent to an Executable Delivery Kit

A Claude skill for the moment *before* the code. İskele (Turkish: *scaffold*)
does not write your project — it **builds the structure the project runs on**:
a domain model, a phased roadmap with go/no-go gates, an atomic backlog with
executable acceptance criteria, a Definition of Done, a live tracking
spreadsheet, and a progress report that regenerates itself from that
spreadsheet.

The three verbs are kept separate on purpose:

> **İskele builds** · [**Mizan**](https://github.com/XINMurat/Mizan) **weighs**
> · [**Kıyas**](https://github.com/XINMurat/Kiyas) **generates**

İskele produces the structure the other two operate on. When the kit is done it
hands off: Mizan audits the kit's own claims, Kıyas generates the missing
features and risks, and those come back as backlog tasks.

## The two ways a plan fails

1. **Unexecutable.** There is a beautiful roadmap, but "what do I do today" is
   unanswered — tasks are not atomic, there is no acceptance criterion, and
   whether something is finished is a matter of opinion.
2. **Untrackable.** There is a task list, but progress is *estimated by hand*.
   The report reflects the author's mood, not the data.

İskele closes both: every task is atomic and has an acceptance criterion you can
actually run, progress is **computed** from the tracker, and the report is a
derivative of the tracker — not a parallel document that drifts.

## The chain

```
03-gorev-listesi.md ──backlog_to_tracker.py──> tracker.xlsx ──progress.py──> 07-ilerleme-raporu.html
     (the source)                                (live status)                  (GEN regions only)
```

`progress.py` rewrites **only** the regions between `GEN:...:BEGIN` / `:END`
markers. Everything else in the report stays hand-editable.

Progress is **effort-weighted**, not task-counted (`S=0.75 · M=1.5 · L=4`
workdays by default): a four-day task must not weigh the same as a half-day one.

Alongside it the report carries a second, deliberately modest indicator: **how
much of the completed effort rests on self-report.** A task whose acceptance
criterion names an arbiter (`**Hakem:** pytest tests/test_authz.py`) counts as
arbitered; one that names none does not. It does not claim the criterion was
actually run — no spreadsheet can know that — and it never moves the progress
percentage, because "done" and "verified" are two different things. On a tracker
built before this column existed, the indicator reads **"unmeasured", not 0%**.

## What is in here

| Path | What it is |
|---|---|
| `skill/iskele/SKILL.md` | The skill itself — the seven-step loop, the output manifest, the red lines |
| `skill/iskele/references/domain-model.md` | Step 2: how to find the distinction the schema rests on |
| `skill/iskele/references/kit-manifest.md` | What each of the ten kit files contains and why |
| `skill/iskele/references/tracking.md` | Tracker schema, GEN markers, generator setup |
| `skill/iskele/assets/templates/` | The fillable templates (00–08) |
| `skill/iskele/scripts/backlog_to_tracker.py` | backlog markdown → `tracker.xlsx` |
| `skill/iskele/scripts/progress.py` | `tracker.xlsx` → the report's GEN regions |
| `skill/iskele/scripts/iskele_to_registry.py` | backlog → a Mizan registry (each acceptance criterion is already a preregistered refutation condition) |
| `skill/iskele/scripts/kiyas_to_backlog.py` | Kıyas seeds → backlog tasks (each seed's cheapest refutation is already an executable acceptance criterion) |
| `iskele.skill` | One-file package for installing the skill |
| `examples/` | A worked backlog + config + report that CI runs end to end |
| `docs/` | Quickstart and usage guide (EN/TR) |

## Install the skill

```bash
cp iskele.skill ~/.claude/skills/
```

Or point your project at `skill/iskele/` directly.

## Run the chain on the example

```bash
pip install -r skill/iskele/scripts/requirements.txt
python skill/iskele/scripts/backlog_to_tracker.py --backlog examples/backlog.example.md --out tracker.xlsx
python skill/iskele/scripts/progress.py --xlsx tracker.xlsx --html examples/07-ilerleme-raporu.example.html --config examples/iskele.config.example.json --check
```

`--check` prints the computed summary without writing. Drop it to rewrite the
GEN regions. `python skill/iskele/scripts/progress.py --self-test` runs the
embedded regression tests.

## The handoff, as files rather than as prose

The three tools exchange artifacts, and the exchange is checked in CI:

```bash
# Kıyas seeds -> backlog tasks (only H-aday seeds become work)
python skill/iskele/scripts/kiyas_to_backlog.py --seeds seeds.yaml --phase F2 --out new-tasks.md

# backlog -> a Mizan registry of preregistered acceptance criteria
python skill/iskele/scripts/iskele_to_registry.py --backlog 03-gorev-listesi.md --out registry.yaml

# ...and Mizan itself returns the verdict on the result
python ../Mizan/tools/mizan_validate.py registry.yaml
```

Two defaults carry the weight here, and both are deliberately unflattering:

**Every task starts at `arbiter: author`.** A `Durum` column filled in by
whoever did the work is self-report, not measurement, so Mizan's R8 keeps
K-promotion closed and stamps a permanent KKE. To earn a real arbiter, name it
in the backlog next to the criterion — `**Hakem:** pytest tests/test_authz.py`
— and the class becomes `runtime`. The adapter never upgrades this on its own;
it reports how many tasks are still self-reported.

**Only `H-aday` seeds become tasks.** A speculative seed is a research
question, not work; putting it in a backlog would let something with no arbiter
count toward effort. `[S]`/`[NK]`/`[GB]` seeds are parked in a visible comment
block instead of being dropped, and a seed whose cost cannot be resolved to
S/M/L gets `(M)` **plus a `TAHMIN: kalibresiz` mark** rather than a silent
weight.

The interop claim is not self-assessed: CI checks out the Mizan repo and runs
`mizan_validate.py` against the generated registry, so the arbiter for "these
tools actually interoperate" lives outside this repository.

## What the tooling does NOT do

It computes progress from **recorded status**. It cannot tell you whether a row
marked `Tamamlandi` was actually verified against its acceptance criterion — a
human ran that check, or nobody did. The generator is an arbiter for
*arithmetic*, never for *truth of status*.

This is why the Definition of Done makes "actually execute the acceptance
criterion" a mandatory item, and why the skill's red lines call out
happy-path verification by name. A spreadsheet that only aggregates self-reports
inherits the honesty of whoever filled it in.

## Honest status of the project's own claim

İskele claims that kits built this way get executed and tracked more reliably
than free-form plans. That claim is currently **speculative** — there is no
control arm and no measured hit rate. It is stated here rather than implied,
which is the same standard the skill applies to every estimate it emits: give
the basis, say it is uncalibrated, recalibrate after the first phase lands.

## No setup required — and a disclosed confound

**You do not need to configure your assistant for this skill to work.** No
custom instructions, no system prompt, no house style. If it only behaves
when your `CLAUDE.md` is arranged a particular way, that is a **defect in the
skill**, not a missing step in your setup — please open an issue.

Honest tier on that claim: **`[K]` for the neutral host**, `[H]` for the
hostile one. İskele was run on a vague real brief with no conflicting *and no
reinforcing* host instructions, and produced the full ten-part kit on disk —
tracker included, acceptance criteria consumer-side, scenario rehearsals in
the gates: see
[`examples/portability-neutral-host.md`](examples/portability-neutral-host.md).
That run also found and fixed a real defect in `backlog_to_tracker.py`. The
**hostile**-host case passed too: under a `CLAUDE.md` banning planning
documents and file creation, the run **created nothing**, named which steps
were disabled, said plainly that nothing measurable was produced, and handed
the decision back with three options — rather than delivering a good-looking
prose plan that no one could track. İskele also has an
extra exposure the other two do not: this file and the skill body are in
Turkish, while the kit it produces should follow the user's language. The
filenames and column headers in the skill are **examples**; the structure —
file order, fields, `GEN:` markers, the column keys the scripts read — is
what is fixed. Translate the names, not the schema.

**Disclosed confound:** this project's author keeps an always-on personal
instruction set that overlaps these rules at several points. Their own
sessions are therefore a maximally reinforcing host, and *"it works well for
me"* from that setup is confounded by construction. That instruction set is
deliberately **not** shipped as a recommendation: installing it would erase
the neutral-host case from the user population — the only case that can
produce field evidence — and it would put the same rules in two places under
separate maintenance, where a user's copy silently overrides the skill.

If a rule must survive an unknown setup, it belongs in a script, not in a
paragraph asking users to reconfigure their assistant. For this skill that is
`backlog_to_tracker.py` and `progress.py`: they run without a model, so the
same backlog yields the same tracker and the same percentage in any host.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Licensing

Dual, deliberately: **code and schemas → MIT** ([`LICENSE`](LICENSE)); **prose,
templates and methodology text → CC-BY-4.0**
([`LICENSE-docs.md`](LICENSE-docs.md)).

### Version

**v1.0** — seven-step loop + domain-distinction procedure + phase gates + atomic
backlog schema + DoD/go-no-go + tracker generator + effort-weighted,
GEN-marked progress report.

---

# İskele — Belirsiz Niyetten Yürütülebilir Teslim Kitine

Koddan *önceki* an için bir Claude skill'i. İskele projeni yazmaz — **projenin
üstünde yürüyeceği yapıyı kurar**: alan modeli, kapılı fazlı yol haritası,
çalıştırılabilir kabul kriterli atomik backlog, Tamamlandı Tanımı, canlı takip
çizelgesi ve o çizelgeden kendini yeniden üreten ilerleme raporu.

Üç fiil bilinçli olarak ayrıdır:

> **İskele kurar** · [**Mizan**](https://github.com/XINMurat/Mizan) **tartar**
> · [**Kıyas**](https://github.com/XINMurat/Kiyas) **üretir**

İskele, diğer ikisinin üzerinde çalıştığı yapıyı üretir. Kit bitince devreder:
Mizan kitin kendi iddialarını denetler, Kıyas eksik özellik ve riskleri üretir,
onlar backlog'a görev olarak geri girer.

## Bir plan iki türlü başarısız olur

1. **Yürütülemez.** Güzel bir yol haritası var ama "bugün ne yapacağım"
   belirsiz — görevler atomik değil, kabul kriteri yok, bitip bitmediği
   tartışmaya açık.
2. **İzlenemez.** Görev listesi var ama ilerleme *el yordamıyla tahmin
   ediliyor*. Rapor veriyi değil, yazarın hissini yansıtıyor.

İskele ikisini de kapatır: her görev atomik ve fiilen koşulabilir kabul
kriterli, ilerleme çizelgeden **hesaplanır**, rapor çizelgenin türevidir — yanına
kurulup zamanla sapan ikinci bir belge değil.

## Zincir

```
03-gorev-listesi.md ──backlog_to_tracker.py──> tracker.xlsx ──progress.py──> 07-ilerleme-raporu.html
      (kaynak)                                  (canlı durum)                  (yalnız GEN bölgeleri)
```

`progress.py` **yalnızca** `GEN:...:BEGIN` / `:END` işaretleri arasındaki
bölgeleri yeniden yazar. Raporun gerisi elle düzenlenebilir kalır.

İlerleme görev sayısıyla değil **efor-ağırlıklı** hesaplanır (varsayılan
`S=0.75 · M=1.5 · L=4` iş-günü): dört günlük görev, yarım günlükle aynı ağırlıkta
sayılmamalı.

Yanında rapor, bilerek mütevazı ikinci bir gösterge taşır: **tamamlanan eforun
ne kadarı öz-beyana dayanıyor.** Kabul kriterinde hakem adı geçen görev
(`**Hakem:** pytest tests/test_authz.py`) hakemli sayılır, geçmeyen sayılmaz.
Kriterin fiilen koşulduğunu iddia etmez — bunu hiçbir çizelge bilemez — ve
ilerleme yüzdesini asla değiştirmez, çünkü "bitti" ile "doğrulandı" iki ayrı
şeydir. Bu sütun yokken üretilmiş çizelgede gösterge **%0 değil, "ölçülmedi"**
basar.

## Depoda ne var

| Yol | Nedir |
|---|---|
| `skill/iskele/SKILL.md` | Skill'in kendisi — yedi adımlı döngü, çıktı manifesti, kırmızı çizgiler |
| `skill/iskele/references/domain-model.md` | Adım 2: şemanın dayandığı ayrım nasıl bulunur |
| `skill/iskele/references/kit-manifest.md` | On kit dosyasının her biri ne içerir, neden var |
| `skill/iskele/references/tracking.md` | Çizelge şeması, GEN işaretleri, üreteç kurulumu |
| `skill/iskele/assets/templates/` | Doldurulacak şablonlar (00–08) |
| `skill/iskele/scripts/backlog_to_tracker.py` | backlog markdown → `tracker.xlsx` |
| `skill/iskele/scripts/progress.py` | `tracker.xlsx` → raporun GEN bölgeleri |
| `skill/iskele/scripts/iskele_to_registry.py` | backlog → Mizan registry'si (her kabul kriteri zaten önkayıtlı bir çürütme koşulu) |
| `skill/iskele/scripts/kiyas_to_backlog.py` | Kıyas tohumları → backlog görevleri (her tohumun en ucuz çürütmesi zaten çalıştırılabilir bir kabul kriteri) |
| `iskele.skill` | Skill'i kurmak için tek-dosya paket |
| `examples/` | CI'ın uçtan uca koştuğu çalışılmış backlog + config + rapor |
| `docs/` | Hızlı başlangıç ve kullanım kılavuzu (EN/TR) |

## Kurulum

```bash
cp iskele.skill ~/.claude/skills/
```

Ya da projeni doğrudan `skill/iskele/` dizinine yönlendir.

## Zinciri örnek üzerinde koştur

```bash
pip install -r skill/iskele/scripts/requirements.txt
python skill/iskele/scripts/backlog_to_tracker.py --backlog examples/backlog.example.md --out tracker.xlsx
python skill/iskele/scripts/progress.py --xlsx tracker.xlsx --html examples/07-ilerleme-raporu.example.html --config examples/iskele.config.example.json --check
```

`--check` yazmadan hesaplanan özeti basar; kaldırınca GEN bölgelerini yeniden
yazar. `python skill/iskele/scripts/progress.py --self-test` gömülü regresyon
testlerini koşar.

## Devir — düzyazı değil, dosya

Üç araç birbirine artefakt geçirir ve bu geçiş CI'da denetlenir:

```bash
# Kıyas tohumları -> backlog görevleri (yalnız H-aday tohumlar işe döner)
python skill/iskele/scripts/kiyas_to_backlog.py --seeds tohumlar.yaml --phase F2 --out yeni.md

# backlog -> önkayıtlı kabul kriterlerinden oluşan Mizan registry'si
python skill/iskele/scripts/iskele_to_registry.py --backlog 03-gorev-listesi.md --out registry.yaml

# ...ve hükmü Mizan'ın kendisi verir
python ../Mizan/tools/mizan_validate.py registry.yaml
```

Yükü taşıyan iki varsayılan var; ikisi de bilerek pohpohlamıyor:

**Her görev `arbiter: author` ile başlar.** İşi yapanın doldurduğu `Durum`
sütunu ölçüm değil öz-beyandır; Mizan'ın R8'i bu durumda K'ye terfiyi kapatır
ve kalıcı bir KKE basar. Gerçek hakem kazanmak için kriterin yanına yaz —
`**Hakem:** pytest tests/test_authz.py` — sınıf `runtime` olur. Adaptör bunu
kendiliğinden yükseltmez; kaç görevin öz-beyanda kaldığını raporlar.

**Yalnız `H-aday` tohumlar göreve döner.** Spekülatif tohum iş değil araştırma
sorusudur; backlog'a koymak, hakemi olmayan bir şeyi efora saydırmak olur.
`[S]`/`[NK]`/`[GB]` tohumlar silinmez, görünür bir yorum bloğunda park edilir;
`cost` alanı S/M/L'ye çözülemeyen tohum sessizce ağırlık almaz, `(M)` **artı
`TAHMIN: kalibresiz` işareti** alır.

Birlikte-çalışırlık iddiası öz-değerlendirme değil: CI, Mizan deposunu checkout
edip üretilen registry'yi `mizan_validate.py`'a veriyor — yani "bu araçlar
gerçekten birbirine bağlanıyor" hükmünün hakemi bu deponun dışında.

## Araçların YAPMADIĞI şey

İlerlemeyi **kaydedilmiş durumdan** hesaplar. `Tamamlandi` işaretli bir satırın
kabul kriterine karşı gerçekten doğrulanıp doğrulanmadığını bilemez — o kontrolü
ya bir insan yaptı ya da kimse yapmadı. Üreteç *aritmetiğin* hakemidir, *durumun
doğruluğunun* değil.

Tamamlandı Tanımı'nda "kabul kriterini fiilen çalıştır" maddesinin zorunlu
olmasının ve skill'in kırmızı çizgilerinde mutlu-yol doğrulamasının adıyla
anılmasının sebebi budur. Yalnızca öz-beyanı toplayan bir çizelge, dolduranın
dürüstlüğünü devralır.

## Projenin kendi iddiasının dürüst durumu

İskele, bu şekilde kurulan kitlerin serbest planlara kıyasla daha güvenilir
yürütüldüğünü ve izlendiğini iddia ediyor. Bu iddia şu an **spekülatif** —
kontrol kolu da ölçülmüş isabet oranı da yok. İma edilmek yerine burada açıkça
yazılıyor; skill'in her tahmine uyguladığı standardın aynısı: tabanını ver,
kalibresiz olduğunu söyle, ilk faz gerçekleşince yeniden kalibre et.

## Katkı

Bkz. [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Lisans

Bilinçli olarak ikili: **kod ve şemalar → MIT** ([`LICENSE`](LICENSE)); **düzyazı,
şablonlar ve metodoloji metni → CC-BY-4.0**
([`LICENSE-docs.md`](LICENSE-docs.md)).

### Sürüm

**v1.0** — yedi adımlı döngü + alan-ayrımı prosedürü + faz kapıları + atomik
backlog şeması + DoD/go-no-go + çizelge üreteci + efor-ağırlıklı, GEN-işaretli
ilerleme raporu.
