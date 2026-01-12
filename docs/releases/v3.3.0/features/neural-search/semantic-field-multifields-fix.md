# Semantic Field MultiFields Fix

## Summary

This bug fix resolves an issue where multiFields defined within a semantic field type were not being indexed. When users configured multiFields (such as a keyword subfield) on a semantic field with a text raw field type, the multiFields were silently ignored during indexing, causing searches against those subfields to fail.

## Details

### What's New in v3.3.0

Fixed the `SemanticFieldMapper` to properly delegate multiFields iteration to the underlying delegate field mapper, enabling multiFields to be indexed correctly.

### Technical Changes

#### Root Cause

The `SemanticFieldMapper` wraps a delegate field mapper (e.g., `TextFieldMapper`) but did not override the `iterator()` method. OpenSearch uses this iterator during indexing to discover and process multiFields. Without the override, the semantic field mapper returned an empty iterator, causing multiFields to be skipped.

#### Fix Implementation

Added an `iterator()` method override in `SemanticFieldMapper` that delegates to the underlying field mapper:

```java
@Override
public Iterator<Mapper> iterator() {
    return delegateFieldMapper.iterator();
}
```

This ensures that when OpenSearch iterates over the semantic field's child mappers during indexing, it correctly discovers and processes any configured multiFields.

### Usage Example

```json
// Create index with semantic field containing multiFields
PUT /my-semantic-index
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "products": {
        "type": "nested",
        "properties": {
          "product_description": {
            "type": "semantic",
            "model_id": "<model_id>",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          }
        }
      }
    }
  }
}

// Index document
PUT /my-semantic-index/_doc/1
{
  "products": [
    {
      "product_description": "High-quality wireless headphones"
    }
  ]
}

// Search against multiField (now works correctly)
GET /my-semantic-index/_search
{
  "query": {
    "nested": {
      "path": "products",
      "query": {
        "match": {
          "products.product_description": "headphones"
        }
      }
    }
  }
}
```

### Migration Notes

No migration required. After upgrading to v3.3.0, existing indices with semantic fields containing multiFields will work correctly for new documents. Existing documents may need to be reindexed to populate the multiFields.

## Limitations

- Existing documents indexed before this fix will not have multiFields populated; reindexing is required
- MultiFields are only supported when the raw field type supports them (e.g., `text`, `keyword`)

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#1572](https://github.com/opensearch-project/neural-search/pull/1572) | Fix not able to index the multiFields for the rawFieldType |

### Issues (Design / RFC)
- [Issue #1571](https://github.com/opensearch-project/neural-search/issues/1571): MultiFields doesn't work for semantic field type
- [Related Issue #3950](https://github.com/opensearch-project/ml-commons/issues/3950): Original user report

## Related Feature Report

- [Full feature documentation](../../../../features/neural-search/semantic-field.md)
