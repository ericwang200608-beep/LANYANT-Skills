# Skill authoring

Use when creating or modifying any skill: a project skill, a personal or team mode skill, or a LANYANT suite skill. **You own the skill's voice.**

Read [writing-for-agents.md](writing-for-agents.md) and [skill-mechanics.md](skill-mechanics.md) before drafting.

## Procedure

1. **Locate.** Find the skill's home: the project skills location, the user skills location, or the suite build copy (see [Maintaining the LANYANT suite](#maintaining-the-lanyant-suite)). Never edit a skill inside an installed plugin, package, or marketplace cache; copy it to a project or user location first. Read the whole existing skill, its references, and any skill that links to it.
2. **Draft.** Write or edit `SKILL.md` and its files:
   - Frontmatter has `name` (equal to the directory name, lowercase kebab case) and `description` (what it does plus the trigger situations, one YAML scalar, at most 1024 characters). Choose model-invoked or user-invoked per [skill-mechanics.md](skill-mechanics.md).
   - The body says when to use, the inputs to read, the numbered procedure, the verification required, the outputs and where state is updated, the completion criteria, and what the skill does not authorize. Leave out sections that would be empty.
   - Keep the body under 500 lines. Disclose depth into `references/*.md`, each linked from `SKILL.md` with when to read it. Executable helpers go in `scripts/`, templates in `assets/`.
   - Delegate to other skills by relative path. Do not restate them.
3. **Validate.** Run every check in [Validate](#validate). Fix and rerun until all pass.
4. **Test cases if structural.** When the change alters a procedure, a gate, a routing, or a trigger, run the [behavior test](#behavior-test). Skip it for subjective output (a mode skill's voice, a tone change); vibe-check with the user instead.
5. **Iterate.** Revise from the test results and the user's feedback, then repeat steps 3 and 4.
6. **Deliver.** Commit when commits are in scope. Opening a PR or pushing follows [pr-delivery](../../pr-delivery/SKILL.md) and needs authorization for that action. For a suite skill, finish with [Maintaining the LANYANT suite](#maintaining-the-lanyant-suite).

When in doubt, delete. Keep only prose that changes a decision. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config) instead of restating them. A workflow you keep hitting that no skill captures: propose a new skill.

**Reply:** summary of the skill, key design decisions, validation notes (each check and its result), and behavior-test results or the reason the test was skipped.

## Validate

Run these on every touched skill:

- Frontmatter parses as YAML, starts on line 1, and has `name` and `description`. `name` matches the directory. `description` is at most 1024 characters.
- Every relative link and every file the skill names exists. Check links that point into sibling skills too.
- Every cross-skill link resolves to a real `SKILL.md`.
- `SKILL.md` is under 500 lines.
- Scripts keep their shebang and executable bit, and any tests shipped with them pass.

A quick link check from the skill directory:

```bash
grep -oE '\]\([^)#]+' SKILL.md references/*.md 2>/dev/null | sed 's/.*](//' | grep -v '^http' | sort -u | while read -r p; do [ -e "$p" ] || [ -e "references/$p" ] || echo "missing: $p"; done
```

Links inside `references/*.md` resolve relative to `references/`; check those from that directory when the quick check reports them. If the environment ships its own skill validator, run it as well. Record each check and its result.

## Behavior test

1. Write 2 to 4 realistic task prompts the skill should handle, covering its main branches, and at least one prompt it should not handle.
2. For each prompt, spawn a fresh agent that has the skill installed or is pointed at its path, with no other context from this session (see [harness-adapters.md](../../multi-agent-delivery/references/harness-adapters.md)). Tell it not to perform outward-facing or irreversible actions. Where the change edits an existing skill, also run the same prompt against the previous version.
3. Read each run's transcript or report. Check that the agent reached the skill, followed each numbered step, met the completion criteria, and stopped where the skill says to stop. A report is a claim; check the files or output it produced.
4. Record per prompt: expected behavior, observed behavior, pass or fail.

If agent spawning is not available, record "behavior test not run: no fresh agent available" and label the skill change unverified for behavior. Do not substitute a self-read of the skill for a fresh run.

## Tune a description

Use when a skill exists but did not trigger when it should have, or triggers when it should not.

1. Write 5 to 10 prompts that should trigger it and 5 to 10 near-miss prompts that should not, phrased the way users actually ask.
2. Rewrite the description by the pointer rules in [writing-for-agents.md](writing-for-agents.md#context-pointers): front-load the leading word, one trigger per branch, cut identity the body already carries.
3. For each prompt, ask a fresh agent with the skill list visible which skill it would open, or run the prompt and see which skill loads.
4. Keep the version with the fewest misses on both sets. Record the before and after counts.

## Maintaining the LANYANT suite

Changes to any LANYANT suite skill, including this one, go through this procedure. Never edit the installed copy directly.

1. **Edit in a build copy.** Work in the suite's maintenance repository build tree (a copy of the full suite), never in the installed or published location. Keep suite rules: English, imperative voice, no em dashes, frontmatter with only `name` and `description`, relative sibling links as `../<name>/SKILL.md`, shared rules linked from [operating-rules.md](../../ask-eric/references/operating-rules.md) rather than restated.
2. **Run the suite validator.** Run the validator that lives in the maintenance repository against the whole build tree, not only the touched skill. It checks structure (frontmatter, required sections, body length, reference files linked from `SKILL.md`), links (every relative link and sibling link resolves), names (directory names match `name`, siblings are named exactly as the router lists them), and runtime independence (no runtime names, install paths, or commands from outside the suite that an installed copy could not resolve). If the validator is missing or fails to run, run the checks in [Validate](#validate) across the suite by hand and record "suite validator not run" as a gap.
3. **Behavior-test with fresh agents.** Run the [behavior test](#behavior-test) with agents that have only the build copy of the suite installed or pointed at, using prompts that reach the changed skill through the router as well as directly.
4. **Record.** Note in the maintenance repository's change record what changed, the validator output, and the behavior-test results, following [operating rule 3](../../ask-eric/references/operating-rules.md#3-evidence-record).
5. **Sync.** Copy the validated build tree to the installed or published location only with the suite maintainer's authorization for that sync. After syncing, confirm the installed copy matches the build copy (for example `diff -r`).
