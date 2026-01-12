# Common Utils Enhancements

## Summary

OpenSearch v3.3.0 includes two enhancements to the common-utils library: improved user attributes XContent parsing logic and an updated GitHub workflow for automatic branch cleanup. The XContent parsing change fixes compatibility issues with downstream plugins by using the existing `custom_attribute_names` field format instead of introducing a new `custom_attributes` property.

## Details

### What's New in v3.3.0

#### User Attributes XContent Parsing Logic Update

PR #878 updates how user custom attributes are serialized and parsed in XContent format. A previous change (#827) introduced a `custom_attributes` property that caused compatibility issues with downstream plugins that had existing mappings expecting only `custom_attribute_names`.

**Key Changes:**
- Custom attributes are now written to `custom_attribute_names` in `key=value` format
- Removed the `custom_attributes` property from XContent serialization
- Updated `User.parse()` to parse `custom_attribute_names` entries as `key=value` pairs
- Added validation that throws `IllegalArgumentException` for malformed entries

**Before (PR #827):**
```json
{
  "name": "user1",
  "custom_attributes": {
    "attr1": "value1"
  },
  "custom_attribute_names": ["attr1"]
}
```

**After (PR #878):**
```json
{
  "name": "user1",
  "custom_attribute_names": ["attr1=value1"]
}
```

This change maintains backward compatibility with existing system index mappings in plugins like Alerting, Anomaly Detection, Index Management, and Security Analytics.

#### Delete Backport Branch Workflow Update

PR #860 enhances the GitHub Actions workflow that automatically deletes merged branches:

- Extended branch cleanup to include `release-chores/` branches in addition to `backport/` branches
- Migrated from `SvanBoxel/delete-merged-branch` action to `actions/github-script@v7`
- Added explicit `contents: write` permission for the workflow

```yaml
if: startsWith(github.event.pull_request.head.ref,'backport/') || startsWith(github.event.pull_request.head.ref,'release-chores/')
```

### Technical Changes

#### Modified Files

| File | Change |
|------|--------|
| `src/main/java/org/opensearch/commons/authuser/User.java` | Updated `toXContent()` and `parse()` methods for custom attributes |
| `src/test/java/org/opensearch/commons/authuser/UserTest.java` | Added tests for new parsing logic |
| `.github/workflows/delete_backport_branch.yml` | Extended branch patterns and updated action |

#### API Changes

The `User` class methods were updated:

```java
// User.toXContent() now writes attributes as key=value
public XContentBuilder toXContent(XContentBuilder builder, Params params) {
    // Writes custom_attribute_names as ["key1=value1", "key2=value2"]
}

// User.parse() now parses key=value format
public static User parse(XContentParser parser) {
    // Parses custom_attribute_names entries and splits on '='
    // Throws IllegalArgumentException if format is invalid
}
```

### Migration Notes

Downstream plugins with tests that create mock `User` objects with `custom_attribute_names` must update to use the `key=value` format:

```java
// Before
List<String> customAttributeNames = List.of("attr1", "attr2");

// After
List<String> customAttributeNames = List.of("attr1=value1", "attr2=value2");
```

## Limitations

- The `custom_attribute_names` field name is retained for backward compatibility, even though it now contains both names and values
- Plugins must update their test fixtures to use the new `key=value` format

## References

### Documentation
- [PR #827](https://github.com/opensearch-project/common-utils/pull/827): Original custom attributes implementation
- [PR #1236](https://github.com/opensearch-project/flow-framework/pull/1236): Flow Framework test fix for new format
- [PR #1583](https://github.com/opensearch-project/security-analytics/pull/1583): Security Analytics test fix

### Pull Requests
| PR | Description |
|----|-------------|
| [#878](https://github.com/opensearch-project/common-utils/pull/878) | Update user attributes XContent parsing logic |
| [#860](https://github.com/opensearch-project/common-utils/pull/860) | Update delete_backport_branch workflow to include release-chores branches |

### Issues (Design / RFC)
- [Issue #1829](https://github.com/opensearch-project/alerting/issues/1829): Related Alerting issue for custom attributes

## Related Feature Report

- [Full feature documentation](../../../../features/common-utils/common-utils.md)
