---
tags:
  - search
  - security
  - sql
---

# SQL Plugin Maintenance

## Summary

This release includes maintenance updates for the SQL plugin, addressing a high-severity security vulnerability (CVE-2024-47554) in the commons-io library and fixing test failures on the 2.18 branch. These changes improve the security posture and stability of the SQL plugin without introducing functional changes.

## Details

### What's New in v2.18.0

#### Security Fix: CVE-2024-47554

The commons-io library was upgraded from version 2.8.0 to 2.14.0 to address CVE-2024-47554, a high-severity vulnerability (CVSS 7.5) that could cause uncontrolled resource consumption.

**Vulnerability Details:**
- The `org.apache.commons.io.input.XmlStreamReader` class could excessively consume CPU resources when processing maliciously crafted input
- Attack Vector: Network
- Attack Complexity: Low
- Privileges Required: None
- Impact: Availability (High)

**Affected Components:**
| Module | Previous Version | Updated Version |
|--------|-----------------|-----------------|
| async-query | 2.8.0 | 2.14.0 |
| datasources | 2.8.0 | 2.14.0 |
| spark | 2.8.0 | 2.14.0 |

#### Test Fixes

Fixed test failures on the 2.18 branch caused by rushed last-minute merging:
- Updated documentation test output formatting (table column widths)
- Fixed import issues in `MalformedCursorIT` due to missing Apache HTTP library in 2.18 branch
- Incorporated fixes from PR #3087

### Technical Changes

#### Dependency Updates

```gradle
// Before
implementation group: 'commons-io', name: 'commons-io', version: '2.8.0'

// After
implementation group: 'commons-io', name: 'commons-io', version: '2.14.0'
```

#### Test Documentation Updates

Multiple RST documentation files were updated to fix table formatting in test output examples. The changes normalize column widths in output tables across various SQL and PPL documentation files.

### Migration Notes

No migration steps required. This is a transparent dependency upgrade and test fix with no API or configuration changes.

## Limitations

None specific to this release.

## References

### Documentation
- [CVE-2024-47554](https://www.mend.io/vulnerability-database/CVE-2024-47554): Vulnerability details

### Blog Posts
- [Apache Commons IO Security Advisory](https://lists.apache.org/thread/6ozr91rr9cj5lm0zyhv30bsp317hk5z1): Official fix announcement

### Pull Requests
| PR | Description |
|----|-------------|
| [#3091](https://github.com/opensearch-project/sql/pull/3091) | Backport commons-io bump to 2.x branch |
| [#3113](https://github.com/opensearch-project/sql/pull/3113) | Fix tests on 2.18 branch |
| [#3083](https://github.com/opensearch-project/sql/pull/3083) | Original commons-io bump (main branch) |

### Issues (Design / RFC)
- [Issue #3055](https://github.com/opensearch-project/sql/issues/3055): CVE-2024-47554 security vulnerability report

## Related Feature Report

- [Full feature documentation](../../../../features/sql/sql-plugin-maintenance.md)
