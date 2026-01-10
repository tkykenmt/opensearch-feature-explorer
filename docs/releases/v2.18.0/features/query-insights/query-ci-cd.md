# Query CI/CD

## Summary

This bugfix upgrades deprecated `actions/upload-artifact` GitHub Actions from v1/v2 to v3 in the query-insights plugin CI workflows. This resolves CI failures caused by GitHub deprecating older versions of the artifact upload action.

## Details

### What's New in v2.18.0

GitHub deprecated `actions/upload-artifact` v1 and v2 in February 2024, causing CI workflows to fail with automatic errors. This change updates all artifact upload actions to v3 across the query-insights CI workflows.

### Technical Changes

#### Files Modified

| File | Changes |
|------|---------|
| `.github/workflows/ci.yml` | Updated 5 `actions/upload-artifact` references from v1/v2 to v3 |
| `.github/workflows/integ-tests-with-security.yml` | Updated 2 `actions/upload-artifact` references from v2 to v3 |

#### Before/After

```yaml
# Before
- uses: actions/upload-artifact@v1
- uses: actions/upload-artifact@v2

# After
- uses: actions/upload-artifact@v3
```

### Migration Notes

No migration required. This is a CI infrastructure change that does not affect plugin functionality.

## Limitations

- `actions/upload-artifact@v3` has different retention and artifact handling compared to v1/v2
- Future upgrades to v4 may be needed as GitHub continues to deprecate older versions

## Related PRs

| PR | Description |
|----|-------------|
| [#117](https://github.com/opensearch-project/query-insights/pull/117) | Upgrade deprecated actions/upload-artifact versions to v3 |

## References

- [GitHub Blog: Deprecation notice for v1 and v2 of artifact actions](https://github.blog/changelog/2024-02-13-deprecation-notice-v1-and-v2-of-the-artifact-actions/): Official deprecation announcement

## Related Feature Report

- [Full feature documentation](../../../../features/ci/cd-build-improvements.md)
