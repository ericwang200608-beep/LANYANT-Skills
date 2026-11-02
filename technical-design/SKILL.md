---
name: technical-design
description: Turn business requirements into a technical plan, data model, interface contracts, and deployment plan. Use to establish technical design before production development, or to design affected modules and interfaces in an existing system.
---

# Technical and Database Design

Read the requirements, resolve unknowns in the technical context, and produce a data model, interface contracts, and a validation guide. Design deep modules that hide substantial behavior behind small interfaces, and verify them through those interfaces.

## 1. Load context

Consider the user's input. Read the requirements specification, confirmed prototype decisions, and the project's existing principles. Check which requirements apply to this design.

Extract the primary goal from the requirements and fill in the technical context:

- Language and version.
- Primary dependencies.
- Storage; explicitly state when it is not applicable.
- Testing approach.
- Target platform.
- Project type.
- Performance goals.
- Technical constraints.
- Scale and scope.

Mark unknowns as "NEEDS CLARIFICATION." Include business conditions that affect the plan: budget, customer network, user devices, data retention requirements, and whether the system must run on an internal network.

Check the project's principles before design and recheck them after design. If an existing requirement is violated without adequate justification, identify the problem and pause the design work that depends on that decision.

If no principles are recorded, derive the minimum necessary technical quality checks from confirmed constraints and project requirements, recording them in the existing plan. Business commitments still require confirmation; no standalone principles file is mandatory.

## 2. Research and resolve unknowns

Extract research tasks from the technical context:

- For each clarification item, identify the question to answer.
- For each dependency, investigate relevant usage practices.
- For each system integration, investigate suitable integration patterns.

Investigate against primary sources: official documentation, source code, specifications, and first-party APIs, rather than secondary accounts of them. Trace each conclusion to the source that owns the fact.

Save findings according to the project's documentation conventions and cite the supporting evidence. For each decision, record:

- **Decision:** What was chosen.
- **Rationale:** Why it was chosen.
- **Alternatives considered:** What else was evaluated.

For critical questions that require observation, perform the smallest validation and record its conditions and results. If a question cannot be resolved immediately, state its impact, owner, and when it will be addressed. Keep dependent parts of the plan pending rather than reporting them as verified.

## 3. Design modules and interfaces

Design deep modules: substantial behavior behind a small interface, placed at a clear seam, testable through that interface. The aim is more capability with less knowledge for callers, changes concentrated in one place for maintainers, and natural testing.

### Use consistent concepts

- **Module:** Anything with an interface and an implementation: a function, class, package, or tier-spanning slice of functionality.
- **Interface:** Everything a caller must know to use the module correctly, including not only type signatures but also invariants, ordering constraints, error modes, required configuration, and performance characteristics.
- **Implementation:** The code inside a module.
- **Depth:** The amount of behavior a caller or test can exercise per unit of interface knowledge. A module is deep when substantial behavior sits behind a small interface, and shallow when its interface is nearly as complex as its implementation.
- **Seam:** A place where behavior can be changed without editing code at that location; the location of a module's interface.
- **Adapter:** A concrete implementation that satisfies an interface at a seam.

### Examine the interface shape

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

Depth is a property of the interface, not the amount of implementation code. A deep module can internally consist of small, mockable, replaceable parts without exposing them through its public interface. A module can have internal seams for its own tests and external seams for callers.

**The deletion test:** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across multiple callers, it was earning its keep.

**The interface is the test surface:** Callers and tests cross the same seam. If tests need to bypass the interface and reach inside, the module may have the wrong shape.

**One adapter means a hypothetical seam. Two adapters mean a real one.** Do not introduce a seam unless something actually needs to vary there.

### Design for testability

1. **Accept dependencies, do not create them.** For example, pass payment capabilities into an order-processing function instead of creating a payment client inside it.
2. **Return results, do not produce side effects.** For example, calculate and return a discount instead of directly modifying the cart total inside the calculation function.
3. **Keep the surface area small.** Fewer methods mean fewer tests; fewer parameters mean simpler test setup.

Record the selected project structure using actual directories, and remove inapplicable options. For necessary additional complexity, state the current need and why a simpler alternative is insufficient.

## 4. Produce the data model

Extract from the requirements specification:

- Entity names, fields, and relationships.
- Validation rules derived from requirements.
- State transitions, where applicable.

Organize these into a data model. The database design should also identify where data is stored, key field types, primary keys, and necessary relationship constraints so the model maps to actual storage.

Actively clarify business terminology and object relationships during design:

- When a user's term conflicts with the existing glossary, point it out immediately and clarify.
- When a term is vague or overloaded, propose a precise canonical name.
- When discussing object relationships, use concrete scenarios to probe boundaries and edge cases.
- When the user describes existing system behavior, cross-check it against the code and surface contradictions.

Update the project glossary as terms are resolved. Keep it limited to business terminology, without technical implementation details, and do not use it as a substitute for requirements.

When a confirmed business rule changes, update the authoritative specification within authorization and assess affected design, tasks, tests, user instructions, and acceptance evidence. Record what remains applicable and what must be revalidated; reopen only affected work. If upstream edits are outside scope, record the exact required updates and their owner rather than silently treating stale artifacts as current.

Create a separate architectural decision record only when all of the following hold: changing the decision later would be costly; future readers would struggle to understand it without context; and real alternatives were compared and a tradeoff made. Otherwise, keep the decision in the current design.

## 5. Define interface contracts

Identify the interfaces the project exposes to users or other systems, and choose a contract format appropriate to the project type. Examples include public library APIs, CLI command schemas, web service endpoints, parser grammars, or application UI interaction contracts.

For a purely internal tool with no external interfaces, a separate interface contract file may be skipped.

For capabilities the system actually needs, explain:

- How pages, backend, and database collaborate.
- Login and identity sources, role permissions, and where authorization is enforced.
- File upload entry points, storage locations, and access methods.
- External system integration, inputs, outputs, and failure handling.

Do not add designs for capabilities outside the system's needs. Explicitly identify where authorization is enforced, rather than describing only whether a page displays a button.

## 6. Complete deployment and validation arrangements

Explain the deployment approach and how it meets customer requirements for networks, devices, data retention, and internal-network operation. Given expected data volume and user counts, describe necessary runtime resources, cost assumptions, and maintenance implications.

Create a validation guide describing scenarios that demonstrate end-to-end behavior, including prerequisites, environment setup, test or run procedures, and expected outcomes. Reference the data model and interface contracts instead of duplicating their contents.

Reuse existing acceptance scenario identifiers and authoritative definitions, adding only design-specific validation details. Include data collection needed for agreed business metrics and pre-launch baselines when it requires engineering work.

Use actual commands when runnable checks exist. Clearly mark checks that are not yet implemented as future validation, without claiming they have been executed.

The validation guide must not contain full implementation code, model or service bodies, database migrations, or complete test suites. Those belong to the subsequent implementation phase.

## 7. Deliver and finish

Record applicable requirement or task identifiers, the artifact or candidate version, environment, execution date and executor, expected and actual outcomes, and evidence links in the existing task or delivery record within authorization; for read-only work, report them in the conversation. Mark planned, failed, unverified, and not-applicable items accurately. For document-only work, identify the document revision and checks performed; do not invent runtime evidence or create a separate report solely for these fields.

Deliver the technical plan, database design, interface contracts, and deployment plan according to project documentation conventions. Place related research and validation guidance appropriately and cross-reference them instead of duplicating content.

Explain the recommended approach, rationale, and implications for cost, usage, and maintenance to the product owner.

Before finishing, check that:

- Each key requirement has a corresponding implementation approach.
- Data relationships, authorization enforcement locations, deployment conditions, and cost constraints are explained.
- Project principles have been rechecked after design.
- Uncertainties affecting feasibility have validation results, or an explicit owner, resolution timing, and pending portions of the design.
- Deliverable files and outstanding items are identified.

For a design-only request, end after delivering the design.

When the request covers only this stage, finish after its agreed deliverables and checks. When the user has already authorized later stages, continue once their prerequisites are met without asking for the same authorization again. Reuse applicable evidence and reopen only affected work. Stage transitions do not grant new permission to publish, send messages, or make production or irreversible changes.

## Design workflows, contracts, and helpers

For substantial module design read [module design](references/module-design.md), [design it twice](references/design-it-twice.md), and [architecture procedure](references/architect.md). Use the [red flags](references/design-red-flags.md), [rationale template](references/rationale-template.md), and [independent runner prompt](references/runner-prompt.md) at the corresponding steps. Preserve genuinely different candidates and compare them before selecting a design.

For a specification-driven plan read [plan workflow](references/plan-workflow.md) and use [the plan template](assets/plan-template.md). Write contracts before implementation at real system boundaries, including request/response shapes, authorization, invariants, error cases, idempotency and concurrency rules. Derive contract tests from agreed behavior. For external consumers use expand, migrate, contract; for callers owned in the same repository migrate and delete in one verified change. Read [refactoring](../refactoring/SKILL.md) for the detailed migration branches.

Python 3 helpers: from the project root run `python3 <this-skill>/scripts/setup_plan.py --json`. It resolves `.lanyant/feature.json` or `LANYANT_FEATURE_DIRECTORY`, preserves existing plans, and copies [the bundled template](assets/plan-template.md) only when needed. The project can override templates; composing manifest layers additionally need PyYAML. Use [agent context](references/agent-context.md) when managed plan pointers belong in agent instructions. `python3 <this-skill>/scripts/update_agent_context.py [plan_path]` requires a configured JSON or YAML context target; YAML syntax beyond JSON requires PyYAML. Report a missing dependency as blocked; a successful no-op is not a context update.
