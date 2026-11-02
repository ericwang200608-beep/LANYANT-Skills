# Set up report intake and reproduction

Read when the user explicitly requests installing or changing recurring intake/reproduction. This procedure prepares two dormant automations and enables them only after thread-safety verification. Use [harness adapters](../../multi-agent-delivery/references/harness-adapters.md) and the native automation tool supported by the current host. A platform-specific editor, trigger, identity, or integration without an equivalent remains blocked. Never create a substitute schedule or duplicate automation silently.

## 1. Install and verify operational files

1. Resolve the target repository and user-owned configuration directory. Copy source-managed intake and reproduction procedures and templates to a stable project-local location only when installation is in scope.
2. Preserve destination-only files, feature maps, routing maps, unrelated settings, and secrets. Review differences in existing managed files and merge local changes rather than overwrite them. Ambiguous ownership blocks replacement.
3. Verify source-thread intake, real-surface reproduction, control adapter, feature-map template, routing example, and the configuration example are present and their links resolve.
4. Make the LANYANT investigation, TDD, technical-writing, engineering-principles, bug-diagnosis, and harness-adapter procedures available to a fresh project-scoped agent. Do not count dependencies loaded only in the installing agent's context.
5. Validate any settings changes. If project-scope installation is unavailable or a dependency does not resolve, record the gap and leave automation disabled.
6. Live prompts use stable project-relative operational paths, never a plugin cache or this installer's local path. If remote checkouts require committed files, verify those files exist on the configured branch. Do not commit or push unless authorized.

## 2. Create user-owned configuration

Copy [configuration example](../assets/intake-configuration.example.yaml), [routing map](routing.example.md), and [feature map](../../bug-diagnosis/assets/feature-map.template.md) to user-owned paths outside source-managed files. Refreshes never overwrite them. Prefer secret-free repository files for remote runners. Reference a file only after confirming that the actual runner can read it; otherwise include only the needed nonsecret settings in the reviewed prompt. Fill a feature-map section for each user-facing feature; describe user paths and states, not frozen implementation internals.

## 3. Resolve required choices

Resolve source location id, optional operations/status location, repository URL and default branch, triage identity, tracker type/team/project/labels/intake status, tracker adapter actions, routing-map path, control adapter, feature-map path, status markers, PR URL format, polling and effort budgets, and supported model for each triage/reproduction/code/media role. Use only model choices the host actually exposes.

Source coordinates, identity, repository, tracker adapter, control adapter, and feature map must be explicit. Fail setup if any stays ambiguous. Keep credentials in the secret manager or environment; never in YAML, prompts, examples, logs, or committed files. Apply [technical writing](../../technical-writing/SKILL.md) to names and prompt shims.

## 4. Check integrations

Triage requires source-thread read/reply, attachment metadata and media reads, plus tracker search/read/create/update and compensating close/cancel. Reproduction requires source-thread read/reply, optional operations-message post/edit, repository and history read, draft-PR creation when authorized, and the completed control adapter. Use documented connectors. A narrow environment token may fill an explicit connector gap, but never expose its value. Missing capabilities fail the corresponding action closed.

## 5. Prepare routing

Replace every routing placeholder with confirmed organization values. Owner mentions stay off by default. Allow only a configured feature owner or strongly evidenced regression author, never a broad on-call group. Without routing configuration, classify conservatively and name no guessed destination or owner. Never cross-post a report.

## 6. Verify the real-surface adapter

Read [control adapter](../../bug-diagnosis/references/control-adapter.md) and the completed feature map. Prove that it can start the app, navigate every mapped feature, exercise declared states, inspect without forcing results, capture screenshots, record and stop video, and clean its own processes and temporary data. Missing ability keeps reproduction disabled.

## 7. Prepare the two live automations

First inspect existing automations through the host's supported API. Update the intended existing automation and preserve unrelated fields. If first creation was requested, prepare one at a time using the native reviewed creation flow. Do not use undocumented backend endpoints or bypass the host's editor/approval rules.

The triage prompt must name its exact operational file, new top-level report trigger, source location, source-thread-only reply rule, tracker adapter, cause tracing, evidence inspection, conservative classification, dedupe, create-only-clear-new-bugs condition, configured marker and optional tracker link, and no top-level source messages.

The reproduction prompt must name its operational file, matching trigger and source location, repository and branch, source-thread-only rule, tracker/control/feature-map requirements, trusted triage-identity marker wait, exact-symptom reproduction twice through the real UI, evidence capture, existing-fix verification, and optional bounded fix plus draft PR only under existing authorization and passing proof. Never post a source root message.

Confirm authentication, readable operational/configuration files on the runner's branch, integrations, complete prompts, supported models, budgets, and readiness through the host's own workflow. For an editor-only host, give a concrete per-automation checklist and leave activation pending. Do not create replacement duplicates.

## 8. Test thread safety before activation

Use a harmless test report in an explicitly authorized test source. Confirm the runner reads the exact committed operational/config files where the platform requires them. Verify all seven assertions:

1. Triage freezes the root thread coordinate and posts exactly one verdict as a reply.
2. The verdict contains exactly one configured marker.
3. Reproduction trusts the marker only from the configured triage identity.
4. Reproduction retains the same immutable source coordinates.
5. No source top-level message is produced.
6. Delegated workers cannot invoke source or tracker write actions.
7. Missing coordinates, deleted parent, or failed preflight cause no post and no tracker issue.

Enable normal traffic only after all seven pass and activation is authorized. Record missing trigger/editor/connector/model capabilities and unexecuted tests in the authoritative configuration task.
