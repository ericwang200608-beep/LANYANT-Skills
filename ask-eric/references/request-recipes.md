# Prompts worth copying

Swap in the real paths, skills, and done checks. Informal wording works.

## Understand

- `ask-eric read <thread>. restate the underlying issue in your own words, in plain english.`
- `technical-writing to restate the request <long or messy ask>`
- `process-improvement to sharpen the prompt <the prompt you're about to send>`
- `ask-eric investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.`
- `use codebase-investigation for mechanics to understand <subsystem>. then use codebase-investigation for historical reasons to find out why it broke recently.`
- `session-continuity to recall prior work my work on <topic> from last week, then read <issue>.`
- `codebase-investigation to teach the reasoning me why you implemented it this way and not <other way>. what did you trade off?`
- `ask-eric take over this branch. read the decision log, find what's done, and continue. don't redo finished work.`

## Build

- Bug: `ask-eric <symptom>. repro first, then fix and verify.`
- Bug in an app: `ask-eric repro this with the project verification harness. if it repros on main, fix it and show me a video as proof.`
- Bug with a cheap test: `ask-eric repro <bug> first. if there's a cheap test path, test-driven-development it. then fix and rerun.`
- Feature: `ask-eric add <behavior>. <current output> stays byte-identical. verify both.`
- Refactor: `ask-eric move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.`
- Perf: `ask-eric <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.`

## Design and plan

- `ask-eric prototype a few options for <feature>. take screenshots or videos for me to compare.`
- `ask-eric we need <feature>. technical-design it first, and answer open questions with prototypes. let me review before proceeding.`
- `ask-eric write a tutorial for how i would use <new package> first. then codebase-investigation to teach the reasoning me why it beats the current one.`
- `ask multi-agent-delivery for competing independent attempts for a second opinion on this thread and our approach.`
- `ask-eric turn this design into a plan. small verifiable PRs, each with its own verification steps.`
- `ask-eric plan the migration of <library> to <target>. small verifiable PRs. the result must match the original exactly, bugs included.`

## Review and ship

- `adversarial-review the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` Read the Dropped list too.
- `verification-harness to create formal verification prove <property> holds in <module>, even when <steps> interleave or retry.` After merges or refactors in that code: `verification-harness to maintain formal verification`.
- `multi-agent-delivery for parallel verification check every package under <dir> against its check script. one worker per package. one report.`
- `ask-eric open the pr. small ordered commits, evidence in the description.`
- `ask-eric babysit this pr. get it green.` For status only: `ask-eric check on pr <number>. anything outstanding?`
- `ask-eric land the stack.`

## Away and back

- `ask-eric im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. don't ask me before committing. an authorized bounded repeat-until loop until done. if you're truly stuck after a few hours, stop and write up why.`
- `session-continuity to read the decision log catch me up on what you did last night.` Read its Attention section first.
- `session-continuity to catch up` catches you up on this chat since your last message and lists every call that waits on you.
- `ask-eric full autopilot on this queue. each item is independent.`
- `ask-eric autopilot these changes, but don't merge. i'll land them.`
- `process-improvement to reflect on the run capture what we learned so the next run doesn't repeat it.` Approve only edits that change a future decision.
- `technical-writing to restate plainly` restates the last reply in plain words.

## Authorization boundary

Every example inherits the current authorization. An unattended run never grants external messages, tracker writes, merges, production changes, paid resources or destructive actions. A request to land a stack needs explicit merge authorization and independent verification at its current head. Preserve a missing-capability blocker when a requested operation cannot run.
