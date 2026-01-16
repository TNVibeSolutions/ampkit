# Planning Templates

## Discovery Report Template

```markdown
# Discovery Report: <Feature Name>

**Date**: <date>
**Requested by**: <user>

## 1. Feature Summary

<1-2 sentence description of what the user wants>

## 2. Architecture Snapshot

### Relevant Packages

| Package                | Purpose         | Key Files |
| ---------------------- | --------------- | --------- |
| `packages/domain`      | Entities, ports | ...       |
| `packages/application` | Use cases       | ...       |
| ...                    | ...             | ...       |

### Entry Points

- API: `packages/api/src/routers/...`
- UI: `apps/web/src/routes/...`
- Server: `apps/server/src/...`

## 3. Existing Patterns

### Similar Implementations

| Feature   | Location                               | Pattern Used            |
| --------- | -------------------------------------- | ----------------------- |
| User CRUD | `packages/domain/src/entities/user.ts` | Entity + Port + UseCase |
| ...       | ...                                    | ...                     |

### Reusable Utilities

- Validation: `packages/domain/src/validation/...`
- Error handling: `packages/contracts/src/errors/...`
- ...

### Naming Conventions

- Entities: `PascalCase` (e.g., `Invoice`)
- Ports: `kebab-case` with `-repository` suffix
- Use cases: `kebab-case` with verb prefix (e.g., `create-invoice.ts`)

## 4. Technical Constraints

### Dependencies

- Node: `>=18`
- Key packages: `drizzle-orm`, `better-auth`, `oRPC`
- New deps needed: <list any new dependencies>

### Build Requirements

- Must pass: `bun run check-types`
- Must pass: `bun run build`

### Database

- ORM: Drizzle
- Schema location: `packages/db/src/schema/`
- Migrations: `bun run db:push` (dev) / `db:migrate` (prod)

## 5. External References

### Library Documentation

- <Library>: <URL or summary>

### Similar Projects

- <Project>: <How they solved similar problem>

## 6. Open Questions

- [ ] <Question needing clarification>
- [ ] <Uncertainty to resolve>

## 7. Clarifications

| Question | Answer | Impact |
| -------- | ------ | ------ |
| ...      | ...    | ...    |

**User Confirmation**: <timestamp or "Skipped - requirements clear">
```

---

## Approach Document Template

```markdown
# Approach: <Feature Name>

**Based on**: Discovery Report
**Date**: <date>

## 1. Gap Analysis

| Component | Have                    | Need                   | Gap Size |
| --------- | ----------------------- | ---------------------- | -------- |
| Entity    | None                    | `Invoice` entity       | New      |
| Port      | None                    | `InvoiceRepository`    | New      |
| Use case  | None                    | `CreateInvoice`        | New      |
| API       | Existing router pattern | New `/invoices` router | Small    |
| UI        | Existing form patterns  | New invoice form       | Small    |
| External  | None                    | Stripe SDK             | New      |

## 2. Recommended Approach

<Description of the recommended strategy>

### Why This Approach

- <Reason 1>
- <Reason 2>

### Tradeoffs

- Pro: ...
- Con: ...

## 3. Alternative Approaches

### Option A: <Name>

- Description: ...
- Tradeoff: ...
- Why not chosen: ...

### Option B: <Name>

- Description: ...
- Tradeoff: ...
- Why not chosen: ...

## 4. Risk Map

| Component        | Risk Level | Reason                        | Verification Needed                    |
| ---------------- | ---------- | ----------------------------- | -------------------------------------- |
| Stripe SDK       | HIGH       | New external dependency       | Spike: Test SDK import, webhook typing |
| Invoice entity   | LOW        | Follows existing User pattern | None                                   |
| oRPC router      | LOW        | Existing pattern              | None                                   |
| Webhook handling | HIGH       | Novel, security-critical      | Spike: Signature verification          |

## 5. Spike Requirements

### Spike 1: Stripe SDK Integration

- **Question**: Can we import and type Stripe SDK correctly?
- **Time-box**: 30 min
- **Success**: Working import, typed customer object

### Spike 2: Webhook Signature

- **Question**: How to verify Stripe webhook signatures?
- **Time-box**: 30 min
- **Success**: Verified signature in test

## 6. Proposed Structure
```

packages/
domain/src/entities/invoice.ts # New entity
domain/src/ports/invoice-repository.ts
application/src/usecases/create-invoice.ts
infrastructure/src/db/invoice-repository.ts
contracts/src/invoice.ts # DTOs
db/src/schema/invoice.ts # Drizzle schema
api/src/routers/invoice.ts # oRPC router
apps/
server/src/container.ts # DI registration
web/src/routes/invoices/ # UI routes

```

## 7. Execution Order

1. Domain layer (entity, port) - no deps
2. Schema + Infrastructure (repo) - depends on domain
3. Application layer (use case) - depends on infra
4. API layer (router) - depends on application
5. UI layer - depends on API

Parallelizable: Domain + Schema can run in parallel
```

---

## Spike Bead Template

````markdown
# Spike: <Specific Question>

**Type**: spike
**Priority**: 0
**Time-box**: 30 minutes
**Output**: `.spikes/<feature>/<spike-id>/`

## Question

Can we <specific, answerable technical question>?

## Background

<Why this needs investigation before main implementation>

## Approach

1. <Step 1>
2. <Step 2>
3. <Step 3>

## Success Criteria

- [ ] Working throwaway code exists in `.spikes/`
- [ ] Answer documented: YES (with approach) or NO (with blocker)
- [ ] Learnings captured for embedding in main plan beads

## On Completion

```bash
# If successful:
bd close <id> --reason "YES: <working approach summary>"

# If blocked:
bd close <id> --reason "NO: <blocker>. Alternative: <suggestion>"
```
````

## Learnings Template

After completion, document:

```markdown
## Learnings from Spike <id>

### What Worked

- <Finding 1>
- <Finding 2>

### Gotchas

- <Watch out for X>
- <Don't forget Y>

### Recommended Approach

<Summary for main plan bead>

### Reference Code

See `.spikes/<feature>/<spike-id>/` for working example.
```

````

---

## Feature Bead with Embedded Learnings

```markdown
# <Action-oriented title>

**Type**: task
**Priority**: <0-4>
**Depends on**: bd-X, bd-Y

## Context

<Brief context on where this fits in the feature>

## Learnings from Spikes

> From spike bd-<id>:
> - <Key learning 1>
> - <Key learning 2>
>
> Reference: `.spikes/<feature>/<spike-id>/`

## Requirements

<What needs to be implemented>

## Technical Notes

- File locations: ...
- Patterns to follow: See `<existing-file>` for reference
- Gotchas: <from spike learnings>

## Acceptance Criteria

- [ ] <Criterion 1>
- [ ] <Criterion 2>
- [ ] <Criterion 3>
- [ ] Passes `bun run check-types`
- [ ] Passes `bun run build`

## File Scope

Files this bead will touch (for track assignment):
- `packages/domain/src/entities/<name>.ts`
- `packages/infrastructure/src/db/<name>-repository.ts`
````
