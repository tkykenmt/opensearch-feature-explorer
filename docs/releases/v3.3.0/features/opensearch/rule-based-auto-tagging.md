# Rule-based Auto-tagging

## Summary

v3.3.0 enhances rule-based auto-tagging for Workload Management (WLM) with security attribute support (username and role), multi-attribute label resolving logic, improved in-memory trie structure, and comprehensive integration tests. These changes enable more granular and flexible automatic workload group assignment based on index patterns combined with user identity.

## Details

### What's New in v3.3.0

- **Security Attributes Support**: Rules can now match on `principal.username` and `principal.role` in addition to `index_pattern`
- **Multi-attribute Label Resolution**: New algorithm evaluates multiple attributes with priority-based scoring
- **In-memory Trie Restructure**: Trie values now stored as sets to support multiple labels per attribute key
- **Nested Attribute Filtering**: GET API supports filtering by nested attributes like `principal.username`
- **Integration Tests**: Comprehensive test coverage for auto-tagging scenarios
- **Bug Fixes**: Improved Update Rule API handling for multiple attributes

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Request Processing"
        REQ[Search Request] --> AF[WlmActionFilter]
        AF --> AE[AttributeExtractors]
    end
    
    subgraph "Attribute Extraction"
        AE --> IPE[IndexPatternExtractor]
        AE --> UE[UsernameExtractor]
        AE --> RE[RoleExtractor]
    end
    
    subgraph "Label Resolution"
        IPE --> FVR[FeatureValueResolver]
        UE --> FVR
        RE --> FVR
        FVR --> FVC[FeatureValueCollector]
        FVC --> TRIE[In-Memory Tries]
    end
    
    subgraph "Storage"
        RULES[.wlm_rules System Index] -->|Periodic Sync| TRIE
    end
    
    FVR -->|Resolved Label| WG[Workload Group Assignment]
```

#### New Components

| Component | Description |
|-----------|-------------|
| `FeatureValueResolver` | Central class for evaluating candidate labels across multiple attributes |
| `FeatureValueCollector` | Extracts and merges values for single attributes with OR/AND logic |
| `AttributeExtractor<String>` | Interface for extracting attribute values from requests |
| `PrincipalAttribute` | Schema for security attributes (username, role) |

#### Rule Schema Update

```json
{
  "_id": "rule-uuid",
  "description": "Production analytics rule",
  "index_pattern": ["logs-prod-*"],
  "principal": {
    "username": ["admin", "analyst"],
    "role": ["all_access"]
  },
  "workload_group": "production_workload_id",
  "updated_at": "2025-09-25T16:28:50Z"
}
```

### Usage Example

**Create Rule with Security Attributes:**
```json
PUT _rules/workload_group
{
  "description": "Admin analytics rule",
  "index_pattern": ["logs-*"],
  "principal": {
    "username": ["admin"],
    "role": ["all_access"]
  },
  "workload_group": "admin_workload_id"
}
```

**Filter Rules by Nested Attributes:**
```
GET _rules/workload_group?principal.username=admin&principal.role=all_access
```

### Label Resolution Algorithm

When multiple rules match a request, the system uses priority-based scoring:

1. Attributes are sorted by priority (username > role > index_pattern)
2. Each attribute contributes a match score (1.0 for exact match, 0.0 for unspecified)
3. Candidate labels are intersected across attributes (AND logic)
4. The rule with the highest combined score wins

### Migration Notes

- Existing rules using only `index_pattern` continue to work unchanged
- New `principal` attribute is optional for backward compatibility
- Rules with security attributes require the Security plugin for username/role extraction

## Limitations

- Security attributes require the OpenSearch Security plugin to be installed
- Maximum 10 values per attribute (e.g., 10 index patterns per rule)
- Index pattern values limited to 100 characters
- Principal attributes only available when security context is present

## Related PRs

| PR | Description |
|----|-------------|
| [#19486](https://github.com/opensearch-project/OpenSearch/pull/19486) | Add autotagging label resolving logic for multiple attributes |
| [#19497](https://github.com/opensearch-project/OpenSearch/pull/19497) | Bug fix on Update Rule API with multiple attributes |
| [#19429](https://github.com/opensearch-project/OpenSearch/pull/19429) | Modify get rule API to suit nested attributes |
| [#19345](https://github.com/opensearch-project/OpenSearch/pull/19345) | Add schema for security attributes (principal.username, principal.role) |
| [#19344](https://github.com/opensearch-project/OpenSearch/pull/19344) | Restructure in-memory trie to store values as a set |
| [#18550](https://github.com/opensearch-project/OpenSearch/pull/18550) | Add autotagging rule integration tests |

## References

- [Issue #16797](https://github.com/opensearch-project/OpenSearch/issues/16797): RFC for automated labeling of search requests
- [Rule-based Auto-tagging Documentation](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/autotagging/)
- [Rules API Documentation](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/rule-lifecycle-api/)

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/workload-management.md)
