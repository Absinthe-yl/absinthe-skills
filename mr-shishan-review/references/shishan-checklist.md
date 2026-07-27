# Shishan Checklist

Use this checklist while reviewing MR changes for maintainability debt. The goal is not to maximize comments. The goal is to catch new low-quality patterns before they fossilize.

## 1. Write Dirty, Read Clean

Flag when the MR writes raw or noisy data into a database, cache, search index, message, or persisted struct and relies on later readers to clean it.

Look for:

- Filtering empty values, invalid values, or duplicates only during reads.
- Writing oversized or mixed-format payloads, then trimming fields every time they are fetched.
- Cache values that require repeated cleanup before use.
- Persisting nullable or sentinel-heavy shapes when the write path already knows the desired canonical form.

Why it matters:

- Every consumer pays the cleanup cost.
- Bad data spreads to new readers.
- Invariants become implicit and easy to break.

Prefer:

- Normalize, deduplicate, filter, and shape data before write.
- Store one canonical representation.
- Keep read paths simple.

## 2. Namespace Spam In Business Logic

Flag when the MR repeatedly writes full package, namespace, or class paths inside a function or business flow.

Look for:

- The same long type path repeated in several branches.
- Builder/helper invocations that use full namespaces inline instead of import or alias.
- Domain code cluttered by infrastructure package names.

Why it matters:

- Noise hides the actual logic.
- Renames become expensive and error-prone.
- Repetition often signals missing local abstraction.

Prefer:

- Imports, aliases, constants, local helper functions, or extracted objects.
- Short domain-facing names inside the business flow.

## 3. Unnecessary Serialization Overhead

Flag when the MR repeatedly serializes and deserializes data without crossing a real boundary.

Look for:

- Object -> JSON -> object inside one request path.
- Map -> string -> map just to access or tweak fields.
- Re-encoding cached values multiple times in the same flow.
- Struct copying implemented through serialization instead of explicit mapping.
- Repeated marshal/unmarshal or encode/decode in adjacent steps that could share one native in-memory representation.

Do not flag:

- Real persistence boundaries.
- Network boundaries.
- Framework APIs that require a specific format.

Why it matters:

- Burns CPU and memory.
- Hides domain intent behind format gymnastics.
- Adds failure modes for encoding, decoding, and schema mismatch.
- Creates pure overhead without adding correctness or boundary isolation.

Prefer:

- Keep values in native form until a real boundary.
- Extract field mapping helpers when conversion is required.
- In review comments, call this category "unnecessary serialization overhead" rather than just "serialization churn".

## 4. Flatten If Pyramids

Flag when the MR adds nested conditionals that can be flattened locally.

Look for:

- Three or more nesting levels.
- Outer `if` blocks that only guard the happy path.
- Repeated null, empty, or type checks inside nested branches.
- Large `if/else if` ladders that are really dispatch by state or type.

Why it matters:

- Harder to read and test.
- Hidden exit conditions.
- Small changes become dangerous because branches are interdependent.

Prefer:

- Guard clauses.
- Early return or continue.
- Extracted predicate helpers.
- Dispatch maps, strategy objects, or state-specific handlers when appropriate.

## 5. Extract Repetition

Flag when the MR repeats meaningful logic, not just a couple of incidental lines.

Look for:

- Similar validation in multiple handlers.
- Repeated field mapping or defaulting logic.
- Same error handling or logging choreography in several branches.
- Repeated cache/database wrapper logic.

Why it matters:

- Bugs get fixed in one copy and missed in another.
- Behavior drifts across branches.
- Review and testing cost grows linearly with copies.

Prefer:

- One helper with a clear name.
- One domain function per repeated behavior.
- One reusable mapper or validator.

## 6. Extra Smells Worth Commenting On

Comment only when they are meaningfully present in the MR:

- Same literal values repeated across branches.
- Domain knowledge encoded as scattered strings.
- One function doing validation, conversion, persistence, and side effects together.
- Temporary data reshaping that exists only to satisfy a messy local design.

## 7. Comment Quality Bar

Before leaving a finding, confirm all of the following:

- The smell is introduced or expanded by this MR.
- The problem is visible from the changed code plus nearby context.
- The comment names the exact waste or maintenance risk.
- The suggested direction is smaller and cleaner than the current approach.
- The comment is not just "this feels ugly".
