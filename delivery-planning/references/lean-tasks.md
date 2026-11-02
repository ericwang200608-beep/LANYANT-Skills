## User Input

```text
<user request>
```

## Outline

1. Read `.lanyant/feature.json` to get the feature directory path.

2. **Load context**: `.lanyant/memory/constitution.md` and `<feature_directory>/spec.md` and `<feature_directory>/plan.md`.

3. Create dependency-ordered implementation tasks and store them in `<feature_directory>/tasks.md`.
   - Every task uses checklist format: `- [ ] [TaskID] Description with file path`
   - Organized by phase: setup, foundational, user stories in priority order, polish
