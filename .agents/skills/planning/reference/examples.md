# Planning Workflow Examples

## Example 1: New Feature - Billing Module with Stripe

### User Request

"Add a billing module with Stripe integration for subscription management"

---

### Phase 1: Discovery

**Parallel Sub-agents launched:**

```
Task("Explore packages/domain and packages/application structure for entity/usecase patterns")
Task("Search for existing payment or subscription code")
Task("Check package.json for existing Stripe or payment deps")
```

**Librarian query:**

```
librarian("How does a typical TypeScript project structure Stripe integration with Clean Architecture?")
```

**Exa query:**

```
mcp__exa__get_code_context_exa("Stripe Node.js SDK subscription checkout session")
```

**Discovery Report Output:**

```markdown
# Discovery Report: Billing Module

## Architecture Snapshot

- Entity pattern: see `packages/domain/src/entities/user.ts`
- Port pattern: see `packages/domain/src/ports/user-repository.ts`
- Use case pattern: see `packages/application/src/usecases/create-user.ts`
- Router pattern: see `packages/api/src/routers/users.ts`

## Existing Patterns

- No existing billing/payment code
- User entity can be referenced for customer mapping
- Existing validation utilities in `packages/domain/src/validation/`

## Technical Constraints

- Node 20, Bun runtime
- Drizzle ORM
- oRPC for API
- No Stripe SDK currently installed

## External References

- Stripe SDK: `stripe` npm package
- Webhooks: Need raw body for signature verification
- Checkout Sessions: Server-side creation, client redirect
```

---

### Phase 2: Clarification (Interactive)

**Agent presents points needing clarification:**

```markdown
## Clarification Needed

Based on the Discovery Report, I need to clarify the following:

1. **Pricing Model**: How many subscription plans (Free, Pro, Enterprise)?
   - Option 1: Fixed predefined plans
   - Option 2: Custom pricing per customer

2. **Trial Period**: Is a trial period needed?
   - Option 1: 14-day trial before charging
   - Option 2: Charge immediately

3. **Metered Billing**: Charge based on usage?
   - Option 1: Fixed monthly price only
   - Option 2: Usage-based add-ons (API calls, storage, etc.)

---
You can:
- Answer each question
- Say "skip" for me to decide based on best practices
- Say "continue" if no concerns
```

**User Response:**

> "3 plans: Free, Pro ($29/mo), Enterprise (custom). 14-day trial for Pro. No metered billing needed."

**Update Discovery Report:**

```markdown
## Clarifications

| Question        | Answer                                       | Impact                     |
| --------------- | -------------------------------------------- | -------------------------- |
| Pricing Model   | 3 fixed plans: Free, Pro ($29), Enterprise   | Plan entity needs 3 tiers  |
| Trial Period    | 14-day trial for Pro                         | Add trial logic to webhook |
| Metered Billing | Not needed                                   | Simplify - no usage events |

**User Confirmation**: 2025-01-13
```

---

### Phase 3: Synthesis (Oracle)

```
oracle(
  task: "Analyze billing feature requirements against codebase",
  files: ["history/billing/discovery.md"]
)
```

**Oracle Output:**

```markdown
# Approach: Billing Module

## Gap Analysis

| Component       | Have           | Need                        | Gap             |
| --------------- | -------------- | --------------------------- | --------------- |
| Customer entity | None           | Subscription, Plan entities | New             |
| Stripe SDK      | None           | stripe package              | Install + spike |
| Webhooks        | Express exists | Raw body middleware         | Modify          |
| UI              | None           | Billing page, checkout      | New             |

## Risk Map

| Component          | Risk | Verification        |
| ------------------ | ---- | ------------------- |
| Stripe SDK import  | HIGH | Spike               |
| Webhook signatures | HIGH | Spike               |
| Entity modeling    | LOW  | Follow User pattern |
| oRPC router        | LOW  | Follow existing     |

## Spike Requirements

1. Spike: Stripe SDK import and typing
2. Spike: Webhook signature verification
3. Spike: Checkout session flow
```

---

### Phase 4: Verification (Spikes)

**Create Spike Beads:**

```bash
bd create "Spike: Billing Integration" -t epic -p 0
# → bd-50

bd create "Spike: Test Stripe SDK import and typing" -t task --blocks bd-50
# → bd-51

bd create "Spike: Verify webhook signature handling" -t task --blocks bd-50
# → bd-52

bd create "Spike: Checkout session creation flow" -t task --blocks bd-50
# → bd-53
```

**Execute via MULTI_AGENT_WORKFLOW:**

```bash
bv --robot-plan  # Assigns spikes to parallel tracks
```

Workers execute, write to `.spikes/billing/`:

```
.spikes/billing/
├── stripe-sdk-test/
│   ├── index.ts        # Working import
│   └── learnings.md
├── webhook-test/
│   ├── handler.ts      # Signature verification
│   └── learnings.md
└── checkout-test/
    ├── session.ts      # Checkout session
    └── learnings.md
```

**Close spikes with learnings:**

```bash
bd close bd-51 --reason "YES: SDK imports cleanly. Use Stripe namespace for types."
bd close bd-52 --reason "YES: Need raw body. Use stripe.webhooks.constructEvent()"
bd close bd-53 --reason "YES: Create session server-side, redirect to session.url"
```

---

### Phase 5: Decomposition

**Load file-beads skill and create main plan:**

```bash
bd create "Epic: Billing Module" -t epic -p 1
# → bd-60

# Domain layer (no deps, can parallelize)
bd create "Create Subscription entity and SubscriptionRepository port" -t task --blocks bd-60
# → bd-61

bd create "Create Plan entity" -t task --blocks bd-60
# → bd-62

# Infrastructure (depends on domain)
bd create "Implement SubscriptionRepository with Drizzle" -t task --blocks bd-60 --deps bd-61
# → bd-63

bd create "Create Drizzle schema for subscriptions and plans" -t task --blocks bd-60 --deps bd-61,bd-62
# → bd-64

# Application layer
bd create "Implement CreateSubscription use case" -t task --blocks bd-60 --deps bd-63
# → bd-65

bd create "Implement CancelSubscription use case" -t task --blocks bd-60 --deps bd-63
# → bd-66

# Stripe integration (HIGH risk - has spike learnings)
bd create "Implement Stripe checkout session creation" -t task --blocks bd-60 --deps bd-65
# → bd-67  ← Embed learnings from bd-53

bd create "Implement Stripe webhook handler" -t task --blocks bd-60 --deps bd-63
# → bd-68  ← Embed learnings from bd-52

# API layer
bd create "Create billing oRPC router" -t task --blocks bd-60 --deps bd-65,bd-66,bd-67
# → bd-69

# UI layer
bd create "Create billing page with plan selection" -t task --blocks bd-60 --deps bd-69
# → bd-70

bd create "Implement checkout flow UI" -t task --blocks bd-60 --deps bd-69,bd-70
# → bd-71
```

**Example bead with embedded learnings (bd-68):**

```markdown
# Implement Stripe webhook handler

## Context

Handles Stripe webhook events for subscription lifecycle.

## Learnings from Spike bd-52

> - MUST use raw body (not parsed JSON) for signature verification
> - Use `stripe.webhooks.constructEvent(rawBody, sig, secret)`
> - Webhook secret from `STRIPE_WEBHOOK_SECRET` env var
> - Handle: checkout.session.completed, invoice.paid, customer.subscription.deleted
>
> Reference: `.spikes/billing/webhook-test/handler.ts`

## Requirements

- Webhook endpoint at `/api/webhooks/stripe`
- Signature verification before processing
- Idempotent event handling

## Acceptance Criteria

- [ ] Raw body middleware configured
- [ ] Signature verification implemented
- [ ] Events update subscription status correctly
- [ ] Passes `bun run check-types`
```

---

### Phase 6: Validation

```bash
bv --robot-suggest   # Check for missing deps
bv --robot-insights  # Find bottlenecks
bv --robot-priority  # Validate priorities
```

**Oracle final review:**

```
oracle(
  task: "Review billing plan for completeness",
  files: [".beads/bd-60.md", ".beads/bd-61.md", ...]
)
```

---

## Example 2: Simple Feature - Add User Avatar

### User Request

"Add avatar upload for user profiles"

---

### Phase 1: Discovery (Lightweight)

Single agent sufficient:

```
Task("Find existing user entity and profile update patterns")
```

**Findings:**

- User entity at `packages/domain/src/entities/user.ts`
- Update use case at `packages/application/src/usecases/update-user.ts`
- No existing file upload, but S3 utility exists

---

### Phase 2: Clarification (Skipped)

Simple feature, clear requirements → Skip Clarification.

---

### Phase 3: Synthesis

**Risk Assessment:**

| Component                | Risk                           |
| ------------------------ | ------------------------------ |
| Add avatar field to User | LOW                            |
| File upload to S3        | MEDIUM (variation of existing) |
| Image resize             | MEDIUM (new but standard)      |

No HIGH risk → Skip spike phase.

---

### Phase 4: Verification (Skipped)

All MEDIUM or LOW → Proceed directly to decomposition.

---

### Phase 5: Decomposition

```bash
bd create "Epic: User Avatar" -t epic -p 2
bd create "Add avatarUrl field to User entity" -t task --blocks bd-80
bd create "Add avatar upload endpoint with S3" -t task --blocks bd-80 --deps bd-81
bd create "Add avatar display to profile UI" -t task --blocks bd-80 --deps bd-82
```

Small, low-risk feature → 3 beads, no spikes, linear dependency.

---

## Decision Tree: When to Spike

```
Is this pattern in the codebase?
├── YES → LOW risk, no spike
└── NO →
    New external dependency?
    ├── YES → HIGH risk, SPIKE REQUIRED
    └── NO →
        Affects >5 files?
        ├── YES → HIGH risk, SPIKE REQUIRED
        └── NO → MEDIUM risk, interface sketch only
```
