---
tags:
  - domain/observability
  - component/server
  - dashboards
  - indexing
---
# Notifications Maintenance

## Summary

This release includes maintenance updates for the OpenSearch Notifications plugin, focusing on dependency modernization and version alignment. The key change is the migration from `javax.mail` to `jakarta.mail` APIs to avoid version conflicts with other OpenSearch components.

## Details

### What's New in v3.1.0

The Notifications plugin received two maintenance updates:

1. **Jakarta Mail Migration**: Upgraded from deprecated `javax.mail` (JavaMail 1.6.2) to `jakarta.mail` (Jakarta Mail 2.0.1) to resolve version conflicts and align with modern Java EE standards.

2. **Version Increment**: Standard version bump to 3.1.0-SNAPSHOT for the new release cycle.

### Technical Changes

#### Dependency Updates

| Old Dependency | New Dependency | Version |
|----------------|----------------|---------|
| `com.sun.mail:javax.mail` | `com.sun.mail:jakarta.mail` | 1.6.2 → 2.0.1 |
| `javax.activation:activation` | `com.sun.activation:jakarta.activation` | 1.1 → 2.0.1 |
| `com.icegreen:greenmail` | `com.icegreen:greenmail` | 1.6.14 → 2.0.1 |

#### Code Changes

The migration required updating import statements across multiple Kotlin files:

| File | Change |
|------|--------|
| `DestinationSesClient.kt` | `javax.mail.*` → `jakarta.mail.*` |
| `DestinationSmtpClient.kt` | `javax.mail.*` → `jakarta.mail.*` |
| `EmailMimeProvider.kt` | `javax.activation.*`, `javax.mail.*` → `jakarta.*` |
| `SesDestinationTransport.kt` | `javax.mail.*` → `jakarta.mail.*` |
| `SmtpDestinationTransport.kt` | `javax.mail.*` → `jakarta.mail.*` |
| `SmtpDestinationTests.kt` | `javax.mail.*` → `jakarta.mail.*` |

### Migration Notes

This is a transparent change for users. The Jakarta Mail API is backward compatible with the JavaMail API at the functional level. No configuration changes are required.

For plugin developers extending the Notifications plugin:
- Update any custom code using `javax.mail` imports to use `jakarta.mail`
- Ensure your dependencies don't conflict with Jakarta Mail 2.0.1

## Limitations

- No functional changes or new features in this release
- This is purely a maintenance/dependency update

## References

### Documentation
- [Jakarta Mail 2.0 Specification](https://jakarta.ee/specifications/mail/2.0/)
- [OpenSearch Notifications Repository](https://github.com/opensearch-project/notifications)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1036](https://github.com/opensearch-project/notifications/pull/1036) | Upgrade javax to jakarta to avoid version conflicts |
| [#1027](https://github.com/opensearch-project/notifications/pull/1027) | Increment version to 3.1.0-SNAPSHOT |

## Related Feature Report

- [Full feature documentation](../../../features/notifications/notifications-plugin.md)
