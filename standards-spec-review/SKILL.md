---
name: standards-spec-review
description: Two-axis review of the changes since a fixed point (commit, branch, tag, merge-base, or the working tree) on Standards (does the code follow this repository's documented coding standards, design documents, and the smell baseline?) and Spec (does the code do what the originating issue or specification asked for?), each run by a fresh independent agent and reported side by side without merging or reranking. Use when the user asks to review a branch, a PR, work in progress, "review since X", "is this built right and is it the right thing", or when another LANYANT skill calls for a standards-and-spec review of a diff. Not for hunting runtime bugs by breaking the change (use adversarial-review) or for full system verification with executed scenarios (use system-verification).
---

# Code Review

Review the diff between `HEAD` and a fixed point along two axes:

- **Standards**: does the code conform to this repository's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue or specification?

Both axes run as **parallel fresh-context agents** so they do not pollute each other's context. Then aggregate their findings. Start every agent with a fresh context window. Prefer running the whole review from a fresh session rather than the session that wrote the code: the same context reviewing itself is confirmation, not review.

## When to use

- A diff exists and the question is whether it is built right **and** is the right thing.
- A stage skill ([system-verification](../system-verification/SKILL.md), [feature-implementation](../feature-implementation/SKILL.md), [multi-agent-delivery](../multi-agent-delivery/SKILL.md)) asks for a standards-and-spec review of a change.
- Per task, to keep each diff small enough that the Spec axis has one clear spec; and once at the end of a branch against the branch point, to catch interactions between tasks that the per-task passes miss.

Use [adversarial-review](../adversarial-review/SKILL.md) to hunt bugs with run proofs, [bug-diagnosis](../bug-diagnosis/SKILL.md) when something is broken, and [refactoring](../refactoring/SKILL.md) when the whole codebase has drifted rather than one diff.

## Inputs to read

- The fixed point the user names. If none is named, look in the task or PR context; if still unresolved, ask. Do not guess.
- The originating issue or specification (step 2).
- Every repository file that documents how code should be written, and the design documents for the domains the change touches (step 3).
- [Smell baseline](references/smell-baseline.md): read it before step 4; its **Baseline text** section is pasted into the Standards brief.
- [Harness adapters](../multi-agent-delivery/references/harness-adapters.md): read it before step 4 to map "spawn a fresh agent" and "read-only agent" to your harness.
- [Operating rules](../ask-eric/references/operating-rules.md), especially sections 1, 3, 4, and 5.7.

## Requirements

- `git`.
- For fetching issues: the project's tracker CLI or connector (for example `gh issue view <n>`, `glab issue view <n>`). Detect absence with `command -v gh` or `command -v glab` and an auth check (`gh auth status`). When absent, use a path the user gives, or ask.

## Procedure

### 1. Pin the fixed point

1. Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, and so on). If they did not specify one, ask for it.
2. Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also record commit identities via `git rev-list <fixed-point>..HEAD`. The coordinator may inspect subjects to locate original issue references, but sends only hashes/ranges to independent reviewers; omit author diagnosis, repair and pass narratives from subjects/bodies as well as files.
3. If the user asks for an exact comparison of two commits, use `git diff <a> <b>` on the endpoints instead of substituting a merge-base comparison, and say so.
4. **Uncommitted work.** The three-dot diff excludes staged, unstaged, and untracked changes. Check `git status --porcelain`. When the work to review is uncommitted (for example an implementation that has not made an interim commit), include the working tree explicitly:
   - tracked changes since the merge-base: `git diff $(git merge-base <fixed-point> HEAD)` (covers committed, staged, and unstaged tracked changes);
   - untracked files: `git ls-files --others --exclude-standard`, passed to the agents as paths to read in full.
   Record in the report which form was reviewed. If the user prefers, commit first, review, then amend or add a fixup commit within authorized scope.
5. Before going further, confirm the fixed point resolves (`git rev-parse --verify <fixed-point>`) and the diff is non-empty. A bad ref or an empty diff fails here, not inside two parallel agents. An empty diff is reported as "no changes found for review", never as a pass.
6. Record the candidate: `git rev-parse HEAD`, plus "with working tree" when step 4 applied.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, and so on), fetched with the project's tracker workflow (the project's instructions file, such as `AGENTS.md` or `CLAUDE.md`, names it; otherwise use `gh` or `glab` per Requirements).
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature, or the project's existing specification or task record for this feature.
4. If nothing is found, ask the user where the spec is. If they say there is none, the **Spec** agent is skipped and the report says "no spec available". Never infer requirements from the code.

Read the full spec, not the developer's completion summary of it.

### 3. Identify the standards sources

1. Search the repository for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list. Also consider `AGENTS.md`, `CLAUDE.md`, `docs/`, style guides, linter and formatter configs (to know what tooling already enforces), and the project constitution if [project-principles](../project-principles/SKILL.md) maintains one.
2. Identify the domains the change touches and list the applicable design or architecture documents (for example a `design/` or `docs/architecture/` folder, ADRs). Read only the documents relevant to the affected domains, not every document for every change.
3. On top of whatever the repository documents, the Standards axis always carries the [smell baseline](references/smell-baseline.md). The repository overrides it, and every smell is a judgement call.

### Prepare an independent input packet

Before spawning, inspect the diff file list, commit metadata and planned source pointers for additional author completion narratives. A fresh context that reads a status table explaining the diagnosis, repair and passing results has already received the author's conclusions.

- Supply original requirements, task definitions, standards, code, tests, configuration and raw execution evidence. Withhold author completion reports and the completion-narrative portions of task/status records. If a record mixes original requirements with conclusions, extract only the original definitions into a temporary review input, labelled as a snapshot of the canonical record. It is not a second specification or tracker.
- Give both agents an explicit reviewed-path allowlist and the withheld-path list. Use a diff that excludes narrative-bearing files, for example `git diff <base>...HEAD -- . ':(exclude)TASKS.md'`, plus the untracked source/test paths. Do not pass an unrestricted diff alongside the filtered one. The example filename is not a universal exclusion; identify the actual records in this repository.
- In each brief say: "Read only the supplied original inputs and allowlisted candidate artifacts (including documents/records when those are the requested review target). Do not read additional withheld completion narratives, including through git diff, git show, task/status files, or another agent's report. Report your own findings before any record audit."
- Preserve full review scope. After both independent reports are recorded, the coordinator accounts for every withheld path and changed hunk under both Standards and Spec: applicable repository/document/governance rules, original requirements, additions/deletions, identifiers, factual accuracy, terminology, traceability and preservation of historical evidence. Verify claims against the actual candidate and raw execution evidence. Record separate Standards and Spec results for this record audit, and identify its executor and independence limit. If the project requires independent review of the record artifacts themselves, use separate record-only reviewers whose target is those artifacts. Report the record audit separately; do not replace, revise or rerank the already recorded independent functional reports. If the requested artifact is itself prose or a status record, it is review input, but an additional completion report about that artifact remains withheld.

### 4. Spawn both agents together

Map the operation with [harness adapters](../multi-agent-delivery/references/harness-adapters.md): spawn two **fresh, read-only** agents in one message, in the foreground, and aggregate the reports they return. Each brief contains only what is listed below: the original inputs and instructions, never your own conclusions about the change (operating rule 5.7). When a second model family is available, prefer it for at least one axis; otherwise record "independent context, same model family".

**Standards agent brief** contains:

- The filtered diff command, reviewed-path allowlist, withheld-path list and commit hashes/ranges prepared above (including applicable working-tree commands and untracked source/test paths).
- The list of standards-source files and applicable design documents found in step 3.
- The **Baseline text** section of [smell-baseline.md](references/smell-baseline.md), pasted in full.
- This brief, verbatim:

  > Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Also check: (c) each code change has tests that verify what the code should do and what it should prevent; (d) changed wording uses the repository's existing terms (skip community-authored or generated content); (e) the change is consistent with the applicable design documents, including boundaries, ownership, and lifecycle: cite the document and section for each mismatch, and distinguish an unexplained design violation from an intentional design change, judging an intentional change by its rationale and evidence (updating the design document alone does not justify it). Do not edit files. Do not invoke a review skill or spawn additional agents: perform this review directly. Under 400 words.

**Spec agent brief** contains:

- The same prepared filtered diff command, reviewed-path allowlist, withheld-path list and commit hashes/ranges, including the filtered staged/unstaged/untracked scope when step 1.4 applied.
- The path or fetched contents of the spec.
- This brief, verbatim:

  > Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. For a bug fix, also report (d) whether a regression test demonstrates the bug was reproducible before the change and is fixed after; if you cannot run the comparison, use the available evidence and state that limitation. Quote the spec line for each finding. Do not edit files. Do not invoke a review skill or spawn additional agents: perform this review directly. Under 400 words.

If the spec is missing, skip the Spec agent and note this in the final report.

After both return, run `git status --porcelain` and confirm neither agent edited files. If one did, discard its edits only when they are its own and unsaved work is not at risk, and record it.

**When agent spawning is not available**, run each axis yourself sequentially in clearly separated passes, re-reading the original inputs before each pass, and record: "Independent agent not available; sequential self-review, same context. Independent review not achieved." Do not present the result as an independent review.

### 5. Aggregate

1. Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings: the two axes are deliberately separate (see Why two axes).
2. Each agent's report is a claim (operating rule 3). Before anyone acts on a finding, open its citation and confirm the location and rule exist; mark a finding whose citation does not check out as unverified rather than silently dropping or rewording it.
3. End with a one-line summary: total findings per axis, and the worst issue *within each axis* (if any). Do not pick a single winner across axes; that is the reranking the separation exists to prevent.
4. State the review scope, candidate (step 1.6), and independence method (fresh agents, model family, or the fallback line).

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing: **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions: **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

## Verification required

- The fixed point resolved and the diff was non-empty before any agent was spawned.
- Every Standards finding names a rule in a repository file, a design document section, or one of the twelve smells, with the hunk quoted; every Spec finding quotes a line of the spec.
- Both agents ran in fresh contexts, or the fallback line is recorded. Their actual inputs excluded additional author completion narratives, including narrative-bearing hunks and commit metadata. A document/record that is itself the requested candidate is reviewed as a set of claims to verify, not as a supplied answer; extra conclusions about it remain withheld. Every withheld path/hunk received its separate complete Standards and Spec audit after the independent functional findings.
- `git status` confirms the review left the tree unchanged.

## Outputs and state

- The two-block report, summary line, scope, candidate, and independence method, in the conversation.
- When task-record updates are within authorized scope, append actionable findings to the project's existing task or delivery record per [system-verification](../system-verification/SKILL.md) section 6; record evidence per [operating rule 3](../ask-eric/references/operating-rules.md#3-evidence-record). Never create a competing tracker.
- Posting findings to a PR or issue is outward-facing: draft them, and post only with authorization for that action (see [pr-delivery](../pr-delivery/SKILL.md)).

## Completion criteria

The review is complete when both axes have reported (or the Spec axis is recorded as "no spec available"), the summary line is written, and the scope, candidate, independence method and separate record-audit outcome (when records were withheld) are stated. Findings do not converge: each fix adds new code, and judgement-call smells vary between runs. Treat a pass as a list of leads, act on the ones with a cited rule behind them, then stop. Do not rerun in a loop until it comes back clean.

## What this skill does not authorize

- Editing code. Fixes happen only when separately authorized, then the changed scope is reviewed again.
- Posting review comments, approving, requesting changes, or merging.
- Declaring technical verification passed; a clean static review does not substitute for runtime evidence ([system-verification](../system-verification/SKILL.md)).
