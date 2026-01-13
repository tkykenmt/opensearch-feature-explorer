---
tags:
  - opensearch
---
# Script Enhancements

## Summary

OpenSearch 2.19.0 extends the availability of `sha1()` and `sha256()` string hashing methods in Painless scripts to the update context. Previously, these methods were only available in ingest pipelines; now they can be used in update, reindex, and update_by_query operations.

## Details

### What's New in v2.19.0

The `sha1()` and `sha256()` augmentation methods for `java.lang.String` are now available in the update script context. This enables hashing string values during document updates without requiring a separate ingest pipeline.

### Supported Operations

| Operation | sha1()/sha256() Support |
|-----------|------------------------|
| Ingest pipeline | Yes (existing) |
| Update document | Yes (new in v2.19.0) |
| Reindex | Yes (new in v2.19.0) |
| Update by query | Yes (new in v2.19.0) |

### Usage Examples

**Update document with hashed field:**
```json
POST /test_index/_update/1
{
  "script": {
    "lang": "painless",
    "source": "ctx._source.url_hash = ctx._source.url.sha256()"
  }
}
```

**Reindex with hashed document ID:**
```json
POST /_reindex
{
  "source": {
    "index": "source_index"
  },
  "dest": {
    "index": "dest_index"
  },
  "script": {
    "lang": "painless",
    "source": "ctx._id = ctx._source.url.sha256()"
  }
}
```

**Update by query with hashing:**
```json
POST /my_index/_update_by_query
{
  "script": {
    "lang": "painless",
    "source": "ctx._source.user_sha1 = ctx._source.user.sha1(); ctx._source.user_sha256 = ctx._source.user.sha256()"
  }
}
```

### Technical Implementation

The change adds a new allowlist file `org.opensearch.update.txt` that registers the `sha1()` and `sha256()` augmentation methods from `org.opensearch.painless.api.Augmentation` for the `UpdateScript.CONTEXT`. This follows the same pattern used for ingest scripts.

## Limitations

- The hashing methods are only available for `java.lang.String` types
- Other script contexts (e.g., search scripts, aggregation scripts) do not have access to these methods

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16923](https://github.com/opensearch-project/OpenSearch/pull/16923) | Update script supports java.lang.String.sha1() and java.lang.String.sha256() methods | [#16423](https://github.com/opensearch-project/OpenSearch/issues/16423) |

### Related Issues
- [#16423](https://github.com/opensearch-project/OpenSearch/issues/16423) - BUG: dynamic method [java.lang.String, sha256/0] not available in _reindex Painless script
