# Assimilation Report: everything-claude-code

**Date**: 2026-03-01
**Target Repo**: `../everything-claude-code` (community-curated Claude Code performance optimization system)
**Method**: 10 haiku search agents + 20 sonnet analysis agents, full-repo coverage

---

## 1. First-Look Baseline (This Repo)

Our framework (`agents/`) is a **minimal-by-default, policy-driven agent operating system** with these core characteristics:

- **Design Philosophy**: Simple, straightforward, atomic, reliable across many agents. Assumes resource-constrained devices ("The Edge Protocol").
- **Strictness**: High. Playbook-first execution; stop on ambiguity; propose before acting.
- **Documentation Burden**: Moderate-to-high. Self-evolving workflow requires simultaneous doc updates with code changes. Seven documentation surfaces must be checked per change.
- **Playbook Coverage**: 12 playbooks covering core workflows (commit, debug, assimilate, TDD, kickoff, kanban moves, review, tool wrappers, downtime).
- **Operational Discipline**: Journal + kanban as first-class operational artifacts. Downtime task system for framework self-improvement. Templates and references for structured output.
- **Atomicity**: Strong. Changes must be atomic, reversible, and approved before execution.
- **Agent Scoping**: Implicit. No formal agent role definitions, model tiering, or tool permission scoping.
- **Enforcement Model**: Prompt-based. Rules live in RULES.md and playbooks; compliance depends on the agent reading and following them.
- **Verification**: Pattern-based. Reference documents describe verification approaches but no deterministic enforcement.

**Baseline Posture Summary**:
| Dimension | Our Framework |
|---|---|
| Minimal vs Batteries-included | Minimal |
| Strictness vs Flexibility | High strictness |
| Documentation burden | Moderate-high |
| Atomicity vs Expressiveness | Strongly atomic |
| Enforcement mechanism | Prompt-only |
| Agent role definition | Implicit |
| Self-improvement mechanism | Downtime tasks + assimilation |

---

## 2. Apparent Opportunity Map

Based on the first-look baseline, these are the hypothesized leverage points where patterns from other frameworks could improve our outcomes:

### O1: Hook-Based Enforcement (vs Prompt-Only)
- **Hypothesis**: Deterministic hooks at tool lifecycle boundaries could enforce rules that prompt-based instructions miss ~20% of the time.
- **Expected Improvement**: Reduced policy violations, especially for formatting, type-checking, and commit hygiene.

### O2: Formal Agent Role Definitions with Model Tiering
- **Hypothesis**: Explicit agent YAML frontmatter (name, description, tools, model) could improve task routing, cost control, and permission scoping.
- **Expected Improvement**: Better multi-agent coordination, predictable cost profiles, reduced capability overreach.

### O3: Context Window Management as Policy
- **Hypothesis**: Explicit rules about context consumption (MCP limits, compaction strategy, tool count caps) could prevent degraded performance in long sessions.
- **Expected Improvement**: More consistent agent behavior in extended sessions, fewer hallucinations from context pressure.

### O4: Mode-Switching via Dynamic System Prompts (Contexts)
- **Hypothesis**: Switchable behavioral modes (dev/research/review) injected at session start could sharpen agent behavior for specific task types.
- **Expected Improvement**: More focused agent output aligned to task intent without playbook bloat.

### O5: Continuous Learning Pipeline (Instincts/Evolution)
- **Hypothesis**: A mechanism to capture learned behaviors, score confidence, and promote to durable artifacts could accelerate framework evolution.
- **Expected Improvement**: Faster convergence on effective patterns, reduced repeated mistakes.

### O6: CI Validation of Framework Artifacts
- **Hypothesis**: Automated schema validation of playbooks, rules, and templates could catch structural drift before it causes agent failures.
- **Expected Improvement**: Higher framework artifact quality, fewer broken references.

### O7: Cross-Tool Adapter Pattern
- **Hypothesis**: Adapter layers between different AI coding tools could make our framework portable across Claude Code, Cursor, Codex, etc.
- **Expected Improvement**: Framework reusability across tools, broader adoption surface.

### O8: Verification/Eval Patterns (pass@k / pass^k)
- **Hypothesis**: Formal evaluation metrics for feature quality gates could replace informal "verify and report" patterns.
- **Expected Improvement**: More rigorous verification, measurable quality thresholds.

### O9: Skills as Composable Knowledge Units
- **Hypothesis**: Encapsulating domain expertise into self-contained skill modules (with metadata, examples, and checklists) could make knowledge more reusable than monolithic playbooks.
- **Expected Improvement**: More modular knowledge management, easier contribution path.

### O10: Security-First Agent Design
- **Hypothesis**: Explicit attack surface analysis, sandboxing policies, and audit logging could harden our framework against prompt injection and unsafe operations.
- **Expected Improvement**: Reduced risk of unintended destructive actions, better security posture.

---

## 3. Comparison Scope for This Round

**In scope** (all 10 opportunities above):
All opportunities O1-O10 are evaluated in this round given the comprehensive evidence collected by 30 parallel agents.

**Explicit non-goals**:
- Full architecture rewrite of our framework.
- Blindly copying ECC's prompt stack or skills library.
- Adopting tooling patterns that conflict with our minimal-by-default philosophy.
- Implementing ECC's npm package/distribution model.
- Adopting ECC's multi-platform support (Cursor, Codex, OpenCode) unless trivially portable.

---

## 4. Repos Reviewed and Evidence Sources

### Primary Target
- **Repo**: `../everything-claude-code`
- **Identity**: Community-curated "performance optimization system" for Claude Code and compatible AI agent harnesses.
- **Scale**: 23 top-level directories, 19 top-level files, 463 markdown files, 56 skills, 36 commands, 14 agents, 30 rules, 17 hooks, 13 test files (~17K lines).

### Evidence Sources (by agent)

| Agent Type | Count | Coverage |
|---|---|---|
| Haiku search agents | 10 | Directory trees, file listings, structural patterns for: top-level, markdown, rules, skills, commands, hooks, docs, contexts/schemas, plugins/mcp-configs, examples/tests, config dirs |
| Sonnet analysis agents | 19 (1 failed) | Deep content analysis of: README, CLAUDE.md, AGENTS.md, CONTRIBUTING.md, longform guide, shortform guide, OpenClaw guide, security guide, rules dir, commands dir, hooks dir, docs dir, contexts dir, plugins/examples/mcp-configs, schemas/scripts/tests, config dirs, install/package, prompt engineering patterns |

### Key Files Examined
- `README.md` (47KB, 1153 lines) - Project documentation and architecture
- `CLAUDE.md` (61 lines) - Terse agent orientation document
- `AGENTS.md` (~6KB) - 13 agents, 5 core principles, parallel execution mandate
- `CONTRIBUTING.md` (~8KB) - Artifact schemas, quality checklists, PR format
- `the-longform-guide.md` (~15KB) - Token economics, eval patterns, orchestration
- `the-shortform-guide.md` (~16KB) - Setup guide, hooks, rules, MCPs
- `the-openclaw-guide.md` (~42KB) - Security critique, prompt injection analysis
- `the-security-guide.md` (~28KB) - Attack vectors, sandboxing, OWASP Agentic Top 10
- `rules/` (30 files) - Two-layer hierarchical policy system
- `commands/` (36 files) - Development quality gates, orchestration, learning pipeline
- `hooks/hooks.json` (17 hooks) - 6 lifecycle event types
- `agents/` (14 YAML files) - Role definitions with model/tool scoping
- `contexts/` (3 files) - Mode-switching system prompts
- `skills/` (56 directories) - Domain expertise modules
- `schemas/` (3 JSON schemas) - Artifact validation
- `scripts/` (29 files) - CI validators, hook implementations, libraries
- `tests/` (13 files) - Zero-dependency test runner

---

## 5. Comparison Findings by Category

### 5.1 Architecture & Project Organization

| Aspect | Our Framework | ECC | Assessment |
|---|---|---|---|
| Core structure | Flat: playbooks/, templates/, references/, downtime/, journal/, kanban/ | Deep: rules/, skills/, commands/, agents/, hooks/, contexts/, schemas/, scripts/, tests/ | ECC is more granular but more complex |
| Agent definitions | Implicit in RULES.md prose | Explicit YAML frontmatter per agent file | **ECC better**: formal scoping reduces ambiguity |
| Rule system | Single RULES.md + playbooks | Two-layer: common/ + language-specific with `paths:` glob auto-activation | **ECC better**: conditional loading is elegant |
| Knowledge units | Playbooks (monolithic) | Skills (composable, self-contained) | Trade-off: our playbooks are simpler but less modular |
| Operational artifacts | Journal + kanban (unique to us) | None equivalent | **We're better**: operational discipline is a strength |
| Self-improvement | Downtime tasks + assimilation | Continuous learning pipeline (`/learn` -> `/evolve`) | Different philosophies, both valid |

### 5.2 Agent Constraints & Policy Design

| Aspect | Our Framework | ECC |
|---|---|---|
| Enforcement model | Prompt-only (RULES.md) | Hooks (deterministic) + Rules (prompt-based) |
| Policy language | Prose paragraphs | CRITICAL/ALWAYS/NEVER severity keywords |
| Compliance rate | Depends on agent reading + following | ~80% prompt + ~20% hook-enforced |
| Resource assumptions | "Edge Protocol" - assume constrained | Token economics as first-class concern, explicit context window budgets |

**What they do better**: Hook-based enforcement catches what prompts miss. Severity keywords (CRITICAL/ALWAYS/NEVER) create scannable, unambiguous directives. Explicit context window management prevents degraded performance.

**What we do better**: Our Edge Protocol is a simpler, more universal constraint model. Our playbook-first approach provides deeper procedural guidance per task type than their rule files.

### 5.3 Planning & Approval Mechanics

| Aspect | Our Framework | ECC |
|---|---|---|
| Planning flow | Playbook -> Plan -> Approve -> Execute | Plan mode (opus, read-only) -> Execute mode (sonnet, write) |
| Approval granularity | Per-task user approval | Model-tiered: opus plans, sonnet executes; Code Sovereignty for external models |
| SESSION_ID continuity | Not present | Plan files carry session IDs for cross-boundary context |

**What they do better**: MODEL tiering separates planning capability from execution cost. SESSION_ID handoff enables context continuity across command boundaries. Code Sovereignty pattern (only Claude writes to filesystem) is a clean safety boundary.

**What we do better**: Our approval flow is simpler and always involves the human. Their model-tiered flow could skip human review if misconfigured.

### 5.4 Tool Interface Design & Failure Handling

| Aspect | Our Framework | ECC |
|---|---|---|
| Tool wrappers | One playbook (`how_to_add_or_modify_a_tool_wrapper_safely.md`) | PostToolUse hooks: auto-format, type-check, console.log warnings after every edit |
| Failure handling | Debugging playbook (evidence-first) | Build-error-resolver agent, build analysis hook, strategic compaction |
| Deterministic checks | None | 17 hooks across 6 lifecycle events |

**What they do better**: PostToolUse hooks (auto-format after edit, type-check after edit, console.log warning after edit) provide deterministic quality gates that don't depend on the agent remembering to run them. The `suggest-compact` hook monitors token usage and advises compaction at the right time.

**What we do better**: Our debugging playbook provides deeper procedural guidance for systematic debugging vs their agent-based approach.

### 5.5 Documentation Maintenance Model

| Aspect | Our Framework | ECC |
|---|---|---|
| Doc surfaces | 7+ (RULES, README, playbooks, references, templates, journal, kanban) | 4 (README, CLAUDE.md, CONTRIBUTING.md, guides) |
| Self-evolution | Mandatory doc updates with every change | CI validators + schema enforcement |
| Drift prevention | Manual (downtime audit tasks) | Automated (CI validation scripts) |

**What they do better**: CI validators (`validate-agents.js`, `validate-commands.js`, etc.) catch structural drift automatically. JSON schemas enforce artifact structure.

**What we do better**: Our self-evolving workflow is more comprehensive in scope. Our downtime task system provides structured framework improvement. Our documentation is more operational (journal, kanban) vs their documentation being more reference-oriented.

### 5.6 Playbook Coverage (Minimal vs Default Set)

| Aspect | Our Framework (12 playbooks) | ECC (0 playbooks, 56 skills + 36 commands) |
|---|---|---|
| Approach | Procedural playbooks for workflows | Declarative skills for knowledge + imperative commands for actions |
| Coverage | Core workflows only | Broad domain coverage (backend, frontend, security, eval, languages) |
| Maintenance | Manual updates required | Frontmatter-driven, schema-validated |
| Discoverability | Index in RULES.md | Frontmatter `description` field for routing |

**Key insight**: ECC has no playbooks but achieves similar outcomes through skills (declarative knowledge) + commands (imperative actions). This is a fundamentally different paradigm, not a better/worse comparison.

### 5.7 Prompt Tone/Timbre & Behavioral Shaping

| Aspect | Our Framework | ECC |
|---|---|---|
| Instruction style | Prose paragraphs, moderate length | 7-layer instruction hierarchy, keyword severity levels |
| Behavioral shaping | `references/how_to_shape_agent_tone_and_timbre.md` | PROACTIVE directives, confidence-gated reporting, hooks-over-prompts philosophy |
| Mode switching | Not present | 3 contexts (dev/research/review) with distinct behavioral profiles |
| Anti-patterns | Listed in playbooks | Dedicated anti-pattern sections with NEVER keywords |

**What they do better**: PROACTIVE trigger language ("When you see X, ALWAYS do Y") creates reflexive behaviors. Confidence-gated reporting (only report findings above threshold) reduces noise. Mode switching via contexts sharpens behavior per task type. The 7-layer instruction hierarchy (CLAUDE.md -> AGENTS.md -> rules -> skills -> commands -> hooks -> contexts) provides clear precedence.

**What we do better**: Our tone/timbre reference is a reusable pattern applicable to any prompt. Our playbook structure provides richer procedural guidance per workflow.

### 5.8 Verification/Debugging Workflow Quality

| Aspect | Our Framework | ECC |
|---|---|---|
| Verification | Reference-based patterns, manual | pass@k / pass^k eval metrics, automated hook checks |
| Debugging | Evidence-first playbook | Build-error-resolver agent, build analysis hook |
| Quality gates | Approval-based | Automated (PostToolUse hooks) + approval-based |

**What they do better**: Eval-driven development (pass@k, pass^k) provides measurable quality thresholds. PostToolUse hooks provide automated quality gates after every tool use.

**What we do better**: Our evidence-first debugging playbook provides more systematic investigation guidance. Our verification references are more broadly applicable.

---

## 6. Transferable Lessons (Ranked)

### Rank 1: Severity Keyword Language in Rules (ADOPT NOW)
- **Source**: `rules/common/*.md` - CRITICAL, ALWAYS, NEVER keywords
- **Problem it solves**: Prose paragraphs in our RULES.md can be ambiguous about priority; agents may treat all instructions as equally important.
- **Smallest useful version**: Add severity keywords (CRITICAL, REQUIRED, NEVER) to the highest-priority rules in RULES.md without restructuring the document.
- **Complexity cost**: Very low. Wording changes only.
- **Reversibility**: Trivially reversible.

### Rank 2: Mode-Switching Contexts (ADOPT NOW)
- **Source**: `contexts/dev.md`, `contexts/research.md`, `contexts/review.md`
- **Problem it solves**: Our agents use the same behavioral profile for all task types. A debugging session benefits from different behaviors than a documentation review.
- **Smallest useful version**: Create 2-3 context files in a new `./contexts/` directory with distinct behavioral profiles. Reference from RULES.md. Agents select mode based on task type.
- **Complexity cost**: Low. 2-3 new files, one RULES.md update.
- **Reversibility**: Fully reversible (delete directory, remove reference).

### Rank 3: Formal Agent Role Definitions (PILOT FIRST)
- **Source**: `agents/*.md` - YAML frontmatter with name, description, tools, model
- **Problem it solves**: When dispatching sub-agents, there's no formal contract for what each agent can do, which model to use, or what tools it needs.
- **Smallest useful version**: Create an `agents.md` or `./agent-roles/` directory defining 3-5 common roles (planner, implementer, reviewer, researcher) with model recommendations and tool scopes.
- **Complexity cost**: Low-medium. New directory/file, RULES.md index update.
- **Reversibility**: Fully reversible.

### Rank 4: Context Window Management Policy (ADOPT NOW)
- **Source**: `rules/common/performance.md`, `the-longform-guide.md`
- **Problem it solves**: No guidance on context consumption, MCP limits, or when to compact. Long sessions may degrade without the agent noticing.
- **Smallest useful version**: Add a "Context Management" section to RULES.md or create a reference document with guidelines on tool count limits, compaction timing, and context budget awareness.
- **Complexity cost**: Very low. Documentation only.
- **Reversibility**: Trivially reversible.

### Rank 5: CI Validation of Framework Artifacts (PILOT FIRST)
- **Source**: `scripts/validate-*.js`, `schemas/*.json`
- **Problem it solves**: Our downtime tasks manually check for index/reference drift. Automated validation would catch issues immediately.
- **Smallest useful version**: A single validation script that checks RULES.md indexes against actual file system contents (playbooks, references, templates, downtime tasks).
- **Complexity cost**: Medium. One script, CI integration optional.
- **Reversibility**: Fully reversible.

### Rank 6: PROACTIVE Trigger Language in Prompts (ADOPT NOW)
- **Source**: `AGENTS.md` proactive triggers, `rules/common/agents.md`
- **Problem it solves**: Our instructions describe what to do but don't always specify trigger conditions. "When you see X, ALWAYS do Y" creates reflexive behaviors.
- **Smallest useful version**: Add proactive trigger patterns to the highest-impact rules in RULES.md (e.g., "When you see a failing test, ALWAYS read the error output before attempting a fix").
- **Complexity cost**: Very low. Wording changes only.
- **Reversibility**: Trivially reversible.

### Rank 7: Structured Anti-Pattern Sections (ADOPT NOW)
- **Source**: `rules/common/coding-style.md` NEVER sections, playbook anti-patterns
- **Problem it solves**: Our playbooks include some anti-patterns but they're mixed into prose. Dedicated NEVER/anti-pattern sections are more scannable.
- **Smallest useful version**: Add a structured "Anti-Patterns" or "NEVER" section to our highest-traffic playbooks and to RULES.md.
- **Complexity cost**: Very low. Formatting changes.
- **Reversibility**: Trivially reversible.

### Rank 8: Pass/Fail Eval Metrics for Verification (DEFER)
- **Source**: `the-longform-guide.md` pass@k / pass^k patterns
- **Problem it solves**: Our verification is qualitative ("verify and report"). Quantitative metrics could provide clearer quality gates.
- **Smallest useful version**: Document eval metric concepts in a reference file for agents to apply when running tests or quality checks.
- **Complexity cost**: Low. One reference document.
- **Reversibility**: Fully reversible.

### Rank 9: Conditional Rule Loading via Path Globs (DEFER)
- **Source**: `rules/` frontmatter `paths:` field for language-specific auto-activation
- **Problem it solves**: All our rules load for all tasks. Language- or domain-specific rules could reduce noise and improve focus.
- **Smallest useful version**: Not directly implementable without tool-level support. Document as an aspirational pattern.
- **Complexity cost**: High (requires tool integration).
- **Reversibility**: N/A until implemented.

### Rank 10: Continuous Learning Pipeline (DEFER)
- **Source**: `commands/learn.md`, `commands/evolve.md`, instinct system
- **Problem it solves**: Framework evolution is currently manual (downtime tasks, assimilations). An automated learning loop could accelerate improvement.
- **Smallest useful version**: A lightweight "lessons learned" log that agents append to after completing tasks, reviewed during downtime. Not the full instinct/evolve pipeline.
- **Complexity cost**: Medium-high for full pipeline, low for lightweight version.
- **Reversibility**: Reversible.

---

## 7. Non-Transferable Lessons (With Reasons)

### N1: 56-Skill Library
- **Decision**: Reject
- **Why**: Our framework is minimal-by-default. Skills as a concept overlap with our playbooks. Adopting a skill system would create a parallel knowledge structure with high maintenance cost. Our playbooks serve the same function with simpler tooling.

### N2: Hook-Based Deterministic Enforcement (Full System)
- **Decision**: Reject for now (revisit when tool support matures)
- **Why**: Our framework is prompt-only by design, intended to work across many agent tools. Full hook integration requires Claude Code-specific infrastructure. The ECC hook system (17 hooks, lifecycle events, adapter patterns) is deeply tied to Claude Code's tool architecture. Our framework aims to be tool-agnostic.
- **Note**: Individual high-value hook patterns (like post-edit type-checking) could be documented as recommendations agents can manually follow.

### N3: npm Package Distribution Model
- **Decision**: Reject
- **Why**: Our framework is a git-native set of markdown files. Package distribution adds build complexity with no benefit for our use case.

### N4: Cross-Tool Adapter Pattern (Cursor, Codex, OpenCode)
- **Decision**: Reject
- **Why**: While portability is valuable, our framework already works across tools by being pure markdown. Adapter layers add complexity for cross-tool runtime hooks we don't use.

### N5: Code Sovereignty Pattern
- **Decision**: Reject
- **Why**: This pattern (only Claude writes files, external models produce diffs only) solves a problem we don't have. Our framework doesn't orchestrate multiple AI models against the same filesystem.

### N6: SESSION_ID Handoff
- **Decision**: Reject
- **Why**: Context continuity across command boundaries is a Claude Code-specific optimization. Our framework operates within single sessions governed by playbooks. Journal entries serve our continuity needs.

### N7: Full Agent Frontmatter YAML Schema
- **Decision**: Defer (see Rank 3 above for lightweight version)
- **Why**: The full YAML schema (tools, model, triggers, description for routing) requires tooling support for parsing and routing. A lightweight markdown-based role definition captures most of the value.

### N8: Strategic Compaction Hooks
- **Decision**: Reject (adopt documentation instead)
- **Why**: The hook itself requires Claude Code infrastructure. But the decision table for when-to-compact-vs-not is valuable as documentation (see Rank 4).

---

## 8. Minimal vs Default-Playbook Recommendation

### Analysis

| Factor | Stay Minimal | Add More Defaults |
|---|---|---|
| Reliability gains | Rules stay simple, less to break | More explicit guidance reduces ambiguity |
| Maintenance cost | Lower | Higher (more files to keep current) |
| Onboarding clarity | Lower (agents must infer from general rules) | Higher (explicit workflows for common tasks) |
| Risk of over-constraining | Lower | Higher |
| Risk of missing guidance | Higher | Lower |

### Recommendation: **Stay Minimal, But Sharpen What Exists**

Our 12 playbooks cover the core workflows well. ECC's 56 skills + 36 commands demonstrate a batteries-included approach that works for their community-curated model but would create maintenance drag for our single-project framework.

**Threshold Rule**: Add a new playbook only when:
1. The task is high-risk (could break the framework or lose work), AND
2. It recurs across multiple sessions, AND
3. The existing playbooks + RULES.md don't provide sufficient guidance.

**Specific additions recommended**:
- No new playbooks needed from this assimilation.
- Instead, sharpen existing artifacts with severity keywords, proactive triggers, and anti-pattern sections (Ranks 1, 6, 7).
- Add context modes as a new lightweight mechanism (Rank 2).
- Add a context management reference (Rank 4).

---

## 9. Proposed Grafts (Atomic)

Listed in recommended execution order. Each graft is independent and reversible.

### Graft 1: Add Severity Keywords to RULES.md (Rank 1)
- **Change**: Add CRITICAL, REQUIRED, NEVER keywords to the highest-priority rules in RULES.md sections 1-3.
- **Impact**: High (clearer priority signals for all agents)
- **Complexity**: Very low (wording changes)
- **Risk**: Negligible
- **Files**: `RULES.md`

### Graft 2: Add PROACTIVE Trigger Language (Rank 6)
- **Change**: Add "When X, ALWAYS Y" trigger patterns to key rules in RULES.md and the most frequently used playbooks.
- **Impact**: Medium-high (reflexive behaviors reduce errors)
- **Complexity**: Very low (wording changes)
- **Risk**: Negligible
- **Files**: `RULES.md`, select playbooks

### Graft 3: Add Structured Anti-Pattern Sections (Rank 7)
- **Change**: Add explicit NEVER/anti-pattern blocks to RULES.md (section 2 especially) and the assimilation, debugging, and commit playbooks.
- **Impact**: Medium (scannable don'ts improve compliance)
- **Complexity**: Very low (formatting changes)
- **Risk**: Negligible
- **Files**: `RULES.md`, select playbooks

### Graft 4: Create Context Modes (Rank 2)
- **Change**: Create `./contexts/` directory with 3 files: `dev.md`, `research.md`, `review.md`. Each defines a behavioral profile for that task type. Add index to RULES.md. Add usage reference.
- **Impact**: High (sharper agent behavior per task type)
- **Complexity**: Low (3 new files, RULES.md update)
- **Risk**: Low (additive, doesn't change existing behavior)
- **Files**: `contexts/dev.md`, `contexts/research.md`, `contexts/review.md`, `RULES.md`

### Graft 5: Add Context Window Management Reference (Rank 4)
- **Change**: Create `./references/context_window_management.md` documenting MCP limits, tool count guidelines, compaction timing, and context budget awareness. Add to RULES.md references index.
- **Impact**: Medium (prevents degraded long-session performance)
- **Complexity**: Very low (one reference doc)
- **Risk**: Negligible
- **Files**: `references/context_window_management.md`, `RULES.md`

### Graft 6: Define Lightweight Agent Roles (Rank 3)
- **Change**: Create `./references/agent_roles_and_model_tiering.md` defining 3-5 common agent roles with recommended model tiers and tool scopes. Referenced from RULES.md.
- **Impact**: Medium (better multi-agent coordination)
- **Complexity**: Low (one reference doc)
- **Risk**: Low (advisory, not enforced)
- **Files**: `references/agent_roles_and_model_tiering.md`, `RULES.md`

### Graft 7: Create Framework Artifact Validator (Rank 5)
- **Change**: Create a validation script (shell or node) that checks RULES.md indexes against filesystem reality (playbooks, references, templates, downtime tasks).
- **Impact**: Medium (automates a downtime task)
- **Complexity**: Medium (new script)
- **Risk**: Low (read-only validation)
- **Files**: `scripts/validate-indexes.sh` (new), optionally CI integration

---

## 10. Risks and Tradeoffs

### Risks

| Graft | Risk | Mitigation |
|---|---|---|
| Severity keywords (G1) | Over-marking everything as CRITICAL dilutes signal | Limit CRITICAL to 3-5 rules maximum |
| PROACTIVE triggers (G2) | Too many triggers could make RULES.md noisy | Add to existing paragraphs, don't create new sections |
| Anti-patterns (G3) | Could grow into a long list | Keep anti-patterns to the top 3-5 per section |
| Context modes (G4) | Agents may not know which mode to select | Make mode selection part of task identification in RULES.md |
| Context management ref (G5) | May become outdated as tools evolve | Mark as "living document, verify against current tool versions" |
| Agent roles (G6) | Could become prescriptive instead of advisory | Frame as recommendations, not requirements |
| Artifact validator (G7) | Script maintenance burden | Keep scope narrow (index checks only) |

### Tradeoffs

- **Grafts 1-3** are pure wording improvements with near-zero downside. The only tradeoff is time spent implementing.
- **Graft 4** (contexts) adds 3 files. Tradeoff: slightly more to maintain, but high leverage for behavioral sharpness.
- **Grafts 5-6** add 2 reference documents. Tradeoff: more documentation surface, but the references fill genuine gaps.
- **Graft 7** adds a script. Tradeoff: code maintenance vs manual downtime task execution.

### Overfitting Risk

ECC is optimized for Claude Code power users running complex, multi-model projects. Our framework serves a broader set of agents on resource-constrained devices. The proposed grafts specifically avoid ECC's infrastructure dependencies (hooks, npm, multi-platform adapters) and focus on knowledge-level improvements (better wording, new reference docs, behavioral modes).

---

## 11. Verification Plan

### For Grafts 1-3 (Wording Changes)
- Read the modified RULES.md and playbooks end-to-end.
- Verify severity keywords are used sparingly and consistently.
- Verify proactive triggers follow the "When X, ALWAYS Y" pattern.
- Verify anti-pattern sections are clearly separated from positive instructions.
- Test: Give a small agent a task that previously triggered a known failure mode and check if the new wording prevents it.

### For Graft 4 (Context Modes)
- Verify each context file has a clear, distinct behavioral profile.
- Verify the RULES.md index includes the new contexts directory.
- Test: Run a research task with `research.md` loaded and verify the agent's behavior differs from a dev task.

### For Grafts 5-6 (Reference Docs)
- Verify each reference is internally consistent and doesn't contradict RULES.md.
- Verify the RULES.md references index is updated.
- Verify cross-references from existing playbooks are not broken.

### For Graft 7 (Validator Script)
- Run the validator against current state; expect zero false positives.
- Add a known inconsistency (e.g., remove a playbook from the index) and verify detection.
- Run in a clean checkout to verify no environment dependencies.

---

## 12. Docs/Playbooks to Update

### If All Grafts Approved

| File | Change Type | Description |
|---|---|---|
| `RULES.md` | Modify | Add severity keywords (G1), proactive triggers (G2), anti-pattern sections (G3), contexts index (G4), references index entries (G5, G6) |
| `contexts/dev.md` | Create | Development mode behavioral profile (G4) |
| `contexts/research.md` | Create | Research mode behavioral profile (G4) |
| `contexts/review.md` | Create | Review mode behavioral profile (G4) |
| `references/context_window_management.md` | Create | Context window management guidelines (G5) |
| `references/agent_roles_and_model_tiering.md` | Create | Agent role definitions and model tier recommendations (G6) |
| `scripts/validate-indexes.sh` | Create | Framework artifact index validator (G7) |
| `docs/assimilations/2026-03-01-everything-claude-code.md` | Create | This assimilation report (trail entry) |
| Select playbooks | Modify | Add proactive triggers and anti-pattern sections where highest-impact (G2, G3) |
| `journal/2026-03-01.md` | Update | Log assimilation work in repo work log |

---

## 13. Approval Request

This report presents 7 atomic grafts ranked by expected impact, all independently reversible. The grafts are designed to sharpen our existing framework without changing its minimal-by-default philosophy.

**Recommended first batch** (lowest risk, highest impact):
- **Grafts 1-3**: Severity keywords, proactive triggers, anti-pattern sections (wording-only changes to existing files)
- **Graft 4**: Context modes (3 new files + index update)

**Recommended second batch** (medium effort):
- **Grafts 5-6**: Reference documents (2 new files + index updates)

**Recommended third batch** (requires scripting):
- **Graft 7**: Artifact validator script

**Request**: Please review this report and indicate:
1. Which grafts to approve for implementation.
2. Any grafts to modify, defer, or reject.
3. Whether to proceed with batch 1 first or a different subset.
4. Any additional context or priorities I should consider.

No changes will be made until explicit approval is received.
