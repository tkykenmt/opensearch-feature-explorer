---
tags:
  - security
---
# Security Testing Framework

## Summary

The Security Testing Framework provides integration test infrastructure for the OpenSearch Security plugin, enabling comprehensive testing of security features including resource access control, plugin extensions, and the sample-resource-plugin. It leverages OpenSearch's Plugin Testing Framework to support `ExtensiblePlugin` patterns in integration tests.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Test Infrastructure"
        TC[Test Class] --> LC[LocalCluster]
        LC --> MN[MockNode]
        MN --> SP[Security Plugin]
        MN --> SRP[Sample Resource Plugin]
    end
    
    subgraph "Plugin Extension"
        SP -->|ExtensiblePlugin| RSE[ResourceSharingExtension]
        SRP -->|implements| RSE
        SRP -->|extendedPlugins| SP
    end
    
    subgraph "Resource Sharing"
        RSE --> RSI[Resource Sharing Index]
        RSI --> RS[ResourceSharing]
        RS --> SW[ShareWith]
        SW --> SWAG[SharedWithActionGroup]
    end
```

### Data Flow

```mermaid
flowchart TB
    A[Test creates resource] --> B[Security plugin intercepts]
    B --> C[Create ResourceSharing entry]
    C --> D[Store in .opensearch_resource_sharing]
    D --> E[Test shares resource]
    E --> F[Fetch ResourceSharing doc]
    F --> G[Update sharing in memory]
    G --> H[Write back to index]
    H --> I[Verify access control]
```

### Components

| Component | Description |
|-----------|-------------|
| `LocalCluster` | Test cluster builder supporting PluginInfo configuration |
| `SampleResourcePlugin` | Example plugin demonstrating resource access control |
| `ResourceSharing` | Model for resource sharing configuration with docId tracking |
| `ShareWith` | Container for access level configurations |
| `SharedWithActionGroup` | Access control configuration per action group |
| `ActionGroupRecipients` | Recipients (users, roles, backend_roles) for an action group |
| `ResourceSharingIndexHandler` | Handles CRUD operations on resource sharing index |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `extendedPlugins` | List of plugins this plugin extends (in PluginInfo) | Empty list |
| `.opensearch_resource_sharing` | System index storing resource sharing entries | Auto-created |

### Usage Example

```java
// Define test cluster with Security plugin and extending plugin
@ClassRule
public static LocalCluster cluster = new LocalCluster.Builder()
    .clusterManager(ClusterManager.SINGLENODE)
    .plugin(PainlessModulePlugin.class)
    .plugin(
        new PluginInfo(
            SampleResourcePlugin.class.getName(),
            "classpath plugin",
            "NA",
            Version.CURRENT,
            "1.8",
            SampleResourcePlugin.class.getName(),
            null,
            List.of(OpenSearchSecurityPlugin.class.getName()),
            false
        )
    )
    .anonymousAuth(true)
    .authc(AUTHC_HTTPBASIC_INTERNAL)
    .users(USER_ADMIN, SHARED_WITH_USER)
    .build();

// Test resource creation and sharing
@Test
public void testCreateAndShareResource() throws Exception {
    // Create resource
    try (TestRestClient client = cluster.getRestClient(USER_ADMIN)) {
        String resource = """
            {"name": "test-resource"}
            """;
        HttpResponse response = client.postJson(SAMPLE_RESOURCE_CREATE_ENDPOINT, resource);
        response.assertStatusCode(HttpStatus.SC_OK);
        String resourceId = response.getTextFromJsonBody("/message").split(":")[1].trim();
        
        // Share with another user
        String sharePayload = shareWithPayload("read_access", SHARED_WITH_USER);
        response = client.postJson(SAMPLE_RESOURCE_SHARE_ENDPOINT + "/" + resourceId, sharePayload);
        response.assertStatusCode(HttpStatus.SC_OK);
    }
    
    // Verify shared user can access
    try (TestRestClient client = cluster.getRestClient(SHARED_WITH_USER)) {
        HttpResponse response = client.get(SAMPLE_RESOURCE_GET_ENDPOINT + "/" + resourceId);
        response.assertStatusCode(HttpStatus.SC_OK);
    }
}
```

## Limitations

- Requires OpenSearch core v3.1.0+ with Plugin Testing Framework enhancements
- Test plugins must be on the classpath
- Extensions require `META-INF/services` files for ServiceLoader discovery
- Resource sharing tests require the Security plugin to be properly configured

## Change History

- **v3.1.0** (2025-05-13): Use extendedPlugins in integrationTest framework for sample resource plugin testing, refactor resource sharing to use in-memory updates
- **v3.0.0** (2025-03-25): Added ConfigurationRepository tests, FLS/field masking tests, refactored InternalAuditLogTest to use Awaitility, migrated packages from com.amazon.dlic to org.opensearch.security


## References

### Documentation
- [Security Plugin Documentation](https://docs.opensearch.org/3.0/security/index/): OpenSearch Security plugin docs
- [PR #5322](https://github.com/opensearch-project/security/pull/5322): Security plugin test framework update
- [PR #16908](https://github.com/opensearch-project/OpenSearch/pull/16908): Core Plugin Testing Framework
- Plugin Testing Framework: Core testing framework feature

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.1.0 | [#5322](https://github.com/opensearch-project/security/pull/5322) | Use extendedPlugins in integrationTest framework |   |
| v3.1.0 | [#16908](https://github.com/opensearch-project/OpenSearch/pull/16908) | Core Plugin Testing Framework enhancement |   |
| v3.0.0 | [#5206](https://github.com/opensearch-project/security/pull/5206) | Tests for ConfigurationRepository class | [#3255](https://github.com/opensearch-project/security/issues/3255) |
| v3.0.0 | [#5214](https://github.com/opensearch-project/security/pull/5214) | Refactor InternalAuditLogTest to use Awaitility |   |
| v3.0.0 | [#5218](https://github.com/opensearch-project/security/pull/5218) | Remove Java version check for reflection args |   |
| v3.0.0 | [#5223](https://github.com/opensearch-project/security/pull/5223) | Migrate from com.amazon.dlic to org.opensearch.security |   |
| v3.0.0 | [#5237](https://github.com/opensearch-project/security/pull/5237) | More tests for FLS and field masking |   |

### Issues (Design / RFC)
- [Issue #3255](https://github.com/opensearch-project/security/issues/3255): Test coverage improvement tracking
