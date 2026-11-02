# Stage 1: Intake

Capture a raw idea, however rough, and normalize it into a single **intake note** at `ASSESS_DIR/intake.md`. This is the front door of the pipeline: it records what the idea is and where it came from without judging it. Research, define, shape, and decide build on it.

Intake **captures; it does not evaluate or solutionize.** No feasibility verdicts, no design. Just a clean, faithful record of the idea and its origin.

## Input

Treat the user input as one of:

1. **Pasted text:** a one-liner, a paragraph, a stakeholder ask, meeting notes, a ticket body.
2. **A URL:** a link to an issue, doc, thread, or page describing the idea. Apply the URL Trust Policy in [safety.md](safety.md#9-url-trust-policy) before fetching.
3. **A codebase pointer:** phrasing like "an idea for this repo" or a path. Read enough of the repository to record what the idea relates to.
4. **A mix** of the above.

There is no requirement for existing source code. Intake works as well on an empty project as on an established codebase. Pasted text and URLs need no codebase; a codebase pointer targets existing code. Both are equally valid.

If the input is empty, ask the user for the idea (interactive), or stop with a note that there is nothing to intake (automated).

## Prerequisites

1. Resolve `ASSESS_ROOT` and run ancestor path safety ([safety.md](safety.md) sections 1 and 2).
2. Resolve and normalize the slug with the intake rules ([safety.md](safety.md) sections 3 and 4).
3. Run path safety, then ensure `ASSESS_DIR` exists, creating it and missing parents if necessary ([safety.md](safety.md) section 5).
4. If `ASSESS_DIR/intake.md` already exists, apply the intake overwrite rules ([safety.md](safety.md) section 7).

## Execution

1. **Capture the idea, redacting secrets.** Preserve the original wording (quoted) plus the source (URL, pasted block, or repo path), applying the same sanitization as the Source field inside the quoted text too: sanitize any credential-bearing URL and redact tokens, passwords, API keys, or cookies. Never persist a secret because it appeared in the original.
2. **Restate it in one or two neutral sentences.** What is being proposed, in plain language, without endorsing or dismissing it.
3. **Record origin and context.** Who raised it, when, and any triggering event (a complaint, an outage, a sales ask, a strategy shift). Mark unknowns as `[NEEDS CLARIFICATION: ...]`.
4. **Note the idea type** so downstream stages know what to weigh: `new-capability` | `improvement` | `fix` | `exploration` | `cost-saving` | `compliance` | `other`.
5. **List first-glance unknowns:** the obvious questions that must be answered before anyone decides. Do not answer them here.
6. **Write the intake note** to `ASSESS_DIR/intake.md`:

   ```markdown
   # Idea Intake: <short title>

   - **Slug**: <ASSESS_SLUG>
   - **Created**: <ISO 8601 date>
   - **Assessment location**: <ASSESS_ROOT> (<existing project convention | default docs/assessments>)
   - **Source**: <sanitized URL, "pasted text", or repo path>
   - **Type**: new-capability | improvement | fix | exploration | cost-saving | compliance | other

   ## Idea (as captured)

   <Quoted original, with any credential-bearing URL sanitized and secrets (tokens, passwords, keys, cookies) redacted. If a URL was fetched, include the title and a short excerpt; link the sanitized URL and record the URL Trust Policy branch taken.>

   ## Restated

   <One or two neutral sentences.>

   ## Origin & Context

   - **Raised by**: <who / [NEEDS CLARIFICATION]>
   - **Trigger**: <what prompted it / [NEEDS CLARIFICATION]>

   ## First-Glance Unknowns

   - [NEEDS CLARIFICATION: ...]
   ```

7. **Report back** with:
   - The slug, on its own line (for example `Slug: <ASSESS_SLUG>`), so later stages reuse it from context.
   - The path `ASSESS_DIR/intake.md`.
   - The next suggested stage: research for this slug, or define if the idea is already well understood and needs no evidence gathering.

## Guardrails

- Writes are limited to `ASSESS_DIR`. Never modify source files or anything outside that directory. Reads may include the supplied sources: inspect the repository (for a codebase-pointer idea) and fetch an allowed URL under the URL Trust Policy, read-only, to capture the idea.
- Never evaluate, size, or solutionize the idea here. That is what the later stages do.
- Never invent origin, ownership, or context the input does not support. Mark it `[NEEDS CLARIFICATION: ...]`.
- Never overwrite an existing `intake.md` without confirmation.
- If there is no coherent idea (empty, spam, unrelated), say so and stop rather than fabricating one.
