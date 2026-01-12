# Documentation Link Updates

## Summary

This release item fixes broken documentation links in the dashboards-search-relevance plugin. The changes update the LICENSE file reference and remove unused Docker-related links to ensure the link checker passes.

## Details

### What's New in v2.17.0

Minor documentation maintenance to fix broken links in the repository's contributing documentation.

### Technical Changes

#### Files Modified

| File | Change |
|------|--------|
| `CONTRIBUTING.md` | Updated LICENSE file link from `LICENSE.txt` to `LICENSE` |
| `DEVELOPER_GUIDE.md` | Removed unused Docker section with broken links |

#### CONTRIBUTING.md Change

The LICENSE file reference was corrected:
- Before: `[LICENSE.txt file](./LICENSE.txt)`
- After: `[LICENSE file](./LICENSE)`

#### DEVELOPER_GUIDE.md Change

Removed the "Run Docker" section that contained broken links to non-existent files:
- Removed reference to `Dockerfile`
- Removed reference to `Using-Docker.md` tutorial

### Usage Example

No usage changes - this is a documentation-only fix.

### Migration Notes

No migration required. This is a documentation fix only.

## Limitations

None - this is a documentation maintenance change.

## References

### Documentation
- [PR #420](https://github.com/opensearch-project/dashboards-search-relevance/pull/420): Main implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#420](https://github.com/opensearch-project/dashboards-search-relevance/pull/420) | Update Links in Documentation |

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-search-relevance/documentation-maintenance.md)
