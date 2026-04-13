---
tags:
  - opensearch
---
# Upgrade Compatibility

## Summary

OpenSearch version handling and upgrade path compatibility, including error messaging when encountering indices created on legacy Elasticsearch versions. OpenSearch uses a bitmask in internal version IDs to distinguish its versions from Elasticsearch versions, and indices created on Elasticsearch cannot be directly opened on OpenSearch 3.x.

## Details

### Version ID System

OpenSearch encodes versions as integer IDs using the formula: `major * 10000 + minor * 100 + revision`, with an additional bitmask (`MASK`) applied to distinguish OpenSearch versions from Elasticsearch versions. When `Version.fromId()` encounters an ID without this mask, it identifies it as a legacy Elasticsearch version.

### Error Handling

The `Version.UnsupportedVersionException` provides clear diagnostics when legacy version IDs are encountered:

```
index with UUID [<uuid>] created on version [ES 7.9.1] is not supported by version [3.6.0]
```

Key components:
| Component | Description |
|-----------|-------------|
| `Version.UnsupportedVersionException` | Exception with human-readable version string for unsupported version IDs |
| `Version.legacyFriendlyIdToString()` | Decodes version IDs, prefixing `"ES "` for Elasticsearch versions |
| `IndexMetadata.indexCreated()` | Catches unsupported versions and adds index UUID context |

## Limitations

- OpenSearch 3.x cannot open indices created on Elasticsearch. Users must reindex through a compatible OpenSearch 2.x version.
- The version decoding only handles the standard version ID encoding scheme.

## Change History
- **v3.6.0**: Replaced cryptic `"Version id must contain OpenSearch mask"` error with human-readable message showing the Elasticsearch version and index UUID

## References

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v3.6.0 | [opensearch-project/OpenSearch#20512](https://github.com/opensearch-project/OpenSearch/pull/20512) | Improve exception messaging when encountering legacy version IDs |

### Related Issues
- [opensearch-project/OpenSearch#20499](https://github.com/opensearch-project/OpenSearch/issues/20499) — Bootstrap error not clear when starting OpenSearch 3.x with an unsupported index version
