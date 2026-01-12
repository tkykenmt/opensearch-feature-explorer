# Rule-based Auto Tagging

## Summary

This release includes bug fixes and improvements for the rule-based auto-tagging feature. Key changes include stricter attribute parameter extraction using a whitelist approach, centralized feature value validation in `RuleValidator`, force refresh after rule creation/update for immediate visibility, and graceful handling of `IndexNotFoundException` during rule synchronization.

## Details

### What's New in v3.2.0

This PR addresses several issues in the rule-based auto-tagging framework:

1. **Stricter Attribute Parameter Extraction**: Changed from exclusion-based to whitelist-based filtering in `RestGetRuleAction`
2. **Centralized Validation**: Moved feature value validation logic into `RuleValidator`
3. **Immediate Rule Visibility**: Added force refresh (`RefreshPolicy.IMMEDIATE`) after rule persistence
4. **Graceful Error Handling**: Added handling for `IndexNotFoundException` during rule sync

### Technical Changes

#### Attribute Parameter Extraction (RestGetRuleAction)

The previous approach filtered out known non-attribute parameters using an exclusion list:

```java
// Before (exclusion-based - could include unintended params)
final Set<String> excludedKeys = Set.of(FEATURE_TYPE, ID_STRING, SEARCH_AFTER_STRING, "pretty");
final List<String> requestParams = request.params().keySet().stream()
    .filter(key -> !excludedKeys.contains(key)).toList();
```

The new approach whitelists only valid attribute names for the given `FeatureType`:

```java
// After (whitelist-based - only valid attributes)
final List<String> attributeParams = request.params()
    .keySet()
    .stream()
    .filter(key -> featureType.getAllowedAttributesRegistry().containsKey(key))
    .toList();
```

This ensures only explicitly defined attributes are parsed and passed for rule filtering.

#### Centralized Feature Value Validation (RuleValidator)

Feature value validation was moved from `CreateRuleRequest.validate()` to `RuleValidator.validateFeatureType()`:

```java
// In RuleValidator.validateFeatureType()
private List<String> validateFeatureType() {
    if (featureType == null) {
        return List.of("Couldn't identify which feature the rule belongs to.");
    }
    try {
        featureType.getFeatureValueValidator().validate(featureValue);
    } catch (Exception e) {
        return List.of(e.getMessage());
    }
    return new ArrayList<>();
}
```

This centralizes validation logic for consistent behavior across different rule APIs.

#### Force Refresh for Immediate Visibility

Added `RefreshPolicy.IMMEDIATE` to rule persistence operations:

```java
// Create rule
IndexRequest indexRequest = new IndexRequest(indexName).id(rule.getId())
    .setRefreshPolicy(WriteRequest.RefreshPolicy.IMMEDIATE)
    .source(rule.toXContent(XContentFactory.jsonBuilder(), ToXContent.EMPTY_PARAMS));

// Update rule
UpdateRequest updateRequest = new UpdateRequest(indexName, ruleId)
    .setRefreshPolicy(WriteRequest.RefreshPolicy.IMMEDIATE)
    .doc(updatedRule.toXContent(XContentFactory.jsonBuilder(), ToXContent.EMPTY_PARAMS));
```

This ensures newly written rules are immediately visible for subsequent read operations.

#### IndexNotFoundException Handling

Added graceful handling when the rules index doesn't exist:

```java
@Override
public void onFailure(Exception e) {
    if (e instanceof IndexNotFoundException) {
        logger.debug("Rule index not found, skipping rule processing.");
        return;
    }
    logger.warn("Failed to get rules from persistence service", e);
}
```

This is expected behavior when no rules have been created yet.

### Usage Example

```bash
# Create a rule - now immediately visible after creation
PUT _rules/workload_group
{
  "description": "Route production logs",
  "index_pattern": ["logs-prod-*"],
  "workload_group": "<workload_group_id>"
}

# Get rules with attribute filter - only valid attributes are processed
GET _rules/workload_group?index_pattern=logs*

# Invalid attributes are now safely ignored
GET _rules/workload_group?index_pattern=logs*&invalid_param=ignored
```

### Migration Notes

- No migration required
- Changes are backward compatible
- Existing rules continue to work without modification

## Limitations

- Force refresh may have minor performance impact on high-frequency rule creation
- Whitelist approach requires attribute registry to be properly configured for each feature type

## References

### Documentation
- [Rule-based Auto-tagging Documentation](https://docs.opensearch.org/3.2/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/autotagging/)
- [Rules API Documentation](https://docs.opensearch.org/3.2/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/rule-lifecycle-api/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#18726](https://github.com/opensearch-project/OpenSearch/pull/18726) | Bug fix and improvements for rule-based auto tagging |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/workload-management.md)
