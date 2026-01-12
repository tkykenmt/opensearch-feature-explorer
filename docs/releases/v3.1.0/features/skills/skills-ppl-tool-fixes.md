# Skills PPL Tool Fixes

## Summary

This bugfix addresses an issue in the PPLTool where multi-field mappings (such as `text` fields with a `keyword` sub-field) were not being properly exposed to the LLM model. The fix enables the model to use sub-fields like `a.keyword` for aggregations on text fields, which is required since PPL/DSL does not allow aggregations directly on text fields.

## Details

### What's New in v3.1.0

The PPLTool now correctly extracts and exposes multi-field mappings to the LLM model. This allows the model to generate valid PPL queries that use keyword sub-fields for aggregation operations.

### Technical Changes

#### Bug Fix

The fix is a single-line change in `PPLTool.java` that modifies the `extractFieldNamesTypes` call to include multi-field mappings:

```java
// Before (v3.0.0)
ToolHelper.extractFieldNamesTypes(mappingSource, fieldsToType, "", false);

// After (v3.1.0)
ToolHelper.extractFieldNamesTypes(mappingSource, fieldsToType, "", true);
```

The fourth parameter (`includeFields`) controls whether the `fields` property in mappings is traversed to extract sub-fields.

#### Affected Scenario

For index mappings like:
```json
{
  "a": {
    "type": "text",
    "fields": {
      "keyword": {"type": "keyword"}
    }
  }
}
```

- **Before**: Only `a` (text) was exposed to the model
- **After**: Both `a` (text) and `a.keyword` (keyword) are exposed

This enables the LLM to generate correct PPL queries for aggregations:
```ppl
source=my_index | stats count() by a.keyword
```

### Impact

- Improves PPL query generation accuracy for indexes with multi-field mappings
- Enables aggregation queries on text fields via their keyword sub-fields
- No configuration changes required

## Limitations

- The fix only affects the `constructTableInfo` method used for OpenSearch indexes
- S3/Spark data sources use a separate code path (`constructTableInfoByPPLResultForSpark`) which was not affected

## References

### Documentation
- [PPL Tool Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/tools/ppl-tool/): Official PPL tool documentation
- [Multi-field Mappings](https://docs.opensearch.org/3.0/field-types/mapping-parameters/fields/): OpenSearch fields mapping parameter

### Pull Requests
| PR | Description |
|----|-------------|
| [#581](https://github.com/opensearch-project/skills/pull/581) | Fix fields bug in PPL tool |

## Related Feature Report

- [Full feature documentation](../../../features/skills/skills-tools.md)
