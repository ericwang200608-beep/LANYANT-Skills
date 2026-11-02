---
name: test-driven-development
description: Red-green test-driven development that produces tests worth keeping. Agree the seams first, write one failing behavior test, watch it fail for the right reason, write the minimal code to pass, repeat in vertical slices. Covers when test-first is mandatory (business logic, permissions, money, quantities, state transitions, concurrency, data consistency, every bug fix with a correct seam) versus proportionate checks, mocking only at system boundaries, test anti-patterns, regression tests for bug fixes with failing-before and passing-after evidence, and typed partial fixtures in TypeScript. Use whenever the user asks for TDD, red-green-refactor, a failing test, a regression test, integration tests, or test-first work; whenever a task touches business rules or critical data; when fixing a bug that has a cheap local test path; when a task template marks tests optional; or when deciding whether a change needs a new test at all.
---

# Test-Driven Development

Test-driven development is the red to green loop. This skill makes that loop produce tests worth keeping: when test-first is required, where tests go, what a good test is, the anti-patterns, the rules of the loop, and the evidence to report. Every section applies on every cycle: consult them before and during the loop, not after.

## When to use

- A task implements or changes business logic, permissions, money, quantities, state transitions, concurrency, or data consistency.
- A bug fix has a correct seam for a regression test (see [bug-diagnosis](../bug-diagnosis/SKILL.md) for finding the cause first).
- The user asks for TDD, a failing test, a regression test, or integration tests.
- You must decide whether a change needs a new test, or a task template says tests are optional.

For the surrounding feature workflow (task order, integration, status updates) use [feature-implementation](../feature-implementation/SKILL.md). This skill governs the test cycle inside it.

## Inputs to read

- The requirement, acceptance criteria, task record, and technical plan for the behavior under test. Expected values come from these, not from running the code.
- The project's domain glossary (for example `GLOSSARY.md`) so test names and interface vocabulary match the project's domain language.
- Architectural decision records in the area you are touching. Respect them.
- The existing test suite: its runner, layout, fixtures, and the closest tests to the code path. Reuse the established harness.
- Explicit project or task test requirements (coverage rules, required test types). They override the defaults below.

## 1. Decide whether test-first is mandatory

Apply these rules in order:

1. **Explicit project or task requirements win.** If the project, constitution, or task record requires or forbids a kind of test, follow it.
2. **Test-first is mandatory** for business logic, permissions, money, quantities, state transitions, concurrency, data consistency, and every bug fix that has a correct seam. Write the failing test first and watch it fail for the right reason before changing production code.
3. **Proportionate checks** apply to wording, styling, and behavior-preserving changes. Inspect the diff and the real output and run the existing checks. Do not manufacture tests that mirror the edit.
4. **"Tests optional" never removes a critical check.** A task template or plan that marks tests optional, or says to include them only if requested, does not remove a check that the requirements make critical. Add the missing critical test tasks to the existing task record and run them.
5. **Prefer no new test over a bad test.** A bad test mostly tests mocks, encodes current implementation details, depends on timing or unrelated global state, needs expensive infrastructure for a small fix, or would be deleted immediately after proving the fix. When the only available test would be bad, use the closest executable check instead (section 7) and record why. For the mandatory categories in rule 2, a missing correct seam is a finding to record, not permission to skip verification.

Record which rule applied in the task record when it is not obvious from the change.

## 2. What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests should not. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it does not care about internal structure.

The core rule: a test is a claim about what the code does for its users (a caller, an end user, or another service). Assert what those users can observe through the interface they use: return values, errors, state they can read back, and effects on systems outside the code. Judge every test against two imagined edits:

- **Break the behavior.** Make the code return a wrong value, skip an effect, or do the effect twice. If the test still passes, it proves nothing.
- **Change the internals.** Keep every observable result the same and restructure the code underneath. If the test now fails, it is pinned to the implementation.

Keep a test that catches the first edit and survives the second. Rewrite or delete the rest. The full rule, including how the contract decides edge cases (calls to external services, empty results, error types versus error messages, invariants), is in [test-behavior-not-implementation](../engineering-principles/references/test-behavior-not-implementation.md).

See [tests.md](references/tests.md) for good and bad examples and [mocking.md](references/mocking.md) for mocking rules. For TypeScript tests that need partial or intentionally wrong fixtures, read [typed-partial-fixtures.md](references/typed-partial-fixtures.md).

## 3. Agree the seams before writing tests

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at agreed seams.** Before writing any test, write down the seams under test. A seam is agreed when the task record, plan, or interface contract already names it, or when the owner confirms it. No test is written at an unagreed seam. You cannot test everything; agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

1. Identify the public interface and seams from the confirmed task and existing contracts. Ask the owner only if selecting the seam changes business meaning or an explicit project rule requires approval. Routine technical seam choices are covered by authorization to implement and verify the task.
2. List each proposed seam with **one line on what it catches and one line on what it misses**.
3. Select the behaviors to test at each seam from the actual requirements. For each business rule in scope, include the checks that apply:
   - Normal operations produce expected outcomes.
   - Unauthorized operations are rejected.
   - Duplicate submissions do not create unintended duplicate data.
   - Concurrent operations preserve quantities or shared state according to confirmed rules.
   - Failed operations preserve the agreed data consistency.
   - New behavior does not break affected existing functionality.
4. Record technically selected seams against the existing contract; this establishes agreement within delegated implementation scope. If a seam needs an unresolved business decision or explicit owner approval, present that specific decision and wait for it. Continue unaffected work while waiting. In an unattended run with no one to confirm, record the proposed seams and the open confirmation as a blocker in the task record; do not write tests at those seams.

When the shape of the interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), use the module, interface, depth, seam, and adapter vocabulary in [refactoring](../refactoring/SKILL.md) and settle the interface in [technical-design](../technical-design/SKILL.md) before testing it. Consult them as references, not as a separate session.

## 4. Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior has not changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test, one implementation, repeat, each test a **tracer bullet** that responds to what the last cycle taught you.
- **Mock-heavy**: mocking anything you control. Mock at system boundaries only (external APIs, time, randomness, sometimes the file system or database; prefer a test database). See [mocking.md](references/mocking.md).
- **Weakened to pass**: changing a test to match a wrong implementation, loosening an assertion, or skipping a failing case to get green.

## 5. Rules of the loop

Each cycle covers one seam, one behavior test, and one minimal implementation:

1. Write a test describing the next expected behavior at an agreed seam.
2. Run it and watch it fail. The failure must be caused by the target behavior being missing or wrong. A compile error, missing import, environment failure, or unrelated assertion does not count: fix the test or the setup and run again until it fails for the right reason. If it passes, the test does not cover the missing behavior; correct it before touching production code.
3. Write only enough code to pass that test. Do not anticipate future tests or add speculative features. Do not remove necessary input validation, error handling, security, or accessibility to stay minimal.
4. Run it again and watch it pass. Run the nearby tests that could be affected.
5. Choose the next behavior from what this cycle taught you, and repeat.

Rules that apply across cycles:

- **Red before green.** No production change for a mandatory behavior without a test that has been seen failing for the right reason.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage ([code-review](../code-review/SKILL.md)) or to a scheduled structural change ([refactoring](../refactoring/SKILL.md)), not to the red to green cycle. Do structural work only when the task schedules it.
- If you forced a red by mutating code or a fixture, `diff` against a pristine copy to prove the mutation landed before you trust the red.
- If a test expectation contradicts the requirements, check its basis and raise the discrepancy with the owner. Never manufacture a pass.

## 6. Test tasks in a task list

When the project plans work as a task list grouped by user story:

- Test tasks for a story are written and seen failing before the implementation tasks they cover. Run each test task as a vertical slice with its implementation: one test, red, the code that makes it green, then the next test. Task order is a dependency constraint, not an instruction to write every test first.
- Contract tests cover each interface or endpoint in the contracts; integration tests cover each user journey. Each story keeps an independent test that shows it works on its own, checked at the story checkpoint before the next story starts.
- Test tasks marked parallel must touch different files and have no dependencies on each other. Tasks touching the same file run in sequence.
- Put requirement and task identifiers in test names and task records, not in code comments.
- Mark a test task complete only after it has been seen failing and then passing. Keep failed, blocked, and unverified items visible.

## 7. Regression tests for bug fixes

Use this when fixing a bug whose cause is known. Find the cause first with [bug-diagnosis](../bug-diagnosis/SKILL.md) when it is not.

1. **Understand the bug.** Identify the intended behavior, current behavior, affected path, and smallest observable reproduction.
2. **Choose the narrowest executable check.** Prefer the closest unit, component, integration, or regression test already used for that code path. The seam is correct only if the test exercises the real bug pattern as it occurs at the call site; a single-caller test for a bug that needs multiple callers gives false confidence. If no practical test path exists, do not create one from scratch just to satisfy the workflow.
3. **Write the failing test first.** Add the smallest focused test that would have caught the bug. It encodes intended behavior, not the current implementation.
4. **Run the new test before fixing.** Confirm it fails for the intended reason. If it passes or fails for an unrelated reason, correct the test or reproduction before editing the implementation.
5. **Fix the bug.** Make the smallest production change that satisfies the intended behavior while preserving nearby contracts.
6. **Rerun the regression test.** Confirm it now passes, then run the nearby tests and project-required checks.
7. When commits are in scope, stage them so the failing test lands before the fix in history.

If a failing test is impractical (it would need broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, vague reproduction steps, or large unrelated fixture churn), use the closest executable regression check instead: a targeted script, manual reproduction command, browser automation, snapshot comparison, log assertion, or focused integration check. If no correct seam exists, record that as a finding: the architecture prevents locking the bug down. Hand it to [refactoring](../refactoring/SKILL.md) as a candidate.

Guardrails:

- Do not change tests merely to match a wrong implementation.
- Do not weaken existing assertions unless the expected behavior has genuinely changed and the reason is clear and recorded.
- Keep the regression test focused on the bug. Avoid broad fixture churn or unrelated coverage expansion.
- If the bug is flaky, make the test deterministic where possible (pin time, seed randomness, isolate the file system and network) and record the signal being locked down.
- If the bug exposes a broader class of failures, first land the focused regression path, then propose sibling coverage as a separate item.

## Verification required

- Every mandatory behavior has a test that was **measured** failing for the right reason before the production change and **measured** passing after it.
- The failing-before output is the target behavior's failure, not a setup or syntax error.
- Nearby tests and the project's required checks pass after the change.
- Every new test passes the two-edit check in section 2.
- Mocks exist only at system boundaries. State which integrations remain unexercised because they were mocked.
- When failing-before evidence could not be produced, the reason and the substitute check are recorded.

## Outputs and where state is updated

Report the evidence, not just the outcome:

- The seams tested, with their catches and misses lines.
- The failing-before test or executable check, its command, and the failure it produced.
- The passing-after run and the nearby validation performed.
- Any substitute check used instead of a new test, and why.
- Unverified items and integrations covered only by mocks.

Record these in the existing task or delivery record following [operating rules section 3](../ask-eric/references/operating-rules.md#3-evidence-record), labeling each claim measured, inferred, or unverified. For read-only work, report them in the conversation. Do not create a separate test report.

## Completion criteria

- The agreed behaviors for this batch each completed a red to green cycle, or have a recorded substitute check and reason.
- Required checks pass, and failures, blocks, and unverified items are recorded as such.
- No test was weakened, skipped, or rewritten to manufacture a pass.
- The task record reflects what was actually run.

## What this skill does not authorize

This skill authorizes reversible local work: writing tests, editing code in the working tree, and running tests. It does not authorize adding dependencies outside the task's scope, committing when commits are not in scope, pushing, opening pull requests, or changing shared test infrastructure used by other teams. Deciding business meaning of an expected value belongs to the owner. Passing tests do not imply independent review, customer acceptance, or release approval ([operating rules section 2](../ask-eric/references/operating-rules.md#2-completion-states-are-separate)).
