---
tags:
  - domain/ml
  - component/server
  - ml
  - observability
  - performance
  - search
  - sql
---
# Skills Log Insight

## Summary

This enhancement increases the `max_sample_count` parameter from 2 to 5 in the log insight feature of the `LogPatternAnalysisTool`. This change provides more representative sample logs for each detected pattern, improving the quality of log analysis insights.

## Details

### What's New in v3.4.0

The log insight feature in `LogPatternAnalysisTool` now returns up to 5 sample logs per pattern instead of 2. This enhancement provides users with more context when analyzing log patterns, making it easier to understand the nature and variations of each detected pattern.

### Technical Changes

#### Configuration Changes

| Setting | Previous Value | New Value | Description |
|---------|---------------|-----------|-------------|
| `max_sample_count` | 2 | 5 | Maximum number of sample logs returned per pattern in log insight mode |

#### Code Change

The change is in the PPL query construction within the `logInsight` method of `LogPatternAnalysisTool`:

```java
// Before
"mode=aggregation max_sample_count=2 "

// After
"mode=aggregation max_sample_count=5 "
```

### Usage Example

When using the `LogPatternAnalysisTool` in log insight mode (without baseline time range), the tool now returns more sample logs:

```json
{
  "logInsights": [
    {
      "pattern": "ERROR <*> failed to connect to <*>",
      "count": 150,
      "sampleLogs": [
        "ERROR service-a failed to connect to database-1",
        "ERROR service-b failed to connect to cache-server",
        "ERROR service-a failed to connect to api-gateway",
        "ERROR service-c failed to connect to message-queue",
        "ERROR service-b failed to connect to database-2"
      ]
    }
  ]
}
```

### Impact

- **Better Pattern Understanding**: More sample logs help users understand the variations within each pattern
- **Improved Debugging**: Additional samples provide more context for troubleshooting
- **No Performance Impact**: The change only affects the number of samples returned, not the pattern detection algorithm

## Limitations

- The `max_sample_count` is currently hardcoded and not configurable by users
- Sample logs are selected by the PPL patterns command, not by the tool itself

## References

### Documentation
- [Log Pattern Tool Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/tools/log-pattern-tool/): Official documentation
- [LogPatternAnalysisTool Source](https://github.com/opensearch-project/skills/blob/main/src/main/java/org/opensearch/agent/tools/LogPatternAnalysisTool.java): Implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#678](https://github.com/opensearch-project/skills/pull/678) | Backport: Increase max_sample_count to 5 for log insight |
| [#677](https://github.com/opensearch-project/skills/pull/677) | Original: Increase max_sample_count to 5 for log insight |

## Related Feature Report

- [Skills Tools](../../../features/skills/skills-tools.md)
