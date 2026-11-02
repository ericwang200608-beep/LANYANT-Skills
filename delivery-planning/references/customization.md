# Workflow and customization contracts

Read this when the project needs preset/template layers, extension hooks, resumable workflows, or toolkit installation mechanisms. These are explicit capabilities with dependencies, not permissions. Follow [operating rules](../../ask-eric/references/operating-rules.md).

## Template layers and feature paths

The canonical `project-environment/scripts/common.py` resolver is executable Python 3. It resolves the active feature from `LANYANT_FEATURE_DIRECTORY` or `.lanyant/feature.json`; an invalid explicit override fails rather than falling back to another project. The pointer has `{"feature_directory": "specs/001-feature"}`. Keep one authoritative specification and task file. Preserve scoped feature layouts.

For each template, the precedence is project `.lanyant/templates/overrides/`, enabled presets in registry priority order, enabled extensions, project `.lanyant/templates/`, then the bundled sibling skill's assets. Replacement, prepend and append manifest layers retain their defined order. Invalid manifest structure, unsafe identifiers, missing replacement bases or an unavailable YAML parser are errors; never silently ignore a higher-priority invalid layer. The common resolver includes these checks. Its executable entry point is `python3 <suite>/project-environment/scripts/resolve_template.py <template-name> --json`; JSON-format manifests need no YAML package. Avoid assuming that a template install provides a workflow engine.

## Lean feature depth

Use the linked lean specification, plan, tasks and implementation procedures when an explicitly small feature benefits from fewer artifacts. Keep the same authoritative spec and task state. Lean mode still enforces agreed acceptance, permission boundaries and risk-based red/green regression checks. Principles remain governing constraints.

## Before and after hooks

1. Inspect the project's actual hook configuration, if any. A conventional optional file is `.lanyant/extensions.yml`, with `hooks.before_<phase>` and `hooks.after_<phase>` lists. Absence means no hooks. An unreadable or invalid file is a reported configuration failure, not evidence that no mandatory hook exists.
2. Filter entries with `enabled: false`; missing `enabled` means enabled. Retain command identifier, description, prompt, optional flag and condition as data.
3. An empty/null condition permits dispatch. A non-empty condition needs an actual supported evaluator. Do not evaluate arbitrary text as shell or invent a truth value. If no evaluator exists, mark that hook environment-blocked; a mandatory hook blocks dependent completion.
4. For an optional hook, show its purpose and proposed action. Existing authorization determines whether it may execute; optional does not mean automatically approved or that the agent must ask again for already-authorized work.
5. For a mandatory hook, resolve the identifier to an installed action, verify its authorization and inputs, actually invoke it and wait for its result. Record the command, outcome and evidence. Printing `EXECUTE_COMMAND` or naming a skill never executes it. A missing runner, mapping, tool or authorization is an explicit blocker; a failed required pre-hook stops dependent work. Continue unaffected work.
6. Run post-hooks only after the corresponding phase outcome, in their declared order. Distinguish phase implementation from post-hook completion. Report failed or unexecuted post-hooks accurately. Hooks cannot grant tracker writes, messages, commits, merges, production access or paid resources.

No generic YAML HookExecutor is bundled in this suite. The agent can dispatch an unconditional installed action using its real tools. Conditional evaluation and unattended execution require a compatible external runner and remain unverified unless exercised there.

## Resumable specification-to-implementation workflow

The full sequence is specification, specification review gate, plan, plan review gate, tasks, implementation. A gate records approve/reject and its owner; reject aborts that dependent run. Existing user authorization and acceptance determine which gates require a new business decision. Do not turn every technical stage transition into a repeated permission request.

Before a run, declare the inputs, integration/runtime, each step's type and expected output, dependencies, stopping predicate and authoritative record. After each completed step record its output and candidate version. On resume validate those outputs and reuse still-applicable evidence; rerun only invalidated steps and their dependents. A failed command is not a completed step. Keep outputs and state scoped to that run; nested workflow inputs/outputs must be explicit so child state cannot overwrite parent intent.

A compatible engine may support command, shell, gate, condition, loop, workflow and additional declarative step types, checkpoint identity, overlays, event emission and resume. This suite provides the engineering procedures and state contracts, not an implementation of that general-purpose persisted workflow engine. Without a real runner, use an authorized foreground step sequence with the same record and state accurately that automated resume and scheduler behavior are unverified.

## Toolkit lifecycle and platform mechanisms

The following are distinct platform capabilities. Inspect the target runtime before claiming equivalence. The suite does not ship a replacement command-line distribution or remote catalog service.

| Capability | Required behavior and completion evidence | Available local path or remaining dependency |
|---|---|---|
| Initialize | Choose verified project root, integration, templates, naming and numbering; preserve existing files; record selected options | Environment setup and bundled templates; no universal installer binary |
| Check | Detect required commands, interpreters, authentication and runtime capabilities; distinguish missing, installed and executable | Actual `command -v`, tool help/version and a meaningful smoke run |
| Version | Report exact installed package/runtime version and source candidate, not a guessed latest release | Runtime's version command and suite delivery manifest |
| MCP configuration | Inspect server transport, command/URL, auth and scoped project configuration; prove a real connection | Depends on the selected runtime's actual connector mechanism |
| Self update | Resolve trusted update, preserve configuration, install atomically, verify and allow recovery | No self-updater bundled; do not claim one |
| Extensions | Discover/validate manifest, compatibility, dependencies, commands/hooks, enable/disable state, safe install/remove and conflicts | Manifest/template resolver supports reading installed layers; catalog/install management requires a real manager |
| Presets | Validate identifiers, priority and compositional template behavior, preserve customization and registry | Executable template resolver; lifecycle installation/remote resolution not bundled |
| Integrations | Detect selected runtime, invocation separator, context file target and command capability; validate before dispatch | Harness adapter and managed agent-context helper; no generated integration package installer |
| Workflows | Validate steps/inputs, execute gates and commands, persist and resume identity without replaying completed work | Foreground procedure above; general engine remains a dependency |
| Bundles | Resolve a versioned set of extensions/presets/workflows, compatibility and lock state as a unit | No bundle package manager bundled |
| Artifacts | Identify typed artifact, owning feature/run, version, location, freshness and producer; preserve reference identity | Existing authoritative task record; no standalone artifact registry API bundled |
| Events | Record ordered lifecycle events with run/step identity, payload schema and failure; real subscribers must acknowledge | Evidence record; no event transport/dispatcher bundled |
| Community submission | Read submission, validate public repository/manifest/license/release/semver/checklists, deduplicate ID, update catalog and docs together, review diff and publish only if authorized | [Complete catalog maintenance procedure](community-catalog.md); target catalog repository and access are required |

Record every missing mechanism as partial, unverified or environment-blocked according to its actual state. A written table is not execution evidence. Capability-specific verification must exercise that capability; structural suite validation is not an integration or end-to-end test.
