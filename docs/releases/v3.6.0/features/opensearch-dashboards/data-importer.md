---
tags:
  - opensearch-dashboards
---
# Data Importer

## Summary

The Data Importer plugin in OpenSearch Dashboards v3.6.0 adds upload alias support for dimensional data enrichment. When importing files (CSV, JSON, NDJSON), users can now specify an optional alias name that creates a filtered OpenSearch alias backed by a discriminator field (`__lookup`). This enables multiple logical datasets to coexist in a single index while remaining individually addressable — a key building block for PPL `lookup` command integration.

## Details

### What's New in v3.6.0

Upload aliases allow users to associate uploaded datasets with a named alias for easy reference in subsequent queries. This is particularly useful for analytics workflows where large fact tables (e.g., request logs) are enriched with small dimension tables (e.g., host metadata, client context).

When an alias is specified during import:

1. A UUID-based lookup ID is generated server-side
2. A `__lookup` keyword field is added to the index mapping
3. Each ingested document is supplemented with the lookup ID in the `__lookup` field
4. A filtered alias is created via the `_aliases` API, scoped to documents matching the lookup ID

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "lookup_data",
        "alias": "hosts",
        "filter": {
          "term": {
            "__lookup": "<generated-uuid>"
          }
        }
      }
    }
  ]
}
```

### Technical Changes

**Frontend (UI)**
- New `importIdentifier` state field in `DataImporterPluginApp`
- `EuiFieldText` input for alias name with placeholder "Alias name"
- Help text: "Create a filtered alias for this dataset to easily reference it later."
- The alias value is passed to both `importFile` and `importText` API calls as a query parameter

**Server Routes (`import_file.ts`, `import_text.ts`)**
- `importIdentifier` query parameter with alphanumeric validation (`/^[a-z][a-z0-9_-]*$/i`)
- UUID generation via `uuid.v4()` for lookup ID
- `__lookup` keyword field injected into index mapping during `createMode`
- Filtered alias creation after successful ingestion (zero failed rows)
- Graceful degradation: alias creation failure is logged but does not fail the import

**Processors (`csv_processor.ts`, `json_processor.ts`, `ndjson_processor.ts`)**
- `IngestOptions` extended with `lookupId` and `lookupField` optional fields
- Each processor injects `{ [lookupField]: lookupId }` into documents when both values are provided

**Utilities (`util.ts`)**
- `ALPHANUMERIC_REGEX_STRING`: `/^[a-z][a-z0-9_-]*$/i`
- `LOOKUP_FIELD`: `'__lookup'`

### Configuration

The alias field is optional. The Data Importer plugin must be enabled:

```yaml
data_importer.enabled: true
```

For local development:
```bash
yarn start:explore --workspace.enabled=true --data_importer.enabled=true
```

## Limitations

- Alias is only created when all rows are successfully ingested (zero failed rows)
- Alias names must be alphanumeric with hyphens/underscores, starting with a letter
- The `__lookup` field name is hardcoded and not configurable per-index
- Upload aliases are only available in `createMode` (new index creation)
- No UI for managing or viewing existing upload aliases after creation

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11303` | Add upload aliases to data importer | `https://github.com/opensearch-project/sql/issues/5074` |

### Related
- RFC: Discriminator-based lookups — `https://github.com/opensearch-project/sql/issues/5074`
- Data Importer Discover integration — `https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11180`
