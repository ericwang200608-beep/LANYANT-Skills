---
name: refactoring
description: Reshape code while preserving behavior, using a passing behavior pin before and after each structural step. Use for renaming, extracting, inlining, moving, deduplicating, architecture improvement reports, module deepening, internal caller migration and deletion, external expand-migrate-contract changes, TypeScript package boundaries, and visual parity. Not for adding behavior or fixing bugs discovered during a refactor; split those into their own authorized work.
---

# Refactoring

You own the contract. The structure changes. The behavior does not.

Distinct from [feature-implementation](../feature-implementation/SKILL.md), which adds behavior, and [bug-diagnosis](../bug-diagnosis/SKILL.md), which corrects it. If the cleanup reveals a missing feature or a real bug, split it out and ship the structural change first against the pinned contract. A redesign is allowed, but name it and route it to feature-implementation. Large or cross-cutting structural work that spans sessions starts with [decision-mapping](../decision-mapping/SKILL.md). This skill is the focused-to-medium change, plus the review that finds such changes.

## When to use

| Situation | Run |
|---|---|
| A specific structural change: extract, inline, rename, reshape an API, delete a legacy path | [Behavior-pinned refactor](#procedure-behavior-pinned-refactor) |
| "Where should this codebase be restructured?", "plan a refactor", "improve the architecture" | [references/architecture-review.md](references/architecture-review.md), then this procedure for the chosen candidate |
| Migrating components or styles where the rendered output must stay identical | [references/visual-parity.md](references/visual-parity.md) |
| Making package boundaries enforceable in a TypeScript repository | [references/ts-deep-modules.md](references/ts-deep-modules.md) (TypeScript-specific option) |

A request for a refactor plan as a document is covered by the architecture review plus the project's specification flow in [technical-design](../technical-design/SKILL.md) and [delivery-planning](../delivery-planning/SKILL.md). Do not create a competing plan file outside the project's authoritative records.

## Inputs to read

- The affected subsystem's code, tests, and callers. Use [codebase-investigation](../codebase-investigation/SKILL.md) to learn how it works and why it is shaped this way.
- The project's glossary (`GLOSSARY.md` or equivalent) and ADRs in the area (`docs/adr/` or equivalent). Do not re-litigate a recorded decision without saying so.
- The architecture vocabulary in [technical-design](../technical-design/SKILL.md#3-design-modules-and-interfaces): module, interface, implementation, depth, seam, adapter, the deletion test, "the interface is the test surface", "one adapter means a hypothetical seam, two adapters mean a real one". Two more terms used here: **leverage** is what callers get from depth (more capability per unit of interface; one implementation pays back across N call sites and M tests); **locality** is what maintainers get from depth (change, bugs, knowledge, and verification concentrate in one place).
- The smell baseline in [standards-spec-review](../standards-spec-review/references/smell-baseline.md) for naming what is wrong.
- Every consumer of any interface you will change: in this repository, in other repositories, published packages, public APIs, stored data, and configuration.

## Procedure: behavior-pinned refactor

1. **Pin the behavior contract first.** Learn the contract with [codebase-investigation](../codebase-investigation/SKILL.md), then write a characterization test, snapshot, or equivalence harness that captures current behavior before any structure moves. If the area has no coverage, write the pin before touching structure. Type check and lint are not a pin. Run the pin and see it green on the unchanged code. Per [operating rules 5.2](../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices), a pin captures existing behavior; it is not a test that mirrors the edit.
2. **Name the structure the code is missing** ([model-the-domain](../engineering-principles/references/model-the-domain.md)). Boring code stays when the shape is already clear and local. The reshape must delete branches or invalid states, not add indirection. Use the smell baseline to name the problem.
3. **Name the target shape.** State what the module layout, types, and call graph should be if built today ([foundational-thinking](../engineering-principles/references/foundational-thinking.md), [redesign-from-first-principles](../engineering-principles/references/redesign-from-first-principles.md)). If the target crosses a function boundary, explore the shape with the design-it-twice exploration in [technical-design](../technical-design/SKILL.md) before the move. For deepening a cluster of shallow modules, classify dependencies and choose the test strategy with [references/deepening.md](references/deepening.md).
4. **Subtract before you add.** Delete dead code, collapse one-caller wrappers, drop redundant validators, and remove orphan references before introducing the new shape ([subtract-before-you-add](../engineering-principles/references/subtract-before-you-add.md)). The smallest change that reaches the target shape ships ([laziness-protocol](../engineering-principles/references/laziness-protocol.md)). A speculative cleanup that "might help" gets reverted.
5. **Move in small behavior-preserving steps, each keeping the pin green.** For API reshapes, decide the migration path from the consumers you found:
   - **Every caller is in this repository:** migrate every caller and delete the old API in the same wave ([migrate-callers-then-delete-legacy-apis](../engineering-principles/references/migrate-callers-then-delete-legacy-apis.md)). No compatibility shims, no parallel old-and-new paths. Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details. This applies when no external users depend on backward compatibility, the project can absorb a coordinated breaking change, and the new API is part of a simplification.
   - **Consumers you do not control exist** (other repositories, published packages, public endpoints, stored data formats): use expand, migrate, contract per [operating rules 5.6](../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices). Add the compatible new form, migrate callers in batches, and remove the old form only after every consumer has moved. Sequence the batches with section 2 of [delivery-planning](../delivery-planning/SKILL.md#2-split-work-into-complete-business-slices). Removing a form that external consumers use needs the owner's agreement on timing.
   - **A wide mechanical change inside the repository that cannot land as one change** also follows the expand-migrate-contract sequencing in [delivery-planning](../delivery-planning/SKILL.md#2-split-work-into-complete-business-slices), with an integration branch when batches cannot pass checks independently.

   Spot-check every rename against the actual files. Renames silently miss usages in strings, prose, configuration, and back-references; search for the old name after the move and expect zero hits. Delegate mechanical edits to a fresh agent with a specific scope (file paths, the names being moved, the behavior to hold), using [multi-agent-delivery](../multi-agent-delivery/SKILL.md) for parallel implementers in worktrees and [harness-adapters](../multi-agent-delivery/references/harness-adapters.md) for spawning and model choice. Review every delegated diff yourself; a subagent report is a claim until checked.
6. **Prove behavior is unchanged on the real artifact, not "it compiles"** ([prove-it-works](../engineering-principles/references/prove-it-works.md)). Run the pin. For larger reshapes, run an equivalence check: a script that diffs old-vs-new outputs, a recorded baseline replayed against the new code, or a smoke run on the matching surface using the project's verification harness ([verification-harness](../verification-harness/SKILL.md)) or real-surface driving tools (the project's UI-driving tool, browser automation, a CLI run, an HTTP client).
7. **Confirm the change is worth keeping.** The success measure is reduced reader load ([minimize-reader-load](../engineering-principles/references/minimize-reader-load.md)): fewer concepts, files, branches, or hops a reader needs to understand the area. State the delta concretely (for example "4 wrappers deleted, one interface instead of three, call path 6 hops to 2"). If the diff does not lower reader load somewhere, revert it.
8. **Shape small ordered commits.** A subtraction commit, then the reshape, then any follow-on cleanup. Each behavior-preserving slice stays green before the next ([sequence-verifiable-units](../engineering-principles/references/sequence-verifiable-units.md)). Stage explicit files. Rewriting local, unpushed history to get this order is reversible local work; rewriting a pushed shared branch is not. When a PR is in scope and authorized, hand off to [pr-delivery](../pr-delivery/SKILL.md).

## References and assets

- [references/architecture-review.md](references/architecture-review.md): read when asked to find or plan structural improvements. Exploration agent, HTML report in the temp directory, strength badges, interview loop.
- [references/html-report.md](references/html-report.md): read while writing the architecture review report. Scaffold, card fields, diagram patterns, tone.
- [references/deepening.md](references/deepening.md): read when a candidate deepens shallow modules. Dependency categories, seam discipline, replace-don't-layer testing.
- [references/visual-parity.md](references/visual-parity.md): read before any migration whose rendered output must stay identical.
- [references/ts-deep-modules.md](references/ts-deep-modules.md): read when the user asks to enforce package boundaries in a TypeScript repository.
- [assets/dependency-cruiser.config.cjs](assets/dependency-cruiser.config.cjs): the config copied into the target repository by the TypeScript procedure.

## Requirements

- The TypeScript boundary procedure needs Node.js and the repository's package manager. Detect with `node --version`; when absent, record the gap and stop that procedure.
- The architecture review report loads Tailwind and Mermaid from CDNs, so it renders fully only with network access. Note this when handing over the path.

## Verification required

- The pin ran green before the first structural change and after every step. Name the pin and its command.
- An equivalence proof on the real artifact for larger reshapes (diff output, replayed baseline, or smoke run), with the command and result.
- A search for every renamed or removed name returns no stale usages, including strings, docs, and configuration.
- The full existing check suite (tests, type check, lint) passes; these are required but are not the pin.
- The reader-load delta is stated. Claims are labeled measured, inferred, or unverified per [operating rules section 3](../ask-eric/references/operating-rules.md#3-evidence-record).

## Outputs and state

- Reply: the structure that changed, the pin you held it against, the equivalence proof, the reader-load delta, what shipped and what got reverted. No new behavior.
- Record evidence per [operating rules section 3](../ask-eric/references/operating-rules.md#3-evidence-record) in the existing task or delivery record. Glossary and ADR updates go to the project's existing files.

## Completion criteria

- Behavior is unchanged as proven by the pin and, where required, the equivalence check.
- No compatibility shims remain for interfaces whose callers are all in this repository; for external consumers, the expand-migrate-contract state (which phase is done, which consumers remain) is recorded.
- Reader load went down, or the change was reverted.
- Commits are ordered subtraction, reshape, cleanup, each green.

## What this skill does not authorize

Editing, testing, and local commits inside the requested scope proceed without asking. Pushing, opening PRs, commenting, and tracker writes need authorization for the specific action; merging, force-pushing a shared branch, deleting worktrees with unsaved work, and removing an interface that external consumers still use need explicit authorization per [operating rules section 1](../ask-eric/references/operating-rules.md#1-authorization-classes). Changing behavior, even to fix an obvious bug found on the way, is out of scope: split it out. Editing a visual-parity baseline or its harness is never authorized by this skill.
