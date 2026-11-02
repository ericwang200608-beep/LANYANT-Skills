---
name: project-maintenance
description: Complete role-based training, administrator and resource handover, monitoring, and maintenance arrangements for a live system, and triage subsequent incidents and enhancement requests. Use for pre-launch training and operations handover preparation, verifying handover, establishing ongoing maintenance, or handling post-launch support under existing arrangements.
---

# Training, Handover, Monitoring, and Ongoing Maintenance

Enable customers to keep using the system, administrators to manage it, someone to take ownership of incidents, and subsequent requirements to have a clear place to be recorded.

## 1. Read the Current State and Handover Evidence

Read confirmed requirements, user scenarios, customer acceptance records, release records, recovery plans, and remaining issues. Inspect existing user instructions, operations documentation, the issue tracker, and monitoring configuration. Prefer updating existing material.

Do not duplicate content already captured in requirements, plans, decision records, issues, or commits; reference it by path or link. Remove secrets, passwords, and unnecessary personal information from handover materials. Transfer access credentials through the agreed secure channel.

Establish whether this task is to prepare handover, verify its results, or handle a specific maintenance item. Execute only relevant steps and carry forward existing authorization and maintenance agreements. For production changes, resource transfers, or external notifications, check that the action is within the authorized scope.

Done when: the current version, completed work, remaining work, and authoritative records are clear. Missing information is listed, and unknown states are not recorded as complete.

## 2. Write Role-Based Instructions and Provide Training

Organize instructions around user journeys, ordered by importance. Describe each journey in plain language, how it can be verified independently, and the value it delivers.

Write executable scenarios for each role and for administrators that demonstrate operations working end to end. Include prerequisites, preparation, entry points, steps, and expected outcomes. Reference existing business rules and data documentation rather than copying implementation code or full test suites.

Reuse the established scenario identifiers and business outcomes, adding role-specific instructions. Training evidence records whether people can use the system; it does not replace technical acceptance results.

Describe critical operations as: **Given an initial state, when an action is performed, then what result should occur?** Include the exception handling and help channels actually needed.

- Role instructions cover critical daily work, permission limits, common errors, and how to correct them.
- Administrator instructions cover the account and permission management, basic configuration, and routine administration the project actually supports.
- Have actual role holders and administrators perform representative operations using the instructions. Record successes, failures, and unverified items. Training may begin before launch; exercises with real business side effects must use the agreed environment and data.

Done when: people in the target roles can follow the instructions to complete critical work, and administrators can perform the agreed management operations. If only documentation or demonstrations exist and users have not tried the operations, record: "Materials complete; training effectiveness awaiting verification."

## 3. Hand Over Resources and Maintenance Responsibilities

Check actual resources such as accounts, domains, servers, databases, code, and deployment platforms. For each resource, record ownership, the management owner, recipient, access entry point, how permissions are obtained, and applicable renewal or expiration matters.

Verify that recipients can access and manage the required resources with the agreed permissions. Listing a resource or sending an invitation does not establish handover completion. Transfer ownership and revoke permissions according to the authorized plan.

The operations manual must reference the project's actual release, backup, recovery, logging, and monitoring entry points. Check the latest successful backup result, recovery rehearsal evidence, and owners. Explain code rollback and data recovery separately. Keep recovery methods that have not been rehearsed marked as unverified.

Document support channels, service hours, incident severity levels, initial response times, escalation paths, and primary and backup owners according to existing agreements. Mark unagreed times or responsibilities as awaiting confirmation; do not independently promise round-the-clock support or resolution deadlines. Record initial response and completed recovery separately.

Done when: resources have clear ownership and recipients, necessary access has been verified, and incident contacts, escalation paths, maintenance responsibilities, and response agreements are clear.

## 4. Verify Monitoring and Notification Paths

Read actual monitoring and backup configuration. Confirm signals required by the project, such as critical business availability, errors, performance, capacity, and backup failures. Every actionable alert must have a trigger condition, receiving channel, owner, and response entry point. Use existing project requirements or confirmed baselines for thresholds.

Within the authorized scope, use test events or safe checks to verify collection, alert delivery, and receipt. Do not cause production failures to prove that alerts work. Record "configured," "trigger verified," and "receipt confirmed" separately, leaving unverifiable stages explicitly open.

Ongoing monitoring must be performed by an actual platform, scheduled task, or responsible person. Without an operating mechanism and an owner, do not claim ongoing monitoring has begun. Preparing handover materials alone does not authorize sending notifications or creating scheduled tasks.

Done when: agreed critical monitoring and incident notification paths have verification evidence, ongoing execution mechanisms and owners are clear, and gaps have a disposition plan.

## 5. Triage Incidents and Enhancement Requests

Use the project's existing issue tracker and its labels and states. Distinguish two categories: **bug**, meaning behavior is broken, and **enhancement**, meaning a new feature or improvement.

Each issue must have one clear category and a current handling state, which can map to needs triage, needs information, ready for implementation, requires human handling, or will not be actioned. If states conflict, clarify the current decision first.

### Gather Context and Verify

1. Read the full issue, comments, and prior handling notes. Do not repeat resolved questions. Read domain terminology and relevant technical decisions as needed.
2. Search existing implementations by business concept, not only the request's wording. Also check duplicate issues and previous rejection or deferral decisions.
3. Verify whether the report holds up. Reproduce bugs using the reported steps and record "confirmed," "not reproduced," or "insufficient information," with actual observations. For bug diagnosis or performance regressions, read the [Incident Diagnosis Appendix](references/incident-diagnosis.md).
4. Explain the recommended category, state, and priority with reasoning. Carry forward existing triage authority. Refer a decision to the owner only when it affects business scope, priority commitments, or rejection and the necessary authorization is missing.

Failure to reproduce does not mean there is no bug. Notes requesting more information must contain "established facts" and "information still needed," with specific, actionable questions. Re-evaluate when new information arrives rather than restarting the investigation.

For incidents affecting production use, first contain the impact under the authorized response plan and escalate to the owner, then perform deeper diagnosis. Reproduction and stress experiments must not obstruct necessary recovery.

### Prepare Work Someone Can Take Over

For items ready for implementation, specify the category, a one-line summary, current behavior, desired behavior, key interfaces, and concrete, testable acceptance criteria. State which adjacent requests this item does not address.

Describe what the system should do rather than prescribing implementation steps. Express work through interfaces, types, and behavioral contracts. Avoid relying on line numbers or the current file structure, which may become stale. Each acceptance criterion must be independently verifiable.

When human handling is needed, explain why, such as business judgment, external access, or manual verification. Link already-implemented requests to the existing capability and its usage instructions. Preserve decisions and reasons for rejected or deferred requests. Publish external comments, close issues, or notify customers only within explicitly authorized scope.

New requirements enter the backlog and the next round of prioritization first; recording them does not promise implementation in this round. For fixed items, record implementation verification, target-environment verification, and user confirmation separately. None substitutes for the others.

When a confirmed business rule changes, update the authoritative specification within authorization and assess affected design, tasks, tests, user instructions, and acceptance evidence. Record what remains applicable and what must be revalidated; reopen only affected work. If upstream edits are outside scope, record the exact required updates and their owner rather than silently treating stale artifacts as current.

## 6. Assess Business Outcomes and Conduct Necessary Retrospectives

Use the originally confirmed success criteria. Criteria must be measurable and independent of the technical implementation, such as task completion time, first-attempt success rate, or reduction in related support requests. Do not treat example values as project targets.

Record metric definitions, pre-launch baselines, observation periods, data sources, and owners. Compare actual results with targets. If baselines, data, or observation time are missing, mark the outcome as awaiting assessment and arrange follow-up checks rather than inferring success.

Only when actual maintenance records reveal development or troubleshooting process problems, or the user requests a retrospective, inspect the primary records and propose improvements in severity order:

- **Navigation:** Did finding information take a long time? Are clearer documentation entry points needed?
- **Automated checks:** Could existing checks have caught the error? Read the project's own check commands and continuous integration configuration first. An existing check that is not connected or silently fails is itself the finding; do not reinvent it.
- **Rules:** Prefer deterministic checks for mechanical rules such as fixed syntax, banned interfaces, or file locations. Reserve review instructions for conventions that require judgment.
- **Information access:** Did missing logs or necessary read-only access prevent a conclusion?
- **Tools and instructions:** Were operations expensive and inefficient, or were instructions redundant without changing behavior?

Associate each improvement with actual evidence and expected benefit, and add it to the existing improvement list. Do not turn every incident into a new general rule.

## 7. Deliver and Close

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Update the existing project status entry point and deliver or link:

- **User manual:** Role-based instructions, training results, and common questions.
- **Operations manual:** Administrator operations, resource inventory, backup and recovery, monitoring, and incident handling entry points.
- **Maintenance responsibilities:** Support channels, owners, service hours, response agreements, and escalation arrangements.
- **Follow-up improvement list:** Remaining bugs, new requirements, business outcome checks, and necessary process improvements, with status, owners, and acceptance criteria.

Done when: customers can use the system, administrators can manage it, resources and maintenance responsibilities have been handed over, someone takes ownership of incidents, and subsequent requirements have a place to be recorded. Keep unfinished hands-on training, access verification, or notification verification explicit; do not claim the entire handover is complete.

After this handover, assign ongoing monitoring, maintenance, and business outcome tracking to the agreed mechanisms and owners. When handling a single maintenance item, finish against that item's acceptance criteria rather than interpreting ongoing maintenance as an indefinitely running task.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Detailed maintenance routes

Use [issue triage](../issue-triage/SKILL.md) for incoming reports and enhancements, [bug diagnosis](../bug-diagnosis/SKILL.md) for reproduction and root cause, and its production-incident branch for containment, recovery validation, evidence preservation, diagnosis and prevention. Use [performance investigation](../performance-investigation/SKILL.md) for measured regressions, [refactoring](../refactoring/SKILL.md) for a behavior-preserving change, [process improvement](../process-improvement/SKILL.md) for evidence-backed process lessons, and [delivery planning](../delivery-planning/SKILL.md) to turn accepted work into ready tickets. A standalone maintenance item closes against its own acceptance criteria; ongoing ownership does not keep the current task open indefinitely.
