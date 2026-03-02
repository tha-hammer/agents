# Playbook: How to Create a TDD Implementation Plan

*Status: Draft*

## Objective

Produce a detailed, behavior-first Test-Driven Development (TDD) plan that breaks work into the smallest testable slices and defines a clear Red -> Green -> Refactor sequence.

## Prerequisites

* A task description, ticket, or equivalent change request.
* Access to relevant repository files (implementation + tests).
* Ability to identify and run project test commands.
* Optional: `br` (beads_rust) available if issue linkage is needed.

## Step-by-Step Instructions

1. **Collect Initial Context**
   * If the request has no parameters, ask for:
     * task/ticket description,
     * constraints/requirements,
     * related docs or prior research.
   * If parameters are provided, begin context gathering immediately.

2. **Read Referenced Inputs Fully**
   * Read all directly mentioned files completely before deeper decomposition.
   * Do not run partial reads for ticket/research/plan inputs.

3. **Research Current State**
   * Locate existing implementation and tests for the target area.
   * Gather concrete evidence with file paths and line references.
   * Capture current testing framework and command patterns.

4. **Present Understanding**
   * Summarize:
     * what behavior exists today,
     * what change is requested,
     * what constraints/patterns must be preserved.
   * Ask only unresolved questions that could not be answered from repository evidence.

5. **Define Smallest Testable Behaviors**
   * Break scope into observable behaviors using Given/When/Then.
   * Start with simplest behavior, then edge cases, then error paths.
   * Focus on externally observable outcomes, not internal implementation details.

6. **Define Test Strategy and Order**
   * Classify behaviors into unit/integration/end-to-end scopes.
   * Specify execution order from lowest-risk/simple to highest-complexity.
   * Confirm behavior breakdown with the user before drafting the full plan.

7. **Draft Plan Structure Before Full Detail**
   * Present intended structure with one Red -> Green -> Refactor subsection per behavior.
   * Get approval on structure before writing full plan content.

8. **Write the TDD Plan Artifact**
   * Use the repository's preferred planning directory.
   * If no project convention exists, agree a path with the user before writing.
   * If the environment uses the `thoughts/` convention, use a date-first filename such as:
     * `thoughts/searchable/shared/plans/YYYY-MM-DD-ENG-XXXX-tdd-description.md`

9. **Populate Required Plan Content**
   * Include, at minimum:
     * Overview
     * Current State Analysis with key discoveries (file:line evidence)
     * Desired End State with observable behaviors
     * Out-of-scope section
     * Testing Strategy (framework + test types + setup)
     * Per-behavior Test Specification (Given/When/Then + edge cases)
     * Per-behavior Red -> Green -> Refactor implementation slices
     * Automated and manual success criteria
     * Integration/E2E validation
     * References (ticket, research, code paths)

10. **Optionally Link Tracker Work (`br`)**
    * Check for an existing issue:
      * `br list --status=open`
    * If needed, create or update tracker state and attach the plan path for traceability.
    * Add dependencies when the work is blocked by or blocks other issues.

11. **Review, Iterate, and Finalize**
    * Present plan location and summarize behavior list + verification commands.
    * Resolve all open questions before marking the plan ready.

## Verification

* All directly referenced input files were read completely.
* Behavior list is explicit, smallest-slice, and written in Given/When/Then form.
* Every behavior has Red -> Green -> Refactor phases.
* Automated and manual verification are both defined.
* Plan references include concrete file paths (and file:line where applicable).
* Optional tracker links are recorded when `br` was used.

## Lifecycle Compliance

Confirm the workflow follows the required cycle:
Prompt -> Plan (based on a known playbook) -> Request approval -> Execute -> Plan/playbook update -> Docs update -> Verification.

If this occurs inside a git repo:
* Review `git status` and relevant diffs.
* Suggest a commit message that summarizes the completed task.
* Commit after approved checkpoint completion.
