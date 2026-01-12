---
tags:
  - ml
---

# ML Skills

## Summary

This release fixes a dependency version conflict in the Skills plugin's build configuration. The `httpclient5` dependency was incorrectly using the `httpcore5` version variable, causing potential version mismatches. Additionally, code formatting was applied to `WebSearchTool.java` using Spotless.

## Details

### What's New in v3.1.0

This is a maintenance release that addresses build configuration issues:

1. **Dependency Version Fix**: Corrected the `httpclient5` dependency to use the proper `${versions.httpclient5}` variable instead of `${versions.httpcore5}`
2. **Code Formatting**: Applied Spotless code formatting to `WebSearchTool.java` for consistent code style

### Technical Changes

#### Build Configuration Fix

The `build.gradle` file had two locations where `httpclient5` was incorrectly referencing the `httpcore5` version:

**Before:**
```gradle
force("org.apache.httpcomponents.client5:httpclient5:5.4.1")
compileOnly(group: 'org.apache.httpcomponents.client5', name: 'httpclient5', version: "${versions.httpcore5}")
```

**After:**
```gradle
force("org.apache.httpcomponents.client5:httpclient5:${versions.httpclient5}")
compileOnly(group: 'org.apache.httpcomponents.client5', name: 'httpclient5', version: "${versions.httpclient5}")
```

#### Code Formatting

The `WebSearchTool.java` file received Spotless formatting changes including:
- Import statement ordering (static imports first)
- String concatenation alignment
- Method parameter alignment
- Conditional expression formatting

### Migration Notes

No migration required. This is a transparent fix that ensures correct dependency resolution.

## Limitations

None specific to this release.

## References

### Documentation
- [Skills Repository](https://github.com/opensearch-project/skills): Source code

### Pull Requests
| PR | Description |
|----|-------------|
| [#575](https://github.com/opensearch-project/skills/pull/575) | Fix conflict in dependency versions |

## Related Feature Report

- [Full feature documentation](../../../../features/skills/skills-tools.md)
