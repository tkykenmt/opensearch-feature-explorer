---
tags:
  - domain/search
  - component/dashboards
  - dashboards
  - search
---
# Dashboards Bugfixes

## Summary

This release item fixes a Sass division warning in the dashboards-search-relevance plugin by updating deprecated Sass division syntax to use the modern `calc()` function. This change ensures compatibility with newer versions of Sass compilers that have deprecated the `/` operator for division.

## Details

### What's New in v2.17.0

The fix addresses a deprecation warning that appeared during the build process when using Sass division with the `/` operator. Modern Sass compilers (Dart Sass) have deprecated this syntax in favor of the `calc()` function or `math.div()`.

### Technical Changes

#### Code Change

The change is minimal but important for build compatibility:

**Before:**
```scss
padding: ($euiSizeXS / 2) $euiSizeXS;
```

**After:**
```scss
padding: calc($euiSizeXS / 2) $euiSizeXS;
```

#### Affected File

| File | Description |
|------|-------------|
| `public/components/query_compare/search_result/result_components/result_grid.scss` | Updated Sass division syntax |

### Background

Sass deprecated the `/` operator for division starting with Dart Sass 1.33.0 (released in 2021). The deprecation warning indicates that this syntax will be removed in Dart Sass 2.0.0. The recommended migration path is to use:

1. `calc()` function (CSS native) - used in this fix
2. `math.div()` function (Sass native)

Using `calc()` is preferred when the result needs to be a CSS value, as it's natively supported by browsers and doesn't require importing the Sass math module.

### Usage Example

The affected code is part of the result grid styling in the Search Relevance plugin's query comparison feature:

```scss
doc-table {
  dt {
    background-color: tintOrShade($euiColorPrimary, 90%, 70%);
    color: $euiTextColor;
    padding: calc($euiSizeXS / 2) $euiSizeXS;  // Fixed division syntax
    margin-right: $euiSizeXS;
    word-break: normal;
    border-radius: $euiBorderRadius;
  }
}
```

## Limitations

- This is a build-time fix only; no runtime behavior changes
- The visual appearance of the UI remains unchanged

## References

### Documentation
- [Sass Breaking Change: Slash as Division](https://sass-lang.com/documentation/breaking-changes/slash-div/)
- [OpenSearch Dashboards PR #5338](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/5338): Replace `node-sass` with `sass-embedded` (related modernization)

### Pull Requests
| PR | Description |
|----|-------------|
| [#426](https://github.com/opensearch-project/dashboards-search-relevance/pull/426) | Fix sass division warning |
| [#435](https://github.com/opensearch-project/dashboards-search-relevance/pull/435) | Backport to 2.x |
| [#436](https://github.com/opensearch-project/dashboards-search-relevance/pull/436) | Backport to 2.17 |

## Related Feature Report

- Dashboards Search Relevance Documentation Maintenance
