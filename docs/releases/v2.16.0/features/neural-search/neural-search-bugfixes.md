---
tags:
  - neural-search
---
# Neural Search Bugfixes

## Summary

OpenSearch v2.16.0 includes several bug fixes and infrastructure improvements for the neural-search plugin. The most significant fix addresses missing results in hybrid queries when concurrent segment search is enabled on shards with 6 or more segments. Additional changes include backward compatibility (BWC) test improvements for batch ingestion and neural sparse two-phase processor, along with CI/build fixes for JDK 21 compatibility.

## Details

### What's New in v2.16.0

#### HybridQuery Concurrent Segment Search Fix

Fixed a critical bug where hybrid queries could return incomplete results when concurrent segment search was enabled on shards with 6 or more segments.

**Root Cause**: The collector manager incorrectly assumed only one hybrid query result collector would exist in the reduce phase. Lucene's `IndexSearcher` creates multiple collectors when processing more than 5 segments (or 250,000 docs per slice), each containing a portion of results.

**Solution**: Implemented proper merging logic at the shard level to combine results from multiple collectors. The merge process:
1. Identifies results from each sub-query across collectors
2. Merges sub-query results separately
3. Wraps merged results back into hybrid query format

#### BWC Test Infrastructure

- Added backward compatibility tests for batch ingestion feature
- Added BWC tests for neural sparse query two-phase search processor
- Improved test infrastructure with cleaner version checks

#### CI/Build Fixes

- Fixed CI errors caused by JDK version mismatch between ml-commons and neural-search
- Updated JDK version to 21 in maven publish workflow
- Corrected gradle file function names and comments

## Limitations

- Concurrent segment search results may still vary due to non-deterministic merge order (documented behavior)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#800](https://github.com/opensearch-project/neural-search/pull/800) | Fix for missing HybridQuery results when concurrent segment search is enabled | [#799](https://github.com/opensearch-project/neural-search/issues/799) |
| [#769](https://github.com/opensearch-project/neural-search/pull/769) | Add BWC for batch ingestion | [#763](https://github.com/opensearch-project/neural-search/issues/763) |
| [#777](https://github.com/opensearch-project/neural-search/pull/777) | Add backward test cases for neural sparse two phase processor | [#646](https://github.com/opensearch-project/neural-search/issues/646) |
| [#795](https://github.com/opensearch-project/neural-search/pull/795) | Fix function names and comments in the gradle file for BWC tests | - |
| [#835](https://github.com/opensearch-project/neural-search/pull/835) | Fix CI for JDK upgrade towards 21 | - |
| [#837](https://github.com/opensearch-project/neural-search/pull/837) | Maven publishing workflow by upgrade jdk to 21 | - |
