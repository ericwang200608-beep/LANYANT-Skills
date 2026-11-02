---
name: delivery-planning
description: Break requirements, technical plans, or clarified discussions into dependency-ordered development tasks and delivery batches, define complete business outcomes and acceptance criteria for each batch, and check consistency across requirements, plans, and tasks. Use before incremental implementation or to adjust the granularity and order of existing tasks.
---

# Development Tasks and Delivery Batches

Break work into complete business slices that cut across layers, declaring which tasks block each slice. Each delivery batch should be independently demonstrable or verifiable, so the product owner knows what capability the next batch adds.

## 1. Gather context

Start with the current conversation and available materials. When the user provides a requirements path, issue number, or link, read its full body and relevant comments.

Read user stories and priorities from the requirements, and the stack, dependencies, and project structure from the technical plan. When available, read the data model, interface contracts, technical decisions, validation scenarios, and project principles. Do not require every project to use the same document names or directories.

If the current code is not yet understood, inspect the relevant code. Use project terminology in task titles and descriptions, and respect relevant architectural decisions. Identify existing work and completed environment foundations to avoid scheduling them again.

Map entities and interfaces to user stories, and technical decisions to necessary preparation. Identify whether local prefactoring would make the change easier. Include only preparation that serves the current implementation.

When missing requirements or technical decisions affect the breakdown, identify the specific gaps. Do not quietly replace unresolved business or architectural decisions with task descriptions.

## 2. Split work into complete business slices

Each slice cuts through the data, interfaces, UI, and verification needed for the behavior, rather than completing only one layer. A completed slice should be independently demonstrable or verifiable and sized to fit within a fresh working context.

List the other slices that block each slice. A slice with no blockers can start immediately. Dependencies represent genuine prerequisites; appearing earlier in a list does not itself make work a dependency.

Assign priorities such as P1, P2, and P3 according to user-story importance. Complete the most important story first, then add capabilities incrementally. Each increment should deliver value while preserving previously established behavior.

Treat one slice or a tightly related group of slices as a delivery batch. Describe batches through business behavior, such as "create and save a purchase order" or "submit and approve a purchase order," rather than "finish the database," "finish the backend," or "finish the frontend."

For each batch, state:

- **What it delivers:** End-to-end behavior from the user's perspective.
- **Blocked by:** Batches or tasks that must complete first, or explicitly none.
- **How to demonstrate it:** The user's actions and observable results.
- **Acceptance criteria:** Clear, checkable passing conditions.

Wide mechanical refactors are an exception. If a shared structural change would break many callers at once and cannot remain usable through business slices, sequence it as expand–migrate–contract. Add a compatible new form first, migrate callers in batches sized by impact, then remove the old form after all migrations finish. If batches cannot pass checks independently, identify a shared integration branch and a final integration-and-verification task. Do not promise independently deliverable intermediate batches.

## 3. Generate actionable tasks for each batch

Organize work as needed:

1. **Setup:** Unfinished project initialization or local prefactoring.
2. **Foundational prerequisites:** Shared capabilities that genuinely block user stories.
3. **User stories:** Each story's goal, independent verification criteria, and required tasks, in priority order.
4. **Completion work:** Cross-story integration, documentation, and verification within scope.

Reference completed setup as an existing condition rather than generating new pending tasks. Shared prerequisites block only the work that depends on them.

Order steps within a batch by dependency: data models before services that use them, services before dependent endpoints or UI, and core behavior before end-to-end verification. When test-first work is required, place tests before the corresponding implementation and require observing failure before completing implementation.

Plan test tasks according to requirements, project conventions, and acceptance risk. Explicitly required tests must appear in the list, and every story needs an independent verification method. For critical rules involving permissions, money, or quantities, specify the checks rather than merely saying "tests pass."

Use stable identifiers and a checklist format for implementation tasks:

```text
- [ ] T001 [US1] Specific task description
- [ ] T002 [P] [US1] Specific task that can run in parallel
```

`US1` identifies the user story; shared setup tasks may omit the story label. Use `[P]` only for tasks with no mutual dependencies that do not modify the same files. Sequence tasks that modify the same file.

Include precise paths in implementation tasks when the project structure is established. Keep business-facing batch or ticket descriptions focused on behavior, acceptance criteria, and blockers rather than accumulating paths and code that may become stale. If a prototype contains a state machine, data structure, or type decision that is more precise than prose, retain only the smallest snippet expressing that decision.

List the dependency order of user stories and identify task groups that can run in parallel. Work is ready to start when all its blockers are complete. For a linear dependency chain, proceed in order.

## 4. Check consistency across requirements, plans, and tasks

Run a consistency check after producing a complete draft. The check itself does not modify requirements, technical plans, or project principles.

Map requirements and user stories to tasks. Preserve existing requirement identifiers. Success criteria requiring engineering work, such as performance-validation infrastructure, also need tasks. Do not treat post-launch business metrics as promises that development tasks alone can fulfill.

Schedule required metric collection and pre-launch baseline work before its collection opportunity is lost, with an owner. Reuse existing acceptance scenario identifiers and definitions instead of creating a competing set.

Focus on:

- **Duplication:** Near-duplicate requirements or tasks.
- **Ambiguity:** Descriptions such as "fast," "secure," or "easy to use" without checkable criteria, and unresolved placeholders.
- **Underspecification:** Actions missing an object or outcome, user stories missing acceptance criteria, or tasks referencing structures absent from the plan.
- **Principle conflicts:** Violations of mandatory project requirements or missing required quality checks.
- **Coverage gaps:** Requirements without tasks, tasks without a requirement or story, or necessary verification absent from the list.
- **Inconsistency:** Terminology drift, conflicting data objects or technology choices, and contradictions between task order and dependencies.

Also check that task identifiers and references are valid, blocking relationships contain no cycles, and each batch includes the work needed to produce a complete outcome.

Report material findings and proposed corrections. Within the current authorization, correct omissions, duplication, and ordering in the task draft. If a correction changes confirmed requirements, technology choices, or project principles, resolve that decision first rather than silently rewriting upstream materials.

When serious conflicts prevent implementation, mark affected tasks as not ready. Requirements-quality checks establish clarity, completeness, and consistency of requirements and plans; they do not establish that software functionality has passed testing.

## 5. Present the breakdown and save tasks

Present batches as a numbered list or table. Each entry should include at least a short title, blockers, delivered behavior, and acceptance criteria. Explain the recommended smallest initial delivery and which work can run in parallel.

When breakdown decisions need user input, group the questions: whether granularity is appropriate, whether blockers are genuine, and which batches should be merged or split further. Retain decisions already made.

Save tasks in the project's existing authoritative task location. For a local checklist, use clear batch headings and retain stable identifiers, dependencies, and acceptance criteria. For local tickets, use one file per ticket, numbered in dependency order, and reference a shared batch plan rather than maintaining duplicate status records.

When the user has authorized publication to an external tracker, create or update tickets with blockers first so dependencies can reference real identifiers. Use native blocking relationships when supported; otherwise list blockers explicitly in the ticket body. Use existing project labels. If the source is a parent issue, link it without closing it on your own.

Without publication authorization, complete the local checklist or ticket drafts. Do not misreport waiting for publication as an incomplete breakdown. Update only affected portions of existing tasks, preserving completion status and historical evidence.

## 6. Deliver and finish

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Deliver an ordered task list with dependencies and acceptance criteria, summarizing:

- The business capability added by each batch and how to demonstrate it.
- The recommended first batch and smallest deliverable scope.
- Blocking relationships and work that can run in parallel.
- Consistency-check results, outstanding decisions, and work that is not yet ready.

Completion means the product owner can understand what capability the next batch adds, implementers can work from the tasks and existing design, and every key requirement has corresponding tasks and passing conditions.

A completed task list does not mean features have been implemented or accepted. A planning-only request ends with the task list; it does not authorize development, commits, or publication.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Detailed planning branches and tools

For tracer-bullet tickets read [ticket decomposition](references/tracer-bullet-tickets.md), preserving vertical user behaviors and real dependency edges. The external-consumer migration exception uses expand, migrate, contract; internal callers use one verified migration wave. Follow existing authorization for publication and business decisions; do not reopen an approved breakdown for routine local choices.

For specification-based tasks read [task generation](references/tasks-workflow.md), use [the task template](assets/tasks-template.md), then run [read-only consistency analysis](references/analyze.md). Analysis keeps the 50-finding cap, severity levels, coverage metrics, and constitution conflict rule. Use [task publishing](references/taskstoissues.md) only for authorized tracker writes.

Python 3 helpers, run from the project root: `scripts/check_prerequisites.py --json [--require-tasks --include-tasks]`; `scripts/setup_tasks.py --json`; `scripts/check_tasks.py <tasks.md> --json`; and `scripts/resolve_tasks.py --json`. Prefix each with `python3 <this-skill>/`. Path resolution uses `.lanyant/feature.json` or `LANYANT_FEATURE_DIRECTORY` and the canonical sibling helper. Checkers are read-only. Existing project template overrides take precedence; composing YAML template layers additionally require PyYAML.

`scripts/tasks_to_issues.py <tasks.md> --root <project-root> --repo <owner/repository>` defaults to offline dry-run. `--apply` is only for an authorized GitHub publication. It checks the exact github.com origin, pins every gh authentication/API operation to `--hostname github.com` even if `GH_HOST` differs, reads both open and closed issues across all pages, deduplicates whole T### identifiers including T1000, and stops on an uncertain write outcome. A rerun checks existing issues again. The helper never closes a parent issue.

For an explicitly lean feature use [lean specification](references/lean-specify.md), [lean planning](references/lean-plan.md), [lean tasks](references/lean-tasks.md), and [lean implementation](references/lean-implement.md). This changes artifact depth, not the tests required by business logic or risk. Read [workflow and customization contracts](references/customization.md) for resumable runs, gates, overlays, hooks, and unsupported platform features.
