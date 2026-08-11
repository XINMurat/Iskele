# Contributing to İskele / İskele'ye Katkı

## English

İskele is a methodology project, so it holds itself to its own discipline.
Contributions are welcome but must respect the rules the skill applies to
everyone.

### Ground rules

1. **Tie every choice to a constraint.** A technology or structure change
   states the constraint that forces it ("on-prem + AD is mandatory, therefore
   …"). A choice that cannot be tied to a constraint is a preference — label it
   as one rather than dressing it up as a requirement.
2. **Acceptance criteria must be executable.** "Works well" is not an
   acceptance criterion. "Returns 403 for an unauthorized request" is. This
   applies to PR descriptions as much as to backlog tasks.
3. **No invented numbers.** Every number in a doc, report, or PR is either
   computed from data or explicitly marked as an estimate with its basis. If it
   is neither, delete it.
4. **No happy-path verification.** Before writing "verified", say *with what
   input*. At least one edge case (invalid value, empty record, localized text)
   must be part of the check. The `ı`/`i` fold in mixed Turkish/English data is
   the classic trap in this codebase.
5. **The generator must not guess silently.** If a value is unknown, warn
   visibly or refuse to write. A silently wrong indicator is worse than a
   missing one.
6. **Bilingual parity is required.** Every user-facing doc change must land in
   **both** `docs/en/` and `docs/tr/` (and both halves of `README.md`,
   `CONTRIBUTING.md`, `docs/QUICKSTART.md`). A PR that updates only one
   language is incomplete.
7. **ASCII for structural names.** Sheet names, column headers, and IDs stay
   ASCII (`Aciklama`, `Gorev`). Cell *content* may be Turkish. Non-ASCII in
   structural names creates cross-platform matching friction.

### Before opening a PR

```bash
pip install -r skill/iskele/scripts/requirements.txt

# 1. the generator's embedded regression tests must pass:
python skill/iskele/scripts/progress.py --self-test

# 2. the backlog parser must build a tracker from the worked example:
python skill/iskele/scripts/backlog_to_tracker.py \
  --backlog examples/backlog.example.md --out /tmp/tracker.xlsx

# 3. the report generator must compute a summary from it:
python skill/iskele/scripts/progress.py --xlsx /tmp/tracker.xlsx \
  --html examples/07-ilerleme-raporu.example.html \
  --config examples/iskele.config.example.json --check

# 4. the packaged skill must match its source:
python - <<'PY'
import zipfile, os, sys
n = lambda b: b.replace(b"\r\n", b"\n"); z = zipfile.ZipFile("iskele.skill")
bad = [k for k in z.namelist()
       if not os.path.exists(os.path.join("skill", k))
       or n(z.read(k)) != n(open(os.path.join("skill", k), "rb").read())]
print("skill in sync" if not bad else "OUT OF SYNC: " + ", ".join(bad))
sys.exit(1 if bad else 0)
PY
```

### Rebuilding the packaged skill

If you change **any** file under `skill/iskele/`, rebuild the one-file package
so it stays in sync (the shipped `iskele.skill` embeds those files):

```bash
python - <<'PY'
import zipfile, os
with zipfile.ZipFile("iskele.skill", "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk("skill/iskele"):
        # Running the scripts leaves __pycache__ behind; git ignores it but a
        # naive packer would ship it, and then the package no longer matches
        # its source on a machine that never ran them.
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in sorted(files):
            if f.endswith(".pyc"):
                continue
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, "skill").replace(os.sep, "/"))
PY
```

CI checks this. A stale package is not a cosmetic problem: users install the
package, not the source, so a drifted `iskele.skill` means the documented
behaviour and the shipped behaviour disagree.

### What lives where

- `skill/iskele/` — the skill: SKILL.md, references, templates (CC-BY-4.0 for
  prose) and scripts (MIT).
- `examples/` — worked material CI runs end to end.
- `docs/` — bilingual guides (CC-BY-4.0).

### Scope discipline

İskele builds structure; it does not adjudicate claims and it does not generate
ideas. Proposals that move evidence tiering or hypothesis registries here belong
in [Mizan](https://github.com/XINMurat/Mizan); proposals about idea generation
or analogical inference belong in [Kıyas](https://github.com/XINMurat/Kiyas).
Keeping the three verbs in three tools is not a packaging accident — a builder
that also grades its own output is an author acting as its own arbiter.

---

## Türkçe

İskele bir metodoloji projesidir; bu yüzden kendi disiplinine kendisi de uyar.
Katkılar memnuniyetle karşılanır ama skill'in herkese uyguladığı kurallara saygı
göstermek zorundadır.

### Temel kurallar

1. **Her seçimi bir kısıta bağla.** Teknoloji veya yapı değişikliği, onu
   zorunlu kılan kısıtı yazar ("on-prem + AD zorunlu olduğu için …"). Kısıta
   bağlanamayan seçim tercihtir; gereklilik kılığına sokma, öyle işaretle.
2. **Kabul kriteri çalıştırılabilir olmalı.** "İyi çalışır" kabul kriteri
   değildir; "yetkisiz istek 403 alır" kriterdir. Bu, backlog görevleri kadar PR
   açıklamaları için de geçerlidir.
3. **Uydurma sayı yok.** Dokümandaki, rapordaki, PR'daki her sayı ya veriden
   hesaplanmıştır ya da tabanıyla birlikte tahmin olarak işaretlenmiştir. İkisi
   de değilse sil.
4. **Mutlu-yol doğrulaması yok.** "Doğruladım" yazmadan önce *hangi girdiyle*
   sorusunu cevapla. En az bir kenar durum (geçersiz değer, boş kayıt,
   yerelleştirilmiş metin) kontrole dahil olmalı. Karışık Türkçe/İngilizce
   veride `ı`/`i` katlaması bu kod tabanının klasik tuzağıdır.
5. **Üreteç sessizce varsaymamalı.** Değer bilinmiyorsa görünür uyarı ver ya da
   yazma. Sessizce yanlış bir gösterge, eksik göstergeden kötüdür.
6. **İki dillilik zorunlu.** Kullanıcıya dönük her doküman değişikliği **hem**
   `docs/en/` **hem** `docs/tr/` içine (ve `README.md`, `CONTRIBUTING.md`,
   `docs/QUICKSTART.md`'in her iki yarısına) girmeli. Tek dili güncelleyen PR
   eksiktir.
7. **Yapısal adlar ASCII.** Sekme adları, sütun başlıkları ve ID'ler ASCII kalır
   (`Aciklama`, `Gorev`); hücre *içeriği* Türkçe olabilir. Yapısal adlardaki
   Türkçe karakter platformlar arası eşleşme sürtünmesi yaratır.

### PR açmadan önce

Yukarıdaki İngilizce bölümdeki dört komutu çalıştır. `skill/iskele/` altında
**herhangi bir** dosyayı değiştirdiysen tek-dosya paketi yeniden üret (aynı
bölümdeki script). CI bunu kontrol eder. Bayat paket kozmetik bir sorun
değildir: kullanıcı kaynağı değil paketi kurar, yani kaymış bir `iskele.skill`
belgelenen davranışla dağıtılan davranışın çelişmesi demektir.

### Kapsam disiplini

İskele yapı kurar; iddia yargılamaz, fikir üretmez. Kanıt katmanlamayı veya
hipotez registry'sini buraya taşıyan öneriler
[Mizan](https://github.com/XINMurat/Mizan)'a; fikir üretimi ve analojik çıkarımla
ilgili öneriler [Kıyas](https://github.com/XINMurat/Kiyas)'a aittir. Üç fiili üç
araçta tutmak paketleme kazası değildir — kendi çıktısını kendi notlandıran bir
kurucu, yazarın hakem olduğu durumdur.
