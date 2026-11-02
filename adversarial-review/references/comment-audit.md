# Comment Audit

Spawn a fresh comment auditor, audit its report, act on accepted findings, and offer encodings for claimed constraints. Defer to the auditor's fresh perspective: it judges comments without the author's reasons in its context.

This applies [operating rule 5.5](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices): a code comment stays only when it states a non-obvious constraint that code cannot express. Requirement and task identifiers belong in test names, task records, commits, and PR text.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree (`git diff $(git merge-base main HEAD)` plus untracked files from `git ls-files --others --exclude-standard`).

**Review-only requests:** when the user asked only for a review, run the auditor as an isolated agent in its own worktree (or a scratch copy), so its comment deletions land there and not in the user's tree. Run steps 1 and 2, then report accepted flags, rejected flags, the auditor's deletion diff as a proposal, and constraint candidates. Do not delete comments or edit code in the user's tree. Steps 3 to 5 need authorization to change the scoped files.

## Steps

1. **Spawn the auditor.** Spawn one fresh agent per [harness adapters](../../multi-agent-delivery/references/harness-adapters.md). Pass the scope and the auditor brief below, verbatim. Pick the agent's reasoning level and speed for the job. Do not add your own reasons for any comment. When agent spawning is not available, run the auditor brief yourself in a separate pass and record "Independent agent not available; sequential self-review, same context. Independent comment audit not achieved."
2. **Audit the auditor.** Inspect its report and diff.
   - Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty.
   - Reshape flags on our-code surprises stay actionable. Do not restore those comments.
   - A keep survives only with proof it is about something we cannot change.
   - Audit missed scoped lint and type-checker suppressions (`eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `# noqa`, `# type: ignore`, `@SuppressWarnings`, and similar). Correctness or safety suppressions stay actionable `MUST KILL`s.
   - Restore deletions only with exact exceptions and scoped proof.
   - Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, run the how-it-works or why-it-is-this-way investigation from [codebase-investigation](../../codebase-investigation/SKILL.md) on their symbol.
   - If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it.
   - Revert and rerun one rejected report with the failure named. Reject a second, report it open, and fail the comment audit.
3. **Fix trivial accepted flags directly** by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, produce one design sketch for the accepted set and surrounding code (use the design method in [technical-design](../../technical-design/SKILL.md)). Stop at the sketch. The sketch shapes. Step 4 implements.
4. **Implement the smallest root-cause fix in scope.** Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The [Fix Root Causes](../../engineering-principles/references/fix-root-causes.md) and [Redesign From First Principles](../../engineering-principles/references/redesign-from-first-principles.md) principles guide intent only. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards. Changes that alter behavior follow the test rules in [operating rule 5.2](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices) and [test-driven-development](../../test-driven-development/SKILL.md).
5. **Constraint comments** say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. For the rest, offer the cheapest in-scope type, runtime check, test, or CI lint that encodes the constraint. Wait for interactive approval. Unattended runs and evals require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. **Report** the deletion count, restored comments, reruns, design sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.

Verify per the [fix/verify loop](../SKILL.md#fixverify-loop): rerun the project's checks after deletions and fixes, and re-audit only the changed scope.

## Auditor brief

Paste this into the auditor's brief with the scope.

> You audit comments. Your input is the scoped files or diff given here. If none is given, use the current diff against `main`. Target narration, banners, commented-out code, and workaround justifications.
>
> Only these exceptions keep a comment:
>
> - Legal or license headers.
> - Non-obvious behavior forced by an external dependency, platform, vendor, or protocol we cannot reshape. Surprises in our own code do not qualify. Delete them and mark the exact symbol `MUST KILL` for rename, extract, type, or rearchitecture that makes the behavior obvious without prose.
> - `// prettier-ignore` (and equivalent formatter directives). Lint suppressions survive only when their rule is faulty, pedantic, or style-only.
> - Doc comments that define a public API contract.
> - Issue or RFC links that explain a constraint code cannot express.
>
> That list is the only leash. When you are not sure a keep clause applies, the comment goes. Everything else goes.
>
> `eslint-disable`, `@ts-ignore`, `@ts-expect-error`, and similar suppressions are suspect. Look up the rule. If it catches real bugs or protects correctness or safety, delete the suppression and mark the exact guilty symbol `MUST KILL`.
>
> `IMPORTANT`, `do not remove`, `too risky`, `fine for now`, and long justifications are signals, not proof. Before judging, read nearby code. If its claim is not obvious there, trace the named symbol or call: what it does and why it is that way (callers, history, blame, linked issues). Only a foreign keep-list gotcha proven true today on a live path keeps its comment. Our-code surprises go, with the reshape flag above. Doubt after the investigation means delete.
>
> A long justification without a proven keep-list exception is a confession that the code is wrong. Delete it. Never polish it into a shorter justification. Mark the exact guilty symbol `MUST KILL`. Your work on that symbol ends there. Do not touch the code.
>
> Every flag names code inside the scope and tells the truth. Invent nothing. You touch comments and identify refactor targets. You never write application code. Do not invoke other skills or spawn additional agents.
>
> Report only. Name touched files, deletion count, `MUST KILL` flags with one line each, and skips.
