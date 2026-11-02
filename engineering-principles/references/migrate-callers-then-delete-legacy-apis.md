# Migrate Callers Then Delete Legacy APIs

**When it applies:** Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers.

- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative

**Scope:** Use this only when every caller is in this repository ([operating rule 5.6](../../ask-eric/references/operating-rules.md#5-rules-that-resolve-competing-practices)). When an interface has consumers you do not control (published packages, public APIs, other teams' services, persisted data or wire formats read elsewhere), change it with expand, migrate, contract instead; see [refactoring](../../refactoring/SKILL.md).
