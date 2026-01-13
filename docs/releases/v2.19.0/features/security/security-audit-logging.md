---
tags:
  - security
---
# Security Audit Logging

## Summary

OpenSearch v2.19.0 includes three bug fixes related to security logging: improved compliance audit log behavior for the `log_request_body` setting, reduced log noise for OpenSSL availability warnings, and corrected log levels for On-Behalf-Of (OBO) authentication messages.

## Details

### What's New in v2.19.0

#### Compliance Audit Log `log_request_body` Setting Fix

The compliance audit logging now properly honors the `log_request_body` setting. Previously, when `write_log_diffs` was enabled, the request body was logged regardless of the `log_request_body` setting. This fix ensures:

- When `log_request_body` is disabled and `write_log_diffs` is enabled, only the diff content is logged without the full request body
- Document creation events now properly compute diffs from an empty source (`{}`) when no original document exists
- The `audit_request_body` field is correctly omitted when `log_request_body` is set to `false`

**Configuration Example**:
```yaml
plugins.security.audit.config.log_request_body: false
plugins.security.compliance.write_log_diffs: true
plugins.security.compliance.write_metadata_only: false
```

#### OpenSSL Availability Warning Reduction

The OpenSSL availability warning is now only logged when OpenSSL is explicitly enabled but not available. Previously, the warning was always logged when OpenSSL was unavailable, even when not explicitly configured. The warning now only appears when:

- `plugins.security.ssl.http.enable_openssl_if_available` is set to `true`, OR
- `plugins.security.ssl.transport.enable_openssl_if_available` is set to `true`

This reduces unnecessary log noise in environments using the default JDK SSL implementation.

#### OBO Authenticator Log Level Fix

The On-Behalf-Of (OBO) authenticator log message "On-behalf-of authentication is disabled" has been changed from `ERROR` to `DEBUG` level. This message is not indicative of an application error—it simply indicates that OBO authentication is not enabled, which is a normal configuration state.

### Technical Changes

| Component | Change | Impact |
|-----------|--------|--------|
| `AbstractAuditLog.java` | Modified `logDocumentWritten()` to respect `log_request_body` setting when `write_log_diffs` is enabled | Compliance audit logs now correctly omit request body when configured |
| `SslSettingsManager.java` | Added conditional check for OpenSSL settings before logging warning | Reduced log noise for default SSL configurations |
| `OnBehalfOfAuthenticator.java` | Changed log level from `ERROR` to `DEBUG` for disabled OBO message | Cleaner logs when OBO is intentionally disabled |

## Limitations

- The compliance audit log fix only affects write operations with `write_log_diffs` enabled
- OpenSSL warning suppression requires explicit configuration of the OpenSSL settings

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#4918](https://github.com/opensearch-project/security/pull/4918) | Honor log_request_body setting in compliance audit log (backport) | [#4534](https://github.com/opensearch-project/security/issues/4534) |
| [#4832](https://github.com/opensearch-project/security/pull/4832) | Honor log_request_body setting in compliance audit log (main) | [#4534](https://github.com/opensearch-project/security/issues/4534) |
| [#4906](https://github.com/opensearch-project/security/pull/4906) | Log OpenSSL warning only when explicitly enabled (backport) | [#4881](https://github.com/opensearch-project/security/issues/4881) |
| [#4901](https://github.com/opensearch-project/security/pull/4901) | Log OpenSSL warning only when explicitly enabled (main) | [#4881](https://github.com/opensearch-project/security/issues/4881) |
| [#4956](https://github.com/opensearch-project/security/pull/4956) | Change OBO disabled log level to DEBUG (backport) | |
| [#4952](https://github.com/opensearch-project/security/pull/4952) | Change OBO disabled log level to DEBUG (main) | |

### Documentation
- [Audit Logs Documentation](https://docs.opensearch.org/2.19/security/audit-logs/index/)
- [Audit Log Field Reference](https://docs.opensearch.org/2.19/security/audit-logs/field-reference/)
