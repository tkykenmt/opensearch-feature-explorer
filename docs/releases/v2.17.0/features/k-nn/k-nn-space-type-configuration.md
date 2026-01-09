# k-NN Space Type Configuration

## Summary

OpenSearch 2.17.0 introduces the ability to specify `space_type` as a top-level parameter when creating k-NN vector fields. Previously, `space_type` could only be defined within the `method` parameter block. This enhancement simplifies the mapping configuration, especially for disk-based vector search where users may not need to specify the full `method` definition.

## Details

### What's New in v2.17.0

This release adds `space_type` as a top-level optional parameter for `knn_vector` field mappings. Users can now configure the distance metric without defining the complete `method` block, improving the out-of-box experience for disk-based vector search.

### Technical Changes

#### New Mapping Parameter

| Parameter | Location | Description | Default |
|-----------|----------|-------------|---------|
| `space_type` | Top-level | Distance metric for vector similarity | `l2` |

The `space_type` parameter can now be specified at two locations:
1. **Top-level** (new): Directly in the field mapping
2. **Method-level** (existing): Inside the `method` parameter block

#### Supported Space Types

| Space Type | Description |
|------------|-------------|
| `l2` | Euclidean distance (default) |
| `cosinesimil` | Cosine similarity |
| `innerproduct` | Inner product (dot product) |
| `l1` | Manhattan distance |
| `linf` | Chebyshev distance |
| `hamming` | Hamming distance (for binary vectors) |

#### Validation Rules

- If `space_type` is specified at both top-level and method-level, they must match
- If only one is specified, that value is used
- If neither is specified, defaults to `l2` (or `hamming` for binary vectors)
- Top-level `space_type` cannot be used with `model_id` (model-based indices)

### Usage Example

**Before v2.17.0** (method-level only):
```json
PUT my-vector-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 4,
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "space_type": "innerproduct"
        }
      }
    }
  }
}
```

**With v2.17.0** (top-level):
```json
PUT my-vector-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 4,
        "space_type": "innerproduct"
      }
    }
  }
}
```

**With mode and compression (disk-based search)**:
```json
PUT my-vector-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 4,
        "mode": "on_disk",
        "compression_level": "32x",
        "space_type": "innerproduct"
      }
    }
  }
}
```

### Migration Notes

- No migration required; this is a backward-compatible addition
- Existing indices with method-level `space_type` continue to work unchanged
- New indices can use either top-level or method-level specification

## Limitations

- Cannot use top-level `space_type` with model-based indices (`model_id` parameter)
- If both top-level and method-level `space_type` are specified, they must be identical

## Related PRs

| PR | Description |
|----|-------------|
| [#2044](https://github.com/opensearch-project/k-NN/pull/2044) | Add spaceType as a top level parameter while creating vector field |

## References

- [Issue #1949](https://github.com/opensearch-project/k-NN/issues/1949): RFC - Disk-based Mode Design
- [k-NN Vector Documentation](https://docs.opensearch.org/2.17/field-types/supported-field-types/knn-vector/): Official field type documentation
- [k-NN Index Documentation](https://docs.opensearch.org/2.17/search-plugins/knn/knn-index/): Index configuration guide

## Related Feature Report

- [Full feature documentation](../../../features/k-nn/k-nn-space-type-configuration.md)
