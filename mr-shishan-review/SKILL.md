---
name: mr-shishan-review
description: Review the current merge request, pull request, git diff, or changed files specifically for legacy-code smells and "shishan code" patterns. Use when Codex needs to inspect MR changes for avoidable maintainability debt such as write-time vs read-time filtering mistakes, repeated fully qualified namespaces in business logic, unnecessary serialization overhead caused by repeated serialization and deserialization, redundant pass-through wrappers that add no useful boundary or semantics, deeply nested or repetitive if branches that should be flattened, duplicated code that should be extracted, or similar low-quality patterns before merge.
---

# MR Shishan Review

Review only the code introduced or modified by the current MR, but read enough surrounding code to avoid shallow or incorrect comments. Focus on maintainability debt that should be fixed before the pattern spreads.

## Workflow

1. Determine the review scope from the MR diff, staged diff, explicit patch, or changed files.
2. Read the local context around each changed hunk before judging.
3. Look for shishan patterns first; do not spend most of the review on generic style issues.
4. Report only findings supported by code evidence. Prefer fewer precise findings over many weak guesses.
5. Give a better pattern or refactoring direction for every finding.

## What Counts As Shishan Code

Treat the following as the primary smell categories:

- Write dirty, read clean: data written into a database, cache, queue payload, or persistent object without normalization/filtering, then repeatedly filtered on read paths.
- Namespace spam in business logic: repeated fully qualified class/module/package names inside the same logical block instead of import, alias, constant, helper, or local abstraction.
- Unnecessary serialization overhead: repeated serialization and deserialization, or equivalent format conversion ping-pong, without crossing a real boundary such as storage, network, IPC, or framework contract.
- Redundant wrappers: pass-through classes, functions, result objects, or state holders that only rename or forward an existing call/value without adding a stable boundary, invariant, validation, adaptation, lifecycle control, observability, reuse, or test seam. Prefer deleting the wrapper and using the underlying abstraction directly.
- Nested if pyramids: control flow that can be flattened with guard clauses, early return, extracted predicates, or dispatch tables.
- Copy-paste logic: repeated branches, transformations, validation, mapping, or side-effect orchestration that should be extracted into one function.

Also flag adjacent smells when they appear in MR code:

- Magic literals copied across branches instead of constants or enums.
- Repeated key-path or field-name strings that create drift risk.
- Large functions that mix validation, transformation, persistence, and side effects.
- Readability workarounds that hide missing domain modeling, such as ad hoc booleans or temporary dict reshaping.
- Repeated database or cache cleanup on read paths that suggests the write path is wrong.

## Review Rules

1. Review the MR, not the whole repository. Mention pre-existing code only when the MR extends or depends on the smell.
2. Prefer maintainability findings over formatting nits.
3. Do not call something a smell without naming the concrete waste or risk:
   repeated CPU work, repeated I/O, schema drift, harder testing, hidden invariants, branching complexity, duplicated bug surface, or readability loss.
4. Distinguish between justified duplication and bad duplication. Small duplication is acceptable when flows are genuinely diverging.
5. Do not flag necessary serialization at system boundaries.
6. When flagging repeated serialization and deserialization, explicitly state why it is unnecessary overhead rather than a required boundary conversion.
7. When flagging a redundant wrapper, identify the direct replacement and explain what the wrapper fails to add. Do not flag adapters, anti-corruption layers, compatibility boundaries, lifecycle/ownership controls, observability hooks, reusable policy enforcement, or deliberate test seams merely because their implementation is currently thin.
8. Do not insist on abstraction unless it clearly reduces repeated logic or repeated domain knowledge.
9. If a pattern is suspicious but not provable from the diff, say what must be verified instead of overstating.

## Output Format

Use this structure:

1. Summary
2. Findings
3. Suggested cleanup order

For each finding, use this format:

```text
🟡 [Category] file_path:line
What changed in the MR:
Why this is shishan code:
Why this is unnecessary overhead:
Better direction:
```

Severity guidance:

- `🔴` Must fix before merge because the MR introduces persistent bad data, major duplicated logic, or complexity that will immediately spread.
- `🟡` Should fix because the smell adds clear maintenance cost and the cleanup is local enough to do now.
- `💭` Optional cleanup because the smell is real but refactoring may be better done in follow-up work.

## Category Guidance

Load [references/shishan-checklist.md](references/shishan-checklist.md) when performing a full review. Use it to classify findings and to pressure-test whether the smell is real, local to the MR, and worth commenting on.
