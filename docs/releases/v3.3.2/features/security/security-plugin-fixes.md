---
tags:
  - security
---
# Security Plugin Fixes

## Summary

Two bug fixes for the OpenSearch Security plugin: WildcardMatcher handling of empty strings and earlier security provider registration during bootstrap.

## Details

### What's New in v3.3.2

- **WildcardMatcher Empty String Fix** (security#5694): Changed `WildcardMatcher` to create a `WildcardMatcher.NONE` when initialized with an empty string, preventing unexpected matching behavior.

- **Security Provider Bootstrap Order** (security#5749): Moved security provider registration earlier in the bootstrap process to ensure cryptographic providers are available when needed during node startup.

## References

| PR | Description |
|----|-------------|
| [#5694](https://github.com/opensearch-project/security/pull/5694) | Create WildcardMatcher.NONE for empty string |
| [#5749](https://github.com/opensearch-project/security/pull/5749) | Add security provider earlier in bootstrap process |
