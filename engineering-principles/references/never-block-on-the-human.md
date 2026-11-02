# Never Block on the Human

**When it applies:** Apply when tempted to ask 'should I do X?' on reversible work.

The human supervises asynchronously. Agents must stay unblocked. Make reasonable decisions, proceed, and let the human course-correct after the fact. Since code changes are reversible and reviewable, a wrong decision usually costs less than blocking.

- Proceed, then present. Do the work, show the result. Don't ask "should I do X?" Do X, explain why.
- Make the system self-healing. When you notice a problem, log it and fix it in the next round.
- Irreversible actions (force-push, delete production data, send external messages) still require confirmation.
- Reversible actions (write code, edit notes, split tasks) should proceed without blocking.
- Product direction comes from the human. Execution should not block.

**Scope:** This applies only to reversible work inside the authorized scope, as [operating rule 1](../../ask-eric/references/operating-rules.md#1-authorization-classes) defines it. Outward-facing actions (push, PR, comments, chat, tracker writes) need authorization for the specific action, and irreversible or production-affecting actions need explicit authorization for that action and target, even during long or unattended runs. Questions of business meaning, scope, priority, or customer commitment go to the owner; continue unaffected work while waiting. "Fix it in the next round" means inside the authorized scope; fix broken tooling you meet in its own change.
