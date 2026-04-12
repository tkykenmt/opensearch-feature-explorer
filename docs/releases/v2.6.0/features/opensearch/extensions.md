---
tags:
  - opensearch
---
# Extensions

## Summary

OpenSearch 2.6.0 introduces 4 new feature(s) and 0 enhancement(s) to Extensions.

## Details

### New Features

- **Add query for initialized extensions**: Create a feature to have an extension query to OpenSearch to obtain a list of initialized extensions and determine whether a particular extension is initialized. Equivalent PR on OpenSearch-sdk-java : https://github.com/opensearch-project/opensearch-sdk-java/pull/300
- **Replace latches with CompletableFutures for extensions**: Removes latches and CompletableFuture .get() calls to make requests asynchronous
- **Add support for minimum compatible version for extensions**: Part of https://github.com/opensearch-project/opensearch-sdk-java/issues/346. Added support to define minimum compatible version for extensions talking to OpenSearch. As we are limiting to minor version compatibility for now, we will revisit this validation when major version compatibility is in the
- **Fix timeout error when adding a document to an index with extension running**: Added in PR #6275.

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#5658](https://github.com/opensearch-project/OpenSearch/pull/5658) | Add query for initialized extensions | OpenSearch |
| [#5646](https://github.com/opensearch-project/OpenSearch/pull/5646) | Replace latches with CompletableFutures for extensions | OpenSearch |
| [#6003](https://github.com/opensearch-project/OpenSearch/pull/6003) | Add support for minimum compatible version for extensions | OpenSearch |
| [#6275](https://github.com/opensearch-project/OpenSearch/pull/6275) | Fix timeout error when adding a document to an index with extension running | OpenSearch |
