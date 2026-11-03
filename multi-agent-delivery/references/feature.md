Apply [operating rules](../../ask-eric/references/operating-rules.md) to every action below. This procedure grants no push, PR, tracker write, merge, production, deletion, schedule, or paid-resource permission. Carry existing scoped authorization forward. Missing platform capabilities are explicit blockers.

### Feature

**You own the design. Plan, review, verify.** Delegate implementation. Stay in the lead.

1. [codebase-investigation](../../codebase-investigation/SKILL.md), Mode 1: Explain how, over the affected subsystem.
2. [technical-design](../../technical-design/SKILL.md) and its [architecture procedure](../../technical-design/references/architect.md) for parallel design exploration.
3. Write the throughput checkpoint as four todo items. A dimension that genuinely does not apply (single file, no fan-out) keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (the [separate-before-serializing-shared-state](../../engineering-principles/references/separate-before-serializing-shared-state.md) principle). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. Delegate code-writing to a subagent using your configured feature model with a specific scope (file paths, named data shape and its organizing structure per [model-the-domain](../../engineering-principles/references/model-the-domain.md), a state machine over scattered booleans, a table/registry over branching, a typed model over repeated shape assumptions, chosen before the delegate writes logic, and success criteria). Use only available models; follow [model roles](model-roles.md). When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), delegate via the **multi-agent-delivery** skill instead so the runners surface the alternatives and the cross-judge guards the pick. Mandatory: no skip-with-reason escape, and Laziness Protocol does not override it (the gain is review separation, not lines saved). A subagent forbidden to spawn satisfies this by owning the diff directly with the same review separation. No "standing by" reply that waits on a nested agent. Write comments according to [operating rule 5.5](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices). Surgical edits, re-ground against the source for upstream-derived files. Port shared-primitive improvements to all consumers and verify each. Commit liberally.
5. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
6. Rebase into small, ordered commits. Stack follow-ups.
   Use the [sequence-verifiable-units](../../engineering-principles/references/sequence-verifiable-units.md) principle, building, verifying, and committing each small unit before the next.
7. If the design is contested, use [adversarial-review](../../adversarial-review/SKILL.md), Interrogate mode, before shipping.
8. Use [pr-delivery](../../pr-delivery/SKILL.md) when PR publication is authorized.

Code-coupled work (one feature, one migration) goes to a single owner with the checkpoint inline. That owner fans out internally after the blocking phase. Parent-level fan-out is for slices that produce independent artifacts (audits, cross-subsystem investigations, competing experiments). Rewrite the checkpoint at phase boundaries. Spawn a fresh owner rather than chaining interrupts.

**Reply:** what you built, what you chose and why, the throughput checkpoint, open decisions. Tables for design alternatives.
