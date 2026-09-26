# Form migration review

## Mapping exercise

Inventory every source question, field type, required rule, conditional visibility, calculation, notification and downstream destination. Assign a stable source-to-target identifier and record unsupported features for human resolution. The sample uses identical fictional field names on both sides to make a calculation error obvious; a real migration should not assume matching names. Preserve accessible labels, help text and error behavior in a real sandbox.

## Acceptance plan

1. Prepare test cases for every conditional branch, edge value, required error, calculated result, attachment and notification variant. Use only fictional respondents.
2. Independently verify each expected source outcome; this tool compares two simulated schemas but doesn't know whether the source is correct.
3. Run parity checks. Any mismatch is a review item, not an automatic rewrite instruction.
4. Build a real destination form only after checking the platform's current feature support and account plan. Confirm routing, permission, retention and email recipients before sending a live test.
5. Run human usability and accessibility checks, then validate exported records in their true downstream destination. Keep rollback and source form available during cutover.

## Tests and limits

Six unit tests cover the intentionally bad calculation, corrected target, hidden/visible required fields, invalid choice and duplicate schema keys. Missing: complex formulas, cross-field dependency graphs, exact numeric formatting, repeating sections, files, webhooks, notifications and vendor API payloads. Decimal arithmetic is local only. This is not a browser test or certified parity with Zoho Forms.
