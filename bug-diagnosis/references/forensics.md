# Runtime and Trace Forensics

Read when the cause must be found from a running process (a spinning CPU, a leak, a visual glitch, a hang) or from a capture that already exists (a CPU profile, a trace file, a heap snapshot, a spindump). Both modes are read-only diagnosis. The deliverable is a cited diagnosis, not a fix. Write no fix unless the user asks for one; once the cause is known, hand back to the fix procedure in [SKILL.md](../SKILL.md) Phase 5, or to [performance-investigation](../../performance-investigation/SKILL.md) for performance work.

Large artifacts can flood the context window. Parse them in a fresh read-only agent and keep only the reduced finding in the main thread; map agent spawning through [harness-adapters.md](../../multi-agent-delivery/references/harness-adapters.md). When spawning is not available, parse with a script and print only the reduced result; record the substitution.

Redact secrets from every quoted line, as in [SKILL.md](../SKILL.md#redact). Keep captures outside source control.

## Runtime forensics: instrument the live process

You own the diagnosis. Instrument the live process; do not theorize from source.

1. **Capture the live signal on the matching surface.** Use the project's UI-driving tool, browser automation, debugger, or profiler to capture a real artifact: a CPU profile for a spinning process, a heap snapshot for a leak, a DevTools protocol trace for a visual glitch. A real artifact, not a guess. Attaching to a production process is a production-affecting action and needs explicit authorization.
2. **Reduce the artifact to the smoking gun**: the function on the hot path, the retainer chain from the leaked object to a GC root, the loop firing without input. Parse large artifacts in a separate agent as above and keep the reduced finding in the main thread.
3. **Prove the mechanism before believing it.** Inject instrumentation into the running process (for example a DevTools protocol `eval`), or hotfix the live code without reloading, to confirm the hypothesis cheaply. Do this only on a local or test process unless authorized otherwise, and remove the injection afterward.
4. **Map the finding back to source**: file, symbol, and the line that allocates or schedules.

**Reply:** the signal captured, the reduced finding, how you proved the mechanism, the source location, and the artifact paths. No fix unless asked.

## Trace forensics: diagnose from an existing artifact

You own the diagnosis from the artifact. The capture already exists. It is a fixed dataset: read it, do not re-run it. Keep tooling generic: a DevTools or trace parser for `.cpuprofile` and `.json.gz`, a text editor for a spindump, your heap tooling for a heap snapshot.

1. **Identify the format and load it with the right tool.** Parse large artifacts in a separate agent and keep the reduced finding in the main thread.
2. **Transform the raw artifact into a form you can query.** Dump the trace or heap snapshot into SQLite, one row per sample, frame, or node. Reach the queryable shape before you read.
3. **Narrow to the cause.** Query for the frames that hold the most time and walk the call tree to the hot path. For a leak, follow the retainer chain from the leaked object to a GC root. For a spindump, find the thread stuck on-CPU or blocked and its wait reason.
4. **Attribute to source.** Map the hot frame to file, symbol, and line via the artifact's own symbols. A frame with no source mapping is not yet a diagnosis. Resolve the symbols, or say plainly that the artifact does not carry them.
5. **Confirm with a paired capture when you have one.** Diff the before and after artifacts. Otherwise mark the finding as the strongest hypothesis the artifact supports, not a confirmed cause (label it **inferred**, not measured).
6. **Hand back a cited diagnosis**, no fix unless asked. Route to the fix procedure or to performance investigation once the cause is known.

**Reply:** the artifact and its format, the reduced finding, the source location, the artifact paths, and whether a paired capture confirmed it.
