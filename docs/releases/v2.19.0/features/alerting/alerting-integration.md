---
tags:
  - alerting
---
# Alerting Integration

## Summary

OpenSearch v2.19.0 introduces AI-powered alerting integration that enables users to create alerts using natural language through the OpenSearch Assistant. This release adds the CreateAlertTool to the skills plugin, enhances the dashboards-assistant UI for in-context alert summarization, and includes several bug fixes for the alerting plugin.

## Details

### What's New in v2.19.0

#### CreateAlertTool

A new tool that allows users to create alerts using natural language queries. The tool leverages LLM capabilities to interpret user requests and generate appropriate alert configurations.

**Input Parameters:**
| Parameter | Description |
|-----------|-------------|
| `question` | User's natural language question about creating an alert |
| `indices` | Target indices for the monitor |
| `chat_history` | Optional conversation history for context |

**Workflow:**
1. Retrieves mapping information from target indices
2. Constructs a prompt with placeholders for question, indices, chat history, and mapping info
3. Requests LLM to generate alert configuration
4. Extracts and returns the alert configuration as JSON output

**Output Format:**
```json
{
  "name": "Alert Name",
  "search": {
    "indices": ["index_name"],
    "timeField": "timestamp",
    "bucketValue": 60,
    "bucketUnitOfTime": "m",
    "filters": [...],
    "aggregations": [...]
  },
  "triggers": [
    {
      "name": "Trigger Name",
      "severity": 1,
      "thresholdValue": 1,
      "thresholdEnum": "ABOVE"
    }
  ]
}
```

#### Custom Prompt Support

The CreateAlertTool now supports passing custom prompts as parameters to override the default prompt, and uses Claude as the default model type when not specified.

#### In-Context Alert Summarization UI

Updated UI in OpenSearch Dashboards for alert summarization:
- Removed blue dashed underline from alert links
- Added sparkle icon next to alerts indicating AI insights availability
- Hover effect with gradient on the icon
- Navigation support limited to visual editor alerts for Discover integration

### Bug Fixes

#### Alerting Plugin Fixes

| PR | Description |
|----|-------------|
| [#1778](https://github.com/opensearch-project/alerting/pull/1778) | Force create last run context in monitor workflow metadata when workflow is re-enabled |
| [#1780](https://github.com/opensearch-project/alerting/pull/1780) | Fix bucket selector aggregation writeable name |
| [#1183](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1183) | Change time format to UTC in notification message preview |
| [#1178](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1178) | Fix error toast message while configuring trigger during alert creation |
| [#1729](https://github.com/opensearch-project/alerting/pull/1729) | Optimize execution of workflow consisting of bucket-level followed by doc-level monitors |

#### Workflow Optimization

The workflow execution for bucket-level followed by doc-level monitors has been optimized with:
- New flag `monitor.shouldCreateSingleAlertForFindings` to skip storage of findings/alerts and `publishFinding` calls
- Single alert generation with notification trigger for matching conditions
- Fixed handling of empty `indexExecutionContext.docIds` from bucket-level monitors
- Sorted sequence numbers in descending order for consistent alert generation

## Limitations

- CreateAlertTool requires ChatAgentRunner to pass chat_history (depends on ml-commons issue #2645)
- Visual editor alerts only support navigation to Discover
- Alert insights feature is experimental and not recommended for production use

## References

### Pull Requests

| Version | PR | Repository | Description |
|---------|-----|------------|-------------|
| v2.19.0 | [#456](https://github.com/opensearch-project/skills/pull/456) | skills | Backport CreateAlertTool to 2.x |
| v2.19.0 | [#452](https://github.com/opensearch-project/skills/pull/452) | skills | Support pass prompt to CreateAlertTool |
| v2.19.0 | [#349](https://github.com/opensearch-project/skills/pull/349) | skills | Add CreateAlertTool (original) |
| v2.19.0 | [#392](https://github.com/opensearch-project/dashboards-assistant/pull/392) | dashboards-assistant | Update UI for In-context summarization in Alerts table |
| v2.19.0 | [#368](https://github.com/opensearch-project/dashboards-assistant/pull/368) | dashboards-assistant | Only support visual editor alerts to navigate to Discover |
| v2.19.0 | [#1778](https://github.com/opensearch-project/alerting/pull/1778) | alerting | Force create last run context fix |
| v2.19.0 | [#1780](https://github.com/opensearch-project/alerting/pull/1780) | alerting | Bucket selector aggregation fix |
| v2.19.0 | [#1729](https://github.com/opensearch-project/alerting/pull/1729) | alerting | Workflow execution optimization |

### Documentation

- [Alert Insights](https://docs.opensearch.org/2.19/dashboards/dashboards-assistant/alert-insight/)
- [OpenSearch Assistant](https://docs.opensearch.org/2.19/dashboards/dashboards-assistant/index/)
- [Alerting](https://docs.opensearch.org/2.19/observing-your-data/alerting/index/)
