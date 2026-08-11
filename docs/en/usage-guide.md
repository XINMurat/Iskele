# İskele — Usage Guide (EN)

The Turkish original of the methodology text lives in
[`../tr/kullanim-kilavuzu.md`](../tr/kullanim-kilavuzu.md); the skill itself
([`skill/iskele/SKILL.md`](../../skill/iskele/SKILL.md)) is written in Turkish
and is the normative source. This guide is the English walkthrough of the same
seven-step loop.

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

The loop closes: **İskele builds → Mizan weighs → Kıyas generates → back into
İskele.**

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
