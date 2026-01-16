---
tags:
  - anomaly-detection
---
# PR Template Updates

## Summary

Added a standardized pull request template to the anomaly-detection repository with an API specification checkbox. This ensures contributors are reminded to document API changes in the central OpenAPI specification repository when making changes that affect the plugin's APIs.

## Details

### What's New in v2.16.0

The anomaly-detection repository now includes a `.github/PULL_REQUEST_TEMPLATE.md` file that provides a consistent structure for pull requests. The template includes:

- Description section for explaining changes
- Related Issues section for linking to relevant issues
- Checklist with key items:
  - Testing requirement
  - Documentation requirement
  - API specification companion PR requirement
  - DCO signoff requirement
  - Public documentation issue/PR requirement

### Technical Changes

| Change | Description |
|--------|-------------|
| New file | `.github/PULL_REQUEST_TEMPLATE.md` added |
| API spec checkbox | Links to opensearch-api-specification DEVELOPER_GUIDE.md |
| DCO reference | Links to CONTRIBUTING.md for signoff instructions |

### Template Content

```markdown
### Description
[Describe what this change achieves]

### Related Issues
Resolves #[Issue number to be closed when this PR is merged]

### Check List
- [ ] New functionality includes testing.
- [ ] New functionality has been documented.
- [ ] API changes companion pull request created.
- [ ] Commits are signed per the DCO using `--signoff`.
- [ ] Public documentation issue/PR created.
```

## Limitations

- No automated enforcement of checklist items
- Relies on contributor and reviewer diligence to ensure compliance

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1262](https://github.com/opensearch-project/anomaly-detection/pull/1262) | Update PULL_REQUEST_TEMPLATE to include an API spec change in the checklist | [opensearch-api-specification#387](https://github.com/opensearch-project/opensearch-api-specification/issues/387) |

### Issues

- [opensearch-api-specification#387](https://github.com/opensearch-project/opensearch-api-specification/issues/387): Proposal to add API spec checkbox to all plugin PR templates
