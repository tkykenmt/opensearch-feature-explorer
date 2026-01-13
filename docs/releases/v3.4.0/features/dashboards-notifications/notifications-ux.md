---
tags:
  - domain/observability
  - component/dashboards
  - dashboards
---
# Notifications UX

## Summary

This release fixes a UX regression in the OpenSearch Dashboards Notifications plugin where editing a channel name would trigger unnecessary API calls on every keystroke, causing the edit page to refresh and lose user input.

## Details

### What's New in v3.4.0

A bug introduced in PR #257 caused the channel edit page to refetch the channel configuration on every keystroke when updating the channel name field. This resulted in:

- Excessive API calls to the backend
- The edit page refreshing with current values, overwriting user input
- Poor user experience when trying to rename channels

### Technical Changes

#### Root Cause

The issue was in `CreateChannel.tsx` where the `useEffect` hook had `name` in its dependency array. Since the name field is bound to component state, every keystroke triggered the effect, which called `getChannel()` to fetch the current configuration from the backend.

#### Fix Implementation

The fix separates the initial data loading from the breadcrumb updates:

```typescript
// Initial load: fetch channel data and set up page
useEffect(() => {
  window.scrollTo(0, 0);
  if (props.edit) {
    getChannel();
  }
}, []);

// Update breadcrumbs when name changes
useEffect(() => {
  // ... breadcrumb logic
  setBreadcrumbs(breadcrumbs);
}, [name, props.edit]);
```

Key changes:
- Initial data fetch now runs only once on component mount (empty dependency array)
- Breadcrumb updates still respond to name changes but no longer trigger data refetch
- Removed `getUseUpdatedUx()` from dependencies as it's not needed for this effect

### Usage Example

After this fix, users can edit channel names normally:

1. Navigate to Notifications → Channels
2. Click on a channel to view details
3. Click Actions → Edit
4. Update the channel name field - input is preserved as expected
5. Click Save to persist changes

## Limitations

- This fix is specific to the channel name field editing flow
- Other fields in the edit form were not affected by this bug

## References

### Documentation
- [OpenSearch Notifications Documentation](https://docs.opensearch.org/latest/observing-your-data/notifications/index/)
- [dashboards-notifications Repository](https://github.com/opensearch-project/dashboards-notifications)

### Pull Requests
| PR | Description |
|----|-------------|
| [#393](https://github.com/opensearch-project/dashboards-notifications/pull/393) | Avoid refetching channel config on every keystroke for name update |
| [#257](https://github.com/opensearch-project/dashboards-notifications/pull/257) | Edit page changes as per new page header (introduced the regression) |

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-notifications/dashboards-notifications.md)
