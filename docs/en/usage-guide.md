# İskele — Usage Guide (EN)

The Turkish counterpart is
[`../tr/kullanim-kilavuzu.md`](../tr/kullanim-kilavuzu.md). The normative
source is the skill itself,
[`skill/iskele/SKILL.md`](../../skill/iskele/SKILL.md) — in English; the
Turkish originals of it and of its references are kept under `docs/tr/`. This
guide is the English walkthrough of the same seven-step loop.

## The seven steps

Do not reorder them. Each step consumes the previous step's output; a skipped
step collapses in the next one.

### 1. Extract the constraints — ask, do not assume

Architecture is decided by constraints, not preferences. Settle at least:

- **Where does it run?** on-prem / cloud / desktop / mobile
- **Scale and identity?** how many users, is SSO mandatory, is it multi-tenant
- **Which output is wanted now?** a plan, a prototype, or both
- **Hard constraints?** existing stack, regulation, deadline, team size

Ask in **one round**, at most three questions. If the user already said it, do
not ask again — derive it from the conversation.

### 2. Find the domain model — look for the distinction

The most critical step, and the one that cannot be mechanized. The question,
however, is fixed: *are there two things in this domain that get conflated but
have separate lifecycles?*

Do not write a schema before the distinction is found. A schema built on the
wrong distinction collapses mid-build and pushes rework into every phase.

Patterns and how to hunt for them:
[`references/domain-model.md`](../../skill/iskele/references/domain-model.md).

Output: entities, relationships, and the **reason the distinction is held
apart**.

### 3. Build phases and gates

Phases are a dependency chain, not a calendar. Put a **gate** (milestone +
go/no-go) at the exit of each. The rule: the data the next phase records must
come from the previous one.

Per phase: goal, scope, **explicit out-of-scope** (this is what stops scope
creep), exit criterion.

### 4. Atomize the backlog

Every task carries: `ID` · epic · layer · **estimate (S/M/L)** · **dependency**
· **acceptance criterion**.

- Keep the ID scheme fixed (e.g. `F{phase}-{layer}-{n}`) — the tracker, the
  report, and the generator all key off it.
- Acceptance criteria must be **executable**: "the endpoint returns 200", "an
  unauthorized request gets 403". "Works well" is not an acceptance criterion.
- A task cannot be "partly done". If it can, it is too big — split it.

### 5. Write the quality gates

Two levels:

- **Definition of Done** — a shared checklist per task. Mandatory item:
  *actually execute the acceptance criterion*. The existence of a comment, a
  button, or a log line is not the existence of the behaviour.
- **Phase go/no-go** — concrete items verified one by one at the gate.
- **Recovery ramps** — piece `09`, the counterpart of the gates: what to do
  when a task will not close, a passed gate stops holding, or the intent moves
  mid-build. Adapt the template rather than pasting it; the ramps and the
  procedure are in
  [`references/recovery.md`](../../skill/iskele/references/recovery.md).

### 6. Set up tracking and the generator

- **Tracker** (`tracker.xlsx`): the backlog row by row plus
  Status/Owner/Dates. `backlog_to_tracker.py` builds it from the backlog
  markdown.
- **Report** (`report.html`): a derivative of the tracker. Numeric regions sit
  between `GEN:...:BEGIN/END` markers; **the script touches only those**, the
  rest stays hand-editable.
- **Generator** (`progress.py`): reads the tracker, computes **effort-weighted**
  progress, regenerates the marked regions.

Contracts and setup:
[`references/tracking.md`](../../skill/iskele/references/tracking.md).

### 7. Hand off

- **Mizan** → audit the kit's own claims (evidence tiers, gap map).
- **Kıyas** → generate missing feature and risk candidates; they re-enter the
  backlog.

The loop closes — and it is two loops, not one ring: **Mizan ⇄ Kıyas** can turn
between themselves for as long as the thinking needs, with nothing being built,
while **İskele** is the branch taken when something survives and is worth
building. Its criteria then return to Mizan as preregistered entries.

## What the loop gained in v1.x

The seven steps above are the stable core. These were added on top of them,
each from a failure seen in a real project; the normative text is
[`SKILL.md`](../../skill/iskele/SKILL.md) and the references it names.

- **Acceptance criteria are written from the consumption side** — "the user
  reaches X", not "the system produces X". A production-side criterion passes
  even when the capability is unreachable. And **a producing task names its
  consuming twin**: anything that produces information a user will see either
  carries the reading surface in its own criterion or names the task that
  brings it (`→ F3-FE-03`). Cutting the backlog by layer makes that gap the
  default.
- **Scenario rehearsal at the gate** — the level DoD and go/no-go cannot see:
  can the domain's real situations be expressed in the model (expressible,
  a written boundary, or a finding), and **when two features are active at
  once, whose guarantee breaks?** The answer lives in the tracker's `Cift`
  sheet, one row per pair, and the report prints it as `GEN:CIFT` with the
  unchecked pairs counted separately. Scenarios come from the domain owner and
  are written when a phase opens, not when it reaches the gate.
- **`check_adr.py` at go/no-go** — validates the ADR chain in piece `06`:
  status vocabulary, forward pointers that resolve, supersede consistency, and
  that each decision lists the options it weighed.
- **Piece `11`, `AGENTS.md`** — the machine-facing signpost: what this project
  is, where each rule lives, what is forbidden.
- **The reading surface stays small** — the ADR log is read through a
  generated one-line index, and closed phases move to `arsiv/` (moved, never
  deleted). Archiving is a reading decision, not a scope decision: the
  percentage comes from the tracker either way.
- **The expectation delta** — an optional `GercekEfor` column (effort actually
  worked, not elapsed time) yields actual / estimated effort, and
  `estimate_basis` in the config decides what that number may be called
  (`unknown` by default). Unit cost is reported with two denominators, and
  `tools/session_cost.py` totals real token usage from local Claude Code
  transcripts — attributing a session to a task stays a human judgement,
  marked `[H]`.
- **The handoff is files, both ways** — `iskele_to_registry.py` turns the
  backlog into Mizan preregistrations, `kiyas_to_backlog.py` turns Kıyas seeds
  into tasks, and `iskele_results.py` writes completed tasks back to the
  registry as results. It appends only and never changes a tier: promotion is
  someone else's decision.

## Red lines

Real failure patterns, each observed in practice.

**False precision.** Do not present estimates as precise numbers. "~78.5 days"
may be arithmetically correct and still be speculative *as a duration
estimate*: the weights are an author's choice and there is no velocity data.
Give the basis, say it is uncalibrated, recalibrate after phase one.

**Happy-path verification.** Before saying "verified", ask *with what input?*
A check that runs on well-behaved data never tests input validation. Try at
least one edge case.

**Silent assumption.** The generator must not quietly fall back to a default for
an unknown value — warn visibly or refuse to write. A silently wrong indicator
is worse than a missing one. (The `ı`/`i` fold in mixed Turkish/English data is
the classic trap.)

**Phase skipping and scope creep.** Do not enter the next phase before the gate
is passed; write each phase's out-of-scope list explicitly.

**Auditing your own work.** If you produced the kit and you also audit it, the
arbiter is the author. Declare it, and stop treating judgment claims as
established.

**Invented numbers.** Every number in the report is either computed from data or
marked as an estimate. If neither, do not write it.
