# Reflect: mine a session for skill edits

Mine the current conversation for durable learnings, then route them into skill edits.

Use when the user says "reflect" or asks to turn what this session learned into skill changes. Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, find this conversation's transcript with [session-transcripts.md](session-transcripts.md). Stay inside the workspace scope. If no transcript matches, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

Spawn three fresh agents at once, one per lens (see [harness-adapters.md](../../multi-agent-delivery/references/harness-adapters.md) for the spawn call). Tell each one not to edit files and check `git status` afterward. Give reviewers connector (MCP) access so they can look up the tickets, chat threads, and observability traces the transcript references; in a harness where a read-only agent loses connector access, use a normal agent with the "do not edit files" instruction instead.

Pick the model per role through the harness's model choice. Use the strongest available model at high effort for judgment, divergent, and synthesizer. Use a different model family for tooling when the harness offers one; when it does not, use the same family and record "independent context, same model family". If the harness rejects a model name, use its default and say so.

| Lens | Model | Prompt template |
|---|---|---|
| Judgment | strongest available, high effort | [reflect-judgment-reviewer.md](reflect-judgment-reviewer.md) |
| Tooling | different family if available, high effort | [reflect-tooling-reviewer.md](reflect-tooling-reviewer.md) |
| Divergent | strongest available, high effort | [reflect-divergent-reviewer.md](reflect-divergent-reviewer.md) |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in their response body.

If agent spawning is not available, run each lens yourself in a separate pass, re-reading the template and the transcript before each, and record "independent agent not available; sequential self-review, same context". The independence of the lenses is then not achieved.

## 3. Synthesize

Spawn one fresh agent with the judgment/divergent model, connector access, and the "do not edit files" instruction. It spot-verifies citations through connectors. Pass [reflect-synthesizer.md](reflect-synthesizer.md) verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. Encoding a lesson as a check follows the [encode lessons as checks](../SKILL.md#encode-lessons-as-checks) procedure; see also [engineering-principles](../../engineering-principles/SKILL.md).

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent that loads them. Do not auto-apply.

Draft each Backlog item for the team's devex or backlog tracker right away. Filing it is a tracker write: file it only when the user has authorized tracker writes; otherwise hand the drafts to the user. Only the Accepted list waits for approval to apply.

Never edit a skill inside an installed plugin, package, or marketplace cache. Before approval, show its destination: the project skills location or the user skills location for this harness (see [harness-adapters.md](../../multi-agent-delivery/references/harness-adapters.md)). After approval, copy the skill folder there and edit the copy. Never open a PR or push.

Edits to a LANYANT suite skill always go through the [suite maintenance procedure](skill-authoring.md#maintaining-the-lanyant-suite), never directly in the installed copy.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than about 10 lines): run the [skill authoring procedure](skill-authoring.md) with its draft, test, and iterate loop.
- `tune description: <skill path>` (the skill exists but did not trigger when it should have): run the [description tuning loop](skill-authoring.md#tune-a-description).
- `new skill via skill authoring: <kebab-name>`: run the [skill authoring procedure](skill-authoring.md). Do not invent the shape ad hoc.

Run the skill validation checks in [skill-authoring.md](skill-authoring.md#validate) on every touched skill before declaring done. If the environment ships its own SKILL.md validator, run that too.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog drafted or filed: `<issue title>` (`<tags>`), with where it was filed or "draft only". One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
