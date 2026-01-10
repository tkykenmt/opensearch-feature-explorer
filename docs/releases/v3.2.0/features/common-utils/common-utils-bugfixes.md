# Common Utils Bugfixes

## Summary

This release includes critical bugfixes for the common-utils library, addressing a security vulnerability (CVE-2025-48734), reverting a breaking API change in the alerting module, and upgrading build infrastructure to Gradle 8.14 and JDK 24.

## Details

### What's New in v3.2.0

Three bugfixes were merged to improve security, API stability, and build compatibility:

1. **CVE-2025-48734 Fix**: Pinned commons-beanutils dependency to version 1.11.0
2. **PublishFindingsRequest Revert**: Restored original list-based API for findings
3. **Build Infrastructure Update**: Upgraded to Gradle 8.14 and JDK 24

### Technical Changes

#### Security Fix: CVE-2025-48734

The `commons-beanutils` dependency was pinned to version 1.11.0 to address a security vulnerability.

```groovy
configurations {
    all {
        resolutionStrategy {
            force "commons-beanutils:commons-beanutils:1.11.0"
        }
    }
}
```

#### API Revert: PublishFindingsRequest

The batch findings API introduced in PR #832 was reverted due to compatibility issues. The following components were removed:

| Component | Type | Description |
|-----------|------|-------------|
| `PublishBatchFindingsRequest` | Class | Request class for batch findings |
| `SUBSCRIBE_BATCH_FINDINGS_ACTION_NAME` | Constant | Action name for batch subscribe |
| `SUBSCRIBE_BATCH_FINDINGS_ACTION_TYPE` | ActionType | Action type for batch findings |
| `publishBatchFindings()` | Method | Interface method in AlertingPluginInterface |

The original `PublishFindingsRequest` with a list of findings remains the supported API.

#### Build Infrastructure: Gradle 8.14 + JDK 24

| Component | Previous | New |
|-----------|----------|-----|
| Gradle | 8.10.2 | 8.14 |
| JDK (CI) | 21, 23 | 21, 24 |
| github-app-token action | v1.5.0 | v2.1.0 |
| Backport workflow | Legacy config | Updated with security checks |

The backport workflow was also improved with:
- Security check: Only reacts to merged PRs
- Updated head template: `backport/backport-<number>-to-<base>`
- Simplified failure label: `backport-failed`

### Migration Notes

- **For plugin developers**: If you were using `PublishBatchFindingsRequest`, switch to `PublishFindingsRequest` with a list of findings
- **For build systems**: Update to JDK 24 for compatibility with the latest common-utils

## Limitations

- The batch findings API is no longer available; use the list-based API instead

## Related PRs

| PR | Description |
|----|-------------|
| [#850](https://github.com/opensearch-project/common-utils/pull/850) | Pinned commons-beanutils dependency to fix CVE-2025-48734 |
| [#847](https://github.com/opensearch-project/common-utils/pull/847) | Revert PublishFindingsRequest to use a list of findings |
| [#848](https://github.com/opensearch-project/common-utils/pull/848) | Switch gradle to 8.14 and JDK to 24 |

## References

- [CVE-2025-48734 Advisory](https://advisories.opensearch.org/advisories/CVE-2025-48734): Security advisory for commons-beanutils
- [OpenSearch PR #18085](https://github.com/opensearch-project/OpenSearch/pull/18085): Related JDK 24 update in OpenSearch core
- [OpenSearch Issue #17661](https://github.com/opensearch-project/OpenSearch/issues/17661): JDK 24 upgrade tracking issue

## Related Feature Report

- [Full feature documentation](../../../features/common-utils/common-utils.md)
