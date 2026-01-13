---
tags:
  - domain/core
  - component/server
  - ml
  - security
---
# Java Agent JRT Protocol Fix

## Summary

This release fixes a bug in OpenSearch's Java agent where connections to external MCP (Model Context Protocol) servers failed with a `SecurityException`. The issue occurred because the Java agent's protection domain extraction incorrectly included JDK internal classes loaded via the `jrt:` protocol, which have no permissions granted.

## Details

### What's New in v3.4.0

The `StackCallerProtectionDomainChainExtractor` now filters out protection domains with `jrt:` protocol URLs. This prevents false security denials when JDK internal classes (like `java.net.http.HttpClient`) appear in the call stack during network operations.

### Technical Changes

#### Root Cause

When OpenSearch's Java agent intercepts network operations, it walks the call stack to identify which code is requesting the operation. Each stack frame's class has a `ProtectionDomain` that determines its permissions.

JDK internal classes (loaded from `jrt:/java.net.http`) have protection domains with no granted permissions. When these classes appeared in the call stack (e.g., when using `HttpClient` for MCP connections), the agent incorrectly denied access because the JDK classes had no socket permissions.

#### The Fix

A single-line filter was added to exclude protection domains with `jrt:` protocol URLs:

```java
.filter(pd -> !"jrt".equals(pd.getCodeSource().getLocation().getProtocol()))
```

This ensures JDK internal classes are treated similarly to classes with null code sources (which were already filtered out).

#### Code Change

```java
// StackCallerProtectionDomainChainExtractor.java
public Collection<ProtectionDomain> apply(Stream<StackFrame> frames) {
    return frames.takeWhile(
        frame -> !(ACCESS_CONTROLLER_CLASSES.contains(frame.getClassName()) 
                   && DO_PRIVILEGED_METHODS.contains(frame.getMethodName()))
    )
        .map(StackFrame::getDeclaringClass)
        .map(Class::getProtectionDomain)
        .filter(pd -> pd.getCodeSource() != null) // Filter out JDK classes
        .filter(pd -> !"jrt".equals(pd.getCodeSource().getLocation().getProtocol())) // NEW: Filter jrt: URLs
        .collect(Collectors.toSet());
}
```

### Error Before Fix

```
java.lang.SecurityException: Denied access to: my-mcp-endpoint:443, 
domain ProtectionDomain (jrt:/java.net.http <no signer certificates>)
 jdk.internal.loader.ClassLoaders$PlatformClassLoader@d8948cd
 <no principals>
 java.security.Permissions@4633b6d ()
```

### Usage Example

After this fix, MCP connector operations work correctly:

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "My MCP Server",
  "description": "External MCP server connector",
  "version": "1",
  "protocol": "mcp",
  "parameters": {
    "endpoint": "https://my-mcp-endpoint:443/sse"
  }
}
```

## Limitations

- This fix specifically addresses the `jrt:` protocol filtering; other protocol-related issues may require separate fixes
- The Java agent security model still requires proper `plugin-security.policy` configuration for plugin code

## References

### Blog Posts
- [Blog: Finding a replacement for JSM in OpenSearch 3.0](https://opensearch.org/blog/finding-a-replacement-for-jsm-in-opensearch-3-0/): Background on Java agent security model

### Pull Requests
| PR | Description |
|----|-------------|
| [#19683](https://github.com/opensearch-project/OpenSearch/pull/19683) | Allow JRT protocol URLs in protection domain extraction |

### Issues (Design / RFC)
- [Issue #4209](https://github.com/opensearch-project/ml-commons/issues/4209): Bug report - Failed to get tools from external MCP server

## Related Feature Report

- Full feature documentation
