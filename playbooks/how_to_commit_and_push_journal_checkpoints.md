# Playbook: Commit and Push Journal Checkpoints

*Status: Stable*

## Objective
Commit and push approved journal checkpoint snapshots while keeping journal workflow policy separate from general repository git operations.

## Prerequisites

- Journal checkpoint files are updated and user has reviewed the snapshot summary.
- Git is available and remote `origin` is configured.

## Step-by-Step Instructions

1. **Confirm Journal Checkpoint Scope**
   - Ensure the checkpoint includes journal updates for repo work performed.
   - Confirm staged files align with the discussed checkpoint.

2. **Review Status, Staging, and Untracked Files**
   - `git status -sb`
   - If untracked files exist, list them and leave them unstaged by default.
   - Do not stage untracked files unless explicitly requested.
   - `git diff --staged --stat`
   - `git diff --staged`

3. **Classify Approval Mode**
   - `journal-only mode`: staged changes are only journal file updates.
   - `mixed mode`: staged changes include non-journal files.

4. **Summarize the Checkpoint**
   - Provide:
     - files changed,
     - journal additions,
     - any kanban moves (verbatim lines).

5. **Apply Commit Approval Rule**
   - In `journal-only mode`, commit approval prompt is not required.
   - In `mixed mode`, ask:
     - "Approve saving this snapshot?"
     - "Approve commit + push for this journal checkpoint?"
   - In both modes, summarize what will be committed before executing.

6. **Commit**
   - Suggested message pattern:
     - `journal: checkpoint YYYY-MM-DD <short description>`
   - In `mixed mode`, run commit only after explicit approval.
   - In `journal-only mode`, run commit immediately after summary.

7. **Push Immediately**
   - Push to `origin` immediately after checkpoint commit.
   - Report success or exact failure.

## Notes

- This playbook applies to journal checkpoint workflow.
- General non-journal git tasks can continue using `./playbooks/how_to_commit_and_push_changes.md`.

## Verification

- Latest commit message matches checkpoint pattern.
- `git status -sb` is clean (or only expected untracked files remain).
- `git push origin HEAD` succeeds for checkpoint commits.

## Lifecycle Compliance

Prompt -> Plan (based on a known playbook) -> Request approval -> Execute -> Plan/playbook update -> Docs update -> Verification.

If this occurs inside a git repo:
- Review `git status` and relevant diffs.
- Ensure today's journal repo work log is updated before commit.
- Suggest a commit message that summarizes the completed checkpoint.
- Commit after checkpoint completion using the applicable approval mode above.
