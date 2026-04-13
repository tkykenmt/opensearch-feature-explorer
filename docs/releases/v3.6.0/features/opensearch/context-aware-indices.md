---
tags:
  - opensearch
---
# Context-Aware Indices

## Summary

OpenSearch v3.6.0 includes two improvements to the Context Aware Segments feature: immutable grouping criteria enforcement and a refactored codec architecture that properly delegates to the underlying codec.

## Details

### What's New in v3.6.0

#### Immutable Grouping Criteria (PR #20250)

Documents indexed into context-aware indices can no longer have their grouping criteria field updated. Previously, updating a document's grouping criteria could cause it to move between segment groups, creating complex version synchronization issues across multiple IndexWriters. This change prevents such updates at two levels:

1. **Version Map Check**: During version resolution in `InternalEngine.resolveDocVersion()`, if the document already exists and the new document has a different grouping criteria, an `UnsupportedOperationException` is thrown.
2. **Segment-Level Check**: In `VersionsAndSeqNoResolver.loadDocIdAndVersion()`, the current criteria is compared against the segment's bucket attribute. If they differ, the operation is rejected.

The `KeyedLock` per-document lock was removed from `CompositeIndexWriter` since criteria immutability eliminates the need for complex version synchronization across child and parent writers. The `validateImmutableFieldNotUpdated()` method was added to the `DocumentIndexWriter` interface.

Documents that have been deleted (tombstone only) can still be re-indexed with a different grouping criteria, as the previous criteria is no longer active.

#### CriteriaBasedCodec Delegate Codec Fix (PR #20442)

The `CriteriaBasedCodec` was refactored to properly work with any delegate codec (e.g., zstd, best_compression) instead of being hardcoded to `Lucene103Codec`. Key changes:

- **Removed**: `CriteriaBasedDocValueFormat` class — bucket attributes are no longer attached via DocValues
- **Added**: `CriteriaBasedPostingsFormat` — a new `PostingsFormat` that attaches bucket attributes via the `_id` field's postings format using Lucene's per-field `PerFieldPostingsFormat` mechanism
- **Changed**: `CriteriaBasedCodec` now uses `super(delegate.getName(), delegate)` instead of hardcoding `"CriteriaBasedCodec"` as the codec name, allowing proper SPI resolution during reads
- **Changed**: `CriteriaBasedCodec` is no longer registered as a Lucene SPI Codec; instead, `CriteriaBasedPostingsFormat` is registered as a SPI PostingsFormat
- **Extended**: `CriteriaBasedMergePolicy` now overrides `findForcedMerges()`, `findForcedDeletesMerges()`, and `findFullFlushMerges()` in addition to `findMerges()`, ensuring group-aware merging in all merge scenarios

The new architecture stores the delegate codec name as a segment attribute (`delegate_codec_key`), enabling the `CriteriaBasedPostingsFormat` to delegate reads to the correct postings format during segment reads.

### Technical Changes

| Change | Before | After |
|--------|--------|-------|
| Bucket attribute storage | `SegmentInfoFormat` (write hook) + `CriteriaBasedDocValueFormat` | `CriteriaBasedPostingsFormat` via `_id` field |
| Codec name in `FilterCodec` | Hardcoded `"CriteriaBasedCodec"` | Delegate codec's name |
| SPI registration | `CriteriaBasedCodec` as Codec | `CriteriaBasedPostingsFormat` as PostingsFormat |
| Per-document locking | `KeyedLock` in `CompositeIndexWriter` | Removed (criteria immutability) |
| Merge policy coverage | `findMerges()` only | `findMerges()`, `findForcedMerges()`, `findForcedDeletesMerges()`, `findFullFlushMerges()` |

## Limitations

- Grouping criteria field updates are now explicitly blocked with `UnsupportedOperationException`
- Feature remains experimental behind the `opensearch.experimental.feature.context_aware.migration.enabled` flag

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#20250](https://github.com/opensearch-project/OpenSearch/pull/20250) | Prevent criteria field updates for context-aware indices | - |
| [#20442](https://github.com/opensearch-project/OpenSearch/pull/20442) | Fix CriteriaBasedCodec to work with delegate codec | - |
