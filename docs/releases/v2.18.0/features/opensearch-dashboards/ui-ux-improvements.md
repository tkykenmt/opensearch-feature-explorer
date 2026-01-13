---
tags:
  - domain/core
  - component/dashboards
  - dashboards
  - neural-search
---
# UI/UX Improvements

## Summary

This release improves the semantic structure and accessibility of page titles in OpenSearch Dashboards application headers. Page titles are now rendered as proper `<h1>` heading elements with appropriate sizing, enhancing screen reader compatibility and HTML semantics.

## Details

### What's New in v2.18.0

The page title in application headers has been changed from a generic text element to a semantic heading element:

- Changed from `<EuiText size="s">` to `<EuiTitle size="xs"><h1>...</h1></EuiTitle>`
- Provides proper document structure with `<h1>` as the main page heading
- Uses extra-small (`xs`) title size to maintain visual consistency
- Improves accessibility for screen readers and assistive technologies

### Technical Changes

#### Component Changes

| Before | After |
|--------|-------|
| `<EuiText size="s">{screenTitle}</EuiText>` | `<EuiTitle size="xs"><h1>{screenTitle}</h1></EuiTitle>` |

#### CSS Updates

The SCSS selector was updated to match the new component:

```scss
.osdTopNavMenuScreenTitle {
  // Changed from .euiText to .euiTitle
  .euiTitle {
    line-height: $euiFormControlCompressedHeight;
    white-space: nowrap;
    overflow: hidden;
  }
}
```

#### Files Changed

| File | Change |
|------|--------|
| `src/plugins/navigation/public/top_nav_menu/top_nav_menu.tsx` | Replace EuiText with EuiTitle + h1 |
| `src/plugins/navigation/public/top_nav_menu/_index.scss` | Update CSS selector |

### Visual Comparison

The change maintains visual consistency across all theme versions (v7, vNext, v9) while improving semantic structure. The page title appearance remains similar but now uses proper heading semantics.

## Limitations

- The change is purely semantic/accessibility focused
- No visual changes are expected in most cases
- Custom CSS targeting `.euiText` within page titles may need updates

## References

### Documentation
- [EUI Title Component](https://oui.opensearch.org/1.6/#/display/title): OpenSearch UI title component documentation
- [PR #8227](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8227): Main implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#8227](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8227) | Change page title of application headers to h1 and xs |

## Related Feature Report

- Full feature documentation
