---
tags:
  - notifications
---
# Mattermost Notifications

## Summary

OpenSearch v3.5.0 adds native support for Mattermost as a notification channel destination. This feature addresses a regression introduced in OpenSearch 3.0.0 where URL validation for Slack channels prevented users from using Slack-compatible platforms like Mattermost, Discord, RocketChat, and Zulip.

## Details

### What's New in v3.5.0

The Mattermost notification channel type provides:

- **New ConfigType**: `MATTERMOST` added to the notifications ConfigType enum
- **Slack-compatible payload**: Uses the same `{"text": "message"}` format as Slack
- **Flexible URL validation**: Accepts webhook URLs matching `https://.*/hooks/.*` pattern
- **Full Dashboards integration**: New UI component for configuring Mattermost channels

### Technical Changes

#### Backend Changes (notifications plugin)

The implementation reuses the existing Slack infrastructure since Mattermost accepts the same payload format:

```kotlin
// ConfigIndexingActions.kt - URL validation
private fun validateMattermostConfig(slack: Slack, user: User?) {
    require(slack.url.contains(Regex("https?://.*/hooks/.*"))) {
        "Wrong webhook url. Should match \"https://.*/hooks/.*\""
    }
}

// SendMessageActionHelper.kt - Message sending
ConfigType.MATTERMOST -> sendSlackMessage(configData as Slack, message, eventStatus, eventSource.referenceId)
```

#### Common-utils Changes

Added `MATTERMOST` to the ConfigType enum and mapped it to use the existing `Slack` reader/parser:

```kotlin
// ConfigType.kt
MATTERMOST("mattermost") {
    override fun toString(): String {
        return tag
    }
}

// ConfigDataProperties.kt
Pair(ConfigType.MATTERMOST, ConfigProperty(Slack.reader, Slack.xParser))
```

#### Dashboards Changes (dashboards-notifications)

New `MattermostSettings` component added with webhook URL input field:

| File | Change |
|------|--------|
| `common/constants.ts` | Added `MATTERMOST: 'mattermost'` to `BACKEND_CHANNEL_TYPE` |
| `models/interfaces.ts` | Added `mattermost?: { url: string }` to `ChannelItemType` |
| `CreateChannel.tsx` | Added Mattermost webhook state and validation |
| `MattermostSettings.tsx` | New component for Mattermost configuration UI |

### Configuration Example

```json
POST _plugins/_notifications/configs
{
  "config_id": "my-mattermost-channel",
  "config": {
    "name": "Mattermost Channel",
    "description": "Send notifications to Mattermost",
    "config_type": "mattermost",
    "is_enabled": true,
    "mattermost": {
      "url": "https://your-mattermost-server.com/hooks/xxx-generatedkey-xxx"
    }
  }
}
```

## Limitations

- URL must match the pattern `https://.*/hooks/.*`
- Uses the same payload format as Slack (`{"text": "message"}`)
- No support for Mattermost-specific features like attachments or custom fields beyond what Slack webhooks support

## References

### Pull Requests
| PR | Repository | Description | Related Issue |
|----|------------|-------------|---------------|
| [#1055](https://github.com/opensearch-project/notifications/pull/1055) | notifications | Add Mattermost as ConfigType for notifications channel | [#1048](https://github.com/opensearch-project/notifications/issues/1048) |
| [#853](https://github.com/opensearch-project/common-utils/pull/853) | common-utils | Add Mattermost as ConfigType for notifications channel | [#1048](https://github.com/opensearch-project/notifications/issues/1048) |
| [#416](https://github.com/opensearch-project/dashboards-notifications/pull/416) | dashboards-notifications | Add Mattermost as a notification channel destination | [#1048](https://github.com/opensearch-project/notifications/issues/1048) |

### Related Issues
- [notifications#1048](https://github.com/opensearch-project/notifications/issues/1048) - [FEATURE] Add support for Mattermost channel as destination
