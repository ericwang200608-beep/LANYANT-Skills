# Delegation Protocol

How to brief, run, and check a delegated agent. Every mode in this skill uses it. Map each generic operation (spawn, isolate, background, message, wait) to your harness with [harness-adapters.md](harness-adapters.md).

## Fresh agent per task

Give new work to a fresh agent with **consolidated scope**: the original brief, every later directive, and the prior agent's report and branch. This holds for a fix round, a follow-up, a retry, and the next queue item.

Resume, message, or queue a follow-up on an existing agent only when the new work strictly needs state that lives in that agent and is costly to move: its local checkout, its uncommitted changes, or a process it still runs (a dev server, a simulator, a PR watcher). A stop or hold order to a running agent is not reuse. A role such as a PR owner outlives its agent: once that agent returns, a fresh agent takes the role's next round. Interrupt-chained resumes silently drop directives, so start a fresh agent with consolidated scope rather than trusting a "done" summary.

A delegate never runs the coordinating procedure itself. The coordinator owns the procedure, the task list, and every spawn. A delegate does one task and reports.

## The brief

Every brief stands alone. The delegate does not see this conversation, its siblings, or your conclusions. Each brief contains:

1. **The goal, restated in your own words**: the user's goal, the problem being solved, and the smallest change expected to meet it.
2. **Consolidated scope**: the task, every directive given since, and the prior agent's report and branch when this is a retry or follow-up.
3. **File pointers, not inlined context**: paths to the specification, task, research notes, previous commits, and upstream reports. Paste an upstream report in full only when the delegate cannot reach it by path.
4. **Where to work**: the worktree path or isolated agent, the branch, and the base SHA it must confirm before starting.
5. **Write boundaries**: the paths it may write and the paths it must not touch, and its own output location when it writes outside the repository.
6. **Forbidden actions**: what it must not do (push, open or comment on PRs, merge, force-push, post messages, write to the tracker, delete worktrees) unless the coordinator's authorization explicitly passes one down.
7. **Explicit evidence of done**: a command and its expected output, a verification-skill check, a screenshot path, or an artifact. If you cannot name the evidence, the unit is not scoped yet.
8. **What to report**: `DONE`, `PASS`, `ISSUES`, or `BLOCKED` (per the mode), with head SHA, commands run, their output, and every issue it can prove, not only the first.
9. **Model and effort** chosen for the role per [model-roles.md](model-roles.md).

For code-writing delegates also name the data shape and its organizing structure before the delegate writes logic (a state machine over scattered booleans, a table or registry over branching, a typed model over repeated shape assumptions), and the success criteria.

## Running delegates

- Run delegates in the background where the harness allows, so other reports do not wait on a foreground call.
- Use agent mode with write access only for delegates that write. A read-only delegate is told "do not edit files", and you check `git status` afterward.
- Give each writing delegate its own worktree or output directory. Parallel agents in one worktree overwrite each other, and nobody can tell which agent changed what.
- Do not message a delegate to check on it; a message can restart an idle agent. Judge progress by side effects (commits, pushes, files written), not status text.
- Never relay messages or status between agents. Each brief carries what its agent needs.

## Owning the result

You own every delegate's work. Read the diff or the artifact yourself, rerun the evidence command when it is cheap, and write your own summary; do not pass through what the delegate said. A delegate's report is a claim until checked (operating rule 3). A second opinion is the same prompt against a different model; agreement is high-signal.

## Throughput checkpoint

Before fanning out code work, write the throughput checkpoint as four task-list items. A dimension that genuinely does not apply keeps its item with `n/a: <reason>` rather than being dropped:

- **Blocking first steps.** Gates that run before fan-out.
- **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
- **Shared mutable state.** Default to splitting the target (see [SKILL.md](../SKILL.md#shared-write-targets)). Serialize only for real invariants.
- **Smallest safe decomposition.** If one worker is best, name why.

Delegation topology:

- Code-coupled work (one feature, one migration) goes to a single owner with the checkpoint inline. That owner fans out internally after the blocking phase.
- Parent-level fan-out is for slices that produce independent artifacts (audits, cross-subsystem investigations, competing experiments).
- When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), delegate through an [arena](arena.md) so the runners surface the alternatives and the cross-judge guards the pick.
- Keep review separation even when you cannot spawn: a delegate forbidden to spawn owns the diff directly and still gets an independent reviewer. Never reply "standing by" while waiting on a nested agent.
- Rewrite the checkpoint at phase boundaries. Spawn a fresh owner rather than chaining interrupts.

## When the harness cannot spawn agents

Follow the fallback in [harness-adapters.md](harness-adapters.md#fallbacks-when-a-capability-is-missing): run each role sequentially in a clearly separated pass, re-reading the original inputs before each pass, and record that independent review was not achieved.
