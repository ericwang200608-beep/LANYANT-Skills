---
name: feature-implementation
description: Implement runnable features from clarified requirements, technical plans, and tasks, validating behavior through risk-appropriate checks, incremental failing tests for business logic, and actual execution, and resolving faults encountered during development. Use for incremental feature development or scoped fixes to implementation and test problems.
---

# Develop Features While Writing and Running Tests

Implement complete business behaviors in task dependency order. Use short red-to-green cycles for business logic and critical rules. For low-impact wording, styling, or behavior-preserving changes, inspect the diff and actual output and run relevant existing checks; do not manufacture a failing test or add tests that merely mirror the edit. Explicit project test requirements still apply. Deliver runnable changes, applicable tests, and actual execution results.

## 1. Load implementation context

Read the current task list and technical plan to establish scope, dependencies, stack, and file structure. When available, read the requirements, data model, interface contracts, technical decisions, project principles, and validation scenarios.

Read the project glossary so test names and interface terminology match the business language, and respect relevant architectural decisions. When tasks are missing or insufficient to execute, identify the gaps and complete the affected task definitions first rather than guessing business requirements.

Check existing requirements-quality checklists. Treat reviewer-maintained checkboxes as read-only; do not mark them as passed yourself. If applicable prerequisites are unmet, report the specific impact and follow project rules. Do not request confirmation again when authorization to continue already exists. Passing requirements-quality checks does not mean implementation or tests have passed.

Confirm the actual run and test entry points, reusing established foundations. Add only configuration needed to unblock this iteration. If new files require ignore rules, check the actual stack and add only missing entries.

## 2. Define tested behaviors and interfaces

Tests should verify behavior through public interfaces rather than implementation details. A good test reads like a specification, such as "a user can check out with a valid cart." It should remain valid when internal code is refactored without changing behavior.

A **seam** is a public interface where behavior can be observed without reaching inside. Test at these interfaces. First state which interfaces this iteration tests, and what each catches and misses. Retain the test scope established in requirements, plans, and tasks; ask the user only when an important choice remains unresolved.

Avoid:

- **Implementation coupling:** Mocking internal collaborators, testing private methods, or asserting only internal call counts and order. Tests breaking during a behavior-preserving refactor are a warning sign.
- **Bypassing the interface:** For example, proving user creation solely by querying internal database tables. Prefer verifying through a public query interface that the user can be retrieved.
- **Tautological assertions:** Recomputing expected results using the same algorithm as the implementation, so the test cannot contradict it. Expected values must come from independent evidence: known-good constants, worked examples, or the requirements specification.
- **Horizontal batching:** Writing all tests first, then all implementation. This tends to verify imagined code shapes instead of actual behavior.

Mock only at external system boundaries as needed, such as external APIs, time, randomness, or the filesystem. Prefer a test database for database work. Do not mock your own internal modules as a substitute for real collaboration. Pass external dependencies in from callers so they can be replaced.

For business rules involved in this iteration, include corresponding behavior checks:

- Normal operations produce expected outcomes.
- Unauthorized operations are rejected.
- Duplicate submissions do not create unintended duplicate data.
- Concurrent operations preserve quantities or shared state according to confirmed rules.
- Failed operations preserve the agreed data consistency.
- New behavior does not break affected existing functionality.

Select scenarios from actual requirements. Add missing critical checks to the tasks rather than omitting them because a template labels testing optional.

## 3. Complete one red-to-green cycle at a time

For work requiring test-first development, each cycle addresses one interface, one behavior test, and one minimal implementation:

1. Write a test describing the expected behavior.
2. Run it and observe failure caused by the target behavior being missing or incorrect. Environment or syntax errors do not substitute for this step.
3. Write only the code needed to pass that test.
4. Run it again and observe it pass.
5. Choose the next behavior based on what the cycle taught you, and repeat.

Do not implement future tests in advance or add speculative features. Do not build an entire test system in one pass; each test should be a small step that checks real behavior.

Prefer existing implementations, standard libraries, platform capabilities, and installed dependencies. Choose the smallest implementation that fully solves the current problem without removing necessary input validation, error handling, security, or accessibility.

This loop does not include a separate refactoring phase. Follow structural changes explicitly scheduled in the tasks, without expanding feature implementation into unrelated cleanup.

## 4. Complete the current batch in dependency order

Extract phases, dependencies, identifiers, paths, and parallel markers from the task list. Execute sequential tasks in dependency order. Only mutually independent tasks that do not modify the same files may run in parallel. Sequence tasks touching the same file.

Satisfy necessary prerequisites, then implement the relevant models, services, pages, or interfaces and integrate databases, logging, and external services. Business logic and critical rules follow red-to-green cycles; low-impact changes use the proportionate checks described above. Phase order does not mean writing all tests before starting implementation.

Run corresponding checks after each verifiable portion before continuing. If a step fails, stop downstream work that depends on it and provide the error and context. Independent work may continue.

For faults that are hard to locate, repeatedly fail, or occur intermittently, read [Fault Diagnosis and Regression Verification](references/debugging.md). Establish a reproduction loop that detects the specific symptom before fixing it. Do not make successive speculative code changes.

If test expectations contradict requirements, check their basis and explain the discrepancy. Never manufacture a pass by weakening assertions, skipping failing cases, or rewriting historical results.

## 5. Verify integration and update task status

After completing the current behavior, run relevant regression tests and project-required checks. Verify that implementation matches requirements and the technical plan, tests pass, and coverage meets project requirements. Do not invent a coverage target where none exists.

Verify through an actual entry point suited to the feature: operate pages in a browser, and make real API or CLI calls. Check user-observable results. Successful compilation or tests with mocked dependencies do not establish that the complete feature works.

Inspect actual artifacts rather than inferring success from agent reports, file timestamps, or cached results. When external services are mocked, state which integrations remain untested. If environment blockers or missing permissions prevent execution, record unverified items and their impact.

Update completed work in the existing task list, checking off tasks only after the corresponding implementation and necessary verification are complete. Preserve failed, blocked, and unverified items, distinguishing implementation defects, test problems, and environment problems. Do not automatically check off requirements-quality checklists or customer acceptance records along with development tasks.

## 6. Deliver and finish

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Deliver runnable changes, automated tests where required, and actual execution results. Briefly explain:

- The business behavior completed in this batch and how to start or demonstrate it.
- The checks actually executed and their results.
- Remaining failures, unverified items, and their effect on the conclusion for this batch.

End this implementation iteration when the agreed features run and can be demonstrated, necessary tests and checks pass, and blockers are resolved or explicitly dispositioned. If evidence needed for this batch's acceptance is missing, report partial completion accurately.

Implementation and testing completion do not imply independent review, customer acceptance, or production release approval. An implementation-only request does not authorize another batch, commits, pushes, or publication.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Implementation branches and checklist gate

For specification-based implementation read [the complete implementation workflow](references/implement-workflow.md). Before changing code, run `python3 <this-skill>/scripts/checklist_gate.py <feature-directory> --json`. A FAIL requires a scoped owner decision or checklist-quality correction by its reviewer; implementation never changes markers to manufacture a pass. NOT_APPLICABLE means no applicable checklist exists and is not an approval.

Use [single-ticket flow](references/single-ticket-flow.md) for one issue, [task-list execution](references/task-list-execution.md) for an ordered plan, and [feature ownership](references/feature-lead-playbook.md) for a parallel feature. Follow [test-driven development](../test-driven-development/SKILL.md) at agreed seams for business logic, quantities, money, permissions, state, concurrency, and defects; inspect real output proportionately for wording and styling. Use [bug diagnosis](../bug-diagnosis/SKILL.md) for a failure and [multi-agent delivery](../multi-agent-delivery/SKILL.md) for parallel ownership. For TypeScript read [best practices](references/typescript.md) and [patterns](references/typescript-patterns.md). Verify at the current candidate with [code review](../code-review/SKILL.md).
