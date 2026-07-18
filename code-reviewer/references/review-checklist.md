# Code Review Checklist — Full Reference

Load this when conducting a deep review. Check each category; report only what applies.

## 🔴 Blockers

### Security
- [ ] SQL/NoSQL injection: user input interpolated into queries; use parameterized queries or ORM bindings.
- [ ] XSS: unescaped user content rendered into HTML; check template auto-escaping is enabled, avoid `dangerouslySetInnerHTML` / `innerHTML` with dynamic data.
- [ ] Command injection: `exec`/`system`/shell calls with user input; prefer argv arrays over string interpolation.
- [ ] Path traversal: file paths built from user input; validate against an allowlist or resolve+prefix-check.
- [ ] AuthN/AuthZ: every new endpoint checks authentication AND object-level authorization (IDOR — verify the requested resource belongs to the caller).
- [ ] Secrets: no hardcoded tokens, keys, passwords; no secrets logged.
- [ ] Deserialization: no `pickle`/`eval`/`yaml.load` on untrusted data.
- [ ] SSRF: outbound requests to user-controlled URLs; validate scheme/host allowlists.
- [ ] Crypto: no MD5/SHA1 for passwords; use bcrypt/scrypt/argon2; no hand-rolled crypto; secure randomness for tokens.

### Correctness & Data Safety
- [ ] Data loss: deletes without confirmation/soft-delete, destructive migrations, missing transactions for multi-step writes.
- [ ] Race conditions: check-then-act (TOCTOU), shared mutable state without locks, missing unique constraints backing upserts.
- [ ] Error handling: critical paths have failure handling; errors are not silently swallowed (`except: pass`, empty `.catch()`); partial failures leave consistent state.
- [ ] API contracts: response shape, status codes, and error formats match the documented/expected contract; no breaking rename/removal without versioning.
- [ ] Boundary conditions: off-by-one, empty collections, null/None on first/last element, overflow, timezone/date edge cases.

## 🟡 Suggestions

### Input Validation
- [ ] External input (HTTP params, env vars, file contents, webhooks) validated at the boundary: type, range, length, format.
- [ ] Validation errors return actionable messages, not stack traces.

### Maintainability
- [ ] Names explain intent; booleans read as predicates (`isReady`, `hasItems`).
- [ ] Functions do one thing; flag functions > ~50 lines or nesting > 3 levels.
- [ ] Duplication: 3+ copies of logic → extract; 2 copies with divergence risk → consider extracting.
- [ ] Magic numbers/strings are named constants.
- [ ] Comments explain *why*, not *what*; dead code and commented-out blocks removed.

### Performance
- [ ] N+1 queries: lookups inside loops over collections; require batch/ prefetch / join.
- [ ] Unbounded queries: missing pagination/LIMIT on list endpoints.
- [ ] Unnecessary allocations in hot loops; repeated regex compilation; string concat in loops (use join/builders).
- [ ] Blocking I/O on async paths; missing timeouts and retries with backoff on network calls.
- [ ] Indexes exist for new query patterns (check migrations).

### Testing
- [ ] New behavior has tests: happy path + at least one failure/edge case.
- [ ] Tests assert behavior, not implementation details; no tests that can't fail.
- [ ] Bug fixes include a regression test that fails without the fix.

## 💭 Nits
- Naming polish, doc gaps, ordering, alternative idioms worth mentioning — only if not linter-covered.

## Language-Specific Pitfalls (spot check)

- **Python**: mutable default args (`def f(x=[])`), late-binding closures in loops, `==` vs `is` for None, bare `except`, sync calls in async handlers.
- **JavaScript/TypeScript**: `==` vs `===`, floating-point money math, missing `await` on promises, unhandled promise rejection, prototype pollution via object merge, `any` leaking type safety.
- **Go**: goroutine leaks, `defer` in loops, unclosed response bodies, ignored returned errors, slice aliasing in range loops (`for _, v := range` capture).
- **Java**: `equals`/`hashCode` contract, unclosed resources (use try-with-resources), string concat in loops, `SimpleDateFormat` thread-safety.
- **SQL**: `SELECT *`, missing WHERE on UPDATE/DELETE, implicit type casts defeating indexes.

## Review Tone Reminders
- State observations, then reasons, then suggestions.
- Treat the author as competent; assume constraints you cannot see.
- One round of complete feedback; end with actionable next steps.
