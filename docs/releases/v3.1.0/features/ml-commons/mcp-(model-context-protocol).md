# MCP (Model Context Protocol)

## Summary

This release includes bugfixes for the MCP (Model Context Protocol) feature in ml-commons. The changes include adding comprehensive unit tests for MCP components and downgrading the MCP SDK version from 0.10.0-SNAPSHOT to 0.9.0 for improved compatibility with MCP servers.

## Details

### What's New in v3.1.0

This release focuses on stability and compatibility improvements for the MCP feature:

1. **Unit Test Coverage**: Added comprehensive unit tests for MCP components to improve code quality and reliability
2. **MCP SDK Version Downgrade**: Changed from custom 0.10.0-SNAPSHOT JAR to official 0.9.0 release for better compatibility

### Technical Changes

#### MCP SDK Version Change

The MCP SDK dependency was changed from a custom snapshot JAR to the official release:

```gradle
// Before (v3.0.0)
api files('libs/mcp-0.10.0-SNAPSHOT.jar')

// After (v3.1.0)
api('io.modelcontextprotocol.sdk:mcp:0.9.0')
```

This change:
- Uses the official MCP SDK 0.9.0 release instead of a custom snapshot
- Improves compatibility with MCP servers
- Includes backported custom headers support from 0.10

#### Content-Type Header Removal

Removed redundant `Content-Type: application/json` header from `McpConnectorExecutor` since the MCP client adds it by default:

```java
// Removed from McpConnectorExecutor.java
builder.header("Content-Type", "application/json");
```

#### Reactor Core Version Pinning

Added explicit version pinning for reactor-core to ensure compatibility:

```gradle
resolutionStrategy.force 'io.projectreactor:reactor-core:3.7.0'
```

#### New Unit Tests

Added comprehensive test coverage for MCP components:

| Test Class | Description |
|------------|-------------|
| `McpConnectorTest` | Tests for MCP connector serialization, encryption, decryption, URL validation, and updates |
| `McpConnectorExecutorTest` | Tests for MCP tool spec retrieval and error handling |
| `McpSseToolTests` | Tests for MCP SSE tool execution, validation, and factory methods |
| `AgentUtilsTest` (extended) | Tests for `getMcpToolSpecs()` including connector handling, tool filtering, and multi-connector merging |

### Usage Example

No changes to the MCP usage API. The MCP connector and server continue to work as documented:

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "External MCP Server",
  "description": "Connect to external MCP server",
  "version": "1",
  "protocol": "mcp_sse",
  "url": "http://mcp-server:8080",
  "headers": {
    "Authorization": "Bearer ${credential.api_key}"
  },
  "credential": {
    "api_key": "your-api-key"
  }
}
```

### Migration Notes

No migration required. The SDK version change is backward compatible.

## Limitations

- MCP remains an experimental feature
- MCP server requires `transport-reactor-netty4` plugin to be enabled

## References

### Documentation
- [Using MCP Tools Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/mcp/index/)
- [Connecting to External MCP Server](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/mcp/mcp-connector/)

### Blog Posts
- [Introducing MCP in OpenSearch Blog](https://opensearch.org/blog/introducing-mcp-in-opensearch/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#3787](https://github.com/opensearch-project/ml-commons/pull/3787) | Add Unit Tests for MCP feature |
| [#3821](https://github.com/opensearch-project/ml-commons/pull/3821) | Downgrade MCP version to 0.9 |

### Issues (Design / RFC)
- [Issue #3743](https://github.com/opensearch-project/ml-commons/issues/3743): Add test cases for MCP experimental feature

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-commons-mcp.md)
