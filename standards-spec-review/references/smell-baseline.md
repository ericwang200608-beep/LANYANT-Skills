# Smell Baseline

The Standards axis always carries this baseline: a fixed set of twelve code smells that applies even when a repository documents nothing. Paste the whole of the section **Baseline text** below into the Standards agent brief. The agent has no other access to it.

## Baseline text

On top of whatever the repo documents, the Standards axis carries this **smell baseline**. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

When suggesting a fix, prefer existing project capabilities, standard libraries, and platform features. Do not reduce code by removing necessary validation, error handling, security, accessibility, or explicitly required capabilities. Explain the concrete maintainability or correctness problem each suggestion solves. Personal preference alone is not a blocking issue.

## Why a fixed baseline

A generic review that does not know the repository's standards flags what is deliberate in the codebase and misses the invariants the codebase depends on. The repository's own documentation is the primary source on the Standards axis, and the repository always overrides. The baseline sits underneath it so that a repository with no written standards still gets a consistent, checkable review, and each smell names its fix so a finding comes with a remedy attached rather than only a complaint.
