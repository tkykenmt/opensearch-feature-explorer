---
tags:
  - search
  - security
---

# Security Integration Test Control

## Summary

This release item adds a system property to control whether integration tests run with the security plugin enabled in the search-relevance repository. This allows developers to selectively enable or disable security plugin integration during testing, improving CI/CD flexibility and test execution control.

## Details

### What's New in v3.4.0

The search-relevance plugin now supports a `-Dsecurity=true` system property that controls whether integration tests are executed with the OpenSearch security plugin. Previously, security-related test resources were always downloaded and processed; now this behavior is conditional.

### Technical Changes

#### Build Configuration Changes

The `build.gradle` file was modified to conditionally download security certificates and test resources:

| Change | Description |
|--------|-------------|
| System property check | Added `runIntegTestWithSecurityPlugin = System.getProperty("security")` |
| Conditional resource download | Security certificates (esnode.pem, kirk.pem, etc.) only downloaded when `security=true` |
| Test resource processing | `processTestResources` only includes security files when enabled |

#### CI Workflow Updates

| File | Change |
|------|--------|
| `.github/workflows/test_security.yml` | Added `-Dsecurity=true` flag to gradle command |
| `scripts/integtest.sh` | Added `-Dsecurity=$SECURITY_ENABLED` to integTestRemote command |

### Usage Example

```bash
# Run integration tests WITH security plugin
./gradlew integTest -Dhttps=true -Dsecurity=true

# Run integration tests WITHOUT security plugin (default)
./gradlew integTest -Dhttps=true
```

### Migration Notes

No migration required. Existing CI workflows that need security testing should add the `-Dsecurity=true` flag to their gradle commands.

## Limitations

- The system property must be explicitly set to `"true"` (string comparison) to enable security testing
- Security certificates are downloaded from the security repository's main branch at build time

## References

### Documentation
- [PR #287](https://github.com/opensearch-project/search-relevance/pull/287): Main implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#287](https://github.com/opensearch-project/search-relevance/pull/287) | Use a system property to control run integ test with security plugin |

## Related Feature Report

- [Full feature documentation](../../../features/search-relevance/search-relevance-security-integ-test-control.md)
