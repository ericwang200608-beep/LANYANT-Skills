---
name: business-discovery
description: Turn customer ideas and existing materials into project scope, current workflows, and formal business requirements through interviews, domain modeling, and specification clarification. Use to define business requirements and update specifications. The scope ends at the requirements phase.
---

# Business Discovery

Focus on what users need and why. Write for business stakeholders, without discussing technology stacks, interface implementation, or code structure. Read and follow existing project principles when available.

For a new project without recorded principles, capture only the necessary confirmed business constraints and quality requirements in the existing specification. Leave technical enforcement choices to design; do not create an empty principles document or invent commitments.

## 1. Confirm Project Scope and Acceptance Criteria

### Interview

Keep questioning until you reach a shared understanding. Organize the discussion as a decision tree: each decision leads to subsequent decisions that depend on it.

Work in rounds. In each round, identify the questions whose prerequisites are settled and that can be answered now. Number them and provide recommended answers, then wait for the user's responses. Make it possible for the user to accept a clear recommendation by saying "yes."

Each round of answers reshapes the decision tree. Reassess which questions can be asked next. Questions that depend on unanswered questions in the current round belong in a later round.

Finding facts is your job. Investigate anything that can be established from materials, files, or existing systems rather than asking the user to look it up. While a fact remains unknown, defer only questions that depend on it and continue with the others. Leave decisions to the user.

End the interview when the relevant decision branches have been discussed and no assumptions have silently been treated as facts. Have the user confirm that you have reached a shared understanding before proceeding on that basis.

### Scope Statement

Organize the following from meeting notes, conversations, and requirement lists:

- Who will use the system and what actual problems it should solve.
- What the first release includes and what will come later.
- What remains unclear.
- Who confirms requirements and who is responsible for acceptance.
- Delivery milestones and how subsequent new requirements will be handled.

Have the user confirm business scope, priorities, and customer commitments.

**Deliverables:** Project scope statement, open questions, and initial acceptance criteria.

**Completion criterion:** The user and customer can explain in a few sentences what the first release will enable which people to accomplish.

### When Someone Else Needs to Answer

Turn matters the user cannot answer alone into a questionnaire for one relevant person to complete asynchronously or together during a meeting.

First establish who will receive it: their role, expertise, and relationship to the user. Then establish which facts or decisions are needed back. Use information already known.

Write questions around information the respondent has that the user lacks. Put important questions first. Each question should ask one thing and provide a space for an answer. Add a sentence explaining why it matters when needed.

Include the purpose, respondent, intended use of answers, brief context, answering instructions, questions grouped by topic, and "What else have we not asked?" Allow partial answers and "I don't know." Include deadlines and estimated effort when agreed. Deliver the questionnaire as a draft.

## 2. Understand Existing Workflows, Data, and Business Concepts

### Build and Clarify the Domain Model

Actively challenge unclear terminology, test concepts with edge-case scenarios, and record terms and decisions as soon as conclusions emerge.

- **Check terminology conflicts.** When the user's wording conflicts with the existing glossary, point it out immediately: "The glossary defines 'cancellation' as X, but you seem to mean Y. Which meaning applies here?"
- **Sharpen vague language.** Propose precise names for ambiguous or overloaded terms: "By 'account,' do you mean the customer or the system user? Those are different concepts."
- **Discuss concrete scenarios.** When discussing object relationships, test understanding with specific edge cases to clarify the boundaries between concepts.
- **Cross-check existing behavior.** When relevant code or system documentation exists, check whether it agrees with the business description. Surface contradictions: "The existing system cancels entire orders, but you said partial cancellation is possible. Which rule should apply?"
- **Update terminology promptly.** Record a term in the glossary as soon as it is resolved rather than batching updates at the end. The glossary explains business language only; it does not store implementation details, draft requirements, or implementation decisions.

Reuse the existing glossary. If the project has a `GLOSSARY-MAP.md`, follow its mappings to the relevant business context. If no glossary exists, create `GLOSSARY.md` when the first term is resolved.

Suggest a separate decision record only when all of these apply: the decision is hard to reverse; a future reader would be confused without its context; and alternatives were genuinely compared and a tradeoff made. Otherwise, skip it.

### Examine Real Materials

Where possible, inspect the customer's actual Excel sheets, orders, quotations, production documents, receipt documents, and legacy system screens. Establish:

- Where a document originates, who handles it, and what outcome it produces.
- Who enters, modifies, and confirms data.
- What fields mean, which information is duplicated, and which rules conflict.
- Whether integration is needed with other systems, scanners, printers, or messaging platforms.
- Whether historical data needs to be imported.

**Deliverables:** Current workflow diagram, data examples, field descriptions, and external system inventory. Mark areas lacking real materials as awaiting additional information.

**Completion criterion:** You can take a real customer document and explain where it comes from, who handles it, and what outcome it produces.

## 3. Define Business Rules and Formal Requirements

### Draft the Specification

1. Extract actors, actions, data, and constraints from the user's description.
2. For unspecified details, use reasonable defaults grounded in the available context and record them under Assumptions. If a choice materially affects scope or user experience, has multiple reasonable interpretations, and lacks a reasonable default, mark it as `[NEEDS CLARIFICATION: specific question]`.
3. Prioritize the three highest-impact ambiguities: scope first, then security and privacy, user experience, and technical details. Continue recording other unresolved matters; do not treat critical business rules as confirmed merely because of the question limit.
4. Write user scenarios. If a clear user flow cannot be determined, explain the gap and return to the interview.
5. Write functional requirements. Every requirement must be verifiable.
6. Define measurable, technology-agnostic success criteria that describe outcomes from the user's and business's perspective.
7. When data is involved, identify key business entities, attributes, and relationships.

Clarify roles and permissions, state transitions, quantity and monetary calculations and rounding, and relevant exceptions such as rejected approvals, cancellations, duplicate submissions, and network interruptions. Have business stakeholders confirm the meanings of states such as "received," "inspected and accepted," and "put into stock."

### Specification Structure

Maintain one main requirements document. Update the existing specification when one is available. Scope, current workflows, and data materials can be sections, or referenced attachments when extensive.

Include the following in the formal specification:

**User Scenarios and Acceptance**

Order user stories by importance, assigning priorities such as P1 and P2. For each story, describe the user journey, the reason for its priority, and how to independently verify the value it delivers.

Write acceptance scenarios as: **Given** an initial state, **When** the user performs an action, **Then** a particular outcome should follow.

List relevant boundary and exception cases: what happens at a boundary condition and how errors are handled.

**Requirements**

Use identifiers such as `FR-001` for specific, verifiable functional requirements. Mark unresolved rules for clarification where they occur. When data is involved, describe what key business entities represent, their important business attributes, and their relationships.

**Success Criteria**

Use identifiers such as `SC-001` to record measurable outcomes. Criteria should be user-focused, independent of implementation technologies such as frameworks, languages, and databases, and verifiable without knowing implementation details.

For post-launch business metrics, establish the definition, data source, baseline collection timing before launch, observation period, and owner. Mark missing agreements as pending. Identify data collection needs early enough for design and planning; do not wait until maintenance to discover that the baseline was never captured.

**Assumptions**

Record adopted defaults and assumptions about users, scope, data, the environment, and external dependencies.

Omit inapplicable optional sections rather than leaving empty placeholders.

### Clarify an Existing Specification

This step applies to a written specification and does not repeat the earlier open-ended interview.

First inspect the following areas, marking them internally as Clear, Partial, or Missing:

- Functional scope, core goals, success criteria, exclusions, and roles.
- Business entities, attributes, relationships, uniqueness, state transitions, and data scale.
- Critical user flows, including error, empty, and loading states.
- Performance, reliability, security, privacy, and relevant compliance constraints.
- External systems, data import and export, and failure scenarios.
- Exception handling, concurrency conflicts, constraints, and tradeoffs.
- Terminology consistency, verifiability of acceptance criteria, open decisions, and vague wording.

Ask only about matters that materially affect subsequent design or validation. Exclude questions already answered, trivial stylistic preferences, and specific implementation methods.

Handle no more than five questions per specification clarification session, presenting one question at a time. Prioritize by impact and uncertainty.

Use complete questions in plain language, followed by why they matter. Where a multiple-choice question is appropriate, offer 2–5 mutually exclusive options, highlight the recommendation, and briefly explain why. Otherwise, request a short answer. The user may accept the recommendation or supply their own answer. Resolve ambiguity in an answer before proceeding.

After each accepted answer:

1. Record one "Question → Answer" entry under Clarifications, grouped by date.
2. Immediately update the relevant requirements, user scenarios, entities, success criteria, or exception descriptions.
3. If the answer invalidates earlier wording, replace it rather than leaving contradictory copies.
4. Save the update, preserving the order and formatting of unrelated sections. Keep new wording concise and verifiable.

When a confirmed business rule changes, update the authoritative specification within authorization and assess affected design, tasks, tests, user instructions, and acceptance evidence. Record what remains applicable and what must be revalidated; reopen only affected work. If upstream edits are outside scope, record the exact required updates and their owner rather than silently treating stale artifacts as current.

End the session when critical ambiguities are resolved early, the user asks to stop, or five questions have been handled. Explicitly mark remaining important matters as deferred and explain why. If no meaningful clarification questions exist, report that directly rather than inventing questions to complete the process.

### Check Specification Quality

Use a separate requirements quality checklist to check that:

- Content focuses on user value and business needs, is written for business stakeholders, and contains no implementation details.
- Requirements are clear and verifiable; success criteria are measurable and technology-agnostic.
- Functional requirements have explicit acceptance criteria, and user scenarios cover the main flows.
- Edge cases are identified, scope is clear, and dependencies and assumptions are explicit.
- Critical clarification items are resolved. Unresolved items remain marked as failing.

Record the specific locations of failing items and revise the specification, with no more than three revision rounds. Preserve any remaining issues accurately. After clarification, reassess the checklist and report both newly passing items and regressions to failing status.

Report the specification's location, modified sections, check results, unresolved matters, and whether it is ready to proceed to solution design.

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

**Completion criterion:** The customer can give clear answers on critical business rules, and any unresolved matters are clearly marked.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Detailed discovery branches and helpers

Read [grilling](references/grilling.md) for an open-ended decision-tree interview and [document-grounded grilling](references/grill-with-docs.md) when existing documents should answer questions first. Open interviews use rounds without a fixed question cap. Use [the questionnaire procedure](references/questionnaire.md) for a third-party respondent. Read [domain modeling](references/domain-modeling.md), [glossary format](references/glossary-format.md), and [decision records](references/adr-format.md) when resolving terminology or recording durable choices.

For synthesis of an already settled conversation, use [conversation-to-spec](references/conversation-to-spec.md), including its complete user-story, implementation-decision, testing-decision, scope, and further-notes fields. Keep business requirements authoritative; put technical decisions in the linked technical plan rather than duplicating them in a second specification. Do not restart an interview when the information already exists. Publish only with tracker-write authorization.

For a feature specification use [the specification workflow](references/specify-workflow.md) and [spec template](assets/spec-template.md). Create its directory with `python3 <this-skill>/scripts/new_feature.py --json --write-pointer "<feature description>"`; omit `--write-pointer` when the project has another active-feature convention. The helper never creates a Git branch. For an existing specification use [clarification](references/clarify-workflow.md), at most five questions one at a time, then [requirements-quality checklists](references/requirements-checklists.md) and [the checklist template](assets/checklist-template.md). Reviewer-owned custom checklist markers are never set by implementation. The built-in [requirements checklist](assets/requirements-checklist.md) tracks specification quality and can be updated after actual re-evaluation.

Requirements: Python 3 for the helper; no helper is needed for an ordinary requirements-only edit. Follow [operating rules](../ask-eric/references/operating-rules.md) for evidence, authorization, and completion states.
