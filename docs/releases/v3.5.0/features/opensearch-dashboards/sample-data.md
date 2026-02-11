---
tags:
  - opensearch-dashboards
---
# Sample Data

## Summary

In v3.5.0, the sample data installation in OpenSearch Dashboards now supports custom `_id` values when inserting documents into sample dataset indices. Previously, the bulk insert operation always auto-generated UUIDs for the `_id` field. This change enables plugins (such as the dashboards-search-relevance plugin) to provide their own `_id` values in sample dataset JSON data, which is essential for datasets like UBI (User Behavior Insights) that require deterministic document IDs.

## Details

### What's New in v3.5.0

The `insertDataIntoIndex` function in the home plugin's sample data install route was updated to check each document for a `_id` field before bulk indexing. If a document contains `_id`, it is extracted and set on the bulk insert command; otherwise, OpenSearch auto-generates the ID as before.

### Technical Changes

The change is in `src/plugins/home/server/services/sample_data/routes/install.ts`:

- The `insertCmd` object is now created per-document (moved inside the `forEach` loop) instead of being shared across all documents
- If `doc._id` exists, it is assigned to `insertCmd.index._id` and then deleted from the document body to avoid indexing it as a field
- Backward compatible: documents without `_id` continue to use auto-generated UUIDs

```typescript
const bulkInsert = async (docs: any) => {
  const bulk: any[] = [];
  docs.forEach((doc: any) => {
    const insertCmd: any = { index: { _index: index } };
    if (doc._id) {
      insertCmd.index._id = doc._id;
      delete doc._id;
    }
    bulk.push(insertCmd);
    bulk.push(updateTimestamps(doc));
  });
  // ...
};
```

### Motivation

This change was driven by the need to support UBI sample datasets in the Search Relevance Workbench (SRW) playground. UBI datasets require specific document IDs to maintain referential integrity between query events and click events. Without custom `_id` support, the sample data service could not properly load UBI datasets.

## Limitations

- Only affects sample dataset installation; regular data ingestion is not impacted
- The `_id` field must be a top-level property in the sample data JSON documents
- The `_id` value is removed from the document body after extraction (not stored as a regular field)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11139](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11139) | Support _id when insert data into sample dataset index | [dashboards-search-relevance#730](https://github.com/opensearch-project/dashboards-search-relevance/issues/730) |

### Related Issues
- [dashboards-search-relevance#730](https://github.com/opensearch-project/dashboards-search-relevance/issues/730): Support UBI sample dataset in playground
