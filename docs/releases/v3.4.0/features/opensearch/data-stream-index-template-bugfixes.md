---
tags:
  - domain/core
  - component/server
  - indexing
  - performance
---
# Data Stream & Index Template Bugfixes

## Summary

This release fixes a bug where unused index templates matching a data stream pattern could not be deleted when a higher-priority template was actually being used by the data stream. Previously, OpenSearch incorrectly reported that lower-priority templates were "in use" even though they weren't the active template for any data stream.

## Details

### What's New in v3.4.0

Fixed the deletion logic for composable index templates to correctly identify which template is actually being used by a data stream based on priority.

### Technical Changes

#### Problem Description

When multiple index templates match a data stream's name pattern:
1. OpenSearch uses the template with the **highest priority** for the data stream
2. Lower-priority templates that also match the pattern are **not used**
3. Before this fix, attempting to delete unused lower-priority templates failed with:
   ```
   unable to remove composable templates [template-name] as they are in use by a data streams [stream-name]
   ```

#### Root Cause

The `dataStreamsUsingTemplate()` method in `MetadataIndexTemplateService` only checked if a template's index pattern matched a data stream name, without verifying if that template was actually the highest-priority template being used.

#### Fix Implementation

The fix modifies two key methods in `MetadataIndexTemplateService.java`:

1. **`dataStreamsUsingTemplate()`**: Now calls `findV2Template()` to verify the template is actually the highest-priority match before reporting it as "in use"

2. **`findV2Template()`**: Optimized to track the winner during iteration instead of collecting all matches and sorting afterward

```java
// Before: Only checked pattern match
dataStreams.stream()
    .filter(stream -> Regex.simpleMatch(indexPattern, stream))
    .forEach(matches::add);

// After: Verifies template is actually used
dataStreams.stream()
    .filter(stream -> Regex.simpleMatch(indexPattern, stream))
    .filter(stream -> {
        final String usingTemplate = findV2Template(state.metadata(), stream, false);
        return templateName.equals(usingTemplate);
    })
    .forEach(matches::add);
```

### Usage Example

```json
// Create two templates with different priorities
PUT _index_template/test
{
  "index_patterns": ["test*"],
  "data_stream": {},
  "priority": 50
}

PUT _index_template/test-data-stream
{
  "index_patterns": ["test"],
  "data_stream": {},
  "priority": 51
}

// Create data stream (uses test-data-stream due to higher priority)
PUT _data_stream/test

// Now you can delete the unused lower-priority template
DELETE _index_template/test
// Success! (Previously failed with "in use" error)
```

### Migration Notes

No migration required. This is a bugfix that enables previously blocked operations.

## Limitations

- The fix only applies to composable index templates (v2 templates)
- Legacy index templates are not affected by this change

## References

### Documentation
- [Data Streams Documentation](https://docs.opensearch.org/3.0/im-plugin/data-streams/): Official docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#20102](https://github.com/opensearch-project/OpenSearch/pull/20102) | Fix deletion failure of unused index template matching data stream |

### Issues (Design / RFC)
- [Issue #20078](https://github.com/opensearch-project/OpenSearch/issues/20078): Original bug report
- [Issue #9194](https://github.com/opensearch-project/OpenSearch/issues/9194): Related earlier fix for non-data-stream templates

## Related Feature Report

- Full feature documentation
