---
tags:
  - dashboards
  - performance
  - search
---

# Alerting Improvements

## Summary

This release includes a refactoring change to the alert summary context feature in the Alerting Dashboards Plugin. The change optimizes the alert context sent to AI agents by limiting it to only the latest active alert instead of multiple alerts, improving the relevance and focus of AI-generated summaries.

## Details

### What's New in v3.0.0

The `DEFAULT_ACTIVE_ALERTS_TOP_N` constant has been renamed to `DEFAULT_ACTIVE_ALERTS_AI_TOP_N` and its value reduced from 10 to 1. This change ensures that when generating AI-powered alert summaries, only the most recent active alert is included in the context sent to the LLM.

### Technical Changes

#### Configuration Changes

| Setting | Previous Value | New Value | Description |
|---------|---------------|-----------|-------------|
| `DEFAULT_ACTIVE_ALERTS_AI_TOP_N` | 10 (as `DEFAULT_ACTIVE_ALERTS_TOP_N`) | 1 | Number of active alerts included in AI summary context |

#### Code Changes

The change affects two files in the alerting-dashboards-plugin:

1. `public/pages/Dashboard/utils/constants.js`:
   - Renamed `DEFAULT_ACTIVE_ALERTS_TOP_N` to `DEFAULT_ACTIVE_ALERTS_AI_TOP_N`
   - Changed value from 10 to 1

2. `public/pages/Dashboard/utils/tableUtils.js`:
   - Updated import to use new constant name
   - Alert filtering now uses `DEFAULT_ACTIVE_ALERTS_AI_TOP_N`

### Rationale

By focusing on only the latest active alert:
- AI summaries are more focused and relevant
- Token usage is reduced when calling LLM APIs
- The most current alert state is prioritized for analysis
- Response quality improves by avoiding context dilution from older alerts

### Usage Example

The change is transparent to users. When viewing alert insights in OpenSearch Dashboards:

1. Navigate to **OpenSearch Plugins > Alerting**
2. Hover over alerts to see the sparkle icon
3. Click to view the AI-generated summary based on the latest active alert

## Limitations

- Only the most recent active alert is analyzed for AI summaries
- Historical alert context is not included in AI analysis
- Requires dashboards-assistant plugin for AI features

## References

### Documentation
- [Alert Insights Documentation](https://docs.opensearch.org/3.0/dashboards/dashboards-assistant/alert-insight/): Official docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#1220](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1220) | Only use latest active alert for alert summary context |

## Related Feature Report

- [Full feature documentation](../../../features/alerting-dashboards-plugin/alerting-dashboards-plugin-alerting-summary-insights.md)
