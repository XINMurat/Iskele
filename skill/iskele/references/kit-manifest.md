# Kit manifest — what each piece contains, and why it exists

The templates live under `assets/templates/`. This document gives each
piece's **purpose** and its **filling rules**; the templates give the skeleton.

On a small project you may skip a piece — but write down in `00` that you
skipped it, and why.

> File names below follow the templates and are examples. Produce the kit in
> the user's language; keep the **order and the fields** unchanged.

---

## 00 — Guide (`00-BASLA-rehber.md`) · required

The map of the kit. Contains: the file table (what each file is for, when it
is used), the recommended reading order, and the working-discipline rules.

Discipline items (at least these):
- No phase skipping.
- A task is one atomic piece of work; there is no "partly done".
- No "done" without evidence.
- Record the negative finding (do not quietly take another route).

---

## 01 — Architecture and data model · required

See `domain-model.md`. Contains: the domain split and its rationale, entities
and relationships (preferably DDL), the technology choices and **why** they
were chosen, deliberate trade-offs.

Rule: every technology choice must be tied to a constraint ("because it is
on-prem and AD is mandatory, ..."). A choice that cannot be tied to a
constraint is a preference; mark it as one.

---

## 02 — Roadmap · required

Phases, gates, dependency chain.

Per phase: purpose, scope, **out-of-scope (explicit)**, exit criterion, rough
effort. Per gate: the milestone name and a pointer to its go/no-go.

Rule: phases are a dependency order, not a calendar. Apply the test "the next
phase's data to record comes from the previous one".

When giving effort: state the basis (a bottom-up sum of tasks, or a top-down
estimate), mark that it is uncalibrated, and write that you will recalibrate
after the first phase.

---

## 03 — Backlog (`03-gorev-listesi.md`) · required

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

## 04 — Quality gates · required

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

## 05 — Dev setup · optional (but needed on most projects)

Prerequisites with versions, folder structure, step-by-step setup commands, a
verification command ("run this, you should see that"), common problems.

---

## 06 — Risks and decisions · required

**Risk register:** risk, impact, likelihood, mitigation, status. Live for the
whole project.

**ADR (decision record):** for each architectural decision, context → decision
→ rationale → consequence. When you change a decision, do not delete the old
one; mark it "superseded (→ ADR-x)". When a route is blocked, write an ADR
saying "tried it, it did not work, because…" — an unrecorded negative finding
means walking into the same wall a second time.

---

## 07 — Progress report (`.html`) · required

The high-level view. Numeric regions sit between `GEN:...:BEGIN/END` markers;
the generator touches only those. Sections: summary indicators, phase cards,
effort-weighted epic bars, the gate/phase timeline, risks, the ADR list.

Rule: **the report is a derivative of the tracker.** If they contradict, the
tracker is right and the report is corrected. Every number in the report is
either computed or marked as an estimate.

---

## 08 — Tracker (`tracker.xlsx`) · required

The backlog row by row, plus Status/Owner/Date/Note. The `Ozet` (summary)
sheet computes with formulas — do not type numbers into it. Schema:
`tracking.md`.

---

## 09 — Onboarding (`08-onboarding.md`) · optional

Fifteen minutes of context for someone joining: what we are doing, the single
most important idea to understand (the domain split), the stack, the critical
rules, the reading order, and a "which question lives in which file" table.

---

## Quality control — before the kit is handed over

- [ ] Is every number the same in all three places? (backlog ↔ tracker ↔ report)
- [ ] Is every task's acceptance criterion executable?
- [ ] Is every phase's out-of-scope written down?
- [ ] Are the effort basis and its lack of calibration marked?
- [ ] Was the generator tried with broken data? (not only the happy path)
- [ ] Are the skipped pieces and the reason for skipping them written in `00`?
