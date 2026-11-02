---
name: workflow-prototype
description: Build interactive temporary prototypes to validate business logic, state transitions, and user workflows, and record trial feedback. Use before production development to confirm workflows, or to evaluate workflow improvements through a demo; compare UI alternatives when there is a concrete interface disagreement.
---

# Workflow Prototype

A prototype is temporary code that answers a question. The question determines its shape. Let non-developers click buttons and observe state changes to judge whether a business workflow meets their actual needs.

## 1. Define the question the prototype answers

Use the user's request, existing requirements, and relevant code to identify the question:

- **"Does this business logic or state model make sense?"** Build a shareable HTML file with free-play buttons and guided scenarios that exercise cases difficult to judge on paper.
- **"What should this interface look like?"** Build alternatives only when there is a concrete interface disagreement, and make them switchable from a common entry point.

Default to business workflow validation. If ambiguity between these questions affects the deliverable, clarify it first. When adopting an assumption based on available information, state it at the top of the prototype.

Before writing code, describe the state model and specific question in one paragraph at the top of the demo, not just in a code comment. Users should be able to judge whether it answers the right question, whether they open it now or later.

## 2. Select user journeys and trial scenarios

Prioritize user stories as user journeys. Each journey should be independently checkable and demonstrable, producing a valuable outcome even if it is the only journey completed.

For each selected journey, explain:

- In plain language, what work the user needs to complete.
- Why this work is a priority for validation.
- How to check it independently and what result to expect.

Describe scenarios as "Given an initial state, When an action is taken, Then the expected outcome occurs." Include the normal flow, a tricky edge case, and an attempt at an invalid action relevant to the question. Mark unclear rules as "NEEDS CLARIFICATION" and record assumptions that affect the judgment.

Reuse existing acceptance scenario identifiers and definitions; add only prototype-specific actions and observations. Simulated results remain prototype evidence, not implementation evidence.

Confirm the entry point, information needed on the page, required fields, submission results, and error messages against the actual work. When multiple roles are involved, let them act in sequence on the same sample record to complete a task.

## 3. Separate logic from the page

Place the logic that answers the question in a single script block, organized as a small, independent module. The page is a temporary shell; validated logic can inform the eventual production implementation.

Choose the shape that fits the question:

- **A pure reducer:** Takes state and an action, returns new state; suitable for discrete events.
- **A state machine:** Explicit states and transitions; suitable for determining which actions are currently allowed.
- **A set of pure functions:** Transforms plain data types; suitable when there is no ongoing state.
- **A class or module with a clear interface:** Suitable when the logic genuinely needs to manage ongoing internal state.

Choose based on the question, rather than merely on what is easiest to wire to the page. Business logic must not access page elements or `document`, and button handlers must not modify module internals directly. The page calls the logic; the logic does not depend on the page.

## 4. Build a shareable demo

For business logic demos, prefer a single self-contained HTML file with inline HTML, CSS, and JavaScript. It should open with a double-click, without a framework, bundler, or server. If a UI comparison requires existing project components, use the project's routing and runtime conventions and provide one clear launch command.

Clearly mark it as a prototype from the start. In an existing project, place it near the relevant module or page and follow the project's prototype and routing conventions. Without an existing project, use a separate prototype directory.

Use in-memory state without persistence by default. Only when the question explicitly concerns persistence should you use a temporary database or file clearly named as disposable. Do not connect to a real business database.

Write the page for non-developers. Use business language for buttons, fields, and states, and explain what is happening in plain words.

Organize the page with a clear hierarchy:

1. **Title and short explanation:** State what the demo lets the user explore.
2. **Current state:** Show relevant state as labeled fields rather than a raw data dump. Refresh it after each click, highlighting what changed when useful.
3. **Free-play buttons:** Provide a button for each action so users can explore in different orders. Each click performs the action and displays the result. Give clear feedback for invalid actions.
4. **Guided scenarios:** Give each scenario its own tab with a short explanation, what to observe, and ordered action buttons. Each step actually performs an action. Starting a scenario resets to a known initial state so results are repeatable.

Provide simulated role switching for workflows that cross roles, clearly stating that this is not production authentication or backend authorization verification. Include a sample-data reset control for repeated trials.

Keep the interface attractive but restrained: clean typography, generous spacing, and one accent color, without competing animations or decoration. Retain error messages needed to run the demo and validate the question. Do not add general abstractions, future features, or a complete testing infrastructure to the prototype.

## 5. Run it and give it to actual users

Open the demo and execute the selected scenarios, observing page and state changes. Check outcomes for normal paths and relevant invalid actions, and fix problems that prevent a useful trial.

Give users the file or open it for them. Have actual users complete a task, such as "a requester creates a purchase request, and a supervisor finds and approves it," and allow free exploration. For mobile scanning, check actual operation on the relevant device. If only the page after scanning is simulated, state that real scanning remains unverified.

Pay attention when users say "that should not happen" or "I assumed this would be different." These reactions reveal problems in the idea, which is what the prototype exists to find. Adjust actions or scenarios based on feedback. If feedback changes business rules, update the relevant requirements after confirmation.

Record actual feedback and its disposition. Without feedback from actual users, state "Ready for trial; business confirmation pending." Mark checks that were not executed as unverified.

When a confirmed business rule changes, update the authoritative specification within authorization and assess affected design, tasks, tests, user instructions, and acceptance evidence. Record what remains applicable and what must be revalidated; reopen only affected work. If upstream edits are outside scope, record the exact required updates and their owner rather than silently treating stale artifacts as current.

## 6. Preserve the conclusion and deliver

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Once the prototype has answered its question, preserve the question, the conclusion, and the prototype itself so later work can revisit and rerun it.

Deliver:

- The interactive prototype and instructions to open or run it.
- Key page and workflow explanations, which may live inside the prototype.
- Customer feedback, confirmed decisions, and questions still awaiting confirmation.

Business confirmation for this stage means actual users can complete the selected task and confirm that its key interactions meet their needs. Record prototype checks and user confirmation separately.

Pass confirmed decisions to subsequent design and implementation. This stage does not automatically modify production code, commit branches, or publish the system. Do not deliver prototype pages directly as a production system.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Detailed prototype branches

Read [logic prototype](references/logic-prototype.md) for free-play state controls and guided scenario tabs. Read [UI alternatives](references/ui-prototype.md) when comparing distinct interface directions. Read [technical prototype](references/technical-prototype.md) for a measurable technical uncertainty. Answer observable engineering questions by running a small experiment rather than asking the user to predict them. Keep prototype evidence separate from production implementation and customer acceptance. Capture a validated question, verdict, and decision-rich code in the existing task record; commit or publish only within existing authorization.
