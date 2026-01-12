---
tags:
  - dashboards
  - search
---

# Dashboards Core Bugfixes

## Summary

This release fixes unit test failures in the OpenSearch Dashboards Assistant plugin caused by missing Web Worker support in the Jest test environment. The fix ensures that tests for the NLQ (Natural Language Query) visualization embeddable component run successfully.

## Details

### What's New in v3.2.0

This bugfix addresses test infrastructure issues that were causing unit tests to fail when running in Jest's jsdom environment.

### Technical Changes

#### Problem

Unit tests for the `NLQVisualizationEmbeddableFactory` component were failing because:
1. The `react-monaco-editor` component requires Web Worker support
2. Jest's jsdom environment does not provide a native `Worker` implementation
3. The Monaco editor (used for code/query editing) relies on Web Workers for syntax highlighting and language services

#### Solution

The fix adds two changes to the test setup:

1. **Global Worker Mock** (`test/setupTests.ts`):
   ```typescript
   // @ts-ignore
   window.Worker = function () {};
   ```
   This provides a no-op Worker constructor globally for all tests.

2. **Monaco Editor Mock** (`nlq_vis_embeddable_factory.test.ts`):
   ```typescript
   jest.mock('react-monaco-editor', () => () => null);
   ```
   This mocks the Monaco editor component to return null, avoiding Worker-related errors.

#### Files Changed

| File | Change |
|------|--------|
| `test/setupTests.ts` | Added fake Worker constructor |
| `public/components/visualization/embeddable/nlq_vis_embeddable_factory.test.ts` | Added Monaco editor mock |
| `CHANGELOG.md` | Added changelog entry |

### Usage Example

No user-facing changes. This fix only affects the development and CI/CD test environment.

## Limitations

- The Worker mock is a no-op implementation and does not provide actual Web Worker functionality
- Tests that rely on real Worker behavior would need additional mocking

## References

### Documentation
- [PR #593](https://github.com/opensearch-project/dashboards-assistant/pull/593): Main implementation
- [OpenSearch Dashboards Assistant](https://github.com/opensearch-project/dashboards-assistant): Repository

### Pull Requests
| PR | Description |
|----|-------------|
| [#593](https://github.com/opensearch-project/dashboards-assistant/pull/593) | Fix failed unit tests due to missing Worker |

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-assistant/dashboards-core-bugfixes.md)
