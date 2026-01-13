---
tags:
  - domain/infra
  - component/server
  - indexing
  - ml
  - search
---
# CI/Test Infrastructure

## Summary

This release includes 11 CI/Test infrastructure improvements across 6 repositories (anomaly-detection, index-management, job-scheduler, ml-commons, neural-search, and learning-to-rank). The changes focus on GitHub Actions version upgrades, test reliability improvements, disk space management for CI runners, and code coverage configuration adjustments.

## Details

### What's New in v3.4.0

This release addresses several CI/Test infrastructure challenges:

1. **GitHub Actions Version Upgrades**: Updated `actions/checkout` from v5 to v6 and `actions/github-script` from v7 to v8 to leverage Node.js 24 support and improved credential handling
2. **Test Reliability**: Fixed oversized bulk request issues in anomaly-detection tests and added BWC tests for Sparse ANN Seismic feature in neural-search
3. **CI Resource Management**: Addressed disk space issues in ml-commons CI by removing unnecessary files and adjusting disk circuit breaker thresholds
4. **S3 Snapshots Integration**: Onboarded neural-search to S3 snapshots for improved CI testing
5. **Multi-node Testing**: Added role assignment multi-node integration testing in neural-search CI
6. **Code Coverage**: Upgraded codecov-action to v5 to fix rate limit issues and adjusted coverage thresholds in learning-to-rank

### Technical Changes

#### GitHub Actions Updates

| Action | Previous | New | Repositories |
|--------|----------|-----|--------------|
| `actions/checkout` | v5 | v6 | job-scheduler |
| `actions/github-script` | v7 | v8 | index-management |
| `codecov/codecov-action` | v4 | v5 | neural-search |

Key improvements in actions/checkout v6:
- Credentials now stored in `$RUNNER_TEMP` instead of local git config
- Requires Actions Runner v2.329.0 or newer
- Node.js 24 support

#### Test Infrastructure Fixes

**Anomaly Detection - Bulk Request Batching**
```java
// Previous: Single bulk request for entire dataset (could exceed 10MB limit)
// New: Batch requests in groups of 1000 documents
```

**ML-Commons - Disk Space Management**
- Added step to remove unnecessary system and tool cache files before building
- Decreased disk circuit breaker free space threshold from 5GB to accommodate CI environments

**Neural-Search - Multi-node Testing**
- Added role assignment multi-node integration testing to discover potential issues earlier
- Onboarded to S3 snapshots for CI testing infrastructure

#### Code Coverage Configuration

**Learning-to-Rank**
- Reduced required coverage threshold from 70% to 50% temporarily until coverage can be improved

### Usage Example

GitHub Actions workflow update for checkout v6:
```yaml
- uses: actions/checkout@v6
  with:
    persist-credentials: true
```

## Limitations

- actions/checkout v6 requires Actions Runner v2.329.0 or newer
- Disk circuit breaker threshold adjustment is a workaround for CI environments with limited disk space
- Code coverage threshold reduction in learning-to-rank is temporary

## References

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1603](https://github.com/opensearch-project/anomaly-detection/pull/1603) | anomaly-detection | Prevent oversized bulk requests in synthetic data test |
| [#1485](https://github.com/opensearch-project/index-management/pull/1485) | index-management | Bump actions/github-script from 7 to 8 |
| [#863](https://github.com/opensearch-project/job-scheduler/pull/863) | job-scheduler | Bump actions/checkout from 5 to 6 |
| [#4405](https://github.com/opensearch-project/ml-commons/pull/4405) | ml-commons | Fix dependency conflict and jar hell |
| [#4413](https://github.com/opensearch-project/ml-commons/pull/4413) | ml-commons | Decrease Disk Circuit Breaker Free Space Threshold |
| [#4487](https://github.com/opensearch-project/ml-commons/pull/4487) | ml-commons | Remove unnecessary files on CI workflow to save space |
| [#1618](https://github.com/opensearch-project/neural-search/pull/1618) | neural-search | Onboard to S3 snapshots |
| [#1657](https://github.com/opensearch-project/neural-search/pull/1657) | neural-search | Add BWC tests for Sparse ANN Seismic feature |
| [#1663](https://github.com/opensearch-project/neural-search/pull/1663) | neural-search | Add role assignment multi-node integ testing in CI |
| [#1676](https://github.com/opensearch-project/neural-search/pull/1676) | neural-search | Upgrade codecov-action to v5 to fix rate limit issue |
| [#258](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/258) | learning-to-rank | Reduce required coverage until improvement |

### Issues (Design / RFC)
- [GitHub Issue #1659](https://github.com/tkykenmt/opensearch-feature-explorer/issues/1659): Investigation tracking issue
- [opensearch-build Issue #5360](https://github.com/opensearch-project/opensearch-build/issues/5360): S3 snapshots onboarding
- [neural-search Issue #1672](https://github.com/opensearch-project/neural-search/issues/1672): Codecov rate limit issue

## Related Feature Report

- Full feature documentation
