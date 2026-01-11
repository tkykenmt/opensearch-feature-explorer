# Security Features

## Summary

The OpenSearch Security plugin provides comprehensive security capabilities including authentication, authorization, audit logging, and access control. This document covers the security features related to audit logging, configuration management, and REST header handling that have been enhanced across OpenSearch versions.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Security Plugin Architecture"
        subgraph "Authentication Layer"
            HTTP[HTTP Request] --> SRF[SecurityRestFilter]
            SRF --> Auth[Authentication]
            Auth --> TC[ThreadContext]
        end
        
        subgraph "Configuration Layer"
            SC[Static Config] --> DCF[DynamicConfigFactory]
            CC[Custom Config] --> DCF
            SIR[SystemIndexRegistry] --> DCF
            DCF --> Config[Resolved Config]
        end
        
        subgraph "Audit Layer"
            AE[Audit Events] --> AS[AuditSink]
            AS --> IS[Internal OpenSearch]
            AS --> ES[External OpenSearch]
            AS --> WS[Webhook Sink]
            AS --> L4J[Log4j]
        end
    end
```

### Data Flow

```mermaid
flowchart TB
    subgraph "Webhook Audit Flow"
        Event[Audit Event] --> Format[Format Message]
        Format --> CheckAuth{Auth Configured?}
        CheckAuth -->|Yes| AddAuth[Add Basic Auth Header]
        CheckAuth -->|No| Send
        AddAuth --> Send[Send to Webhook]
    end
    
    subgraph "REST Header Flow"
        REQ[HTTP Request] --> Extract[Extract Headers]
        Extract --> Filter[Filter Allowlisted]
        Filter --> Propagate[Propagate to ThreadContext]
        Propagate --> Handler[Request Handler]
    end
```

### Components

| Component | Description |
|-----------|-------------|
| SecurityRestFilter | Filters REST requests and manages header propagation to ThreadContext |
| WebhookSink | Sends audit log events to external webhook endpoints with optional authentication |
| DynamicConfigFactory | Resolves security configuration from static and custom sources |
| SystemIndexRegistry | Central registry for system indices from all plugins |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.security.audit.type` | Audit log storage type (debug, internal_opensearch, external_opensearch, webhook, log4j) | internal_opensearch |
| `plugins.security.audit.config.webhook.url` | Webhook endpoint URL | None |
| `plugins.security.audit.config.webhook.format` | Message format (URL_PARAMETER_GET, URL_PARAMETER_POST, TEXT, JSON, SLACK) | JSON |
| `plugins.security.audit.config.username` | Username for webhook/external_opensearch Basic Auth | None |
| `plugins.security.audit.config.password` | Password for webhook/external_opensearch Basic Auth | None |
| `plugins.security.audit.config.webhook.ssl.verify` | Verify TLS certificate of webhook endpoint | true |
| `plugins.security.system_indices.indices` | Manual system indices list (DEPRECATED in v3.4.0) | None |

### Usage Example

**Webhook Audit Log Configuration**:
```yaml
# opensearch.yml
plugins.security.audit.type: webhook
plugins.security.audit.config.webhook.url: "https://audit-collector.example.com/logs"
plugins.security.audit.config.webhook.format: json
plugins.security.audit.config.username: "opensearch_audit"
plugins.security.audit.config.password: "secure_audit_password"
plugins.security.audit.config.webhook.ssl.verify: true
plugins.security.audit.config.webhook.ssl.pemtrustedcas_filepath: /path/to/ca.pem
```

**Search Relevance Permissions**:
```json
PUT _plugins/_security/api/roles/search_relevance_reader
{
  "cluster_permissions": [
    "cluster:admin/opensearch/search_relevance/experiment/get",
    "cluster:admin/opensearch/search_relevance/judgment/get",
    "cluster:admin/opensearch/search_relevance/queryset/get",
    "cluster:admin/opensearch/search_relevance/search_configuration/get"
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

## Limitations

- Webhook audit log authentication only supports HTTP Basic Authentication
- Static security configs always take precedence over custom configs when there is overlap
- The `plugins.security.system_indices.indices` setting is deprecated and will be removed in v4.0.0

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.4.0 | [#5792](https://github.com/opensearch-project/security/pull/5792) | Add Basic Authentication support for webhook audit log sink |
| v3.4.0 | [#5396](https://github.com/opensearch-project/security/pull/5396) | Ensure REST headers from ActionPlugin.getRestHeaders are carried to ThreadContext |
| v3.4.0 | [#5775](https://github.com/opensearch-project/security/pull/5775) | Deprecate plugins.security.system_indices.indices setting |
| v3.4.0 | [#5805](https://github.com/opensearch-project/security/pull/5805) | Allow overlap of static and custom security configs, prefer static |
| v3.4.0 | [#5590](https://github.com/opensearch-project/security/pull/5590) | Update read access to search-relevance indices |

## References

- [Issue #5738](https://github.com/opensearch-project/security/issues/5738): Webhook audit log authentication bug report
- [Issue #4799](https://github.com/opensearch-project/security/issues/4799): SecurityRestFilter drops ThreadContext headers
- [Issue #5565](https://github.com/opensearch-project/security/issues/5565): Deprecate system_indices.indices setting
- [Audit Log Storage Types Documentation](https://docs.opensearch.org/3.0/security/audit-logs/storage-types/)
- [System Indexes Documentation](https://docs.opensearch.org/3.0/security/configuration/system-indices/)
- [Security Settings Documentation](https://docs.opensearch.org/3.0/install-and-configure/configuring-opensearch/security-settings/)

## Change History

- **v3.4.0** (2026-01): Added webhook Basic Auth support, fixed REST header propagation, deprecated system_indices.indices setting, allowed static/custom config overlap, updated search relevance permissions
