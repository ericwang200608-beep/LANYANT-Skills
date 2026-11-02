# Guard the Context Window

**When it applies:** Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.

**Scope:** Map "route bulk to subagents" to your harness with [harness adapters](../../multi-agent-delivery/references/harness-adapters.md). When agent spawning is not available, cap scope per phase yourself and record the gap.
