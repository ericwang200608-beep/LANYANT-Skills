# Harness Adapters

LANYANT skills describe agent operations by role, not by one product's tool names. Read this file once per session when a skill asks you to spawn agents, isolate work, ask structured questions, schedule wake-ups, or run hooks. Map each generic operation to the harness you are running in. If a row says **not available**, follow [operating rule 4](../../ask-eric/references/operating-rules.md#4-capability-gaps-are-blockers-not-silent-downgrades): record the gap in one line, use the stated fallback, and keep the affected result labeled.

Verify the mapping against your actual tool list before relying on it. Tool surfaces change between versions; the tool list you can see wins over this table.

## Generic operations

| Operation | Meaning in LANYANT skills |
|---|---|
| **Spawn a fresh agent** | Start a new agent whose context contains only the brief you write. It does not inherit this conversation. |
| **Read-only agent** | An agent told not to edit files. Check `git status` afterward to confirm. |
| **Isolated agent** | An agent working in its own git worktree or its own copy, on a named branch or commit. |
| **Background agent** | An agent that runs while you continue other work; you collect its result later. |
| **Message / follow up** | Send further instructions to an existing agent. Prefer a fresh agent with a consolidated brief unless the existing agent holds costly local state. |
| **Wait for agents** | Block until one or more agents report. |
| **Ask the user (structured)** | A multiple-choice question tool. When absent, ask in plain text with numbered options. |
| **Schedule a wake-up / loop** | Re-enter the task after a delay or an event. |
| **Hook** | A harness-level command run before or after a tool call (used by git guardrails). |
| **Model choice** | Selecting a model family and effort for a role. |

## Codex (desktop app and `codex` CLI)

| Operation | Mapping |
|---|---|
| Spawn a fresh agent | `spawn_agent` (multi-agent feature). Set `fork_turns: "none"` and put the full brief in the task text. The default may inherit this thread, which is not an independent context. |
| Read-only agent | State "do not edit files" in the brief; check `git status` afterward. The sandbox mode of the session still applies. |
| Isolated agent | Use a managed worktree tool when listed by the desktop harness. In a CLI session without that tool, create one with the shell: `git worktree add <path> -b <branch> <base>`, and name that path in the brief. The desktop app can also open a thread in a worktree; record which mechanism you used. |
| Background agent | Agents spawned with `spawn_agent` run concurrently; continue work and collect results with `wait_agent` or `list_agents`. |
| Message / follow up | `send_message` or `followup_task`; stop with `interrupt_agent`. |
| Wait for agents | `wait_agent`. |
| Ask the user (structured) | Use the question tool actually listed in the current mode. Some tools are plan-only; asynchronous questions may be unavailable. In `codex exec` there is no user; treat questions as blockers and record them. |
| Schedule a wake-up / loop | Use the desktop automation tool when it is listed and the user requested recurring work. The earlier CLI probe did not expose a scheduler. For bounded waits use `sleep` (clock) or a shell polling loop with a timeout; for long-running goals use the goal tools (`create_goal`, `update_goal`) when available. Unattended overnight loops are **not available** unless the desktop app's scheduled tasks are configured by the user. |
| Hook | `hooks` feature (config). Shell-command hooks are configured in Codex config, not in the repository; record when the project relies on Claude Code hooks that Codex will not run. |
| Model choice | Per-agent model selection when `spawn_agent` accepts it; otherwise all agents run on the session model. Record "same model family" for independence. |
| Instructions file | `AGENTS.md` (repository) and `~/.codex/AGENTS.md` (global). |
| Skills location | `~/.codex/skills/<name>/SKILL.md`. |

## Claude Code

| Operation | Mapping |
|---|---|
| Spawn a fresh agent | `Agent` tool with `subagent_type: "general-purpose"` (or a named agent type). |
| Read-only agent | `subagent_type: "Explore"`; it still has a shell, so the brief says "do not edit files" and you check `git status`. |
| Isolated agent | `isolation: "worktree"`; name the branch or commit the agent checks out. |
| Background agent | Agents run in the background and notify on completion. |
| Message / follow up | `SendMessage` to the agent id; otherwise spawn a new agent with the earlier result pasted in. |
| Wait for agents | Completion notifications arrive automatically; do not poll. |
| Ask the user (structured) | `AskUserQuestion`; in non-interactive mode ask in plain text. |
| Schedule a wake-up / loop | `ScheduleWakeup` or `/loop` when the session offers them; `CronCreate` for recurring tasks. |
| Hook | `.claude/settings.json` `hooks.PreToolUse` (project) or `~/.claude/settings.json` (global). |
| Model choice | `model: opus|sonnet|haiku|fable` plus `effort`. Non-Claude families are not available. |
| Instructions file | `CLAUDE.md`, else `AGENTS.md`. |
| Skills location | `.claude/skills/` or `~/.claude/skills/`. |

## Cursor

| Operation | Mapping |
|---|---|
| Spawn a fresh agent | `Task` with `subagent_type: generalPurpose`. |
| Read-only agent | `readonly: true` (note: this strips MCP access; use `readonly: false` with "do not edit files" when the agent needs connectors). |
| Isolated agent | `environment: "cloud"` (own VM and branch, `cloud_base_branch` for a non-default base) or a local worktree. |
| Background agent | `run_in_background: true`. |
| Message / follow up | `resume` only when local state is costly to move; otherwise a fresh `Task`. |
| Ask the user (structured) | `AskQuestion`. |
| Schedule a wake-up / loop | `/loop` (fixed or dynamic). |
| Model choice | Explicit `model` slug per role; mixed families (for example Claude and Grok) are available. |
| Instructions file | the project rules directory, `AGENTS.md`. |

## Fallbacks when a capability is missing

| Missing | Fallback | What to record |
|---|---|---|
| Agent spawning | Run each role sequentially yourself in a clearly separated pass, re-reading the original inputs before each pass. | "Independent agent not available; sequential self-review, same context." Independent review and adversarial review are then **not** achieved. |
| Worktrees | Separate clones in a temporary directory. | Paths used. |
| A second model family | Fresh context on the same family. | "Independent context, same model family." |
| Background execution | Sequential execution. | Elapsed time impact only. |
| Scheduling | Bounded polling inside the turn; hand the remaining watch to an owner. | What was not watched and who owns it. |
| Structured questions | Plain-text numbered options. | Nothing. |
| Hooks | Run the guardrail check manually before risky commands, or rely on server-side branch protection. | That the guardrail is not enforced. |


## Probe scope

A CLI probe and a desktop session can expose different worktree, scheduling, question, hook, and model controls. The CLI probe on 2026-11-02 observed collaboration tools but no worktree or scheduler tool. The desktop session on that date exposed managed worktree and automation tools. These are observations, not permanent product limitations. Check the current tool schemas before use. Never create a goal unless the user explicitly requests one.
