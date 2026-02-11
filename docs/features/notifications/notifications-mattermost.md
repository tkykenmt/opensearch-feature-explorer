---
tags:
  - notifications
---
# Mattermost Notifications

## Summary

Mattermost notification channel support enables OpenSearch to send notifications directly to Mattermost servers via incoming webhooks. This feature provides native integration for organizations using Mattermost as their team communication platform, allowing alerts, reports, and other notifications to be delivered to Mattermost channels.

## Details

### Architecture

```mermaid
graph TB
    subgraph "OpenSearch Cluster"
        A[Alerting Plugin] --> N[Notifications Plugin]
        B[Reporting Plugin] --> N
        C[Index Management] --> N
    end
    
    subgraph "Notifications Core"
        N --> T[Transport Layer]
        T --> WH[Webhook Client]
    end
    
    subgraph "Mattermost"
        WH -->|POST {"text": "..."}| MW[Mattermost Webhook]
        MW --> MC[Mattermost Channel]
    end
```

### Components

| Component | Description |
|-----------|-------------|
| `ConfigType.MATTERMOST` | Enum value identifying Mattermost channel type |
| `MattermostSettings` | Dashboards UI component for configuration |
| `Slack` (reused) | Data model for webhook URL storage |
| `sendSlackMessage` (reused) | Message delivery function |

### Configuration

| Setting | Description | Example |
|---------|-------------|---------|
| `config_type` | Must be `"mattermost"` | `"mattermost"` |
| `mattermost.url` | Mattermost incoming webhook URL | `https://mattermost.example.com/hooks/xxx` |

### URL Validation

Mattermost webhook URLs must match the pattern:
```
https?://.*/hooks/.*
```

This is more flexible than Slack's validation (`https://hooks\.(?:gov-)?slack\.com/services`) to accommodate self-hosted Mattermost instances.

### Usage Example

#### Create Mattermost Channel via API

```json
POST _plugins/_notifications/configs
{
  "config_id": "mattermost-alerts",
  "config": {
    "name": "Mattermost Alerts",
    "description": "Send alerts to Mattermost",
    "config_type": "mattermost",
    "is_enabled": true,
    "mattermost": {
      "url": "https://your-mattermost-server.com/hooks/xxx-generatedkey-xxx"
    }
  }
}
```

#### Use in Alerting Monitor

```json
{
  "trigger": {
    "name": "High CPU Alert",
    "actions": [
      {
        "name": "Notify Mattermost",
        "destination_id": "mattermost-alerts",
        "message_template": {
          "source": "CPU usage exceeded threshold: {{ctx.results.0.hits.total.value}} events"
        }
      }
    ]
  }
}
```

### Message Format

Mattermost receives messages in the same format as Slack:

```json
{
  "text": "Your notification message here"
}
```

## Limitations

- **Payload format**: Only supports the basic `{"text": "..."}` format; Mattermost-specific features like attachments, buttons, or custom fields are not supported
- **URL pattern**: Must contain `/hooks/` in the path
- **HTTPS recommended**: While HTTP is technically supported, HTTPS is strongly recommended for security

## Change History

- **v3.5.0** (2026-01-27): Initial implementation - Added Mattermost as a native notification channel type

## References

### Documentation
- [Mattermost Incoming Webhooks](https://developers.mattermost.com/integrate/webhooks/incoming/)
- [OpenSearch Notifications Plugin](https://github.com/opensearch-project/notifications)

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v3.5.0 | [notifications#1055](https://github.com/opensearch-project/notifications/pull/1055) | Add Mattermost as ConfigType for notifications channel |
| v3.5.0 | [common-utils#853](https://github.com/opensearch-project/common-utils/pull/853) | Add Mattermost as ConfigType for notifications channel |
| v3.5.0 | [dashboards-notifications#416](https://github.com/opensearch-project/dashboards-notifications/pull/416) | Add Mattermost as a notification channel destination |

### Related Issues
- [notifications#1048](https://github.com/opensearch-project/notifications/issues/1048) - Feature request for Mattermost support
