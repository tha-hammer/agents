# Reference: Context Window Management

Guidelines for managing context consumption during agent sessions. These are advisory — adopt the relevant practices based on your runtime environment.

## Why This Matters

Large language models have finite context windows. As context fills, performance degrades: instructions get forgotten, outputs become less coherent, and hallucination risk increases. Proactive context management keeps agent behavior consistent throughout long sessions.

## Key Principles

### 1. Know Your Budget
- A 200k token context window can shrink significantly when MCP servers, system prompts, and tool schemas are loaded.
- Treat usable context as roughly 50-70% of the advertised window after system overhead.
- When you notice declining output quality or instruction-following, context pressure is the likely cause.

### 2. Tool and MCP Limits
- Each active MCP server consumes context even when idle (tool schemas, connection metadata).
- **Guideline**: Keep active MCP servers under 10 and total active tools under 80 per session.
- When a tool is not needed for the current task, prefer not loading it over having it "just in case."
- If your runtime supports dynamic tool loading, load tools on demand rather than all at startup.

### 3. When to Compact or Summarize
- **ALWAYS compact** when shifting between major task phases (e.g., research complete, starting implementation).
- **ALWAYS compact** when you've accumulated large tool outputs (file reads, search results) that are no longer needed for the current step.
- **NEVER compact** mid-implementation when you need precise context about what you just changed.
- **NEVER compact** while actively debugging — you need the full error context.

### Compaction Decision Table

| Situation | Action |
|---|---|
| Research phase complete, starting implementation | Compact: summarize findings, release raw evidence |
| Large file reads accumulated from exploration | Compact: summarize what was learned, release file contents |
| Mid-implementation with active edits | Do NOT compact — you need precise diff context |
| Debugging with error traces loaded | Do NOT compact — you need full error evidence |
| Long conversation with many completed tasks | Compact: summarize completed work, keep only current task context |
| About to start a new unrelated task | Compact: clear prior task context |

### 4. Strategies for Long Sessions
- **Summarize before proceeding**: When finishing a research phase, write a summary of findings before starting implementation. This lets you release raw evidence from context.
- **Use files as external memory**: Write intermediate results to files rather than keeping them in context. Read them back when needed.
- **Chunk large operations**: Instead of reading 10 files into context at once, read 2-3, extract what you need, then proceed to the next batch.
- **Be explicit about what you're keeping**: When you need to retain specific details across a long conversation, state them explicitly in your responses so they survive compaction.

### 5. Signs of Context Pressure
Watch for these indicators that your context window is getting full:
- You start forgetting instructions from earlier in the conversation.
- Your outputs become more generic or less specific to the task.
- You repeat work you already did earlier in the session.
- Tool calls start failing or producing unexpected results.

When you notice these signs → ALWAYS inform the user and suggest compaction or a fresh session.
