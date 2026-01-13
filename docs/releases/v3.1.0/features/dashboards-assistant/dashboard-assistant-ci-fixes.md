---
tags:
  - domain/ml
  - component/dashboards
  - dashboards
---
# Dashboard Assistant CI Fixes

## Summary

This release fixes CI failures in the dashboards-assistant plugin caused by path alias changes introduced in OpenSearch Dashboards core. The fix ensures Jest tests can properly resolve module imports using the new path alias babel configuration.

## Details

### What's New in v3.1.0

The CI pipeline was failing because OpenSearch Dashboards core introduced a path alias babel configuration in PR #9831. This change required plugins to update their babel configuration to use the new reusable path alias plugin.

### Technical Changes

#### Root Cause

OpenSearch Dashboards core extracted the path alias babel configuration into a reusable function (`@osd/babel-preset/path_alias`) to allow plugins to share the same module resolution behavior during testing.

#### Fix Applied

The `babel.config.js` file was updated to:
1. Import the `pathAliasPlugin` from `@osd/babel-preset/path_alias`
2. Add the plugin to the babel configuration for test environments

```javascript
const pathAliasPlugin = require('@osd/babel-preset/path_alias');

module.exports = function (api) {
  if (api.env('test')) {
    return {
      presets: [
        require('@babel/preset-env', { ... }),
        require('@babel/preset-react'),
        require('@babel/preset-typescript'),
      ],
      plugins: [pathAliasPlugin({})],
    };
  }
  return {};
};
```

### Files Changed

| File | Change |
|------|--------|
| `babel.config.js` | Added path alias plugin import and configuration |
| `CHANGELOG.md` | Added entry under Infrastructure section |

## Limitations

- This fix only affects the test environment configuration
- No runtime behavior changes

## References

### Documentation
- [PR #580](https://github.com/opensearch-project/dashboards-assistant/pull/580): Main fix implementation
- [PR #9831](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9831): Root cause - path alias extraction in OSD core

### Pull Requests
| PR | Description |
|----|-------------|
| [#580](https://github.com/opensearch-project/dashboards-assistant/pull/580) | Fix failed CI due to path alias |
| [#9831](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9831) | Extract path alias babel config to reusable function (OSD core) |

## Related Feature Report

- Full feature documentation
