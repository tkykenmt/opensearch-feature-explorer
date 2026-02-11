---
tags:
  - security
---
# Security Enhancements

## Summary

OpenSearch v3.5.0 brings significant security enhancements including JWT authentication for gRPC transport, HTTP/3 server-side support, new DLS write blocking settings, audit log timezone configuration, and nested JWT claim access via dot notation. This release also includes numerous bug fixes and dependency updates.

## Details

### What's New in v3.5.0

#### JWT Authentication for gRPC Transport
The security plugin now supports JWT authentication over the gRPC transport layer. This enables secure authentication for gRPC-based communication using the same JWT configuration as the REST API.

Key features:
- Shares auth domains with REST API
- Uses same JWT HTTP headers as REST API
- Tokens validated against the same authentication backend
- Currently supports `HTTPJwtAuthenticator` only

Limitations:
- Superuser authentication not supported over gRPC (use REST API for configuration changes)
- Anonymous auth not supported over gRPC

Configuration example:
```yaml
aux.transport.types: [secure-transport-grpc]
plugins.security.ssl.aux.secure-transport-grpc.pemkey_filepath: esnode-key.pem
plugins.security.ssl.aux.secure-transport-grpc.pemcert_filepath: esnode.pem
plugins.security.ssl.aux.secure-transport-grpc.pemtrustedcas_filepath: root-ca.pem
plugins.security.ssl.aux.secure-transport-grpc.enabled: true
```

#### HTTP/3 Server-Side Support
Added support for HTTP/3 transport in the security plugin, enabling QUIC-based communication for improved performance and security.

#### DLS Write Blocking Setting
New dynamic cluster setting `plugins.security.dls.write_blocked` to block all write operations against indices where DLS restrictions apply.

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.security.dls.write_blocked` | Block all writes when DLS restrictions apply | `false` |

When set to `true`, all write operations (IndexRequest, UpdateRequest, DeleteRequest) are blocked. When `false` (default), only UpdateRequest is blocked.

#### Nested JWT Claims via Dot Notation
Enhanced JWT claim access to support nested claims using dot notation, enabling access to deeply nested JWT structures.

Example JWT:
```json
{
  "sub": "Leonard McCoy",
  "active_tenant": {
    "tenant_id": "enterprise",
    "roles": ["admin", "user"]
  }
}
```

Access nested claims:
- `attr.jwt.sub` = "Leonard McCoy"
- `attr.jwt.active_tenant.tenant_id` = "enterprise"
- `attr.jwt.active_tenant.roles` = ["admin", "user"]

### Technical Changes

#### New Features
| PR | Description |
|----|-------------|
| [#5916](https://github.com/opensearch-project/security/pull/5916) | JWT authentication for gRPC transport |
| [#5886](https://github.com/opensearch-project/security/pull/5886) | HTTP/3 server-side support |
| [#5828](https://github.com/opensearch-project/security/pull/5828) | DLS write blocking setting |
| [#1366](https://github.com/opensearch-project/security-dashboards-plugin/pull/1366) | Standardize rule structure across API and UI |
| [#2350](https://github.com/opensearch-project/security-dashboards-plugin/pull/2350) | Multi-datasource support in Resource Access Management |

#### Enhancements
| PR | Description |
|----|-------------|
| [#5891](https://github.com/opensearch-project/security/pull/5891) | Nested JWT claims via dot notation |
| [#5858](https://github.com/opensearch-project/security/pull/5858) | Skip hasExplicitIndexPrivilege check for plugin users accessing own system indices |
| [#5894](https://github.com/opensearch-project/security/pull/5894) | Implement buildSecureClientTransportEngine with serverName parameter |
| [#5883](https://github.com/opensearch-project/security/pull/5883) | Serialize Search Request object in DLS Filter Level Handler only when needed |
| [#1636](https://github.com/opensearch-project/security-dashboards-plugin/pull/1636) | Include AdditionalCodecs argument for additional Codec registration |

#### Bug Fixes
| PR | Description |
|----|-------------|
| [#5929](https://github.com/opensearch-project/security/pull/5929) | Make gRPC JWT header keys case insensitive |
| [#5478](https://github.com/opensearch-project/security/pull/5478) | Fix partial cache update post snapshot restore |
| [#5797](https://github.com/opensearch-project/security/pull/5797) | Fix IllegalArgumentException when resolved indices are empty |
| [#5897](https://github.com/opensearch-project/security/pull/5897) | Fix test failure related to content-encoding response headers |
| [#5861](https://github.com/opensearch-project/security/pull/5861) | Fix NPE in LDAP recursive role search |
| [#1370](https://github.com/opensearch-project/security-dashboards-plugin/pull/1370) | Fix CVE-2025-64718 by bumping js-yaml version |
| [#1631](https://github.com/opensearch-project/security-dashboards-plugin/pull/1631) | Replace java.security.AccessController with OpenSearch replacement |

#### Dependency Updates
| PR | Description |
|----|-------------|
| [#5874](https://github.com/opensearch-project/security/pull/5874) | Bump lz4-java 1.10.1 → 1.10.2 |
| [#5919](https://github.com/opensearch-project/security/pull/5919) | Bump logback-classic 1.5.21 → 1.5.26 |
| [#5904](https://github.com/opensearch-project/security/pull/5904) | Bump nimbus-jose-jwt 10.6 → 10.7 |
| [#5922](https://github.com/opensearch-project/security/pull/5922) | Bump metrics-core 4.2.37 → 4.2.38 |
| [#5913](https://github.com/opensearch-project/security/pull/5913) | Bump byte-buddy 1.18.2 → 1.18.4 |
| [#5921](https://github.com/opensearch-project/security/pull/5921) | Bump cryptacular 1.2.7 → 1.3.0 |
| [#5892](https://github.com/opensearch-project/security/pull/5892) | Update Jackson to 2.20.1 |
| [#5911](https://github.com/opensearch-project/security/pull/5911) | Bump spring_version 7.0.2 → 7.0.3 |

## Limitations

- gRPC JWT authentication does not support superuser or anonymous authentication
- HTTP/3 client-side support not yet available
- DLS write blocking is a cluster-wide setting affecting all indices with DLS restrictions

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#5916](https://github.com/opensearch-project/security/pull/5916) | JWT authentication for gRPC transport | [#5812](https://github.com/opensearch-project/security/issues/5812) |
| [#5886](https://github.com/opensearch-project/security/pull/5886) | HTTP/3 server-side support | [#5884](https://github.com/opensearch-project/security/issues/5884) |
| [#5828](https://github.com/opensearch-project/security/pull/5828) | DLS write blocking setting | |
| [#5891](https://github.com/opensearch-project/security/pull/5891) | Nested JWT claims via dot notation | [#5687](https://github.com/opensearch-project/security/issues/5687) |
| [#5929](https://github.com/opensearch-project/security/pull/5929) | gRPC JWT header case insensitivity fix | |
| [#5858](https://github.com/opensearch-project/security/pull/5858) | Plugin system index access fix | [job-scheduler#865](https://github.com/opensearch-project/job-scheduler/issues/865) |
