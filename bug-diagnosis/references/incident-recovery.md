# Incident Diagnosis

Read when a fault needs deeper diagnosis. For simple problems with clear causes, verify the fix directly with the relevant failing test. Use isolated environments for reproduction, stress tests, and fault injection; production probes require appropriate authorization.

For production incidents, restore service under the authorized response plan before deeper diagnosis where necessary. Reproduction must not delay emergency recovery. A passing local test does not prove production recovery: follow the project release process within existing authorization and record service restoration, root cause confirmation, fix completion, and target-environment verification separately.

Read the existing domain glossary and relevant technical decisions when exploring code.

## 1. Build a feedback loop

First establish a loop that produces a pass or fail for this specific fault. Prefer a failing test. Alternatives include HTTP requests, CLI checks with fixed inputs, browser scripts, replaying captured requests, or a minimal harness. Differential runs, property tests, or automated bisection may help when applicable. If only a human can operate the interface, define repeatable steps and capture the observed results.

The loop must have actually run, exercise the real failure path, and check the original symptom rather than merely "not crashing." Make it fast, stable, and repeatable by the agent where possible, or use the explicit human feedback procedure when necessary. Pin time and random seeds, and isolate variable conditions such as files and networking.

For intermittent faults, aim to increase the reproduction rate. Repeat triggers, add controlled stress, or narrow triggering conditions. Record the observed frequency; one run without the problem is not proof of a fix.

Before displaying commands, logs, or captured artifacts, remove secrets and replace them with `<REDACTED>`. Use credentials through environment variables and retain only output needed for diagnosis.

If a reproduction loop genuinely cannot be built, list the methods tried and the missing environment access or redacted artifacts. Pause speculative fixes rather than treating a guess as the root cause.

## 2. Reproduce and minimize

Confirm that the failure is the original symptom, not a different nearby error. Record the error message, incorrect output, or performance behavior.

Remove one input, call, configuration item, or step at a time, rerunning the loop after each reduction. Keep the smallest scenario that still triggers the fault. Explain any part that cannot safely be minimized.

## 3. Form and test hypotheses

For complex problems, first list three to five hypotheses ranked by likelihood. Each must be falsifiable, for example: "If X is the cause, changing Y should make the fault disappear; changing Z should make it more pronounced."

Show the user a short ranked list and continue testing within existing authorization. Do not stop independent work while waiting for feedback.

Change one variable at a time. Prefer a debugger or interactive inspection, then targeted logs that distinguish hypotheses. Do not log everything and search blindly afterward. Use a consistent, unique prefix for temporary logs so they are easy to remove.

For performance issues, establish a measurement baseline before locating the change. Measure first, modify second.

## 4. Fix and establish a regression check

Before fixing the fault, turn the minimal reproduction into a failing test. The test interface must reproduce the actual failure pattern at the call site. Do not substitute a shallow unit test when the fault requires multiple callers or a complete call chain.

If there is no suitable test interface, explicitly record the limitation. Do not treat unrelated passing tests as proof. Preserve a check that can actually reproduce and verify the fault.

Apply fixes only within authorization. Observe the test fail, fix the root cause, then observe it pass. Rerun the original, unminimized scenario to confirm that the fix covers the original problem. Run affected regression checks and project-required checks and retain their results.

## 5. Clean up and record

Before finishing, confirm that the original reproduction no longer fails, the regression check passes, and temporary logs have been removed. Move temporary tools to a clearly marked debugging location or clean them up under existing authorization. Retain necessary reproduction evidence.

Record the actual root cause and verification results in the existing task record or handoff notes, including requirement or issue identifiers, candidate version, environment, date, executor, and evidence links. Keep unproven conclusions unproven. Do not create an extra commit or standalone report merely to record the conclusion.


## Recovery boundaries and proof

1. Declare incident scope, severity, incident commander, impacted environment, timeline, and current user impact in the existing incident record. Preserve logs and candidate versions before intervention.
2. Read-only diagnosis and isolated recovery simulation proceed within scope. Production rollback, failover, writes, restart, or data repair require explicit target authorization.
3. Prefer the smallest reversible containment with a known rollback. Record the pre-change state and stop or rollback predicates.
4. Verify recovery through the original user-visible path, error rate, queue state, data invariants, and agreed observation window. Do not confuse service recovery with root-cause resolution.
5. Return to the six-phase diagnosis loop for the root cause in isolation; add a regression, rehearse repair/recovery, and record unresolved production validation separately.
6. Close the technical unit once recovery or diagnosis criteria are met; customer and incident closure belong to the owner.
