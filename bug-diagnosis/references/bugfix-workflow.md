# Recorded bugfix workflow

1. Assess the report and write `assessment.md` using [bug artifacts](bug-artifacts.md). Keep source code unchanged.
2. Record the assessment review checkpoint. An assess-only request stops here; an authorized fix continues. Business-rule ambiguity blocks the affected fix.
3. Run the six-phase [diagnosis loop](../SKILL.md), reproduce and minimize, then fix with a failing regression at the correct seam. Write `fix.md` without changing the assessment.
4. Run Test as a distinct validation phase against the original reproduction, regression, and affected checks. Write `test.md`; unresolved original reproduction is partial, not verified.
5. Update the authoritative issue or task record within authorization. A failed test returns to assessment with the preserved failure. A bundle is this same ordered assess/fix/test flow, not a separate implementation.

Read [bug fix execution](bug-fix.md) for full reproduction, instrumentation, patch, and proof requirements.
