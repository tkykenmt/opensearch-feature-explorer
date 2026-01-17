---
tags:
  - ml-commons
---
# Conversation Memory

## Summary

In OpenSearch 2.16.0, the Conversation Memory feature has been promoted from experimental to generally available (GA). This change removes the "experimental" designation from all Conversation Memory APIs and error messages, signaling that the feature is now production-ready and stable.

## Details

### What's New in v2.16.0

The Conversation Memory feature, which was introduced as experimental in v2.12.0, is now officially GA. The primary change involves:

- Removing the "experimental" label from error messages across all Conversation Memory transport actions
- Centralizing the disabled feature message into a constant (`ML_COMMONS_MEMORY_FEATURE_DISABLED_MESSAGE`)
- Code cleanup including method reference improvements and logging format updates

### Technical Changes

The following transport actions were updated to use the new standardized error message:

| Transport Action | Description |
|-----------------|-------------|
| `CreateConversationTransportAction` | Creates a new conversation memory |
| `CreateInteractionTransportAction` | Creates a message within a conversation |
| `DeleteConversationTransportAction` | Deletes a conversation memory |
| `GetConversationTransportAction` | Retrieves a single conversation |
| `GetConversationsTransportAction` | Lists all conversations |
| `GetInteractionTransportAction` | Retrieves a single message |
| `GetInteractionsTransportAction` | Lists messages in a conversation |
| `SearchConversationsTransportAction` | Searches conversations |
| `SearchInteractionsTransportAction` | Searches messages |
| `UpdateConversationTransportAction` | Updates conversation metadata |
| `UpdateInteractionTransportAction` | Updates message metadata |

### Error Message Change

Before v2.16.0:
```
The experimental Conversation Memory feature is not enabled. To enable, please update the setting plugins.ml_commons.memory_feature_enabled
```

After v2.16.0:
```
The Conversation Memory feature is not enabled. To enable, please update the setting plugins.ml_commons.memory_feature_enabled
```

## Limitations

- The feature must still be explicitly enabled via the `plugins.ml_commons.memory_feature_enabled` setting (default: `true`)
- When the Security plugin is enabled, all memories exist in a private security mode - only the user who created a memory can interact with it

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2592](https://github.com/opensearch-project/ml-commons/pull/2592) | Removing experimental from the Conversation memory feature | - |

### Documentation
- [Memory APIs](https://docs.opensearch.org/2.16/ml-commons-plugin/api/memory-apis/index/)
- [Conversational Search](https://docs.opensearch.org/2.16/search-plugins/conversational-search/)
