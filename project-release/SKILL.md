---
name: project-release
description: Prepare and execute production releases, pilot rollouts, and business cutovers; verify critical operations after release and handle code rollback and data recovery when a release fails. Use for projects that have completed staging acceptance and are preparing for production, or need executable release and recovery procedures.
---

# Production Release and Cutover

Deliver the accepted version for production use through the project's actual release process, leaving a release record and an executable recovery plan.

## 1. Establish the Current and Target States

Read the project before asking questions.

- Read the task list, technical plan, customer acceptance records, and remaining issues. Read the data model, interface contracts, and critical business scenarios as needed.
- Inspect project documentation, example environment configuration, deployment configuration, and continuous integration workflows to identify the actual release, migration, backup, and recovery entry points. Read only necessary configuration and do not expose secrets in output.
- For a migration or cutover, identify the current state, target state, and irreversible actions between them.
- Identify the release version or build artifact, production environment, release time, executor, incident owner, and scope of authorized operations.

Check whether acceptance evidence applies to this version. A checked checklist does not establish implementation completion, customer acceptance, or release authorization. List missing release prerequisites separately; block only operations that depend on them.

Done when: you can clearly state which version, business operations, and data will move from which state to which target state. Required prerequisites and authorization have evidence or are explicitly marked as pending.

## 2. Prepare Executable Release Steps

List the steps in dependency order and the result each produces. For every step, specify the actual command or operational entry point, target environment, executor, expected result, and response to failure.

Identify steps that require a human and values that must be obtained along the way. For each value, specify where it comes from, where it is written, and whether it is secret. Delegate only operations that a human must perform; directly execute operations supported by available permissions and tools.

For manual steps, give the precise path: which page to open, what action to take, and where to obtain the required value. If the current interface or exact command is unknown, check the documentation or ask rather than inventing steps.

Include what the actual project requires:

- Checks of production accounts, role permissions, baseline data, and production configuration.
- A pre-release backup, database changes, and data import.
- Application deployment, switching business entry points, and checks that must run immediately after release.
- Pilot departments, users, or business scope; the observation period; and conditions for expanding usage.

When handing over between old and new systems, specify when writes to the old system stop, how the final incremental changes are handled, and when writes to the new system begin. Concurrent writes must follow an existing, verified synchronization plan.

Carry forward existing authorization. Seek additional confirmation before an operation only when its release target, data impact, or irreversible actions exceed that authorization. If the request is only to prepare a plan, complete it and mark it as awaiting execution.

Done when: every step has concrete instructions an unfamiliar executor can follow, with clear dependencies, checkpoints, and stopping conditions.

## 3. Prepare Backup and Recovery

Document code rollback and data recovery separately. Redeploying an older version is not a substitute for a data recovery plan.

- **Code rollback:** Specify the rollback version, execution entry point, configuration restoration, and steps for routing traffic back. Check whether the old code is compatible with the changed database.
- **Data recovery:** Specify the recovery point, backup location, recovery target, actual recovery commands, and verification method. Explain potential data loss and how data added after release will be preserved, re-entered, or reconciled.
- **Recovery decisions:** Specify when to stop the release, when to roll back or recover, who decides, and what to check after recovery.

Verify that the pre-release backup actually completed and inspect rehearsal evidence applicable to the current recovery method. A file's existence alone does not prove recoverability. If recovery evidence is missing, mark it as unverified and complete the necessary checks in an isolated environment before making production data changes that depend on it.

Confirm that ongoing backups are configured and running according to project requirements; record the most recent successful result and the owner. Before recovery overwrites production data, check that the target and data-loss impact fall within the authorized recovery scope.

Done when: code rollback and data recovery both have concrete steps, applicability conditions, and verification evidence. Any operation that cannot be recovered has an explicit impact assessment and disposition.

## 4. Execute the Release and Cutover

Execute phase by phase, completing the current phase before moving to the next. Respect dependencies and verify results at each checkpoint.

- Recheck the target environment, current version, and release artifact before execution.
- Apply only changes needed for this release. Confirm completed steps from actual state without repeating their side effects.
- Every state-changing operation must answer: What happens if this runs twice? What happens if the previous run stopped halfway?
- Derive the next step from existing state: read the current state, compare it with the target, and apply only the difference. For steps that cannot safely repeat, determine what has already completed before choosing to resume or recover.
- Update the existing release record after each step. If a sequential step fails, stop subsequent dependent steps, preserve the error and incident context, and follow the recovery plan.

When a command times out or a connection drops, inspect the actual server-side result first. Do not treat an unknown outcome as failure and immediately rerun the operation. When an agreed stopping or recovery condition is met, stop expanding the impact. Follow the authorized plan and refer recovery operations outside its scope to the responsible decision-maker.

Done when: executed steps and results can be checked; failed or unexecuted steps retain their true status; and the current production version, data state, and business entry points are clear.

## 5. Verify Real Usage and Decide Whether to Expand

Test through real interfaces and verify behavior users care about. Check what happens rather than how it is implemented internally. Expected results must come from confirmed business rules or independent examples, not from repeating the implementation's calculations.

Check the real thing directly: read actual results and check whether services are running. Do not infer success from cached screenshots, indirect state, or successful compilation. When a check can be repeated with a deterministic script, run it and retain the results.

- Check the version actually served at the production entry point and run the critical post-release scenarios.
- Have pilot users perform critical operations with production permissions on real devices and networks, confirming results through normal business interfaces or APIs. Verification that produces real business side effects must stay within the authorized scope.
- If data is imported or cut over, reconcile record counts, amounts, and relationships within the agreed scope. Stop expanding usage that depends on this data if unexplained discrepancies appear.
- Check business failures, errors, and operational metrics over the agreed observation period. Expand in batches only after pilot success criteria are met and expansion is authorized. Check that existing business operations remain usable in each batch.

Each increment should add value without breaking existing business operations. Stop at any checkpoint to validate the current scope independently.

Without evidence from real users, record: "Technical checks complete; real usage awaiting confirmation." If only the pilot is complete, record the actual coverage. If you cannot continue observing, assign the remaining checks to an explicit owner rather than claiming the observation period is complete.

## 6. Deliver and Close

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Update the existing project status entry point and deliver:

- **Production system:** The actual running version, entry points, and enabled scope.
- **Release record:** Execution times, executors, completed steps, verification evidence, failures and their disposition, and remaining items.
- **Executable recovery plan:** Entry points, applicability conditions, owners, and verification status for code rollback and data recovery.

Done when: within the agreed rollout scope, customers can complete critical operations on real devices and networks; release checks pass; blockers for the agreed release scope are resolved and any non-blocking limitations have been explicitly accepted by an authorized owner with their impact and follow-up arrangements recorded; and the team knows who handles incidents and how to recover.

Record "plan prepared," "technical release complete," "pilot passed," and "production cutover complete" separately. A successful rollback must be recorded as "release failed; service restored," not as a successful release. Hand future maintenance items to an owner rather than using them to extend this release task indefinitely.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## PR and release boundary

Use [PR delivery](../pr-delivery/SKILL.md) for preparing, opening, babysitting and landing an authorized pull request or stack. A merged PR, green CI or passing independent verification is not production-release authorization. Keep the release target, approved candidate, rollout, rollback, environment checks and customer acceptance states in the existing release record under [operating rules](../ask-eric/references/operating-rules.md). Use [bug diagnosis](../bug-diagnosis/SKILL.md) for rollback or incident diagnosis when the authorized response plan requires it.
