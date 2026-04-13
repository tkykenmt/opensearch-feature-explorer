---
tags:
  - opensearch
---
# Upgrade Compatibility

## Summary

Improved error messaging when OpenSearch encounters indices originally created on Elasticsearch. Previously, attempting to open such indices produced a cryptic error (`"Version id 7090199 must contain OpenSearch mask"`). Now, the error clearly identifies the unsupported Elasticsearch version and the index UUID, making it much easier for users to diagnose upgrade issues.

## Details

### What's New in v3.6.0

A new `Version.UnsupportedVersionException` replaces the generic `IllegalArgumentException` thrown when `Version.fromId()` encounters a version ID without the OpenSearch bitmask. The exception includes a human-readable version string that decodes the legacy Elasticsearch version (e.g., `"ES 7.9.1"` from version ID `7090199`).

The `IndexMetadata.indexCreated()` method now catches this exception and wraps it with additional context including the index UUID and the current OpenSearch version:

```
index with UUID [<uuid>] created on version [ES 7.9.1] is not supported by version [3.6.0]
```

### Technical Changes

| Component | Change |
|-----------|--------|
| `Version.UnsupportedVersionException` | New inner exception class with `getVersionString()` accessor |
| `Version.legacyFriendlyIdToString()` | New private method that decodes version IDs, prefixing `"ES "` for IDs without the OpenSearch mask |
| `Version.fromId()` | Throws `UnsupportedVersionException` instead of `IllegalArgumentException` for legacy IDs |
| `IndexMetadata.indexCreated()` | Catches `UnsupportedVersionException` and re-throws with index UUID and current version context |
| `Version.stringHasLength()` | Removed; replaced by `Strings.hasLength()` from core library |
| `SemverRange.fromString()` | Updated to use `Strings.hasLength()` |

### Background

Users migrating from Elasticsearch to OpenSearch sometimes have indices created on older Elasticsearch versions (e.g., ES 7.x). OpenSearch uses a bitmask in version IDs to distinguish its versions from Elasticsearch versions. When OpenSearch 3.x encounters an index with an Elasticsearch version ID, the previous error message referenced an internal "OpenSearch mask" concept that was meaningless to users.

## Limitations

- This change only improves the error message — it does not add support for opening Elasticsearch-created indices on OpenSearch 3.x. Users must still reindex from a compatible OpenSearch 2.x version first.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [opensearch-project/OpenSearch#20512](https://github.com/opensearch-project/OpenSearch/pull/20512) | Improve exception messaging when encountering legacy version IDs | [opensearch-project/OpenSearch#20499](https://github.com/opensearch-project/OpenSearch/issues/20499) |
