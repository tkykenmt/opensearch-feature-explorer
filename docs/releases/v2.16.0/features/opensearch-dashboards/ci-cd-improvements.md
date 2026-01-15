---
tags:
  - opensearch-dashboards
---
# CI/CD Improvements

## Summary

This release improves CI/CD efficiency by skipping test runs when only the CODEOWNERS file is modified. This optimization reduces unnecessary CI resource usage for administrative changes that don't affect code functionality.

## Details

### What's New in v2.16.0

The `build_and_test_workflow.yml` GitHub Actions workflow now includes `CODEOWNERS` in the `paths-ignore` list for both `push` and `pull_request` triggers. This means:

- Pushes that only modify CODEOWNERS will not trigger the full test suite
- Pull requests that only modify CODEOWNERS will not trigger the full test suite

### Technical Changes

The workflow file was updated to add `CODEOWNERS` to the existing `paths-ignore` patterns:

```yaml
on:
  push:
    branches: ['**']
    paths-ignore:
      - '**/*.md'
      - 'docs/**'
      - '.lycheeignore'
      - 'CODEOWNERS'  # Added in v2.16.0
      - 'changelogs/fragments/**'
  pull_request:
    branches: ['**']
    paths-ignore:
      - '**/*.md'
      - 'docs/**'
      - '.lycheeignore'
      - 'CODEOWNERS'  # Added in v2.16.0
      - 'changelogs/fragments/**'
```

## Limitations

- This optimization only applies to commits that exclusively modify CODEOWNERS
- If CODEOWNERS is modified alongside other files, the full test suite will still run

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7197](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7197) | Skip running tests for updates in CODEOWNERS | N/A |
