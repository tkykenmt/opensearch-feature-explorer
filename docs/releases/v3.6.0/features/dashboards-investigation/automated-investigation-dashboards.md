---
tags:
  - dashboards-investigation
---
# Automated Investigation (Dashboards)

## Summary

OpenSearch v3.6.0 brings significant enhancements to the Automated Investigation plugin for OpenSearch Dashboards. This release adds hypothesis acceptance workflows, duration tracking for investigations, comprehensive telemetry metrics, improved error handling, and multiple UX refinements. The changes span 15 PRs covering new features, enhancements, and bug fixes.

## Details

### What's New in v3.6.0

#### Accept Hypothesis Feature
Users can now explicitly accept a hypothesis during an investigation, providing a clear resolution workflow. This adds an "accept" action alongside the existing "rule out" and "replace primary" hypothesis actions.

#### Duration Tracking
Duration tracking has been added at three levels of granularity:
- **Investigation level**: Total time from start to completion
- **Step level**: Time taken for each investigation step
- **Sub-step level**: Time for individual sub-steps within a step

Duration is calculated from `create_time` to `updated_time` of agentic messages, providing better audit and performance visibility.

#### Comprehensive Telemetry Metrics
A full telemetry system has been integrated using the core `PluginTelemetryRecorder`. Events tracked include:

| Category | Events |
|----------|--------|
| Investigation lifecycle | `investigation_success`, `investigation_failure`, `investigation_reinvestigate` |
| Duration metric | `investigation_duration` (milliseconds) |
| Investigation steps | `investigation_steps_expand`, `investigation_steps_explain`, `reinvestigate_click` |
| Feedback | `investigation_thumb_up`, `investigation_thumb_down` |
| Hypothesis actions | `hypothesis_click`, `hypothesis_replace_primary`, `hypothesis_rule_out`, `hypothesis_rule_in`, `hypothesis_accept` |
| Finding actions | `finding_confirm`, `finding_reject`, `finding_undo_feedback`, `finding_thumb_up`, `finding_thumb_down`, `finding_undo_mark` |

Each event includes contextual data such as `notebookId`, `hypothesisId`, `findingId`, and `durationMs` where applicable.

#### Visualization Summary Image Size Limit
A max length limit has been added for visualization summary images to prevent oversized payloads when generating visualization summaries via the ML agent.

#### Log Analysis Rerun During Reinvestigation
Log analysis can now be rerun during reinvestigation, allowing users to get fresh log analysis results when reinvestigating with updated parameters.

### UX Enhancements

- **Tool result style alignment**: Investigation tool result styling updated to align with the chat interface; path removed from tool results to prevent LLM from generating links
- **Absolute time in reinvestigation**: The reinvestigation time picker now shows absolute time instead of relative time, and the modal has been enlarged for full text display
- **Investigation detail card wording**: Updated wording on investigation detail cards for clarity; fixed missing workspace in investigation URLs
- **Summary agent timeout**: Increased from default to 60 seconds with retries disabled (`maxRetries: 0`) to accommodate long-running visualization summary generation
- **Polling retry count**: Increased polling retry count for trace and step operations to handle longer-running investigations
- **PPL query validation**: Switched to `/_plugins/_ppl/_explain` API for lightweight syntax validation instead of executing queries; added centralized `extractErrorMessage` utility for consistent error handling across PPL/SQL errors, HTTP client errors, and standard errors
- **Investigation steps style**: Fixed styling in `hypotheses_step.tsx` and `message_trace_flyout.tsx`

### Bug Fixes

- **Hypothesis detail buttons placement**: Fixed misaligned buttons in the hypothesis detail view
- **Duplicate confirm/reject buttons**: Removed duplicate confirm/reject buttons that appeared on findings
- **Wrong datasource ID from chat**: Fixed incorrect `datasourceId` being passed from the chat tool executor to the investigation plugin
- **Chat integration type conflict**: Fixed a type conflict where `chat` from `depsStart` was overriding the `chat` instance from `coreStart` in `NoteBookServices`; removed unnecessary `any` cast and fixed `chatConetxt` → `chatContext` typo

## Limitations

- Telemetry events are client-side only; no server-side aggregation dashboard is provided out of the box
- The 60-second summary agent timeout is a fixed value and not configurable

## References

### Pull Requests
| PR | Description | Category |
|----|-------------|----------|
| `https://github.com/opensearch-project/dashboards-investigation/pull/321` | Add accept hypothesis feature | feature |
| `https://github.com/opensearch-project/dashboards-investigation/pull/320` | Add duration tracking for investigations, steps, and sub-steps | feature |
| `https://github.com/opensearch-project/dashboards-investigation/pull/342` | Add comprehensive telemetry metrics for investigation actions | feature |
| `https://github.com/opensearch-project/dashboards-investigation/pull/326` | Add max length limit for visualization summary image size | feature |
| `https://github.com/opensearch-project/dashboards-investigation/pull/322` | Allow log analysis to rerun during reinvestigation | feature |
| `https://github.com/opensearch-project/dashboards-investigation/pull/319` | Update investigation tool result style to align with chat | enhancement |
| `https://github.com/opensearch-project/dashboards-investigation/pull/318` | Show absolute time in reinvestigation time picker | enhancement |
| `https://github.com/opensearch-project/dashboards-investigation/pull/338` | Update wording of investigation detail card and fix missing workspace in URL | enhancement |
| `https://github.com/opensearch-project/dashboards-investigation/pull/334` | Increase summary agent timeout to 60s and enhance error handling | enhancement |
| `https://github.com/opensearch-project/dashboards-investigation/pull/327` | Increase polling retry count for trace and step | enhancement |
| `https://github.com/opensearch-project/dashboards-investigation/pull/335` | Improve error handling for invalid PPL queries and fix investigation steps style | enhancement |
| `https://github.com/opensearch-project/dashboards-investigation/pull/339` | Fix hypothesis detail buttons placement | bugfix |
| `https://github.com/opensearch-project/dashboards-investigation/pull/325` | Remove duplicate confirm/reject buttons on finding | bugfix |
| `https://github.com/opensearch-project/dashboards-investigation/pull/337` | Fix wrong datasource ID being passed from chat | bugfix |
| `https://github.com/opensearch-project/dashboards-investigation/pull/329` | Fix chat integration type conflict | bugfix |
