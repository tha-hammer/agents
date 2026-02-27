# Playbook: Move Kanban Tasks Verbatim

*Status: Stable*

## Objective
Move tasks across kanban columns or boards without modifying task text.

## Prerequisites

- Read `./references/kanban_verbatim_handling.md`.
- Identify source board, source section, destination board, destination section.

## Step-by-Step Instructions

1. **Locate Exact Source Line**
   - Find the exact Markdown bullet line in the source section.
   - Preserve exact bytes including spaces and punctuation.

2. **Check for Ambiguity**
   - If multiple identical lines exist in the same source section, stop and ask the user to disambiguate.

3. **Perform Copy + Remove**
   - Copy the exact line into destination section.
   - Remove the same exact line from source section.
   - Do not reorder other task lines unless explicitly instructed.

4. **Generate Evidence**
   - Produce diff or before/after excerpts showing unchanged task text.
   - List each move as: `source -> destination: exact line`.

5. **Checkpoint Approval Boundary**
   - Present summary before commit approval.
   - If this is part of daily workflow, route commit/push through journal checkpoint policy.
   - Ensure today's journal repo work log captures the kanban move checkpoint before commit.

## Verification

- Task appears exactly once in destination (unless user requested duplicates).
- Task removed from source exactly once.
- Text in destination is byte-for-byte identical to original source line.

## Lifecycle Compliance

Prompt -> Plan (based on a known playbook) -> Request approval -> Execute -> Plan/playbook update -> Docs update -> Verification.

If this occurs inside a git repo:
- Review `git status` and relevant diffs.
- Suggest a commit message that summarizes the completed task.
- Commit after approved checkpoint completion.
