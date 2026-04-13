---
tags:
  - security-analytics
---
# Security Analytics Bug Fixes

## Summary

OpenSearch v3.6.0 includes several bug fixes for Security Analytics across both the backend plugin and the dashboards plugin. These fixes address detector deletion failures, UI display issues in the findings and alerts tables, detector creation error handling, and CVE remediations in the security-analytics-commons dependency.

## Bug Fixes

### Backend Plugin (security-analytics)

#### Fix Detector Deletion with Empty Monitor ID List

The DeleteDetector API was failing with a `groupSize must be greater than 0 but was 0` error when attempting to delete a detector that had no associated rules (and therefore no monitors). The `monitor_id` attribute becomes an empty array when a detector is edited to have 0 rules. The fix adds a check to skip monitor deletion API calls when the monitor IDs list is empty.

- Affected class: `TransportDeleteDetectorAction`
- Root cause: `GroupedActionListener` requires a non-zero group size, but was being passed an empty monitor ID list

#### CVE-2025-67735 Remediation

Updated the security-analytics-commons JAR to address CVE-2025-67735. The CVE was resolved in the security-analytics-commons package via `opensearch-project/security-analytics-commons/pull/30`.

#### CVE-2026-33871 and CVE-2026-33870 Remediation

Updated the security-analytics-commons JAR to address CVE-2026-33871 and CVE-2026-33870. The fixes were applied in the security-analytics-commons package via `opensearch-project/security-analytics-commons/pull/33`.

### Dashboards Plugin (security-analytics-dashboards-plugin)

#### Fix Empty Severity Column in Findings Table

The severity column in the findings table was displaying `-` instead of the actual severity value. This bug was specific to 3.x versions and resulted from the removal of visualization assets in 3.x. The functions previously used to prepare visualizations were also pulling the information needed to populate the severity column.

#### Fix Empty Alerts Table

The detection rule alerts table was empty because state was not being updated with the retrieved alerts before the `filterDeletectionRuleAlerts` function call. The fix changes the function signature to accept alerts as a parameter instead of reading from state.

#### Fix Detector Creation Failure Propagation

Detector creation failures were not being propagated to the user via error toast notifications. Instead, the UI would silently redirect to a blank detector details page. The fix adds proper error checking after the create detector API call and displays an error toast when creation fails.

#### Fix Blank Details Page After Successful Creation

After successful detector creation, the UI was redirecting to a blank details page using a `PENDING_DETECTOR_ID` placeholder instead of the actual detector ID from the API response. The fix uses `createDetectorRes.response._id` for the redirect URL.

#### Fix Silent Failures in Error Handling

The `errorNotificationToast` utility was calling `toLowerCase()` on the error message, which would fail silently when the error message was not a string. The fix uses `JSON.stringify()` before calling `toLowerCase()` to handle non-string error objects.

## References

### Pull Requests
| PR | Title | Repository |
|----|-------|------------|
| `https://github.com/opensearch-project/security-analytics/pull/1648` | Fix bug when deleting detector with 0 rules | security-analytics |
| `https://github.com/opensearch-project/security-analytics/pull/1653` | Update security-analytics-commons jar (CVE-2025-67735) | security-analytics |
| `https://github.com/opensearch-project/security-analytics/pull/1685` | Update security-analytics-commons jar (CVE-2026-33871, CVE-2026-33870) | security-analytics |
| `https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1376` | Fix empty alerts table, detector creation failure propagation, blank details page, silent failures | security-analytics-dashboards-plugin |
| `https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1392` | Fix empty severity column in findings table | security-analytics-dashboards-plugin |
