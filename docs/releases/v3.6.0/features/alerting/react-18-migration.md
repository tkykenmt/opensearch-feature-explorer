---
tags:
  - alerting
---
# React 18 Migration

## Summary

Multiple OpenSearch Dashboards plugins were upgraded from React 16 to React 18 in v3.6.0. This cross-plugin effort addressed breaking API changes introduced in React 18, updated test infrastructure, and resolved CVE-2025-64718 in the index-management-dashboards-plugin. Affected plugins include alerting-dashboards-plugin, anomaly-detection-dashboards-plugin, dashboards-maps, dashboards-search-relevance, index-management-dashboards-plugin, and security-dashboards-plugin.

## Details

### What's New in v3.6.0

The React 18 migration across these plugins follows a consistent pattern of changes:

#### Core Rendering API Migration
All plugins replaced the deprecated `ReactDOM.render()` / `ReactDOM.unmountComponentAtNode()` pattern with the new `createRoot()` API:

```tsx
// Before (React 16)
import ReactDOM from 'react-dom';
ReactDOM.render(<App />, element);
return () => ReactDOM.unmountComponentAtNode(element);

// After (React 18)
import { createRoot } from 'react-dom/client';
const root = createRoot(element);
root.render(<App />);
return () => root.unmount();
```

#### Test Infrastructure Updates
- Replaced `enzyme-adapter-react-16` with `@cfaester/enzyme-adapter-react-18`
- Migrated from `@testing-library/react-hooks` (deprecated) to `@testing-library/react` which now includes `renderHook` and `waitFor` natively
- Replaced `waitForNextUpdate()` pattern with `waitFor(() => expect(...))` for async test assertions
- Updated snapshot tests to reflect React 18 rendering differences (whitespace changes, attribute additions)

#### Plugin-Specific Changes

| Plugin | Key Changes |
|--------|-------------|
| anomaly-detection-dashboards-plugin | Upgraded `react-redux` from v7 to v8; added explicit `children` prop to `PageHeaderProps` interface; migrated 3 app entry points (`anomaly_detection_app.tsx`, `daily_insights_app.tsx`, `forecasting_app.tsx`) |
| security-dashboards-plugin | Incremented version to 3.6.0; migrated `account-app.tsx` rendering; replaced `@testing-library/react-hooks` with `@testing-library/react`; split multitenancy tests into separate file |
| index-management-dashboards-plugin | Upgraded `@types/react` to v18; fixed race conditions in `ShrinkIndex` and `SplitIndex` components where `setState` was read before async operations completed; fixed Cypress tests; resolved CVE-2025-64718 |
| dashboards-maps | Migrated `application.tsx`, `map_embeddable.tsx`, and `create_tooltip.tsx`; updated test files from `react-dom` render to `createRoot`; replaced `react-test-renderer` usage with `@testing-library/react` in some tests |
| dashboards-search-relevance | Migrated `application.tsx`; updated 15+ test files; removed deprecated snapshot-based tests for `search_config` |

### Technical Changes

The migration addresses React 18 breaking changes:

1. `ReactDOM.render` is deprecated — replaced with `createRoot` API across all plugin entry points and embeddable components
2. `React.FC` no longer implicitly includes `children` prop — explicit `children?: React.ReactNode` added where needed (anomaly-detection)
3. `@testing-library/react-hooks` is deprecated — `renderHook` is now exported directly from `@testing-library/react`
4. Stricter batching in React 18 — tests updated to use `waitFor` for async state assertions instead of `waitForNextUpdate`
5. `react-redux` v7 incompatible with React 18 — anomaly-detection upgraded to `react-redux` v8 which uses `useSyncExternalStore`

## Limitations

- The alerting-dashboards-plugin PR (#1369 in the issue) could not be verified via the GitHub API — the PR number may reference a different repository naming convention
- These changes are maintenance/infrastructure updates with no user-facing behavioral changes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [anomaly-detection-dashboards-plugin#1144](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1144) | Upgrade AD plugin to React 18 | — |
| [security-dashboards-plugin#2371](https://github.com/opensearch-project/security-dashboards-plugin/pull/2371) | Increment version to 3.6, upgrade to React 18 and adapt unit tests | [#2365](https://github.com/opensearch-project/security-dashboards-plugin/issues/2365) |
| [dashboards-maps#789](https://github.com/opensearch-project/dashboards-maps/pull/789) | React 18 compatibility updates for dashboards-maps plugin | [#788](https://github.com/opensearch-project/dashboards-maps/issues/788) |
| [dashboards-search-relevance#741](https://github.com/opensearch-project/dashboards-search-relevance/pull/741) | React 18 compatibility updates for dashboards-search-relevance plugin | [#740](https://github.com/opensearch-project/dashboards-search-relevance/issues/740) |
| [index-management-dashboards-plugin#1391](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1391) | Upgrade React from 16 to 18 | [#1384](https://github.com/opensearch-project/index-management-dashboards-plugin/issues/1384), CVE-2025-64718 |
