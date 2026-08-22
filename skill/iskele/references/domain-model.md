# Step 2 — Finding the domain model

This is the one step of the kit that cannot be mechanised. Iskele will not
*find* the split for you; it forces you to look, and mechanises everything
after you have found it. Honesty matters here: the remaining six steps are
template work, this step is judgement.

## The question to ask

> Are there two things in this domain that get conflated but have **separate
> life cycles**?

The separate-life-cycle test: when A changes, must B change too? If the answer
is **no**, they are separate entities and belong in separate tables.

## Recurring split patterns

| Pattern | A (slow-changing) | B (fast-produced) | Example domain |
|---|---|---|---|
| **Definition / Instance** | Template, procedure, recipe | One run of that template | Process management, workflow, exams, checklists |
| **Catalogue / Order** | Product definition, price list | A placed order line | E-commerce, procurement |
| **Rule / Assessment** | Policy, formula, tariff | The result applied to one event | Insurance, billing, scoring |
| **Plan / Actual** | Budget, schedule, route | Real spend, record, trace | Project management, logistics |
| **Identity / Event** | Person, asset, account | What happens to that entity | CRM, accounting, IoT |
| **Version / Snapshot** | Live document | Published frozen copy | Documents, contracts, legislation |

A domain can carry more than one pattern. Name all of them.

## Three questions that surface the split

1. **The retrospection question:** "Six months from now, will someone ask 'how
   were we doing this back then?'" If yes, you need a *frozen copy* mechanism
   that preserves the past; projecting the live record backwards destroys that
   answer.
2. **The multiplication question:** "Which record is written once, and which is
   produced anew on every use?" Different rates of multiplication mean
   different entities.
3. **The ownership question:** "Who can change this, and who only uses it?"
   Different permission classes usually point at different entities.

## Once the split is found — three mandatory decisions

**a) Freezing.** Which state of A produced B? Does it hold a reference or a
copy? With a reference, B's history breaks when A changes. If history matters,
**copy and freeze** (snapshot); do not merely point at it.

**b) Identity traceability.** The frozen copy must be traceable back to the
live record (`source_id` + `version`) without being *dependent* on it.

**c) Permission asymmetry.** Editing A is usually a narrow permission and
producing B a broad one. Model this from the start; retrofitting hurts.

## Anti-patterns

- **The single-table temptation.** "They are both steps, I will keep one
  table" → two life cycles are crushed into one place, and queries and
  permissions tangle.
- **Polymorphic ownership.** `owner_type` + `owner_id` for multi-type
  ownership in one table is practical, but **a foreign key cannot be
  enforced** (risk of orphan rows). Acceptable at small scale; **write it
  down and mark it** as a deliberate trade-off, never silently.
- **Premature generalisation.** Do not build a branching or rule engine on a
  model that has not been validated yet. Get the flat version working first
  (see the vertical slice).

## Output: what to write

In `01-mimari-ve-veri-modeli.md` (or its equivalent in your language):

1. The split(s) found and **why they are kept apart** (one paragraph).
2. The entity list and relationships (preferably executable DDL).
3. If there is a freezing mechanism, its structure and its verification test:
   *"change A → the old B must not change"*. This test goes into the gate
   (go/no-go).
4. Deliberate trade-offs (what are we losing, when will we revisit).

## The vertical-slice rule

Once the model is in place, the first build task must be a **vertical slice**:
run one small flow end to end, from the database to the screen. "Finishing"
the layers separately and meeting the surprise at integration is the most
expensive source of rework. If the vertical slice does not run, the model or
the infrastructure is not really connected.
