---
tags:
  - domain/security
  - component/server
  - search
  - security
---
# Security Features

## Summary

OpenSearch v3.4.0 introduces several security plugin enhancements including HTTP Basic Authentication support for webhook audit log sinks, improved REST header handling for request tracing, deprecation of the manual system indices configuration setting, static/custom security config overlap handling, and updated permissions for search relevance indices.

## Details

### What's New in v3.4.0

#### 1. Webhook Audit Log Basic Authentication

Adds HTTP Basic Authentication support to the webhook audit log sink, enabling secure communication with authenticated webhook endpoints.

**Background**: In OpenSearch 2.x, users could embed credentials in webhook URLs (e.g., `https://user:pass@url.com`), but this was deprecated in 3.x due to the Apache HttpComponents Client5 upgrade. The existing `username` and `password` configuration settings only worked for `external_opensearch` sinks.

**New Behavior**:
- Webhook sinks now read `username` and `password` from configuration
- When credentials are configured, a properly formatted HTTP Basic Authentication header is automatically included
- Fully backward compatible - webhooks without credentials continue to work

**Configuration Example**:
```yaml
plugins.security.audit.type: webhook
plugins.security.audit.config.webhook.url: "https://your-webhook-endpoint.com/audit"
plugins.security.audit.config.webhook.format: "json"
plugins.security.audit.config.username: "audit_user"
plugins.security.audit.config.password: "secure_password"
```

#### 2. REST Headers ThreadContext Propagation

Fixes a bug where `SecurityRestFilter` was dropping allowlisted HTTP headers from the ThreadContext, preventing end-to-end request tracing.

**Problem**: The security plugin only preserved `X_OPAQUE_ID` header, dropping all other headers defined in `ActionPlugin.getRestHeaders()`.

**Solution**: All allowlisted headers from `ActionPlugin.getRestHeaders()` are now properly carried from HTTP headers to ThreadContext headers.

#### 3. System Indices Setting Deprecation

Deprecates `plugins.security.system_indices.indices` setting for removal in OpenSearch 4.0.

**Rationale**: Since OpenSearch 2.17, the security plugin uses the `SystemIndexRegistry` from OpenSearch core, which is composed of indices declared via `SystemIndexPlugin.getSystemIndexDescriptors()`. The manual configuration is no longer needed.

**Migration**: Remove `plugins.security.system_indices.indices` from your configuration. System indices are now automatically discovered from the registry.

#### 4. Static and Custom Security Config Overlap

Relaxes the restriction that prevented overlap between static config values (in `static_action_groups.yml` and `static_roles.yml`) and custom configs.

**Previous Behavior**: An exception was thrown if custom configs overlapped with static configs (e.g., `all_access`).

**New Behavior**: Overlap is now allowed, with static config values taking precedence. This enables adding missing static configs (like `kibana_all_read` and `kibana_all_write`) without breaking existing custom configurations.

#### 5. Search Relevance Index Permissions

Updates read access permissions for search relevance indices to support OpenSearch Dashboards visualization features.

**New Permissions**: The `search_relevance_read_access` action group now includes access to `search-relevance-experiment-results` index for visualization support.

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Audit Log Flow"
        AL[Audit Event] --> WS[WebhookSink]
        WS --> |"With Auth"| BA[Basic Auth Header]
        BA --> WH[Webhook Endpoint]
        WS --> |"Without Auth"| WH
    end
    
    subgraph "REST Header Flow"
        HTTP[HTTP Request] --> SRF[SecurityRestFilter]
        SRF --> TC[ThreadContext]
        TC --> |"All Allowlisted Headers"| Handler[Request Handler]
    end
    
    subgraph "Config Resolution"
        SC[Static Config] --> DCF[DynamicConfigFactory]
        CC[Custom Config] --> DCF
        DCF --> |"Prefer Static"| FC[Final Config]
    end
```

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.security.audit.config.username` | Username for webhook Basic Auth | None |
| `plugins.security.audit.config.password` | Password for webhook Basic Auth | None |

#### Deprecated Configuration

| Setting | Deprecation | Removal |
|---------|-------------|---------|
| `plugins.security.system_indices.indices` | v3.4.0 | v4.0.0 |

### Usage Example

**Webhook Audit Log with Basic Auth**:
```yaml
# opensearch.yml
plugins.security.audit.type: webhook
plugins.security.audit.config.webhook.url: "https://audit-collector.example.com/logs"
plugins.security.audit.config.webhook.format: json
plugins.security.audit.config.username: "opensearch_audit"
plugins.security.audit.config.password: "secure_audit_password"
plugins.security.audit.config.webhook.ssl.verify: true
```

**Search Relevance Read Access Role**:
```json
PUT _plugins/_security/api/roles/search_relevance_reader
{
  "cluster_permissions": [
    "cluster:admin/opensearch/search_relevance/experiment/get",
    "cluster:admin/opensearch/search_relevance/judgment/get"
  ],
  "index_permissions": [
    {
      "index_patterns": ["search-relevance-*"],
      "allowed_actions": [
        "indices:admin/mappings/get",
        "indices:data/read/search*",
        "indices:data/read/get*"
      ]
    }
  ]
}
```

### Migration Notes

1. **Webhook Authentication**: If using webhook audit logs with authenticated endpoints, add `username` and `password` settings instead of embedding credentials in URLs.

2. **System Indices**: Remove `plugins.security.system_indices.indices` from configuration files. The setting is deprecated and will be removed in v4.0.0.

3. **Static Config Overlap**: If you have custom configs that overlap with static configs, they will now be silently overridden by static values instead of throwing an exception.

## Limitations

- Webhook Basic Auth only supports HTTP Basic Authentication; other authentication methods (OAuth, API keys) are not supported
- The deprecated `plugins.security.system_indices.indices` setting still functions but will be removed in v4.0.0

## References

### Documentation
- [Audit Log Storage Types Documentation](https://docs.opensearch.org/3.0/security/audit-logs/storage-types/)
- [System Indexes Documentation](https://docs.opensearch.org/3.0/security/configuration/system-indices/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#5792](https://github.com/opensearch-project/security/pull/5792) | Add Basic Authentication support for webhook audit log sink |
| [#5396](https://github.com/opensearch-project/security/pull/5396) | Ensure REST headers from ActionPlugin.getRestHeaders are carried to ThreadContext |
| [#5775](https://github.com/opensearch-project/security/pull/5775) | Deprecate plugins.security.system_indices.indices setting |
| [#5805](https://github.com/opensearch-project/security/pull/5805) | Allow overlap of static and custom security configs, prefer static |
| [#5590](https://github.com/opensearch-project/security/pull/5590) | Update read access to search-relevance indices |

### Issues (Design / RFC)
- [Issue #5738](https://github.com/opensearch-project/security/issues/5738): Webhook audit log authentication bug report
- [Issue #4799](https://github.com/opensearch-project/security/issues/4799): SecurityRestFilter drops ThreadContext headers
- [Issue #5565](https://github.com/opensearch-project/security/issues/5565): Deprecate system_indices.indices setting

## Related Feature Report

- Full feature documentation
