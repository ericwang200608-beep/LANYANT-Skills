---
name: project-environment
description: Set up or complete project foundations from an established technical plan, including repository conventions, development startup, automated checks, test data, and development, test, and production environment configuration. Use to prepare engineering foundations before business feature development or to address environment gaps in an existing project. Also use to author or test local toolkit extension and preset packages.
---

# Development, Test, and Production Foundations

Inspect the project's starting state, establish its structure, dependencies, and configuration, then verify actual runtime results. Deliver a project that starts, repeatable checks, and clearly separated development, test, and production environments.

## 1. Inspect the current state and technical plan

Read what exists rather than assuming:

- The technical plan's stack, architecture, and directory structure.
- Existing environment tasks and their dependency order; read the data model, interface contracts, technical research, and quickstart instructions when available.
- `git remote -v` and Git configuration to identify the repository and remote addresses.
- Root `AGENTS.md` and `CLAUDE.md`, and existing issue-tracking and documentation conventions.
- Dependency manifests, lockfiles, run scripts, continuous integration configuration, and deployment configuration.
- Existing glossaries and architectural decisions; for multiple business contexts, read the portions relevant to this work.

If a glossary or architectural records do not exist, continue without creating empty files merely to fill a directory. Use existing business terminology in outputs. Explicitly surface conflicts with architectural decisions instead of silently overriding them.

Summarize what exists and the actual gaps. Retain established choices and ask only for missing information that changes execution. If there is no actionable technical plan, establish the necessary stack and deployment target first without independently redesigning the entire architecture.

## 2. Configure the repository and collaboration conventions

Use the place where the project actually tracks work. Keep an existing issue tracker. If none has been chosen, recommend the platform matching the remote repository, or use local Markdown records in the repository. For other trackers, record the user's existing workflow.

For a remote issue tracker, verify that the repository is accessible. If no remote is connected, configure a user-provided or verified address; do not guess one. Initialize Git when a new project needs version control. Preserve existing history and remote settings in an existing repository.

Default to a single business context: a root glossary and a shared architectural decision directory. Consider a per-context layout only when the project actually has multiple packages and contexts. Record documentation locations and reading conventions; save specific terms and decisions when they arise.

Update the project's existing collaboration instructions and relevant sections in place, without duplicate additions or overwriting surrounding user content. If no instructions file exists and one is genuinely needed, determine which kind to create. Reuse existing task labels. Do not introduce a label system when no triage workflow is in use.

Add only conventions needed for this environment setup. Do not make other skills or a new workflow prerequisites.

## 3. Initialize project structure and dependencies

Create the project structure according to the technical plan, initialize dependencies for the chosen language and framework, and configure applicable linting and formatting tools. In an existing project, fill only the gaps.

Reuse the project's tools, components, and configuration first, then consider standard libraries, platform capabilities, and installed dependencies. If a simple approach already meets the need, do not add another dependency or wrapper.

Identify the package manager from lockfiles and configuration, and use the project's installation method. Prepare database connections and migration tooling, basic routing, error handling, logging, and environment configuration management as needed. These are foundations, not a mandate to implement complete business features.

Create or verify ignore rules based on the actual stack:

- Check `.gitignore` for Git repositories.
- Check `.dockerignore` when building containers.
- Check the corresponding ignore configuration when using linting or formatting tools.
- Check publishing and infrastructure-tool ignore rules only when publishing packages or using those tools.

When an ignore file exists, add only missing essential rules. Otherwise, create it for the actual stack. Handle dependency directories, build artifacts, caches, logs, and local secret configuration appropriately. Retain lockfiles that belong in version control and configuration examples without real secrets.

## 4. Configure repeatable checks

Establish or reuse clear installation, startup, build, and test entry points, using the project's actual tools. Include formatting, linting, and type checks where applicable.

When pre-commit checks are needed and appropriate, type checks and tests may follow staged-file checks. Reuse an existing mechanism. If scripts are missing, state that explicitly rather than adding steps that call nonexistent commands or claiming tests passed.

Configure automated builds and tests on the project's continuous integration platform. Reuse local check commands and declare required runtimes, dependencies, and test configuration. Execute the initial configuration once and provide the result. If configuration is written but cannot be triggered, mark remote execution as unverified.

If business features do not yet exist, establish a minimal environment check that verifies startup and required service connections. Do not add empty tests just to produce a passing result. Passing environment checks does not establish business acceptance.

## 5. Separate development, test, and production environments

Implement the purpose, access points, and configuration of the three environments according to the established deployment plan: development for daily changes, test or staging for rehearsals, and production for actual use.

Separate connection configuration, credentials, and business data by environment. Provide configuration examples without real secrets. Keep real secrets in the target platform's secret settings or the project's existing management mechanism, not in the repository or handoff documentation.

Prepare test accounts and sample data, with a repeatable initialization or reset method. Before execution, verify that the target is a development or test environment. Sample initialization must not overwrite production data.

Configure the target runtime within existing authorization, and verify deployment entry points and necessary connections. Creating paid resources, modifying real production environments, or enabling external access requires corresponding authorization. Use authorization already given; when it is missing, complete unaffected preparation and identify the remaining work.

Environment configuration files do not establish that an environment exists. Distinguish configured, started, verified, and awaiting creation. Production readiness does not imply authorization to release a business version.

## 6. Prepare logging, backups, and monitoring

Configure basic logging and necessary health checks according to the technical plan. Identify where to inspect startup failures, application errors, and runtime status. Avoid logging secrets or sensitive data.

For persistent data, implement the backup and recovery arrangements agreed for this stage: what is backed up, how it runs, where it is stored, and who is responsible. Verify the recovery path using test data. If it has not been rehearsed, state that explicitly; backup configuration is not verified recovery.

Configure necessary status or failure monitoring and identify notification destinations. Mark portions lacking available accounts, resources, or authorization as pending, rather than inventing an enabled status.

## 7. Run verification and deliver

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Execute work in dependency order, verifying each completed portion before proceeding. If a step fails, stop downstream operations that depend on it and preserve the error and context. Unaffected work may continue.

Inspect actual results directly. Do not infer environment usability from agent reports, file modification times, or successful compilation:

- Actually install dependencies and start the project; inspect the process and application entry point.
- Run the build and applicable checks; read their output and exit results.
- Check required service connections, test accounts, and sample data.
- Check that test and production environments point to separate configuration and data.
- Inspect actual continuous integration runs and the status of configured logging, monitoring, and backups.

Prefer preserving repeatable checks as simple commands or scripts that others can rerun. Mark steps not executed as unverified. Never rewrite known failures as passes.

Update startup and validation instructions according to project documentation conventions. Include prerequisites, installation and startup commands, how to obtain configuration, check commands, expected results, and environment locations. Record completed environment tasks and retain outstanding items with their reasons.

Deliver a project that starts, repeatable checks, and separate environments. Completion means actual startup and check results meet this iteration's requirements, and the locations and status of test and production systems can be clearly explained. If only preparation files exist and environments have not been created or started, report partial completion rather than claiming all environments are ready.

For an environment-only request, stop when this stage is complete. Environment preparation alone does not authorize business feature development, commits, pushes, or a production release.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Conditional environment procedures

Read [setup](references/setup.md) when selecting tracker and domain-document conventions. Use the appropriate adapter: [GitHub](references/issue-tracker-github.md), [GitLab](references/issue-tracker-gitlab.md), or [local files](references/issue-tracker-local.md), plus [labels](references/triage-labels.md) and [domain document placement](references/domain-docs.md). Reuse the project's existing choices.

Use [pre-commit setup](references/pre-commit.md) when requested; [exercise scaffolding](references/scaffold-exercises.md) for course repositories; and [a wizard](references/wizard.md) with [the shell template](assets/setup-wizard.template.sh) only for steps a human must perform. Run agent-accessible work directly.

Read [Git initialization](references/git-initialize.md), [feature branches](references/git-feature.md), [remotes](references/git-remote.md), [validation](references/git-validate.md), and [commit hooks](references/git-commit.md) when that specific operation is in scope. Python 3 versions live in `scripts/initialize_repo.py`, `scripts/create_new_feature_branch.py`, `scripts/git_common.py`, and `scripts/auto_commit.py`. Auto-commit is disabled by default. Configuration never authorizes committing unrelated user changes; stage an inspected scope and preserve existing changes.

For a requested shell hook use [Git guardrails](references/git-guardrails.md) and `scripts/block-dangerous-git.sh`, the hardened default. It requires Python 3 and the adjacent `scripts/block-dangerous-git.py` parser, handles static quoted tokens, Git global options such as `-C` and equivalent force flags, and fails closed if the interpreter, JSON or tokens cannot be read. This is a hook adapter, not a universal command sandbox. Apply it only in a runtime that actually supports the hook; otherwise record the enforcement gap and follow [the harness adapter](../multi-agent-delivery/references/harness-adapters.md).

Resolve a composed template with `python3 <this-skill>/scripts/resolve_template.py <template-name> --json`. It shares the canonical resolver used by plan and task setup. JSON-format preset manifests work with the Python standard library; other YAML syntax requires PyYAML. Invalid or missing declared layers fail rather than falling back to unrelated content.

For a requested extension or preset authoring task, follow [extension and preset authoring](references/extension-authoring.md), with the complete starter packages and lifecycle self-test linked there. Treat self-test packages as isolated test assets. Document resolution is supported by the Python helper; catalog installation and command registration require an actual target-runtime manager and remain blocked when it is unavailable.
