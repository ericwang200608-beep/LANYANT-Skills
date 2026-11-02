---
name: delivery-proof
description: Verify delivery in a staging environment using customer data and actual role-based workflows, rehearse historical data imports when needed, reconcile data, and record customer acceptance and remaining issues. Use for data rehearsals and business acceptance before production cutover; this does not replace production release authorization.
---

# Staging, Data Import Rehearsal, and Customer Acceptance

Verify behavior users care about through real entry points, and inspect actual results directly. Deliver a data reconciliation report, customer acceptance records, and a remaining-issues list, distinguishing technical verification from customer confirmation.

## 1. Establish the acceptance basis

Read confirmed requirements, user stories, acceptance criteria, technical plans, data models, and test and review results for the current candidate. Use project business terminology and confirmed decisions. Do not redefine acceptance requirements to match the current implementation.

Confirm the version, staging entry point, data scope, participating roles, and people responsible for confirmation. Read the project's actual startup, migration, import, and verification scripts. Use commands appropriate to installed tool versions rather than inferring script behavior from names.

Check the separation between staging and production, and the availability of test accounts and data. Establish the disposition of known issues affecting this acceptance round. Mark scenarios with missing prerequisites as pending execution; prepared documentation does not substitute for actual acceptance.

Use customer-provided data within authorization. Redact sensitive material and restrict access according to project requirements. Staging operations should not trigger real payments, notifications, or other production business side effects. Any genuine need for those requires corresponding authorization.

## 2. Prepare executable acceptance scenarios

Organize user journeys by importance. Each journey should be independently demonstrable or verifiable and produce a meaningful business outcome.

For each scenario, include:

- The corresponding requirement or acceptance criterion.
- The executing role, prerequisites, and data used.
- "Given an initial state, When an action is performed, Then the expected outcome occurs."
- Actual steps, expected results, and where results will be recorded.

Cover normal flows and relevant boundary and exception cases. Expected results must come from independent evidence, such as the requirements specification, reconciled customer documents, or worked examples, rather than duplicating the implementation algorithm and comparing it with itself.

Validation instructions include prerequisites, preparation, execution steps, and expected outcomes. Reference existing interfaces, data models, and test materials rather than maintaining duplicate content.

Reuse existing acceptance scenario identifiers and authoritative definitions. Add customer roles, rehearsal data, and acceptance observations to those scenarios rather than rewriting a parallel set of expected behaviors.

Focus on what users can accomplish. Do not ask customers to inspect private methods or internal call counts. Give each scenario clear business judgment criteria instead of undefined terms such as "normal," "fast," or "accurate."

## 3. Prepare staging and rehearse imports when needed

Prepare the candidate version in staging within authorization, recording the actual version and environment. After startup, directly check the application entry point and necessary connections rather than relying only on successful build or deployment commands.

When historical data import is involved, read [Data Import Rehearsal and Reconciliation](references/data-rehearsal.md). Complete field mapping, data-quality handling, trial import, reconciliation, and recovery verification before customers use those data for acceptance.

If there is no historical import, explicitly record it as not applicable and use customer examples or test data suitable for the scenarios. Do not create migration work merely to complete a process.

## 4. Run verification and arrange customer trials

Run repeatable technical checks first. Then have actual staff complete their work in staging using their own test accounts. For example, a requester creates a purchase request, a supervisor approves it, and warehouse staff record receipt.

Check business behavior through real pages, interfaces, and necessary system integrations. Internal implementation may change as long as public behavior still meets requirements. Successful mocked internal calls do not substitute for a successful real workflow.

Read actual state and values directly rather than inferring results from file timestamps, cached screenshots, completion claims, or compilation. For critical outcomes such as persistence, quantities, and amounts, inspect actual records and subsequent reads. Record the evidence for technical reconciliation queries and customer actions separately.

Preserve repeatable automated checks as existing project commands or simple scripts, and actually run them. Record execution conditions and results for others to recheck. If real integrations or devices cannot be used, state what was simulated and what remains unverified.

During customer trials, record actual actions, observations, and feedback. An agent completing a workflow is technical verification, not customer approval. Without actual customer feedback, retain the status "Awaiting customer acceptance."

Send invitations, messages, or acceptance materials to customers only within existing explicit authorization to send. Otherwise, prepare the materials and outstanding questions without sending them.

## 5. Address gaps and reverify

Compare actual results with requirements item by item. Distinguish missing requirements, partial completion, behavior contradicting requirements, and new requirements outside this round. Reference acceptance criteria and actual evidence for each issue, explaining its effect on use.

Record actionable remaining work in the project's existing issue or task location. Reference an existing issue when it already covers the matter, avoiding duplicates. Do not modify expected results, hide failures, or automatically relax business rules to make acceptance pass.

When fixes are authorized, reverify affected scenarios after fixing them. When only acceptance work is requested, deliver findings without independently modifying the application. If the candidate version or imported data changes, state which evidence remains applicable and what needs to be rerun.

For decisions in which customers change rules or accept known limitations, record who confirmed them, when, and their explicit position. Keep the decision pending until confirmation arrives. Record new requirements separately without automatically expanding the acceptance scope.

When a confirmed business rule changes, update the authoritative specification within authorization and assess affected design, tasks, tests, user instructions, and acceptance evidence. Record what remains applicable and what must be revalidated; reopen only affected work. If upstream edits are outside scope, record the exact required updates and their owner rather than silently treating stale artifacts as current.

## 6. Deliver acceptance evidence

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Save results according to existing project documentation conventions, keeping the content together:

1. **Data reconciliation report:** Data sources and batches, mapping basis, import and reconciliation results, discrepancies, and their disposition. State not applicable if there was no import.
2. **Customer acceptance record:** Candidate version, environment, participants, scenarios, expected and actual outcomes, evidence, and the customer's explicit position.
3. **Remaining-issues list:** Impact, ownership, handling arrangements, and whether each issue blocks this acceptance round.

Every important acceptance criterion should have a passed, failed, or unverified result. Record technical results separately from customer confirmation. If a customer explicitly accepts a limitation, retain the limitation and original failure facts rather than rewriting the failure as a technical pass.

This stage is complete when customers confirm that key workflows meet their needs, data reconciliation holds, and blockers for this acceptance scope are resolved. Non-blocking limitations may remain only when an authorized owner explicitly accepts their impact and records follow-up arrangements. Acceptance of a limitation does not turn a failed technical check into a pass or grant release authorization. If customers have not participated, critical data do not reconcile, or blockers remain, accurately report the corresponding portions as pending.

Do not repeat completed technical preparation merely while waiting for customers; retain business acceptance as pending. Completing this stage does not authorize production cutover. Release and production data import require their own applicable authorization, including authorization already given.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Detailed verification and evidence routes

Use [code review](../code-review/SKILL.md), [adversarial review](../adversarial-review/SKILL.md), and [verification harness](../verification-harness/SKILL.md) for their respective independent checks. Use [bug diagnosis](../bug-diagnosis/SKILL.md) for a failed proof, [performance investigation](../performance-investigation/SKILL.md) for a performance claim, and [PR delivery](../pr-delivery/SKILL.md) for current-head CI evidence. Evidence identifies the version, environment, actual run and its limits. Keep implementation completion, technical verification, customer acceptance and release authorization separate under [operating rules](../ask-eric/references/operating-rules.md).
