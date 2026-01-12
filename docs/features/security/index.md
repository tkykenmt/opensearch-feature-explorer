---
tags:
  - security
---

# Security Plugin

Authentication, authorization, and access control for OpenSearch.

## Overview

- [Security Plugin](security-plugin.md) - Core security functionality
- [Security Features](security-features.md) - Feature overview

## Authentication

| Document | Description |
|----------|-------------|
| [JWT Authentication](security-jwt-authentication.md) | JSON Web Token auth |
| [Client Certificate](security-client-certificate-authentication.md) | X.509 certificate auth |
| [SPIFFE X.509 SVID](security-spiffe-x.509-svid-support.md) | SPIFFE identity |
| [Auth Enhancements](security-auth-enhancements.md) | Authentication improvements |
| [Argon2 Password Hashing](security-argon2-password-hashing.md) | Secure password storage |

## Authorization

| Document | Description |
|----------|-------------|
| [Permissions](security-permissions.md) | Permission management |
| [Permission Validation](security-permission-validation.md) | Permission checks |
| [Role Mapping](security-role-mapping.md) | Role assignments |
| [Resource Access Control](security-resource-access-control-framework.md) | Fine-grained access |
| [Multi-tenancy](security-multi-tenancy.md) | Tenant isolation |

## TLS/SSL

| Document | Description |
|----------|-------------|
| [SSL/TLS Compatibility](security-ssl-tls-compatibility.md) | TLS configuration |
| [Auxiliary Transport SSL](security-auxiliary-transport-ssl.md) | Transport layer security |

## Configuration

| Document | Description |
|----------|-------------|
| [Configuration](security-configuration.md) | Security settings |
| [Configuration Versioning](security-configuration-versioning.md) | Config version management |
| [FIPS Compliance](security-opensearch-fips-compliance.md) | FIPS 140-2 support |

## Integration

| Document | Description |
|----------|-------------|
| [Alerting Comments](security-alerting-comments-security.md) | Alerting integration |
| [Correlation Alerts](security-correlation-alerts.md) | Security analytics |

## Performance & Maintenance

| Document | Description |
|----------|-------------|
| [Cache Management](security-cache-management.md) | Security cache |
| [Performance](security-performance-improvements.md) | Performance tuning |
| [Health Check](security-plugin-health-check.md) | Plugin health |
| [AccessController Migration](security-accesscontroller-migration.md) | Java security migration |
| [Testing Framework](security-testing-framework.md) | Security tests |
| [CI/CD](security-ci-cd.md) | Build infrastructure |
| [Dependencies](security-opensearch-plugin-dependencies.md) | Dependency updates |
| [GitHub Actions](security-github-actions-updates.md) | CI updates |
| [Protobufs Sync](security-protobufs-version-sync.md) | Protocol buffers |
