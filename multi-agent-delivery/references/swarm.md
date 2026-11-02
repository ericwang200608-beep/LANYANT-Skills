# Swarm

Fan out N parallel workers, drain them, and return one report. Use for parallel coverage (one worker per package, per feature-map entry, per slice), races of identical briefs, gauntlets of verifier lanes, and exploration partitions.

A swarm partitions slices or declared race arms and aggregates one report. It is not an [arena](arena.md): an arena repeats one design or code brief, then picks a base and grafts the best parts. Do not use an arena for coverage.

## Start

Open a task list with one entry per phase before launching anything:

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Pick the worker model from the swarm-workers role in [model-roles.md](model-roles.md). If no value is recorded, use the default there. For `auto` or `inherit-parent`, omit the model so workers run on the parent model. If the harness rejects a model, use the default and say so; if it rejects the default, use the closest valid model of the same family from its error message. For a model race, name each arm's model up front. Pick each worker's effort and speed for the job per [model-roles.md](model-roles.md).
4. Give each worker its own writable output when it writes (its own worktree, or `/tmp/swarm-<slug>/worker-<n>/`). When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Spawn all N workers in one message as fresh, isolated, background agents ([harness-adapters.md](harness-adapters.md)), with the step 3 model, left unset for `auto` or `inherit-parent`. Isolate each worker in its own worktree. Use a remote or cloud agent only when authorization covers cloud agents (see [SKILL.md](../SKILL.md#authorization-map)); use a local agent when the worker needs something on this machine.

When a worker must start from a non-default branch, name the branch or SHA it checks out first.

Every brief stands alone ([delegation-protocol.md](delegation-protocol.md)). Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front: first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated report with a result table, issue one-liners, gaps or dropouts, and the race rule when used.

## Swarm as verifier

When the swarm verifies a PR or an integration head, every lane is a verifier that did not write the code, works at the named head SHA, and reruns the evidence itself (see [SKILL.md](../SKILL.md#independent-verifier-rule)). Typical lanes: one gates lane (the repository's checks), live lanes that drive the real surface through the project's verification skill or UI-driving tool ([system-verification](../../system-verification/SKILL.md)), a perf lane when the change claims or risks a performance change ([performance-investigation](../../performance-investigation/SKILL.md)), and two or more audit lanes that read the diff and the receipts and distrust the PR body.
