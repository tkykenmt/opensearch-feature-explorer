---
tags:
  - opensearch
---
# Search Query Fixes

## Summary

OpenSearch v3.6.0 includes eight bug fixes addressing correctness and reliability issues across search queries, field mappings, aggregations, and index template management. These fixes resolve problems with `copy_to` for geo_point fields, `field_caps` with `disable_objects` mappings, terms lookup clause count limits, wildcard aggregation concurrency, range query validation, synonym_graph analyzer dependency ordering, index template pattern collision false positives, and a missing `IndicesOptions` static accessor.

## Details

### What's New in v3.6.0

#### Fix `copy_to` for geo_point Fields (PR #20542)

The `copy_to` attribute on `geo_point` fields failed when values were represented as objects (`{"lat": 40.71, "lon": 74.00}`) or arrays (`[74.00, 40.71]`). The XContent parser consumed all tokens during initial field parsing, leaving no data for the `copy_to` operation.

The fix serializes complex values to a byte array before parsing begins, then creates fresh parser instances for each `copy_to` target field. New methods `parseFieldWithCopyTo()` and `parseChildToBytes()` were added to `DocumentParser`.

#### Fix `field_caps` with `disable_objects` Mappings (PR #20814)

Two bugs were fixed:
1. `_field_caps` returned empty results for indexes where a `disable_objects: true` object field had child fields. When walking the parent chain of a flattened leaf field, intermediate paths with no `ObjectMapper` caused failures. A null check was added to skip them.
2. Field name corruption occurred after subsequent document indexing (e.g., `attributes.foo.bar` became `attributes.foo.foo.bar`). `ParametrizedFieldMapper.merge()` used `name().lastIndexOf('.')` incorrectly to reconstruct the parent `ContentPath`. The fix computes the boundary from `simpleName.length()` instead.

#### Fix Terms Lookup `max_clause_count` (PR #20823)

`TermsQueryBuilder.fetch()` read `indices.query.max_clause_count` (a non-existent setting path) with a hardcoded fallback of 1024, instead of the actual cluster setting `indices.query.bool.max_clause_count`. The fix replaces the raw `idxSettings.getAsInt(...)` call with `IndexSearcher.getMaxClauseCount()`, which reflects the cluster setting via `SearchService.INDICES_MAX_CLAUSE_COUNT_SETTING`.

#### Fix Wildcard Aggregation Concurrency (PR #20842)

An `ArrayIndexOutOfBoundsException` occurred with wildcard fields and aggregations under concurrent access. Multiple threads simultaneously called the `valueFetcher` object, causing the buffer to be read and written concurrently. The fix addresses the thread-safety issue in the value fetcher.

#### Add Range Validations (PR #20518)

Added range validation in the query builder and field mapper to prevent invalid range values from being accepted. This resolves cases where out-of-range values could cause unexpected behavior during query execution.

#### Fix synonym_graph with word_delimiter_graph (PR #19248)

The `synonym_graph` filter failed when used with `word_delimiter_graph` and a custom `synonym_analyzer` using whitespace or classic tokenizer. Two root causes were identified:
1. If an analyzer failed during build, the exception stopped the entire process, preventing the custom synonym analyzer from being instantiated.
2. If the synonym analyzer depended on another analyzer not yet built, the process failed because `analysisRegistry.getAnalyzer()` only checked built-in analyzers.

The fix introduces fail-safe analyzer building and dependency-aware ordering via an `order` attribute that defines precedence between analyzers. A new `analyzersBuiltSoFar` parameter is passed to `getChainAwareTokenFilterFactory`.

#### Fix Index Template Pattern Collision False Positives (PR #20702)

The previous implementation used full Lucene automaton intersection (`Operations.intersection`) to detect template pattern conflicts, which produced false positives for multi-wildcard patterns sharing a common literal prefix. The fix replaces the automaton intersection with a minimum-string heuristic: each `*` is substituted with `""` to produce the minimum matching string, then checked against the other pattern set using `Regex.simpleMatch`.

#### Expose `STRICT_EXPAND_OPEN_HIDDEN_FORBID_CLOSED` (PR #20980)

The `IndicesOptions` class provided static methods for all index options except `STRICT_EXPAND_OPEN_HIDDEN_FORBID_CLOSED`. A static accessor method was added for consistency and to enable proper documentation of this option.

## Limitations

- The wildcard aggregation concurrency fix (PR #20842) could not be reproduced in integration tests; the fix was verified through local reproduction only.
- The index template pattern collision fix uses a heuristic approach that may not catch all theoretically possible conflicts, but correctly handles realistic index naming patterns.

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/OpenSearch/pull/20542` | Fix `copy_to` for geo_point fields with object/array values | `https://github.com/opensearch-project/OpenSearch/issues/20540` |
| `https://github.com/opensearch-project/OpenSearch/pull/20814` | Fix `field_caps` empty results for `disable_objects` mappings | `https://github.com/opensearch-project/OpenSearch/issues/20811` |
| `https://github.com/opensearch-project/OpenSearch/pull/20823` | Fix terms lookup to use cluster `max_clause_count` setting | `https://github.com/opensearch-project/OpenSearch/issues/20820` |
| `https://github.com/opensearch-project/OpenSearch/pull/20842` | Fix `ArrayIndexOutOfBoundsException` with wildcard aggregations | `https://github.com/opensearch-project/OpenSearch/issues/20838` |
| `https://github.com/opensearch-project/OpenSearch/pull/20518` | Add range validations in query builder and field mapper | `https://github.com/opensearch-project/OpenSearch/issues/20497` |
| `https://github.com/opensearch-project/OpenSearch/pull/19248` | Fix synonym_graph filter with word_delimiter_graph | `https://github.com/opensearch-project/OpenSearch/issues/18037` |
| `https://github.com/opensearch-project/OpenSearch/pull/20702` | Fix index template pattern collision false positives | `https://github.com/opensearch-project/OpenSearch/issues/837` |
| `https://github.com/opensearch-project/OpenSearch/pull/20980` | Expose `STRICT_EXPAND_OPEN_HIDDEN_FORBID_CLOSED` index option | `https://github.com/opensearch-project/OpenSearch/issues/20963` |
