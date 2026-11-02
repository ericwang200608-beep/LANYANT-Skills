---
description: "Create a feature specification (preset override)"
scripts:
  sh: scripts/bash/create-new-feature.sh "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 "{ARGS}"
---

## User Input

```text
<user request>
```

Given the feature description above:

1. **Create the feature directory and specification** with the bundled helper:
   - Bash: `python3 <suite>/business-discovery/scripts/new_feature.py --json --write-pointer --short-name "<short-name>" "<description>"`
   - The JSON output contains FEATURE_DIR, FEATURE_NUM and SPEC_FILE paths.

2. **Read the spec-template** to see the sections you need to fill.

3. **Write the specification** to SPEC_FILE, replacing the placeholders in each section
   (Overview, Requirements, Acceptance Criteria) with details from the user's description.
