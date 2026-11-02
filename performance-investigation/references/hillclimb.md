# Hill-climb loop

You own the metric and the experiment's integrity. Supervise and review. Delegate the attempts.

Use this for sustained, iterative improvement of one measurable thing against a target. A one-off fix is the one-off procedure in [../SKILL.md](../SKILL.md) or a bug fix in [bug-diagnosis](../../bug-diagnosis/SKILL.md). This is the loop.

Core discipline: one change, one measurement, keep or revert. Never stack untested changes, and never claim a win from code inspection ([prove-it-works](../../engineering-principles/references/prove-it-works.md)).

## Procedure

1. **Ground the workload and architecture before choosing the metric.** Use [codebase-investigation](../../codebase-investigation/SKILL.md) over the target, name the realistic workload dimensions that can move the result (data size, history, state, concurrency), and select a case that reproduces the user's complaint. If no case reproduces it, fix the repro instead of hill-climbing. Then fix:
   - one **metric**,
   - the **direction** that counts as better,
   - a checkable **stop predicate** that pairs a target with a floor on attempts so a lucky early win cannot end the run (for example "at least 50% better than baseline and at least 10 iterations").

   Use the user's numbers when given. Otherwise agree them with the owner; the target is a business or scope decision per [operating rules section 1](../../ask-eric/references/operating-rules.md#1-authorization-classes). Record the predicate before the first attempt; per [operating rules 5.9](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices) it is never relaxed to declare success.
2. **Build the measurement harness, prove its sensitivity, then freeze it** ([build-the-lever](../../engineering-principles/references/build-the-lever.md)). Run contrasting realistic workloads and confirm the target case reproduces the symptom while easier cases separate as expected. If the harness cannot distinguish them, revise the workload or metric. Vet the harness with the [benchmark checklist](benchmark-checklist.md) before you freeze it, and make it print its error count and a count of the work done. Once frozen, one repeatable command emits the metric, sampled enough to clear the noise (median of N, not a single run). Do not modify the harness after freezing; a needed harness change ends the comparison and starts a new baseline, logged as its own row. Record the baseline metric and a green run of the regression gate (the tests that must keep passing) before any change.
3. **Open the decision log.** Copy [../assets/decision.tsv](../assets/decision.tsv) to a path outside the repository, or to a path the repository already ignores, or add the path to `.git/info/exclude` (local, not committed). Do not edit the committed `.gitignore` for this unless that is in scope. One row per attempt with these columns:
   - `id`: attempt number, starting at 0 for the baseline row.
   - `hypothesis`: the specific mechanism, one line.
   - `change`: what was changed (files, commit SHA if kept).
   - `before`: the metric before, from the frozen harness.
   - `after`: the metric after, from the frozen harness.
   - `delta`: after minus before, with unit or percent.
   - `tests`: regression gate result (`green`, `red: <test>`).
   - `verdict`: `kept` or `reverted`.
   - `note`: noise range, limiter, or why reverted.

   Read the log before each attempt. Cells stay single-line; evidence is a pointer, not prose.
4. **Ground each hypothesis in the architecture model from step 1**, so it names a specific mechanism ("defer X off the boot path because it blocks first paint"), not "try memoizing something". For a perf metric, order hypotheses by the performance mantras in step 2 of the one-off procedure in [../SKILL.md](../SKILL.md). Borrow only their order, not that step's stop rule.
5. **Loop, one hypothesis per iteration:**
   - Hand the change to a fresh agent with a tight scope (files, the mechanism, the behavior to hold), mapping spawning and model choice per role through [harness-adapters](../../multi-agent-delivery/references/harness-adapters.md). Supervise and review the diff rather than typing it ([guard-the-context-window](../../engineering-principles/references/guard-the-context-window.md)). When several independent hypotheses are live, fan them out to parallel agents, each in its own git worktree ([separate-before-serializing-shared-state](../../engineering-principles/references/separate-before-serializing-shared-state.md)); measure each one alone against the same baseline, then re-measure after integrating any two kept wins. When agents or worktrees are not available, run the attempts sequentially yourself and record the gap per [operating rules section 4](../../ask-eric/references/operating-rules.md#4-capability-gaps-are-blockers-not-silent-downgrades).
   - Measure before and after with the frozen harness, and run the regression gate.
   - Accept only when the metric moves past noise and the gate stays green. Otherwise revert the change in full. A tweak that "might help" is not kept.
   - One commit per accepted fix, staging only the files you changed (`git add <files>`, never `git add -A` or `git add .`). Log the row either way, kept or reverted.

   Each iteration ends in a check before the next begins ([sequence-verifiable-units](../../engineering-principles/references/sequence-verifiable-units.md)). If the run is unattended, borrow only the wake mechanism from the autonomous runs and loops in [multi-agent-delivery](../../multi-agent-delivery/SKILL.md) (scheduling is mapped in [harness-adapters](../../multi-agent-delivery/references/harness-adapters.md)), not its stop rule. Unattended runs still never push, open PRs, or merge without authorization.
6. **Push past the first plateau.** On a stall (several rejects in a row), pivot category, combine near-misses, re-read the source, or try something more radical before concluding the hill is climbed. Correctness and simplicity outrank the number. Revert a win that breaks behavior, and keep a simplification that holds the number ([laziness-protocol](../../engineering-principles/references/laziness-protocol.md)).
7. **Stop** when the predicate is met, or when the remaining ideas are marginal and not worth their cost. Do not relax the predicate to meet it, and do not quit while cheap untried hypotheses remain. A plateau is not an exit. If you are stuck, surface it instead of spinning.
8. **Deliver.** When a PR is in scope and authorized, hand off to [pr-delivery](../../pr-delivery/SKILL.md) with the accepted commits stacked in the order they landed. Otherwise leave the commits on the local branch and report.

## Reply

The metric and target, baseline to final with the percent delta, iterations run (kept vs reverted), each accepted fix on one line, the `decision.tsv` path, and the best idea you would try next if pushed further. Use the hill-climb section of [../assets/verdict-report.md](../assets/verdict-report.md).
