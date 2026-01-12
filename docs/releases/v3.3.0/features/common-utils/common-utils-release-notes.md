---
tags:
  - indexing
---

# Common Utils Release Notes

## Summary

This release item adds release notes documentation for common-utils version 2.13.0.0. The release notes document the changes, enhancements, and maintenance updates included in the 2.13.0.0 release of the common-utils library.

## Details

### What's New in v3.3.0

PR #869 backports the release notes for common-utils 2.13.0.0 from the 2.13 branch to the main branch. This ensures the release notes are available in the main branch for reference.

### Technical Changes

#### Release Notes Content

The release notes for version 2.13.0.0 document the following changes:

| Category | Description | PR |
|----------|-------------|-----|
| Maintenance | Increment version to 2.13.0-SNAPSHOT | [#591](https://github.com/opensearch-project/common-utils/pull/591) |
| Enhancement | Add queryFieldNames field in Doc Level Queries | [#582](https://github.com/opensearch-project/common-utils/pull/582), [#597](https://github.com/opensearch-project/common-utils/pull/597) |
| Feature | Fix findings API enhancements | [#611](https://github.com/opensearch-project/common-utils/pull/611), [#617](https://github.com/opensearch-project/common-utils/pull/617) |
| Feature | Feature findings enhancement | [#596](https://github.com/opensearch-project/common-utils/pull/596), [#606](https://github.com/opensearch-project/common-utils/pull/606) |
| Documentation | Added 2.13.0.0 release notes | [#622](https://github.com/opensearch-project/common-utils/pull/622) |

#### File Added

| File | Description |
|------|-------------|
| `release-notes/opensearch-common-utils.release-notes-2.13.0.0.md` | Release notes for version 2.13.0.0 |

### Usage Example

The release notes file follows the standard OpenSearch release notes format:

```markdown

## Limitations

- This is a documentation-only change with no functional impact
- The release notes document changes from the 2.13.0.0 release cycle

## References

### Documentation
- [Common Utils Repository](https://github.com/opensearch-project/common-utils)
- [Release Notes File](https://github.com/opensearch-project/common-utils/blob/main/release-notes/opensearch-common-utils.release-notes-2.13.0.0.md)

### Pull Requests
| PR | Description |
|----|-------------|
| [#869](https://github.com/opensearch-project/common-utils/pull/869) | Backport release notes for 2.13 to main branch |
| [#623](https://github.com/opensearch-project/common-utils/pull/623) | Original PR adding release notes for 2.13 |

## Related Feature Report

- [Full feature documentation](../../../../features/common-utils/common-utils.md)
