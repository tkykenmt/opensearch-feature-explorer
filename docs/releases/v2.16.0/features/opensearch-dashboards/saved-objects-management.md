---
tags:
  - opensearch-dashboards
---
# Saved Objects Management

## Summary

Fixed error handling in the Saved Objects Management page when workspace read-only users attempt to delete saved objects. Previously, the UI would display an infinite loading spinner; now it shows a proper error toast notification and allows users to continue with other operations.

## Details

### What's New in v2.16.0

This release fixes a UX issue in the Saved Objects Management page where workspace read-only users experienced a broken UI state when attempting to delete saved objects they don't have permission to delete.

### Problem

When a workspace read-only user attempted to delete a saved object:
1. A loading spinner would appear and never stop
2. The user could not interact with the table or perform other operations
3. No error message was displayed to explain the failure

### Solution

The `delete` method in `SavedObjectsTable` component was refactored to:
1. Wrap the delete operation in a try-catch block
2. Display an error toast notification when deletion fails
3. Keep the delete confirmation modal open on failure so users can cancel
4. Reset the `isDeleting` state to allow further interactions

### Technical Changes

The fix modifies `src/plugins/saved_objects_management/public/management_section/objects_table/saved_objects_table.tsx`:

```typescript
delete = async () => {
  const { savedObjectsClient, notifications } = this.props;
  // ... existing code ...
  
  try {
    // Delete operations
    await Promise.all(deletes);
    this.setState({ selectedSavedObjects: [] });
    await this.fetchSavedObjects();
    await this.fetchCounts();
    this.setState({ isShowingDeleteConfirmModal: false });
  } catch (error) {
    notifications.toasts.addDanger({
      title: i18n.translate(
        'savedObjectsManagement.objectsTable.unableDeleteSavedObjectsNotificationMessage',
        { defaultMessage: 'Unable to delete saved objects' }
      ),
      text: `${error}`,
    });
  }
  
  this.setState({ isDeleting: false });
};
```

### User Experience

| Before | After |
|--------|-------|
| Infinite loading spinner | Error toast notification |
| UI becomes unresponsive | Modal stays open, user can cancel |
| No feedback on failure | Clear error message displayed |

## Limitations

- The error toast displays a generic message; specific permission errors are not detailed
- Users must have appropriate workspace permissions to delete saved objects

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6756](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6756) | Show error toast when fail to delete saved objects |   |
