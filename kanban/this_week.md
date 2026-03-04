# This Week

## Metadata

- Scope: this_week
- Purpose: Near-term work expected within the current week.

## To Do

### BLOCKER: Auth Refactor (Phase 1 - Critical Path)

- **Phase 1a**: Create single auth boundary (AuthContext + validator) on all identity-sensitive routes including /api/finalize
- **Phase 1b**: Stop trusting userId from request bodies (kpi/primary, onboarding/complete, finalize) — derive only from validated auth
- **Phase 1c**: Add ownership checks in services/DAOs (WHERE id = ? AND user_id = ? semantics) for answer/session mutations
- **Phase 1d**: Verify all 30 route handlers use unified auth contract

### BLOCKER: Session State Normalization (Phase 1 - unblocks story flow)

- Normalize session state contract across start/get responses (initialized vs INIT)
- Fix questionId routing at init so stage mapping can't route to ORIENT unexpectedly
- Preserve active-session uniqueness checks when moving to new initializer

### BLOCKER: Agent Network Integration (Phase 1 - unlocks openclaudein)

- Integrate auth boundary with openclaudein skill registration
- Verify dual-token system prerequisites (Phase 1 auth must be solid first)

### Feature: Finalize/Story Flow Compatibility (Phase 2 - unblocked by Phase 1)

- Add compatibility for finalize/story flows still reading sessions until fully migrated
- Update finalize endpoint to use unified auth contract

### Feature: Dual-Token System (Phase 3 - low priority until baseline auth solid)

- Implement /api/auth/skill endpoint
- Auth token lifecycle management
- User token persistence and binding

### Feature: UI Workflow Changes (Phase 2)

- [CosmicHR] Update workflow UX to match session state normalization
- Ensure UI correctly handles INIT vs initialized states

## Doing

<!-- Add task lines as markdown bullets: - exact task text -->

## Done

- [CosmicHR] Implement first round of voice-loop functions
- [CosmicHR] Fix broken Writer pipeline
- [CosmicHR] Wire up voice-loop UI
- [CosmicHR] Test voice-loop end-to-end
- [CosmicHR] Fix Writer transcribe and voice edit
- [CosmicHR] Get voice-loop basic flow working
- [CosmicHR] Add multiple turns support to voice-loop
- [CosmicHR] Add texting support post-call
- [CosmicHR] Add multiple selections for questions
- [CosmicHR] Add URL-based question scraping
- [CosmicHR] Build URL input and results page
- [CosmicHR] Build onboarding step with resume upload and LinkedIn paste
- [CosmicHR] Add LinkedIn API connection option
- [CosmicHR] Build shortlist generation
- [CosmicHR] Build connection finder
- [CosmicHR] Build contribution discovery
- [CosmicHR] Build LinkedIn post drafting tool
