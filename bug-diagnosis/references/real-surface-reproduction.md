# Reproduce Through the Real Surface, Then Fix

Read when a reported bug lives in a user-facing app (web, desktop, mobile, CLI, or TUI) and must be reproduced through the real interface before any fix, when a report arrives through a chat thread, issue, or tracker that you may later answer, or when running a report-driven repro-and-fix automation. The rules here are stricter than a general fix flow: no confirmed repro means no authored fix.

Reproduce the exact symptom through the target app's real UI. Verify an existing fix when one exists. Attempt a bounded fix only after a confirmed repro.

Load the configuration the run depends on (source location, triage identity, budgets, control adapter, feature map, artifact directory, operations location). If the configuration, a required action, the control adapter, or the completed feature map is missing, fail closed: report `Blocked` with what is missing.

## Hard safety rules

Every post, comment, or status update below is outward-facing. Make it only when the run's authorization covers that action and that destination ([operating rules section 1](../../ask-eric/references/operating-rules.md#1-authorization-classes)). Without it, prepare the text and report it in the run output.

- Freeze the source coordinates (channel or project, and the thread, issue, or item identifier) before doing any work.
- Never post a new top-level message in the source location.
- Preflight the source parent before every source post.
- The coordinator (the lead agent) is the only poster.
- Delegated analysis workers are read-only and return findings or media notes.
- A fix-phase code worker may edit only when its environment provably excludes posting credentials and every outward write action. Otherwise the coordinator edits.
- Every child prompt explicitly forbids posting, commenting, messaging, and every other outward write.
- Never give a child a posting token, posting instructions, source coordinates for posting, or permission to report externally.
- If a child needs outward write access to run, do not launch it.
- Utility bots are evidence sources. They do not own the fix unless a person explicitly delegated the fix to them.
- The exact discriminating symptom must appear twice through real UI interaction.
- State inspection may confirm an observation. It must not inject or force the symptom.
- No confirmed repro means no authored fix.
- Existing pull requests or commits switch the run to verify mode ([verify-existing-fix.md](verify-existing-fix.md)). Do not author over them, and never open a competing pull request.
- Use the code host's regular web links for pull requests (for example `https://github.com/{owner}/{repo}/pull/{number}`).
- Keep captures, recordings, logs, and tokens out of source control.
- Keep large artifact analysis in separate read-only agents and only reduced findings in the main thread; map spawning through [harness-adapters.md](../../multi-agent-delivery/references/harness-adapters.md).
- Sequence verifiable units (repro, then fix, then proof), fix root causes, and prove the result on the running app, per [engineering-principles](../../engineering-principles/SKILL.md).

## 1. Freeze source coordinates

Before making a work list or delegating:

1. Require the trigger location to equal the configured source location.
2. Set the source thread identifier to the trigger's parent thread when present; otherwise use the trigger message itself.
3. Require a nonempty source thread identifier.
4. Store the source location and source thread identifier as immutable values.
5. Read the source thread and verify its root has those exact coordinates.
6. Fetch the source permalink.

Never replace these values with a reply identifier, an operations identifier, or a status-message identifier.

Before every source post:

1. Read the thread by the immutable coordinates.
2. Confirm the parent exists, is not deleted, and still belongs to the source location.
3. Send only to the source location and source thread.
4. Read the thread again and verify the new message is a reply.

If any check fails, post nothing. Never retry at the top level or in a fallback location.

## 2. Wait for the triage verdict

When the run is gated on triage, watch the source thread for the configured verdict budget. Stay silent while waiting. Triage itself belongs to [issue-triage](../../issue-triage/SKILL.md).

Accept a verdict only when:

- Its author matches the configured triage identity.
- It is a reply under the source thread.
- It contains exactly one configured verdict marker (for example `bug`, `performance`, or `other`, optionally with a tracker link).

Proceed only for `bug` or `performance`. Capture the optional tracker URL. Stop silently for `other`, a missing verdict, an untrusted author, conflicting markers, or a timeout. A `performance` verdict continues in [performance-investigation](../../performance-investigation/SKILL.md) once reproduced.

Interactive runs without a triage gate skip this step: the user's request is the verdict.

## 3. Apply ownership and fix-artifact gates

Re-read the thread immediately before starting work.

### Someone is explicitly fixing it

Stop when a person clearly claims the fix, gives a concrete implementation plan, or asks another agent to implement, patch, fix, or open a pull request.

These are not fix ownership:

- A bot summarizes evidence.
- A tool looks up logs or tickets.
- Someone asks a bot to diagnose, explain, inspect, or reproduce.
- A bot posts a cause hypothesis without agreeing to implement it.

Judge the requested action, not the presence of a bot.

### A fix artifact already exists

If an open pull request or merged commit plausibly fixes this report, switch to [verify-existing-fix.md](verify-existing-fix.md).

An artifact may come from the thread, tracker issue, repository history, or pull request search. A claim without a commit or pull request is not a fix artifact.

If a person owns the work but has not produced an artifact, stop. Do not race them.

## 4. Open an optional operations thread

If an operations location is configured and authorized, the coordinator may create one top-level status message there. This is the only allowed top-level post in the repro workflow. Store its coordinates separately and never confuse them with the source coordinates.

Use plain status strings and keep them short:

- Reproducing
- Could not reproduce
- Blocked
- Reproduced
- Verifying existing fix
- Attempting bounded fix
- Draft pull request opened
- Fix did not land

Prefer the harness's configured messaging actions. Use a separately configured token only for a narrow missing capability, such as editing this one status message. Never expose the token to a worker.

If no operations location is configured, keep detailed status in the run output. Do not substitute a source top-level message.

## 5. Load and check the control adapter

Read [control-adapter.md](control-adapter.md) and the completed feature map (template: [feature-map.template.md](../assets/feature-map.template.md)), then load the project's UI-driving tool or browser automation that implements the adapter.

Find the feature-map section that matches the reported user path. Read it before driving the app. If no section covers the feature, mark the run blocked instead of inventing a path or selector.

Require all seven capabilities:

1. Bring up the configured target app and test environment.
2. Navigate the mapped feature and exercise its documented states.
3. Drive the real UI with clicks, typing, keys, scrolling, drag, resize, or navigation.
4. Inspect state without mutating it.
5. Capture screenshots.
6. Start and stop a screen recording.
7. Clean up processes, sessions, profiles, and temporary data.

If the adapter is absent or any required capability is missing, mark the status blocked and stop. Do not pretend a screenshot, unit test, state mutation, or source reading is a UI repro. Record the gap per [operating rules section 4](../../ask-eric/references/operating-rules.md#4-capability-gaps-are-blockers-not-silent-downgrades).

## 6. Study the report

Read the full source thread and the tracker issue when present.

Collect:

- Exact action path
- Expected behavior
- Observed behavior
- Discriminating state where they diverge
- Frequency
- Version, environment, and platform
- Attachments and error signatures
- Candidate code area

Inspect screenshots and video. Use read-only parallel workers for code history, test ideas, blast-radius mapping, and media review when useful. Each worker gets a narrow question and the outward-write prohibition.

Trace the action through the repository and its regression history with [codebase-investigation](../../codebase-investigation/SKILL.md). Form competing cause hypotheses and identify the evidence that would separate them.

## 7. Reproduce

Bring up the target app through the control adapter.

Confirm the correct app, workspace, account, data set, and feature state before acting. Use stable app markers. Do not rely on window order or a familiar title alone.

Drive the reported path through real UI actions.

Before calling it reproduced:

1. Name the correct final state.
2. Name the broken final state.
3. Reach the point where they diverge.
4. Observe the broken state.
5. Reset enough state to make the second attempt independent.
6. Repeat the same path and observe the same broken state again.
7. Cross-check a real state value when possible.

An expected dialog, loading state, or setup step is not the bug. Capture the final state that distinguishes correct from broken behavior.

Use the configured repro budget. If the symptom does not reproduce within it, report a clean `Could not reproduce`. If the environment cannot provide a required capability, report `Blocked` and state what was missing.

## 8. Capture and review evidence

For a successful repro:

- Record the full path through the symptom.
- Capture a screenshot of the broken final state.
- Save a short note with the exact steps and observed state.
- Keep artifacts in the configured temporary artifact directory, outside the repository.

Have a read-only media reviewer (a fresh agent) answer one question: does the evidence visibly show the discriminating broken state? When spawning is unavailable, review it yourself in a separate pass and record "independent agent not available".

If the answer is no or uncertain, the repro is not confirmed. Capture better evidence or report `Could not reproduce`.

Post detailed evidence only in the operations thread when configured. Keep any source update concise.

## 9. Report the repro outcome

Update the operations status first.

For `Could not reproduce` or `Blocked`, post nothing in the source thread. The operations thread or run output carries the result.

For a confirmed repro, when authorized, run the source preflight and post at most one unprompted source reply:

- Say the issue reproduced.
- Link the operations evidence thread when one exists.
- Include at most three short findings.
- Link the tracker issue when one exists.
- Do not ping an owner by default.

Attach evidence only when the configured messaging action keeps it inside the same source thread and the organization's retention policy allows it.

Wait for the configured rejection window. If a person shows that the setup or interpretation was wrong, correct the repro once. Do not start the fix phase until the window closes without a valid rejection.

## 10. Verify an existing fix

When a fix artifact exists, follow [verify-existing-fix.md](verify-existing-fix.md). Verification must show the symptom on the baseline and its absence on the patched build, each through the real UI twice. Do not edit the existing fix, add a competing patch, or open a replacement pull request.

## 11. Qualify a bounded fix

Attempt a fix only when all of these hold:

- The outcome is a plain confirmed repro.
- Media review confirmed the broken final state.
- No existing fix artifact appeared.
- No person claimed the fix during the rejection window.
- Runtime evidence identifies the root cause.
- The likely change fits the configured fix budget and repository scope.
- The control adapter can run both baseline and patched builds.
- Fixing is within the run's authorization.

If any condition fails, keep the repro report and stop without a pull request.

When the gate passes, update the status to `Attempting bounded fix`.

## 12. Root-cause and implement

The coordinator owns every post, the final diff review, commits, and the pull request.

Read-only workers may:

- Trace code and history
- Propose tests
- Map blast radius
- Review a diff
- Review media

They do not edit, run outward writes, post status, or own the fix.

A tightly scoped code edit may be delegated in this phase only when tool isolation removes posting credentials and every outward write action from that worker. Its prompt still carries the explicit outward-write ban. The coordinator reviews the edit and runs or verifies the required tests. If tool isolation is uncertain, keep the edit in the coordinator.

Confirm the mechanism with runtime evidence. Eliminate competing hypotheses before editing.

Fix the root cause with the smallest justified change.

- Follow [test-driven-development](../../test-driven-development/SKILL.md) when there is a cheap local test target: write the failing test before the fix.
- State why test-first was skipped when the path is expensive, unclear, or integration-heavy.
- Keep unrelated cleanup out.
- Stop if the change grows beyond the configured effort or risk budget.

## 13. Prove the fix

Keep the original baseline evidence.

On the patched build:

1. Run the same real UI path.
2. Repeat it twice.
3. Show that the broken state is gone.
4. Show the expected state in its place.
5. Capture an after recording and screenshot.
6. Cross-check the same real state value used for the baseline.

A compile, unit test, code review, or plausible diff is not after evidence.

Run focused tests, then smoke the blast radius around the changed behavior. Cover nearby states, inputs, permissions, platforms, and failure paths that the change could affect. Stop without a pull request if a regression remains.

## 14. Open a draft pull request

Only after before-and-after proof, and only when opening a pull request is authorized:

- Review the final diff for unrelated changes and secrets.
- Run the repository's required checks.
- Create small ordered commits when the repository workflow allows it, with the failing repro before the fix.
- Open a **draft** pull request through [pr-delivery](../../pr-delivery/SKILL.md). Never merge or deploy from this workflow.
- Link the tracker issue using the tracker's supported pull request syntax.
- Use the code host's regular pull request URL form.
- Include the repro steps, root cause, test result, before and after evidence, and blast-radius checks.
- Write the pull request text and every status update with [technical-writing](../../technical-writing/SKILL.md).

When the pull request is not authorized, stop at a local branch with ordered commits (if commits are in scope) and a drafted pull request body, and report them.

If pull request creation fails, do not claim success. Keep the commit or branch state in the run output and mark the status `Fix did not land`.

On success, mark the status `Draft pull request opened` and post one concise reply in the operations thread with the linked pull request. Do not create a second source top-level message or an unprompted source reply.

## 15. Follow-ups and cleanup

Watch the operations thread for one follow-up window when a watch mechanism exists (see [harness-adapters.md](../../multi-agent-delivery/references/harness-adapters.md) for scheduling; record what was not watched when it does not).

- Answer a direct question from evidence already gathered.
- Apply one concrete correction and rerun the repro once when it invalidates the setup.
- Stay out of human coordination and side chatter.
- Stop when asked.

Always call the control adapter's cleanup capability. Keep artifacts only as long as the retention policy allows.
