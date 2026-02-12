---
tags:
  - opensearch
---
# S3 Repository Setting Fix

## Summary

Added the `S3Repository.LEGACY_MD5_CHECKSUM_CALCULATION` setting to the list of registered repository-s3 settings.

## Details

### What's New in v3.3.2

The `LEGACY_MD5_CHECKSUM_CALCULATION` setting was missing from the registered settings list for the repository-s3 plugin. This backport (from OpenSearch#19788) adds it to ensure the setting is properly recognized and configurable.

## References

| PR | Description |
|----|-------------|
| [#19789](https://github.com/opensearch-project/OpenSearch/pull/19789) | Add S3Repository.LEGACY_MD5_CHECKSUM_CALCULATION to repository-s3 settings |
| [#19788](https://github.com/opensearch-project/OpenSearch/pull/19788) | Original PR (main branch) |
