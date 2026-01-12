---
tags:
  - dashboards
  - indexing
---

# Testing Library Updates

## Summary

This bugfix updates the `@testing-library/user-event` dependency from version 12.x/13.x to version 14.4.3 across multiple OpenSearch Dashboards plugins. The update addresses compatibility issues and aligns the testing infrastructure with the latest testing library best practices, requiring test code modifications to use the new async API pattern.

## Details

### What's New in v3.1.0

The `@testing-library/user-event` library was updated to version 14.4.3 in two dashboards plugins:
- **anomaly-detection-dashboards-plugin**: Updated from `^12.1.6` to `^14.4.3`
- **index-management-dashboards-plugin**: Updated from `^13.1.9` to `^14.4.3`

### Technical Changes

#### API Changes

The major version upgrade (v12/v13 → v14) introduces breaking changes in how user events are simulated:

| Aspect | Old API (v12/v13) | New API (v14) |
|--------|-------------------|---------------|
| Setup | Direct import and use | Requires `userEvent.setup()` |
| Method calls | Synchronous: `userEvent.click(element)` | Asynchronous: `await user.click(element)` |
| Import pattern | `import userEvent from '@testing-library/user-event'` | `import userEventModule from '@testing-library/user-event'` |

#### Migration Pattern

```typescript
// Before (v12/v13)
import userEvent from '@testing-library/user-event';

test('example test', () => {
  userEvent.click(button);
  userEvent.type(input, 'text');
});

// After (v14)
import userEventModule from '@testing-library/user-event';

describe('test suite', () => {
  const userEvent = userEventModule.setup();
  
  test('example test', async () => {
    await userEvent.click(button);
    await userEvent.type(input, 'text');
  });
});
```

#### Files Modified

**anomaly-detection-dashboards-plugin** (PR #1042):
- `package.json` - Dependency version update
- `yarn.lock` - Lock file update
- Multiple test files updated to use async API pattern

**index-management-dashboards-plugin** (PR #1321):
- `package.json` - Dependency version update
- `.github/actions/run-cypress-tests/action.yaml` - Updated `actions/setup-java` from v1 to v4
- `.github/workflows/verify-binary-installation.yml` - Updated OpenSearch version to 3.1.0
- 30+ test files updated to use async API pattern

### Additional Changes

The index-management-dashboards-plugin PR also included:
- GitHub Actions workflow updates for Java setup
- OpenSearch version bump in CI workflows from `3.0.0-beta1` to `3.1.0`

## Limitations

- Tests must be updated to use async/await pattern when calling user event methods
- The `userEvent.setup()` call should be placed at the describe block level for optimal performance

## References

### Documentation
- [@testing-library/user-event v14 Migration Guide](https://testing-library.com/docs/user-event/intro)
- [GitHub: @testing-library/user-event](https://github.com/testing-library/user-event)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1042](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1042) | anomaly-detection-dashboards-plugin | Update testing-library/user-event dependency |
| [#1321](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1321) | index-management-dashboards-plugin | Updated @testing-library/user-event dependency |

## Related Feature Report

- [Full feature documentation](../../../../features/multi-plugin/testing-library-updates.md)
