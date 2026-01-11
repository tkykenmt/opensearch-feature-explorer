# Search Relevance Fixes

## Summary

This bugfix improves the `ImportJudgmentsProcessor` in the Search Relevance plugin to handle ratings provided in numeric formats (integers, floats) in addition to strings. Previously, passing numeric ratings caused a `ClassCastException` that crashed the OpenSearch process. The fix also ensures imported judgments maintain their original order.

## Details

### What's New in v3.3.0

The `ImportJudgmentsProcessor` now properly handles ratings data in any numeric format, converting them to strings internally before processing. This fix addresses a critical bug where importing judgments with numeric ratings would cause OpenSearch to crash.

### Technical Changes

#### Bug Description

When importing judgments via the Search Relevance API, users could provide ratings as either strings or numbers:

```json
// String format (worked)
{"docId": "doc1", "rating": "1.0"}

// Numeric format (caused crash)
{"docId": "doc1", "rating": 1.0}
```

The numeric format caused a `ClassCastException`:
```
java.lang.ClassCastException: class java.lang.Integer cannot be cast to class java.lang.String
    at org.opensearch.searchrelevance.judgments.ImportJudgmentsProcessor.generateJudgmentRating
```

#### Fix Implementation

The fix modifies `ImportJudgmentsProcessor.java` to:

1. Accept ratings as `Object` instead of `String`
2. Convert any numeric type to String using `String.valueOf()`
3. Preserve the original order of imported judgments using a `List` instead of `HashMap`

```java
// Before (caused ClassCastException)
String rating = (String) ratingInfo.get("rating");

// After (handles any type)
Object ratingObj = ratingInfo.get("rating");
String rating = String.valueOf(ratingObj);
```

#### Order Preservation

The fix also addresses a secondary issue where imported judgments could be returned in a different order than submitted. The implementation now uses an `ArrayList` to maintain insertion order:

```java
// Before: HashMap lost ordering
Map<String, String> docRatings = new HashMap<>();

// After: ArrayList preserves order
List<Map<String, String>> docIdRatings = new ArrayList<>();
```

### Usage Example

Import judgments with mixed rating formats:

```json
PUT _plugins/_search_relevance/judgments
{
  "name": "Product Search Judgments",
  "type": "IMPORT_JUDGMENT",
  "judgmentRatings": [
    {
      "query": "laptop",
      "ratings": [
        {"docId": "doc1", "rating": 1},
        {"docId": "doc2", "rating": "0.5"},
        {"docId": "doc3", "rating": 0.75}
      ]
    }
  ]
}
```

All rating formats (integer `1`, string `"0.5"`, float `0.75`) are now handled correctly.

## Limitations

- Ratings must still be valid numeric values (parseable as float)
- Non-numeric strings like `"high"` or `"relevant"` will still fail validation

## Related PRs

| PR | Description |
|----|-------------|
| [#230](https://github.com/opensearch-project/search-relevance/pull/230) | Improve ImportJudgmentsProcessor handling of ratings data types |

## References

- [Issue #229](https://github.com/opensearch-project/search-relevance/issues/229): Bug report - Posting rating as integer causes class cast issues
- [Search Relevance Plugin Repository](https://github.com/opensearch-project/search-relevance)
- [Search Relevance Workbench Documentation](https://docs.opensearch.org/3.0/search-plugins/search-relevance/index/)

## Related Feature Report

- [Full feature documentation](../../../../features/search-relevance/search-relevance-workbench.md)
