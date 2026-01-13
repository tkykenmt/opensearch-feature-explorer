---
tags:
  - domain/core
  - component/dashboards
  - dashboards
---
# Dashboards CI/Tests

## Summary

This bugfix updates the OpenSearch Dashboards unit test workflow to include support for 3.* branches, ensuring CI/CD pipelines properly run tests across all supported version branches.

## Details

### What's New in v3.4.0

The unit test workflow configuration was updated to include 3.* branch patterns in the CI trigger configuration. This ensures that:

- Unit tests run automatically on pull requests targeting 3.x branches
- CI pipelines properly validate code changes for the 3.x release line
- Test coverage is maintained across all active development branches

### Technical Changes

#### Workflow Configuration Update

The GitHub Actions workflow file was modified to include the 3.* branch pattern in the branch filter configuration, enabling automated test execution for the OpenSearch 3.x release series.

```yaml
# Example workflow trigger configuration
on:
  push:
    branches:
      - main
      - 2.*
      - 3.*  # Added in this update
  pull_request:
    branches:
      - main
      - 2.*
      - 3.*  # Added in this update
```

### Impact

| Aspect | Description |
|--------|-------------|
| CI Coverage | Unit tests now run on 3.x branches |
| Branch Support | Aligns CI with OpenSearch 3.x release line |
| Test Reliability | Ensures consistent test execution across versions |

## Limitations

- This is a CI/infrastructure change with no user-facing impact
- Requires GitHub Actions workflow permissions to be properly configured

## References

### Documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenSearch Dashboards Repository](https://github.com/opensearch-project/OpenSearch-Dashboards)

### Pull Requests
| PR | Description |
|----|-------------|
| [#780](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/780) | Update unit test workflow to include 3.* branch |

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-dashboards/dashboards-dashboards-observability-search-relevance-ci-tests.md)
