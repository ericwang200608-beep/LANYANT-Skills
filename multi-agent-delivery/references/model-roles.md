# Model Roles

Choose a model and effort for each agent role, and record the project's choices where every session reads them. Read this when a mode asks you to pick a model per role, or when the user wants to configure which models the agent roles use.

## Roles

| Role | What it does | Default choice |
| --- | --- | --- |
| feature and refactoring delegate | Writes code for a feature or refactor | Fast code model at xhigh effort |
| bug-fix delegate | Writes a fix and its regression test | Fast code model at xhigh effort |
| performance delegate | Profiles and changes code for a measured slowdown | Fast code model at xhigh effort |
| hill-climb delegate | Iterates one metric | Fast code model at xhigh effort |
| judgment and prose | Plans, reviews, synthesis, writing for people | Strongest judgment model at xhigh effort |
| hardest tasks | Cross-cutting design, concurrency, subtle algorithms, whether vague or precisely specified | Strongest judgment model, effort raised one step |
| explorer and investigator | Reads code and history, returns pointers | Fast code model |
| explainer and synthesizer | Turns findings into an explanation | Strongest judgment model |
| arena runners | Candidates in an [arena](arena.md); a list, one runner per entry | One strong model from each available family |
| arena cross-judge pool | Ordered list; one judge from a family other than the coordinator's | Strongest model of each other family |
| swarm workers | Default model for every [swarm](swarm.md) worker and every verifier lane | Fast code model |
| design runners | Candidates for design exploration | Same as arena runners |
| adversarial reviewers | Adversaries in [adversarial-review](../../adversarial-review/SKILL.md) | One strong model from each available family |

A panel role's value is a list. One agent runs per entry, so the list length sets the panel size. The swarm-workers value is the default for every worker unless a race or comparison assigns a model per arm.

## Matching effort to the job

Before each spawn, start from the role's recorded value or default and pick the effort and speed the job needs:

- The recorded budget sets each role's starting effort. Without a budget, start at xhigh (the `large` budget).
- Raise effort one step, up to the maximum, for the hardest or subtlest work. Lower it one step for judgment and two or more steps for routine work.
- Use a fast or priority mode only when the job is urgent: CI or trunk is red, or a person is blocked on the result right now. Otherwise use standard speed.
- Verification is the exception: it stays on the swarm-workers model and speed.
- Change only effort and speed, and keep the family the role names, so a diverse panel stays diverse. If the family has no model at that effort, use its nearest.
- A role set to `inherit-parent` (or `auto`) runs on the coordinator's own model: omit the model field when spawning.
- If the harness rejects a chosen model, do not try another adjusted value. Fall back to the role's recorded value or default and say so. If that is rejected too, use the closest valid model of the same family from the error's list, or omit the model so the agent runs on the parent model, and say so.

Effort ladder, highest first: `max` > `xhigh` > `high` > `medium` > `low`. Budget labels map to a target effort for every real model: `unlimited` to `max`, `large` to `xhigh`, `medium` to `high`, `small` to `medium`. When a family tops out below the target, use its highest available effort.

## Configuring the project's roles

Run this when the user asks to configure model roles, or when a mode needs a role choice and none is recorded.

1. **Detect available models.** Enumerate the models and efforts you can pass when spawning an agent in this session (the agent tool's schema is the dependable source; see [harness-adapters.md](harness-adapters.md) for each harness's model field). If you cannot detect any, ask the user to paste what they have access to. Never record a model you have not confirmed is available. `inherit-parent` and `auto` are always valid.
2. **Load current state.** If the project instructions already hold a model-roles block, read its budget line and role values as the current choices. Otherwise start from the defaults above. Drop a line whose role is not in the table, and list it.
3. **Budget, map, and confirm.** Ask for a budget with these options (structured question when available): `unlimited (max effort)`, `large (xhigh effort)`, `medium (high effort)`, `small (medium effort)`. Name the current budget when one is recorded. Apply it to every real model's effort, keeping roles the user set to a specific family, list, or alias. Show every role with its value, marking any value not in the detected set as needing a choice, and ask whether to accept or change specific roles. Offer the detected models plus `inherit-parent` and `auto`. For the cross-judge pool, explain that order is preference and an alias entry never judges.
4. **Validate.** Every real model written must be in the detected set. If a chosen model is unavailable, stop and ask again.
5. **Record.** Write a model-roles block in the project's instructions file (see [harness-adapters.md](harness-adapters.md) for the file per harness: `AGENTS.md`, `CLAUDE.md`, or the harness's rules directory). Writing the instructions file changes persistent configuration that other people and agents read, so do it only when the user asked for the configuration; otherwise show the block for them to add. Overwrite the whole block so re-runs stay idempotent. Shape:

   ```markdown
   ## Agent model roles
   <!-- One line per role. Delete a line to fall back to the default. inherit-parent or auto: run on the coordinator's model (omit the model field). Alias entries in a panel list still count toward its size. -->
   budget: large (xhigh)
   feature, refactoring: <model> <effort>
   bug-fix: <model> <effort>
   perf-issue: <model> <effort>
   hillclimb: <model> <effort>
   judgment and prose: <model> <effort>
   hardest tasks: <model> <effort>
   explorer: <model> <effort>
   explainer: <model> <effort>
   arena runners: <model> <effort>, <model> <effort>
   arena cross-judge pool: <model> <effort>, <model> <effort>
   swarm workers: <model> <effort>
   design runners: <model> <effort>, <model> <effort>
   adversarial reviewers: <model> <effort>, <model> <effort>
   ```

6. **Confirm.** Tell the user where the block was written and that it applies to new sessions. Re-running this procedure updates it.
7. **Offer verification setup (optional, once each).** If the project has no way to drive the real app for proof (a project verification skill or an existing harness), offer once to create one with [verification-harness](../../verification-harness/SKILL.md). If it has no formal verification for a key property, offer once the same way. On no, move on without pushing.

## When only one model family is available

Record "independent context, same model family" for every cross-judge, verifier, and adversary (operating rule 5.7). A one-family arena still runs, with all runners on that family; its cross-judge is skipped and the coordinator picks the base alone and says so.
