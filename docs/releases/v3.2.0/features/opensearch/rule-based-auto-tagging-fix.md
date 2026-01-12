---
tags:
  - indexing
---

# Rule-based Auto Tagging Fix

## Summary

This bugfix resolves an issue where delete rule events were not properly consumed for wildcard-based index pattern rules in the `InMemoryRuleProcessingService`. When a rule with a wildcard pattern (e.g., `test-*`) was deleted, the in-memory data structure was not correctly updated because the wildcard character was not stripped during the remove operation.

## Details

### What's New in v3.2.0

This release fixes a bug in the rule-based auto-tagging feature where deleting rules with wildcard index patterns did not properly remove them from the in-memory data structure.

### Technical Changes

#### Bug Description

The rule-based auto-tagging feature stores rules in an in-memory trie data structure for efficient pattern matching. When adding a rule, the wildcard character (`*`) is stripped from the pattern before storing (e.g., `test-*` becomes `test-`). However, the remove operation was not applying the same transformation, causing delete events for wildcard-based rules to fail silently.

#### Root Cause

In `InMemoryRuleProcessingService.removeOperation()`, the code was calling:
```java
valueStore.remove(value);
```

This did not strip the wildcard, so when trying to remove `test-*`, it looked for a key that didn't exist in the trie (since it was stored as `test-`).

#### Fix Applied

The fix ensures the wildcard is stripped during removal, matching the behavior of the add operation:

```java
// Before (broken)
valueStore.remove(value);

// After (fixed)
valueStore.remove(value.replace(WILDCARD, ""));
```

#### Code Change

```java
private void removeOperation(Map.Entry<Attribute, Set<String>> attributeEntry, Rule rule) {
    AttributeValueStore<String, String> valueStore = 
        attributeValueStoreFactory.getAttributeValueStore(attributeEntry.getKey());
    for (String value : attributeEntry.getValue()) {
        valueStore.remove(value.replace(WILDCARD, ""), rule.getFeatureValue());
    }
}
```

### Usage Example

```bash
# Create a rule with wildcard pattern
PUT _rules/workload_group
{
  "description": "Route test indexes",
  "index_pattern": ["test-*"],
  "workload_group": "<workload_group_id>"
}

# Delete the rule - now correctly removes from in-memory store
DELETE _rules/workload_group/<rule_id>

# Subsequent searches to test-* indexes will no longer be auto-tagged
# (previously, the rule would remain in memory until node restart)
```

### Migration Notes

- No migration required
- The fix is automatically applied after upgrading to v3.2.0
- Existing rules with wildcard patterns will be correctly handled on delete

## Limitations

- This fix only affects the delete operation for wildcard-based rules
- Rules without wildcards were not affected by this bug

## References

### Documentation
- [Rule Lifecycle API Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/rule-lifecycle-api/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#18628](https://github.com/opensearch-project/OpenSearch/pull/18628) | Fix delete rule event consumption for wildcard index based rules |

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/workload-management.md)
