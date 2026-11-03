# Architecture review: find deepening opportunities

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This review is informed by the project's domain model and built on a shared design vocabulary:

- Use the architecture vocabulary in [technical-design](../../technical-design/SKILL.md#3-design-modules-and-interfaces) (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter means a hypothetical seam, two adapters mean a real one"). **Leverage** and **locality** are defined in [../SKILL.md](../SKILL.md#inputs-to-read). Use these terms exactly in every suggestion, and do not drift into "component," "service," "API," or "boundary."
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this review should not re-litigate.

**No code changes during the review.** Steps 1 and 2 are read-only. The report lands outside the repository. Code changes start only after the user picks a candidate and the interview settles its shape, and then follow the behavior-pinned procedure in [../SKILL.md](../SKILL.md).

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`GLOSSARY.md`) and any ADRs in the area you are touching first.

Then spawn a fresh read-only agent to walk the codebase (map the operation through [harness-adapters](../../multi-agent-delivery/references/harness-adapters.md); its brief says "do not edit files", and you check `git status` afterward). Give it the scope, the glossary and ADR paths, the vocabulary above, and the questions below. Do not give it rigid heuristics; it explores organically and notes where it experiences friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they are called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything suspected to be shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want. The smell baseline in [standards-spec-review](../../standards-spec-review/references/smell-baseline.md) helps name what the agent finds.

When agent spawning is not available, walk the codebase yourself in a separate pass and record "exploration agent not available; explored in the main context" per [operating rules section 4](../../ask-eric/references/operating-rules.md#4-capability-gaps-are-blockers-not-silent-downgrades). Check the agent's findings against the files before putting them in the report.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repository. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user (`xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows) and tell them the absolute path. If opening fails (headless session), give the path only.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph, flow, or sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals: use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram**: side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you would tackle first and why.

**Use GLOSSARY.md vocabulary for the domain, and the architecture vocabulary for the architecture.** If `GLOSSARY.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (for example a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Do not list every theoretical refactor an ADR forbids.

See [html-report.md](html-report.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Interview loop

Once the user picks a candidate, walk the decision tree with them in rounds, using the interview method in [business-discovery](../../business-discovery/SKILL.md): constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive. Answer observable questions yourself by reading code or prototyping; ask the user only for meaning, scope, and priority ([operating rules section 1](../../ask-eric/references/operating-rules.md#1-authorization-classes)). Open-ended interview rounds have no question cap ([operating rules 5.8](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices)).

Side effects happen inline as decisions crystallize; keep the domain model current with the glossary and ADR practice in [technical-design](../../technical-design/SKILL.md):

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Add the term to `GLOSSARY.md`. Create the file lazily if it does not exist.
- **Sharpening a fuzzy term during the conversation?** Update `GLOSSARY.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing; skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Use the design-it-twice parallel-agent exploration in [technical-design](../../technical-design/SKILL.md).

Glossary and ADR edits are documentation changes in the repository; they are the only repository edits during this loop.

When the shape is settled, plan with [references/deepening.md](deepening.md) for the dependency category and test strategy, then run the behavior-pinned procedure in [../SKILL.md](../SKILL.md). If the work is large enough to need batches, sequence it with [delivery-planning](../../delivery-planning/SKILL.md).

## Output

- The absolute path of the report, the list of candidates with strength, and the top recommendation.
- After the interview: the settled shape, glossary and ADR changes made, and the next step.
