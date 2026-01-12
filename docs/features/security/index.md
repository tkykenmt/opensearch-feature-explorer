---
tags:
  - security
---

# Security Plugin

Authentication, authorization, and access control for OpenSearch.

## Overview

- [Overview](overview.md) - Core security functionality
- [Features](features.md) - Feature overview

## Authentication

| Document | Description |
|----------|-------------|
| [JWT Authentication](jwt-authentication.md) | JSON Web Token auth |
| [Client Certificate](client-certificate-authentication.md) | X.509 certificate auth |
| [SPIFFE X.509 SVID](spiffe-x.509-svid-support.md) | SPIFFE identity |
| [Auth Enhancements](auth-enhancements.md) | Authentication improvements |
| [Argon2 Password Hashing](argon2-password-hashing.md) | Secure password storage |

## Authorization

| Document | Description |
|----------|-------------|
| [Permissions](permissions.md) | Permission management |
| [Permission Validation](permission-validation.md) | Permission checks |
| [Role Mapping](role-mapping.md) | Role assignments |
| [Resource Access Control](resource-access-control-framework.md) | Fine-grained access |
| [Multi-tenancy](multi-tenancy.md) | Tenant isolation |

## TLS/SSL

| Document | Description |
|----------|-------------|
| [SSL/TLS Compatibility](ssl-tls-compatibility.md) | TLS configuration |
| [Auxiliary Transport SSL](auxiliary-transport-ssl.md) | Transport layer security |

## Configuration

| Document | Description |
|----------|-------------|
| [Configuration](configuration.md) | Security settings |
| [Configuration Versioning](configuration-versioning.md) | Config version management |
| [FIPS Compliance](fips-compliance.md) | FIPS 140-2 support |

## Integration

| Document | Description |
|----------|-------------|
| [Alerting Comments](alerting-comments-security.md) | Alerting integration |
| [Correlation Alerts](correlation-alerts.md) | Security analytics |

## Performance & Maintenance

| Document | Description |
|----------|-------------|
| [Cache Management](cache-management.md) | Security cache |
| [Performance](performance.md) | Performance tuning |
| [Health Check](health-check.md) | Plugin health |
| [AccessController Migration](accesscontroller-migration.md) | Java security migration |
| [Testing Framework](testing-framework.md) | Security tests |
| [CI/CD](ci-cd.md) | Build infrastructure |
| [Dependencies](dependencies.md) | Dependency updates |
| [GitHub Actions](github-actions-updates.md) | CI updates |
| [Protobufs Sync](protobufs-version-sync.md) | Protocol buffers |
