# Steering Reference

Source: https://kiro.dev/docs/cli/steering/

Steering gives Kiro persistent knowledge about your project through markdown files.

## Scope

- **Workspace**: `.kiro/steering/*.md` — applies to current workspace only
- **Global**: `~/.kiro/steering/*.md` — applies to all workspaces
- Workspace steering overrides global steering on conflict.

### Team Steering

Global steering can define centralized steering files for entire teams. Team steering files can be pushed to user PCs via MDM solutions or Group Policies, or downloaded from a central repository, and placed into `~/.kiro/steering/`.

## Foundational Files

- `product.md` — Product purpose, target users, key features, business objectives
- `tech.md` — Frameworks, libraries, development tools, technical constraints
- `structure.md` — File organization, naming conventions, import patterns, architecture

## Creating Custom Steering Files

1. Create a new `.md` file in `.kiro/steering/`
2. Choose a descriptive filename (e.g., `api-standards.md`)
3. Write guidance using standard markdown
4. Use natural language to describe requirements

## Custom Agents + Steering

Steering files are NOT automatically included in custom agents. Add explicitly:

```json
{
  "resources": ["file://.kiro/steering/**/*.md"]
}
```

## AGENTS.md

Kiro supports the [AGENTS.md](https://agents.md/) standard. Place in `~/.kiro/steering/` or workspace root. Always included automatically (unlike regular steering files in custom agents).

## Best Practices

- Keep files focused: one domain per file
- Use clear names: `api-rest-conventions.md`, `testing-unit-patterns.md`
- Include context: explain why decisions were made, not just what
- Provide examples: code snippets and before/after comparisons
- Security first: never include API keys, passwords, or sensitive data
- Maintain regularly: review during sprint planning and architecture changes

## Common Steering File Strategies

- **API Standards** (`api-standards.md`) — REST conventions, error formats, auth flows, versioning
- **Testing Approach** (`testing-standards.md`) — Unit test patterns, mocking, coverage expectations
- **Code Style** (`code-conventions.md`) — Naming patterns, file organization, anti-patterns
- **Security Guidelines** (`security-policies.md`) — Auth requirements, input sanitization, secure coding
- **Deployment Process** (`deployment-workflow.md`) — Build procedures, CI/CD, rollback strategies
