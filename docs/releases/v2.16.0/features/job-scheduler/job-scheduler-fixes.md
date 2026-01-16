---
tags:
  - job-scheduler
---
# Job Scheduler Fixes

## Summary

Fixed GitHub Actions CI workflow failure caused by GLIBC version incompatibility on older runner images by enabling Node16 fallback.

## Details

### What's New in v2.16.0

The CI workflow was failing with GLIBC version errors when running the checkout action:

```
/__e/node20/bin/node: /lib64/libm.so.6: version `GLIBC_2.27' not found (required by /__e/node20/bin/node)
/__e/node20/bin/node: /lib64/libc.so.6: version `GLIBC_2.28' not found (required by /__e/node20/bin/node)
```

### Technical Changes

Added `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true` environment variable to the CI workflow to allow using Node16 actions instead of Node20, which requires newer GLIBC versions not available on the runner image.

```yaml
env:
  ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true
```

This is a temporary workaround until the runner images are updated with newer GLIBC versions.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#650](https://github.com/opensearch-project/job-scheduler/pull/650) | Fix checkout action failure | [actions/checkout#1809](https://github.com/actions/checkout/issues/1809) |
