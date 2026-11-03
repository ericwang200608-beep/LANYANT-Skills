---
name: system-verification
description: Independently review implementation against engineering standards and business requirements, identify gaps against requirements, technical plans, and tasks, and execute key system scenarios to produce verification evidence. Use for post-development code review, delivery-batch verification, and rechecking fixes.
---

# Independent Review and System Verification

Answer two questions separately: does the code follow project standards, and does it implement the requirements? Then directly verify system behavior so each important acceptance criterion has a corresponding result. Passing one axis must not hide failure on the other.

## 1. Pin the review target

Establish the feature, delivery batch, and candidate version for this review. Distinguish change review from current-implementation assessment: the former examines changes against a baseline, while the latter checks whether current code satisfies this iteration's requirements, beyond the diff alone.

When the user supplies a commit, branch, or tag as the baseline, verify that it resolves. For branch reviews, compare against the common ancestor with the baseline, for example `git diff <base>...HEAD`, and record the relevant commits. If the user requests an exact comparison of two commits, compare the endpoints rather than substituting a merge-base comparison.

When reviewing the working tree, explicitly include staged, unstaged, and untracked files; these do not automatically appear in a branch diff. If no valid baseline is known, first look in task or PR context, then ask if it remains unresolved. If the diff is empty, report that no changes were found for review rather than treating it as proof that the system is verified.

Record the candidate version and verification environment. If fixes change the candidate, update the current version record rather than directly counting old results as passes for the new version.

## 2. Locate requirements and standards

Read user-specified requirements or issues. Otherwise, inspect issues referenced in commits and project requirements matching the feature. Read the full requirements and relevant decisions; do not substitute the developer's completion summary for them.

Load the relevant technical plan, data model, tasks, and project principles. These materials define scope; do not independently expand it to the entire codebase.

Find repository files documenting how code should be written. Include `CODING_STANDARDS.md` and `CONTRIBUTING.md` when present. Use project terminology and architectural decisions.

If requirements are unavailable, explicitly report: "No requirements available; requirements-conformance review was not completed." If plans or tasks are missing, explain which completeness judgments cannot be made. Perform supported standards checks and verification where possible, but do not report full convergence.

## 3. Run the two review axes separately

When independent agents or contexts are available and authorized, assign each axis to a fresh context so their conclusions do not influence each other. Supply original requirements, candidate code, comparison instructions, and standards. Follow the [independent input-packet procedure](../standards-spec-review/SKILL.md#prepare-an-independent-input-packet): withhold author diagnosis, repair and pass narratives even when they appear in the task/status diff. Pass only original task definitions from mixed records. Give explicit reviewed and withheld paths and a filtered diff; do not expose an unrestricted diff or completion record to the independent reviewers. After their findings are recorded, separately audit withheld records against real evidence so those changes remain reviewed. Reading conclusions and merely promising not to trust them does not preserve independence. If those tools are unavailable, perform the checks separately and state that independent-context review was not obtained.

### Engineering standards

Check whether the diff violates documented repository standards. For every finding, cite the specific rule and code location, distinguishing explicit violations from judgment-based improvement suggestions.

Read [Code Structure Review Guidelines](references/code-quality.md) and use its signals to guide judgment. Explicit repository standards override these heuristics. Do not flag a permitted project pattern merely because of a general preference. Reuse tool-enforced check results instead of creating duplicate manual style findings.

### Requirements conformance

Check for:

- Required functionality that is missing or only partly implemented.
- Behavior added beyond the requirements.
- Requirements that appear implemented but are implemented incorrectly.

Cite the corresponding requirement and code evidence for each finding. A checked task alone does not establish that its behavior is implemented.

Keep the two reports separate. Clean up wording if useful, but do not merge them into one ranking or offset problems on one axis with a pass on the other. Report finding counts and the most important issue within each axis separately.

## 4. Assess gaps in the current implementation

Use requirements, plans, tasks, and confirmed changes as the source of intent, with project principles as constraints. Check every currently applicable task, regardless of checkbox state. For chains of fixes, assess the final required behavior rather than demanding preservation of superseded implementation details.

Map functional requirements, acceptance scenarios, success criteria requiring engineering work, and plan decisions to the implementation. Reuse existing identifiers such as `FR-003` or `US1/AC2`. Do not treat post-launch business metrics as outcomes already proven by code.

Record findings only where gaps exist, classified as:

- **Missing:** Required work is entirely absent.
- **Partial:** Implementation exists but does not fully satisfy the requirement.
- **Contradicts:** Code behavior conflicts with confirmed intent or a mandatory principle.
- **Unrequested:** Implementation falls outside requirements, plans, or tasks and needs its justification assessed; do not delete it automatically.

Each finding includes a stable identifier, requirement reference, gap type, severity, evidence location, and remaining work. Assign severity by impact:

- **Critical:** Violates a mandatory project principle or blocks basic functionality of a highest-priority story.
- **High:** Core functionality or acceptance criteria are missing or incomplete.
- **Medium:** Secondary requirements are partly unmet, or added scope has unclear justification.
- **Low:** Minor gaps or low-risk additional implementation.

When little code exists, accurately list the unimplemented scope. When everything is satisfied, do not add tasks merely to produce findings.

## 5. Execute system verification directly

Run important acceptance scenarios for this iteration in an appropriate test environment. Inspect actual results rather than inferring usability from compilation, completion claims, or updated screenshots.

Based on the requirements, focus on:

- Whether normal business workflows complete through actual pages or interfaces.
- Whether authorization denials, invalid inputs, and relevant exceptions are handled according to the rules.
- Whether data is actually persisted and remains correct when read later or after reopening a page.
- Whether connected modules work together, distinguishing real integrations from simulated portions.
- Whether measured duration of key operations meets established targets. Without an explicit target, provide measurement conditions and results rather than independently declaring a pass.
- Whether existing behavior affected by the change still holds.

Reuse project tests, browser tools, and continuous integration tooling. Preserve recurring critical paths as repeatable checks where useful, with isolated test data and state. Record commands or actions, environment, expected outcomes, and observed results. Reference existing evidence directly when it still applies to the current candidate.

If execution is unavailable, accounts are missing, or the environment is unsuitable, mark items "unverified" and explain their impact. Missing evidence does not itself prove missing implementation, and does not justify assuming a pass.

## 6. Record remaining work and reverify fixes

First present evidence-backed findings. Keep the basis for standards issues, requirements gaps, and runtime failures distinct. Link findings that share a root cause to avoid duplicate remediation tasks.

With read-only review authorization, report results in the conversation without modifying files. When task-record updates are within authorized scope, append actionable remaining work to the existing task list, referencing finding and requirement identifiers and prioritizing critical and high-impact issues.

Use new, unused identifiers for appended tasks. Preserve task identifiers and historical evidence. Update affected current statuses, acceptance descriptions, and wording superseded by confirmed decisions within authorization; do not delete or reorder unrelated tasks. A finding against a completed task must update its current status or link it to the remaining work so the summary is not misleading. Reference an existing open task if it already covers the same problem instead of appending a duplicate. If no new work remains, add no empty section or duplicate task; update stale current status only when necessary and authorized.

Review and task supplementation do not themselves modify requirements, plans, or application code. When fixes are explicitly authorized, perform them within that scope and record the corresponding findings and verification results. Otherwise, deliver the list of work awaiting fixes.

After fixes, check that the original findings are resolved and rerun affected scenarios and necessary regression checks. Broaden review only for new changes, failures, or concrete risks, reusing evidence that remains applicable. Preserve the original failure facts and update the current conclusion in the existing task entry point.

## 7. Deliver and finish

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Deliver the findings list, records of fixes actually performed, and verification evidence. If no fixes were executed, clearly mark them as pending rather than inventing fix records.

Include:

- Review scope, candidate version, and independent-review method.
- Separate conclusions for engineering standards and requirements conformance.
- Passed, failed, or unverified results for important acceptance criteria.
- Remaining issues, task references, and their impact on this iteration's conclusion.

When there are no actionable gaps, report no remaining implementation work found within the checked scope. Report this iteration's technical verification as passed only when necessary verification also passes. A clean static review does not substitute for runtime evidence.

A read-only review ends with delivery of its results. Work that includes fixes ends when the agreed issues are handled and necessary rechecks pass. Unverified items block this iteration's conclusion only if they affect its acceptance criteria. Track target-environment validation, customer acceptance, and release authorization separately.

Stop when this iteration's completion conditions are met. Do not repeatedly reopen review for optional optimization or automatically create PRs, merge, or publish.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Review and convergence branches

Use [code review](../standards-spec-review/SKILL.md) for independent standards/specification review, [adversarial review](../adversarial-review/SKILL.md) for concrete risk challenges, and [verification harness](../verification-harness/SKILL.md) when building or maintaining repeatable or formal proofs. Reuse existing check commands and evidence that still apply. Same-family independent contexts must be labeled as such.

After implementation, run [the complete convergence assessment](references/converge.md) against the authoritative spec, plan, tasks and governing principles. It assesses current implementation, not merely the diff. Keep all existing task bytes unchanged. Use `python3 <this-skill>/scripts/append_convergence.py <tasks.md> <findings.json> --dry-run` to preview severity-ordered, traceable tasks, then append within scope. No findings means no write and no empty phase header. This helper never edits the specification or plan and never marks implementation complete. The append helper requires Python 3 on a POSIX system (macOS or Unix) for file locking; Windows execution is unverified. If tasks change concurrently, it reports a conflict without restoring an old snapshot or deleting current bytes.
