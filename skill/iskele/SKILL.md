---
name: iskele
description: Turns a vague project intent into an executable delivery kit — domain model, phased roadmap with gates, atomic backlog with acceptance criteria, Definition-of-Done quality gates, a tracking spreadsheet, and a progress report that regenerates itself from the tracker. Use this skill whenever someone wants to plan, scope, structure, or kick off a software project or major feature — including "proje planla", "yol haritası çıkar", "task listesi / backlog çıkar", "nereden başlayacağımı bilmiyorum", "bu projeyi nasıl kurarım", "geliştirme planı", "kit oluştur", "sprint planı", "MVP kapsamı", "ilerleme raporu / takip çizelgesi kur" — and also when a user merely describes an app or system they want to build and clearly needs structure rather than code. Use it too when an existing project has a roadmap but no tracking, no acceptance criteria, or no way to see progress. Generative sibling of mizan (audits claims) and kiyas (generates ideas); iskele builds the structure they operate on.
---

# Iskele

It *builds* a project: it turns a vague intent into an executable, trackable
system of work.

The trio's verbs are separate — **iskele builds, mizan weighs, kiyas
generates.** Do not mix them: an evidence or audit question goes to mizan, an
idea or stuck-point question goes to kiyas.

## Why this skill exists

Planning output fails in two typical ways:

1. **A plan you cannot execute** — there is a handsome roadmap, but "what do
   I do today" is unclear; tasks are not atomic, there are no acceptance
   criteria, and whether something is finished is open to argument.
2. **A plan you cannot track** — a task list exists, but progress is estimated
   by hand; the report reflects the author's feeling rather than the truth.

Iskele closes both: every task is atomic and carries an acceptance criterion,
progress is *computed* from data, and the report becomes a derivative of the
tracker.

## When to use it, when not to

**Use:** a new project, product or major feature is being planned; an existing
project has no backlog, no tracking or no acceptance criteria; the question is
"where do I start".

**Do not use:** a single file or function change (just do it); pure ideation
(kiyas); auditing existing claims only (mizan); an urgent bug (fix it first).

## The core loop — seven steps

Do not break the order. Each step takes the previous one's output as input; a
skipped step collapses in the next.

### 1. Elicit the constraints (ask; do not assume)

Architecture is decided by constraints, not preferences. Settle at least:

- **Where will it run?** (on-prem / cloud / desktop / mobile)
- **Scale and identity?** (how many users, is SSO mandatory, multi-tenant)
- **Which deliverable is wanted now?** (a plan, a prototype, both)
- **Hard constraints?** (existing stack, regulation, deadline, team size)

If the answers are unclear, ask **in one round**; never more than three
questions. If the user already said it, do not ask again — derive it from the
conversation.

### 2. Find the domain model — look for the split (the critical step)

This step cannot be mechanised; but **the question to ask is fixed**: *are
there two things in this domain that get conflated but have separate life
cycles?*

Do not write a schema before the split is found. A schema built on the wrong
split collapses mid-build and pushes rework onto every phase.

For the split patterns and how to hunt for them, read
**`references/domain-model.md`**.

Output: entities, relationships, and the rationale for *why the split is kept
apart*.

### 3. Build the phases and their gates

Phases are a dependency chain, not a calendar. Put a **gate** (milestone +
go/no-go) at each phase exit. The rule: the next phase's *data to record* must
come from the previous one.

Per phase: purpose, scope, **explicit out-of-scope** (this is what prevents
scope drift), exit criterion.

### 4. Atomise the backlog

Every task: `ID` · epic · layer · **estimate (S/M/L)** · **dependency** ·
**acceptance criterion**.

- Keep the ID scheme fixed (e.g. `F{phase}-{layer}-{no}`) — the tracker, the
  report and the generator all bind to it.
- The acceptance criterion must be **executable**: "the endpoint returns 200",
  "an unauthorised request gets 403". "Works well" is not a criterion.
- The criterion is written **from the consumption side**: *"the user reaches
  X"*, not *"the system produces X"*. These are different sentences, and the
  first does **not** imply the second. A production-side criterion passes when
  production was done correctly — even if the capability is left unreachable.
- **A producing task names its consuming twin.** Any task that produces
  information a user will see either carries the reading surface in its own
  acceptance criterion, or names the ID of the task that brings it
  (`→ F3-FE-03`). Cutting the backlog along layers (BE/FE) makes this gap the
  **default**: it lives between tasks, where no single task's own list can see
  it.
- A task cannot be "partly done"; if it can, it is too big — split it.

> **The concrete failure that produced this rule:** a notification task was
> closed on the criterion *"the relevant event produces a notification"*. The
> endpoints and twelve tests were in place; the front end made not one
> notification call — the user could see no notification at all. One of the
> tests was named `read_all_clears_the_badge`: it was testing **a badge that
> did not exist**. The same class recurred four times in that project (audit
> trail, attachment deletion, password, notifications) and **none of them came
> out of the plan** — all four were noticed by accident.

### 5. Write the quality gates

Two levels:

- **Definition of Done (DoD)** — a shared checklist for every task. Two
  mandatory items: *actually run the acceptance criterion* (the existence of a
  comment, a button or a log line is not the existence of behaviour) and
  *every piece of produced information has a reading surface* (the production
  side alone is not enough).
- **Phase go/no-go** — concrete items verified one by one at the gate.

- **Scenario rehearsal** — the third level, and the most skipped item at any
  gate. DoD and go/no-go audit *what was written*: did the criterion hold, is
  the endpoint reachable. Neither can see **what was never written**. Two
  classes of question surface only here:

  1. **Can the reality of the domain be expressed in the model?** List the
     situations that routinely occur in the field and try them one by one.
     Three outcomes: expressible (fine) · not expressible **but written down
     as a deliberate boundary** (fine — that is a decision) · not expressible
     **and written nowhere** (a finding).
     *An undocumented gap is always worse than a decided boundary.*
  2. **When two features are active at once, whose guarantee breaks?**
     Atomising the backlog (step 4) destroys exactly this defect: once split
     into parts, a fault that exists only at the *intersection* becomes
     invisible. So it is deliberately reassembled at the gate. For each new
     feature, list the existing guarantees it can touch and ask *"does that
     guarantee still hold while this feature is active?"* The two most
     fragile: **derived signals** (anything computed from an absence —
     "untouched for 3 days", "unassigned" — silently changes meaning the
     moment a new state exists) and **guarantees enforced call-site by
     call-site** (a privacy rule applied correctly in five places is pierced
     wholesale by a sixth bulk surface). **Order counts too:** some pairs are
     safe in one direction only.

  **You cannot write that list alone, and must not pretend to.** Ask the
  person who knows the domain; invented plausible scenarios are fiction
  wearing an evidence label. **And the scenarios are written BEFORE the
  finding:** a scenario written afterwards finds what it was written to find
  and proves nothing about coverage (HARKing). So the rule matters more than
  the list: **every new phase adds its own scenarios when the phase opens**,
  not when it reaches the gate.

  A green test suite is not counter-evidence here: tests are written per
  feature, so they speak about the parts and stay silent about the pair.

### 6. Set up tracking and the generator

- **Tracker** (`tracker.xlsx`): the backlog row by row, plus
  Status/Owner/Date. `scripts/backlog_to_tracker.py` produces it from the
  backlog markdown.
- **Report** (`report.html`): a derivative of the tracker. Numeric regions sit
  between `GEN:...:BEGIN/END` markers; **the script touches only those**, and
  the rest stays hand-editable.
- **Generator** (`scripts/progress.py`): reads the tracker, computes
  **effort-weighted** progress, regenerates the report's marked regions.

Setup and contracts: read **`references/tracking.md`**.

### 7. Hand off

When the kit is complete:

- **mizan** → audit the kit's own claims (evidence tiers, Gap Map). Put every
  sentence that says "verified" through a counter-example sweep.
- **kiyas** → generate missing-feature and risk candidates; they re-enter the
  backlog as tasks.

The handoff is a file, not prose. Two adapters carry it:

```bash
python scripts/iskele_to_registry.py --backlog 03-gorev-listesi.md --out registry.yaml
python scripts/kiyas_to_backlog.py --seeds tohumlar.yaml --phase F2 --out yeni.md
```

Every acceptance criterion is a refutation condition written before the work
started — precisely what Mizan's R1 asks for. So the backlog is already a
preregistration set; the adapter converts it into the schema Mizan reads, and
in the other direction Kiyas's "cheapest refutation" becomes an acceptance
criterion directly.

**The arbiter defaults to `author`, and it should stay that way.** The person
doing the work fills in the tracker's `Durum` (status) column; that is
self-report, not measurement, and Mizan closes promotion to K on it. If a
task's arbiter really is executable, name it in the backlog:

```markdown
- *Kabul:* Yetkisiz istek 403 alır. **Hakem:** pytest tests/test_authz.py
```

The adapter will not upgrade the class unless you write it — a silent
promotion is the most expensive kind of silent assumption.

**The handoff is also a context cut point.** In a long session every turn
re-sends the whole conversation: the cost grows with the transcript, not with
the finding. The moment the kit is written to files there is no reason to
carry that weight — the next phase can start in a **fresh session**, because
everything it needs (backlog, ADR log, tracker, handoff note) is on disk. Say
so explicitly at the phase boundary; carrying the whole history forward out of
habit defeats the kit's reason to exist.

The everyday version of the same principle: **read ranges, not files** (search
first, then open the lines you need), **give fan-out searching to a subagent**
(let it return a conclusion, not raw material), and **write a finding to the
file the moment it is produced** — a finding saved for the end is paid for on
every turn and lost at the first context reset.

The loop closes: **iskele builds → mizan weighs → kiyas generates → back into
iskele.**

## The output manifest

The full kit is ten pieces. On a small project you may shorten it, but **say
which piece you skipped and why** — never silently.

| # | File | Required | Function |
|---|---|---|---|
| 00 | `00-BASLA-rehber.md` | ✓ | Map of the kit, reading order, working discipline |
| 01 | `01-mimari-ve-veri-modeli.md` | ✓ | Domain model, schema, architectural decisions |
| 02 | `02-yol-haritasi.md` | ✓ | Phases, gates, dependency chain |
| 03 | `03-gorev-listesi.md` | ✓ | Atomic backlog, acceptance criteria |
| 04 | `04-kalite-kapilari.md` | ✓ | DoD + go/no-go + security list |
| 05 | `05-gelistirme-kurulumu.md` | — | Local environment, run steps |
| 06 | `06-riskler-ve-kararlar.md` | ✓ | Risk register + ADRs (decision rationale) |
| 07 | `07-ilerleme-raporu.html` | ✓ | High-level report (GEN-marked) |
| 08 | `tracker.xlsx` | ✓ | Live tracking sheet |
| 09 | `08-onboarding.md` | — | One page of context for the team |

The file names above come from the templates in `assets/templates/` and are
**examples**; the **order and the fields** are what must not change (see the
language note below).

### Reading surface — the kit grows, the handoff cost must not

The manifest says **which** pieces exist; this section says **how large** they
may get. Because if the kit's handoff is cheap the session can be cleared, and
that cheapness is not self-maintaining.

Two files are append-only by nature and must stay that way: the ADR log (a
decision's rationale is never deleted) and the closed part of the backlog (the
evidence for an acceptance criterion is never deleted). Both are correct rules.
**Their intersection is expensive:** the handoff surface grows without bound
until "clear it and continue from the files" costs more than continuing to
talk — which inverts the kit's reason to exist.

Three moves, all the same pattern — **the source stays, what is read shrinks**:

- **A generated index.** The ADR log is reduced to a one-line index (number,
  decision, summary, status). The index is read first; a decision's full text
  is opened **when needed**. The index is **generated, not hand-maintained** —
  every hand-kept number goes stale the moment nobody looks at it (a measured
  case: a hand-kept summary table said 79 while the truth was 87).
- **Closed work to the archive.** The full text of completed phases moves to
  `arsiv/`; the live backlog carries **open work**. It moves, it is **not
  deleted** — the evidence stays where it is.
- **Numbers come from the tracker, not from the text.** Archiving does not
  change the percentage, because progress is derived from `tracker.xlsx`.
  Write that distinction down: archiving is a **reading** decision, not a
  scope decision. Confused, it looks like deleting work, and nobody does it.

**When:** at a phase close — the handoff is being written at that moment
anyway (step 7).

**A measured example, including the part that lowers expectations.** On one
project the handoff surface fell from 420 KB to 133 KB (ADR log: 177 KB of
source → 19 KB of index, 9x); the arbiters and the progress generator were
unaffected. **But when the same handoff task was given to two fresh agents,
the token difference was only 16%** — while bytes fell 3.2x. The ratio does
not carry, because the agent reads what it needs rather than the whole file.
**Write it that way:** "we shrank the reading surface" is true in bytes and
still overstates the token gain. The index's real benefit is not size but
**direction** — the indexed agent ran the generator and got the exact number,
while the other read an estimate out of the prose. Justify it by going to the
right place, not by size.

Templates: `assets/templates/`. The rationale for the piece list and what each
file contains: **`references/kit-manifest.md`**.

## Operating assumptions (this skill runs inside someone else's setup)

Iskele is loaded into an environment that already has its own instructions — a
project's `CLAUDE.md`, org policy, other skills — and **those take
precedence.** The resulting failure is quiet: a plan is still *produced*, it
just stops being a kit and becomes prose. And a prose roadmap is exactly what
this skill exists to prevent.

- **Name the conflict; do not comply silently.** Write down which host
  instruction disabled which step and what the output can no longer claim,
  then let the user decide. The three most common: a **brevity cap** (the
  first thing cut is the measurable half of the acceptance criteria — the one
  property that makes a backlog a preregistration set), a **"write code, don't
  plan" directive** (which silences this skill exactly where it should fire),
  and a **pinned output language** (see below).
- **Language: this file being in English does not mean the kit will be in
  English.** The file names (`03-gorev-listesi.md`), column headings and status
  values used here are **examples, not requirements**; the kit is produced in
  the user's language. The one thing that does not change is the
  **structure**: the same file order, the same fields, the `GEN:` markers, and
  the column keys the scripts read. Translate the names, never the schema —
  the scripts look at the schema. (The Turkish originals of this file and of
  the three references are kept in the repository under `docs/tr/`.)
- **Check a tool before assuming it.** `backlog_to_tracker.py` and
  `progress.py` need **openpyxl**. If it is missing: **say so**, and offer an
  explicit alternative (a CSV tracker, or waiting for the install and
  continuing with the backlog). **Silently saying "here is what the table
  would look like" instead of producing the tracker is a production-side claim
  itself** — step six appears done and there is nothing trackable. The same
  goes for subagents and shell access: if it is absent, the method must not
  depend on it.
- **Read the references on demand** (`domain-model.md` at step 2,
  `tracking.md` at step 6), not all of them up front — reading everything at
  the start spends the context the kit itself needs.
- **The scripted part is the part that travels.** `backlog_to_tracker.py` and
  `progress.py` run without a model: whatever anyone's `CLAUDE.md` says, the
  same backlog yields the same tracker and the same tracker yields the same
  percentage. Anything forced only by this prose is negotiable by the host's
  prose. **If you want a rule to survive an unknown setup, put it in a script,
  not in a paragraph** — which is the arbiter rule of step 5 applied to itself.

## Red lines

These are real failure patterns; each has been seen in the field.

**False precision.** Do not present estimates as exact numbers. "~78.5 days"
may be arithmetically correct and is still speculative *as a duration
estimate*: the weights are the author's choice and there is no velocity data.
When you give effort numbers, state the basis and that they are uncalibrated;
recalibrate once the first phase lands.

**Happy-path verification.** Before saying "verified", ask: *with what input?*
Verification run on well-behaved data never tests input validation. Try at
least one edge case (invalid value, empty record, localised text).

**Silent assumption.** The generator must not fall back to a default for an
unknown value; warn visibly, or do not write it. A silently wrong indicator is
worse than a missing one. (In mixed Turkish/English data the `ı/i` folding is
the classic trap.)

**Skipping phases and scope drift.** Do not enter the next phase before the
gate is passed; write each phase's out-of-scope list explicitly.

**Auditing your own work.** If you produced the kit and you are also auditing
it, arbiter = author. Declare it plainly, and stop treating judgement claims
as proven.

**Invented numbers.** Every number in the report is either computed from data
or marked as an estimate. If it is neither, do not write it.

## References

- `references/domain-model.md` — Step 2: patterns and questions for finding the split
- `references/kit-manifest.md` — Steps 1–5: what each file contains and why
- `references/tracking.md` — Step 6: tracker schema, GEN markers, generator setup
- `assets/templates/` — templates to fill in
- `scripts/backlog_to_tracker.py` — backlog markdown → `tracker.xlsx`
- `scripts/progress.py` — `tracker.xlsx` → update the report's GEN regions
- `scripts/iskele_to_registry.py` — Step 7: backlog → Mizan registry (preregistration)
- `scripts/kiyas_to_backlog.py` — Step 7: Kiyas seeds → backlog tasks
