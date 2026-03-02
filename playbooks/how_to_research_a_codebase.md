# Playbook: How to Research a Codebase

*Status: Draft*

## Objective

Conduct comprehensive codebase research that documents what exists today, where it lives, how it works, and how components interact, without proposing changes unless explicitly requested.

## Prerequisites

* A clear research question or area of interest.
* Access to repository files and related documentation.
* Ability to gather file/line references from source files.
* Optional: `br` (beads_rust) available for issue linkage.

## Step-by-Step Instructions

1. **Initialize Research**
   * If no query is provided, ask for:
     * research question/topic,
     * relevant files/tickets,
     * constraints or scope boundary.
   * If query/inputs are provided, begin immediately.

2. **Read Directly Mentioned Files First**
   * Read all user-mentioned files fully before decomposition.
   * Do not spawn decomposition tasks before primary-source reading.

3. **Apply Documentation-Only Posture**
   * Document current state only:
     * what exists,
     * where it exists,
     * how it behaves,
     * how it connects.
   * Do not critique, recommend improvements, or propose refactors unless explicitly requested.

4. **Decompose the Research Question**
   * Break query into focused sub-areas (components, flows, patterns, docs).
   * Track sub-areas with a concise research task list.

5. **Run Parallel Evidence Gathering**
   * Gather findings across:
     * code locations,
     * implementation behavior,
     * recurring patterns,
     * historical context (for example `thoughts/` when present),
     * external references only if user requested web research.
   * Wait for all research branches before synthesis.

6. **Synthesize Findings**
   * Prioritize live code evidence as source of truth.
   * Connect component interactions and architectural patterns.
   * Include concrete file references with line numbers.

7. **Collect Research Metadata**
   * Capture:
     * current date/time,
     * active branch,
     * commit hash,
     * repository context,
     * researcher identity (if defined by environment).
   * If local tooling provides metadata generation, use it.

8. **Write Research Document**
   * Use repository conventions for research path/filename.
   * Include:
     * frontmatter metadata (when used in repo conventions),
     * research question,
     * summary,
     * detailed findings by area,
     * code references,
     * architecture notes,
     * historical context references,
     * related research links,
     * explicit open questions.

9. **Add Permalinks When Appropriate**
   * If commit/repo context supports stable links, include permalinks for referenced code locations.

10. **Optionally Link Tracker Work (`br`)**
    * Check for related open work:
      * `br list --status=open`
    * If relevant, create/update linked issues and include research artifact path for traceability.
    * Sync tracker state if your environment requires explicit sync commands.

11. **Present Findings and Handle Follow-Ups**
    * Share concise findings summary with key references.
    * For follow-up questions:
      * append to same research document when appropriate,
      * update metadata fields (`last_updated`, updater, note),
      * add a timestamped follow-up section.

## Verification

* Mentioned files were read fully before decomposition.
* Output remains documentation-only unless user requested recommendations.
* Findings include concrete file references and cross-component linkage.
* Research artifact includes required metadata and sections.
* Follow-up updates preserve document continuity and metadata integrity.
* Optional tracker links were recorded when `br` was used.

## Lifecycle Compliance

Confirm the workflow follows the required cycle:
Prompt -> Plan (based on a known playbook) -> Request approval -> Execute -> Plan/playbook update -> Docs update -> Verification.

If this occurs inside a git repo:
* Review `git status` and relevant diffs.
* Suggest a commit message that summarizes the completed task.
* Commit after approved checkpoint completion.
