---
tags:
  - indexing
---

# Normalizer Enhancements

## Summary

OpenSearch v3.4.0 adds support for using the `truncate` token filter within normalizers. This enhancement allows users to truncate keyword field values to a specified length during normalization, providing an alternative to the `ignore_above` mapping parameter when you want to keep truncated data rather than discard it entirely.

## Details

### What's New in v3.4.0

The `truncate` token filter can now be used in custom normalizers. Previously, the truncate filter was only available for use in analyzers. This change enables keyword fields to have their values shortened to a maximum character length during the normalization process.

### Technical Changes

#### Implementation

The change involves marking `TruncateTokenFilterFactory` as a `NormalizingTokenFilterFactory`:

```java
public class TruncateTokenFilterFactory extends AbstractTokenFilterFactory 
    implements NormalizingTokenFilterFactory {
    // ...
}
```

This simple interface implementation allows the truncate filter to be recognized as compatible with normalizers.

#### How Normalizers Work

A normalizer functions similarly to an analyzer but outputs only a single token. It does not contain a tokenizer and can only include specific types of character and token filters that perform character-level operations. The truncate filter qualifies because it operates on individual characters without changing the token structure.

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `length` | Maximum number of characters for the token | Required (no default) |

### Usage Example

Create an index with a custom normalizer using the truncate filter:

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_truncate": {
          "type": "truncate",
          "length": 10
        }
      },
      "normalizer": {
        "my_normalizer": {
          "type": "custom",
          "filter": ["lowercase", "my_truncate"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "product_code": {
        "type": "keyword",
        "normalizer": "my_normalizer"
      }
    }
  }
}
```

Index a document with a long value:

```json
POST /my_index/_doc/1
{
  "product_code": "ABCDEFGHIJKLMNOP"
}
```

The stored and indexed value will be truncated to `abcdefghij` (10 characters, lowercased).

### Use Cases

- **Data preservation**: Keep truncated keyword values instead of ignoring documents that exceed `ignore_above`
- **Consistent field lengths**: Ensure all keyword values conform to a maximum length
- **Combined normalization**: Apply truncation along with other normalizing filters like `lowercase` or `asciifolding`

## Limitations

- The `length` parameter is required and must be a positive integer
- Truncation happens at the character level, which may split multi-byte characters in certain edge cases
- Cannot be combined with non-normalizing token filters in a normalizer

## References

### Documentation
- [Truncate Token Filter Documentation](https://docs.opensearch.org/3.0/analyzers/token-filters/truncate/)
- [Normalizers Documentation](https://docs.opensearch.org/3.0/analyzers/normalizers/)
- [Documentation PR #11429](https://github.com/opensearch-project/documentation-website/pull/11429): Public documentation update

### Pull Requests
| PR | Description |
|----|-------------|
| [#19779](https://github.com/opensearch-project/OpenSearch/pull/19779) | Make truncate filter a normalizer token filter |

### Issues (Design / RFC)
- [Issue #19778](https://github.com/opensearch-project/OpenSearch/issues/19778): Feature request for truncate filter in normalizers

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/normalizer-enhancements.md)
