# Skill mechanics

The skill-specific branch of [`writing-for-agents.md`](writing-for-agents.md): what changes when the document is a skill (frontmatter, the invocation choice, and router skills). Everything else about writing it is the universal reference in `writing-for-agents.md`.

## Invocation

Two choices, trading the two loads:

- A **model-invoked** skill keeps a `description`, so the agent can fire it autonomously, and other skills can reach it. You can still type its name: model-invocation always _includes_ user reach; a description only ever adds agent discovery, never removes the human's. The description is the skill's top-level context pointer, forced to stay loaded at all times: permanent context load in exchange for discoverability. A model-invoked skill whose content is all reference is also one home for shared reference: another skill can invoke it, so reference needed by several skills lives in one place. Mechanics: leave implicit invocation enabled (see the harness table below), and write a model-facing description carrying the trigger branches (the pointer-writing rules in `writing-for-agents.md` apply in full).
- A **user-invoked** skill strips the description from the agent's reach: only the human typing its name can invoke it, and no other skill can. Zero context load, but it spends cognitive load: you are the index that must remember it exists. Mechanics: disable implicit invocation (see the harness table below); the `description` becomes human-facing: a one-line summary, trigger lists stripped.

Pick model-invocation only when the agent must reach the skill on its own, or another skill must. If it only ever fires by hand, make it user-invoked and pay no context load.

Shared reference that two user-invoked skills both need can live in neither: with no descriptions, neither can fire the other. Push it to a plain file outside the skill system: external reference any skill can point at.

## How harnesses load skills

Verify against the harness you are running in; its documentation and your actual tool list win over this table. Skill locations per harness are in [harness-adapters.md](../../multi-agent-delivery/references/harness-adapters.md).

| Harness | What sits in context | How the user invokes by hand | How to make a skill user-invoked |
|---|---|---|---|
| Claude Code | Each skill's `name` and `description` from frontmatter; the body loads when the skill fires. | Typing `/<name>` or naming the skill. | Frontmatter `disable-model-invocation: true`. |
| Codex | Each skill's `name` and `description` from frontmatter; the body loads when the agent opens `SKILL.md`. | Naming the skill in the prompt or picking it from the app's skill list. | `agents/openai.yaml` in the skill directory with `policy:` `allow_implicit_invocation: false`; give it an `interface:` `display_name` and `short_description` for the human. |

When one skill must work in both harnesses as user-invoked, set both mechanisms. When the harness offers no way to disable implicit invocation, the skill is model-invoked; write its description as a model-facing pointer.

**LANYANT suite skills are model-invoked.** Their frontmatter carries only `name` and `description`, because the router and sibling skills must reach each other. Never add `disable-model-invocation` or an implicit-invocation opt-out to a suite skill. Personal or team mode skills are a different case; see [mode-skill.md](mode-skill.md).

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `writing-for-agents.md`): split off a model-invoked skill when you have a distinct leading word that should trigger it on its own (a trigger word you actually use in your prompts), or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

When user-invoked skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**: one user-invoked skill that names the others and when to reach for each, so the human has one skill to remember instead of many. It can only hint, never fire them: user-invoked skills have no description, so nothing but the human can reach them.

A model-invoked router (the LANYANT suite's `ask-eric`) is the other shape: its description is always loaded, and it links siblings by relative path so the agent opens the right one.
