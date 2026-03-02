# Reference: Agent Roles and Model Tiering

Advisory guidance for dispatching sub-agents with appropriate roles, model tiers, and tool scopes. These are recommendations, not enforced constraints.

## Why This Matters

Different tasks have different requirements for capability, cost, and speed. Using the most capable model for every sub-task wastes resources. Using the cheapest model for complex analysis produces poor results. Matching the model to the task improves both outcomes and efficiency.

## Model Tier Guidelines

### Tier 1: Lightweight (e.g., Haiku)
**Best for**: Fast, narrow, well-defined tasks with low ambiguity.
- File searching, pattern matching, directory exploration
- Simple text extraction and formatting
- Structural analysis (file counts, directory trees, dependency lists)
- Running pre-defined checks or validations

**Characteristics**: Fast, cheap, reliable for narrow scope. Poor at nuance, multi-step reasoning, or ambiguous instructions.

### Tier 2: Balanced (e.g., Sonnet)
**Best for**: Standard development, analysis, and review tasks.
- Code implementation and modification
- Code review with specific focus areas
- Documentation writing and updating
- Test writing and debugging
- Single-domain analysis (one system, one codebase)

**Characteristics**: Good balance of capability and cost. Handles most development tasks well. May struggle with very complex architectural decisions or cross-domain synthesis.

### Tier 3: Advanced (e.g., Opus)
**Best for**: Complex reasoning, architecture, and cross-cutting analysis.
- Architecture and design decisions
- Cross-system analysis and integration planning
- Assimilation and deep comparison work
- Planning complex multi-step implementations
- Resolving ambiguous or conflicting requirements

**Characteristics**: Highest capability, highest cost, slower. Use when the task genuinely requires deep reasoning or when lower tiers have failed.

## Common Agent Roles

### Planner
- **Purpose**: Analyze requirements and produce implementation plans.
- **Recommended tier**: Tier 3 (complex planning) or Tier 2 (straightforward planning).
- **Tool scope**: Read-only. Planners should NOT modify files.
- **Key behavior**: Produce atomic, reviewable plans. Identify risks and unknowns. NEVER implement during planning.

### Implementer
- **Purpose**: Execute approved plans by writing code and documentation.
- **Recommended tier**: Tier 2.
- **Tool scope**: Read + write for files in the approved plan scope.
- **Key behavior**: Follow the plan exactly. Stop and report if the plan doesn't match reality. Run tests after changes.

### Reviewer
- **Purpose**: Inspect code, docs, or changes for bugs, risks, and quality issues.
- **Recommended tier**: Tier 2 (standard review) or Tier 3 (security/architecture review).
- **Tool scope**: Read-only.
- **Key behavior**: Severity-first (see `./contexts/review.md`). Report issues with specific locations and suggested fixes. NEVER modify files during review.

### Researcher
- **Purpose**: Gather and synthesize information from codebases, documentation, or external sources.
- **Recommended tier**: Tier 2 (focused research) or Tier 1 (structural search).
- **Tool scope**: Read-only + web search if applicable.
- **Key behavior**: Evidence-first (see `./contexts/research.md`). Cite sources. Distinguish facts from inferences.

### Search Worker
- **Purpose**: Find files, patterns, or structural information quickly.
- **Recommended tier**: Tier 1.
- **Tool scope**: Read-only (grep, glob, ls, file reads).
- **Key behavior**: Return results efficiently. No analysis or recommendations — just the data.

## Dispatching Sub-Agents

When dispatching multiple sub-agents:

1. **Match the role to the tier**: Use the guidelines above to select the appropriate model.
2. **Define scope explicitly**: Tell each agent exactly what files/directories to examine and what output to produce.
3. **Prefer parallel dispatch**: When sub-agent tasks are independent, dispatch them all at once.
4. **Keep search agents narrow**: A search agent should answer one specific question, not explore broadly.
5. **Reserve advanced tiers for synthesis**: Use Tier 1/2 agents to gather data, then Tier 3 to synthesize if needed.

## Anti-Patterns
- NEVER use Tier 3 for simple file searches or pattern matching.
- NEVER use Tier 1 for tasks requiring nuanced judgment or complex reasoning.
- NEVER give a read-only role write access "just in case."
- NEVER dispatch a single agent to do work that could be parallelized across 3-5 agents.
