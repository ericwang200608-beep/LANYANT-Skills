---
name: project-principles
description: "Create or amend the project's principles document (its constitution): the non-negotiable rules, quality gates, and governance that design, planning, and verification check against. Fills the template's placeholder tokens, bumps the semantic version by the MAJOR/MINOR/PATCH rules, writes a Sync Impact Report, validates the result, and defers non-governance requests instead of executing them. Use when someone says \"set up our project principles\", \"write a constitution\", \"add a principle\", \"amend the governance rules\", \"we now require X on every change\", \"bump the constitution version\", or asks to propagate amended principles into the project's own templates and guidance docs. Has a short mode for small projects and an opt-in sync mode for dependent templates."
---

# Project Principles

Maintain one principles document per project. It holds declarative, testable rules (MUST and SHOULD with rationale), the additional constraints and workflow gates the team commits to, and the governance that controls amendments. Other skills read it at run time:

- [technical-design](../technical-design/SKILL.md) checks the principles before design and rechecks them after design, and pauses dependent design work on an unjustified violation.
- [delivery-planning](../delivery-planning/SKILL.md) runs its consistency check against the principles and treats a violation of a MUST rule as a critical finding that marks affected tasks not ready.
- [system-verification](../system-verification/SKILL.md) uses the principles as constraints on the intent it verifies; full convergence is not reported while a MUST rule is violated.
- [business-discovery](../business-discovery/SKILL.md) reads and follows existing principles; [idea-assessment](../idea-assessment/SKILL.md) uses them for strategic fit.

Follow the shared [operating rules](../ask-eric/references/operating-rules.md).

## When to use

- A project needs its first principles document and the user (or confirmed project context) supplies real principles.
- An existing principles document needs a principle added, removed, redefined, or clarified, or its governance or dates updated.
- The user asks to propagate amended principles into the project's own templates, command files, and guidance docs (sync mode).

## Inputs to read

- The user's input. You MUST consider it before proceeding (if not empty).
- The existing principles document, if any: its current values, amendments, version, and dates.
- The active principles template resolved through all configured override, preset and extension layers, using [template resolution](../delivery-planning/references/customization.md#template-layers-and-feature-paths); the final core fallback is [assets/constitution-template.md](assets/constitution-template.md).
- Repository context for inferring values: README, docs, contributing guide, earlier versions of the principles.

## Location

Use the project's existing principles file, wherever it lives (for example `docs/constitution.md`, `CONSTITUTION.md`, `PRINCIPLES.md`, or a principles document the instructions file points to). If none exists, use `docs/constitution.md`. Record the chosen path, and why, in the Sync Impact Report and in the final summary, and link it from the project's instructions file (`AGENTS.md` or `CLAUDE.md`) only when that edit is in scope.

**Never create an empty principles file.** Do not write the template with unreplaced placeholders as a new document, and do not invent commitments to fill it. If the user has not supplied principles and none can be inferred from confirmed project context, ask for them (interactive) or stop and record that no principles were supplied (automated). For a new project without principles, the minimum confirmed constraints belong in the existing specification or plan, as [business-discovery](../business-discovery/SKILL.md) and [technical-design](../technical-design/SKILL.md) describe.

## Scope guard

This skill's own work is limited to updating the principles document itself. Dependent templates, command files, and guidance read the principles at run time and are not modified here, except in sync mode when the user asks for propagation.

- Classify every part of the user input as either principles content or a separate, non-governance intent.
- If the input includes feature implementation, code generation, refactoring, building, or deployment requests, you MUST NOT execute them. Extract them as deferred intents instead.
- You MUST NOT create, modify, or delete application source files, feature routes, components, tests, deployment files, or other artifacts unrelated to the principles workflow.
- If it is unclear whether an instruction is principles content, ask for clarification before making changes.
- After completing the update, include a `Next Actions` section for each deferred intent. List the original intent and suggest the appropriate follow-up LANYANT skill (for example [business-discovery](../business-discovery/SKILL.md) for a new feature, or [feature-implementation](../feature-implementation/SKILL.md) for a defined change) without invoking it.
- If there are no non-governance intents, omit the `Next Actions` section.

## Modes

| Mode | Use when | Procedure |
|---|---|---|
| **Full** (default) | Creating or amending principles in any project that will be checked against them. | Steps 1 to 8 below. |
| **Short** | The user asks for a lean or quick principles document, or the project is small. | [references/short-mode.md](references/short-mode.md). The scope guard and the never-empty rule still apply. |
| **Sync** | The user asks to propagate amended principles into the project's own dependent templates, command files, and guidance docs. | Steps 1 to 8, then [references/sync-dependent-templates.md](references/sync-dependent-templates.md). Without that request, the scope guard holds and nothing outside the principles document is edited. |

## Procedure (full mode)

1. **Pre-amendment steps and hooks.** Read [the hook dispatch protocol](../delivery-planning/references/customization.md#before-and-after-hooks) and inspect `.lanyant/extensions.yml` for `hooks.before_constitution`, alongside any project-defined pre-amendment steps. Preserve each hook's identifier, description, prompt, enabled/optional flags and condition. Missing `enabled` means enabled; skip only explicitly disabled entries. Dispatch authorized unconditional mandatory hooks through actual installed actions and wait for their result before changing the document. List optional hooks and execute only within existing authorization. A nonempty condition requires a real supported evaluator; never invent its truth value. Record parser errors, absent runners/evaluators and missing authorization as blockers to the affected mandatory step. Listing or printing a command never satisfies execution; continue only unaffected work.

2. **Load the structure and current values.**
   - Resolve the active `constitution-template` with the shared template resolver in [customization](../delivery-planning/references/customization.md#template-layers-and-feature-paths), including configured overrides, ordered preset composition, extension layers and the core [bundled fallback](assets/constitution-template.md). Use the complete resolved content as the required structure. A resolution or parsing error stops dependent amendment work; do not silently discard a contributing layer. Do not write back to any template.
   - If the principles document exists, load it as the source of current project-specific values and amendments. Preserve information that is still applicable when applying the structure.
   - If it does not exist, use the template as the initial structure (subject to the never-empty rule).
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   - The user might require fewer or more principles than the template has. If a number is specified, respect it and follow the general template.

3. **Collect or derive values for placeholders.**
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repository context (README, docs, prior versions of the principles).
   - Governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown, ask or mark TODO). `LAST_AMENDED_DATE` is today if changes are made; otherwise keep the previous value.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning:
     - **MAJOR:** backward-incompatible governance or principle removals or redefinitions.
     - **MINOR:** a new principle or section added, or materially expanded guidance.
     - **PATCH:** clarifications, wording, typo fixes, non-semantic refinements.
   - If the bump type is ambiguous, propose your reasoning before finalizing.

4. **Draft the updated content** using the template as the required structure.
   - Replace every placeholder with concrete text. No bracketed tokens remain except intentionally retained template slots the project has chosen not to define yet; explicitly justify any left.
   - Preserve the heading hierarchy. Template comments can be removed once replaced unless they still add clarifying guidance.
   - Each principle section has a succinct name line, a paragraph or bullet list capturing the non-negotiable rules, and an explicit rationale if not obvious.
   - The Governance section lists the amendment procedure, the versioning policy, and compliance review expectations.

5. **Produce a Sync Impact Report** as an HTML comment at the top of the principles file. It is temporary scratch material for human review of the amendment, not governance content, and is expected to be removed before the amended file is committed.
   - Version change: old to new.
   - Modified principles (old title to new title if renamed).
   - Added sections.
   - Removed sections.
   - Location chosen (when the file was created this run) and why.
   - Follow-up TODOs if any placeholders were intentionally deferred.

6. **Validate before final output.**
   - No remaining unexplained bracket tokens.
   - The version line matches the report.
   - Dates are ISO format `YYYY-MM-DD`.
   - Principles are declarative, testable, and free of vague language ("should" is replaced with MUST or SHOULD plus rationale where appropriate).

7. **Write** the completed document back to the principles file (overwrite). Write only that file; do not create or modify template source files.

8. **Post-amendment steps and summary.** Apply the same actual dispatch, enabled/condition/optional and blocker rules to `hooks.after_constitution` and project-defined post-amendment steps, in declared order. Wait for authorized mandatory hooks to finish. A document may be written while post-hook verification remains blocked; record those states separately and do not mark the amendment fully verified. Then output a final summary to the user with:
   - The new version and bump rationale.
   - The file path, and whether it was created or amended.
   - Any TODO placeholders or deferred items requiring manual follow-up.
   - A suggested commit message (for example `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).
   - A `Next Actions` section for any deferred non-governance intents.

If the user supplies partial updates (for example only one principle revision), still perform the validation and version-decision steps.

If critical information is missing (for example the ratification date is truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include it in the Sync Impact Report under deferred items.

### Formatting and style

- Use Markdown headings exactly as in the template (do not demote or promote levels).
- Wrap long rationale lines for readability (under 100 characters ideally) without awkward hard breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

## Verification required

- Rerun the step 6 checks on the written file, not on the draft: `grep -nE '\[[A-Z][A-Z0-9_]+\]' <file>` returns only justified slots; the version line equals the report's new version; every date matches `[0-9]{4}-[0-9]{2}-[0-9]{2}`.
- The diff touches only the principles file (plus, in sync mode, the files listed in the extended report). Check with `git status` / `git diff --stat`.
- The bump type matches the change classification in the Sync Impact Report.
- Every required pre/post hook actually completed with evidence; disabled, optional, conditional, failed and blocked hooks retain their accurate state. The full template resolver succeeded before the amendment.

## Outputs and state

- The principles file, with the Sync Impact Report comment for review.
- The final summary from step 8. Committing follows the project's convention and the current authorization; the Sync Impact Report comment is removed before the commit.
- When the amendment belongs to a tracked task, record the version change and file link in that task record per [operating rule 3](../ask-eric/references/operating-rules.md#3-evidence-record). Do not create a separate tracker.

## Completion criteria

The principles file holds concrete, validated content at the new version; the bump rationale and deferred items are reported; deferred non-governance intents are listed in `Next Actions`; and, in sync mode, every dependent file is marked updated or pending in the report. Mandatory hook execution and complete template resolution must pass before the workflow is declared verified; missing capabilities remain explicit blockers.

## What this skill does not authorize

- Executing feature, code, refactor, build, or deployment requests found in the input.
- Editing templates, command files, or guidance docs outside sync mode, or editing package-managed files in any mode.
- Inventing business commitments or principles the user has not confirmed.
- Creating an empty or placeholder-only principles file.
- Committing, pushing, or opening a PR beyond the current authorization ([operating rule 1](../ask-eric/references/operating-rules.md#1-authorization-classes)).
