---
tags:
  - domain/core
  - component/dashboards
  - dashboards
  - search
  - sql
---
# PPL/Query Enhancements

## Summary

OpenSearch Dashboards v3.3.0 introduces several improvements to the PPL (Piped Processing Language) query experience in the Query Panel. Key enhancements include a new PPL Formatter for automatic code formatting, updated PPL grammar support, improved error display, and fixed keyboard behavior in the query editor.

## Details

### What's New in v3.3.0

This release focuses on improving the developer experience when writing PPL queries:

1. **PPL Formatter**: New code formatting capability using `Shift+Option+F` (Mac) or `Shift+Alt+F` (Windows/Linux)
2. **Updated PPL Grammar**: Synchronized with the latest PPL grammar from the SQL plugin
3. **Cleaner Error Display**: Removed redundant error popover, errors now display only under the input box
4. **Fixed Enter Key Behavior**: Resolved issues with Enter key when switching between query languages

### Technical Changes

#### PPL Formatter

A new document formatting provider has been added to the Monaco editor for PPL queries:

| Feature | Description |
|---------|-------------|
| Keyboard Shortcut | `Shift+Option+F` (Mac) / `Shift+Alt+F` (Windows/Linux) |
| Trigger | Manual via keyboard shortcut |
| Scope | Entire PPL document |

The formatter parses PPL queries and applies consistent formatting rules for improved readability.

#### PPL Grammar Update

The simplified PPL grammar has been updated to match the latest version from the [SQL plugin](https://github.com/opensearch-project/sql/pull/4106). This ensures:

- Consistent syntax highlighting
- Accurate autocomplete suggestions
- Proper query validation

#### Query Editor Keyboard Behavior

Fixed Enter key behavior when switching between DQL/Lucene and PPL/SQL:

| Scenario | Before | After |
|----------|--------|-------|
| Enter with suggestion visible | Unpredictable | Accepts suggestion |
| Enter without suggestion | Cleared query, ran empty query | Moves to next line |
| Run query | Unpredictable | Use `Cmd+Enter` / `Ctrl+Enter` |

#### Error Display Cleanup

Removed the redundant error icon/popover next to Saved Queries button. Error messages now display only in the designated area under the query input box, reducing visual clutter.

### Usage Example

```ppl
# Before formatting
source=logs|where status=200|stats count() by host|sort -count()

# After formatting (Shift+Option+F)
source = logs
| where status = 200
| stats count() by host
| sort - count()
```

### Migration Notes

No migration required. These are additive improvements to the existing Query Panel functionality.

## Limitations

- PPL Formatter requires the query to be syntactically valid for best results
- Formatting preferences are not configurable in this release

## References

### Documentation
- [PPL Documentation](https://docs.opensearch.org/3.3/search-plugins/sql/ppl/index/): Official PPL documentation
- [Query Workbench](https://docs.opensearch.org/3.3/dashboards/query-workbench/): Query Workbench documentation
- [SQL Plugin PR #4106](https://github.com/opensearch-project/sql/pull/4106): Source PPL grammar update

### Pull Requests
| PR | Description |
|----|-------------|
| [#10503](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10503) | Add PPL Formatter in Query panel |
| [#10536](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10536) | Update Simplified PPL grammar to latest version |
| [#10581](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10581) | Remove error popover from query panel |
| [#10446](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10446) | Fix Enter command behaviour in query editor |

## Related Feature Report

- Full feature documentation
