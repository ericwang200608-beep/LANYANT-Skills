# Auto-Commit Changes

Commit only the reviewed, already-staged scope after an authorized phase completes.

## Behavior

This command is invoked as a hook after (or before) core commands. It:

1. Determines the event name from the hook context (e.g., if invoked as an `after_specify` hook, the event is `after_specify`; if `before_plan`, the event is `before_plan`)
2. Checks `.lanyant/extensions/git/git-config.yml` for the `auto_commit` section
3. Looks up the specific event key to see if auto-commit is enabled
4. Falls back to `auto_commit.default` if no event-specific key exists
5. Determines the commit message based on `commit_style` (see below)
6. If enabled and there are uncommitted changes, runs `git commit` on the already-staged scope. The helper never stages unrelated files

## Commit Message Styles

Controlled by the `commit_style` key in `.lanyant/extensions/git/git-config.yml`:

- **`fixed`** (default): use the per-command `message` if configured, otherwise a generic `[LANYANT] Auto-commit <phase> <command>` message.
- **`conventional`**: inspect the actual changes (`git diff` / `git status`) since the last commit and generate a single-line [Conventional Commit](https://www.conventionalcommits.org/) message (`type(scope): subject`, e.g. `feat: add OAuth specification` or `docs: update implementation plan`) that accurately summarizes the change. Write this message to a temporary file and pass the file's path to the script (see Execution below). The configured `message` values are ignored in this mode.

## Execution

Determine the event name from the hook that triggered this command, then run the script:

- **Bash**: `<this-skill>/scripts/auto_commit.py <event_name> [--message-file <path>]`
- **PowerShell**: `<this-skill>/scripts/auto_commit.py <event_name> [-MessageFile <path>]`

Replace `<event_name>` with the actual hook event (e.g., `after_specify`, `before_plan`, `after_implement`). Only pass a generated message when `commit_style: conventional` is configured ,  first check `.lanyant/extensions/git/git-config.yml` for the value of `commit_style`:

- If `conventional`: inspect the diff and generate a Conventional Commit message. **Do not interpolate the generated message directly into a shell command string** ,  its content is derived from repository changes and may contain characters (quotes, `$(...)`, backticks) that a shell would execute or that would break command quoting. Instead, write the message to a temporary file using your file-editing tool (not a shell `echo`/`printf`), then pass that file's path via `--message-file <path>` (Bash) or `-MessageFile <path>` (PowerShell).
- If `fixed` or absent: run the script with just `<event_name>`; it uses the configured/static message.

## Configuration

In `.lanyant/extensions/git/git-config.yml`:

```yaml
# "fixed" (default) uses the messages below; "conventional" asks the agent
# to generate a Conventional Commit message from the diff instead.
commit_style: fixed

auto_commit:
  default: false          # Global toggle ,  set true to enable for all commands
  after_specify:
    enabled: true          # Override per-command
    message: "[LANYANT] Add specification"
  after_plan:
    enabled: false
    message: "[LANYANT] Add implementation plan"
```

## Graceful Degradation

- If Git is not available or the current directory is not a repository: skips with a warning
- If no config file exists: skips (disabled by default)
- If no changes to commit: skips with a message
- If `commit_style: conventional` is set and no generated message was supplied: fails with a clear error instead of silently falling back to the fixed message format

## Executable scope and message binding

Run `python3 <this-skill>/scripts/auto_commit.py <event_name> [--message-file <path>]` from the project root. Auto-commit stays disabled without an explicit configuration. Stage only the inspected, authorized files before invoking an enabled hook. The helper does not run `git add .`. Existing staged changes must be confirmed as part of that scope; do not include unrelated user changes. For `commit_style: conventional`, supply the literal message file; absence fails before committing. This hook never pushes.
