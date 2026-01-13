---
tags:
  - domain/security
  - component/server
  - indexing
  - security
---
# Security Analytics Detectors

## Summary

OpenSearch v2.17.0 enhances Security Analytics detectors with two key improvements: the Get Detectors API now includes trigger information in its response, and secure REST tests have been added for threat intelligence monitor APIs. These changes improve the usability of the Detector API and strengthen security testing coverage.

## Details

### What's New in v2.17.0

#### Triggers in Get Detectors API Response

The Get Detectors API (`GET /_plugins/_security_analytics/detectors/{detector_id}`) now includes the `triggers` field in its response. This enhancement fixes an issue where Security Analytics would crash when users attempted to create alerts in the Detector Details Page while viewing Findings.

Previously, the API response only included basic detector information. Now it returns complete trigger configuration including:
- Trigger ID, name, and severity
- Detection types (rules, threat_intel)
- Associated rule IDs and tags
- Action configurations with notification templates

#### Secure REST Tests for Threat Intel Monitor APIs

New secure REST integration tests have been added for threat intelligence monitor APIs, ensuring proper access control and security validation. The tests cover:
- Creating threat intel monitors with and without backend roles
- Full access role permissions for monitor creation
- Index-level access control for monitor operations

### Technical Changes

#### API Response Enhancement

The `GetDetectorResponse` class now serializes the triggers field:

```java
.field(Detector.TRIGGERS_FIELD, detector.getTriggers())
```

#### Example API Response

```json
{
    "_id": "akpmM5EB3Y4wm-vZ4JFZ",
    "_version": 1,
    "detector": {
        "name": "detector1",
        "detector_type": "ad_ldap",
        "enabled": true,
        "schedule": {
            "period": {
                "interval": 1,
                "unit": "MINUTES"
            }
        },
        "inputs": [...],
        "last_update_time": "2024-08-08T19:10:59.741Z",
        "enabled_time": "2024-08-08T19:10:59.738Z",
        "threat_intel_enabled": true,
        "triggers": [
            {
                "id": "W0pmM5EB3Y4wm-vZyJGY",
                "name": "Trigger 1",
                "severity": "1",
                "types": ["ad_ldap"],
                "ids": [],
                "sev_levels": [],
                "tags": [],
                "actions": [...],
                "detection_types": ["rules", "threat_intel"]
            }
        ]
    }
}
```

#### New Security Permissions

The secure REST tests added new cluster permissions for threat intelligence:
- `cluster:admin/opensearch/securityanalytics/threatintel/*`
- `cluster:admin/opensearch/securityanalytics/connections/*`

### Usage Example

Retrieve a detector with its triggers:

```bash
GET /_plugins/_security_analytics/detectors/{detector_id}
```

The response now includes the complete trigger configuration, enabling UI components to properly display and manage alert triggers without additional API calls.

## Limitations

- The trigger information is only included when fetching individual detectors, not in bulk search operations
- Trigger actions require proper notification channel configuration

## References

### Documentation
- [Detector APIs Documentation](https://docs.opensearch.org/2.17/security-analytics/api-tools/detector-api/)
- [Creating Detectors](https://docs.opensearch.org/2.17/security-analytics/sec-analytics-config/detectors-config/)
- [About Security Analytics](https://docs.opensearch.org/2.17/security-analytics/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1226](https://github.com/opensearch-project/security-analytics/pull/1226) | Added triggers in getDetectors API response |
| [#1212](https://github.com/opensearch-project/security-analytics/pull/1212) | Secure rest tests for threat intel monitor APIs |

## Related Feature Report

- [Full feature documentation](../../../features/security-analytics/security-analytics-detectors.md)
