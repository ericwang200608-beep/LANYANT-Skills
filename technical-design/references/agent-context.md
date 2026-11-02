# Update Coding Agent Context

Refresh the managed LANYANT section inside the active coding agent's context/instruction file (e.g. `CLAUDE.md`, `.github/copilot-instructions.md`, `AGENTS.md`).

## Behavior

The script reads the agent-context extension config at
`.lanyant/extensions/agent-context/agent-context-config.json` (preferred, Python standard library) or `agent-context-config.yml` in the same directory (PyYAML required for YAML syntax beyond JSON) to discover:

- `context_file` ,  the path of the coding agent context file to manage.
- `context_files` ,  optional project-relative paths for multiple coding agent context files. When non-empty, the script updates each listed file and the list takes precedence over `context_file`.
- `context_markers.start` / `.end` ,  the delimiters surrounding the managed section. Defaults to `<!-- LANYANT START -->` and `<!-- LANYANT END -->` when the field is missing.

It then creates, replaces, or appends the managed block so that the section points at the most recent plan path when one can be discovered (any `plan.md` under `specs/`, including nested scoped layouts such as `specs/<scope>/<feature>/plan.md`).

If `context_files` and `context_file` are empty, the command reports nothing to do and exits successfully. Context file paths must stay project-relative; absolute paths, Windows drive paths, backslash separators, and `..` path segments are rejected.

## Execution

- **Bash**: `python3 <this-skill>/scripts/update_agent_context.py [plan_path]`
- **PowerShell**: `python3 <this-skill>/scripts/update_agent_context.py [plan_path]`

When `plan_path` is omitted, the script auto-detects the most recently modified `specs/**/plan.md` (searched recursively, so nested scoped layouts are discovered).

## Portable configuration

```json
{"context_files": ["AGENTS.md"], "context_markers": {"start": "<!-- LANYANT START -->", "end": "<!-- LANYANT END -->"}}
```

Run from the project root. A missing configuration or target is a reported no-op, not proof of a refresh. Invalid configuration, an unavailable required YAML parser or an unsafe target is a nonzero failure. The current `.lanyant/feature.json` plan pointer takes precedence over the latest-plan fallback. Existing text outside the managed block is retained.

Before writing any configured target, preflight every target's managed markers. An incomplete, duplicate or reversed marker pair fails closed and leaves every target's original bytes unchanged; do not guess where human-authored rules end. Repair markers only as an explicit scoped edit.
