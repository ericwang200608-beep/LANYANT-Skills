# Task Graph Execution

Implement a specification whose tasks form a dependency graph, with one fresh implementer per task in its own worktree and an integration branch that collects the merged result.

Read this when a specification already has tasks (tickets) with blocking relationships, and the goal is the entire specification implemented on one integration branch. The tasks come from the project's authoritative task record (see [delivery-planning](../../delivery-planning/SKILL.md)); this procedure never creates a competing tracker.

## Inputs

- The specification and its tasks, with their blocking relationships.
- The issue tracker or task record, and how it closes work (by PR, by status change, by checkbox in a task file). If the tracker is not known, ask the owner where tasks live before starting; do not guess.
- The project's automated checks (typecheck, lint, tests, format) and its system-level verification route.
- The authorization in force: whether commits, pushes, draft PRs, tracker writes, and merges are in scope (see the authorization map in [SKILL.md](../SKILL.md#authorization-map)).

## Core ideas

- The tasks are not a list of steps. They are a **task graph** with blocking relationships between them. There is always a **frontier** of tasks that are ready to be grabbed: every task whose blockers are all complete.
- Start every subagent with a fresh context window ([delegation-protocol.md](delegation-protocol.md)).
- Communication to and from subagents is sparse. Communicate primarily through **context pointers**: to the specification, tasks, research notes, and previous commits. Do not duplicate information already available through pointers.
- Run **implementer subagents** in the background where the harness allows it, for maximum concurrency ([harness-adapters.md](harness-adapters.md)).
- One writer per branch. Each implementer owns its task branch. The merger owns the integration branch. You, the coordinator, own neither.

## Parallel marker rule

When the task record marks tasks as parallelizable (for example `[P]`), a task may carry the marker only when it touches different files from every other concurrent task and has no dependency on an incomplete task. Apply the same rule when you compute the frontier yourself:

- Respect dependencies. Run sequential tasks in order; tasks marked parallel can run together.
- File-based coordination. Tasks that affect the same files run sequentially, even when the graph shows no blocker. Two frontier tasks that write the same file are not both on the frontier; split the shared target first (see [SKILL.md](../SKILL.md#shared-write-targets)) or serialize them.
- Halt the run if a non-parallel task fails. For parallel tasks, continue with the successful tasks and report the failed ones.
- Within one user story or slice, tests are written and fail before implementation; models before services; services before endpoints; core implementation before integration. Mark each completed task in the task record as it completes (for example `[X]`), so a later run picks up where this one stopped.

## Steps

1. **Read the specification and tasks to understand the task graph.** Write the graph down in your working notes: each task, its blockers, the files it is expected to touch, and the initial frontier.

2. **(Optional) Explore first.** Use an **exploration subagent** to conduct any exploration the tasks require: relevant codebase files or external documentation. The exploration subagent must be able to save files. It saves its markdown notes in a directory outside the repository, accessible by all later subagents (for example a temporary directory named in every later brief). This lets implementer subagents focus on implementation rather than exploration. The exploration subagent is read-only toward the repository.

3. **Create the integration branch** from the agreed base: `git switch -c <integration-branch> <base>` (local, reversible). If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of the base cannot open one), marked as closing the specification and tasks. Pushing the branch and opening the draft PR are outward-facing: do them only when authorization covers them; otherwise prepare the PR text with [pr-delivery](../../pr-delivery/SKILL.md) and record "draft PR not opened: not authorized".

4. **Use a fresh implementer subagent for each task on the frontier, each in its own worktree on its own branch.** Create the worktree from the integration branch tip (`git worktree add <path> -b <task-branch> <integration-branch>`, or the harness's isolated-agent mapping in [harness-adapters.md](harness-adapters.md)). Write each brief per [delegation-protocol.md](delegation-protocol.md): goal, the task pointer, the specification pointer, the exploration notes path, the worktree path and branch, the files it may and may not write, the evidence of done, and the actions it must not take (no push, no PR, no merge into the integration branch, no tracker writes). Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting (`git merge-base --is-ancestor <integration-branch-at-spawn> HEAD`), and resets onto it if not;
   - builds the task with [test-driven-development](../../test-driven-development/SKILL.md), following operating rule 5.2 for when test-first is mandatory;
   - runs the project's checks for the touched paths and commits on its own branch;
   - merges the integration branch tip into its own branch before reporting done, resolving any conflict per [merge-conflicts.md](merge-conflicts.md) and re-running the checks;
   - reports `DONE` with the head SHA, the check commands and their output, and the task identifier, or `BLOCKED` with the blocker and evidence.

5. **Once an implementer subagent completes, merge its work to the integration branch with a merger subagent.** The merger is a fresh subagent and the only writer of the integration branch. Before merging, read the implementer's diff and check output yourself; a report is a claim until checked (operating rule 3). The merger:
   - checks out the integration branch in its own worktree;
   - fast-forwards when possible: `git merge --ff-only <task-branch>`;
   - when the integration branch moved since the implementer's last merge, merges with `git merge --no-ff <task-branch>`, resolves conflicts per [merge-conflicts.md](merge-conflicts.md), and never invents behavior that neither side wrote;
   - runs the project's full automated checks on the merge result and reports the new integration head SHA with the output;
   - on a red check it cannot fix within the merge's intent, reverts its own merge on the integration branch (local, reversible) and reports `BLOCKED` with evidence; the task returns to the frontier with a consolidated brief for a fresh implementer.

6. **If the merge changes the frontier of available tasks, start more implementer subagents on the new tasks.** This allows maximum concurrency. Mark the completed task in the task record when authorization covers that write; otherwise list it as complete in your report. Account for every implementer you spawned as merged, replaced, or blocked.

7. **Once all tasks are complete, run [standards-spec-review](../../standards-spec-review/SKILL.md) on the integration branch** against the base, in fresh independent contexts. Fix every issue the review raises in a single fresh implementer subagent with a consolidated brief (the review findings, the specification, the branch), merged by the merger as in step 5.

8. **Run final integration verification on the integration branch head.** See [Final integration verification](#final-integration-verification). Fix failures with a fresh implementer and repeat from step 5 for that fix.

9. **Close out within authorization.** If a draft PR exists and authorization covers it, mark it ready for review per the project's convention. Otherwise, resolve each task the way the issue tracker closes work when authorization covers tracker writes, or list the resolutions for the owner. Report the integration branch and its head SHA. Opening or readying a PR never authorizes merging it (operating rule 5.4).

10. **Clean up all implementer and merger worktrees** per [worktree-cleanup.md](worktree-cleanup.md): `git worktree remove <path>` for each clean worktree whose branch is merged into the integration branch, then `git worktree prune`. Any worktree with uncommitted work pauses for a decision. Branch refs survive, so no commits are lost.

## Final integration verification

Verification runs on the integrated branch head, never only on the task branches, because a set of individually green branches can still break together.

1. Record the integration head SHA.
2. Run the project's full automated checks on that SHA from a clean checkout (typecheck, lint, the whole test suite, build, format). Record each command and its output.
3. Run system-level verification of the specification's key scenarios on that SHA with [system-verification](../../system-verification/SKILL.md), in a context that did not write the code (see [SKILL.md](../SKILL.md#independent-verifier-rule)).
4. When the change is contested or high blast radius, run [adversarial-review](../../adversarial-review/SKILL.md) on the integration diff.
5. Record the verdict against the head SHA per operating rule 3. A new head needs a new verdict, except where the patch-id rule in [SKILL.md](../SKILL.md#independent-verifier-rule) carries a result.

## When the run outgrows one context

Large specifications often run smoothly through planning, then degrade during implementation: the coordinator loses track of the plan, ignores tasks, or invents results, usually right before or after context compaction. The cause is context window exhaustion. Scope each run so it stays well within limits:

| Approach | Best for |
| --- | --- |
| Limit how many tasks run per invocation ("execute tasks T001 to T010, then stop and report progress", or one phase) | Any harness; simplest; no subagent support needed |
| Delegate each parallel task to a subagent with one task plus the relevant plan excerpts | Harnesses with subagents; maximizes parallelism; the main session never compacts |
| Combine both (one phase per run, parallel tasks delegated) | Large features on subagent-capable harnesses |
| Decompose into a roadmap of smaller specifications | When even a single phase overwhelms the context |

Completed tasks are marked in the task record, so the next run picks up where the last stopped. Before a run boundary, leave a resume note with [session-continuity](../../session-continuity/SKILL.md).

### Roadmap of sub-specifications

Use decomposition only when the lighter options are insufficient. It adds the most overhead.

1. **State the whole feature** (the epic) in a sentence or two.
2. **Identify independent slices.** Propose a small set of sub-features that each deliver a coherent, independently testable piece; implementing just one leaves something demonstrable.
3. **Draw the boundaries.** For each slice write one line of intent and an explicit scope boundary (what is in, what is deferred to a sibling slice).
4. **Order by dependency.** Sequence prerequisites first. Slices with no dependency on each other can be built in any order; to build them in parallel, use separate worktrees so each run has isolated active-feature state.
5. **Record the result as a roadmap** in the project's existing planning location (feature-scoped `specs/<epic-slug>/roadmap.md`, or a top-level `ROADMAP.md` for a cross-cutting epic, following the project's convention).

The roadmap names and orders sub-features; it does not design them. Template:

```markdown
# Roadmap: <epic name>

<One or two sentences: what the epic is and why it is being decomposed.>

**Status legend**: planned · in-progress · done

| ID | Sub-feature | Intent | Scope boundary | Depends on | Status | Sub-spec |
|----|-------------|--------|----------------|-----------|--------|----------|
| R1 | <name>      | <one line> | <in / deferred> | none   | planned | none |
| R2 | <name>      | <one line> | <in / deferred> | R1     | planned | none |
```

Keep the `ID` column immutable once a sub-specification references it. Fill `Sub-spec` with each sub-feature's specification path as it is created, and update `Status` as work progresses.

Specify each sub-feature one at a time: pick the next entry whose dependencies are `done`, specify only that slice from its roadmap entry, plan, task, and implement it (this procedure), then mark it `done`. Link both ways: each sub-specification names its parent roadmap and entry id in its input line (`**Input**: Parent roadmap: specs/<epic>/roadmap.md entry **R3**.`), and the roadmap's `Sub-spec` column points back. When scope shifts, update the roadmap entry first, then reconcile the affected sub-specifications. If a slice is still too large, give it its own roadmap and recurse only as deep as the context problem requires.

## Outputs

- The integration branch with every task merged, its head SHA, and the final verification record.
- Task record updates (within authorization) or a list of resolutions for the owner.
- A worktree cleanup record.

## Completion criteria

Every task is merged into the integration branch, the code review findings are fixed, the full checks and system-level verification pass at the integration head with an independent verdict, the task record reflects the result (or the owner has the list), and every implementer worktree is removed or explicitly held with a reason.
