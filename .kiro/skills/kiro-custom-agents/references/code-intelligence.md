# Code Intelligence Reference

Source: https://kiro.dev/docs/cli/code-intelligence/

Kiro CLI provides out-of-the-box code intelligence for 18 languages without setup.

## Built-in Features (No Setup)

- Symbol search (fuzzy matching), document symbols, symbol lookup
- AST-based pattern search and rewrite
- Codebase overview and codebase map

Supported: Bash, C, C++, C#, Elixir, Go, Java, JavaScript, Kotlin, Lua, PHP, Python, Ruby, Rust, Scala, Swift, TSX, TypeScript

## Slash Commands

- `/code overview [path]` — Codebase overview (add `--silent` for cleaner output)
- `/code summary` — Generate AGENTS.md, README.md, or CONTRIBUTING.md (interactive)
- `/code init` — Initialize LSP integration
- `/code init -f` — Force restart LSP servers
- `/code status` — Show workspace status and LSP server states
- `/code logs` — Check LSP logs

### /code logs Options

```bash
/code logs                    # Last 20 ERROR logs
/code logs -l INFO            # INFO level and above
/code logs -n 50              # Last 50 entries
/code logs -l DEBUG -n 100    # Last 100 DEBUG+ logs
/code logs -p ./lsp-logs.json # Export logs to JSON
```

Flags: `-l, --level` (ERROR/WARN/INFO/DEBUG/TRACE, default ERROR), `-n, --lines` (default 20), `-p, --path` (export to JSON).

## Pattern Search & Rewrite

AST-based structural code search and transformation using metavariables:
- `$VAR` — Matches single node (identifier, expression)
- `$$$` — Matches zero or more nodes (statements, parameters)

Search examples:
```
console.log($ARG)                           # Find all console.log calls
async function $NAME($$$PARAMS) { $$$ }     # Find all async functions
$E.unwrap()                                 # Find all .unwrap() calls
```

Rewrite examples:
```
var $N = $V  →  const $N = $V
$O.hasOwnProperty($P)  →  Object.hasOwn($O, $P)
$E.unwrap()  →  $E.expect("unexpected None")
```

Workflow: pattern_search → review matches → pattern_rewrite with dry_run: true → apply with dry_run: false.

## LSP Integration (Optional)

Enables: find references, go to definition, hover docs, rename refactoring, diagnostics, completions.

Initialize: `/code init` (creates `.kiro/settings/lsp.json`)

Auto-initialization: after first `/code init`, Kiro CLI auto-initializes on startup when `lsp.json` exists.

Disable: delete `lsp.json`. Re-enable with `/code init`.

### Language Servers

| Language | Server | Install |
|----------|--------|---------|
| TypeScript/JS | typescript-language-server | `npm install -g typescript-language-server typescript` |
| Rust | rust-analyzer | `rustup component add rust-analyzer` |
| Python | pyright | `pip install pyright` |
| Go | gopls | `go install golang.org/x/tools/gopls@latest` |
| Java | jdtls | `brew install jdtls` |
| Ruby | solargraph | `gem install solargraph` |
| C/C++ | clangd | `brew install llvm` (macOS) or `apt install clangd` (Linux) |
| Kotlin | kotlin-language-server | `brew install kotlin-language-server` |

### Using Language Servers

Natural language queries for semantic code intelligence:

- Find symbols: "Find the UserRepository class"
- Find references: "Find references of Person class"
- Go to definition: "Find the definition of UserService"
- Get file symbols: "What symbols are in auth.service.ts?"
- Rename (dry run): "Dry run: rename FetchUser to fetchUserData"
- Get diagnostics: "Get diagnostics for main.ts"
- Hover docs: "What's the documentation for the authenticate method?"
- Discover APIs: "What methods are available on s3Client?"

### Custom Language Servers

Edit `.kiro/settings/lsp.json`:

```json
{
  "languages": {
    "mylang": {
      "name": "my-language-server",
      "command": "my-lsp-binary",
      "args": ["--stdio"],
      "file_extensions": ["mylang"],
      "project_patterns": ["mylang.config"],
      "exclude_patterns": ["**/build/**"],
      "multi_workspace": false,
      "initialization_options": {},
      "request_timeout_secs": 60
    }
  }
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|---------|
| Code tool not enabled | Agent missing code tool | Add `"code"` to tools array, or use `@builtin` |
| Workspace still initializing | LSP servers starting | Wait, or `/code init -f` to restart |
| LSP initialization failed | — | Check `/code logs -l ERROR` |
| No symbols found | Still indexing or syntax errors | Check file for errors, try broader search |
| No definition found | Position doesn't point to symbol | Verify row/column numbers |

## Best Practices

1. Initialize once per project with `/code init`
2. Use exact positions for row/column queries
3. Use dry_run for renames before applying
4. Check diagnostics first — syntax errors prevent analysis
5. Be specific in searches: "UserService" > "user"
6. Ask naturally: "What does the login method do?"
7. Discover APIs conversationally: "What methods does s3Client have?"
