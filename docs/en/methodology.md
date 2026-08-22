# İskele — Methodology (English counterpart of the skill)

> This document is the English counterpart of the four files inside
> `iskele.skill`: `SKILL.md`, `references/domain-model.md`,
> `references/kit-manifest.md` and `references/tracking.md`. **Those files
> are written in Turkish**, and this is the mirror image of the family's
> usual arrangement — in Mizan, Kıyas and ux-mizan the skill body is
> English and the Turkish docs are its counterpart. Here it runs the other
> way, so this file exists for the same reason theirs do.
>
> The skill notes this itself: *"this file being in Turkish does not mean
> the kit will be in Turkish"*. File names, column headings and status
> values are **examples, not requirements** — the kit is produced in the
> user's language. **What never changes is the structure**: the same file
> order, the same fields, the `GEN:` markers, and the column keys the
> scripts read. Translate the names, never the schema — the scripts look
> at the schema.

---

## Why this skill exists

Planning output fails in two typical ways:

1. **A plan you cannot execute** — a handsome roadmap, but "what do I do
   today" is unclear; tasks are not atomic, there are no acceptance
   criteria, and whether something is finished is open to argument.
2. **A plan you cannot track** — a task list exists, but progress is
   estimated by hand, so the report reflects the author's feeling rather
   than the state of the work.

İskele closes both: every task is atomic and carries an acceptance
criterion, progress is **computed** from data, and the report is a
derivative of the tracker.

**The three verbs are kept in three tools:** İskele builds · Mizan weighs ·
Kıyas generates. If the question is about evidence, go to Mizan; if it is
about ideas or being stuck, go to Kıyas.

**Use it** for a new project, product or major feature; for an existing
project with no backlog, tracking or acceptance criteria; when the question
is "where do I even start".

**Do not use it** for a single-file change (just do it), for pure ideation
(Kıyas), for auditing existing claims (Mizan), or for an urgent bug (fix it
first).

---

## The core loop — seven steps

Do not reorder them. Each step consumes the previous one's output; a
skipped step collapses in the next.

### 1. Elicit the constraints (ask; do not assume)

Architecture is decided by constraints, not preferences. Settle at least:
where it runs (on-prem / cloud / desktop / mobile), scale and identity (how
many users, is SSO mandatory, multi-tenant?), which deliverable is wanted
**now** (a plan, a prototype, both), and the hard constraints (existing
stack, regulation, deadline, team size).

Ask in **one round**, never more than three questions, and never re-ask
what the user already said.

### 2. Find the domain model — look for the split (the critical step)

This step cannot be mechanised, but **the question to ask is fixed**:

> Are there two things in this domain that get conflated but have
> **separate life cycles**?

The test: when A changes, must B change too? If **no**, they are separate
entities and belong in separate tables. Do not write a schema before the
split is found — a schema built on the wrong split collapses mid-build and
pushes rework onto every phase.

**Recurring split patterns:**

| Pattern | A (slow-changing) | B (fast-produced) | Example domain |
|---|---|---|---|
| **Definition / Instance** | Template, procedure, recipe | One run of that template | Process management, workflow, exams, checklists |
| **Catalogue / Order** | Product definition, price list | A placed order line | E-commerce, procurement |
| **Rule / Assessment** | Policy, formula, tariff | The result applied to one event | Insurance, billing, scoring |
| **Plan / Actual** | Budget, schedule, route | Real spend, record, trace | Project management, logistics |
| **Identity / Event** | Person, asset, account | What happens to it | CRM, accounting, IoT |
| **Version / Snapshot** | Live document | Published frozen copy | Documents, contracts, legislation |

A domain can carry several patterns at once. Name them all.

**Three questions that surface the split:**

1. **The retrospection question:** will someone ask, six months from now,
   "how were we doing this back then?" If yes, you need a frozen-copy
   mechanism; projecting the live record backwards destroys that answer.
2. **The multiplication question:** which record is written once, and which
   is produced anew on every use? Different rates of multiplication mean
   different entities.
3. **The ownership question:** who may change this, and who only uses it?
   Different permission classes usually indicate different entities.

**Three mandatory decisions once the split is found:**

- **Freezing.** Which state of A produced B — a reference, or a copy? A
  reference means B's history breaks when A changes. If history matters,
  **copy and freeze** (snapshot); do not merely point.
- **Identity traceability.** The frozen copy must be traceable back to the
  live record (`source_id` + `version`) without depending on it.
- **Permission asymmetry.** Editing A is usually a narrow permission and
  producing B a broad one. Model this from the start; retrofitting hurts.

**Anti-patterns:** the single-table temptation ("both are steps, one table")
crushes two life cycles into one place; polymorphic ownership
(`owner_type` + `owner_id`) is practical but **cannot enforce a foreign
key** — acceptable at small scale as a deliberate trade-off, written down,
never silent; and premature generalisation (a rule engine on an unvalidated
model).

**The vertical-slice rule.** The first build task after the model is a
**vertical slice**: one small flow running end to end, database to screen.
Finishing layers separately and meeting the surprise at integration is the
most expensive source of rework.

### 3. Build the phases and their gates

Phases are a dependency chain, not a calendar. Put a **gate** (milestone +
go/no-go) at each phase exit. The rule: the next phase's *data to record*
must come from the previous one.

Per phase: purpose, scope, **explicit out-of-scope** (this is what prevents
scope drift), exit criterion.

### 4. Atomise the backlog

Every task: `ID` · epic · layer · **estimate (S/M/L)** · **dependency** ·
**acceptance criterion**.

- Keep the ID scheme fixed (e.g. `F{phase}-{layer}-{no}`) — the tracker,
  the report and the generator all bind to it.
- The acceptance criterion must be **executable**: "the endpoint returns
  200", "an unauthorised request gets 403". "Works well" is not a criterion.
- **Write it from the consumption side:** *"the user reaches X"*, not *"the
  system produces X"*. These are different sentences, and the first does
  **not** imply the second. A production-side criterion passes when
  production was done correctly — even if the capability is left
  unreachable.
- **A producing task names its consuming twin.** Any task that produces
  information a user will see either carries the reading surface in its own
  acceptance criterion or names the ID of the task that brings it
  (`→ F3-FE-03`). Cutting the backlog along layers (BE/FE) makes this gap
  the **default**: it lives between tasks, where no single task's list can
  see it.
- A task cannot be "partly done". If it can be, it is too big — split it.

> **The concrete failure that produced this rule:** a notification task was
> closed on the criterion *"the relevant event produces a notification"*.
> The endpoints and twelve tests were in place; the front end made not one
> notification call — no user could see any notification. One of the tests
> was called `read_all_clears_the_badge`: it was testing **a badge that did
> not exist**. The same class recurred four times in that project, and
> **none of them came out of the plan** — all four were noticed by accident.

### 5. Write the quality gates

**Definition of Done** — a shared checklist per task, with two mandatory
items: *actually run the acceptance criterion* (the existence of a comment,
a button or a log line is not the existence of behaviour), and *every
piece of produced information has a reading surface* (the production side
alone is not enough).

**Phase go/no-go** — concrete items verified one by one at the gate.

**Scenario rehearsal** — the third level, and the most skipped. DoD and
go/no-go audit *what was written*: did the criterion hold, is the endpoint
reachable. Neither can see **what was never written**. Two classes of
question surface only here:

1. **Can the reality of the domain be expressed in the model?** List the
   situations that routinely occur in the field and try each. Three
   outcomes: expressible (fine) · not expressible **but recorded as a
   deliberate boundary** (fine — that is a decision) · not expressible
   **and recorded nowhere** (a finding). *An undocumented gap is always
   worse than a decided boundary.*
2. **When two features are active at once, whose guarantee breaks?**
   Atomising the backlog (step 4) destroys exactly this defect: split into
   parts, a fault that exists only at the intersection becomes invisible.
   So it is deliberately reassembled at the gate. For each new feature,
   list the existing guarantees it can touch and ask *"does that guarantee
   still hold while this feature is active?"* The two most fragile:
   **derived signals** (anything computed from an absence — "untouched for
   3 days", "unassigned" — silently changes meaning when a new state
   appears) and **guarantees enforced call-site by call-site** (a privacy
   rule applied correctly in five places is pierced wholesale by a sixth
   bulk surface). **Order counts too:** some pairs are safe in one
   direction only.

**You cannot write that list alone, and must not pretend to.** Ask the
person who knows the domain; invented plausible scenarios are fiction
wearing an evidence label. **And scenarios are written BEFORE the finding:**
a scenario written afterwards finds what it was written to find and proves
nothing about coverage (HARKing). So the rule matters more than the list:
**every new phase adds its own scenarios when the phase opens**, not when
it reaches the gate.

A green test suite is not counter-evidence here: tests are written per
feature, so they speak about the parts and are silent about the pair.

### 6. Set up tracking and the generator

```
03-backlog.md ──backlog_to_tracker.py──> tracker.xlsx ──progress.py──> 07-report.html
   (source)                                (live state)                 (GEN regions)
```

The backlog is the source of "what will be done"; the tracker carries daily
state; the report is the readable view. Do not keep them in sync by hand —
run the generator.

**Tracker schema** (sheet `Takip`; the generator looks for these column
keys): `ID`, `Faz`, `Epik`, `Gorev`, `Katman`, `Tahmin`, `Bagimlilik` are
generated from the backlog; `Durum`, `Sorumlu`, `Baslangic`, `Bitis`, `Not`
are filled by hand; `Hakem` is generated from the acceptance criterion and
may be empty. The `Hakem` column is appended **at the end**, never inserted,
because the `Ozet` formulas and the dropdown validation depend on `Durum`
staying in its column.

Keep sheet and column names ASCII; Turkish characters create cross-platform
friction in file and column matching. Cell *contents* can be in any
language — the generator handles the `ı/i` folding.

**Effort-weighted progress:**

```
progress % = Σ(effort of completed tasks) / Σ(effort of all tasks)
```

Weighted by **effort**, not task count: a four-day task must not count the
same as a 0.75-day one. Default weights `S=0.75 · M=1.5 · L=4` (work-days);
if you change them, change them in all three places (backlog scale, config,
report footnote).

**The credit rule.** Only `Tamamlandi` earns credit. Giving partial credit
to `Devam` inflates progress and manufactures the "almost done" illusion;
if you do it, do it deliberately and write it in the report.

**The arbiter column and the second indicator.** If the acceptance
criterion says `**Hakem:** pytest tests/test_authz.py`, the generator moves
it into the `Hakem` column. If you do not write one, the column stays empty
— that is normal and **is not invented**. The report prints this as its own
region: *how much of the completed effort names an arbiter other than the
author.* Two cautions: it **does not change the progress percentage**
("done" and "verified" are two different things, and melting them into one
indicator makes both unreadable), and it does not show that the criterion
was actually run — no tracker can know that; the Definition of Done knows
it. On older trackers with no `Hakem` column the indicator prints **"not
measured", not 0%.** Showing an unmeasured thing as zero is the most
expensive kind of silent assumption: it looks like a measurement.

### 7. Hand off

When the kit is complete: **Mizan** audits the kit's own claims (evidence
tiers, Gap Map) — put every sentence saying "verified" through a
counter-example sweep. **Kıyas** generates missing-feature and risk
candidates, which re-enter the backlog as tasks.

The handoff is a file, not prose. Two adapters carry it:

```bash
python scripts/iskele_to_registry.py --backlog 03-gorev-listesi.md --out registry.yaml
python scripts/kiyas_to_backlog.py --seeds seeds.yaml --phase F2 --out new.md
```

**Every acceptance criterion is a refutation condition written before the
work started** — precisely what Mizan's R1 asks for. So the backlog is
already a preregistration set; the adapter converts it into the schema
Mizan reads, and in the other direction Kıyas's "cheapest refutation"
becomes an acceptance criterion directly.

**The arbiter defaults to `author`, and it should stay that way.** The
person doing the work fills in `Durum`; that is self-report, not
measurement, and Mizan closes promotion to `[K]` on it. If a task's arbiter
really is executable, name it in the backlog — the adapter will not upgrade
the class unless you write it, and a silent promotion is the most expensive
kind of silent assumption.

**The handoff is also a context cut point.** In a long session every turn
re-sends the whole conversation: the cost grows with the transcript, not
with the finding. Once the kit is on disk there is no reason to carry that
weight — the next phase can start in a **fresh session**, because
everything it needs (backlog, ADR log, tracker, handoff note) is in files.
Say so explicitly at the phase boundary. The daily version of the same
principle: **read ranges, not files**; give fan-out searching to a subagent
so it returns a conclusion rather than raw material; and **write a finding
to the file the moment it is produced** — a finding saved for the end is
paid for on every turn and lost at the first context reset.

The loop closes: **İskele builds → Mizan weighs → Kıyas generates → back
into İskele.**

---

## The output manifest

The full kit is ten pieces. On a small project you may shorten it, but
**say which piece you skipped and why** — never silently.

| # | File | Required | Function |
|---|---|---|---|
| 00 | `00-START-guide.md` | ✓ | Map of the kit, reading order, working discipline |
| 01 | `01-architecture-and-data-model.md` | ✓ | Domain model, schema, architectural decisions |
| 02 | `02-roadmap.md` | ✓ | Phases, gates, dependency chain |
| 03 | `03-backlog.md` | ✓ | Atomic backlog, acceptance criteria |
| 04 | `04-quality-gates.md` | ✓ | DoD + go/no-go + security list |
| 05 | `05-dev-setup.md` | — | Local environment, run steps |
| 06 | `06-risks-and-decisions.md` | ✓ | Risk register + ADRs |
| 07 | `07-progress-report.html` | ✓ | High-level report (GEN-marked) |
| 08 | `tracker.xlsx` | ✓ | Live tracking sheet |
| 09 | `08-onboarding.md` | — | One page of context for the team |

(The Turkish file names in the skill are the examples; these are their
English equivalents. The **order and the fields** are what must not change.)

### Reading surface — the kit grows, the handoff cost must not

Two files are append-only by nature and must stay that way: the ADR log (a
decision's rationale is never deleted) and the closed part of the backlog
(the evidence for an acceptance criterion is never deleted). Both are right
rules. **Their intersection is expensive:** the handoff surface grows
without bound until "clear the session and continue from the files" costs
more than continuing to talk — which inverts the kit's reason to exist.

Three moves, all the same pattern — **the source stays, what is read
shrinks**:

- **A generated index.** The ADR log is reduced to a one-line index
  (number, decision, summary, status). The index is read first, and a
  decision's full text is opened **when needed**. The index is
  **generated, not maintained by hand** — every hand-maintained number goes
  stale the moment nobody looks at it (a measured case: a hand-kept summary
  table said 79 while the truth was 87).
- **Closed work to the archive.** The full text of completed phases moves
  to `archive/`; the live backlog carries **open work**. It moves, it is
  **not deleted** — the evidence stays where it is.
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
not carry, because an agent reads what it needs rather than the whole file.
**Write it that way:** "we shrank the reading surface" is true in bytes and
overstates the token gain. The index's real benefit is not size but
**direction** — the indexed agent ran the generator and got the exact
number, while the other read an estimate out of the prose. Justify it by
going to the right place, not by size.

---

## Operating assumptions (this skill runs inside someone else's setup)

İskele is loaded into an environment that already has its own instructions
— a project's `CLAUDE.md`, org policy, other skills — and **those take
precedence.** The resulting failure is quiet: a plan is still *produced*,
it just stops being a kit and becomes prose. And a prose roadmap is exactly
what this skill exists to prevent.

- **Name the conflict; do not comply silently.** Say which host instruction
  disabled which step and what the output can no longer claim, then let the
  user decide. The three most common: a **brevity cap** (the first thing
  cut is the measurable half of the acceptance criteria — the single
  property that makes a backlog a preregistration set), a **"write code,
  don't plan" directive** (which silences this skill exactly where it
  should fire), and a **pinned output language**.
- **Language.** This skill's own files being Turkish does not mean the kit
  will be. File names, column headings and status values are examples; the
  kit is produced in the user's language. **The structure is what does not
  change:** the same file order, the same fields, the `GEN:` markers, the
  column keys the scripts read. Translate the names, not the schema.
- **Check a tool before assuming it.** `backlog_to_tracker.py` and
  `progress.py` need **openpyxl**. If it is missing: **say so**, and offer
  an explicit alternative (a CSV tracker, or continuing with the backlog
  until it is installed). **Silently substituting "here is what the table
  would look like" for the tracker is a production-side claim** — step six
  appears done and nothing is trackable. The same goes for subagents and
  shell access.
- **Read the references on demand** — `domain-model.md` at step 2,
  `tracking.md` at step 6 — not all of them up front, which spends the
  context the kit itself needs.
- **The scripted part is the part that travels.** `backlog_to_tracker.py`
  and `progress.py` run without a model: whatever anyone's `CLAUDE.md`
  says, the same backlog yields the same tracker and the same tracker
  yields the same percentage. Anything enforced only by this prose is
  negotiable by the host's prose. **If you want a rule to survive an
  unknown setup, put it in a script, not in a paragraph** — which is the
  arbiter rule of step 5 applied to itself.

---

## Red lines

Real failure patterns; each has been seen in the field.

**False precision.** Do not present estimates as exact numbers. "~78.5
days" may be arithmetically correct and is still speculative *as a
duration*: the weights are the author's choice and there is no velocity
data. State the basis and that it is uncalibrated; recalibrate after the
first phase lands.

**Happy-path verification.** Before saying "verified", ask *with what
input?* Verification run on well-behaved data never tests input validation.
Try at least one edge case (invalid value, empty record, localised text).

**Silent assumption.** A generator must not fall back to a default for an
unknown value. Warn visibly, or do not write it. A silently wrong indicator
is worse than a missing one.

**Skipping phases and scope drift.** Do not enter the next phase before the
gate is passed; write each phase's out-of-scope list explicitly.

**Auditing your own work.** If you produced the kit and you are also
auditing it, arbiter = author. Declare it, and stop treating judgement
claims as proven.

**Invented numbers.** Every number in the report is either computed from
data or marked as an estimate. If it is neither, do not write it.

---

## Where each topic lives in the skill

| Topic | File |
|---|---|
| The seven steps, the manifest, operating assumptions, red lines | `skill/iskele/SKILL.md` |
| Step 2 — finding the split, patterns, freezing decisions | `references/domain-model.md` |
| Steps 1–5 — what each kit file contains and why | `references/kit-manifest.md` |
| Step 6 — tracker schema, `GEN:` markers, the generator | `references/tracking.md` |
| Fillable templates | `assets/templates/` |
| Backlog → tracker, tracker → report, and the two handoff adapters | `scripts/` |
