# Discover Summary / AI Assistant Integration

## Summary

This release includes multiple bug fixes and UX improvements for the Discover Summary feature in OpenSearch Dashboards. The Discover Summary uses AI/LLM to generate human-readable summaries of query results, helping users quickly understand their data. These fixes address markdown rendering, empty result handling, text styling, and error state management.

## Details

### What's New in v3.0.0

This release focuses on improving the user experience and reliability of the Discover Summary feature through several targeted bug fixes:

1. **Markdown Format Support**: Summary output now properly renders markdown formatting for better readability
2. **Empty Response Handling**: Summary panel no longer displays when there are no query results
3. **Text Size Consistency**: Summary text size standardized to "s" (small) for visual consistency
4. **UX Style Improvements**: Natural language input field alignment, icon updates, and padding adjustments
5. **Empty Result Regression Fix**: Fixed regression where summary failed when results were empty
6. **T2PPL Error Handling**: Summary now clears properly when text-to-PPL translation fails
7. **Placeholder Cleanup**: Removed placeholder showing last asked question after query failure

### Technical Changes

#### Component Updates

| Component | Change | PR |
|-----------|--------|-----|
| `QueryAssistSummary` | Added `EuiMarkdownFormat` for rendering markdown in summaries | #9464, #9553 |
| `QueryAssistSummary` | Hide summary when no response data | #9480 |
| `QueryAssistSummary` | Set text size to "s" for consistency | #9492 |
| `QueryAssistSummary` | Clear summary on T2PPL failure, improved error message | #9552 |
| `QueryAssistBar` | Clear generated query on failure, update state properly | #9552 |
| `QueryAssistInput` | Removed previous question from placeholder | #9552 |
| Discover Summary UI | Compressed input field, updated caution icon, adjusted padding | #9509 |

#### UI/UX Improvements

The following visual improvements were made to the Discover Summary section:

- Natural language input field height reduced to align with the button
- Caution banner icon updated for better visual communication
- Top margin added to natural language input field
- Consistent padding between elements within the discover summary panel

### Usage Example

The Discover Summary feature is accessed through the Discover page when using PPL queries:

1. Navigate to **OpenSearch Dashboards > Discover**
2. Select **PPL** from the query language dropdown
3. Enter a natural language question or PPL query
4. View the AI-generated summary below the query results

The summary now renders with proper markdown formatting:

```markdown
## Summary
- Total records: 383
- Error rate: 15%
- Top sources: artifacts.opensearch.org

### Key Findings
1. Most errors are 404 responses
2. Peak traffic from CN region
```

## Limitations

- Summary generation requires a configured Data2Summary agent
- Markdown rendering depends on `EuiMarkdownFormat` component capabilities
- Summary unavailable message now indicates to check for "results or errors" (improved from just "results")

## Related PRs

| PR | Description |
|----|-------------|
| [#9464](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9464) | Organizing generated summary by using markdown format |
| [#9480](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9480) | Should not show summary if there is no response |
| [#9492](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9492) | Text size in generated summary should be s |
| [#9509](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9509) | Fix minor UX style issues on discover summary section |
| [#9519](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9519) | Discover summary regression when result is empty |
| [#9552](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9552) | Clear discover summary if t2ppl failed |
| [#9553](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9553) | Use markdown in discover summary |

## References

- [Data Summary Documentation](https://docs.opensearch.org/3.0/dashboards/dashboards-assistant/data-summary/): Official documentation for the data summary feature
- [OpenSearch Assistant for OpenSearch Dashboards](https://docs.opensearch.org/3.0/dashboards/dashboards-assistant/index/): Parent feature documentation

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-dashboards/query-assistant.md)
