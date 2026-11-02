# Single-Ticket Implementation Flow

Read when the work arrives as one ticket, one spec, or a plan just agreed in the conversation, and the job is to build what was already decided. This flow builds settled work. It does not reopen the plan: no new interview, no alternative design proposal. When a task definition is insufficient to execute, follow [section 1 of the skill](../SKILL.md#1-load-implementation-context) and complete the gap in the task record rather than redesigning while building.

## 1. Pick the right entry point

| The work is... | Do this |
| --- | --- |
| A ticket on the tracker | Implement that one ticket in this run. Clear context between tickets. |
| A spec not yet split up, and the build spans sessions | Split it with [delivery-planning](../../delivery-planning/SKILL.md) first, then implement one ticket per run. |
| A spec, and the build is small | Implement directly against the spec. |
| Only in the conversation just held, and still small | Implement in the same session. State that the plan lives in the thread so you do not hunt for a file that does not exist. |
| Not written down anywhere yet | Clarify it first with [business-discovery](../../business-discovery/SKILL.md) or [technical-design](../../technical-design/SKILL.md). |
| One concrete behavior wanted test-first, with no spec | Use [test-driven-development](../../test-driven-development/SKILL.md) directly. |
| Already built, and it needs checking | Use [code-review](../../code-review/SKILL.md) directly. |
| A whole spec or ready frontier in one run | Use [multi-agent-delivery](../../multi-agent-delivery/SKILL.md): each ready ticket goes to its own isolated agent in its own worktree, merged onto one integration branch. |

## 2. Prerequisites

1. **Ticket reference.** When given a ticket reference, fetch it from the project's issue tracker and state its title before starting. If the reference is ambiguous (for example `#2` could match a numbered todo file or checklist already in context), ask. A full issue URL or `owner/repo#N` removes the ambiguity. Check that the stated title matches the ticket the user meant.
2. **Branch.** Commits land on the branch you are on. Check the current branch before the first commit. Create or switch branches only when that is in scope; otherwise report the branch you would commit to.
3. **Commits in scope.** Commit only when commits are in the requested scope (operating rules section 1). An implementation-only request without commit scope ends with an uncommitted, verified working tree and a summary.
4. **One checkout, one session.** Never run several implementation sessions side by side in one checkout. They share one working directory, one index, and one HEAD: an amend in one session can land on another session's commit, stashes vanish, and commits land on the wrong branch. Use separate worktrees for parallel work, and remember that `refs/stash` is shared across worktrees too, so do not rely on `git stash` across parallel sessions. See [multi-agent-delivery](../../multi-agent-delivery/SKILL.md).

## 3. What one run does

A run has five steps, in order:

1. Read the ticket or spec and work out the seams. Restate what you will build before writing code.
2. Drive [test-driven-development](../../test-driven-development/SKILL.md) at the pre-agreed seams, one red-green slice at a time (the cycle in [section 3 of the skill](../SKILL.md#3-complete-one-red-to-green-cycle-at-a-time)).
3. Run the type checker often and run the single affected test file as you go.
4. Run the full test suite once, at the end.
5. Review with [code-review](../../code-review/SKILL.md), then commit to the current branch when commits are in scope.

One run covers one ticket. Tickets are vertical slices sized to fit one fresh context window, so the rhythm is: clear context, implement one ticket, commit, clear again. Each ticket is self-contained; discard the previous ticket's context.

## 4. Pre-agreed seams

A **seam** is the public boundary where behavior is observed without reaching inside. Tests live at seams. When the seam is agreed before code exists, the tests last and the implementation underneath can be rewritten without changing them.

Agree the seams before the first test. Look for them in the spec or task record first. If the spec names none, propose them in the first exchange of the run and confirm them under [section 2 of the skill](../SKILL.md#2-define-tested-behaviors-and-interfaces). If the seams are agreed nowhere, the run degrades into "just write the code" and nothing warns you; say so and stop to agree them rather than silently writing tests at guessed seams.

## 5. Review before committing

The review must see the change. A review of `git diff <base>...HEAD` excludes staged and working-tree changes, so a review run before any commit sees nothing. Either:

- commit the slice first (when commits are in scope), then review against the fixed point you branched from; or
- review the working tree explicitly, including staged, unstaged, and untracked files.

An agent reviewing code it just wrote is biased toward its own solution. Run the review in a fresh context against the fixed point, per [operating rule 5.7](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices). Map the fresh context through [harness adapters](../../multi-agent-delivery/references/harness-adapters.md); when no fresh context is available, record "independent review not achieved; sequential self-review, same context."

Act on blocking review findings inside the ticket's scope, rerun the affected tests, and record the rest as open items. Review findings are not silently dropped.

## 6. Close-out

The run ends at a verified change (and a commit when in scope). It does not close the tracker item by itself:

- Update the project's existing task record per [section 5 of the skill](../SKILL.md#5-verify-integration-and-update-task-status).
- Closing the issue, ticking its acceptance boxes on the tracker, or commenting on it is an outward-facing tracker write. Do it only with authorization; otherwise list exactly what to close and which criteria were met.
- On a dependency chain, unclosed tickets keep their dependents blocked. Say which tickets become unblocked once this one is closed.
- To open a pull request, use [pr-delivery](../../pr-delivery/SKILL.md) and only with authorization to open one.

## 7. Sizing

A non-trivial ticket exceeding 100k tokens of context is normal: exploration, a red-green loop per seam, a full suite, and a review. If a single ticket keeps going over, split it in the task record rather than raising effort.

## 8. The run is working if

- It opens by reading the ticket or spec and restating what it will build, rather than asking what to build.
- Behavior tests appear red then green at agreed seams, visible in the run, not only as tests in the diff.
- Type checks and single test files run repeatedly during the run, and the full suite runs once near the end.
- It reaches a verified change (and a commit when in scope) without prompting to carry on.
- The diff is one ticket's worth of change: a vertical slice through every layer, not several tickets swept together.
