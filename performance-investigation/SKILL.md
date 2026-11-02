---
name: performance-investigation
description: Measure, diagnose, and fix performance problems with evidence instead of code reading. Use when something is slow, a latency, throughput, memory, startup, render, or query time regressed, a user asks to "make it faster", "speed this up", "why is this slow", "profile this", or "benchmark A vs B", when you are about to report or act on a speedup or regression you measured, when choosing a library or config on performance grounds, or when a metric must be driven toward a target over many attempts (hill-climbing with a decision log). Covers baseline traces, the benchmark checklist (limiter, tuning, limits, errors, repeatability, relevance, did the work happen), the performance mantras in cost order, post-fix traces and artifact comparison, the keep-or-revert hill-climb loop with a frozen harness, and explaining a number before trusting it.
---

# Performance Investigation

You own the measurement story. Plan, review, and verify the numbers. Tie every fix to a measurement; do not read source instead of measuring.

## When to use

- A one-off performance problem: a slow path, a regression, a "this got slower" report. Run [One-off perf fix](#procedure-one-off-perf-fix).
- Sustained, iterative improvement of one measurable thing against a target. Run the [hill-climb loop](references/hillclimb.md).
- Any time you produce a performance number: a before and after, a regression claim, a harness, or a library or config choice. Run the [benchmark checklist](references/benchmark-checklist.md) on it before you report or act on it.

Distinct from [bug-diagnosis](../bug-diagnosis/SKILL.md), which corrects wrong behavior. When the slowness is a live process you must instrument first (a spinning CPU, a leak, a trace of a visual glitch) and the cause is unknown, run the runtime and trace forensics branch of [bug-diagnosis](../bug-diagnosis/SKILL.md) to get a cited diagnosis, then come back here to fix and measure. For performance regressions logs are usually wrong: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Core rule: explain the number

Apply before you measure, and before you trust, report, or act on any number (speedup, regression, throughput, latency, eval result). Full text: [explain-the-number](../engineering-principles/references/explain-the-number.md).

- **Write the decision before you run.** Name the result that would change a decision, and the noise floor. Stop when the run-to-run spread is larger than the effect.
- **Ask "why not double?"** Name the resource or code path that bounds the result, such as a core, a lock, the disk, the network, or the load generator itself. Get it from a profile or from system counters taken during a run, then map it to source. A guess from reading the code is not a limiter. If you cannot say why the number is not twice as good, you do not know what you measured.
- **List what else the number could be measuring, and rule out each one with evidence.** The usual suspects are errors, skipped or cached work, code that never ran, an untuned side (one left on default settings), noise, and a piece too small to matter end to end.
- **Keep the evidence with the number.** Put the run count, the spread, and the limiter in the notes or a linked artifact.

You skipped this when a run started without the result that would change a decision, when the evidence behind a number has no run count, no spread, or no named limiter, or when the time saved is larger than the time the changed piece took.

## Inputs to read

- The user's complaint and any numbers they gave (target, workload, environment).
- The project's existing benchmark, profiling, or load scripts, and the project's verification harness ([verification-harness](../verification-harness/SKILL.md)). Read the measurement script before running it.
- The architecture of the affected path. Use [codebase-investigation](../codebase-investigation/SKILL.md) to ground hypotheses in how the code actually works.
- The authoritative task or spec record for the work, where results will be recorded.

## Procedure: one-off perf fix

1. **Capture a baseline trace.** Use the project's verification harness (see [verification-harness](../verification-harness/SKILL.md)) or real-surface driving tools (the project's UI-driving tool or browser automation, a CLI run, an HTTP client against a running server, a profiler) on the surface where the user sees the problem. Vet the baseline, and each later number, with the [benchmark checklist](references/benchmark-checklist.md). Save the raw artifact (profile, trace JSON, timing output) to a path you can cite.
2. **Ground hypotheses.** Use [codebase-investigation](../codebase-investigation/SKILL.md) on the hot path the trace shows. Do not claim a perf ceiling without running it first.
   Try the performance mantras in order, cheapest first:
   1. Don't do it. Stop work whose result nothing uses rather than cheapening it.
   2. Do it, but don't do it again.
   3. Do it less.
   4. Do it later.
   5. Do it when they're not looking.
   6. Do it concurrently.
   7. Do it cheaper.

   When an earlier mantra meets the target, stop.
3. **Plan the fix from the trace.** If it crosses a function boundary, design it first with [technical-design](../technical-design/SKILL.md) (including its design-it-twice exploration). Delegate the implementation to a fresh agent with a tight brief (files, the mechanism to change, the behavior to hold) when your harness can spawn one; map the operation and the model choice per role through [harness-adapters](../multi-agent-delivery/references/harness-adapters.md). When spawning is not available, implement it yourself and record that. Review the diff yourself. Capture a post-fix trace with the same command, workload, and environment as the baseline.
   Verify each attempt before trying the next ([sequence-verifiable-units](../engineering-principles/references/sequence-verifiable-units.md)). Never stack untested changes.
4. **Parse and compare the artifacts.** Load the baseline and post-fix artifacts into something queryable (for example JSON to sqlite, or a script that extracts the relevant spans), then diff them. "Inconclusive" or a measurement on the wrong surface is not a pass. Flag it.
5. **Run the regression gate.** The tests and checks that must keep passing stay green. A faster path that changes behavior is reverted.
6. **Cite the measurement.** Fill the [verdict report template](assets/verdict-report.md). Record it per [operating rules section 3](../ask-eric/references/operating-rules.md#3-evidence-record) in the existing task or delivery record. When a PR is in scope and authorized, hand off to [pr-delivery](../pr-delivery/SKILL.md) and keep the PR body to one primary number with the runs, range, and limiter in a linked artifact.

For sustained improvement against a metric rather than a one-off fix, use the [hill-climb loop](references/hillclimb.md).

## References and assets

- [references/benchmark-checklist.md](references/benchmark-checklist.md): read every time you run a benchmark or report a measured speedup or regression. The seven questions, the pre-run steps, and the verdict vocabulary.
- [references/hillclimb.md](references/hillclimb.md): read before starting any iterative optimization run against a target. Metric, direction, stop predicate, frozen harness, decision log, keep-or-revert, parallel hypotheses, plateau rules.
- [assets/decision.tsv](assets/decision.tsv): header row for the hill-climb decision log. Copy it outside the tree to start a log.
- [assets/verdict-report.md](assets/verdict-report.md): the reporting template for any performance result.

For a general decision trail across a long session (not the per-attempt hill-climb log), use [session-continuity](../session-continuity/SKILL.md).

## Verification required

- A baseline and a post-fix measurement from the same frozen command, workload, and environment, each vetted with the benchmark checklist.
- Questions 4 (did it error) and 7 (did it even happen) of the checklist answered with evidence for every reported number, including a one-run ballpark.
- The regression gate green after the change.
- A named limiter for every claimed difference; otherwise the verdict is inconclusive.
- Claims labeled measured, inferred, or unverified per [operating rules section 3](../ask-eric/references/operating-rules.md#3-evidence-record).

## Outputs and state

- One-off fix reply: baseline number, post-fix number, delta, artifact path, verdict.
- Hill-climb reply: see the reply section of [references/hillclimb.md](references/hillclimb.md).
- Raw artifacts stay outside the committed tree unless the project keeps benchmark results in the repository.
- Results go into the project's existing task or delivery record. Do not create a separate performance tracker.

## Completion criteria

- The verdict (faster, slower, no measurable difference, or inconclusive) is stated with its number, unit, run count, range, and limiter.
- Every kept change has its own measurement and the regression gate is green.
- For a hill-climb, the stop predicate is met, or the remaining ideas are marginal and listed, and the predicate was not relaxed.

## What this skill does not authorize

Measuring, editing, profiling, and local commits inside the requested scope are reversible local work. Pushing, opening or commenting on PRs, posting results to chat or trackers, running load against shared or production systems, and changing production configuration follow [operating rules section 1](../ask-eric/references/operating-rules.md#1-authorization-classes) and need authorization for the specific action. Accepting a performance limitation as good enough for the business is the owner's call.
