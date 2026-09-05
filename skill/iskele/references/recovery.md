# Recovery — when the build goes wrong, and the ramps the kit hands over

Read this when a run stops behaving: a promised artifact did not run, a task
will not close, the tracker and reality disagree, the intent moved, or the
session has gone soft.

The rest of this skill describes the kit being built. This file has two jobs,
and they are different:

1. **Ramps for the run producing the kit** — `RR-00`…`RR-12` below.
2. **A ramp catalogue the kit hands over** — piece `09` of the manifest,
   template in `assets/templates/09-kurtarma-rampalari.md`. Steps 3 and 5
   produce gates for when work goes *right*. Nothing in the kit says what to
   do when it goes wrong, and that gap is inherited by everyone who executes
   the plan — human or agent.

The second job is the one specific to a **generative** skill. Mizan and
ux-mizan carry their ramps for themselves; iskele carries them for itself
*and* ships a copy to the project, because the project outlives the session
that planned it.

## Ramp shape

```
TRIGGER      what you just observed
FIRST MOVE   what to do before anything else
FORBIDDEN    the shortcut that hides the failure instead of fixing it
OUTPUT       what you hand back -- never "sorted it out"
BACKED BY    the step, red line or script that catches you if you skip it
```

**Name the ramp you are on, in writing.** A kit that silently recovered has an
unmeasurable defect rate, and the whole point of computing progress from data
was to stop measuring by feeling.

---

## The failure classes these ramps exist for

The ramps are the remedies; these are the diseases. They are model failure
modes, not project mishaps — they recur across hosts and models, because they
are what a producer that is also the judge does under pressure to look useful.

| Class | How it shows up while building a kit | Ramp |
|---|---|---|
| **Production-side closure** | The endpoint exists, the tests pass, the user can reach nothing. The tracker says done. | RR-03 |
| **Optimistic reporting** | "Set up", "tracked", "verified" with no artifact behind it | RR-01 |
| **Criterion softening** | The criterion did not hold, so the criterion is reworded until it does | RR-02 |
| **Silent gap-filling** | A constraint was never answered, a plausible one was assumed, and the schema was built on it | RR-10 |
| **Task inflation** | Forty tasks because forty looks like a plan; estimates padded to look considered | RR-06 |
| **Scope drift** | Work outside the phase's out-of-scope list, because the detour was interesting | RR-07 |
| **Plan capture** | The intent changed and the backlog was patched while the domain model kept the old split | RR-08 |
| **Confirming your own kit** | The run that wrote the acceptance criteria decides whether they were met | RR-00 |
| **False precision** | "~78.5 days" from uncalibrated weights, presented as a schedule | RR-12 |
| **Context decay** | Hour three: still producing tasks, no longer checking them against the model | RR-09 |
| **Escape without a class** | It got out, the fix went in, and nothing changed about what the next gate checks. The scorecard counts it; a count is not a loop | RR-13 |

---

## RR-00 — You are about to judge your own kit

**TRIGGER.** The next thing you were going to do is verify, sign off or audit
something produced earlier in this same run — your own acceptance criteria,
your own gate list, your own scenario list.

**FIRST MOVE.** Declare the switch in one line, and cap what the claim can be:

```
ROLE CHANGE: producer -> auditor of my own kit. Arbiter: author.
Judgement claims are self-reported, not measured.
```

Then either hand it to a separate pass (that is what step 7's mizan handoff is
*for*), or continue with the cap stated.

**FORBIDDEN.** Writing scenario-rehearsal scenarios yourself and calling the
result coverage — invented plausible scenarios are fiction wearing an evidence
label. Upgrading a task's arbiter class because the work looks done.

**OUTPUT.** The declaration, plus which claims are self-reported. If no
separate pass is possible here, say that rather than implying one happened.

**BACKED BY.** The *Auditing your own work* red line; step 7 (`arbiter
defaults to author, and it should stay that way`); step 5's scenario rule.

---

## RR-01 — A promised artifact did not run

**TRIGGER.** No openpyxl, no shell, no subagent; or `backlog_to_tracker.py` /
`progress.py` raised.

**FIRST MOVE.** Diagnose before substituting. Does the missing tool remove a
**capability** or a **convenience**? Without openpyxl there is no tracker, and
with no tracker there is no computed progress — step 6 did not happen. A
missing subagent only costs fan-out speed.

**FORBIDDEN.** Printing "here is what the table would look like" instead of
producing the tracker. That is a production-side claim committed by the
planner: step six *appears* done and nothing is trackable.

**OUTPUT.** The constraint, named in the kit: which piece was not produced,
what the kit therefore cannot do, and the explicit alternative offered (a CSV
tracker, or waiting for the install). Also record it as a skipped manifest
piece — the manifest rule already says never skip silently.

**BACKED BY.** Operating assumptions (*check a tool before assuming it*), the
manifest's "say which piece you skipped and why".

---

## RR-02 — A task will not close

**TRIGGER.** The work looks finished and the acceptance criterion does not
hold — or it holds only if you read it generously.

**FIRST MOVE.** Decide which of three things is wrong, **before** editing
anything:

1. **The work** — incomplete. Finish it.
2. **The task** — too big; it is "partly done", which the backlog rule says
   is impossible. Split it, and let the split inherit the criterion.
3. **The criterion** — written from the production side, or unmeasurable as
   written. Rewrite it **from the consumption side**, and record the rewrite:
   a criterion changed after seeing the result is no longer a preregistration,
   and step 7 sold this backlog to mizan precisely as one.

**FORBIDDEN.** Loosening the criterion to fit what was built. Closing on "the
endpoint returns the data" when the criterion said the user reaches it.
Marking done in the tracker to unblock a dependent task.

**OUTPUT.** Either a closed task with the criterion actually run, or a split,
or a dated criterion revision with its reason. All three are progress; only
the first is done.

**BACKED BY.** Step 4 (atomic tasks, consumption-side criteria), the DoD's
*actually run the acceptance criterion*, the *happy-path verification* red
line.

---

## RR-03 — The tracker and reality disagree

**TRIGGER.** A capability is marked done and cannot be reached. Or a test
exists for a surface that does not.

**FIRST MOVE.** This is the failure the backlog rules were written from, and
it is never a single task's fault: the gap lives **between** tasks, where no
single checklist can see it. So look for the pair, not the bug. For the closed
task, find its consuming twin — the task that brings the reading surface. If
no such task exists, the plan is missing a task, not the build.

**FORBIDDEN.** Fixing it quietly inside the closed task and moving on. That
repairs one instance and leaves the class: the same gap recurred four times on
the project that produced this rule, and none of the four came out of the
plan.

**OUTPUT.** A new backlog task for the missing reading surface, with the
producing task's ID pointing at it (`→ F3-FE-03`), and a note in the risk file
about the class. Then check the other closed tasks in that phase for the same
shape — one instance found by accident implies the sweep was never run.

**BACKED BY.** Step 4 (a producing task names its consuming twin), the DoD's
reading-surface item.

---

## RR-04 — A passed gate stopped holding

**TRIGGER.** Something that worked at the last gate no longer does, and no
task in the current phase was about it.

**FIRST MOVE.** Restore first, diagnose second — a regression under
investigation is a regression still shipped. Then ask the gate's own question
rather than a debugging question: **whose guarantee broke, and which pair
broke it?** The two fragile shapes are named in step 5: a **derived signal**
(anything computed from an absence — "untouched for 3 days", "unassigned" —
which silently changes meaning the moment a new state exists) and a guarantee
**enforced call-site by call-site** (correct in five places, pierced wholesale
by a sixth).

**FORBIDDEN.** Treating a green test suite as counter-evidence. Tests are
written per feature; they speak about the parts and stay silent about the
pair — which is exactly why scenario rehearsal exists as a separate level.

**OUTPUT.** The restored state, a new scenario added to the phase's rehearsal
list (**written before the next finding**, not after this one), and a task for
the real fix. If the pair was one the rehearsal list should have contained,
say so: that is a finding about the *plan*, and it is worth more than the fix.

**BACKED BY.** Step 5 scenario rehearsal, step 3 (gates), the *skipping
phases* red line.

---

## RR-05 — Something noticed that is not in the plan

**TRIGGER.** Mid-build you find a real problem — dead code, a missing check, a
broken promise — that no task covers.

**FIRST MOVE.** Do not fix it, and do not expand the task. Produce the
**minimal record**: which file, which behaviour, what would demonstrate it.
Then route it:

- **Demonstrable** → a backlog task with an acceptance criterion, placed in a
  phase. It enters the plan; it does not enter the current task.
- **Not demonstrable** → close it in the risk file with the reason it could
  not be pinned down. A closed observation is a record; an unpinned worry in a
  backlog is noise the next reader cannot distinguish from work.

**FORBIDDEN.** Fixing it silently because it is small. Every silent fix is an
untracked change to a plan whose whole claim is that progress is computed from
data.

**OUTPUT.** A task or a written closure — and either way, the current task
closes on its own criterion, unchanged.

**BACKED BY.** Step 3's explicit out-of-scope lists, `06-riskler-ve-kararlar`
as the home for blockages and negative findings.

---

## RR-06 — Rounds are piling up on one task

**TRIGGER.** The same task has come back three or more times, or the backlog
is growing while nothing closes.

**FIRST MOVE.** **Stop working the task and go up a level.** A task that will
not close after repeated rounds is usually not a hard task; it is a task
standing on the wrong split. Re-read step 2's question — are two things with
separate life cycles being conflated here? — and check whether the phase
boundary put the data on the wrong side of a gate.

**FORBIDDEN.** A fourth attempt with the same framing. Adding tasks so the
board shows movement. Padding estimates so the round count looks reasonable.

**OUTPUT.** A written diagnosis — model, phase boundary, or task — and *only*
a diagnosis. No code on this ramp. If it is the model, the ADR log gets the
revision and the affected tasks get re-derived, which is RR-08.

**BACKED BY.** Step 2 (do not write a schema before the split is found), step
3 (the next phase's data comes from the previous one).

---

## RR-07 — Work drifted outside the phase

**TRIGGER.** What is being built is not in this phase's scope, or is on its
explicit out-of-scope list.

**FIRST MOVE.** List the drift: which changes were outside, and whether each
was necessary or merely adjacent. Then park them as tasks in the phase where
they belong.

**FORBIDDEN.** Folding the detour into the current task's diff. Deleting the
out-of-scope line because it turned out to be inconvenient — that line is what
prevents scope drift, and editing it after the fact is the drift.

**OUTPUT.** A parked list handed back for a decision: move the phase boundary,
or leave the work parked. That is the owner's call, not the builder's.

**BACKED BY.** Step 3 (explicit out-of-scope per phase), the *scope drift* red
line.

---

## RR-08 — The intent moved

**TRIGGER.** The owner changes what the project is for, or a constraint
answered in step 1 turns out to be wrong — after the backlog exists.

**FIRST MOVE.** Update **in the loop's own order**: constraints → domain model
→ phases → backlog → tracker. Then produce a **delta list**: which tasks
changed, which were dropped, which are new.

**FORBIDDEN.** Patching the backlog alone. A backlog re-derived from an
unchanged model inherits the old split silently, and step 2 already says what
a wrong split does: it collapses mid-build and pushes rework onto every phase.
Also: never edit closed tasks to look as though they had always said this —
the closed backlog is append-only for the same reason the ADR log is.

**OUTPUT.** A dated ADR for the change of intent, the delta list, and a
re-run of `backlog_to_tracker.py` so the tracker matches the plan rather than
the memory of it.

**BACKED BY.** The seven-step order ("do not break the order"), the
append-only rule for ADRs and closed backlog.

---

## RR-09 — The session has gone soft

**TRIGGER.** Long run. Tasks are still being produced but no longer checked
against the model; you cannot recall which decisions were recorded.

**FIRST MOVE.** Write the state to files and cut. This skill already has the
move — the handoff *is* the context cut point. Flush the backlog, regenerate
the ADR index, archive closed phases, run `progress.py`, and write the handoff
note. Then start the next phase in a fresh session.

**FORBIDDEN.** Pushing on because the phase feels nearly closed — the last
tasks are then written under the worst conditions of the run and read as
though they were written under the first. Reconstructing a decision from
memory instead of opening the ADR.

**OUTPUT.** A written kit and an explicit boundary statement. And keep the
expectation honest: shrinking the reading surface is a real gain in
*direction*, not the token saving the byte count suggests.

**BACKED BY.** Step 7 (the handoff is a context cut point), the reading-surface
section.

---

## RR-10 — Ambiguity, or the plan and the code disagree

**TRIGGER.** Two readings of a constraint are defensible; or the backlog, the
ADR log and the implementation disagree about what was decided.

**FIRST MOVE.** Do not assume — and do not ask empty-handed. **Whoever brings
the question brings a recommendation and its reason.**

```
SITUATION:      <what is undecided, one sentence>
OPTIONS:        A <...>  B <...>
RECOMMENDATION: A
BECAUSE:        <tied to a constraint or the domain model, not to taste>
COST IF WRONG:  <what taking A and being wrong costs>
```

A recommendation can be disagreed with in one word; a bare question hands the
work back to the person who asked for a plan. The decision stays theirs — **a
recommendation is not approval, and an unanswered recommendation is not
consent.** Step 1's rule still applies to the asking: one round, at most three
questions.

A plan/code contradiction is additionally **a finding**: the team has been
reading a description of a system it does not have, and every downstream
estimate rests on it.

**FORBIDDEN.** Picking the reading that makes the plan tidier. Recording your
own inference as a decided constraint — an undocumented gap is always worse
than a decided boundary, and an *invented* one is worse than both.

**OUTPUT.** A decision recorded as an ADR, or — on a question the owner leaves
open — a stated default marked as an assumption, with the tasks that rest on
it named.

**BACKED BY.** Step 1 (ask, do not assume), step 5's boundary rule, the
*silent assumption* red line.

---

## RR-11 — Rolling back shipped work

**TRIGGER.** A phase's output has to come out — the gate was passed in error,
or the approach was wrong.

**FIRST MOVE.** Roll forward, not backward: the rollback is a new recorded
event, not the erasure of the work. The tasks stay closed with their evidence;
a new task carries the removal, and an ADR carries why.

**FORBIDDEN.** Deleting the tasks, their criteria or the ADR that argued for
the approach. The ADR log is the one document written for six months from now,
and a decision that was reversed is the most useful kind to find there.

**OUTPUT.** The removal task, the ADR with the reversal and its trigger, and a
recomputed progress number. Progress going **down** is a correct output; a
percentage that only ever rises is a report about feelings.

**BACKED BY.** The append-only ADR log, step 6 (progress is computed from the
tracker, not asserted).

---

## RR-12 — The estimate did not hold

**TRIGGER.** A phase overran, or the effort-weighted number stopped matching
what actually happened.

**FIRST MOVE.** Recalibrate from data, not from feeling. The S/M/L weights
were the author's choice and uncalibrated; the first closed phase is the first
real velocity data this project has ever had. Change **one** thing — the
weights — and re-derive; changing weights and scope together produces one
number and no attribution.

**FORBIDDEN.** Re-estimating the remaining tasks by hand to make the total
land where it should. Presenting a recalculated number without saying the
basis changed. Reporting "~78.5 days" as though the decimal were earned.

**OUTPUT.** New weights, the phase they were calibrated on, and a restated
estimate that says it is uncalibrated for anything beyond that phase.

**BACKED BY.** The *false precision* and *invented numbers* red lines, step 6
(effort-weighted progress).

---

## RR-13 — Something escaped the gate, and the plan has not moved

**TRIGGER.** A defect turned up after the gate closed — a user hit it, it broke
in production, the next phase tripped over it — and it stands on ground this
phase's criteria covered. Also fires on the quieter version: a lesson written
down as "worth adding to the DoD" that no checklist ever received.

**FIRST MOVE.** Put it in the scorecard's `Kacan` cell **before** diagnosing
it. The pull is to fix the bug and carry on; the fix belongs to the product,
the escape belongs to the plan, and only the first of the two normally gets
written down anywhere.

Then answer one question, in writing, in `KacanSinifi`: **which check should
have caught this?**

- **A check exists and did not fire.** Name it — a DoD item, a go/no-go line,
  an acceptance criterion, a rehearsal scenario. Then the finding is about this
  phase, not about the kit: the item was skipped, or scoped out, or run and
  misread. *"We never rehearsed the two-people-on-one-step scenario for this
  phase"* is a real answer, and a better one than a new rule nobody needs.
- **No check covers it.** Then write the one that now does — as a question the
  next gate can ask, not as a description of this bug. *"Can two people work
  the same step at once?"* is a scenario. *"We should think about concurrency"*
  is a mood. New scenarios go into the **next** phase's list when that phase
  opens (step 5), never backdated into the closed one.

**FORBIDDEN.** Closing an escape with the fix alone. Filling `Kacan` and
leaving `KacanSinifi` empty — the count exists to be consumed by this ramp,
not to be admired. Backdating the new scenario into the phase that missed it:
the escape is evidence that the phase's coverage claim was wrong, and saying
so plainly is the honest move.

**OUTPUT.** One escape recorded with a class beside it, and — when the class
is new — the DoD item, go/no-go line or scenario it became, added to the phase
that is open now.

**WHY IT MATTERS MORE HERE THAN ANYWHERE.** The kit's other measures all come
from inside the plan: the plan judges whether the plan was followed. This one
number comes from outside it, which is why the scorecard calls it the only
measure that cannot be gamed from inside. The two scenario classes in step 5
were themselves born from escapes — the consuming-twin gap and the conjunction
defect were both noticed by accident, four times and five times respectively,
before anyone wrote them down as classes. That is the evidence for this ramp
and also the indictment.

**BACKED BY.** The scorecard's `Kacan` / `KacanSinifi` pair, step 5 (DoD,
go/no-go, scenario rehearsal), RR-03 (the consuming-twin gap), the
`SenaryoProvali` / `SenaryoTesadufi` ratio — rehearsed beats lucky, and an
escape is the third category the ratio cannot see.

---

## Closing a phase: the process scorecard

Fill this in at each gate, next to the go/no-go. It does not grade the team —
it finds where the **plan** leaks, and it only works if it is filled in
honestly. A high number is not a failure; a hidden number is.

| Measure | Value | Reading |
|---|---|---|
| **Backlog revisions after the gate opened** | | How many tasks changed after the phase started. High → the phase was opened before its inputs were ready. |
| **Rework rounds** | | How many tasks came back more than once. Concentrated on one epic → suspect the split (RR-06), not the people. |
| **Criteria rewritten after the work** | | Every one of these is a preregistration that stopped being one. Zero is achievable; unexamined is not. |
| **Consuming-twin gaps found** | | Capabilities closed on the production side alone. **And where each was found:** at the gate, or by accident. The second number is the one that matters. |
| **Scenario findings: rehearsed / accidental** | / | Defects the scenario list caught vs. those noticed by luck. A list that catches nothing is not a clean project; it is an unexercised list. |
| **Out-of-scope entries** | | How often work left the phase (RR-07). |
| **Ramps used** | | Which `RR-nn` fired. A phase that used none either went perfectly or did not notice. |
| **Escaped** | | Defects found after the gate that this phase's criteria covered. The only measure from outside the process, and the only one that cannot be gamed from inside it. |
| **Escape class** | | For each escape: the check that should have fired, or the check that now exists because of it (RR-13). An escape with no class beside it taught the plan nothing. |
| **Pairs checked / broken** | / | From the tracker's `Cift` sheet: how many feature x guarantee pairs the gate actually re-assembled, and how many broke. A phase with zero pairs did not run the pass -- atomising the backlog destroys exactly this class, so nothing else in the plan can find it. |

**Reading:** two or three sentences. Not "the phase went well" — what changes
in the next phase, and which number says so.

**It has a home in the tracker.** `backlog_to_tracker.py` emits a `Skorkart`
sheet with a row per phase; `progress.py` reads it and renders it beside the
progress bars (`GEN:SKORKART`), so the scorecard is filled in where the work is
tracked rather than in a document nobody opens again. The generator refuses the
two mistakes that would make it lie: a missing sheet reads *not kept* rather
than zeros, and `IkizKapida` above `IkizBoslugu` is a validation error, because
a subset larger than its set inverts the indicator instead of merely breaking
it. Schema: `references/tracking.md`.

The scorecard is a claim like any other. Filled in by whoever did the work,
its arbiter is `author` and it is self-reported. Say so; the same sentence
step 7 makes about the tracker's status column applies here.

---

## Shipping the ramps with the kit

Piece `09` (`09-kurtarma-rampalari.md`) is where the project keeps its own
copy. Produce it at step 5, alongside the quality gates — the gates say what
"done" means, the ramps say what to do when it is not.

- **Adapt, do not paste.** Drop the ramps that cannot occur here (no shipped
  phases yet → no RR-11) and add the ones this domain forces. Say in the file
  which were dropped.
- **Every ramp names its evidence.** A ramp with no output artifact is advice,
  and the kit is not an advice document.
- **The catalogue is for whoever executes**, human or agent. Write it in the
  project's language, like every other kit piece, and give each ramp a code —
  a code is what makes a ramp callable in a commit message or a stand-up
  (`RR-05: parked, task F2-BE-07`) instead of a paragraph nobody quotes.
