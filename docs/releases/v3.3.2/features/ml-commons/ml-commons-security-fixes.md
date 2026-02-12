---
tags:
  - ml-commons
---
# ML Commons Security Fixes

## Summary

Security fixes in v3.3.2 address CVE-2025-58057 and a regex bypass vulnerability in both ml-commons and skills plugins.

## Details

### What's New in v3.3.2

- **CVE-2025-58057 Fix** (ml-commons#4338): Patched a security vulnerability identified as CVE-2025-58057.

- **Regex Bypass Fix** (ml-commons#4336, skills#656): Fixed a regex bypass issue that could allow unauthorized access patterns. The fix was applied to both the ml-commons plugin and the skills plugin to ensure consistent security enforcement.

## References

| PR | Repository | Description |
|----|------------|-------------|
| [#4338](https://github.com/opensearch-project/ml-commons/pull/4338) | ml-commons | Fix CVE-2025-58057 |
| [#4336](https://github.com/opensearch-project/ml-commons/pull/4336) | ml-commons | Fixing regex bypass issue |
| [#656](https://github.com/opensearch-project/skills/pull/656) | skills | Fix regex bypass issue |
