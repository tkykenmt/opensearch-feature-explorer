---
tags:
  - dashboards-flow-framework
---
# Dashboards ML Agents

## Summary

OpenSearch v3.5.0 promotes the ML Agents configuration UI in AI Search Flows from experimental to production-ready status. The update removes experimental badges and improves form field labels for better clarity when configuring agents.

## Details

### What's New in v3.5.0

#### Production-Ready Status

The agentic search configuration UI is now considered production-ready:
- Removed "EXPERIMENTAL" badge from the workflow card on the new workflow page
- Removed "EXPERIMENTAL" badge from the "Configure Agent" panel header on the details page

#### Improved Form Labels

Form field labels have been updated for better clarity:

| Previous Label | New Label | Location |
|----------------|-----------|----------|
| Model | Large language model | Agent LLM fields, Query Planning Tool |
| LLM Interface | LLM interface | Agent Advanced Settings |

The "Large language model" label disambiguates the LLM selection from other model types (e.g., embedding models) used in the workflow.

### Technical Changes

Files modified:
- `configure_flow.tsx`: Removed `EuiBetaBadge` import and experimental badge from Configure Agent panel
- `use_case.tsx`: Simplified card title by removing experimental badge wrapper
- `agent_llm_fields.tsx`: Changed "Model" label to "Large language model"
- `query_planning_tool.tsx`: Changed "Model" label to "Large language model"
- `agent_advanced_settings.tsx`: Fixed capitalization "LLM Interface" → "LLM interface"

## Limitations

- No functional changes; this is a UI polish release
- Agent configuration capabilities remain the same as v3.4.0

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#832](https://github.com/opensearch-project/dashboards-flow-framework/pull/832) | Remove experimental badging | |
| [#836](https://github.com/opensearch-project/dashboards-flow-framework/pull/836) | Update agent form field titles | |
