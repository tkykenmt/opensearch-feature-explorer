---
tags:
  - opensearch
---
# Query Fixes

## Summary

OpenSearch v2.16.0 includes two important bug fixes for query functionality: a fix for `match_phrase_prefix` query not working correctly on text fields with multiple values and `index_prefixes`, and a fix for `FuzzyQuery` on keyword fields to properly use `IndexOrDocValuesQuery` when both index and doc_values are enabled.

## Details

### match_phrase_prefix Query Fix

**Issue**: When executing a `match_phrase_prefix` query on a text field with multiple values and `index_prefixes` enabled, the query would fail to return expected results. This occurred because the sub-field `{text_field}._index_prefix` was not using the `position_increment_gap` parameter (which defaults to 100), causing the `spanNearQuery` to not work correctly.

**Root Cause**: The `PrefixFieldType` was not properly inheriting the `position_increment_gap` from the parent text field's analyzer. When multiple values are indexed in an array field, OpenSearch uses `position_increment_gap` to create a fake gap between values to prevent phrase queries from matching across array boundaries.

**Fix**: The `PrefixWrappedAnalyzer` class was updated to accept and use the `position_increment_gap` from the parent analyzer. The `PrefixFieldType` now properly sets the analyzer with the correct position increment gap.

**Changed Files**:
- `TextFieldMapper.java`: Updated `PrefixWrappedAnalyzer` to include `positionIncrementGap` parameter and override `getPositionIncrementGap()` method
- `TextFieldTypeTests.java`: Added test for position increment gap on index prefix field

### FuzzyQuery on Keyword Field Fix

**Issue**: `FuzzyQuery` on keyword fields was not using `IndexOrDocValuesQuery` when both `index` and `doc_values` were set to `true`, missing potential query optimization.

**Root Cause**: In `FuzzyQueryBuilder.doToQuery()`, the call to `fieldType.fuzzyQuery()` was going to `StringFieldType.fuzzyQuery()` instead of `KeywordFieldMapper.fuzzyQuery()` because the method signature didn't include the `RewriteMethod` parameter.

**Fix**: Added a new overloaded `fuzzyQuery()` method in `StringFieldType` that accepts the `RewriteMethod` parameter, and updated `FuzzyQueryBuilder` to call this new method. This allows `KeywordFieldMapper` to properly construct an `IndexOrDocValuesQuery` that can leverage both the inverted index and doc values for better query performance.

**Changed Files**:
- `StringFieldType.java`: Added new `fuzzyQuery()` method with `RewriteMethod` parameter
- `KeywordFieldMapper.java`: Fixed call to `super.fuzzyQuery()` to include `method` parameter
- `FuzzyQueryBuilder.java`: Updated to call the new method signature

## Limitations

- The `match_phrase_prefix` fix requires reindexing documents to take effect for existing indices
- The `FuzzyQuery` optimization only applies when both `index: true` and `doc_values: true` are set on keyword fields

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#10959](https://github.com/opensearch-project/OpenSearch/pull/10959) | Fix match_phrase_prefix_query not working on text field with multiple values and index_prefixes | [#9203](https://github.com/opensearch-project/OpenSearch/issues/9203) |
| [#14378](https://github.com/opensearch-project/OpenSearch/pull/14378) | Fix FuzzyQuery in keyword field will use IndexOrDocValuesQuery when both of index and doc_value are true | [#14377](https://github.com/opensearch-project/OpenSearch/issues/14377) |

### Documentation
- [Fuzzy Query](https://docs.opensearch.org/2.16/query-dsl/term/fuzzy/)
- [Match Phrase Prefix Query](https://docs.opensearch.org/2.16/query-dsl/full-text/match-phrase-prefix/)
