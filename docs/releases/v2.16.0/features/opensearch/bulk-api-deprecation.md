---
tags:
  - opensearch
---
# Bulk API Deprecation

## Summary

In v2.16.0, the `batch_size` parameter on the Bulk API was deprecated and its default value changed to `Integer.MAX_VALUE`. This change makes batch processing automatic for ingest pipelines, eliminating the need for users to manually configure batch sizes. Additionally, a bug fix ensures that `default_pipeline` and `final_pipeline` settings from index templates are correctly applied during bulk upsert operations when auto-creating indexes.

## Details

### batch_size Parameter Deprecation

The `batch_size` parameter was introduced in v2.14.0 to control how many documents are batched together when processed by ingest pipelines. However, requiring users to manually set this parameter created unnecessary complexity.

**Changes in v2.16.0:**
- Default value changed from `1` to `Integer.MAX_VALUE`
- Using the `batch_size` parameter now emits a deprecation warning
- All documents in a bulk request are now processed together by default

This change allows ingest processor developers to optimize batch processing internally, providing performance benefits without requiring changes to client ingestion tooling.

### Pipeline Resolution Bug Fix

A bug was fixed where bulk upsert operations would not honor `default_pipeline` and `final_pipeline` settings defined in index templates when the target index didn't exist and was auto-created.

**Root Cause:**
When executing an update action with upsert in the Bulk API, if the specified index doesn't exist but matches an index template, the `index` field was `null` in the `IndexRequest`. This caused the pipeline resolution code path to be skipped.

**Fix:**
The pipeline resolution logic now correctly resolves pipelines from index templates even when the index is being auto-created during the bulk operation.

## Limitations

- The `batch_size` parameter is deprecated and will be removed in a future version (removed in v3.0.0)
- Users should update their tooling to remove explicit `batch_size` settings

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14725](https://github.com/opensearch-project/OpenSearch/pull/14725) | Change default batch size to Integer.MAX_VALUE and add deprecation warning | [#14283](https://github.com/opensearch-project/OpenSearch/issues/14283) |
| [#12891](https://github.com/opensearch-project/OpenSearch/pull/12891) | Fix bulk upsert ignores default_pipeline and final_pipeline | [#12888](https://github.com/opensearch-project/OpenSearch/issues/12888) |

### Documentation
- [Bulk API Documentation](https://docs.opensearch.org/2.16/api-reference/document-apis/bulk/)
