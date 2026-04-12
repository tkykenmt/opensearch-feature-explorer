---
tags:
  - anomaly-detection
---
# Anomaly Detection

## Summary

OpenSearch 2.6.0 brings 3 enhancement(s) to Anomaly Detection, along with 5 bug fixes.

## Details

### Enhancements

- **Update cold start message**
- **Changed required minimum intervals in cold start message**
- **Remove `auto_expand_replicas` override in sample data indices**

### Bug Fixes

- Fixing dls/fls logic around numeric aggregations
- Revert changes to exception message
- Upgrade filter bug
- Dynamically set bwc current version from properties version
- Bump @sideway/formula to 3.0.1

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#398](https://github.com/opensearch-project/anomaly-detection/pull/398) | Update cold start message | anomaly-detection |
| [#411](https://github.com/opensearch-project/anomaly-detection/pull/411) | Changed required minimum intervals in cold start message | anomaly-detection |
| [#423](https://github.com/opensearch-project/anomaly-detection/pull/423) | Remove `auto_expand_replicas` override in sample data indices | anomaly-detection |
| [#800](https://github.com/opensearch-project/anomaly-detection/pull/800) | Fixing dls/fls logic around numeric aggregations | anomaly-detection |
| [#803](https://github.com/opensearch-project/anomaly-detection/pull/803) | Revert changes to exception message | anomaly-detection |
| [#402](https://github.com/opensearch-project/anomaly-detection/pull/402) | Upgrade filter bug | anomaly-detection |
| [#778](https://github.com/opensearch-project/anomaly-detection/pull/778) | Dynamically set bwc current version from properties version | anomaly-detection |
| [#418](https://github.com/opensearch-project/anomaly-detection/pull/418) | Bump @sideway/formula to 3.0.1 | anomaly-detection |
