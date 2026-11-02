# Outcome-Oriented Execution

**When it applies:** Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code.

Optimize for the intended, verifiable end state rather than preserving smooth intermediate states.

**Why:** Keeping every intermediate step fully stable often creates temporary compatibility code that becomes long-lived debt. Converge on the target architecture and prove correctness at explicit verification boundaries.

**Core rule:**
- Prioritize end-state integrity over transitional stability
- Intermediate breakage is acceptable when it is planned, scoped, and reversible

**Guardrails:**
- Use this for planned rewrites and migrations with explicit phase boundaries
- Declare where temporary breakage is acceptable
- Keep high-signal checks for actively touched areas while migrating
- Require full static and runtime verification at plan completion

**Scope:** Planned intermediate breakage is acceptable only on work that no one else consumes yet (an unshared branch, an integration branch the plan owns). It never extends to a shared trunk, a released interface, or consumers you do not control; those follow expand, migrate, contract ([operating rule 5.6](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices)).
