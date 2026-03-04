# Playbook: Prioritize Work by KPI Impact

*Status: New*

## Objective

Take a list of blockers, bugs, refactors, and features. Score each against the four KPI dimensions. Output a ranked work queue with go/nogo/todo decisions.

## Prerequisites

- Understand the four KPI dimensions (Signal Density, Story Completion, Truth Confirmation, Conversion)
- Have a list of current work items (blockers, bugs, UI changes, features)
- Know your constraints (timeline, resource capacity, dependencies)

## The Scoring Matrix

For each work item, score it 0-3 on each KPI dimension:

| Score | Impact | Definition |
|-------|--------|-----------|
| 0 | None | Doesn't touch this KPI |
| 1 | Low | Fixes a minor issue in this KPI area |
| 2 | Medium | Directly improves this KPI |
| 3 | High | Blocker for this KPI; feature won't work without it |

---

## Step 1: List All Current Work Items

Dump everything:
- Blockers (what's stopping e2e tests?)
- Bugs (what breaks KPIs?)
- Refactors (what debt must be paid?)
- Features (what improves KPIs?)
- Integration work (what unblocks the pipeline?)

**Template:**

```
## Current Work Items (Unsorted)

### Blockers
- [ ] [Item] — [brief reason]
- [ ] [Item] — [brief reason]

### Bugs
- [ ] [Item] — [brief reason]

### Refactors
- [ ] [Item] — [brief reason]

### Features
- [ ] [Item] — [brief reason]

### Integration
- [ ] [Item] — [brief reason]
```

---

## Step 2: Score Each Item Against KPIs

For each work item, ask four questions:

### Signal Density Impact
- Does this prevent/enable extracting concrete, specific evidence?
- Score: 0 (none), 1 (minor), 2 (medium), 3 (blocker)

### Story Completion Impact
- Does this prevent/enable capturing complete narratives?
- Score: 0 (none), 1 (minor), 2 (medium), 3 (blocker)

### Truth Confirmation Impact
- Does this prevent/enable verifying claims or marking unverified ones?
- Score: 0 (none), 1 (minor), 2 (medium), 3 (blocker)

### Conversion Impact
- Does this prevent/enable recruiter signal or interview decisions?
- Score: 0 (none), 1 (minor), 2 (medium), 3 (blocker)

**Scoring Decision Tree:**

For each KPI:
- Ask: "If this item is NOT done, can we still move the KPI needle?"
  - YES → Score 0-1 (low impact, can defer)
  - MAYBE → Score 2 (medium impact, should do soon)
  - NO → Score 3 (blocker, must do first)

**Template:**

```
## Work Item: [Name]

### Signal Density
- Question: [your question about signal extraction]
- If NOT done: [what breaks]
- Score: [0-3]

### Story Completion
- Question: [your question about narrative capture]
- If NOT done: [what breaks]
- Score: [0-3]

### Truth Confirmation
- Question: [your question about claim verification]
- If NOT done: [what breaks]
- Score: [0-3]

### Conversion
- Question: [your question about recruiter signal]
- If NOT done: [what breaks]
- Score: [0-3]

### Total Score: [sum] / 12
### Type: [Blocker | Bug | Refactor | Feature | Integration]
```

---

## Step 3: Calculate Priority Score

**Total Score = Sum of four KPI scores (0-12)**

Interpretation:
- **10-12:** GO (critical, do immediately)
- **7-9:** TODO (high priority, do this week)
- **4-6:** DEFER (medium priority, backlog)
- **0-3:** NOGO (low impact, don't do unless time permits)

---

## Step 4: Apply Dependencies

Some items must be done before others. Ask:

**For each item:**
- What must be done first?
- What can't start until this is done?

**Dependency rules:**
- Blockers (score 10-12) unlock other work
- Bugs (especially in data model) must be fixed before features
- Refactors that fix data contracts (like auth) should come before features that depend on those contracts

**Output: Dependency Graph**

```
Phase 1 (Blockers - must go first):
├── Auth boundary (unlocks agent network integration)
├── Session state normalization (unlocks story flow consistency)
└── Ownership checks (unlocks data integrity)

Phase 2 (Unblocked by Phase 1):
├── UI workflow changes
├── Finalize flow migration
└── Dual-token system

Phase 3 (Polish):
└── Optimization, hardening
```

---

## Step 5: Output Three Lists

### GO List (Score 10-12)
Items that **must** be done first. Work on these until complete. Blocker for everything else.

Format:
```
## GO (Critical Path)

1. [Item] — Score [X]/12
   - Why: [blocking which KPIs]
   - Unblocks: [what can start after]
   - Estimated effort: [low/medium/high]
```

### TODO List (Score 7-9)
Items that **should** be done soon. Can run in parallel with GO work if resources allow.

Format:
```
## TODO (High Priority - This Week)

1. [Item] — Score [X]/12
   - Why: [improves which KPIs]
   - Dependencies: [what must be done first]
   - Estimated effort: [low/medium/high]
```

### NOGO List (Score 0-6)
Items that **can be deferred** or are not KPI-aligned. Backlog for later.

Format:
```
## NOGO (Defer or Backlog)

1. [Item] — Score [X]/12
   - Why: [low KPI impact]
   - Revisit when: [condition]
```

---

## Example: CosmicHR Auth Refactor

Let's walk through a simplified version:

### Work Item 1: Auth Boundary (AuthContext + validator)

**Signal Density:**
- Question: Does inconsistent auth prevent correct signal attribution?
- If NOT done: Claims are unattributed or misattributed → low signal
- Score: **3 (blocker)**

**Story Completion:**
- Question: Does auth enable session resumption?
- If NOT done: User can't resume session → incomplete stories
- Score: **3 (blocker)**

**Truth Confirmation:**
- Question: Does auth enable claim verification?
- If NOT done: Verified claims can't be linked to users → no confirmation chain
- Score: **3 (blocker)**

**Conversion:**
- Question: Does auth enable recruiter trust?
- If NOT done: Recruiter can't trust claim attribution → pass on candidate
- Score: **3 (blocker)**

**Total: 12/12 — GO immediately**

---

### Work Item 2: Stop Trusting userId from Request Bodies

**Signal Density:**
- Question: Does trusting request-body userId break signal attribution?
- If NOT done: Candidate can claim to be someone else → false signal
- Score: **3 (blocker)**

**Story Completion:**
- Question: Does ownership validation prevent session hijacking?
- If NOT done: One user can overwrite another's story
- Score: **3 (blocker)**

**Truth Confirmation:**
- Question: Can unvalidated userId break the verification chain?
- If NOT done: SMS confirmation goes to wrong user
- Score: **3 (blocker)**

**Conversion:**
- Question: Does security breach damage recruiter trust?
- If NOT done: Recruiter discovers candidate spoofing → massive trust loss
- Score: **3 (blocker)**

**Total: 12/12 — GO immediately (Phase 1 after auth boundary)**

---

### Work Item 3: Add Dual-Token System

**Signal Density:**
- Question: Does a dual-token system improve signal extraction?
- If NOT done: Signal extraction still works (not blocked)
- Score: **1 (minor polish)**

**Story Completion:**
- Question: Does dual-token enable better session persistence?
- If NOT done: Session persistence works without it (not blocked)
- Score: **1 (minor polish)**

**Truth Confirmation:**
- Question: Does dual-token improve claim verification?
- If NOT done: Verification works with single token (not blocked)
- Score: **1 (minor polish)**

**Conversion:**
- Question: Does dual-token improve recruiter signal?
- If NOT done: Recruiter still gets valid signal (not blocked)
- Score: **1 (minor polish)**

**Total: 4/12 — DEFER (can add after baseline auth is solid)**

---

## Step 6: Create Execution Plan

Once you have GO/TODO/NOGO lists, create a phase plan:

```
## Execution Plan

### Phase 1: Critical Path (GO items, score 10-12)
- Item A: Auth boundary
- Item B: Stop trusting request-body userId
- Item C: Ownership checks in services/DAOs
- **Gate:** All items complete + verified with KPI checklist

### Phase 2: High Priority (TODO items, score 7-9)
- Item D: Session state normalization
- Item E: QuestionId routing fix
- Item F: Finalize/story flow compatibility
- **Gate:** All Phase 1 items complete

### Phase 3: Polish (Score 0-6)
- Item G: Dual-token system
- Item H: Performance optimization
- **Gate:** Phase 1+2 complete, e2e tests passing
```

---

## Verification Checklist

Before moving from one phase to the next:

```
## Phase Exit Criteria

- [ ] All items in this phase are code-complete
- [ ] All items have passing tests
- [ ] No KPI regressions (Signal Density, Story Completion, Truth Confirmation, Conversion all intact)
- [ ] Downstream items can now start (dependencies unblocked)
- [ ] Commit + pushed with phase summary
```

---

## Anti-Patterns

- **Doing NOGO items first:** Common trap. Don't optimize before core KPI work is solid.
- **Deferring GO items:** If something scores 10-12, it's blocking your north star. Do it first.
- **Ignoring dependencies:** A high-scoring item might be blocked by a lower-scoring item. Honor the dependency order.
- **Feature creep mid-phase:** Don't add new items to GO while Phase 1 is in progress. Add to TODO or NOGO.

---

## Reusability

Run this playbook:
- **Weekly:** Reprioritize current work against any new items
- **On blocker discovery:** Item blocking e2e tests? Score it and reorder
- **At sprint planning:** Input last week's work + new items, output this week's queue

Template is in `./templates/kpi_priority_matrix.md` — copy, fill in, share with team.
