# Arena

Spawn N parallel candidates at the same task, pick a base, and graft the strongest parts of the losers into it. Use when one attempt at a non-trivial artifact would lock in the wrong shape: a design sketch, a naming or format decision, an algorithm, an implementation that admits several valid shapes, or a second opinion on the current approach (the current design becomes one candidate among several).

Open a task list with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric: 3 to 6 concrete, gradeable criteria for what success looks like on this task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners from the arena-runners role in [model-roles.md](model-roles.md). If no value is recorded, default to one runner on the strongest model of each available family. An `auto` or `inherit-parent` entry means the parent model, so omit the model for it. If the harness rejects a configured entry, run that seat on its family's default and say so. If the family has no default, or the harness rejects it, use the closest valid model of the same family from its error message, or drop the seat and say so when there is none. If dropped seats leave fewer than two runners, add runners until there are two (or one when the role has one entry), on a remaining runner's model, or on the parent model when none remain, and say so. Spawn more runners when the arena covers multiple design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive. Pick each runner's effort and speed per [model-roles.md](model-roles.md).
4. Give each candidate its own output location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), so no two candidates share a write target.

## Phase B: Fan out

Spawn all N candidates in one message as fresh background agents ([harness-adapters.md](harness-adapters.md)), each with the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all Phase B candidates complete, choose one model from the arena cross-judge pool in [model-roles.md](model-roles.md) and spawn one read-only judge. The judge is never from the coordinator's own model family. Try only the pool entries from another family, in pool order. An `auto` or `inherit-parent` entry is the parent model, so it never judges. If the harness rejects an entry, use a valid model of the same family at the closest effort from the error message, or move to the next entry. If no entry from another family runs, skip the judge, pick the base alone in Phase D, and say so (record "independent context, same model family" is not available for the judge; the judge was skipped). If you do not know your own model, try the pool in order and say that the family check did not run.

The judge sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your reading in Phase D. Do not spawn it while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous; read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, redesigning so the result stays coherent under one mental model. Do not paste mechanically.

If the candidates converge on one shape, that is strong agreement: note it and ship the consensus shape with no graft. If they wildly diverge, Phase A was under-specified: reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, on the real artifact (the Prove It Works principle in [engineering-principles](../../engineering-principles/SKILL.md)). If verification finds a problem the arena missed, either Phase A was wrong (reframe and re-run) or a candidate caught it and you missed the graft (return to Phase E). Do not paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.

## How other procedures use the arena

- **Design exploration.** [technical-design](../../technical-design/SKILL.md) grounds the affected systems first (with [codebase-investigation](../../codebase-investigation/SKILL.md)), then runs this arena with the design-sketch task and the grounding artifacts, taking runners from the design-runners role. It requires at least two structurally distinct candidates (whole-shape alternatives, not point fixes inside one shape) before synthesis, screens each against design red flags, prefers the design that hides more complexity behind a smaller public surface, and uses the arena's synthesis decision as the design rationale's synthesis section.
- **Adversarial review.** [adversarial-review](../../adversarial-review/SKILL.md) runs Phase A steps 3 and 4 and Phase B with four changes: it takes the adversarial-reviewers role in place of arena runners, copies the scope's uncommitted changes into each worktree, spawns each adversary as a general agent, and gives each the scope, the intent, and a break-this-change brief in place of the arena task. It verifies each finding per Phase F by rerunning its command, and skips Phases C, D, and E, because adversaries find different failures and the verdict keeps every verified finding.
- **Delegated implementation with several valid shapes** ([delegation-protocol.md](delegation-protocol.md#throughput-checkpoint)).
- **Blinded evals** ([eval.md](eval.md)) use Phase B for candidates and Phase C for the blinded judge.
