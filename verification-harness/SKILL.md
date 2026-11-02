---
name: verification-harness
description: Generate, execute, and maintain project-local runtime verification skills and feature maps; generate and resynchronize formal verification for costly invariants, concurrency, retries, parsers, or unsafe code; run bounded TLA+ checks and explain counterexamples as statecharts. Use when a project lacks an executable way to prove real user behavior, when verification drifts after code changes, or when tests alone cannot cover a stated safety property.
---

# Verification harness

Use this skill to leave an executable, evidence-producing verification workflow for the next engineer. Select one mode, read its complete procedure, and preserve its completion gate. Runtime proof and formal proof answer different questions; a bounded model pass does not establish whole-system correctness.

## Inputs and scope

Read the original requested behavior, the existing project skill directory, documented build/run commands, feature entry points, relevant tests, and the authoritative task record. Read [operating rules](../ask-eric/references/operating-rules.md) before making changes. Ask only for facts that code and safe experiments cannot establish.

| Trigger | Required procedure |
|---|---|
| No scripted way to drive the real app | [Generate runtime verification](references/create-runtime.md) |
| Existing feature map or runtime harness may have drifted | [Maintain runtime verification](references/maintain-runtime.md) |
| A costly promise needs model checking, a verifier, or proof | [Generate formal verification](references/create-formal.md) |
| Covered code changed after the verification sync commit | [Maintain formal verification](references/maintain-formal.md) |
| Run a TLA+ model or explain a violation as a state path | [Bounded statecharts](references/statechart.md) |

## Procedure

1. Locate the current project verification skill by its behavior, not a fixed name. Select generation only when no relevant harness exists. Follow the project's supported skill location; `.agents/skills/` in the mode references is a local example, not a runtime requirement.
2. Ground commands, selectors, covered code, assumptions, and prerequisites in the actual checkout. First establish that the base builds and starts, or record the precise blocker.
3. Execute the selected mode in full. Runtime generation must launch, doctor, drive a mapped feature, capture action/result/side-effect evidence, and clean up. Runtime maintenance must read every mapped feature from source and drive every feature live. Formal generation must catch a deliberate real-code mutation. Formal maintenance must reconcile every covered change since the sync commit and classify drift separately from product bugs.
4. Keep instances, databases, sessions, and ports isolated. Kill only processes created by the run. Preserve evidence after cleanup and verify that it still exists. A failed iteration also requires scoped cleanup.
5. Keep findings as findings. Change product code only within an authorized implementation task. Do not weaken a journey, property, bound, or assumption to manufacture a pass.
6. Update the existing task record and the generated verification skill with the actual candidate, commands, bounds, outcomes, evidence, and remaining limitations. Move a formal sync commit only after checking correspondence to code. Apply the [completion-state and evidence rules](../ask-eric/references/operating-rules.md#2-completion-states-are-separate).

## Statechart requirements and commands

The executable [statechart launcher](scripts/statechart/statechart) selects Node 22.18 through 22.x, Node 23.6 or later, Bun 1.1.5 or later, or Deno 2 or later. Detect availability with the runtime's `--version`. The checker needs TLC 1.7.4 and Java 11 or later. `mise` can provision the pinned tools with network access. If `mise` is unavailable, set `TLA2TOOLS` to a verified jar and optionally `JAVA` to the Java binary. The pinned jar SHA256 is `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`. Check its checksum before executing it.

Run from a scratch folder outside the product repository:

```sh
<verification-harness dir>/scripts/statechart/statechart SPEC.tla --config SPEC.cfg --view view.ts --out proof-1
```

Read the [complete model, chart, bound, result, and handoff rules](references/statechart.md) before running. Exit 0 means the configured checks held, exit 1 denotes a model violation, and exit 2 denotes a tooling/model execution error; inspect the report rather than inferring from a single exit alone. Each unchecked rule remains unverified. Replay each reported bug path against real code. Render only through the [rendering procedure](references/statechart-render.md) when an image is requested; record absent rendering capability accurately.

## Completion

A runtime harness is deliverable only after its own launch/doctor/drive/evidence/cleanup cycle has run and proof survives teardown. A maintenance pass is clean only after every mapped feature has source and live coverage. A formal harness must fail on a relevant real-code break and return to its prior outcome after the mutation is removed. State the verified scope and what remains outside it in plain language.

This skill authorizes no production access, product repair outside the task, external publication, PR creation, scheduler creation, or paid resource. Apply existing authorization and map unavailable agent capabilities through [harness adapters](../multi-agent-delivery/references/harness-adapters.md).
