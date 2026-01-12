# Security Plugin Maintenance

## Summary

OpenSearch v2.18.0 includes maintenance updates for the Security plugin, including maintainer changes, API deprecation warnings, code refactoring for FIPS compatibility, security vulnerability fixes, and test improvements.

## Details

### What's New in v2.18.0

This release focuses on project maintenance, security fixes, and preparation for future changes:

1. **Maintainer Updates**: Project governance changes with maintainer transitions
2. **API Deprecation Warning**: Added deprecation warning for cache endpoint methods being removed in v3.0.0
3. **Securityadmin Script**: Removed deprecation warning as no replacement is planned
4. **FIPS Compatibility**: Refactored ASN1 calls to support multiple security providers
5. **CVE Fix**: Addressed CVE-2024-47554 by upgrading commons-io
6. **Test Improvements**: Fixed BWC tests and release workflow issues

### Technical Changes

#### API Deprecation

The following cache endpoint methods are deprecated and will be removed in v3.0.0:

| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/_plugins/_security/api/cache` | Deprecated |
| POST | `/_plugins/_security/api/cache` | Deprecated |
| PUT | `/_plugins/_security/api/cache` | Deprecated |

Users should migrate to alternative approaches before upgrading to v3.0.0.

#### Securityadmin Script

The `securityadmin.sh` script deprecation warning has been removed. The script remains the recommended tool for security configuration management with no planned replacement.

#### FIPS Compatibility

Refactored `DefaultSecurityKeyStore` to use ASN1 methods compatible with both standard Bouncy Castle and FIPS-compliant Bouncy Castle libraries:

```java
// Before: Direct getObject() call
ASN1Primitive obj = asn1TaggedObject.getObject();

// After: Compatible with BC 2.x FIPS
ASN1Primitive obj = ASN1TaggedObject.getInstance(asn1TaggedObject).getBaseObject();
```

#### Pagination Support

Added `isActionPaginated` method to `DelegatingRestHandler` to support paginated REST actions in the security plugin.

#### Security Vulnerability Fix

| CVE | Severity | Fix |
|-----|----------|-----|
| CVE-2024-47554 | Medium | Upgraded commons-io from 2.11.0 to 2.17.0 |

CVE-2024-47554 is a vulnerability in Apache Commons IO that could allow denial of service through malicious input.

### Test Improvements

#### BWC Test Fixes

Fixed `SecurityBackwardsCompatibilityIT.testDataIngestionAndSearchBackwardsCompatibility()`:

- Fixed bulk request serialization (was double-encoding JSON)
- Added assertions to verify bulk items are actually indexed
- Fixed DLS rules to match test documents
- Added assertions for DLS/FLS rule application

#### Release Workflow Fix

Fixed `integTest` not being called during release test workflows.

## Limitations

- Cache endpoint deprecation warnings will appear in logs when using deprecated methods
- FIPS compatibility requires Bouncy Castle 2.x FIPS libraries

## References

### Documentation
- [CVE-2024-47554](https://nvd.nist.gov/vuln/detail/CVE-2024-47554): Apache Commons IO vulnerability

### Pull Requests
| PR | Description |
|----|-------------|
| [#4667](https://github.com/opensearch-project/security/pull/4667) | Move @cliu123 to emeritus status |
| [#4796](https://github.com/opensearch-project/security/pull/4796) | Add Derek Ho as maintainer |
| [#4804](https://github.com/opensearch-project/security/pull/4804) | Move Stephen to emeritus |
| [#4776](https://github.com/opensearch-project/security/pull/4776) | Add deprecation warning for GET/POST/PUT cache |
| [#4768](https://github.com/opensearch-project/security/pull/4768) | Undeprecate securityadmin script |
| [#4765](https://github.com/opensearch-project/security/pull/4765) | Add isActionPaginated to DelegatingRestHandler |
| [#4740](https://github.com/opensearch-project/security/pull/4740) | Refactor ASN1 call for FIPS compatibility |
| [#4815](https://github.com/opensearch-project/security/pull/4815) | Fix integTest not called during release |
| [#4831](https://github.com/opensearch-project/security/pull/4831) | Fix bulk index requests in BWC tests |
| [#4792](https://github.com/opensearch-project/security/pull/4792) | Fix CVE-2024-47554 |

### Issues (Design / RFC)
- [Issue #4728](https://github.com/opensearch-project/security/issues/4728): ASN1 refactoring for FIPS support
- [Issue #4790](https://github.com/opensearch-project/security/issues/4790): CVE-2024-47554 tracking

## Related Feature Report

- [Full feature documentation](../../../../features/security/security-plugin.md)
