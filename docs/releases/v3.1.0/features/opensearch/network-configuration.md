---
tags:
  - domain/core
  - component/server
  - search
---
# Network Configuration

## Summary

This release fixes a critical bug where OpenSearch failed to start on systemd-based Linux distributions (such as Debian 12) when using `network.host: 0.0.0.0`. The issue occurred because the systemd service file was missing the `seccomp` system call in its `SystemCallFilter` configuration, preventing OpenSearch's bootstrap checks from completing successfully.

## Details

### What's New in v3.1.0

The `seccomp` system call has been added to the `SystemCallFilter` directive in the OpenSearch systemd service file. This allows OpenSearch to properly install its system call filters when binding to non-loopback addresses.

### Technical Changes

#### Root Cause

When `network.host` is set to `0.0.0.0` (or any non-loopback address), OpenSearch triggers production-mode bootstrap checks. One of these checks verifies that system call filters are properly installed using the `seccomp` system call. However, the systemd service file's `SystemCallFilter` directive was blocking this call, causing the bootstrap check to fail with:

```
system call filters failed to install; check the logs and fix your configuration
```

The underlying error in logs showed:
```
java.lang.UnsupportedOperationException: seccomp(BOGUS_OPERATION): Operation not permitted
```

#### Fix Applied

The systemd service file (`opensearch.service`) was updated to allow the `seccomp` and `mincore` system calls:

**Before:**
```ini
SystemCallFilter=madvise mincore mlock mlock2 munlock get_mempolicy sched_getaffinity sched_setaffinity fcntl
```

**After:**
```ini
SystemCallFilter=seccomp mincore
SystemCallFilter=madvise mlock mlock2 munlock get_mempolicy sched_getaffinity sched_setaffinity fcntl
```

#### Affected File

| File | Description |
|------|-------------|
| `distribution/packages/src/common/systemd/opensearch.service` | Systemd unit file for OpenSearch service |

### Configuration Context

The `network.host` setting controls which network interfaces OpenSearch binds to:

| Setting | Description | Default |
|---------|-------------|---------|
| `network.host` | Binds OpenSearch to an address. Use `0.0.0.0` for all interfaces | `_local_` (loopback only) |
| `network.bind_host` | Address for incoming connections | Value of `network.host` |
| `network.publish_host` | Address published to other nodes | Value of `network.host` |

When `network.host` is set to a non-loopback address, OpenSearch enforces production bootstrap checks including system call filter verification.

### Migration Notes

Users who previously worked around this issue by manually editing `/lib/systemd/system/opensearch.service` should:

1. Remove any manual modifications to the systemd service file
2. Upgrade to v3.1.0 or later
3. Reload systemd: `sudo systemctl daemon-reload`
4. Restart OpenSearch: `sudo systemctl restart opensearch`

## Limitations

- This fix only applies to systemd-based installations (RPM/DEB packages)
- Docker and tarball installations are not affected as they don't use systemd

## References

### Documentation
- [Network Settings Documentation](https://docs.opensearch.org/3.0/install-and-configure/configuring-opensearch/network-settings/): Official network configuration guide

### Pull Requests
| PR | Description |
|----|-------------|
| [#18309](https://github.com/opensearch-project/OpenSearch/pull/18309) | Add seccomp in systemd config |

### Issues (Design / RFC)
- [Issue #18273](https://github.com/opensearch-project/OpenSearch/issues/18273): Bug report - 3.0.0 fails to start on Debian due to bootstrap checks

## Related Feature Report

- Full feature documentation
