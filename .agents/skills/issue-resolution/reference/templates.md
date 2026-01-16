# Issue Resolution Templates

## Issue Brief Template

````markdown
# Issue Brief: <Short Title>

**ID**: <issue-id>
**Date**: <date>
**Reported by**: <user or system>
**Severity**: CRITICAL / HIGH / MEDIUM / LOW
**Type**: Regression / Edge case / Race condition / UI / Performance / Other
**Reproduction Required**: Failing test / Manual OK

## Symptom

<Clear description of what is happening>

## Expected Behavior

<What should happen instead>

## Reproduction

### Steps (if manual)

1. <Step 1>
2. <Step 2>
3. <Step 3>
4. Observe: <symptom>

### Test (if exists)

```bash
bun test <file> --filter "<test name>"
```
````

### Conditions

- Environment: dev / staging / prod
- Data state: <relevant data conditions>
- User type: <if relevant>

## Evidence

### Error Message

```
<Exact error message>
```

### Stack Trace

```
<Full stack trace if available>
```

### Logs

```
<Relevant log entries>
```

### Screenshots

<If UI issue, attach screenshots>

## Affected Area

- **Files**: `<list affected files if known>`
- **Modules**: `<list affected modules>`
- **Features**: `<list affected features>`

## Timeline

- **When did it start**: <date/time or "unknown">
- **Last known working**: <date/time or "unknown">
- **Recent changes in area**: <list relevant commits>

## Additional Context

<Any other relevant information>
```

---

## Reproduction Report Template

````markdown
# Reproduction Report: <Issue Title>

**Issue ID**: <issue-id>
**Date**: <date>

## Reproduction Method

- [ ] Failing test created
- [ ] Manual reproduction documented

### Failing Test

**File**: `<path to test file>`
**Test name**: `<test name>`

```typescript
// Test code
it('should <expected behavior>', async () => {
  // Setup
  const input = ...

  // Execute
  const result = await functionUnderTest(input)

  // Assert - THIS CURRENTLY FAILS
  expect(result).toEqual(expectedValue)
})
```
````

### Manual Reproduction

1. <Step 1>
2. <Step 2>
3. Observe: <symptom>

Reproducible: Always / Sometimes / Rarely

## Error/Behavior Captured

### Actual Output

```
<Exact error or unexpected output>
```

### Expected Output

```
<What should have been output>
```

## Code Path

### Stack Trace Analysis

1. **Entry**: `<file>:<line>` - `<function>`
2. **Calls**: `<file>:<line>` - `<function>`
3. **Calls**: `<file>:<line>` - `<function>`
4. **Fails at**: `<file>:<line>` - `<function>`

### Traced with gkg

```
gkg get_definition → <findings>
gkg get_references → <findings>
```

## Recent Changes

### Git Log (affected files)

```
<commit-hash> <date> <author> - <message>
<commit-hash> <date> <author> - <message>
```

### Git Blame (relevant lines)

```
<blame output for problematic lines>
```

## Notes

<Any observations during reproduction>
```

---

## RCA Report Template

```markdown
# Root Cause Analysis: <Issue Title>

**Issue ID**: <issue-id>
**Date**: <date>
**Iteration**: <N>

## Iteration History

| Iteration | Hypothesis   | Outcome                |
| --------- | ------------ | ---------------------- |
| 1         | <hypothesis> | ELIMINATED / CONFIRMED |
| 2         | <hypothesis> | ELIMINATED / CONFIRMED |

## Hypotheses Considered

### Hypothesis A: <Description>

**Likelihood**: HIGH / MEDIUM / LOW

**Reasoning**:
<Why this could be the cause>

**Supporting Evidence**:

- <Evidence that supports this hypothesis>
- <Evidence that supports this hypothesis>

**Refuting Evidence**:

- <Evidence against this hypothesis>

**Verdict**: ✓ CONFIRMED / ✗ ELIMINATED / ? NEEDS MORE EVIDENCE

---

### Hypothesis B: <Description>

**Likelihood**: HIGH / MEDIUM / LOW

**Reasoning**:
<Why this could be the cause>

**Supporting Evidence**:

- <Evidence>

**Refuting Evidence**:

- <Evidence>

**Verdict**: ✓ CONFIRMED / ✗ ELIMINATED / ? NEEDS MORE EVIDENCE

---

## Root Cause (Confirmed)

### The Cause

<Clear, concise statement of the root cause>

### Causal Chain
```

1. <Initial condition or trigger>
      │
      ▼
2. <Intermediate state or action>
      │
      ▼
3. <Further consequence>
      │
      ▼
4. <Symptom observed>

```

### Evidence That Confirms

- <Key evidence point>
- <Key evidence point>
- <Key evidence point>

## Why This Happened

### Immediate Cause
<The direct code issue - e.g., missing null check>

### Underlying Cause
<Why the code was written this way - e.g., assumption that input is always valid>

### Systemic Cause (if applicable)
<Process or design issue - e.g., no validation layer, missing tests>

## Fix Approach

### Immediate Fix
<What code change will resolve the symptom>

### Preventive Measures
<How to prevent similar bugs in future>
- [ ] Add test coverage for edge case
- [ ] Add input validation
- [ ] Update documentation
- [ ] Add runtime check

## Verification Plan

The fix is correct if:
- [ ] Regression test changes from failing to passing
- [ ] Original symptom no longer reproducible
- [ ] No new test failures
- [ ] Types check passes
- [ ] Build succeeds
```

---

## Impact Report Template

```markdown
# Impact Assessment: <Issue Title>

**Issue ID**: <issue-id>
**Date**: <date>

## Fix Summary

<Brief description of the proposed fix>

## Blast Radius

### Files Directly Modified

| File     | Change                  |
| -------- | ----------------------- |
| `<file>` | <description of change> |
| `<file>` | <description of change> |

### Callers of Modified Code

Found via `gkg get_references`:

| Caller       | File     | Risk         |
| ------------ | -------- | ------------ |
| `<function>` | `<file>` | HIGH/MED/LOW |
| `<function>` | `<file>` | HIGH/MED/LOW |

### Related Code (Similar Patterns)

<Code that might have the same bug or be affected by the fix>

| Location | Pattern   | Needs Same Fix?  |
| -------- | --------- | ---------------- |
| `<file>` | <pattern> | Yes / No / Maybe |

## Regression Risk

**Overall Risk Level**: HIGH / MEDIUM / LOW

### Risk Factors

| Factor                 | Present? | Impact   |
| ---------------------- | -------- | -------- |
| High-traffic code path | Y/N      | <impact> |
| Public API change      | Y/N      | <impact> |
| Shared utility         | Y/N      | <impact> |
| Database schema        | Y/N      | <impact> |
| External integration   | Y/N      | <impact> |

### Mitigation

<How to reduce regression risk>
- <Mitigation 1>
- <Mitigation 2>

## Test Coverage

### Existing Tests

| Test          | File     | Covers           |
| ------------- | -------- | ---------------- |
| `<test name>` | `<file>` | <what it covers> |

### Tests to Add

| Test          | Purpose                 |
| ------------- | ----------------------- |
| `<test name>` | <what it should verify> |

## Spike Validation (if needed)

**Spike required**: Yes / No

**Reason**: <why spike is/isn't needed>

**Spike location**: `.spikes/<issue-id>/`

**Spike result**: <summary of findings>

## Deployment Considerations

- [ ] Feature flag needed?
- [ ] Gradual rollout?
- [ ] Rollback plan?
- [ ] Monitoring/alerting updates?

## Sign-off

- [ ] Impact assessment reviewed
- [ ] Risk level acceptable
- [ ] Test plan approved
- [ ] Ready to proceed with fix
```

---

## Fix Bead Template

````markdown
# Fix: <Issue Title>

**Type**: bug
**Priority**: <0-4>
**Fixes**: <issue-id>

## Root Cause Summary

> <Brief summary from RCA>

## Fix Implementation

### What to Change

<Description of the fix>

### Why This Fixes It

<Explanation of how the fix addresses the root cause>

## Files to Modify

| File     | Change           |
| -------- | ---------------- |
| `<file>` | <what to change> |
| `<file>` | <what to change> |

## Implementation Notes

<Any gotchas, edge cases, or specific approaches to use>

### Reference

- RCA: `history/issues/<id>/rca.md`
- Spike (if any): `.spikes/<id>/`

## Acceptance Criteria

- [ ] Regression test passes: `<test file>:<test name>`
- [ ] Original symptom no longer reproducible
- [ ] No new test failures in affected area
- [ ] Full test suite passes
- [ ] `bun run check-types` passes
- [ ] `bun run build` passes

## Verification Steps

```bash
# 1. Run regression test
bun test <test-file> --filter "<test name>"

# 2. Run related tests
bun test <affected-area>

# 3. Full suite
bun run test

# 4. Type check and build
bun run check-types
bun run build
```
````

```

```
