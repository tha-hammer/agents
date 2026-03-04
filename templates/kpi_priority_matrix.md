# KPI Priority Matrix

Use this template to score and prioritize work items. Copy, fill in, commit.

## Instructions

1. List all current work items (blockers, bugs, refactors, features, integration)
2. For each item, score it 0-3 on each KPI (0=none, 1=low, 2=medium, 3=blocker)
3. Sum scores (0-12 total)
4. Categorize: 10-12=GO, 7-9=TODO, 4-6=DEFER, 0-3=NOGO
5. Add dependencies
6. Output three lists

---

## Work Items (Unsorted)

### Item: [Name]

**Type:** [Blocker | Bug | Refactor | Feature | Integration]

**Description:** [What is this work?]

#### KPI Scoring

**Signal Density (0-3):**
- Question: Does this prevent/enable extracting concrete evidence?
- If NOT done: [what breaks]
- Score: **[0-3]**

**Story Completion (0-3):**
- Question: Does this prevent/enable capturing complete narratives?
- If NOT done: [what breaks]
- Score: **[0-3]**

**Truth Confirmation (0-3):**
- Question: Does this prevent/enable verifying claims?
- If NOT done: [what breaks]
- Score: **[0-3]**

**Conversion (0-3):**
- Question: Does this prevent/enable recruiter signal?
- If NOT done: [what breaks]
- Score: **[0-3]**

**Total Score: [sum]/12**

**Dependencies:** [what must be done first]

**Estimated Effort:** [low/medium/high]

---

## Summary

### GO (Score 10-12) — Critical Path

| Rank | Item | Score | Effort | Unblocks |
|------|------|-------|--------|----------|
| 1 | | /12 | | |
| 2 | | /12 | | |

### TODO (Score 7-9) — High Priority

| Rank | Item | Score | Effort | Dependencies |
|------|------|-------|--------|---|
| 1 | | /12 | | |
| 2 | | /12 | | |

### NOGO (Score 0-6) — Defer/Backlog

| Rank | Item | Score | Reason |
|------|------|-------|--------|
| 1 | | /12 | |
| 2 | | /12 | |

---

## Execution Plan

```
Phase 1 (GO):
├── [Item]
├── [Item]
└── [Item]
    Gate: All complete + KPI checklist pass

Phase 2 (TODO):
├── [Item]
└── [Item]
    Gate: Phase 1 complete, dependencies unblocked

Phase 3 (DEFER):
└── [Item]
    Gate: Phase 1+2 complete, time permits
```

---

## Phase Exit Checklist

- [ ] All items complete
- [ ] Tests passing
- [ ] No KPI regressions
- [ ] Downstream items unblocked
- [ ] Committed and pushed
