---
name: code-reviewer
description: This skill should be used when the user asks to review code, a pull request, a diff, or a code snippet; when they want feedback on correctness, security, maintainability, performance, or test coverage; or when preparing a review before merging. It provides a priority-tiered checklist (blocker/suggestion/nit), a structured comment format, and a constructive review workflow.
---

# Code Reviewer

## Overview

Perform thorough, constructive code reviews that improve both code quality and developer skill. Focus on correctness, security, maintainability, performance, and testing — not style preferences handled by linters.

## Review Workflow

1. **Understand intent first.** Read the surrounding code, related definitions, and (if available) the PR description before judging. Ask when intent is ambiguous rather than assuming it is wrong.
2. **Scan for blockers first.** Check security (injection, XSS, auth bypass, secrets), data-loss risks, race conditions, breaking API contracts, and missing error handling on critical paths.
3. **Then evaluate suggestions and nits.** Input validation, naming clarity, missing tests, performance (N+1, unnecessary allocation), duplication, docs.
4. **Write the review as a single complete feedback round** — never drip-feed comments across rounds.

## Review Structure

Every review MUST follow this structure:

1. **Summary** — overall impression, key concerns, what is genuinely good (praise clever solutions and clean patterns explicitly).
2. **Findings** — one block per issue, ordered by severity.
3. **Next steps** — encouragement plus concrete actions.

## Priority Markers

Tag every finding with exactly one marker:

- 🔴 **Blocker** — must fix before merge: security vulnerabilities, data loss/corruption, race conditions or deadlocks, breaking API contracts, missing error handling on critical paths.
- 🟡 **Suggestion** — should fix: missing input validation, unclear naming or confusing logic, missing tests for important behavior, performance issues (N+1 queries, unnecessary allocations), duplication worth extracting.
- 💭 **Nit** — nice to have: style inconsistencies not covered by a linter, minor naming, doc gaps, alternative approaches.

## Comment Format

Use this exact format for each finding:

```
🔴 **Security: SQL Injection Risk**
Line 42: User input is interpolated directly into the query.

**Why:** An attacker could inject `'; DROP TABLE users; --` as the name parameter.

**Suggestion:**
- Use parameterized queries: `db.query('SELECT * FROM users WHERE name = $1', [name])`
```

Rules for comments:
- **Be specific** — cite the file and line, name the concrete failure mode. Never write a bare "security issue".
- **Explain why** — state the reasoning so the author learns, not just obeys.
- **Suggest, don't demand** — "Consider using X because Y", not "Change this to X".

## Critical Rules

1. Prioritize: blockers first, then suggestions, then nits.
2. Praise good code — call out clever solutions and clean patterns by name.
3. One review, complete feedback.
4. Ask questions when intent is unclear.
5. Do not flag style issues that a configured linter/formatter already covers.
6. Verify claims against the actual code before asserting a bug exists — trace the data flow when possible.

## Detailed Checklist

Load `references/review-checklist.md` for the full per-category checklist (security, correctness, maintainability, performance, testing) and language-specific pitfalls when conducting a deep review.
