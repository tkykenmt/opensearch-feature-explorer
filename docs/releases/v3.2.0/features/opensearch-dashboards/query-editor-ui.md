# Query Editor UI

## Summary

OpenSearch Dashboards v3.2.0 includes several UI/UX improvements to the Query Editor in the Explore plugin. These changes improve the autocomplete behavior, generated query display, and "Edit query" button placement for a better user experience.

## Details

### What's New in v3.2.0

Three bugfixes improve the Query Editor experience:

1. **Autocomplete fixes**: Fixed stale query data being passed to the autocomplete service, improved Tab and Enter key handling for suggestion selection
2. **Generated query UI**: Made the generated query display scrollable with a max height instead of using ellipsis truncation
3. **Edit query button placement**: Moved the "Edit query" button closer to the generated PPL query and changed it from a button to a badge, then refined to use `EuiButtonEmpty` with "Replace query" label

### Technical Changes

#### Autocomplete Improvements (PR #9960)

The autocomplete system had issues with stale query data and keyboard handling:

| Issue | Fix |
|-------|-----|
| Stale query passed to autocomplete | Use `model.getValue()` instead of `localQuery` state |
| Tab selection not triggering next autocomplete | Added Tab key handler to accept suggestion and retrigger |
| Enter key behavior inconsistent | Added Enter key handler to check suggestion widget visibility |

Key code changes in `resuable_editor.tsx`:
```typescript
// Tab key: accept suggestion and trigger next autocomplete
editor.addCommand(monaco.KeyCode.Tab, () => {
  editor.trigger('keyboard', 'acceptSelectedSuggestion', {});
  setTimeout(() => {
    editor.trigger('keyboard', 'editor.action.triggerSuggest', {});
  }, 100);
});

// Enter key: accept suggestion if visible, otherwise run query
editor.addCommand(monaco.KeyCode.Enter, () => {
  const suggestWidgetVisible = contextKeyService?.getContextKeyValue('suggestWidgetVisible');
  if (suggestWidgetVisible) {
    editor.trigger('keyboard', 'acceptSelectedSuggestion', {});
    setTimeout(() => {
      editor.trigger('keyboard', 'editor.action.triggerSuggest', {});
    }, 100);
  } else {
    onRun(editor.getValue());
    onEdit();
  }
});
```

Also enabled `tabCompletion: 'on'` in editor configuration.

#### Generated Query UI (PR #10337)

Changed the generated query display from ellipsis truncation to scrollable:

| Before | After |
|--------|-------|
| Single line with ellipsis | Scrollable with max height |
| `text-overflow: ellipsis` | `max-height: calc($ouiSize * 3)` |
| `white-space: nowrap` | `overflow-y: auto` |

The button was also changed from `EuiBadge` to `EuiButtonEmpty` with icon changed from `editorCodeBlock` to `sortUp`, and label changed from "Edit query" to "Replace query".

#### Edit Query Button Placement (PR #10259)

Moved the "Edit query" button to be adjacent to the generated query text:

- Changed from `EuiButtonEmpty` to `EuiBadge` (later reverted in PR #10337)
- Added `filter: brightness(0.65)` to prompt icon for better visibility
- Simplified CSS by removing separate right section wrapper

### Usage Example

The Query Editor in Explore now provides smoother autocomplete interaction:

1. Type a query in the editor
2. Press Tab to accept a suggestion and immediately see next suggestions
3. Press Enter within suggestion widget to accept and continue
4. Press Enter outside suggestion widget to execute the query
5. View the full generated PPL query in a scrollable area
6. Click "Replace query" to copy the generated query to the editor

## Limitations

- The 100ms delay for retriggering suggestions is a workaround and may feel slightly delayed
- The max height for generated query is fixed at `3 * $ouiSize`

## References

### Documentation
- [Query Editor Feature](../../../features/opensearch-dashboards/query-editor.md): Full feature documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#9960](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9960) | Fix autocomplete for new query panel |
| [#10259](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10259) | Change query editor UI - edit button placement |
| [#10337](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10337) | Change generated query UI - scrollable display |

## Related Feature Report

- [Query Editor](../../../features/opensearch-dashboards/query-editor.md)
