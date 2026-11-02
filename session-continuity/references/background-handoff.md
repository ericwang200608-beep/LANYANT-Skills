Write a handoff summary of the current conversation so a fresh background agent can continue. Save it to the operating system's temporary directory. Use the native agent launcher described in [harness adapters](../../multi-agent-delivery/references/harness-adapters.md), give the agent a descriptive name, and seed a fresh context with the summary file's literal contents. Do not interpolate the summary into a shell command. Name the working directory and how to collect the result. A separate user-owned chat is created only when the user explicitly requested one; ordinary continuation uses a subagent. If no background launcher exists, return the portable handoff and mark automatic pickup unavailable.

Include a "suggested skills" section in the summary, naming which skills the next agent should read the relevant LANYANT procedure for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information, since the summary becomes the agent's prompt.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the summary accordingly.
