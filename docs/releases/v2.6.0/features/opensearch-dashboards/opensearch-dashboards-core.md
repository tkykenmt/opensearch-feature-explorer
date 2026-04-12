---
tags:
  - opensearch-dashboards
---
# OpenSearch Dashboards Core

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to OpenSearch Dashboards Core.

## Details

### New Features

- **Add disablePrototypePoisoningProtection configuration to prevent JS client from erroring when cluster utilizes JS reserved words**: Enables the configuration of `disablePrototypePoisoningProtection` by setting `opensearch.disablePrototypePoisoningProtection`. Enables users to store protected logs that include reserve words from JS without the OpenSearch JS client throwing errors. We should still consider transforming unsafe data

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#2992](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/2992) | Add disablePrototypePoisoningProtection configuration to prevent JS client from erroring when cluster utilizes JS reserved words | OpenSearch-Dashboards |
