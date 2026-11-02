# Visual parity

You own pixel-exact equivalence. The baseline is the spec. You do not touch it. Equivalence is verified by image diff, not by eye.

Use this for any migration whose rendered output must stay identical: a styling system swap, a component library change, a framework port, or matching two implementations.

## Procedure

1. **Establish the baseline first, before any migration.** Build a visual regression harness that screenshots the current component across its states (for example with Playwright screenshots, or the project's verification harness in [verification-harness](../../verification-harness/SKILL.md)), plus the target when matching two implementations. Fix viewport, fonts, device scale, animation, time, and data so runs are deterministic, and run the harness twice on unchanged code to confirm a zero diff against itself. No baseline, no parity claim. This is a blocking prerequisite, not a follow-up.
2. **State and hold the anti-shortcut rules:**
   - no harness modifications,
   - no baseline tampering (no re-capturing, editing, or deleting baseline images),
   - no component restructuring to make a diff pass.

   If the baseline looks wrong, stop and ask the owner; do not edit it. Include these rules verbatim in every brief you give a delegated agent.
3. **Migrate one component at a time.** Shared primitives migrate first as a blocking phase. Then parallelize across worktrees, one owner per component ([separate-before-serializing-shared-state](../../engineering-principles/references/separate-before-serializing-shared-state.md)), using [multi-agent-delivery](../../multi-agent-delivery/SKILL.md) for the worktrees and integration branch and [harness-adapters](../../multi-agent-delivery/references/harness-adapters.md) for spawning. Without agents or worktrees, migrate sequentially and record the gap.
4. **Verify each component against its baseline via image diff** on the matching surface, using the project's verification harness or real-surface driving tools. A nonzero diff is a fail. Investigate the pixel delta. Iterate per component until the diff is zero. Check delegated work yourself: open the diff images and confirm the screenshots are not blank or of the wrong state before accepting a zero.
5. **Deliver per component or per safe batch.** When PRs are in scope and authorized, hand off to [pr-delivery](../../pr-delivery/SKILL.md).

## Reply

Components migrated, the diff result for each, the baseline harness location, what is left.
