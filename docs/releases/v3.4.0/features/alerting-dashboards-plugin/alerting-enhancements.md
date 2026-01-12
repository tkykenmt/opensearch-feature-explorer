# Alerting Enhancements

## Summary

OpenSearch v3.4.0 introduces two enhancements to the Alerting Dashboards plugin: support for keyword filters in bucket-level monitor triggers and proper Multi-Data Source (MDS) client usage for OpenSearch API calls. These improvements fix issues where keyword filters were not being attached to bucket-level triggers and ensure correct data source routing when MDS is enabled.

## Details

### What's New in v3.4.0

#### Keyword Filter Support for Bucket-Level Monitor Triggers

Previously, keyword filters were not being attached to bucket-level monitor triggers because the validation logic did not account for the `TRIGGER_OPERATORS_MAP.INCLUDE` and `TRIGGER_OPERATORS_MAP.EXCLUDE` operators. The `validateFormField` function incorrectly returned `false` for these cases, assuming the field value was empty.

This fix adds proper handling for the INCLUDE and EXCLUDE operators in the `validateWhereFilter` function, ensuring keyword filters are correctly attached to bucket-level monitor triggers.

#### Multi-Data Source (MDS) Client Support

When Multi-Data Source is enabled, the alerting dashboards server was not correctly resolving the data source ID for OpenSearch API calls (cluster plugins, settings, health). This caused the wrong client to be used when making API calls.

The fix updates the following API routes to properly validate and use the data source ID from the browser request:
- `/api/alerting/_plugins`
- `/api/alerting/_settings`
- `/api/alerting/_health`

### Technical Changes

#### Modified Files

| File | Change |
|------|--------|
| `public/pages/CreateMonitor/components/MonitorExpressions/expressions/utils/whereHelpers.js` | Added INCLUDE/EXCLUDE operator handling in `validateWhereFilter` |
| `server/routes/opensearch.js` | Added query validation schema for MDS data source ID |

#### Code Changes

The keyword filter fix adds handling for two additional operator cases:

```javascript
case TRIGGER_OPERATORS_MAP.INCLUDE:
case TRIGGER_OPERATORS_MAP.EXCLUDE:
  filterIsValid = filterIsValid && !_.isEmpty(filter.fieldValue?.toString());
  break;
```

The MDS fix adds query validation to OpenSearch API routes:

```javascript
router.get(
  {
    path: '/api/alerting/_plugins',
    validate: {
      query: createValidateQuerySchema(dataSourceEnabled),
    },
  },
  opensearchService.getPlugins
);
```

### Usage Example

With this fix, users can now create bucket-level monitor triggers with keyword filters using the INCLUDE or EXCLUDE operators:

```json
{
  "trigger": {
    "name": "high-error-rate",
    "condition": {
      "buckets_path": {
        "count_var": "_count"
      },
      "parent_bucket_path": "composite_agg",
      "script": {
        "source": "params.count_var > 5"
      }
    },
    "filters": [
      {
        "fieldName": "status",
        "fieldOperator": "INCLUDE",
        "fieldValue": ["error", "critical"]
      }
    ]
  }
}
```

## Limitations

- The MDS client fix requires Multi-Data Source to be enabled in OpenSearch Dashboards configuration
- Keyword filters are only applicable to bucket-level monitors, not query-level or document-level monitors

## References

### Documentation
- [Alerting Documentation](https://docs.opensearch.org/3.0/observing-your-data/alerting/index/): Official alerting documentation
- [Triggers Documentation](https://docs.opensearch.org/3.0/observing-your-data/alerting/triggers/): Trigger configuration guide
- [Per Query and Per Bucket Monitors](https://docs.opensearch.org/3.0/observing-your-data/alerting/per-query-bucket-monitors/): Monitor types documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#1325](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1325) | Allow keyword filter to be attached to bucket level monitor trigger |
| [#1313](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1313) | Onboarded opensearch apis to use MDS client when MDS is enabled |

## Related Feature Report

- [Full feature documentation](../../../features/alerting-dashboards-plugin/alerting-dashboards.md)
