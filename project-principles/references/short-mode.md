# Short Mode

Use for a lean principles document: a small project, a prototype that will still be checked against rules, or an explicit request for a quick version.

## Scope guard

This mode's own work is limited to creating or updating the principles document, and propagating principle-driven changes to dependent project artifacts only when the user asks (then follow [sync-dependent-templates.md](sync-dependent-templates.md)).

- Classify every part of the user input as principles content or a separate non-governance intent. Feature implementation, code generation, refactoring, build, and deployment requests are examples of non-governance intents.
- You MUST NOT execute any non-governance intent. Defer each one to `Next Actions`.
- You MUST NOT create, modify, or delete application source files or other artifacts unrelated to the principles workflow.
- If an instruction could be either principles content or a non-governance intent, ask for clarification before making changes.
- After updating the principles, list each deferred intent in a `Next Actions` section with an appropriate follow-up LANYANT skill, but do not invoke it.
- Omit `Next Actions` when there are no non-governance intents.

## Procedure

1. Create or update the principles document at the location chosen by the [Location rule](../SKILL.md#location) (existing file, else `docs/constitution.md`; record the choice). The never-empty rule applies: write only principles the user supplied or confirmed context supports.
2. Include:
   - the project name;
   - the guiding principles;
   - the non-negotiable rules.
3. Derive content from user input and existing repository context (README, docs).
4. Add a version line (`**Version**: X.Y.Z | **Ratified**: YYYY-MM-DD | **Last Amended**: YYYY-MM-DD`) and bump it with the same MAJOR/MINOR/PATCH rules as full mode, so the consuming skills can cite which version they checked against.
5. Report the path, the version, and any `Next Actions`.

Short mode skips the full template structure and the Sync Impact Report. If the project later needs a governance section or a reviewed amendment trail, rerun in full mode; that is a MINOR bump.
