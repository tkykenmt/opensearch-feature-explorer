---
tags:
  - ml
  - search
---

# Search Relevance CI/Tests

## Summary
This release includes several improvements to the Search Relevance plugin's CI/CD infrastructure and test framework. The changes fix test dependencies, improve debugging capabilities, remove deprecated API usage, and clean up test code.

## Details

### What's New in v3.4.0

#### Test Dependency Fixes
- Fixed `CalculateJudgmentsIT.java` integration test dependency on UBI plugin by adding manual UBI mappings
- Tests no longer require the UBI plugin to be installed for proper execution

#### Debugging Improvements
- Added JDWP debug support to the `test` Gradle task, enabling developers to debug unit tests with `-Dtest.debug=1`
- Fixed duplicate JDWP configuration in `integTest` task that caused JVM TI agent load failures
- Consistent debug port usage: `8000` for test JVM, `5005` for cluster

#### Code Modernization
- Removed deprecated `AccessController.doPrivileged()` usage from `JsonUtils`
- OpenSearch does not run under a SecurityManager, making privileged blocks unnecessary
- Eliminates deprecation warnings for newer Java versions

#### Test Code Cleanup
- Applied IntelliJ-recommended fixes to test classes
- Improved code quality and maintainability

### Technical Changes

#### New Configuration
| Setting | Description | Default |
|---------|-------------|---------|
| `test.debug` | Enable JDWP debugging for unit tests | disabled |

#### Usage Example
```bash
# Debug unit tests
./gradlew test -Dtest.debug=1

# Debug integration tests
./gradlew :integTest -Dtest.debug=1
```

## Limitations
- Debug mode runs tests with `maxParallelForks = 1` for proper debugger attachment

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#311](https://github.com/opensearch-project/search-relevance/pull/311) | Fixed CalculateJudgmentsIT dependency on UBI plugin |
| [#300](https://github.com/opensearch-project/search-relevance/pull/300) | Added JDWP debug support for test Gradle task |
| [#296](https://github.com/opensearch-project/search-relevance/pull/296) | Fixed duplicate JDWP configuration in integTest |
| [#307](https://github.com/opensearch-project/search-relevance/pull/307) | Removed deprecated AccessController.doPrivileged() |
| [#288](https://github.com/opensearch-project/search-relevance/pull/288) | Small cleanups to test classes |

### Issues (Design / RFC)
- [Issue #302](https://github.com/opensearch-project/search-relevance/issues/302): CalculateJudgmentsIT UBI dependency issue
- [Issue #299](https://github.com/opensearch-project/search-relevance/issues/299): JDWP debug support request
- [Issue #295](https://github.com/opensearch-project/search-relevance/issues/295): Duplicate JDWP configuration bug
- [Issue #306](https://github.com/opensearch-project/search-relevance/issues/306): AccessController deprecation warnings

## Related Feature Report
- [Full feature documentation](../../../../features/search-relevance/ci-tests.md)
