# Step 6 — Tracking and the generator

The goal is not to *estimate* progress but to *compute* it. The report is a
derivative of the tracker.

## The chain

```
03-gorev-listesi.md ──backlog_to_tracker.py──> tracker.xlsx ──progress.py──> 07-ilerleme-raporu.html
      (source)                                  (live state)                    (GEN regions)
```

The backlog is the source of "what will be done"; the tracker carries daily
state; the report is the readable view. Do not keep them in sync by hand — run
the generator.

## Tracker schema (`tracker.xlsx`)

**Sheet `Takip`** — columns (the generator looks for these names):

| Column | Generated | Values |
|---|---|---|
| `ID` | ✓ from the backlog | unique |
| `Faz` (phase) | ✓ | the phase codes in the config |
| `Epik` (epic) | ✓ | `F1.2 Title` (the first word is the epic code) |
| `Gorev` (task) | ✓ | title |
| `Katman` (layer) | ✓ | derived from the ID |
| `Tahmin` (estimate) | ✓ | `S` / `M` / `L` |
| `Bagimlilik` (dependency) | ✓ | list of IDs |
| `Durum` (status) | **by hand** | `Yapilacak` / `Devam` / `Bloke` / `Tamamlandi` |
| `Sorumlu` `Baslangic` `Bitis` `Not` | **by hand** | free text |
| `Hakem` (arbiter) | ✓ from the acceptance criterion | may be empty |

> The `Hakem` column is appended **at the end**, never inserted: `Durum` must
> stay in column H, because the `Ozet` formulas and the dropdown validation
> depend on it.

**The column keys are part of the schema, not of the language.** Produce the
kit in the user's language, but if you rename these keys, rename them in the
config and the scripts too — the generator matches on the key, not on the
label.

## The arbiter column and the second indicator

If the acceptance criterion says `**Hakem:** pytest tests/test_authz.py`, the
generator carries it into the `Hakem` column. If you do not write one, the
column stays empty — that is normal, and it **is not invented**.

The report prints this as its own region (`GEN:HAKEM`): *how much of the
completed effort names an arbiter other than the author.* Two cautions:

- **It does not change the progress percentage.** "Done" and "verified" are
  two different things; melting them into one indicator makes both
  unreadable.
- **It does not show that the criterion was actually run.** No tracker can
  know that; the Definition of Done knows it. The indicator only says how much
  of the "done" verdict rests on the self-report of the person who did the
  work.

On older trackers with no `Hakem` column, the indicator prints **"not
measured", not 0%.** Showing an unmeasured thing as zero is the most expensive
kind of silent assumption: it looks like a measurement.

**Sheet `Ozet`** — status and phase breakdown via `COUNTIF`/`COUNTIFS`. Do not
type numbers; you will break the formulas.

**Sheet `Skorkart`** — the phase-close scorecard. **Optional, hand-filled, and
every number in it is self-reported.** One row per phase, written at the gate,
next to the go/no-go.

| Column | Filled | Meaning |
|---|---|---|
| `Faz` | ✓ pre-written | the phase codes from the config |
| `BacklogRevizyon` | **by hand** | tasks that changed after the phase opened |
| `YenidenTur` | **by hand** | tasks that came back more than once |
| `KriterYenidenYazilan` | **by hand** | acceptance criteria rewritten *after* the work |
| `IkizBoslugu` | **by hand** | consuming-twin gaps found (RR-03) |
| `IkizKapida` | **by hand** | how many of those were caught **at the gate** |
| `SenaryoProvali` / `SenaryoTesadufi` | **by hand** | scenario findings: rehearsed vs. noticed by luck |
| `KapsamDisi` | **by hand** | times work left the phase (RR-07) |
| `Rampalar` | **by hand** | which `RR-nn` fired, free text |
| `Kacan` | **by hand** | defects found after the gate that this phase's criteria covered |
| `KacanSinifi` | **by hand**, optional | for each escape: the check that should have fired, or the check that now exists because of it (RR-13). Optional so existing trackers keep loading; an escape count with this cell empty prints as *sinifsiz kacak* — the loop did not close |
| `Cikarim` | **by hand** | one or two sentences |

Nothing here can be generated from the backlog, and that is the point: what is
being measured is not the work but **where the plan leaked**, and only the
person standing at the gate knows that.

**Three rules the generator enforces, for the same reason the rest of §6 exists:**

- **No sheet ≠ zeros.** A tracker without the sheet prints *"olculmedi"* — not
  kept. A row of zeros would be the most flattering possible lie: no rework, no
  rewritten criteria, nothing escaped.
- **An empty cell ≠ zero.** The `Faz` column is pre-written so the table is
  half-filled rather than blank, so "a row exists" is not "a phase closed". A
  row with nothing filled in is skipped, and a partly filled column prints how
  many phases actually answered it (`3 (2/4 faz)`).
- **`IkizKapida` ≤ `IkizBoslugu`.** It is a subset: gaps caught at the gate, out
  of gaps found. Reversed, the "caught at the gate" ratio exceeds 1 and the
  table reads as good news — the indicator does not merely go wrong, it points
  the other way. That is a validation error (exit 2), not a number.

**It does not touch the progress percentage.** A phase can close at 100% and
carry four rewritten criteria; that is not a contradiction, it is the
information. Melting the two into one indicator would make both unreadable —
the same argument as the `Hakem` column.

The report prints it as its own region (`GEN:SKORKART`), and prints on every
render that the numbers are self-reported. The scorecard is a claim like any
other: filled in by whoever did the work, its arbiter is `author`.

Where the measures come from and how to read them:
[`references/recovery.md`](recovery.md) — the phase-close scorecard.

**Sheet `Aciklama`** — which column is filled by hand and which is generated.

> ASCII note: keep sheet and column names ASCII (`Aciklama`, `Gorev`).
> Non-ASCII characters create cross-platform friction in file and column
> matching. Cell *contents* can be in any language — the generator handles the
> `ı/i` folding.

## Effort-weighted progress

```
progress % = Σ(effort of completed tasks) / Σ(effort of all tasks)
```

Weighted by **effort**, not by task count: a four-day task must not weigh the
same as a 0.75-day one.

Default weights `S=0.75 · M=1.5 · L=4` (work-days). If you change them, change
them in three places at once: the backlog scale, `iskele.config.json`, and the
report footnote.

**The credit rule.** The default is binary: only `Tamamlandi` earns credit.
Giving partial credit to `Devam` (say 0.5) inflates progress and manufactures
the "almost done" illusion; if you do it, do it deliberately and write it in
the report.

## GEN markers

Every region to be generated in the report HTML is wrapped in this pair:

```html
<!-- GEN:BARS:BEGIN (produced by progress.py; source: tracker.xlsx) -->
    <div class="bars">...</div>
<!-- GEN:BARS:END -->
```

The generator changes **only** the inside of these regions. Everything outside
(commentary, risks, the ADR list, footnotes) stays hand-editable and is
preserved. That separation matters: the report stays both automatic and
writable.

Default region keys: `CHIPS` (top badges), `KPI` (summary indicators), `CARDS`
(phase cards), `BARS` (epic bars), `TIMELINE` (gate/phase flow), `HAKEM`
(how much of the completed effort names an arbiter other than the author) and
`SKORKART` (the phase-close scorecard).

`tools/check_doc_claims.py` binds this list to the generator's `RENDERERS`
dict, because it went stale twice: `HAKEM` shipped, then `SKORKART` shipped,
and this sentence kept saying five in both languages.

## Configuration (`iskele.config.json`)

The single file that binds the generator to the project. Template:
`assets/iskele.config.example.json`.

```jsonc
{
  "phases": ["F0", "F1"],
  "effort_weights": {"S": 0.75, "M": 1.5, "L": 4.0},
  "status_credit": {"Tamamlandi": 1.0, "Devam": 0.0,
                    "Bloke": 0.0, "Yapilacak": 0.0},
  "workdays_per_month": 21,
  "phase_meta": {
    "F0": {"title": "F0 · Setup", "repo": "phase/f0", "stack": "Docker",
           "ms": "M0", "dep": null, "desc": "..."}
  },
  "epic_display": {"F0.1": "F0.1 Project skeleton"},
  "static_steps": [{"t": "Architecture approved", "m": "01-...md"}],
  "flow": [{"kind": "phase", "phase": "F0", "mk": "M0",
            "t": "M0 — Skeleton", "m": "..."},
           {"kind": "gate", "phase": "F0", "mk": "◆",
            "t": "Gate M0", "m": "go/no-go"}]
}
```

`phase_meta` / `epic_display` / `flow` are **curated** (a human writes them);
the numbers come from the tracker. Keep that separation: prose in the config,
numbers in the data.

## Input validation — no silent assumptions

The generator must not quietly fall back to a default for an unknown value.
Three errors seen in the field, and the rule for each:

| Error | Silent behaviour (wrong) | Correct behaviour |
|---|---|---|
| Invalid `Tahmin` (`XL`) | silently weigh it as `M` | ERROR, write nothing |
| Localised `Durum` (`Tamamlandı` vs `Tamamlandi`) | silently 0 credit → progress understated | normalise + WARN |
| `Faz` outside the phase list (`F9`) | shows in the epic bar, missing from the total | **invariant violation** → ERROR |

**Invariant:** `Σ epic effort == Σ phase effort`. A divergence means a task
has fallen outside the defined phases, and the indicator is silently falsified.
The generator checks this and stops on a violation.

`progress.py` exit codes: `0` success · `2` validation error (the report was
not written) · `3` invariant violation. `--force` overrides the error (not
recommended); `--check` prints a summary without writing.

## Weekly flow

1. Update the `Durum` column in the tracker.
2. Run `python progress.py`.
3. If it warns or errors, fix the tracker (not the report).
4. Refresh the hand-written sections of the report (risks, "this week's
   focus").
