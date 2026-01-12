# Dependency Updates (Dashboards)

## Summary

This release includes critical dependency updates for OpenSearch Dashboards that address security vulnerabilities and improve UTF-8 handling in JSON operations. The updates fix a significant bug where Discover became unusable due to JSON parsing errors with certain character encodings.

## Details

### What's New in v2.18.0

Two key dependency updates were made to improve security and stability:

1. **JSON11 Upgrade (1.1.2 → 2.0.0)**: Fixes UTF-8 safety issues when stringifying JSON data, resolving the "Bad escaped character in JSON" error that made Discover unusable after upgrading from v2.13 to v2.15.

2. **Chokidar Bump (3.5.3 → 3.6.0)**: Updates the file watching library used during development.

### Technical Changes

#### Bug Fix: JSON Parsing Error

The JSON11 upgrade resolves [Issue #7367](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7367) where users experienced:

```
SyntaxError: Bad escaped character in JSON at position 911476 (line 1 column 911477)
    at fetch_Fetch.fetchResponse
```

This error occurred in Discover when processing documents containing certain UTF-8 characters that were not properly escaped during JSON stringification.

#### Changed Files

| File | Change |
|------|--------|
| `package.json` | Updated `**/json11` from `^1.1.2` to `^2.0.0` |
| `packages/osd-std/package.json` | Updated `json11` dependency to `^2.0.0` |
| `yarn.lock` | Updated lockfile with new dependency versions |

### Migration Notes

No migration steps required. The dependency updates are backward compatible.

## Limitations

- These are development/build-time dependency updates
- The JSON11 fix specifically addresses UTF-8 encoding issues in JSON stringification

## References

### Documentation
- [OpenSearch Forum Discussion](https://forum.opensearch.org/t/json-parse-bad-escaped-character/20211): Community report of the issue

### Pull Requests
| PR | Description |
|----|-------------|
| [#8603](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8603) | Upgrade JSON11 from 1.1.2 to 2.0.0 to ensure UTF-8 safety |
| [#8490](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8490) | Bump chokidar from 3.5.3 to 3.6.0 |

### Issues (Design / RFC)
- [Issue #7367](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7367): JSON.parse: bad escaped character bug report

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/dependency-updates.md)
