<!-- GENERATED PAGE - do not edit here.
     Source of truth: skill/iskele/references/kit-manifest.md
     Regenerate:      python tools/sync_en_docs.py
     CI (`--check`) fails if this page drifts from its source. -->

# Kit manifest — what each piece contains

> **Mirrored from the skill package.** This is the canonical English text that
> Claude actually loads, published here so it can be read next to its Turkish
> mirror instead of only on GitHub. Edit the source above, not this
> page; the Turkish mirror is `docs/tr/kit-manifesti.md`.

## Kit manifest — what each piece contains, and why it exists

The templates live under `assets/templates/`. This document gives each
piece's **purpose** and its **filling rules**; the templates give the skeleton.

On a small project you may skip a piece — but write down in `00` that you
skipped it, and why.

> File names below follow the templates and are examples. Produce the kit in
> the user's language; keep the **order and the fields** unchanged.

---

### 00 — Guide (`00-BASLA-rehber.md`) · required

The map of the kit. Contains: the file table (what each file is for, when it
is used), the recommended reading order, and the working-discipline rules.

Discipline items (at least these):
- No phase skipping.
- A task is one atomic piece of work; there is no "partly done".
- No "done" without evidence.
- Record the negative finding (do not quietly take another route).

---

### 01 — Architecture and data model · required

See `domain-model.md`. Contains: the domain split and its rationale, entities
and relationships (preferably DDL), the technology choices and **why** they
were chosen, deliberate trade-offs.

Rule: every technology choice must be tied to a constraint ("because it is
on-prem and AD is mandatory, ..."). A choice that cannot be tied to a
constraint is a preference; mark it as one.

---

### 02 — Roadmap · required

Phases, gates, dependency chain.

Per phase: purpose, scope, **out-of-scope (explicit)**, exit criterion, rough
effort. Per gate: the milestone name and a pointer to its go/no-go.

Rule: phases are a dependency order, not a calendar. Apply the test "the next
phase's data to record comes from the previous one".

When giving effort: state the basis (a bottom-up sum of tasks, or a top-down
estimate), mark that it is uncalibrated, and write that you will recalibrate
after the first phase.

---

### 03 — Backlog (`03-gorev-listesi.md`) · required

Format (the generator depends on it — see `tracking.md`):

```markdown
### Epic F1.2 — Process & steps
- [ ] **F1-BE-04** (M) Process CRUD API. **Dep.:** F1-BE-02, F1-BE-03
  - *Acceptance:* Creating and editing a process works with the permission
    check; it starts as a draft.
```

Required fields: ID, estimate `(S|M|L)`, title, dependency, **acceptance
criterion**.

The acceptance-criterion test: *can I verify this by running it?* If not,
rewrite it.

| Bad | Good |
|---|---|
| "Search works well" | "Searching by a word in the title returns results; results from an unauthorised unit do not appear" |
| "Security is added" | "An unauthorised request gets 403; a request with no token gets 401" |

Estimate scale (default): `S≈0.75`, `M≈1.5`, `L≈4` work-days. It can change
per project, but it **must be the same in the backlog, the tracker and the
generator**.

---

### 04 — Quality gates · required

Two sections:

**Definition of Done (DoD)** — applies to every task. Core items:
- The acceptance criterion was **actually run** (not eyeballed).
- The change landed on the main branch.
- If behaviour changed, there is an automated test.
- If it is a new interface, there is a permission check.
- The tracker was updated.
- Blockers and negative findings were recorded.

**Phase go/no-go** — concrete, individually checkable items per gate. Every
gate must include the domain model's critical invariant (e.g. the freezing
test).

---

### 05 — Dev setup · optional (but needed on most projects)

Prerequisites with versions, folder structure, step-by-step setup commands, a
verification command ("run this, you should see that"), common problems.

---

### 06 — Risks and decisions · required

**Risk register:** risk, impact, likelihood, mitigation, status. Live for the
whole project.

**ADR (decision record):** for each architectural decision, **status → context
→ options considered → decision → rationale → consequence.** When you change a
decision, do not delete the old one: a new ADR is written and the old one's
status becomes `superseded → ADR-x`. When a route is blocked, write an ADR
saying "tried it, it did not work, because…" — an unrecorded negative finding
means walking into the same wall a second time.

**The status vocabulary is fixed** — proposed · accepted · rejected ·
deprecated · superseded → ADR-x. An open-ended status field becomes a field
where everyone writes their own word and nothing can be compared. `accepted` is
immutable in practice: if a live ADR can be quietly edited, the reader six
months from now cannot tell which decision was taken when, and the collection's
only claim to trustworthiness is gone.

**Options considered is its own section**, not a clause inside the rationale.
The most expensive part of a decision is the road not taken, and folded into
"rationale" it is the first thing trimmed. **Doing nothing is on the list** —
it is often the real competitor.

`scripts/check_adr.py` enforces the mechanical half: the vocabulary, forward
pointers that actually resolve, a superseded chain that does not loop or end
with nothing in force, and at least two options per decision. It cannot tell
whether a decision was *right* — no script can — which is exactly why the parts
it can check should not be left to prose.

---

### 07 — Progress report (`.html`) · required

The high-level view. Numeric regions sit between `GEN:...:BEGIN/END` markers;
the generator touches only those. Sections: summary indicators, phase cards,
effort-weighted epic bars, the gate/phase timeline, risks, the ADR list.

Rule: **the report is a derivative of the tracker.** If they contradict, the
tracker is right and the report is corrected. Every number in the report is
either computed or marked as an estimate.

---

### 08 — Tracker (`tracker.xlsx`) · required

The backlog row by row, plus Status/Owner/Date/Note. The `Ozet` (summary)
sheet computes with formulas — do not type numbers into it. Schema:
`tracking.md`.

---

### 09 — Onboarding (`08-onboarding.md`) · optional

Fifteen minutes of context for someone joining: what we are doing, the single
most important idea to understand (the domain split), the stack, the critical
rules, the reading order, and a "which question lives in which file" table.

---

### 10 — Recovery ramps (`09-kurtarma-rampalari.md`) · required

The counterpart of piece `04`. The quality gates define "done"; this defines
what happens when done does not arrive — a task that will not close, a passed
gate that stopped holding, a finding with no task, an intent that moved
mid-build.

It is required for the same reason `04` is: without it, the answer to "it
isn't working" is improvised by whoever is at the keyboard, and the most
common improvisation is the cheapest one — loosen the criterion, mark it done,
move on. That is not a discipline problem, it is a missing document.

Contents: a coded ramp table (`RR-nn`, so a ramp is quotable in a commit
message rather than being a paragraph nobody cites), long-form entries for the
two or three most often misapplied, and the phase-close process scorecard that
sits beside the go/no-go.

**Adapt it; do not paste it.** Drop the ramps that cannot occur on this
project and add the ones this domain forces — and write down which were
dropped and why, the same rule the manifest applies to skipped pieces. Every
ramp names an output artifact: a ramp with no output is advice, and this kit
is not an advice document.

Written at step 5, next to the quality gates. Procedure and the full ramp set:
`references/recovery.md`.

---

### 11 — Agent signpost (`AGENTS.md`) · required

The machine-facing entry point. `00` is the human's map of the kit; this is the
agent's, and they are not the same document — an agent needs the build command,
the boundaries and the definition of done, not a reading order.

It is a **signpost, not a rule store.** Every rule already lives in a kit file;
this points at it. That matters because a second copy of a rule is a second
copy that can go stale, and the one an agent reads first is the one that wins.
So the file carries the conflict rule explicitly: *if this contradicts the kit,
the kit wins — and report the contradiction.* Silently obeying one of two
conflicting sources makes both wrong.

`AGENTS.md` is a cross-tool convention rather than this project's invention:
the format came out of work by several agent-tool teams and is now stewarded by
the Agentic AI Foundation. Emitting it means the kit is legible to whichever
agent the team actually uses, not only the one that produced it. In a monorepo
the closest `AGENTS.md` wins, so a sub-package that needs different rules gets
its own.

Keep it short — start at 30-50 lines and add a section only when an agent
repeatedly makes the same mistake. A long signpost is a rule store wearing a
different name, and it will drift from the kit it was supposed to point at.

---

### Quality control — before the kit is handed over

- [ ] Is every number the same in all three places? (backlog ↔ tracker ↔ report)
- [ ] Is every task's acceptance criterion executable?
- [ ] Is every phase's out-of-scope written down?
- [ ] Are the effort basis and its lack of calibration marked?
- [ ] Was the generator tried with broken data? (not only the happy path)
- [ ] Are the skipped pieces and the reason for skipping them written in `00`?
- [ ] Does every recovery ramp in `09` name an output artifact, and is the
      adaptation note (which ramps were dropped, and why) filled in?
