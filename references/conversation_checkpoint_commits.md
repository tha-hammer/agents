# Conversation Checkpoint Commits

## What Is a Checkpoint

- A checkpoint is a completed conversation slice, not project completion.
- Examples:
  - Daily kickoff captured and written.
  - Kanban moves applied and recorded.
  - A focused bugfix discussion captured with resulting file edits.

## What to Include in Checkpoint Summary

- Files changed and why.
- Journal updates added in this checkpoint.
- Kanban moves with exact task text.
- Any unresolved items or follow-up questions.

## Approval Language Pattern

- "Here is what I captured and where it will be written."
- "Approve saving this snapshot?"
- "Approve commit + push for this journal checkpoint?"
- Journal-only exception: if staged scope is only journal updates, commit/push may proceed without a commit approval prompt after summary.

## Avoiding Commit Spam While Preserving Auditability

- Commit at meaningful checkpoint boundaries rather than every single message.
- Keep each checkpoint commit small and scoped.
- Use consistent commit messages with date + checkpoint intent.
- Treat "completed change" as "completed checkpoint" for commit cadence in this workflow.
