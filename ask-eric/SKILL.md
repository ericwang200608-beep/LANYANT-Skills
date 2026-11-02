---
name: ask-eric
description: Choose the right LANYANT skill or path for the current situation, from a one-line wording fix to a full customer project, a bug, a performance regression, a refactor, parallel multi-agent work, a PR whose CI is failing, a production incident, or resuming interrupted work. Use whenever the user asks where to start, which skill or flow to use, what to do next, how to continue across stages, or whether the current work is complete. Also use when a request spans several kinds of work and the order matters.
---

# Ask Eric

You do not need to remember every skill. Start with the current situation and choose the smallest path that achieves the user's requested outcome.

Before describing a skill's behavior or recommending that a step be skipped, read that skill's actual `SKILL.md`. The maps below are for orientation. Locate skills through the available skill catalog or the sibling directories linked below. If a file is unavailable, report the missing skill rather than pretending to have read or invoked it. Every LANYANT skill remains independently usable; this router is optional.

All skills follow the [LANYANT Operating Rules](references/operating-rules.md): authorization classes, separate completion states, the evidence record, capability gaps as blockers, and the rules that resolve competing practices. Read them once per session before acting on a route.

## Establish Where the Work Stands

Read the user's request, existing authorization, project status, and the relevant requirements, tasks, and evidence. Find facts in those records before asking the user. Ask only for a missing decision that changes the route, and continue unaffected work.

Restate in one or two sentences the goal, the problem behind it, and the smallest change you expect to deliver. Do not wait for confirmation of that restatement; correct course if the user objects. If the evidence shows the requested change will not achieve the goal, show the evidence and stop before building.

Distinguish implementation complete, technical verification passed, customer acceptance passed, release authorized, and handover complete. For PR work also distinguish PR opened, CI green, independently verified at the current head, and merged. Checked tasks, a green build, or a successful deployment do not establish the other states.

If the requested outcome already meets its completion criteria, recommend stopping. Do not create another review or improvement task merely because more work is imaginable.

## Main Flow: Business Need to Ongoing Use

| Guide steps | Skill | Use when the current gap is… | Result to carry forward |
|---|---|---|---|
| 0 | [idea-assessment](../idea-assessment/SKILL.md) | An idea has not yet earned a specification: unclear problem, evidence, or value. | A go, needs-clarification, or kill verdict with a handoff. |
| 1–3 | [business-discovery](../business-discovery/SKILL.md) | Scope, existing workflows, data meanings, business rules, or acceptance criteria are unclear. | One authoritative specification, confirmed examples, and explicit open questions. |
| N/A | [project-principles](../project-principles/SKILL.md) | The project needs, or must amend, binding engineering and quality principles. | A versioned principles document that design, planning, and verification check against. |
| 4 | [workflow-prototype](../workflow-prototype/SKILL.md) | A workflow, interaction, or technical approach question needs a runnable answer. | A prototype, observed results or trial feedback; confirmed rule changes return to the specification. |
| 5 | [technical-design](../technical-design/SKILL.md) | Implementation, data relationships, interfaces, or deployment choices need design. | Technical and database plans, contracts, and validation arrangements. |
| 6 | [project-environment](../project-environment/SKILL.md) | Startup, checks, environments, credentials, tracker conventions, operational foundations, or extension/preset authoring are needed. | A running foundation, repeatable checks, and explicit environment readiness. |
| 7 | [delivery-planning](../delivery-planning/SKILL.md) | Work needs complete business slices, dependencies, and acceptance criteria. | An ordered task or batch plan in the authoritative tracker, checked for consistency. |
| 8 | [feature-implementation](../feature-implementation/SKILL.md) | A scoped behavior or fix is ready to implement. | Runnable changes and risk-appropriate execution evidence. |
| 9 | [system-verification](../system-verification/SKILL.md) | Implementation needs review against requirements and standards, convergence against intent, or system-level verification. | Findings, authorized fixes, and current verification results. |
| N/A | [pr-delivery](../pr-delivery/SKILL.md) | Verified changes must go up as a pull request, CI is failing, review threads are open, or a verified stack must land. | An open PR with evidence, a green and independently verified head, and merge only when authorized. |
| 10 | [delivery-proof](../delivery-proof/SKILL.md) | Staging trials, historical import rehearsal, or customer acceptance remain. | Data reconciliation, customer decisions, and remaining issues. |
| 11 | [project-release](../project-release/SKILL.md) | Release preparation, a pilot, production cutover, or release recovery is needed. | Actual release status, release records, and executable recovery procedures. |
| 12 | [project-maintenance](../project-maintenance/SKILL.md) | Training, resource handover, monitoring, support, or subsequent requests need handling. | Manuals, verified responsibilities and access, and a maintained follow-up list. |

These are stages, not mandatory stops on every request. Training and operational preparation may start before launch. Existing projects start at the current gap, using applicable evidence for completed stages. A prototype is useful when there is a question to answer, not a compulsory artifact for every change. PR delivery and production release are different procedures with different authorization: merging a PR never releases to production, and a release never skips the project's PR rules.

## Specialty Skills

Stage skills call these when a trigger occurs. Each runs a complete procedure with its own verification and completion criteria; invoke it whole rather than borrowing a few lines.

| Trigger | Skill |
|---|---|
| Building or fixing business logic, permissions, money, quantities, state, or concurrency; any bug with a correct test seam | [test-driven-development](../test-driven-development/SKILL.md) |
| A fault is hard to locate, intermittent, regressed, or reported by someone else; a production incident after containment; a captured trace or profile to read | [bug-diagnosis](../bug-diagnosis/SKILL.md) |
| A branch, PR, or diff needs review against standards and requirements | [code-review](../code-review/SKILL.md) |
| A finished or contested change must be attacked, its blast radius proven, comments audited, or bot review comments triaged | [adversarial-review](../adversarial-review/SKILL.md) |
| Something is slow, a benchmark number is quoted, or a metric must be improved by iteration | [performance-investigation](../performance-investigation/SKILL.md) |
| Structure must change while behavior stays, the architecture needs an improvement review, an interface migration, or visual parity | [refactoring](../refactoring/SKILL.md) |
| Work splits across several agents, worktrees, or PRs; an unattended or overnight run; a multi-PR program plan; a blinded evaluation | [multi-agent-delivery](../multi-agent-delivery/SKILL.md) |
| "How does this work?", "Why is it like this?", a technical question needing primary sources, learning a topic, or a message that did not land | [codebase-investigation](../codebase-investigation/SKILL.md) |
| Incoming bug reports, requests, or external PRs need triage into agent-ready or human-ready work | [issue-triage](../issue-triage/SKILL.md) |
| A large, foggy effort needs its decisions mapped across sessions before anyone builds | [decision-mapping](../decision-mapping/SKILL.md) |
| Work must move to another session, harness, directory, or person; resume after interruption; pause safely; catch up on what happened | [session-continuity](../session-continuity/SKILL.md) |
| A run went sideways, a mistake keeps recurring, instructions or skills need improving, or a prompt needs sharpening | [process-improvement](../process-improvement/SKILL.md) |
| Documents, PR text, commit messages, manuals, or any prose for people | [technical-writing](../technical-writing/SKILL.md) |
| The project needs a repeatable way to drive and observe the real product, or formal checking of orderings and invariants | [verification-harness](../verification-harness/SKILL.md) |
| A design or implementation choice applies a named engineering principle | [engineering-principles](../engineering-principles/SKILL.md) |

## Choose the Shortest Applicable Path

- **Small wording or styling change:** Clarify the requested result, change it, inspect the diff and the real rendered output, run relevant existing checks, and deliver. Do not demand a new specification, prototype, failing test, independent review, or full delivery cycle unless a real risk or project rule requires it.
- **Well-defined feature:** Reuse existing requirements, design, and environments. Plan only missing work, implement the batch with test-first cycles for business rules, and perform necessary verification. Independent review follows project requirements or concrete risk, not an automatic extra loop.
- **New customer project:** Follow the main flow across the stages actually needed, starting with discovery. Resolve business commitments with the user; make routine technical choices within scope. Collect business metric baselines before launch where required.
- **Business rule changed mid-development or mid-acceptance:** Confirm its meaning, update the authoritative specification, identify affected design, tasks, tests, manuals, and evidence, then reopen only that work. Acceptance or release evidence for changed behavior must be reassessed; unaffected evidence stays valid.
- **Bug report or failing behavior:** Reproduce first through [bug-diagnosis](../bug-diagnosis/SKILL.md); fix with a regression test; verify on the same surface that showed the bug.
- **Performance regression:** Measure a baseline before touching code, with [performance-investigation](../performance-investigation/SKILL.md). Report the measured delta, not an expectation.
- **Production incident:** Use the maintenance incident procedure and the project's authorized recovery plan to contain impact first. Use release procedures when rollback or data recovery is necessary. Deep diagnosis must not delay emergency recovery; do not send the incident back through discovery by default. Record service restored, root cause confirmed, fix complete, and target-environment verified separately.
- **Historical data import, interruption, or retry:** Rehearse in staging through [delivery-proof](../delivery-proof/SKILL.md) and its data rehearsal procedure; production import follows [project-release](../project-release/SKILL.md).
- **Parallel work or several agents:** Use [multi-agent-delivery](../multi-agent-delivery/SKILL.md) for the task graph, isolation, integration branch, conflict resolution, and final integrated verification.
- **Failing CI or open review threads on a PR:** Use [pr-delivery](../pr-delivery/SKILL.md): classify the failure before any retry, fix the cause, and re-verify at the new head.
- **Incoming bugs and requests:** Triage through [issue-triage](../issue-triage/SKILL.md). Already-defined implementation tasks can go directly to implementation when their prerequisites are met; do not triage them again merely because they are tickets.
- **Customer accepted a known limitation:** Check the authority, impact, and follow-up decision. Non-blocking acceptance may allow the relevant stage to close, while technical failures remain recorded. It does not authorize production release.
- **No customer, missing permission, or missing tool:** Finish authorized technical preparation and retain customer acceptance, training confirmation, or the blocked step as pending, naming the missing capability. Do not repeat completed checks while waiting, impersonate customer approval, or describe a skipped step as done.
- **Asked only for review:** Deliver findings and recommendations. Do not interpret review as authorization to edit application code or publish changes.
- **Resuming interrupted or handed-over work:** Use [session-continuity](../session-continuity/SKILL.md) to reconstruct state from the task record and trail, verify inherited claims on the real artifact, then route the remaining work.
- **"Is this done?":** Compare the requested deliverable with its completion criteria and evidence. If they are met, say so and recommend stopping.

## Continue Across Stages Without Losing Decisions

Maintain one authoritative specification and one authoritative task status. Reuse stable scenario identifiers and applicable evidence; record version, environment, date, executor, and outcomes where relevant. Keep implementation evidence, customer decisions, and release authorization separate. When a skill produces findings or remaining work, it writes them back to that same record instead of starting a parallel one.

For an advice-only request, explain the route without executing changes. For an action request, read the selected skill and perform the authorized work. When several stages are already authorized, continue after each prerequisite is met without asking for the same approval again. New external actions, production mutations, merges, and irreversible operations still require applicable authorization.

Stay in the current conversation when it holds useful context. At a phase boundary, decide between continuing, clearing, handing off, delegating to an agent, or compacting with the order in [session-continuity](../session-continuity/SKILL.md). If work must move to a different workspace or session, leave the current scope, decisions, evidence links, blockers, and next action in the existing task record. Do not require context clearing, a new branch, another chat, or subagents merely to cross a stage boundary.

## Help Mode

When the user asks what LANYANT can do or how to get set up, answer from this file and the linked skills; do not start work. Check once, and offer once, whether the project has: an agent workflow block in its instructions file naming the tracker, labels, glossary, and decision record locations ([project-environment](../project-environment/SKILL.md)); a project verification skill ([verification-harness](../verification-harness/SKILL.md)); and recorded principles where the project wants them ([project-principles](../project-principles/SKILL.md)). For how agent operations map to Codex, Claude Code, or Cursor, point to [harness adapters](../multi-agent-delivery/references/harness-adapters.md).

For help wording a task, read [request-writing](references/request-writing.md). For concrete task, review, parallel-work, unattended-run and resume examples, read [request-recipes](references/request-recipes.md).

A good request to any LANYANT skill states the goal, how "done" will be checked, the evidence expected, known facts and constraints, and the authorization boundary. It does not need to name skills or prescribe the method.

## Respond Clearly and Stop at the Requested Outcome

Briefly state:

1. Where the work stands, based on available evidence.
2. The next skill or short path and why it addresses the gap.
3. The concrete deliverable and evidence that will establish completion.
4. Any missing business decision, authorization, or capability that actually blocks it.

If no required work remains, say that the current task is complete and recommend stopping. Treat optional improvements as optional, and do not add an extra report solely to record this routing decision.
