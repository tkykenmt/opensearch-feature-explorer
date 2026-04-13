---
tags:
  - security
---
# Security Enhancements

## Summary

OpenSearch v3.6.0 delivers a broad set of security plugin improvements spanning new features, performance optimizations, resource sharing enhancements, FIPS build support, and numerous bug fixes. Key highlights include gRPC basic authentication support, optimized index pattern matching with ~50% latency reduction for role configuration updates, parent-child resource authorization in the resource sharing framework, and fixes for audit logging, security context propagation, and DLS error reporting.

## Details

### New Features

#### gRPC Basic Authentication (PR #6005)
Previously, only JWT authentication was supported for gRPC auxiliary transport requests. This required complex configuration overhead, especially for integration testing against secure clusters. v3.6.0 adds HTTP Basic Authentication support for gRPC transport, allowing both JWT and Basic Auth methods.

### Enhancements

#### Optimized Index Pattern Matching (PR #5988)
Introduces two key optimizations for `RoleBasedActionPrivileges`:
- All compilation of index patterns, static DLS queries, etc. is decoupled into a new `CompiledRoles` class, guaranteeing each pattern is compiled only once even when used across different components
- The `IndexPattern` class provides optimized matching for prefix patterns (e.g., `index_*`) and exact patterns (e.g., `index_a`), leveraging the cluster state's `TreeSet` for O(log n) prefix matching instead of O(n)

Benchmark results show ~56% improvement:
- Before: 2317ms total (3000 roles, 6000 indices, 9000 aliases)
- After: 1013ms total

#### Optimized FLS Field Filter (PR #5777)
Optimizes `getFieldFilter` to only return a predicate when an index actually has Field-Level Security (FLS) restrictions for the current user. Previously, `dlsFlsValve.isFieldAllowed()` was called for all indices regardless of restrictions, adding unnecessary overhead to `GET _mapping` calls.

#### Parent-Child Resource Authorization (PR #5735)
Extends `ResourceProvider` to support `parentType` and `parentIdField`, enabling plugins to declare parent-child relationships for authorization. For example, read access to a Report Definition can automatically grant read access to its associated Report Instances through access levels defined in `resource-access-levels.yml`.

#### Default Access Level in resource-access-levels.yml (PR #6018)
Plugin authors can now mark a default access level per resource type by adding `default: true` in `resource-access-levels.yml`. The `default_access_level` field in the migration API request becomes optional — when omitted, the registered default is used. If explicitly supplied, the request value takes precedence.

#### Custom Action Prefixes for Resource Plugins (PR #6020)
The sample resource plugin now uses custom action prefixes (`sampleresource:` and `sampleresourcegroup:`) instead of the generic `cluster:admin/` prefix, improving readability and providing a pattern for plugin authors.

#### Hardened Input Validation for Resource Sharing APIs (PR #5831)
Introduces input length limits on string parameters in resource-sharing REST APIs. Previously, users could submit practically infinite-length strings in input parameters.

#### Optional encryption_key for OBO Token Authenticator (PR #6017)
The `encryption_key` for on-behalf-of (OBO) token configuration is now optional. Previously both `signing_key` and `encryption_key` were required. The `encryption_key` was used to encrypt roles/backend_roles claims for confidentiality from extensions. Now cluster administrators can choose whether to hash these claims or leave them plain.

#### FIPS Build Parameter Awareness (PR #5952)
The security plugin now recognizes the `-Pcrypto.standard=FIPS-140-3` build parameter. When present, BouncyCastle FIPS jars are provided by core and available at runtime (marked `compileOnly`). When absent, the security plugin includes them in its assembly (`implementation`). This prevents jar hell errors when installing the security plugin on a FIPS-enabled core build.

### Bug Fixes

#### Security Context Propagation Fix (PR #6006)
Fixes a propagation issue for security context, resolving problems reported in Issue #5990.

#### Audit Log Rollover Fix (PR #5900)
Fixes audit log writing errors when using an alias with a rollover policy. Previously, when an audit log index already existed under an alias, OpenSearch threw an error and failed to insert audit events. Now the audit log detects existing indices and inserts events correctly.

#### X-Request-Id Header Fix (PR #5954)
Fixes the unprocessed `X-Request-Id` header in the security plugin, resolving Issues #5951 and OpenSearch #20601.

#### Audit Log NONE Sentinel Fix (PR #6021)
Fixes the `NONE` sentinel value not being respected in dynamic configuration for `disabled_rest_categories` and `disabled_transport_categories`. `AuditCategory.parse()` now treats a single "NONE" value (case-insensitive) as an empty set consistently across both static and dynamic configuration paths. Also fixes the `ignore_users` handling via the REST/dynamic path.

#### DLS User Attribute Error Messages (PR #5975)
Improves error messages when DLS queries reference undefined user attributes. Previously the error showed the raw query string; now it identifies which attributes are missing and lists available attributes.

#### CVE Fixes (PRs #1411, #1410, #1412)
Fixes for CVE-2025-13465, CVE-2025-15284, and CVE-2026-2739 security vulnerabilities.

#### Resource Access Levels YAML Rename (PR #1163)
Renamed `resource-action-groups.yml` to `resource-access-levels.yml` to fix security checks.

#### Other Fixes
- Stop fetching security snapshot artifacts in non-snapshot builds (PR #560)
- Use html2canvas-pro with CSP nonce to fix content security policy violation (PR #313)
- Replace `java.security.AccessController` with `org.opensearch.secure_sm.AccessController` (PR #1974 — note: this PR number in the issue body appears to reference a different PR; the actual AccessController migration work was tracked separately)

## Limitations

- gRPC Basic Authentication shares the same credential store as HTTP Basic Auth
- The `encryption_key` being optional means OBO token claims may be visible in plain text if not configured
- FIPS build parameter awareness requires both core and security plugin to be built with matching FIPS settings

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6005](https://github.com/opensearch-project/security/pull/6005) | Enable Basic Authentication for gRPC transport |  |
| [#5735](https://github.com/opensearch-project/security/pull/5735) | Parent-child resource authorization in ResourceProvider | [#4500](https://github.com/opensearch-project/security/issues/4500) |
| [#5777](https://github.com/opensearch-project/security/pull/5777) | Optimize getFieldFilter for FLS restrictions |  |
| [#5988](https://github.com/opensearch-project/security/pull/5988) | Optimized string matching for RoleBasedActionPrivileges | [#5998](https://github.com/opensearch-project/security/issues/5998) |
| [#5831](https://github.com/opensearch-project/security/pull/5831) | Harden input validation for resource sharing APIs |  |
| [#6017](https://github.com/opensearch-project/security/pull/6017) | Make encryption_key optional for OBO token authenticator |  |
| [#6018](https://github.com/opensearch-project/security/pull/6018) | Default access level in resource-access-levels.yml |  |
| [#6020](https://github.com/opensearch-project/security/pull/6020) | Custom action prefixes for sample resource plugin | [#4500](https://github.com/opensearch-project/security/issues/4500) |
| [#5952](https://github.com/opensearch-project/security/pull/5952) | FIPS build parameter awareness | [opensearch-build#5979](https://github.com/opensearch-project/opensearch-build/issues/5979) |
| [#6006](https://github.com/opensearch-project/security/pull/6006) | Fix security context propagation | [#5990](https://github.com/opensearch-project/security/issues/5990) |
| [#5900](https://github.com/opensearch-project/security/pull/5900) | Fix audit log rollover-enabled alias indices | [#5878](https://github.com/opensearch-project/security/issues/5878) |
| [#5954](https://github.com/opensearch-project/security/pull/5954) | Fix unprocessed X-Request-Id header | [#5951](https://github.com/opensearch-project/security/issues/5951) |
| [#6021](https://github.com/opensearch-project/security/pull/6021) | Fix audit log NONE sentinel and unknown setting error | [#2673](https://github.com/opensearch-project/security/issues/2673) |
| [#5975](https://github.com/opensearch-project/security/pull/5975) | Improve DLS undefined user attribute error messages | [#1310](https://github.com/opensearch-project/security/issues/1310) |
| [#1411](https://github.com/opensearch-project/security/pull/1411) | Fix CVE-2025-13465 |  |
| [#1410](https://github.com/opensearch-project/security/pull/1410) | Fix CVE-2025-15284 |  |
| [#1412](https://github.com/opensearch-project/security/pull/1412) | Fix CVE-2026-2739 |  |
| [#1163](https://github.com/opensearch-project/security/pull/1163) | Rename resource-action-groups.yml to resource-access-levels.yml |  |
| [#560](https://github.com/opensearch-project/security/pull/560) | Stop fetching snapshot artifacts in non-snapshot builds |  |
| [#313](https://github.com/opensearch-project/security/pull/313) | Fix CSP violation with html2canvas-pro |  |
| [#4737](https://github.com/opensearch-project/security/pull/4737) | Rename resource-action-groups.yml to resource-access-levels.yml |  |
