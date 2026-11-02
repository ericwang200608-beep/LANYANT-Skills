# Specify Workflow

Read this when you write a new feature specification from a feature description, or when you set up a feature directory for one. It expands [SKILL.md section 3](../SKILL.md#3-define-business-rules-and-formal-requirements) with the full procedure, the quality validation loop, and the clarification question format.

Use it only when no authoritative specification for this feature already exists. When one exists, update it in place and use [clarify-workflow.md](clarify-workflow.md) instead. Never create a competing specification.

## 1. Generate a concise short name

Create a 2-4 word short name for the feature:

- Analyze the feature description and extract the most meaningful keywords.
- Create a 2-4 word short name that captures the essence of the feature.
- Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug").
- Preserve technical terms and acronyms (OAuth2, API, JWT, etc.).
- Keep it concise but descriptive enough to understand the feature at a glance.
- Examples:
  - "I want to add user authentication" → "user-auth"
  - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
  - "Create a dashboard for analytics" → "analytics-dashboard"
  - "Fix payment processing timeout bug" → "fix-payment-timeout"

## 2. Create the feature directory and spec file

Follow the project's existing specification location first. When the project keeps feature specifications in numbered directories (or has no specification location yet and the user accepts this layout), create one feature directory per specification run:

- Specs live under `specs/` unless the project uses another directory (pass it with `--specs-dir`).
- Prefix: `NNN` (next available 3-digit number after scanning existing directories, skipping timestamp-prefixed directories) or, when the project uses timestamp numbering, `YYYYMMDD-HHMMSS`.
- Directory name: `<prefix>-<short-name>` (e.g., `003-user-auth` or `20260319-143022-user-auth`).

Run the helper from the project root:

```bash
python3 <skill-dir>/scripts/new_feature.py --json --short-name "<short-name>" "<feature description>"
```

Options: `--dry-run` (compute names and paths, create nothing), `--timestamp`, `--number N` (a preference; moves to the next free number if the prefix is taken), `--allow-existing` (reuse an existing directory; never overwrites an existing `spec.md`), `--specs-dir <dir>` (project-relative only), `--template <path>`, `--write-pointer`. The output JSON is `{"FEATURE_DIR": ..., "SPEC_FILE": ..., "FEATURE_NUM": ...}` (plus `"DRY_RUN": true` for a dry run). Names longer than 244 bytes are truncated with a warning. The helper never creates or switches git branches; the specification directory name and any branch name are independent and branching is the user's choice.

By default the helper writes the project's composed `spec-template` to `SPEC_FILE`: project override, priority-ordered preset layers, extension, project core, then [the bundled asset](../assets/spec-template.md). An invalid declared layer fails before creating a feature. `--template <path>` explicitly chooses that file instead. Resolve final feature/spec/pointer paths inside the project root; symlinks must not redirect writes outside it.

**Feature pointer file.** When the project opts in (`--write-pointer`, or `"write_feature_pointer": true` in `.lanyant/config.json`), the helper records the active feature directory in `.lanyant/feature.json`:

```json
{"feature_directory": "specs/003-user-auth"}
```

Later stages (technical design, delivery planning) read it to locate the feature without relying on branch names. The same config file may set `"feature_numbering": "timestamp"`. Without the opt-in, report the feature directory path in your summary instead; do not write configuration the project did not ask for.

Create only one feature per run.

If Python 3 is not available, create the directory and copy the template by hand following the same naming rules, and record that the helper was not run.

## 3. Load context

Read the spec template to understand required sections. If the project has recorded principles, load them and follow them (see [project-principles](../../project-principles/SKILL.md)).

## 4. Execution flow

1. Parse the user description. If empty: stop with "No feature description provided".
2. Extract key concepts from the description. Identify: actors, actions, data, constraints.
3. For unclear aspects:
   - Make informed guesses based on context and industry standards.
   - Only mark with `[NEEDS CLARIFICATION: specific question]` if:
     - The choice significantly impacts feature scope or user experience
     - Multiple reasonable interpretations exist with different implications
     - No reasonable default exists
   - **Limit: at most 3 `[NEEDS CLARIFICATION]` markers in the specification at once.**
   - Prioritize clarifications by impact: scope > security/privacy > user experience > technical details.
   - Critical business rules (roles and permissions, money and quantity calculations, state meanings, customer commitments) are never settled by a guess just because the marker limit is reached. Record the remaining ones as open questions in the scope statement and carry them into the interview or [clarify-workflow.md](clarify-workflow.md).
4. Fill the User Scenarios & Testing section. If no clear user flow can be determined: stop with "Cannot determine user scenarios", explain the gap, and return to the interview.
5. Generate Functional Requirements. Each requirement must be testable. Use reasonable defaults for unspecified details and document them in the Assumptions section.
6. Define Success Criteria. Create measurable, technology-agnostic outcomes. Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion). Each criterion must be verifiable without implementation details.
7. Identify Key Entities (if data involved).
8. Return: the specification is ready for quality validation.

## 5. Write the specification

Write the specification to `SPEC_FILE` using the template structure, replacing placeholders with concrete details derived from the feature description while preserving section order and headings.

## 6. Specification quality validation

After writing the initial spec, validate it against quality criteria.

**a. Create the spec quality checklist.** Copy [assets/requirements-checklist.md](../assets/requirements-checklist.md) to `<FEATURE_DIR>/checklists/requirements.md` (or next to the project's specification when it has no feature directory) and fill in the feature name, date, and spec link. Keep its items exactly; they are the fixed validation items:

- Content Quality: no implementation details (languages, frameworks, APIs); focused on user value and business needs; written for non-technical stakeholders; all mandatory sections completed.
- Requirement Completeness: no `[NEEDS CLARIFICATION]` markers remain; requirements are testable and unambiguous; success criteria are measurable; success criteria are technology-agnostic; all acceptance scenarios are defined; edge cases are identified; scope is clearly bounded; dependencies and assumptions identified.
- Feature Readiness: all functional requirements have clear acceptance criteria; user scenarios cover primary flows; feature meets measurable outcomes defined in Success Criteria; no implementation details leak into specification.

This built-in checklist is maintained by the specification and clarification procedures. Custom requirements-quality checklists are reviewer-owned; see [requirements-checklists.md](requirements-checklists.md).

**b. Run the validation check.** Review the spec against each checklist item:

- For each item, determine if it passes or fails.
- Document specific issues found (quote relevant spec sections).

**c. Handle validation results.**

- **If all items pass:** mark the checklist complete and go to the completion report.
- **If items fail (excluding `[NEEDS CLARIFICATION]`):**
  1. List the failing items and specific issues.
  2. Update the spec to address each issue.
  3. Re-run validation until all items pass (max 3 iterations).
  4. If still failing after 3 iterations, document remaining issues in the checklist notes and warn the user.
- **If `[NEEDS CLARIFICATION]` markers remain:**
  1. Extract all `[NEEDS CLARIFICATION: ...]` markers from the spec.
  2. **Limit check:** if more than 3 markers exist, keep only the 3 most critical (by scope/security/UX impact) and make informed guesses for the rest, recording each guess under Assumptions (critical business rules follow the rule in step 4.3).
  3. For each clarification needed (max 3), present options to the user in this format:

     ```markdown
     ## Question [N]: [Topic]

     **Context**: [Quote relevant spec section]

     **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]

     **Suggested Answers**:

     | Option | Answer | Implications |
     |--------|--------|--------------|
     | A      | [First suggested answer] | [What this means for the feature] |
     | B      | [Second suggested answer] | [What this means for the feature] |
     | C      | [Third suggested answer] | [What this means for the feature] |
     | Custom | Provide your own answer | [Explain how to provide custom input] |

     **Your choice**: _[Wait for user response]_
     ```

  4. **Table formatting:** ensure markdown tables are properly formatted:
     - Use consistent spacing with pipes aligned.
     - Each cell should have spaces around content: `| Content |` not `|Content|`.
     - Header separator must have at least 3 dashes: `|--------|`.
     - Check that the table renders correctly in markdown preview.
  5. Number questions sequentially (Q1, Q2, Q3; max 3 total).
  6. Present all questions together before waiting for responses.
  7. Wait for the user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B").
  8. Update the spec by replacing each `[NEEDS CLARIFICATION]` marker with the user's selected or provided answer.
  9. Re-run validation after all clarifications are resolved.

**d. Update the checklist.** After each validation iteration, update the checklist file with current pass/fail status.

## 7. Completion report

Report to the user:

- The feature directory path.
- The spec file path.
- Checklist results summary.
- Readiness for the next phase: clarification ([clarify-workflow.md](clarify-workflow.md)) or technical design ([technical-design](../../technical-design/SKILL.md)).

Done when the specification is written to `SPEC_FILE` and validated against the quality checklist, and the completion report has been given.

## Quick guidelines

- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.
- Do not embed checklists in the spec. Checklists are separate files.

### Section requirements

- **Mandatory sections:** must be completed for every feature.
- **Optional sections:** include only when relevant to the feature.
- When a section doesn't apply, remove it entirely (don't leave it as "N/A").

### When generating a spec from a prompt

1. **Make informed guesses:** use context, industry standards, and common patterns to fill gaps.
2. **Document assumptions:** record reasonable defaults in the Assumptions section.
3. **Limit clarifications:** at most 3 `[NEEDS CLARIFICATION]` markers; use them only for critical decisions that:
   - Significantly impact feature scope or user experience
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications:** scope > security/privacy > user experience > technical details.
5. **Think like a tester:** every vague requirement should fail the "testable and unambiguous" checklist item.
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Feature scope and boundaries (include/exclude specific use cases)
   - User types and permissions (if multiple conflicting interpretations possible)
   - Security/compliance requirements (when legally/financially significant)

**Examples of reasonable defaults** (don't ask about these):

- Data retention: industry-standard practices for the domain.
- Performance targets: standard web/mobile app expectations unless specified.
- Error handling: user-friendly messages with appropriate fallbacks.
- Authentication method: standard session-based or OAuth2 for web apps.
- Integration patterns: use project-appropriate patterns (REST/GraphQL for web services, function calls for libraries, CLI args for tools, etc.).

Record each adopted default under Assumptions so the business owner can see and overturn it.

### Success criteria guidelines

Success criteria must be:

1. **Measurable:** include specific metrics (time, percentage, count, rate).
2. **Technology-agnostic:** no mention of frameworks, languages, databases, or tools.
3. **User-focused:** describe outcomes from the user/business perspective, not system internals.
4. **Verifiable:** can be tested/validated without knowing implementation details.

**Good examples:**

- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (implementation-focused):

- "API response time is under 200ms" (too technical; use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail; use a user-facing metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)
