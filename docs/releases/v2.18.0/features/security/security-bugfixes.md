# Security Bugfixes

## Summary

OpenSearch v2.18.0 includes multiple security-related bug fixes across the Security plugin, Security Analytics plugin, and Alerting plugin. These fixes address issues with system index access control, SAML authentication audit logging, demo configuration detection, SSL dual mode settings propagation, stored field handling, closed index mappings, and alerting role permissions.

## Details

### What's New in v2.18.0

This release addresses 9 bug fixes across security-related components:

| Bug Fix | Repository | Description |
|---------|------------|-------------|
| Admin system index read | security | Prevent admin users from reading security system indices registered through core |
| SAML failed login audit | security | Remove misleading failed login audit entries for SAML authenticator |
| Demo config detection | security | Handle non-flat YAML settings for demo configuration detection |
| SSL dual mode propagation | security | Ensure dual mode enabled flag from cluster settings propagates to core |
| HashingStoredFieldVisitor | security | Fix stored fields handling in HashingStoredFieldVisitor |
| Closed index mappings | security | Fix Get mappings request on closed indices |
| Alerting role permissions | alerting | Fix comments permission for alerting_ack_alerts role |
| OS launch exception | security-analytics | Remove redundant logic causing OpenSearch launch exception |
| Forecasting security tests | security-analytics | Forward port flaky test fix and add forecasting security tests |

### Technical Changes

#### System Index Access Control Fix (PR #4774)

Prevents unauthorized reads on security system indices registered through OpenSearch core. Previously, admin users could potentially read protected system index data.

**Impact**: Enhanced security for system indices by enforcing proper access controls.

#### SAML Authentication Audit Fix (PR #4762)

Removes audit log entries for failed login attempts during SAML authentication. SAML authentication always re-requests authentication, causing misleading "failed login" audit entries.

**Related Issue**: [#4608](https://github.com/opensearch-project/security/issues/4608)

#### Demo Configuration Detection Fix (PR #4793)

Fixes the demo configuration tool to correctly detect nested YAML settings for security configuration. Previously, the tool failed to recognize security settings in nested YAML format.

**Related Issue**: [#4735](https://github.com/opensearch-project/security/issues/4735)

**Technical Details**: Uses SnakeYaml library to properly parse and search for nested configuration cases.

#### SSL Dual Mode Settings Propagation (PR #4820)

Ensures the `plugins.security_config.ssl_dual_mode_enabled` cluster setting properly propagates to OpenSearch core. This fix enables dynamic changes to dual mode settings to take effect across the cluster.

**Companion PR**: [OpenSearch#16387](https://github.com/opensearch-project/OpenSearch/pull/16387)

**Configuration**:
```yaml
plugins.security_config.ssl_dual_mode_enabled: true
plugins.security.ssl_only: true
```

#### HashingStoredFieldVisitor Fix (PR #4826)

Fixes a bug in `HashingStoredFieldVisitor` to properly handle [stored_fields](https://opensearch.org/docs/latest/search-plugins/searching-data/retrieve-specific-fields/#searching-with-stored_fields) which are stored separately from `_source` in the backing index.

#### Closed Index Mappings Fix (PR #4685)

Fixes an issue filtering out fields on GET Mappings requests for closed indices. Updates the indices options used when getting concrete indices.

#### Security Analytics Fixes

- **PR #1303**: Removes redundant logic that caused OpenSearch launch exceptions and updates `actions/upload-artifact` to v3
- **Related Issue**: [#1273](https://github.com/opensearch-project/security-analytics/issues/1273)

## Limitations

- The SSL dual mode fix requires the companion OpenSearch core PR to be present
- Some fixes are backports from the main branch to the 2.x release branch

## References

### Documentation
- [OpenSearch stored_fields documentation](https://opensearch.org/docs/latest/search-plugins/searching-data/retrieve-specific-fields/#searching-with-stored_fields)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#4775](https://github.com/opensearch-project/security/pull/4775) | security | Fix bug where admin can read system index (backport) |
| [#4770](https://github.com/opensearch-project/security/pull/4770) | security | Remove failed login attempt for SAML authenticator (backport) |
| [#4798](https://github.com/opensearch-project/security/pull/4798) | security | Handle non-flat YAML settings for demo config detection (backport) |
| [#4830](https://github.com/opensearch-project/security/pull/4830) | security | Ensure dual mode enabled flag propagates to core (backport) |
| [#4827](https://github.com/opensearch-project/security/pull/4827) | security | Fix HashingStoredFieldVisitor with stored fields (backport) |
| [#4777](https://github.com/opensearch-project/security/pull/4777) | security | Fix Get mappings on closed index (backport) |
| [#1303](https://github.com/opensearch-project/security-analytics/pull/1303) | security-analytics | Remove redundant logic to fix OS launch exception |

### Issues (Design / RFC)
- [Issue #4608](https://github.com/opensearch-project/security/issues/4608): SAML failed login audit issue
- [Issue #4735](https://github.com/opensearch-project/security/issues/4735): Demo config nested YAML issue
- [Issue #4755](https://github.com/opensearch-project/security/issues/4755): Admin system index read issue
- [Issue #1273](https://github.com/opensearch-project/security-analytics/issues/1273): OS launch exception issue
