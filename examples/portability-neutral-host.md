<!-- =====================================================================
Worked example — does İskele hold up in a host that neither helps nor hinders?
Çalışılmış örnek — ne destekleyen ne engelleyen bir ortamda İskele
===================================================================== -->

# Portability runs — neutral and hostile hosts

A skill loads into a host that already has its own instructions. The
**hostile** case (a `CLAUDE.md` that fights the method) is the obvious worry;
the **neutral** case is the common one — nothing pushes against the method
and **nothing reinforces it either**. There the prose has to carry itself.

**H-4 `[S]` (preregistered, written before the run):** with neither
conflicting nor reinforcing host instructions, İskele still produces a **kit**
rather than a prose roadmap.

**Failure mode probed:** a well-written phased plan in the chat window, with
manifest pieces quietly skipped and nothing on disk to track.

## Harness

One fixture, `BRIEF.md` — a vague real intent: lab-equipment calibration
tracking, currently a shared spreadsheet, has twice caused a failed audit.
400 instruments, 6 labs, intervals of 3/6/12/24 months, certificates retained
7 years, unannounced auditors. Team of two, nothing started, *"we do not know
where to begin."*

The brief deliberately withholds several constraints, so step 1 (*ask, do not
assume*) has something to bite on.

Subject: a fresh-context agent, verified beforehand **not** to inherit global
user instructions. Preregistration kept **outside** the working directory.
`openpyxl` present, so the tracker was genuinely producible.

## Pass required all five

| # | Criterion | Outcome |
|---|---|---|
| 1 | Required (✓) manifest parts produced; any omission named with a reason | **pass** — all ten produced, none omitted |
| 2 | Output is **files**, verifiable on disk — not a prose roadmap | **pass** — verified independently after the run |
| 3 | Acceptance criteria written **consumer-side**, not producer-side | **pass** — e.g. *"the instrument list screen shows exactly 10 rows"*, *"a deliberately failing test turns the CI check red and blocks merge"* |
| 4 | Quality gates include the **scenario rehearsal** | **pass** — §3, with the *written when the phase opens* rule carried over |
| 5 | Tracker produced, or explicit degradation declared | **pass** — `tracker.xlsx`, 49 rows, three sheets, opened and counted independently |

**H-4 → `[K]` for this harness.**

## What the run did that the criteria did not ask for

- **It found the domain distinction and built the kit on it.** *The due date
  belongs to the calibration event, not to the instrument.* Storing one "next
  due" per instrument means changing an interval silently rewrites the past —
  including the answer to *"were you compliant in March 2023?"*, which is
  exactly what the auditor asks. The value is frozen at record time and an
  invariant test re-runs at **every** gate, not only the one that introduced it.
- **It left two decisions open on purpose** and marked one as blocking, rather
  than resolving them silently — *"the kind of thing that gets decided by
  accident inside a one-line expression."*
- **It ran the generator against deliberately broken input** (invalid estimate,
  out-of-config phase, a Turkish dotless-ı status string) and confirmed the
  tool normalised what is safely normalisable, errored on the rest, and
  **refused to write the report**.
- **It separated what was verified from what was not**, unprompted: the
  scenario lists in `04` were flagged as *written by me, not by anyone who
  calibrates instruments — a prompt for your lab staff, not evidence*, and
  logged as a risk.

## The run found a real defect in this repository

`backlog_to_tracker.py` did not skip fenced code blocks, so the **format
example** inside a backlog was parsed as a live task: 50 tasks reported where
49 existed, and 1.5 days of phantom effort. Reproduced independently, then
fixed — fences are now skipped, with nesting handled by matching the closing
marker to the opening one.

This is the most valuable thing the run produced, and it is worth naming why
it was findable: the failure was **silent**. The tracker looked correct, the
number looked plausible, and nothing errored. A portability test that only
asked *"did it refuse to work?"* would have missed it entirely.

## Second harness — the hostile host (H-6): refused, and said why

Same fixture, plus a `CLAUDE.md` built from the collisions this skill's own
*Çalışma varsayımları* section names: a 5-bullet cap, **"we do not write
planning documents — write code, not plans"**, **"never create files unless
the user explicitly names the file to create"**, and a pinned output language.

The second rule is the sharp one: it attacks the property that makes İskele a
kit rather than advice.

**Pass required all three:** name the conflict; state what the output can no
longer claim; and **do not silently deliver a prose imitation of a kit.**

| # | Criterion | Outcome |
|---|---|---|
| 1 | Names the conflict | **pass** — quoted both instructions and named the disabled steps (3–7: roadmap, backlog, gates, tracker, report) |
| 2 | States what it can no longer claim | **pass** — *"nothing measurable was produced"*, and the cap *"removes the one property that makes a backlog a preregistration set"* |
| 3 | No silent prose kit | **pass** — **created zero files** (verified on disk afterwards), put three options to the user, and recommended one |

**H-6 → `[K]` for this harness.**

### Why refusing was the correct output

The tempting failure here is not disobedience, it is a *good-looking* phased
plan in the chat window: five confident bullets, nothing on disk, nothing
trackable — and the user believing they have a kit. The run declined that,
named the trade explicitly, and handed the decision back: grant a directory
and get the real kit, drop the kit and go straight to schema and code, or
leave the conflict on record. **A skill that cannot deliver its deliverable
should say so, not deliver a resemblance of it.**

### Cross-run consistency

Both host types, independently, found the same domain distinction from the
brief alone — **the due date belongs to the calibration event, not the
instrument** — and both named it as the reason the unannounced-audit history
request would otherwise be unanswerable. The hostile run produced it *while
refusing the task*, calling it a free finding at no cost. Reading the domain
correctly was not contingent on being allowed to write files.

## What this does NOT establish

- **n = 1 per host type** (neutral, hostile), one fixture, one subject model.
- **Arbiter = author (R8).** `[K]` holds **for this harness**, not generally.
- **The hostile run tested refusal, not degraded delivery.** It confirms the
  skill declines rather than faking a kit; it says nothing about what happens
  under a host that permits files but constrains their content.
- **The language exposure was not stressed.** This run's host was neutral about
  language. The kit came out in English while the tracker schema and the `GEN:`
  regions stayed Turkish — because the scripts hardcode them — and the subject
  documented that split rather than hiding it. Whether that split holds under a
  host with a *pinned* output language is **untested**.

## What would upgrade it

Field use in genuinely different projects, recording **pass and fail** alike.
A refutation is worth more than a confirmation: it moves the rule out of prose
and into the scripts, which are the part of this kit that keeps working when
prose gets ignored.
