---
tags:
  - search
---

# Common Infrastructure

## Summary

This release item updates the pull request template across OpenSearch repositories to include a checkbox requiring contributors to document API changes in the OpenAPI specification. This enhancement improves the consistency of API documentation and ensures that language client libraries stay synchronized with API changes.

## Details

### What's New in v2.17.0

The `PULL_REQUEST_TEMPLATE.md` in the common-utils repository was updated to include a new checklist item that prompts contributors to create companion pull requests for API specification changes.

### Technical Changes

#### Template Updates

The pull request template was restructured with the following changes:

| Section | Before | After |
|---------|--------|-------|
| Issues Section | "Issues Resolved" | "Related Issues" with clearer format |
| Checklist | Basic testing/docs items | Added API spec change checkbox |
| DCO Reference | Linked to OpenSearch repo | Linked to common-utils repo |

#### New Checklist Items

```markdown
### Check List
- [ ] New functionality includes testing.
- [ ] New functionality has been documented.
- [ ] API changes companion pull request [created](https://github.com/opensearch-project/opensearch-api-specification/blob/main/DEVELOPER_GUIDE.md).
- [ ] Commits are signed per the DCO using `--signoff`.
- [ ] Public documentation issue/PR [created](https://github.com/opensearch-project/documentation-website/issues/new/choose).
```

### Usage Example

When creating a pull request that includes API changes, contributors should:

1. Create the main PR in the plugin repository
2. Create a companion PR in [opensearch-api-specification](https://github.com/opensearch-project/opensearch-api-specification) with the OpenAPI spec changes
3. Check the "API changes companion pull request created" checkbox

### Migration Notes

No migration required. This is a process improvement that applies to new pull requests.

## Limitations

- The checkbox is a reminder only; there is no automated enforcement
- Contributors must manually create companion PRs for API changes

## References

### Documentation
- [OpenSearch API Specification](https://github.com/opensearch-project/opensearch-api-specification): Central repository for API specifications
- [Developer Guide](https://github.com/opensearch-project/opensearch-api-specification/blob/main/DEVELOPER_GUIDE.md): Guide for contributing API specs

### Pull Requests
| PR | Description |
|----|-------------|
| [#696](https://github.com/opensearch-project/common-utils/pull/696) | Update PULL_REQUEST_TEMPLATE to include API spec change checkbox |

### Issues (Design / RFC)
- [Issue #387](https://github.com/opensearch-project/opensearch-api-specification/issues/387): Proposal to add checkbox in plugin PR templates

## Related Feature Report

- [Full feature documentation](../../../../features/common/common-pr-template-api-spec.md)
