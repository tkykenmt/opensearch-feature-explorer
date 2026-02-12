# Troubleshooting

Source: https://kiro.dev/docs/cli/custom-agents/troubleshooting/

## Configuration Errors

**Invalid JSON**: Validate JSON syntax. Check for missing commas, trailing commas, unmatched brackets, unescaped quotes. Use `/agent schema` to verify structure.

**Schema validation**: Compare config against schema. Check field name typos (e.g. `allowedTools` not `allowedTool`). Verify data types match.

## Agent Loading Issues

**Agent not found**:
- Verify file location: Global `~/.kiro/agents/[name].json`, Local `.kiro/agents/[name].json`
- Check file permissions and `.json` extension
- Filename must match agent name

**Wrong version loading**: Local agents take precedence over global. Use `/agent list` to check which version loads.

## Tool Permission Problems

**Tool not available**:
- Verify tool names in `tools` array
- For MCP tools: ensure server configured in `mcpServers` and use `@server_name/tool_name` syntax
- Check MCP servers are running

**`/tools` returns empty**: Check `tools` array has valid names. Verify MCP tool format (use `@server-name___tool-name` for server-prefixed format). Test with default agent.

**Unexpected permission prompts**: Ensure tools listed in BOTH `tools` and `allowedTools`. Use full server-prefixed name for MCP tools. Verify `toolAliases` are correctly applied.

## Debugging

**Missing context/resources**: Verify file paths exist. Check glob patterns. Test hook commands manually. Check timeout settings.

**MCP server issues**: Verify commands are in PATH. Check env vars. Test servers independently. Increase timeout values.

## Testing Checklist

1. Validate JSON syntax
2. Check against schema: `/agent schema`
3. Test loading: `/agent list`
4. Switch to agent: `/agent swap [name]`
5. Test each tool individually
6. Verify resources and hooks
7. Test common workflows
