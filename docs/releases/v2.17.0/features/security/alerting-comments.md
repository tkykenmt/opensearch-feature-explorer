# Alerting Comments Security Actions

## Summary

This bugfix adds and corrects security actions for the Alerting Comments feature in the Security plugin's `roles.yml`. The changes ensure proper role-based access control for alerting comments, allowing users with appropriate roles to create, read, update, and delete comments on alerts.

## Details

### What's New in v2.17.0

Two key changes were made to the security roles configuration:

1. **Added comments search permission to alerting roles**: The `alerting_read_access` and `alerting_ack_alerts` roles now include the `cluster:admin/opensearch/alerting/comments/search` permission, enabling users to view comments on alerts.

2. **Expanded comments permission for `alerting_ack_alerts` role**: Changed from search-only (`cluster:admin/opensearch/alerting/comments/search`) to full access (`cluster:admin/opensearch/alerting/comments/*`), allowing users who can acknowledge alerts to also create, edit, and delete comments.

### Technical Changes

#### Security Role Updates

| Role | Before | After |
|------|--------|-------|
| `alerting_read_access` | No comments permission | `cluster:admin/opensearch/alerting/comments/search` |
| `alerting_ack_alerts` | `cluster:admin/opensearch/alerting/comments/search` | `cluster:admin/opensearch/alerting/comments/*` |
| `alerting_full_access` | Already has full access | No change |

#### Configuration Changes

The `config/roles.yml` file was updated:

```yaml
# alerting_read_access role - added:
- 'cluster:admin/opensearch/alerting/comments/search'

# alerting_ack_alerts role - changed from:
- 'cluster:admin/opensearch/alerting/comments/search'
# to:
- 'cluster:admin/opensearch/alerting/comments/*'
```

### Usage Example

Users with the `alerting_ack_alerts` role can now perform all comment operations:

```bash
# Search comments (was already possible)
GET _plugins/_alerting/comments/_search

# Create comment (now possible with alerting_ack_alerts)
POST _plugins/_alerting/comments
{
  "alert_id": "alert-123",
  "content": "Investigating this alert"
}

# Update comment (now possible with alerting_ack_alerts)
PUT _plugins/_alerting/comments/{comment_id}
{
  "content": "Updated investigation notes"
}

# Delete comment (now possible with alerting_ack_alerts)
DELETE _plugins/_alerting/comments/{comment_id}
```

### Migration Notes

No migration required. The updated roles are automatically applied when upgrading to v2.17.0. Existing users mapped to `alerting_ack_alerts` will gain full comment access.

## Limitations

- Comment permissions are inherited from the monitor's backend roles
- If the Security plugin is not installed, comment authors display as "Unknown"

## Related PRs

| PR | Description |
|----|-------------|
| [security#4700](https://github.com/opensearch-project/security/pull/4700) | [Backport 2.x] Adding alerting comments security actions to roles.yml |
| [security#4724](https://github.com/opensearch-project/security/pull/4724) | [Backport 2.17] Changing comments permission for alerting_ack_alerts role |
| [security#4699](https://github.com/opensearch-project/security/pull/4699) | Adding alerting comments security actions to roles.yml (main) |
| [security#4709](https://github.com/opensearch-project/security/pull/4709) | Changing comments permission for alerting_ack_alerts role (main) |

## References

- [Alerting Comments Documentation](https://docs.opensearch.org/2.17/observing-your-data/alerting/comments/): Official documentation for alerting comments
- [Alerting Security Documentation](https://docs.opensearch.org/2.17/observing-your-data/alerting/security/): Security configuration for alerting
- [alerting#1561](https://github.com/opensearch-project/alerting/pull/1561): Alerting Comments feature implementation

## Related Feature Report

- [Full feature documentation](../../../features/security/alerting-comments-security.md)
