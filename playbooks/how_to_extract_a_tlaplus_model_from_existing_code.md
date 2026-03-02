# Playbook: How to Extract a TLA+ Model from Existing Code

*Status: Draft*

## Objective

Extract a behavioral model from existing code, express it as a path specification suitable for TLA+ verification, validate the model, and hand it off to planning and TDD workflows.

## Prerequisites

* A change request describing what behavior is being modified or extended.
* Entry points (file paths, functions, or modules) for extraction scope.
* Access to relevant source files and callers/callees.
* `silmari verify-path` available for model verification.
* Optional: `br` (beads_rust) available for tracker linkage.

## Step-by-Step Instructions

1. **Collect Scope Inputs**
   * Confirm:
     * proposed change,
     * code entry points,
     * optional depth/boundary for tracing.
   * If scope is ambiguous, ask for a narrow confirmation before modeling.

2. **Read Referenced Files Fully**
   * Read all directly mentioned files completely before decomposition.
   * Do not delegate or summarize before primary-source reading.

3. **Map the Extraction Boundary**
   * Identify:
     * functions to model directly,
     * direct callers (who observe terminal behavior),
     * direct callees (dependencies and possible opaque boundaries),
     * model boundary (in-scope vs out-of-scope).
   * Present this scope and request confirmation before state extraction.

4. **Extract State/Transition Semantics**
   * For each in-scope function, document:
     * states (entry, processing, terminal success/error),
     * transitions (conditions that move between states),
     * invariants (ordering, contracts, resource, error semantics),
     * caller-visible expectations.

5. **Synthesize Behavioral Model**
   * Merge per-function findings into one coherent model.
   * Explicitly mark uncertain assumptions rather than guessing.
   * Present model summary and confirm it reflects current behavior.

6. **Generate Path Spec Artifact**
   * Write model file to:
     * `specs/orchestration/<scope-name>-model.md`
   * Include:
     * purpose,
     * trigger,
     * resource references,
     * step list,
     * terminal condition,
     * feedback loops,
     * extracted invariants with source file:line,
     * change impact analysis.

7. **Map Invariants to Properties and Oracles**
   * For each invariant, define:
     * TLA+ property target (for example Reachability, TypeInvariant, ErrorConsistency),
     * corresponding code-level test oracle/assertion.

8. **Run Path Verification**
   * Execute:
     * `silmari verify-path specs/orchestration/<scope-name>-model.md`
   * Record outcome and interpret any failures:
     * reachability gaps,
     * type/contract inconsistencies,
     * error-path inconsistencies.

9. **Handoff to Planning/TDD**
   * Convert:
     * each model step -> testable behavior,
     * each property/invariant -> test assertion.
   * Use the resulting model as input to TDD planning playbooks/commands.

10. **Optionally Link Tracker Work (`br`)**
    * Check/open issue linkage:
      * `br list --status=open`
    * Create/update issue for model extraction and include:
      * model artifact path,
      * scope,
      * invariant count,
      * dependent issues if applicable.

## Verification

* Extraction scope (functions/callers/callees/boundary) is explicitly documented.
* Model states and transitions match current observed code behavior.
* Invariants cite concrete source locations.
* Path spec file exists at agreed location with required sections.
* `silmari verify-path` was run and results were reported.
* Handoff mapping to planning/TDD artifacts is explicit.

## Lifecycle Compliance

Confirm the workflow follows the required cycle:
Prompt -> Plan (based on a known playbook) -> Request approval -> Execute -> Plan/playbook update -> Docs update -> Verification.

If this occurs inside a git repo:
* Review `git status` and relevant diffs.
* Suggest a commit message that summarizes the completed task.
* Commit after approved checkpoint completion.
