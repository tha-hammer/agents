# Playbook: Plan a KPI-Aligned Feature

*Status: New*

## Objective

Ensure every feature plan connects explicitly to product KPIs before implementation. Prevent isolated specs that ignore upstream constraints and downstream consequences.

## Prerequisites

- Understand the four KPI dimensions: Signal Density, Story Completion, Truth Confirmation, Conversion
- Have access to the product's KPI definitions (CosmicHR example: application-to-interview conversion is the north star)
- Read the feature request or user story that triggered the work

## The Four KPI Dimensions

Use this as your north star frame. Every feature must answer these four questions.

### 1. Signal Density

**Definition**: Does this help extract concrete, specific evidence (not vague narratives)?

**Questions to answer:**
- What artifacts (metrics, names, dates, timelines, outcomes, tools, people) will this feature help the user capture or surface?
- What makes the evidence "dense" (specific) vs "sparse" (vague)?
- How does the feature prevent or detect low-signal filler?

**Example (CosmicHR voice-loop):**
- Feature: LLM-assisted voice feedback loop
- Artifact extraction: "Tell me a specific metric from this project"
- Signal density test: LLM feedback includes "I heard you mention 50% improvement (metric), which is concrete" vs "You said it went well (vague, low signal)"
- Prevents: Candidate saying "had a good experience" without specifics

### 2. Story Completion

**Definition**: Does this move the user toward capturing a complete, structured narrative?

**Questions to answer:**
- What narrative slots or fields does this feature fill?
- What story structure is required (e.g., situation → action → obstacle → outcome)?
- How does the feature signal to the user that the story is "complete"?

**Example (CosmicHR voice-loop):**
- Feature: Multi-turn voice session with slot-based state machine
- Story slots: Situation (context), Challenge (what stood in the way), Actions (what you did), Outcome (measurable result), Confirmation (verified claim)
- Completion signal: "You've filled 5/5 slots for this question. Ready to move to next question?"
- Incomplete handling: If user only provides 3/5 slots, system prompts "Tell me more about the challenge and outcome"

### 3. Truth Confirmation

**Definition**: Does this help verify claims or clearly mark unverified assertions?

**Questions to answer:**
- What claims does this feature allow the user to make (metrics, scope, environment, people involved)?
- How are verified claims marked vs unverified ones?
- What confirmation mechanism exists (voice capture, SMS follow-up, artifact reference)?

**Example (CosmicHR voice-loop + SMS follow-up):**
- Feature: Voice loop captures claim + SMS verification (optional)
- Claim types: "I improved conversion rates by 40%", "Led a team of 5", "Deployed to production in 2 days"
- Verification: "Did you say 40%?" (SMS, voice recorded) vs "Unconfirmed: estimated 40%"
- Unverified handling: LLM notes claim as tentative; recruiter sees "Candidate reports 40% improvement (not confirmed)"

### 4. Conversion

**Definition**: Does this improve recruiter signal, leading to higher interview rates?

**Questions to answer:**
- What does a recruiter see as the output of this feature?
- How does completed/verified output differ from incomplete/unverified?
- What recruiter action becomes more likely (click "interview" vs "pass")?

**Example (CosmicHR complete pipeline):**
- Feature: File upload + voice loop + confirmation flow
- Recruiter sees (complete): Profile with specifics, verified claims, complete stories → recruiter impression: "This is a real person with real impact"
- Recruiter sees (incomplete): Vague narratives, unverified claims → recruiter impression: "Polished but generic"
- Action: Complete signal → interview decision; incomplete → pass decision

---

## Step-by-Step Planning

### 1. Define the Feature in One Sentence

Write a user-centric description of what the feature does, not how.

**Example:** "Help the user capture specific, measurable outcomes from their work experience via voice-guided conversation"

**Not:** "Implement a multi-turn state machine with voice input and LLM parsing"

### 2. Fill in the KPI Mapping Template

For each KPI dimension, answer the questions above. Write concisely, but specifically.

**Template:**

```
## Feature: [Name]

### Signal Density
- Artifacts captured: [what specific data points]
- Signal test: [what makes it concrete vs vague]
- Anti-pattern: [what would be low-signal]

### Story Completion
- Narrative slots: [list the required fields/steps]
- Completion signal: [how user knows story is complete]
- Incomplete handling: [what happens if slots are missing]

### Truth Confirmation
- Claims allowed: [what can user assert]
- Verification mechanism: [how claims are verified]
- Unverified marking: [how tentative claims are flagged]

### Conversion
- Recruiter sees: [output/artifact]
- Complete vs incomplete: [what's different]
- Recruiter action: [what decision improves]
```

### 3. Identify Upstream Constraints

Ask: What data model, architecture, or spec do I need to assume exists?

**Example (voice-loop on auth issue):**
- Assumption: User identity is preserved across sessions
- Constraint: Auth handler must be consistent (13 handlers using filter, 17 reading header directly = broken assumption)
- Impact on KPIs: If user identity is broken, Story Completion and Truth Confirmation collapse (can't track whose session it is)

**Action:** If a constraint is missing or broken, add it to the plan as a blocker before implementing the feature.

### 4. Write the Feature Spec with KPI Callouts

In your implementation plan, tie each major component back to a KPI.

**Example structure:**

```
## Voice Loop Spec

### Entry (Supports Story Completion + Signal Density)
- File upload → extract questions from job description
- Default questions → ensure complete story slots covered
- LLM coaching → push user toward concrete evidence

### Recall Phase (Supports Signal Density + Truth Confirmation)
- Voice capture → record user's exact words (verifiable)
- LLM feedback → flag vague language ("went well" → ask for metric)
- Slot tracking → confirm all 5 narrative slots are filled

### Review Phase (Supports Conversion)
- Show recruiter view → user sees what recruiter will see
- Highlight verified vs unconfirmed claims → user can correct or provide confirmation
- Signal density score → user understands what recruiter values

### Confirm Phase (Supports Truth Confirmation)
- SMS/email optional confirmation loop → user can verify claimed metrics
- Final draft → shows all claims marked as verified or tentative
```

### 5. Create Verification Checklist

Before calling the feature "done," verify it actually moves the KPI needle.

**Template:**

```
## Verification Checklist

- [ ] Signal Density: Can I extract 3+ concrete metrics/specifics from test session?
- [ ] Story Completion: Does the system guide user to fill all required narrative slots?
- [ ] Truth Confirmation: Can I distinguish verified claims from unverified ones in the output?
- [ ] Conversion: Does recruiter view show higher-signal output than before this feature?
- [ ] No regression: Did previous features' KPI impact stay the same or improve?
```

---

## Example: Auth Handler Unification (Retrospective)

Apply this playbook retroactively to the auth issue to see what was missed:

**Feature:** Unified auth across all route handlers

**Signal Density:**
- ❌ MISSED: No spec for how auth state feeds into session-level signal tracking
- Impact: Lost visibility into "which user claimed this metric"
- Fix: Auth spec should require: "User identity must be preserved 1:1 through session lifecycle so signal can be attributed"

**Story Completion:**
- ❌ MISSED: No constraint that sessions must be resumable (user can come back and continue)
- Impact: Auth mismatch broke session continuity
- Fix: Auth contract: "User can resume session → identity must survive restart"

**Truth Confirmation:**
- ❌ MISSED: No spec for "confirmed by which user" or "at what time"
- Impact: When auth handlers differ, claim attribution becomes ambiguous
- Fix: Auth spec: "Every claim is tagged with (user_id, timestamp, verification_method)"

**Conversion:**
- ❌ MISSED: No recruiter-facing requirement that claims are attributed to real sessions
- Impact: Recruiter can't trust signal if user identity is broken
- Fix: Auth spec: "Recruiter sees verified claims with session attribution → trust increases"

**Lesson:** Auth spec lived in isolation. If you'd asked "How does auth impact Signal Density, Truth Confirmation, and Conversion?" upstream, you'd have caught the identity-derivation bug at design time.

---

## Lifecycle Compliance

1. **Before planning:** Run the KPI mapping template for any feature request
2. **During planning:** Call out upstream constraints and downstream KPI impacts
3. **Before implementation:** Get approval that KPI mapping is complete and realistic
4. **During implementation:** Refer to KPI checklist to catch scope creep
5. **During testing:** Verify feature actually moves the KPI needles
6. **On completion:** Document the KPI impact in the commit message and journal

---

## Common Pitfalls

- **Isolation:** Planning a feature without asking "how does this feed the KPI pipeline?" Example: building auth without asking how identity impacts signal attribution
- **Vague mapping:** Saying "this feature helps with conversion" without explaining how. Be specific: "User can now verify 3 claims via SMS → recruiter sees verified evidence → interview likelihood increases from X% to Y%"
- **Missing constraints:** Assuming data contracts exist downstream when they don't. Example: assuming session identity is preserved (it wasn't, because auth handlers were inconsistent)
- **Incomplete verification:** Calling feature done without checking if it actually moved the KPI. Test with real user data.

---

## Further Reading

- `./templates/change_plan.md` — Use this template after KPI mapping is complete
- `./kanban/ideas.md` — The "CosmicHR KPI Compass" captures the KPI definitions in one place
- CosmicHR KPI-to-Code Traceability doc (shared in onboarding) — Maps KPIs → implementation artifacts
