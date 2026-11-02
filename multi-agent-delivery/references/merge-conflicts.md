Apply [operating rules](../../ask-eric/references/operating-rules.md) to every action below. This procedure grants no push, PR, tracker write, merge, production, deletion, schedule, or paid-resource permission. Carry existing scoped authorization forward. Missing platform capabilities are explicit blockers.

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Stage only the resolved files inside the authorized merge scope, preserving unrelated user edits, and commit only when local commits are authorized. If rebasing, continue the rebase process until all commits are rebased.


Stop for a business decision if the two intents are incompatible and the original requirements do not select one. Do not fabricate a compromise merely to finish the merge.
