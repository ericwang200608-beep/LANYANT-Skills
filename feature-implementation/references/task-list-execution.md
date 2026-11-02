# Task-List Execution

Read when implementing a feature from a written task list (with a spec and technical plan) rather than a single ticket. It details the checklist gate, context loading, project setup verification, and phase-by-phase execution that [sections 1 and 4 of the skill](../SKILL.md) summarize. It assumes a complete task breakdown exists. If tasks are incomplete or missing, complete them first with [delivery-planning](../../delivery-planning/SKILL.md).

## 1. Project workflow hooks (before implementation)

Some projects register commands to run before or after implementation in their workflow configuration. If the project has such a registry:

- If the configuration cannot be parsed, do not skip silently. Tell the user it could not be read (include the parser error) and that no hooks were checked, including any mandatory ones, then continue.
- Ignore hooks explicitly disabled. Treat hooks without an enabled flag as enabled.
- Do not evaluate hook conditions yourself. A hook with no condition is executable; a hook with a non-empty condition is left to the project's own hook runner.
- **Optional hook:** list its name, command, description, and prompt so the user can run it.
- **Mandatory hook:** actually run it and wait for it to finish before continuing. Listing it is not running it.
- A hook that is outward-facing or irreversible still needs authorization per [operating rules section 1](../../ask-eric/references/operating-rules.md#1-authorization-classes).

If no registry exists or no hooks are registered, skip silently. Repeat the same procedure for after-implementation hooks before reporting completion.

## 2. Checklist gate

When the feature directory has a `checklists/` directory, run the read-only gate:

```sh
python3 <skill-dir>/scripts/checklist_gate.py <feature-dir>
```

- The built-in requirements checklist is maintained by specification and clarification work. Custom checklists are reviewer-owned requirements-quality artifacts. A checked item means the reviewer judged the requirements-quality criterion satisfied. It does not mean implementation work is complete.
- Treat checklist markers as read-only. Never edit checklist files or markers to pass the gate.
- For each checklist the gate counts total items (`- [ ]`, `- [x]`, `- [X]`), checked items, and unchecked items, and prints a table with a PASS or FAIL per checklist. The overall gate passes only when every checklist has zero unchecked items (exit 0); otherwise it fails (exit 1). Exit 0 with "NOT APPLICABLE" means there is no checklist to gate on.
- **If any checklist has unchecked items:** show the table and stop. Ask: "Some checklists have unchecked items. Do you want to proceed with implementation anyway? (yes/no)". Wait for the answer. On "no", "wait", or "stop", halt. On "yes", "proceed", or "continue", go on. Skip the question only when the user already authorized proceeding with these specific unchecked items; record that authorization with the table.
- **If all checklists pass:** show the table and proceed.

## 3. Load the implementation context

- **Required:** the task list (complete task list and execution plan).
- **Required:** the technical plan (stack, architecture, file structure).
- **If present:** the data model (entities and relationships), interface contracts (API specifications and test requirements), research or decision notes (technical decisions and constraints), project principles (governance constraints), and validation scenarios (integration scenarios).

## 4. Project setup verification

Create or verify ignore files for the actual project setup. Detect first:

- `git rev-parse --git-dir 2>/dev/null` succeeds: create or verify `.gitignore`.
- `Dockerfile*` exists or the plan uses Docker: `.dockerignore`.
- `.eslintrc*` exists: `.eslintignore`.
- `eslint.config.*` exists: ensure the config's `ignores` entries cover the required patterns.
- `.prettierrc*` exists: `.prettierignore`.
- `.npmrc` or `package.json` exists: `.npmignore` (only if publishing).
- Terraform files (`*.tf`) exist: `.terraformignore`.
- Helm charts present: `.helmignore`.

If the ignore file exists, verify it contains the essential patterns and append only missing critical patterns. If it is missing, create it with the full pattern set for the detected technology. Add only entries the actual stack needs.

**Common patterns by technology** (from the plan's stack):

- **Node.js/JavaScript/TypeScript:** `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
- **Python:** `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
- **Java:** `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
- **C#/.NET:** `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
- **Go:** `*.exe`, `*.test`, `vendor/`, `*.out`
- **Ruby:** `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
- **PHP:** `vendor/`, `*.log`, `*.cache`, `*.env`
- **Rust:** `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
- **Kotlin:** `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
- **C++:** `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
- **C:** `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `*.dll`, `autom4te.cache/`, `config.status`, `config.log`, `.idea/`, `*.log`, `.env*`
- **Swift:** `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
- **R:** `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
- **Universal:** `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

**Tool-specific patterns:**

- **Docker:** `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
- **ESLint:** `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
- **Prettier:** `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- **Terraform:** `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
- **Kubernetes/k8s:** `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

## 5. Parse the task list

Extract:

- **Task phases:** for example Setup, Tests, Core, Integration, Polish.
- **Task dependencies:** sequential versus parallel execution rules.
- **Task details:** ID, description, file paths, parallel markers `[P]`.
- **Execution flow:** order and dependency requirements.

## 6. Execute phase by phase

- **Phase-by-phase execution:** complete each phase before moving to the next.
- **Respect dependencies:** run sequential tasks in order; tasks marked `[P]` may run together.
- **Tests with code:** for behavior that requires test-first work, write the failing test for one behavior, then its implementation, one cycle at a time per [section 3 of the skill](../SKILL.md#3-complete-one-red-to-green-cycle-at-a-time). A test-before-code phase never means writing every test before any implementation.
- **File-based coordination:** tasks affecting the same files run sequentially.
- **Validation checkpoints:** verify each phase's completion before proceeding.

Execution order inside the plan:

- **Setup first:** project structure, dependencies, configuration.
- **Tests before code** where tests are required: contracts, entities, integration scenarios.
- **Core development:** models, services, CLI commands, endpoints.
- **Integration work:** database connections, middleware, logging, external services.
- **Polish and validation:** unit tests, performance work, documentation.

## 7. Progress tracking and error handling

- Report progress after each completed task.
- Halt execution if any non-parallel task fails. Stop downstream work that depends on it.
- For parallel `[P]` tasks, continue with the successful ones and report the failed ones.
- Give clear error messages with context for debugging, and suggest next steps if implementation cannot proceed.
- Mark a task `[X]` in the task list only after its implementation and its necessary verification have actually passed. Never mark requirements-quality checklists or customer acceptance records as part of this.

## 8. Completion validation

- Verify all required tasks are completed.
- Check that implemented features match the original specification.
- Validate that tests pass and coverage meets the project's stated requirement (do not invent a target).
- Confirm the implementation follows the technical plan.
- Run after-implementation hooks per section 1.
- Report the final status with a summary of completed work.

Done when every required task is complete and marked `[X]` after verification, the implementation is validated against the spec, plan, and test requirements, hooks were run or skipped per section 1, and completion was reported. A later convergence check in [system-verification](../../system-verification/SKILL.md) may append remaining work as a new phase; implement those tasks the same way.
