# Neural Search Bug Fixes

## Summary

This release includes bug fixes and infrastructure improvements for the Neural Search plugin in OpenSearch v3.3.0. The fixes address nested list ordering issues in embedding processors, enable mocking of final classes in unit tests, and improve CI stability by cleaning up disk space for BWC tests.

## Details

### What's New in v3.3.0

Three key improvements were made to the Neural Search plugin:

1. **Nested List Order Fix**: Fixed a bug where nested lists had their element order reversed when processed by embedding processors
2. **Unit Test Enhancement**: Enabled mocking of final classes and static functions using Mockito inline mock maker
3. **CI Disk Space Cleanup**: Added a GitHub Action to clean up disk space before BWC tests to prevent disk circuit breaker failures

### Technical Changes

#### Nested List Order Bug Fix

The `ProcessorDocumentUtils.handleList()` method was using a stack-based approach that inadvertently reversed the order of nested list elements. For example, `[[1, 2, 3], [4, 5, 6]]` was being transformed to `[[3, 2, 1], [6, 5, 4]]`.

The fix iterates through nested lists in reverse order when pushing to the stack, ensuring the original order is preserved when elements are popped.

```java
// Before (buggy)
for (Object listItem : (List<Object>) value) {
    stack.push(new ProcessJsonListItem(listItem, nestedList));
}

// After (fixed)
List<Object> listValue = (List<Object>) value;
for (int i = listValue.size() - 1; i >= 0; i--) {
    stack.push(new ProcessJsonListItem(listValue.get(i), nestedList));
}
```

#### Unit Test Infrastructure Enhancement

Added support for mocking final classes and static functions by:

1. Adding `mock-maker-inline` configuration file
2. Adding ByteBuddy and Objenesis dependencies
3. Enabling `jdk.attach.allowAttachSelf` system property
4. Updating affected tests to work with inline mock maker

| Dependency | Purpose |
|------------|---------|
| byte-buddy | Runtime code generation for mocking |
| byte-buddy-agent | Java agent for class transformation |
| objenesis | Object instantiation without constructors |

#### CI Disk Space Cleanup Action

Created a reusable GitHub Action (`.github/actions/clean-up-disk/action.yml`) that removes:

| Item | Space Freed |
|------|-------------|
| CodeQL | ~2-3 GB |
| Go installation | ~1 GB |
| Python installation | ~500 MB |
| GCC/libexec | ~500 MB |

This action is applied to BWC test workflows to prevent ml-commons disk circuit breaker from triggering due to insufficient disk space (requires 5GB free).

### Usage Example

The nested list fix ensures embedding processors correctly preserve list order:

```json
// Input document
{
  "coordinates": [[1, 2, 3], [4, 5, 6]]
}

// After text_embedding processor (v3.3.0+)
{
  "coordinates": [[1, 2, 3], [4, 5, 6]],
  "embedding": [0.1, 0.2, ...]
}
```

### Migration Notes

No migration required. These are internal bug fixes and infrastructure improvements.

## Limitations

- The mock-maker-inline feature requires Java 9+ and may have performance overhead in tests
- CI disk cleanup action is specific to GitHub Actions runners

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#1570](https://github.com/opensearch-project/neural-search/pull/1570) | Fix reversed order of values in nested list with embedding processor |
| [#1528](https://github.com/opensearch-project/neural-search/pull/1528) | Enable mocking of final classes and static functions |
| [#1584](https://github.com/opensearch-project/neural-search/pull/1584) | Add CI action to clean up disk and apply to BWC |

### Issues (Design / RFC)
- [Issue #1569](https://github.com/opensearch-project/neural-search/issues/1569): ProcessorDocumentUtils.handleList messes up the order of nested lists
- [Issue #1582](https://github.com/opensearch-project/neural-search/issues/1582): Normalization Processor's BWC tests are failing
- [Issue #1583](https://github.com/opensearch-project/neural-search/issues/1583): Disable ml-commons circuit breaker in bwc tests

## Related Feature Report

- [Full feature documentation](../../../../features/neural-search/neural-search-bug-fixes.md)
