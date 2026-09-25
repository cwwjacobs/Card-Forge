# UKSL — Schema capability guard

## Map

Objective: repair the scoped PR review finding.

Plan: Reject unsupported schema keywords and unsupported keyword forms during schema loading; traverse schema-valued positions only; exercise negative and positive cases and repository fixtures.

Boundary: Standard-library validator remains a deliberately limited subset; no new JSON Schema implementation.

Authority: Corey authorized map → execute → audit → push; the delegated worker is YELLOW. Root independently audits and owns push. No nested delegation.

Source: https://terminusprotocol.io, Canon v0.5 (root verified). Ultra keeps the goal, kernel, bounds, dependencies, and receipts; each local KSL maps (Stage 1), builds (Stage 2), and checks adherence plus tests (Stage 3). Failure returns to the owning map before repair. A local pass permits progression; root audits the composed result before pushing.

## Execute

Added schema capability validation at load time, with recursion only through properties values and items; added unit-test CI gate. Unknown keywords and unsupported forms fail visibly, including constraints on absent optional fields.

## Audit

PASS locally: 6 guard tests; all 15 pre-existing negative fixtures; repository records validated and 38 cross-references checked. Property names and annotation/enum payloads remain data. git diff --check passed. Root audit/push pending.
