# Security Dashboards UI Fixes

## Summary

This release includes four bug fixes for the OpenSearch Dashboards Assistant plugin that improve UI behavior, error logging, and performance. The fixes address issues with unnecessary embeddable options in dropdown menus, improved error logging, optimized HTTP request timing for insights, and better conversation loading state management.

## Details

### What's New in v3.1.0

This release focuses on improving the user experience and code quality of the Dashboards Assistant plugin through targeted bug fixes.

### Technical Changes

#### Fix Unnecessary Embeddable in Create New Dropdown (PR #579)

The "Visualization with natural language" option was incorrectly appearing in the "Create new" dropdown menu. This fix adds a `canCreateNew()` method to `NLQVisualizationEmbeddableFactory` that returns `false`, preventing the option from appearing in the dropdown.

**Changed Files:**
- `public/components/visualization/embeddable/nlq_vis_embeddable_factory.ts`

```typescript
public canCreateNew() {
  return false;
}
```

#### Improved Error Logging (PR #548)

Error logging was previously outputting entire error objects, which could be verbose and difficult to parse. This fix modifies the error handler to log only the error body or message.

**Changed Files:**
- `server/routes/error_handler.ts`

```typescript
// Before
logger.error('Error occurred', e);

// After
logger.error('Error occurred', e.body || e.message);
```

#### Optimized Insights HTTP Request Timing (PR #520)

Previously, the HTTP request for insights was triggered immediately after the summary request, even if the user didn't intend to view insights. This fix defers the insights API call until the user explicitly clicks the "View insights" button.

**Changed Files:**
- `public/components/incontext_insight/generate_popover_body.tsx`

Key changes:
- Extracted `getInsightParams()` helper function for reuse
- Added `handleInsightClick()` function that triggers insight generation only on button click
- Removed automatic insight generation from the summary response handler

#### Fixed Chat Page Conversation Loading State (PR #569)

The chat page was showing a loading screen during history page loading when switching conversations. This fix introduces a standalone `ConversationLoadService` with its own status observable to separate conversation loading from history page loading.

**Changed Files:**
- `public/services/conversation_load_service.ts`
- `public/chat_header_button.tsx`
- `public/tabs/chat/chat_page.tsx`

Key changes:
- Added `getLatestConversationId()` method to `ConversationLoadService`
- Created separate `latestIdStatus$` observable for tracking conversation ID loading
- Refactored `loadLatestConversation()` to use the new service method

### Usage Example

No configuration changes are required. These fixes are automatically applied when upgrading to v3.1.0.

## Limitations

- The NLQ visualization embeddable is still available through other means (e.g., from within the assistant chat), just not from the "Create new" dropdown.

## Related PRs

| PR | Description |
|----|-------------|
| [#579](https://github.com/opensearch-project/dashboards-assistant/pull/579) | Fix unnecessary embeddable in create new dropdown |
| [#548](https://github.com/opensearch-project/dashboards-assistant/pull/548) | Log error body or message instead of the entire error object |
| [#520](https://github.com/opensearch-project/dashboards-assistant/pull/520) | Fix http request for insights to be triggered only after view insights button is clicked |
| [#569](https://github.com/opensearch-project/dashboards-assistant/pull/569) | Fix chat page conversation loading state |

## References

- [dashboards-assistant repository](https://github.com/opensearch-project/dashboards-assistant)

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-assistant/dashboards-assistant.md)
