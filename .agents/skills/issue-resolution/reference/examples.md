# Issue Resolution Examples

## Example 1: Regression Bug - Login Fails After Auth Refactor

### Input

**Type**: Error report from user

```
Error: Cannot read property 'id' of undefined
    at getUser (packages/application/src/usecases/get-user.ts:15)
    at handler (packages/api/src/routers/users.ts:42)
```

---

### Phase 0: Triage

**Input Type**: Error with stack trace

**Actions**:

```bash
# Parse stack trace - identify affected files
# packages/application/src/usecases/get-user.ts:15
# packages/api/src/routers/users.ts:42
```

**Severity Assessment**:

- Production error affecting login → CRITICAL
- Was working before → REGRESSION
- **Reproduction Required**: Failing test REQUIRED

**Issue Brief**:

```markdown
# Issue Brief: Login returns "Cannot read property 'id' of undefined"

**Severity**: CRITICAL
**Type**: Regression
**Repro Required**: Failing test

## Symptom

Login API returns 500 error with "Cannot read property 'id' of undefined"

## Expected

Login should return user token

## Evidence

Stack trace points to get-user.ts:15, called from users.ts:42
```

---

### Phase 1: Reproduction

**Create Failing Test**:

```typescript
// packages/application/src/__tests__/get-user.regression.test.ts
it('should handle user lookup correctly', async () => {
	const userId = 'user-123'
	const result = await getUser({ userId })

	// This currently fails with "Cannot read property 'id' of undefined"
	expect(result.id).toBe(userId)
})
```

**Run test**:

```bash
bun test packages/application/src/__tests__/get-user.regression.test.ts
# FAIL - Cannot read property 'id' of undefined
```

**Code Path Tracing**:

```bash
# Read the failing line
Read packages/application/src/usecases/get-user.ts

# Line 15: return { id: user.id, email: user.email }
# user is undefined!
```

**Recent Changes**:

```bash
git log --oneline -10 packages/application/src/usecases/get-user.ts
# abc123 - 2 days ago - "Refactor auth to use new user lookup"
```

---

### Phase 2: Root Cause Analysis

**Hypotheses**:

| #   | Hypothesis                                        | Likelihood |
| --- | ------------------------------------------------- | ---------- |
| A   | User lookup returns undefined instead of throwing | HIGH       |
| B   | User ID not passed correctly                      | MEDIUM     |
| C   | Database connection issue                         | LOW        |

**Evidence Gathering**:

```bash
# Check the refactor commit
git show abc123

# Found: Changed from `findUserOrThrow` to `findUser`
# findUser returns undefined when not found
# Old code expected exception, new code doesn't handle undefined
```

**Verdict**:

- Hypothesis A: CONFIRMED
- Cause: Refactor changed lookup behavior, but caller wasn't updated

**RCA Report**:

```markdown
## Root Cause (Confirmed)

**Cause**: Commit abc123 changed `findUserOrThrow` to `findUser`,
which returns `undefined` instead of throwing. Caller at line 15
assumes user is always defined.

**Causal Chain**:

1. User ID passed to getUser
2. findUser called (returns undefined for non-existent user)
3. Code tries to access user.id on undefined
4. TypeError thrown

## Fix Approach

Add null check before accessing user properties, or revert to throwing behavior.
```

---

### Phase 3: Impact Assessment

```bash
# Check who else uses findUser
gkg get_references findUser
# Found 5 other callers - all might have same bug!
```

**Impact Report**:

```markdown
## Blast Radius

- get-user.ts (current issue)
- update-user.ts (same pattern - VULNERABLE)
- delete-user.ts (same pattern - VULNERABLE)
- get-user-profile.ts (has null check - OK)
- admin-get-user.ts (has null check - OK)

## Regression Risk: MEDIUM

Need to fix 3 files, all internal use cases
```

---

### Phase 4: Fix Decomposition

```bash
bd create "Epic: Fix user lookup null handling" -t epic -p 0
# → bd-100

bd create "Add regression tests for user lookup edge cases" -t task --blocks bd-100
# → bd-101

bd create "Fix null handling in get-user.ts" -t bug --blocks bd-100 --deps bd-101
# → bd-102

bd create "Fix null handling in update-user.ts" -t bug --blocks bd-100 --deps bd-101
# → bd-103

bd create "Fix null handling in delete-user.ts" -t bug --blocks bd-100 --deps bd-101
# → bd-104
```

---

### Phase 5: Verification

```bash
# Run regression test - should pass now
bun test packages/application/src/__tests__/get-user.regression.test.ts
# PASS

# Run all user-related tests
bun test packages/application/src/__tests__/
# PASS

# Full suite
bun run test
# PASS

# Type check
bun run check-types
# PASS
```

---

## Example 2: Edge Case - Special Characters in Username

### Input

**Type**: Vague user report

```
"Can't create account with my name"
```

---

### Phase 0: Triage

**Clarification Questions**:

- What name are you trying to use?
- What error do you see?
- What browser/device?

**User Response**:

```
Name: "José García"
Error: "Invalid username"
Browser: Chrome
```

**Issue Brief**:

```markdown
# Issue Brief: Cannot create account with accented characters

**Severity**: MEDIUM
**Type**: Edge case
**Repro Required**: Failing test PREFERRED

## Symptom

Usernames with accented characters (José, García) rejected as "Invalid"

## Expected

Unicode characters should be accepted in names
```

---

### Phase 1: Reproduction

**Create Failing Test**:

```typescript
it('should accept unicode characters in username', () => {
	const result = validateUsername('José García')
	expect(result.valid).toBe(true)
})
```

**Trace**:

```bash
gkg search_definitions validateUsername
# Found: packages/domain/src/validation/username.ts

Read packages/domain/src/validation/username.ts
# Line 5: const VALID_PATTERN = /^[a-zA-Z0-9_]+$/
# Only allows ASCII letters!
```

---

### Phase 2: Root Cause Analysis

**Root Cause**: Regex pattern only allows ASCII letters, excludes unicode.

**No iteration needed** - cause is obvious from code inspection.

---

### Phase 3: Impact Assessment

```bash
gkg get_references validateUsername
# Used in: signup, profile-update
```

**Regression Risk**: LOW - expanding validation is additive.

---

### Phase 4: Fix Decomposition

Single bead (simple fix):

```bash
bd create "Fix: Allow unicode in username validation" -t bug -p 2
```

**Fix**:

```typescript
// Change from:
const VALID_PATTERN = /^[a-zA-Z0-9_]+$/

// To:
const VALID_PATTERN = /^[\p{L}\p{N}_]+$/u // Unicode letters and numbers
```

---

### Phase 5: Verification

```bash
bun test packages/domain/src/__tests__/username.test.ts
# PASS - José García now accepted
```

---

## Example 3: Race Condition - Duplicate Records

### Input

**Type**: Intermittent bug report

```
"Sometimes getting duplicate order records"
```

---

### Phase 0: Triage

**Severity**: HIGH (data integrity)
**Type**: Race condition
**Repro Required**: Failing test REQUIRED (non-deterministic)

---

### Phase 1: Reproduction

**Challenge**: Race conditions are hard to reproduce deterministically.

**Approach**:

```typescript
it('should not create duplicate orders under concurrent requests', async () => {
	const orderId = 'order-123'

	// Simulate concurrent requests
	const results = await Promise.all([
		createOrder({ orderId }),
		createOrder({ orderId }),
		createOrder({ orderId }),
	])

	// Only one should succeed, others should fail or be deduplicated
	const successes = results.filter((r) => r.success)
	expect(successes.length).toBe(1)
})
```

**Stress test**:

```bash
# Run 100 times to catch race condition
for i in {1..100}; do bun test order.race.test.ts; done
```

---

### Phase 2: Root Cause Analysis

**Add timing logs**:

```typescript
console.log(`[${Date.now()}] Checking if order exists: ${orderId}`)
// ... check
console.log(`[${Date.now()}] Order not found, creating`)
// ... create
```

**Oracle Analysis**:

```
oracle(
  task: "Analyze race condition in order creation",
  context: """
    Pattern: Check-then-create
    Timing logs show both requests see "not found" before either creates

    What's the fix?
  """,
  files: ["packages/application/src/usecases/create-order.ts"]
)
```

**Root Cause**: Classic TOCTOU (time-of-check to time-of-use) race.

- Request A checks, order doesn't exist
- Request B checks, order doesn't exist
- Request A creates order
- Request B creates order (duplicate!)

---

### Phase 3: Impact Assessment

**Fix Options**:

1. Database unique constraint (let DB handle it)
2. Distributed lock (complex)
3. Upsert instead of check-then-insert

**Spike**: Test upsert approach

```bash
bd create "Spike: Test upsert for order creation" -t task -p 0
```

---

### Phase 4: Fix Decomposition

```bash
bd create "Fix: Prevent duplicate orders with upsert" -t bug -p 1
```

**Fix**:

```typescript
// Change from check-then-create to upsert
const order = await db.orders.upsert({
	where: { orderId },
	create: { orderId, ...data },
	update: {}, // No-op if exists
})
```

---

### Phase 5: Verification

```bash
# Run stress test 100 times
for i in {1..100}; do bun test order.race.test.ts || exit 1; done
# All pass - no duplicates
```

---

## Decision Tree Summary

```
Issue arrives
     │
     ▼
What type of input?
├── Vague report → Clarify, explore, reproduce
├── Error/Stack → Parse, locate, reproduce
└── Failing test → Run, trace, analyze
     │
     ▼
What type of bug?
├── Regression → git bisect to find breaking commit
├── Edge case → Analyze boundaries, find missing validation
├── Race condition → Add timing, stress test, fix concurrency
├── Data corruption → Trace state flow, find invariant violation
└── External dep → Check versions, API changes
     │
     ▼
Complex fix?
├── Yes → Multiple beads with deps
└── No → Single bead with test
     │
     ▼
Fix works?
├── Yes → Done!
└── No → Loop back to RCA with new evidence
```
