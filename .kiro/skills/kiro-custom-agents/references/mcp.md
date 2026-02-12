# MCP (Model Context Protocol) Reference

Source: https://kiro.dev/docs/cli/mcp/

MCP extends Kiro's capabilities by connecting to specialized servers that provide additional tools and context.

Use `/mcp` slash command in chat to see loaded MCP servers.

## Setup Methods

### CLI

```bash
kiro-cli mcp add \
  --name "server-name" \
  --scope global \
  --command "uvx" \
  --args "package@latest" \
  --env "KEY=value"
```

### mcp.json

Location: `<project-root>/.kiro/settings/mcp.json` or `~/.kiro/settings/mcp.json`

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-run",
      "args": ["arg1"],
      "env": { "KEY": "value" },
      "disabled": false
    }
  }
}
```

### In Agent Config

```json
{
  "mcpServers": {
    "fetch": { "command": "fetch3.1", "args": [] }
  },
  "includeMcpJson": false
}
```

`includeMcpJson: true` merges servers from workspace and user-level mcp.json files into the agent.

## Remote MCP Servers

```json
{
  "mcpServers": {
    "remote-service": {
      "type": "http",
      "url": "https://api.example.com/mcp"
    }
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection failures | Verify prerequisites installed |
| Permission errors | Check tokens/API keys |
| Tool not responding | Review MCP logs |
| Config not loading | Validate JSON syntax |

## Additional Resources

- [Official MCP Documentation](https://modelcontextprotocol.io/introduction)
- [MCP Examples](https://kiro.dev/docs/cli/mcp/examples/)
- [MCP Security Best Practices](https://kiro.dev/docs/cli/mcp/security/)
- [MCP Configuration](https://kiro.dev/docs/cli/mcp/configuration/)
