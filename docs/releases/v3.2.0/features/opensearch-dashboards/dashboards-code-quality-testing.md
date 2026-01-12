# Dashboards Code Quality & Testing

## Summary

OpenSearch Dashboards v3.2.0 includes significant improvements to code quality, testing infrastructure, and development guidelines. This release introduces comprehensive testing and development documentation, replaces the TypeScript error baseline with inline `@ts-expect-error` comments, adds extensive Cypress tests for the Explore feature, and refactors components for better maintainability.

## Details

### What's New in v3.2.0

This release focuses on improving developer experience and code quality through:

1. **Testing & Development Guidelines**: New documentation establishing standards for unit tests, integration tests, functional tests (Selenium/Cypress), performance tests, and linting/type error handling.

2. **TypeScript Error Handling Improvement**: Migration from `ts_error_baseline` to inline `// @ts-expect-error` comments, reducing maintenance overhead and improving IDE error visibility.

3. **Explore Feature Testing**: Comprehensive Cypress test coverage for the new Explore feature including autocomplete, visualization rules, saved queries, AI mode, and filter actions.

4. **Component Refactoring**: Page components split into smaller container components for better maintainability.

### Technical Changes

#### Development Guidelines

| Area | Description |
|------|-------------|
| Unit Tests | Standards for `yarn test:jest` |
| Integration Tests | Standards for `yarn test:jest_integration` |
| Functional Tests | Cypress and Selenium test requirements |
| Type Checking | `// @ts-expect-error` for known TypeScript errors |
| Code Coverage | Codecov status check enforcement |

#### TypeScript Error Handling

The new approach replaces the centralized baseline file with inline comments:

```typescript
// Before: ts_error_baseline file tracked all errors
// After: Inline comments mark expected errors

// @ts-expect-error TS2345 TODO(ts-error): fixme
someFunction(incorrectType);
```

Benefits:
- Reduced maintenance when error lines shift
- Clear IDE indication of expected vs. new errors
- Workspace diagnostics show only new errors
- No risk of accidentally ignoring new errors during baseline updates

#### New Cypress Tests

| Test Suite | Coverage |
|------------|----------|
| Default Visualization Rules | Line chart, bar chart, heatmap, scatterpoint, metric |
| Autocomplete Experience | New autocomplete in Explore |
| Recent Query | Re-enabled tests for Explore |
| AI Mode | Cypress tests for AI mode |
| Filter Actions | Filter In/Filter Out actions |
| Saved Queries | Unskipped saved queries test |
| PPL Validation | Query not starting with source |

#### Code Quality Fixes

| Fix | Description |
|-----|-------------|
| Linting Error | Fixed linting error in new discover state tab slice |
| caniuse Update | Updated caniuse version for browser compatibility data |
| TS Types Refactor | Improved TypeScript types for Explore visualization interfaces |
| Component Split | Page components split into smaller container components |

### Usage Example

Running tests with the new infrastructure:

```bash
# Unit tests
yarn test:jest

# Integration tests
yarn test:jest_integration

# Cypress tests for Explore
yarn cypress:run --spec "cypress/integration/explore/**/*.spec.ts"

# Type checking (no longer needs baseline update)
yarn typecheck
```

### Migration Notes

For developers working with TypeScript errors:

1. Do not use `yarn update-ts-baseline` anymore
2. For existing errors, use `// @ts-expect-error TSxxx TODO(ts-error): fixme`
3. New errors should be fixed, not suppressed
4. IDE will now clearly distinguish expected vs. new errors

## Limitations

- `// @ts-expect-error` does not support expecting specific error codes (TypeScript limitation)
- Error codes in comments are for reference only

## References

### Documentation
- [OpenSearch Dashboards Repository](https://github.com/opensearch-project/OpenSearch-Dashboards)

### Pull Requests
| PR | Description |
|----|-------------|
| [#9922](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9922) | Add guidelines on testing and development |
| [#9931](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9931) | Use `// @ts-expect-error` instead of ts_error_baseline |
| [#9912](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9912) | Refactor TS types of explore visualization interfaces |
| [#9976](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9976) | Add Shenoy Pratik (@ps48) as a maintainer |
| [#10124](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10124) | Split page components into smaller container components |
| [#10263](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10263) | Add cypress test for default vis on rule matching |
| [#10288](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10288) | Add integ tests for New Autocomplete experience in Explore |
| [#10290](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10290) | Re-enable recent query cypress test for explore |
| [#10299](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10299) | Cypress tests for AI mode for explore |
| [#10302](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10302) | Add Tests for Filter In/Filter Out Actions in Explore |
| [#10307](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10307) | Unskip saved queries test for explore |
| [#10310](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10310) | Add Test to validate PPL query not starting with source |
| [#10328](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10328) | Fixed linting error of new discover state of tab slice |
| [#10328](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10328) | Update caniuse version |

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-dashboards/dashboards-code-quality-testing.md)
