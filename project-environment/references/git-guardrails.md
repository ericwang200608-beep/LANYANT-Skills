# Setup Git Guardrails

Sets up a PreToolUse hook that intercepts and blocks dangerous git commands before Claude executes them.

## What Gets Blocked

- `git push` (all variants including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

When blocked, Claude sees a message telling it that it does not have authority to access these commands.

## Steps

### 1. Ask scope

Ask the user: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Copy the hook script

The bundled entry point is [block-dangerous-git.sh](../scripts/block-dangerous-git.sh) and its required adjacent parser is [block-dangerous-git.py](../scripts/block-dangerous-git.py). Python 3 is required. The parser uses only standard-library JSON and shlex; jq is not required. Missing Python, invalid JSON or invalid static shell tokens fail closed with exit 2.

Copy both files together to the target hook directory based on the already-authorized scope:

- **Project**: `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/hooks/block-dangerous-git.sh`

Keep `block-dangerous-git.py` adjacent to the shell entry point and make the shell entry executable with `chmod +x`. Do not install a shell wrapper without its parser.

### 3. Add hook to settings

Add to the appropriate settings file:

**Project** (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Global** (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into the existing `hooks.PreToolUse` array. Don't overwrite other settings.

### 4. Ask about customization

Apply an already-requested policy customization to the copied parser; ask only if the desired policy is missing. Keep the documented dangerous-operation coverage and verify equivalent flags and quoted static tokens. The hook recursively parses static strings passed through shell `-c`/combined flags without executing them, with excessive nesting failing closed. It does not evaluate aliases, dynamic expansions or arbitrary shell programs and is not a universal shell sandbox.

### 5. Verify

Run a quick test:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

Should exit with code 2 and print a BLOCKED message to stderr.


Also test `git -C /tmp reset --quiet --hard HEAD`, `git -C /tmp clean -df`, `git -C /tmp checkout -- '.'`, and `git -C /tmp branch -d -f branch` (all block), plus `git -C /tmp status` (allow). Run the same tests without jq. Runtime registration is a separate integration check: a subprocess test does not prove the host invokes its PreToolUse hook.
