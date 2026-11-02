---
name: engineering-principles
description: Apply the 24 engineering principles to concrete design, implementation, testing, measurement, refactoring, and delegation decisions. Use when a user names a principle, another skill points to one, or a multi-step engineering task needs a rule for a real tradeoff. Read the triggered leaf before citing it, and name the decision it changed.
---

# Engineering Principles

Each principle is a short rule with a trigger. Read the index at the start of a multi-step task, apply the principles the task triggers, and name each applied principle in your reply together with the decision it changed.

## When to use

- At the start of any multi-step engineering task: scan the index for triggers.
- When the user steers with a principle name. Each name points at a complete rule, so one phrase redirects the work more precisely than a paragraph of instructions.
- When a decision (a design choice, a sequencing choice, what counts as proof, whether to ask) needs a stated rule behind it.
- When another LANYANT skill cites a principle.

## Inputs to read

- This index.
- The leaf for every principle you apply: **read the leaf before citing it.** The index line is a trigger, not the rule.
- [Operating rules](../ask-eric/references/operating-rules.md), section 5, which wins when a principle and an operating rule compete (see Conflicts below).

## Index

Read the leaf in full for any principle you apply.

### Core

| Principle | When it applies | Leaf |
|---|---|---|
| Laziness Protocol | Refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion and the smallest change that solves the problem. | [laziness-protocol.md](references/laziness-protocol.md) |
| Foundational Thinking | Before writing logic: core types and data structures, scaffold-vs-feature sequencing, what concurrent actors share. | [foundational-thinking.md](references/foundational-thinking.md) |
| Redesign From First Principles | Integrating a new requirement into an existing design. Redesign as if it had been foundational from day one. | [redesign-from-first-principles.md](references/redesign-from-first-principles.md) |
| Attack the Premise | Two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before another fix that assumes it. | [attack-the-premise.md](references/attack-the-premise.md) |
| Subtract Before You Add | Sequencing an addition, refactor, or rewrite. Remove dead weight first, then build on the simpler base. | [subtract-before-you-add.md](references/subtract-before-you-add.md) |
| Minimize Reader Load | Reviewing or shaping code that is hard to trace. Count layers and hidden state, collapse one-caller wrappers, shrink mutable scope. | [minimize-reader-load.md](references/minimize-reader-load.md) |
| Outcome-Oriented Execution | Planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; do not preserve throwaway compatibility states. | [outcome-oriented-execution.md](references/outcome-oriented-execution.md) |
| Experience First | Product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience. | [experience-first.md](references/experience-first.md) |
| Exhaust the Design Space | A novel interaction or architectural decision with no precedent. Build 2-3 competing prototypes and compare before committing. | [exhaust-the-design-space.md](references/exhaust-the-design-space.md) |
| Build the Lever | Any non-trivial work. Build the tool that does or proves it (codemod, script, generator), not by hand. The tool is the artifact a reviewer reruns. | [build-the-lever.md](references/build-the-lever.md) |

### Architecture

| Principle | When it applies | Leaf |
|---|---|---|
| Model the Domain | Writing stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a structure instead of scattered conditionals. | [model-the-domain.md](references/model-the-domain.md) |
| Boundary Discipline | Wiring validation, error handling, or framework adapters. Guards at system boundaries, trust internal types, keep business logic pure. | [boundary-discipline.md](references/boundary-discipline.md) |
| Type System Discipline | Designing types or a signature in any typed language. Make illegal states unrepresentable, brand primitives, parse external data at boundaries. | [type-system-discipline.md](references/type-system-discipline.md) |
| Make Operations Idempotent | Designing commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state. | [make-operations-idempotent.md](references/make-operations-idempotent.md) |
| Migrate Callers Then Delete Legacy APIs | Introducing a new internal API while old callers exist and every caller is in this repository. Migrate and delete in one wave. | [migrate-callers-then-delete-legacy-apis.md](references/migrate-callers-then-delete-legacy-apis.md) |
| Separate Before Serializing Shared State | Concurrent actors might write the same file, branch, key, or object. Eliminate the sharing first. | [separate-before-serializing-shared-state.md](references/separate-before-serializing-shared-state.md) |

### Verification

| Principle | When it applies | Leaf |
|---|---|---|
| Prove It Works | After a task, before declaring done. Verify against the real artifact, not a proxy or "it compiles". | [prove-it-works.md](references/prove-it-works.md) |
| Fix Root Causes | Debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate. | [fix-root-causes.md](references/fix-root-causes.md) |
| Sequence Work into Verifiable Units | Multi-step work (sweeps, migrations, runs of similar edits) and how you stack commits and PRs. Small units that each end in a check; order delivery so the sequence proves itself. | [sequence-verifiable-units.md](references/sequence-verifiable-units.md) |
| Test Behavior, Not Implementation | Writing, changing, or keeping a test. Assert what the code's users can observe. | [test-behavior-not-implementation.md](references/test-behavior-not-implementation.md) |
| Explain the Number | Before you measure, and before you trust, report, or act on a measured number. Find what limits it and rule out that it measured something else. | [explain-the-number.md](references/explain-the-number.md) |

### Delegation

| Principle | When it applies | Leaf |
|---|---|---|
| Guard the Context Window | Context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents, keep summaries in the main thread. | [guard-the-context-window.md](references/guard-the-context-window.md) |
| Never Block on the Human | Tempted to ask "should I do X?" on reversible, authorized work. Proceed, present the result, let the human course-correct. | [never-block-on-the-human.md](references/never-block-on-the-human.md) |

### Meta

| Principle | When it applies | Leaf |
|---|---|---|
| Encode Lessons in Structure | You catch yourself writing the same instruction a second time. Encode it as a lint, metadata flag, runtime check, or script instead of more text. | [encode-lessons-in-structure.md](references/encode-lessons-in-structure.md) |

## Procedure

1. At the start of a multi-step task, scan the index and list the principles the task triggers.
2. Read the leaf of each triggered principle in full before applying or citing it.
3. Check the Conflicts table. Where a principle meets an operating rule, the operating rule sets the boundary.
4. Apply the principle to a concrete decision: what you will build, delete, sequence, verify, or ask.
5. Cite it (below). When a principle produced nothing, do not cite it.

## How to cite a principle

- Name the principle and the decision it changed, in one line: "Subtract Before You Add: deleted the two unused adapters before adding the new one." A citation with no decision behind it means the rule was named, not applied.
- Cite only principles whose leaf you read in this task.
- Some principles leave an artifact. Build the Lever produces a codemod, script, generator, or delegate brief in the diff; if there is none, you did not apply it. Prove It Works and Explain the Number produce a run output or a script a reviewer can rerun; link it.
- Put the citation where the decision is recorded: the reply, the plan, the decision log ([session-continuity](../session-continuity/SKILL.md)), the commit message, or the PR text. Do not put principle names in code comments (operating rule 5.5).
- When two principles pull against each other, say which one won for this decision and why.

## Conflicts with operating rules

| Principle | Boundary |
|---|---|
| Never Block on the Human | Applies only to reversible work inside the authorized scope. Outward-facing and irreversible actions follow [operating rule 1](../ask-eric/references/operating-rules.md#1-authorization-classes) even in unattended runs. Business meaning, scope, and priority go to the owner. |
| Migrate Callers Then Delete Legacy APIs | Applies only when every caller is in this repository and there are no external consumers. Otherwise use expand, migrate, contract ([operating rule 5.6](../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices), [refactoring](../refactoring/SKILL.md)). |
| Outcome-Oriented Execution | Planned breakage stays on unshared or plan-owned branches; never on a shared trunk or interfaces with external consumers. |
| Sequence Work into Verifiable Units | Rebasing is local; force-pushing a shared branch needs explicit authorization. |
| Test Behavior, Not Implementation | Test-first is mandatory where [operating rule 5.2](../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices) says so; do not manufacture tests that mirror a wording or styling edit. See [test-driven-development](../test-driven-development/SKILL.md). |
| Prove It Works, Build the Lever | Committing a proof script or lever happens only when commits are in scope; otherwise keep it as a visible artifact and link it in the evidence record (operating rule 3). |
| Guard the Context Window | Map subagents with [harness adapters](../multi-agent-delivery/references/harness-adapters.md); a missing capability is recorded, not simulated (operating rule 4). |

## Where principles become procedures

- Fix Root Causes, Attack the Premise: [bug-diagnosis](../bug-diagnosis/SKILL.md).
- Explain the Number: [performance-investigation](../performance-investigation/SKILL.md).
- Test Behavior, Not Implementation: [test-driven-development](../test-driven-development/SKILL.md).
- Migrate Callers, Subtract Before You Add, Minimize Reader Load, Redesign From First Principles: [refactoring](../refactoring/SKILL.md).
- Separate Before Serializing Shared State, Guard the Context Window: [multi-agent-delivery](../multi-agent-delivery/SKILL.md).
- Encode Lessons in Structure: [process-improvement](../process-improvement/SKILL.md).
- Exhaust the Design Space, Experience First: [workflow-prototype](../workflow-prototype/SKILL.md), [technical-design](../technical-design/SKILL.md).

## Verification required

Every cited principle names the decision it changed, its leaf was read in this task, and any artifact it implies (lever, proof script, run output) exists and is linked.

## Completion criteria

This skill is complete for a task when the triggered principles are listed, applied to named decisions, and cited where those decisions are recorded.

## What this skill does not authorize

No principle widens authorization. Principles shape how in-scope work is done; they never authorize outward-facing or irreversible actions, scope changes, or skipping verification the operating rules require.
