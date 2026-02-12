# Context Management Reference

Source: https://kiro.dev/docs/cli/chat/context/

## Context Approaches

| Approach | Context Window Impact | Persistence | Best For |
|----------|----------------------|-------------|----------|
| Agent Resources | Always active (consumes tokens) | Persistent across sessions | Essential project files, standards, configs |
| Skills | On demand | Persistent across sessions | Large guides, reference docs, specialized knowledge |
| Session Context | Always active (consumes tokens) | Current session only | Temporary files, quick experiments |
| Knowledge Bases | Only when searched | Persistent across sessions | Large codebases, extensive documentation |

Decision: >10MB or thousands of files → Knowledge Bases. Need in every conversation → Agent Resources. Otherwise → Session Context.

## Persistent Context (Agent Resources)

```json
{
  "resources": [
    "file://README.md",
    "file://docs/**/*.md",
    "file://src/config.py"
  ]
}
```

URI schemes: `file://` (loaded at startup), `skill://` (on demand), `knowledgeBase` (indexed, searched on demand).

## Session Context (Temporary)

```bash
/context add README.md           # Add single file
/context add docs/*.md           # Add with glob
/context show                    # View usage and breakdown
/context remove src/temp-file.py # Remove file
/context clear                   # Clear all session context
```

Session context is temporary — does not persist across sessions. To make permanent, add to agent's `resources` field.

Cannot remove agent-defined context via `/context` commands.

## Knowledge Bases

For large datasets that would exceed context window limits:

```bash
kiro-cli settings chat.enableKnowledge true
/knowledge add /path/to/codebase --include "**/*.py" --exclude "node_modules/**"
```

Searched on-demand, doesn't consume context window until searched.

## Conversation Compaction

Summarizes older messages to free context window space.

- Manual: `/compact`
- Automatic: triggers on context window overflow
- Settings: `compaction.excludeMessages` (default 2), `compaction.excludeContextWindowPercent` (default 2)
- Creates a new session; resume original via `/chat resume`

## Context Window Limits

- Context files limited to 75% of model's context window
- Files exceeding limit are automatically dropped
- Monitor with `/context show`

## Default Agent for Context

Set a default agent to auto-load preferred context:

```bash
kiro-cli settings chat.defaultAgent my-project-agent
```
