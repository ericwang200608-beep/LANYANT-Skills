## User Input

```text
<user request>
```

## Outline

1. Read `.lanyant/feature.json` to get the feature directory path.

2. **Load context**: `.lanyant/memory/constitution.md` and `<feature_directory>/spec.md` and `<feature_directory>/plan.md` and `<feature_directory>/tasks.md`.

3. **Execute tasks** in order:
   - Complete each task before moving to the next
   - Mark completed tasks by changing `- [ ]` to `- [x]` in `<feature_directory>/tasks.md`
   - Halt on failure and report the issue

4. **Validate**: Verify all tasks are completed and the implementation matches the spec.
