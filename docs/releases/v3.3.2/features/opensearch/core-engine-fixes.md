---
tags:
  - opensearch
---
# Core Engine Fixes

## Summary

Two core engine bug fixes: a build system fix for patch version bumps and an IndexOutOfBoundsException fix in terms aggregations.

## Details

### What's New in v3.3.2

- **Patch Version Build Fix** (OpenSearch#19377): Fixed an issue where bumping the core version to a patch number other than 0 (e.g., 3.3.1, 3.3.2) caused `./gradlew localDistro` to fail with `Expected exactly 2 majors in parsed versions but found: [2, 3, 6, 7]`. The fix removes legacy Elasticsearch version number references from `BwcVersions` parsing, as they are more than two major versions behind.

- **Terms Aggregation Fix** (OpenSearch#19637): Fixed an `IndexOutOfBoundsException` when running `include`/`exclude` filters on a non-existent prefix in terms aggregations.

## References

| PR | Description |
|----|-------------|
| [#19377](https://github.com/opensearch-project/OpenSearch/pull/19377) | Fix issue with updating core with a patch number other than 0 |
| [#19637](https://github.com/opensearch-project/OpenSearch/pull/19637) | Fix IndexOutOfBoundsException in terms aggregations |
| [opensearch-build#5720](https://github.com/opensearch-project/opensearch-build/issues/5720) | Related build issue |
