# Data Import Rehearsal and Reconciliation

Use only when this round involves historical data import. Execute in staging or an isolated test environment. Rehearsal authorization is not authorization for a production import.

## 1. Establish data scope and field mapping

Confirm which data must be imported, the source batch, and the target scope. Preserve original inputs and perform cleaning and transformations on working copies.

Record mappings between old and new fields, their types, and transformation rules, especially for identifiers, statuses, dates, units, quantities, and amounts. Follow confirmed business rules. Resolve decisions first when handling missing, duplicate, or incorrect data would change business meaning.

Identify duplicate records, missing required values, invalid values, and missing related objects. Record rules for accepting, rejecting, quarantining, or merging them. Do not silently discard invalid data or guess replacement values.

## 2. Check import and recovery procedures

Read the project's actual migration and import scripts. Confirm the target environment, parameters, and write behavior. For database schema changes, inspect and preview planned changes first and verify which operations the current tool version supports.

Define the rehearsal's data scope and how to identify it, along with how to recover or clean up this batch after failure. Keep necessary recovery points and identify affected data. Do not substitute wiping the entire environment for scoped recovery.

Every state-changing operation must answer: What happens if it runs twice in a row? What happens after a previous run fails halfway? Does re-execution reach the same correct final state?

Determine the next step from actual current state, not just what the previous run intended to do. Partially completed records or temporary files left by an import must be recognizable and handled according to the rules on the next run.

## 3. Trial import, then reconcile

First trial the import using samples covering main data shapes and error cases, then execute the scope agreed for this round. Record the input batch, script or version, execution results, and error details. A successful command exit does not establish data correctness.

At minimum, reconcile:

- Whether input records reconcile with accepted, rejected, skipped, merged, and other processing outcomes under explicit accounting rules.
- Whether counts of newly created or updated target records match mapping and deduplication rules.
- Whether critical quantities, amounts, and aggregates match independent reconciliation evidence.
- Whether relationships between parent records, line items, customers, suppliers, and other objects are correct.
- Whether imported data are usable through actual system queries or operations.

When merging, expanding rows, or updating existing records, explain why counts do not map one-to-one. Do not substitute a simple comparison of two totals for reconciliation. Trace discrepancies to specific records and explain their causes rather than reporting only an aggregate pass.

## 4. Verify repeated execution and failure recovery

Repeat the same batch within an isolated scope. Verify the agreed skip, update, or rejection rules without creating unintended duplicates.

Rehearse interruptions at failure points affecting this import's correctness. Verify that rerunning, recovery, or cleanup restores the agreed state. Record the failure points actually tested; do not claim a limited rehearsal verifies every possible interruption.

After recovery, recheck counts, amounts, and relationships, and confirm that data meant to survive from before the rehearsal remain intact. If unexplained discrepancies arise, stop subsequent acceptance work that depends on those data, preserve evidence, and investigate.

## 5. Save results

In the existing data reconciliation record, include requirement or scenario identifiers, candidate and script versions, environment, date, executor, mappings, processing rules, execution results, discrepancies, and evidence for repeated execution and recovery. When confirmed mappings or business rules change, identify affected batches and evidence, update the authoritative rules within authorization, and revalidate only affected work. State which items are verified, which remain unverified or awaiting business confirmation, and provide repeatable procedures.

Reference only necessary details and evidence. Do not duplicate or expose unrelated customer data.
