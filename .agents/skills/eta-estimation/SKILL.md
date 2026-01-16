---
name: eta-estimation
description: Create quick ballpark ETA reports for bidding. Use when estimating effort for new projects - focuses on solution approach and rough hours. Target < 30 minutes per estimate.
version: 2.0.0
---

# Ballpark ETA Skill

Quick estimates to win bids. Solution-focused, not code-focused.

```
🎯 GOAL: Ballpark estimate to WIN BIDS (< 30 min)

✅ Input → Research → Solution → ETA Table
❌ NOT: Detailed tasks, coding specs, exact hours
```

---

## Workflow (3 Phases)

```
📥 Phase 1: Collect & Extract (5-10 min)
    ↓
🔬 Phase 2: Research & Solution (10-15 min)
    ↓
📊 Phase 3: ETA Table (5-10 min)
```

---

## Phase 1: Collect & Extract

### 1.1 Collect Assets

Ask user for all available assets:

```
Please share all available assets for this project:
- 📄 PDF/Word documents (SOW, specs, requirements)
- 🖼️ Images/Screenshots (mockups, designs, wireframes)
- 📝 Markdown/Text files (notes, user stories)
- 🔗 URLs (Figma, existing site, references)

Reply "done" when you've shared everything.
```

### 1.2 Process Assets

**Asset Processing Priority:**

1. **`look_at`** - Built-in tool, try first for images/PDFs
2. **`skill("ai-multimodal")`** - If available, better vision capabilities
3. **Fallback tools** - `Read`, `read_web_page`, `skill("docx")`, `skill("pdf")`

**Processing Flow:**

```
For each asset:
  1. Try look_at (built-in, works for images/PDFs)
  2. If need better analysis → check skill("ai-multimodal")
  3. If skill unavailable → use fallback tools
  4. Extract key info → save to assets.md
```

**Tool Selection by Asset Type:**

| Asset Type | Primary | Secondary | Fallback |
|------------|---------|-----------|----------|
| Image/Screenshot | `look_at` | `skill("ai-multimodal")` | - |
| PDF | `look_at` | `skill("ai-multimodal")` | `skill("pdf")` |
| DOCX | `skill("docx")` | - | - |
| Markdown/Text | `Read` | - | - |
| URL | `read_web_page` | - | - |

**Example Processing:**

```python
# Image/PDF - try look_at first
look_at(
  path="assets/dashboard-mockup.png",
  objective="Extract UI components, layout structure, and features",
  context="ETA estimation for new project"
)

# If need deeper analysis, check ai-multimodal skill
skill("ai-multimodal")  # Load if available
# Then use Gemini for better vision analysis

# DOCX - use docx skill
skill("docx")
# Extract requirements from document

# Markdown - direct read
Read("path/to/requirements.md")

# URL - fetch and extract
read_web_page(
  url="https://figma.com/...",
  objective="Extract design components and layout"
)
```

### 1.3 Track & Cache Assets

**Tạo folder assets để lưu trữ và reuse:**

```bash
mkdir -p plans/$(date +%Y%m%d)-<project-slug>/assets
```

**Copy/move assets vào folder:**
```bash
# Copy assets để tracking
cp <path-to-asset> plans/YYYYMMDD-<project>/assets/
```

**Tạo asset registry** `plans/YYYYMMDD-<project>/assets.md`:

```markdown
# Asset Registry: <Project Name>

## Tracked Assets

| ID | Type | Filename | Summary | Extracted |
|----|------|----------|---------|-----------|
| A1 | PDF | requirements.pdf | SOW with 15 features | ✅ |
| A2 | Image | dashboard-mockup.png | Main dashboard layout | ✅ |
| A3 | DOCX | user-stories.docx | 20 user stories | ✅ |
| A4 | URL | figma.com/... | Design system | ✅ |

## Asset Details

### A1: requirements.pdf
- **Location:** `assets/requirements.pdf`
- **Pages:** 12
- **Key Extracts:**
  - Feature list (page 2-5)
  - User roles (page 6)
  - Timeline (page 10)

### A2: dashboard-mockup.png
- **Location:** `assets/dashboard-mockup.png`
- **Components identified:**
  - Header with navigation
  - 4 stat widgets
  - Data table
  - Chart section

### A3: user-stories.docx
- **Location:** `assets/user-stories.docx`
- **Stories:** 20 total
- **Epics mapped:** E1 (5), E2 (8), E3 (4), E4 (3)
```

**Reuse trong các session sau:**

Khi cần reuse context từ project đã ETA:
```
Read plans/YYYYMMDD-<project>/assets.md để xem asset registry
Read plans/YYYYMMDD-<project>/context.md để xem extracted requirements
```

---

### 1.4 Create Context File

Save extracted info to project folder for reuse:

```bash
mkdir -p plans/$(date +%Y%m%d)-<project-slug>
```

Create `plans/YYYYMMDD-<project>/context.md`:

```markdown
# Context: <Project Name>

## Assets Received

| # | Type | Name | Summary |
|---|------|------|---------|
| 1 | PDF | requirements.pdf | 15 features, 3 user roles |
| 2 | Image | dashboard.png | Main dashboard with 4 widgets |

## Key Requirements

1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Screens Identified

- Dashboard
- Settings
- User Management

## Open Questions

- [Question 1]
- [Question 2]
```

---

## Phase 2: Research & Solution

### 2.1 Clarify (if needed)

Ask critical questions before estimating:

| Domain | Questions |
|--------|-----------|
| **Platform** | Web only? Mobile? Responsive? |
| **Auth** | SSO? OAuth providers? 2FA? |
| **Integrations** | Which APIs? Docs available? |
| **Data** | Migration needed? Volume? |
| **Timeline** | Hard deadline? Phased? |

### 2.2 Research

Use available skills:

| Need | Skill/Tool |
|------|------------|
| Library docs | `skill("docs-seeker")` |
| Tech comparison | `web_search` |
| Architecture advice | `oracle` |
| Similar solutions | `web_search` |

### 2.3 Solution Approach

Document in `plans/YYYYMMDD-<project>/solution.md`:

```markdown
# Solution: <Project Name>

## Recommended Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Backend | Node.js/NestJS | Team expertise, TypeScript |
| Frontend | React/Next.js | SSR, client preference |
| Database | PostgreSQL | Relational data, ACID |
| Hosting | AWS/Vercel | Scalability, cost |

## Architecture

[2-3 sentences describing how components connect]

## Key Decisions

1. **[Decision]**: [Approach] - [Why]
2. **[Decision]**: [Approach] - [Why]
```

---

## Phase 3: ETA Table

### 3.1 Epic Sizing Guide

| Size | Hours | Examples |
|------|-------|----------|
| **S** | 8-16h | Simple CRUD, basic UI |
| **M** | 16-40h | Auth, API integration |
| **L** | 40-80h | Dashboard, complex flows |
| **XL** | 80-160h | AI/ML, real-time sync |

### 3.2 Common Epic Estimates

| Epic Type | Size | Hours |
|-----------|------|-------|
| Auth/Login | M | 24-32h |
| Dashboard | L | 48-64h |
| CRUD module | M | 20-30h |
| API integration | M-L | 24-48h |
| Payment | L | 40-60h |
| Admin panel | M | 20-32h |
| Reports/Export | S-M | 12-24h |
| Testing & QA | M | 16-24h |

### 3.3 Generate ETA Table

**Output Format:**

```markdown
# ETA: <Project Name>

## Epic Breakdown

| Epic | Task | Description | Platform | Hours |
|------|------|-------------|----------|-------|
| E1: Authentication | Setup auth module | JWT/OAuth configuration | BE | 8h |
| | Login API | Endpoint with validation | BE | 4h |
| | Login UI | Form with error handling | FE | 4h |
| | Registration flow | API + UI + email verify | FS | 8-12h |
| **E1 Total** | | | | **24-28h** |
| E2: Dashboard | Dashboard layout | Responsive grid layout | FE | 8h |
| | Data APIs | Aggregation endpoints | BE | 8h |
| | Charts | Analytics components | FE | 8h |
| | Real-time updates | WebSocket integration | FS | 16h |
| **E2 Total** | | | | **40-48h** |
| E3: Integrations | Third-party setup | API client configuration | BE | 8h |
| | Data sync | Background job service | BE | 12h |
| | Error handling | Retry logic, logging | BE | 8h |
| **E3 Total** | | | | **28-32h** |
| E4: Admin | User management | CRUD UI for users | FE | 8h |
| | Admin APIs | Permission-based endpoints | BE | 8h |
| | Settings page | Config management | FS | 8h |
| **E4 Total** | | | | **24-28h** |
| E5: QA | Integration tests | API test coverage | BE | 8h |
| | E2E tests | Critical user flows | FE | 8h |
| | Bug fixes | Polish and fixes | FS | 8h |
| **E5 Total** | | | | **24h** |
| **TOTAL** | | | | **140-160h** |

## Summary

| Metric | Range |
|--------|-------|
| Base Hours | 140-188h |
| Buffer (+20%) | +28-38h |
| **Total** | **168-226h** |
| Duration (1 dev) | 4-6 weeks |
| Duration (2 devs) | 2-3 weeks |

## Cost Estimate

| Rate | Min | Max |
|------|-----|-----|
| $100/hr | $16,800 | $22,600 |
| $125/hr | $21,000 | $28,250 |
| $150/hr | $25,200 | $33,900 |

## Assumptions

1. Design provided by client
2. Standard hosting requirements
3. No data migration

## Risks

1. [Risk] - [Impact]
2. [Risk] - [Impact]

## Open Questions

1. ❓ [Question affecting scope]
2. ❓ [Question affecting timeline]
```

---

## Output Files

| File | Purpose |
|------|---------|
| `plans/YYYYMMDD-<project>/assets.md` | Asset registry - tracking all inputs |
| `plans/YYYYMMDD-<project>/assets/` | Folder chứa copies của assets |
| `plans/YYYYMMDD-<project>/context.md` | Extracted requirements từ assets |
| `plans/YYYYMMDD-<project>/solution.md` | Tech stack, architecture decisions |
| `plans/YYYYMMDD-<project>/eta.md` | Final ETA table and summary |

---

## Reuse Context

Khi cần tiếp tục hoặc update ETA cho project đã có:

```bash
# List existing ETA projects
ls plans/

# Load context từ project cũ
Read plans/YYYYMMDD-<project>/assets.md    # Asset registry
Read plans/YYYYMMDD-<project>/context.md   # Requirements
Read plans/YYYYMMDD-<project>/solution.md  # Tech decisions
Read plans/YYYYMMDD-<project>/eta.md       # Previous ETA
```

---

## Quick Reference

### Time Budget

| Phase | Time |
|-------|------|
| Collect & Extract | 5-10 min |
| Research & Solution | 10-15 min |
| ETA Table | 5-10 min |
| **Total** | **< 30 min** |

### Formula

```
Total = Σ(Epic hours) × 1.2 (buffer)
Duration = Total ÷ 40h/week
Cost = Total × rate
```

### DO NOT

- ❌ Detailed task breakdown
- ❌ Exact hours (use ranges)
- ❌ Code specs or DB schemas
- ❌ Over-research (15 min max)

---

## Principles

1. **Speed wins bids** - First reasonable estimate often wins
2. **Ranges are honest** - "100-140h" better than "120h"
3. **Solution sells** - Show you understand HOW to build it
4. **20% buffer always** - Never bid without buffer

---

See [reference/report-template.md](reference/report-template.md) for full report template.
