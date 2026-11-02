---
name: session-continuity
description: Resume a prior session, reconstruct recent project context, pause safely on request, hand off to a fresh agent, audit a decision trail, or catch the user up in text or video. Preserve existing evidence and the exact authorized resume point.
---

# Session continuity

## Inputs and boundaries

Read the user's focus, existing task entry, source artifact paths, current branch and diff, available chat readers, and prior evidence. Apply [operating rules](../ask-eric/references/operating-rules.md). A handoff grants no new publication, merge, deployment, deletion, schedule, or external-message permission.

## Procedure

1. Choose the branch by the user's request. A supplied full state capsule skips transcript mining. A specific prior run uses [session pickup](references/session-pickup.md); cross-chat recent context uses [recall](references/recall.md).
2. Verify inherited claims against the real artifact and current revision. Reuse evidence that still applies; preserve failed historical results. State what was inherited and what needed rechecking.
3. At a real phase boundary, apply the ordered choices in [phase boundaries](references/phase-boundaries.md). Continue when the next step needs primary context; use a portable file only when work is travelling.
4. For an explicit pause, follow [pause safely](references/pause-safely.md). Finish or back out of the current atomic step, stop nested workers, preserve work, and name the first action on resume. `Keep going` is not a pause request.
5. For a portable handoff, follow [handoff](references/handoff.md). For an authorized immediate background pickup, follow [background handoff](references/background-handoff.md) and the [harness adapter](../multi-agent-delivery/references/harness-adapters.md). Use a fresh context and explicit workspace.
6. For an auditable run, follow [decision trail](references/decision-trail.md). Append checkpoints, pivots, failed attempts, decisions, and evidence. Audit this run's rows against its raw trace and obtain independent review with the actual model-family limitation.
7. For a human catch-up, follow [catch-up](references/catch-up.md). Cover all still-pending human decisions with enough context to decide. Use [video catch-up](references/catch-up-video.md) only when requested and rendering is available.

## Requirements and validation

The log helper requires Bash. Run `bash scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`. Its first use writes a header, appends one timestamped row, strips tabs and newlines, and protects spreadsheet formula prefixes. The format template is [decision-log-template.tsv](assets/decision-log-template.tsv).

Check every artifact pointer, candidate version, current task status, decision, authorization boundary, pending item, and first resume action. Redact secrets and private details. Read only explicitly in-scope project transcripts. A missing transcript, connector, independent model, or renderer is an explicit blocked or unverified step.

## Output and completion

Keep the authoritative task record current; a handoff links it rather than creating another tracker. Store portable notes in the operating system's temporary directory unless the user names a durable location. Finish when a cold-start agent can locate the work, understand preserved decisions and failures, identify verified versus pending state, and take the exact next action. For catch-up, finish once the user has the current state and every real decision waiting on them.
