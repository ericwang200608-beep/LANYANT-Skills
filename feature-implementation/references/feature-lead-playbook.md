# Feature Lead Playbook

Read when you lead a non-trivial feature and can delegate code-writing to other agents. You own the design. Plan, review, verify. Delegate implementation. Stay in the lead.

Map every agent operation (spawn, isolate, background, model choice) through [harness adapters](../../multi-agent-delivery/references/harness-adapters.md). When a capability is missing, use the fallback listed there and record the gap per [operating rule 4](../../ask-eric/references/operating-rules.md#4-capability-gaps-are-blockers-not-silent-downgrades).

Open a todo list whose first items are the steps below, copied verbatim. A step you choose not to do stays in the list with a one-line `skip: <reason>`.

## Steps

1. **How.** Explain the affected subsystem before changing it with [codebase-investigation](../../codebase-investigation/SKILL.md).
2. **Architect.** Explore the design in parallel before code: sketch types, signatures, and module boundaries, and compare alternatives. Use [technical-design](../../technical-design/SKILL.md) for the sketch and [multi-agent-delivery](../../multi-agent-delivery/SKILL.md) for parallel exploration across agents.
3. **Throughput checkpoint.** Write it as four todo items. A dimension that genuinely does not apply (single file, no fan-out) keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target ([separate before serializing shared state](../../engineering-principles/references/separate-before-serializing-shared-state.md)). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. **Delegate with a specific scope.** Delegate code-writing to a fresh agent on the configured implementation model (see model choice in the harness adapters). The scope names:
   - file paths;
   - the named data shape and its organizing structure, chosen before the delegate writes logic ([model the domain](../../engineering-principles/references/model-the-domain.md)): a state machine over scattered booleans, a table or registry over branching, a typed model over repeated shape assumptions;
   - success criteria.

   Pick each agent's reasoning level and speed for the job: stronger judgment for the hardest changes (cross-cutting design, concurrency, subtle algorithms), a fast model for trivial mechanical edits. When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), delegate competing implementations through the arena procedure in [multi-agent-delivery](../../multi-agent-delivery/SKILL.md) so the alternatives surface and an independent judge guards the pick.

   Delegation is mandatory for this playbook: the gain is review separation, not lines saved, and there is no skip-with-reason escape. An agent forbidden to spawn satisfies this by owning the diff directly with the same review separation (a separate reviewing context). When agent spawning is not available at all, record "independent agent not available; review separation not achieved" and continue sequentially. Never reply "standing by" while waiting on a nested agent.

   Comments follow [operating rule 5.5](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices): keep a comment only for a non-obvious constraint the code cannot show; a verification script gets no phase-narrating comments, the assertion text documents the step. Make surgical edits. For files derived from an external source, re-ground against that source. Port improvements to a shared primitive to all its consumers and verify each. Commit liberally on the working branch when commits are in scope.

   You own every delegate's work. Review the diff and write your own summary; do not pass through what it said. A delegate's report is a claim until you have checked its diff and output ([operating rules section 3](../../ask-eric/references/operating-rules.md#3-evidence-record)).
5. **Verify on the matching surface.** UI changes in a running UI, API changes through real calls, CLI changes through the CLI. "Inconclusive" or a wrong-surface check is not a pass; flag it. Use [verification-harness](../../verification-harness/SKILL.md) when the project has, or needs, a repeatable verification skill.
6. **Small ordered commits.** Rebase into small, ordered commits and stack follow-ups ([sequence verifiable units](../../engineering-principles/references/sequence-verifiable-units.md)): build, verify, and commit each small unit before the next. Rewriting history is local work only; force-pushing a shared branch is irreversible and needs explicit authorization.
7. **Interrogate if contested.** If the design is contested, run [adversarial-review](../../adversarial-review/SKILL.md) before shipping.
8. **Open the PR.** With authorization to open one, follow [pr-delivery](../../pr-delivery/SKILL.md). Without it, prepare the PR body and stop.

## Fan-out rules

Code-coupled work (one feature, one migration) goes to a single owner with the checkpoint inline. That owner fans out internally after the blocking phase. Parent-level fan-out is for slices that produce independent artifacts (audits, cross-subsystem investigations, competing experiments). Rewrite the checkpoint at phase boundaries. Spawn a fresh owner with a consolidated brief (original brief, every later directive, prior report and branch) rather than chaining interrupts to an existing one.

## Reply

State what you built, what you chose and why, the throughput checkpoint, and open decisions. Use tables for design alternatives. Label each claim measured, inferred, or unverified.
