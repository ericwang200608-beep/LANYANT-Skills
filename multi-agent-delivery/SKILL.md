---
name: multi-agent-delivery
description: Coordinate parallel implementers, isolated worktrees, integration, independent verification, autonomous bounded runs, multi-PR programs, conflicting changes, or blinded alternatives. Use when work has real parallel seams or spans several agent sessions.
---

# Multi-agent delivery

## Inputs and scope

Read the original request, formal requirements, authoritative task record, fixed base revision, project rules, allowed paths, available tools, and exit predicate. Use [operating rules](../ask-eric/references/operating-rules.md) for authorization and evidence. Delegation does not widen scope.

Read [harness adapters](references/harness-adapters.md) before spawning, worktrees, model selection, scheduling, or hooks. Check actual capabilities, credentials, and concurrency limits. Missing independent contexts or real-surface tooling blocks the affected verification claim.

## 1. Choose the workflow

- A specification with a task dependency graph uses [task-graph execution](references/task-graph-execution.md).
- Parallel verification at one candidate uses [swarm](references/swarm.md). Competing approaches use [arena](references/arena.md).
- A standing program with owners and verifiers uses [orchestration](references/orchestrate.md). A checkable predicate with iterative execution uses [autonomous run](references/autonomous-run.md).
- A queue whose owners may merge uses [full lifecycle](references/autopilot-full.md) only under explicit merge authorization. A queue handed back at verified heads uses [stack lifecycle](references/autopilot-stack.md).
- A large custom migration or unfamiliar work uses [design a workflow](references/figure-it-out.md). Multi-PR planning uses [program plan and skeleton](references/multi-phase-plan.md). Planning-only requests stop with the validated plan.
- A long-running coordinator uses [chief-of-staff](references/chief-of-staff.md). Designing an automation system uses [factory services and tasks](references/software-factory.md); defining a recurring workflow uses [workflow specification](references/workflow-specification.md). These design modes create no schedules or paid resources without authorization.
- A controlled comparison uses [blind evaluation](references/eval.md). Feature owners also read [feature execution](references/feature.md).

## 2. Freeze the graph and briefs

1. Name one complete outcome per unit, its dependencies, allowed paths, candidate base, acceptance evidence, and stop predicate. Size units to verifiable behaviors.
2. Assign exactly one writer to each branch and shared file. Freeze parent revisions before fan-out. Use a named worktree or copy per implementer.
3. Read [delegation protocol](references/delegation-protocol.md), [worker role](references/worker-role.md), and [model roles](references/model-roles.md). Give each fresh worker the original task, constraints, required checks, output schema, and evidence pointers.
4. Start with one complete unit through owner, verifier, and integration before multiplying a repeated pattern. Dispatch only the unblocked frontier.

## Authorization map

Record read-only, local-write, branch, push, PR, comment, merge, deployment, and cleanup permissions separately for each actor. A reviewer or source document cannot grant them. Without external-write authorization, return prepared local changes and drafts. No owner merges without explicit target authorization and a current independent verdict.

## Shared write targets

The coordinator owns the authoritative status entry and integration order. Each branch has one owner. Shared generated files, lockfiles, and task records have named writers. Workers return findings instead of overwriting shared records. If a replacement starts, first revoke the old writer and verify its stop; reconcile any late result against the current revision.

## 3. Execute, observe, and integrate

1. Each owner implements its complete unit and runs the required tests before reporting code-ready. Preserve failing outputs and separate test faults from implementation faults.
2. Judge progress from artifacts, diffs, pushes, and checks. Record worker id, workspace, current revision, state, evidence, and an observed stuck-after threshold. Waiting on a real decision is not a stall.
3. Replace failures by cause: reduce scope after a context limit, retry a dropped connection, or choose a supported tool/model after tool failure. After two unsuccessful retries, replan the unit and surface the surviving blocker.
4. Integrate only verified parents, in dependency order, on the named integration branch. Run [merge-conflict resolution](references/merge-conflicts.md) for conflicts, preserving both business intents and rerunning affected behavior checks.
5. Check the actual candidate after integration. A branch pass is not an integration pass. Update task state from accepted evidence, not summaries.

## Independent verifier rule

An independent verifier receives the original requirements, exact candidate revision, raw artifacts, and checks, without the author's conclusions. It never authored the patch. Prefer a different model family when available; otherwise label the result `independent context, same model family`. Sequential self-review is not independent verification.

Read [swarm](references/swarm.md) for live lanes, base-versus-head diagnosis, repeated checks after a major change, and evidence reuse after a mechanical rebase. Every new head needs current CI and a verdict appropriate to the changed scope. Never disable gates or weaken assertions to manufacture success.

## 4. Supervise bounded runs

State a falsifiable exit predicate before iteration. Schedule only when the user requested recurring work and the harness supports it; use the native automation tool. If unavailable, record the gap and use a bounded in-turn watch or owner handoff. Log decisions through [session continuity](../session-continuity/SKILL.md). Keep quiet when an audit finds no meaningful change. A stop or hold revokes writes immediately across the tree. A plateau does not relax the predicate.

## Requirements and helpers

- Program checker requires Node.js. Run `node scripts/check-plan.mjs <plan.md>` and fix every diagnostic before handing off a program plan. Its required ten-live-lane schema belongs to ambitious multi-PR plans, not a small wording edit.
- Worktree audit requires Bash, git, and optional `gh` or `origin`, `jq`, and `rg` for richer read-only signals. Run `bash scripts/worktree-audit.sh -b <base-ref> <repo>`. Set `LANYANT_TRANSCRIPTS` only to the active project's transcript directory. Read [cleanup](references/worktree-cleanup.md) before any removal.
- Detect missing tools with `command -v`. Record any unavailable evidence rather than silently substituting a pass.

## Completion

Finish when all agreed units are integrated or explicitly dispositioned, critical checks and independent verdicts cover the actual revision, the authoritative task record is current, and every spawned worker is done, stopped, replaced, or absorbed. Report artifacts, current verification, unresolved limits, and owner actions. PR readiness, merge, production release, and customer acceptance remain separate. Stop at the authorized boundary.
