# GitHub Actions Updates

## Summary

This release includes updates to GitHub Actions dependencies across the security and security-dashboards-plugin repositories. These updates ensure CI/CD workflows use the latest action versions with Node.js 24 support, improved security, and enhanced functionality.

## Details

### What's New in v3.4.0

The security repositories updated their GitHub Actions dependencies to newer major versions, primarily to support Node.js 24 runtime and benefit from security improvements.

### Technical Changes

#### Updated Actions in security Repository

| Action | Previous Version | New Version | Key Changes |
|--------|------------------|-------------|-------------|
| `actions/checkout` | 5 | 6 | Node.js 24 support, credentials stored in separate file |
| `actions/upload-artifact` | 4 | 5 | Node.js 24 support |
| `actions/download-artifact` | 5 | 6 | Node.js 24 support |
| `github/codeql-action` | 3 | 4 | Node.js 24 support, improved telemetry |
| `stefanzweifel/git-auto-commit-action` | 6 | 7 | Node.js 24 support, restored skip_fetch/skip_checkout/create_branch options, tag message support |
| `derek-ho/start-opensearch` | 7 | 8 | Added resource-sharing feature option for cypress tests |

#### Updated Actions in security-dashboards-plugin Repository

| Action | Previous Version | New Version | Key Changes |
|--------|------------------|-------------|-------------|
| `actions/checkout` | 5 | 6 | Node.js 24 support, credentials stored in separate file |
| `actions/setup-java` | 4 | 5 | Node.js 24 support, improved error handling |
| `stefanzweifel/git-auto-commit-action` | 6 | 7 | Node.js 24 support, restored options |
| `derek-ho/setup-opensearch-dashboards` | 1 | 3 | Retry on download step, custom plugin suffix support |
| `Wandalen/wretry.action` | 3.3.0 | 3.8.0 | Added pre_retry_command option, complex expressions support |

### Migration Notes

These are automated dependency updates managed by Dependabot. No manual migration is required for users of OpenSearch Security.

For workflow maintainers:
- Ensure GitHub Actions runners are updated to v2.327.1 or newer for Node.js 24 support
- `actions/checkout@v6` stores credentials in `$RUNNER_TEMP` instead of local git config

## Limitations

- Node.js 24 runtime requires Actions Runner v2.327.1 or newer
- Some actions may have breaking changes in their major version updates

## References

### Documentation
- [actions/checkout v6 Release](https://github.com/actions/checkout/releases/tag/v6.0.0)
- [actions/upload-artifact v5 Release](https://github.com/actions/upload-artifact/releases/tag/v5.0.0)
- [actions/download-artifact v6 Release](https://github.com/actions/download-artifact/releases/tag/v6.0.0)
- [actions/setup-java v5 Release](https://github.com/actions/setup-java/releases/tag/v5.0.0)
- [github/codeql-action v4](https://github.com/github/codeql-action)
- [stefanzweifel/git-auto-commit-action v7 Release](https://github.com/stefanzweifel/git-auto-commit-action/releases/tag/v7.0.0)

### Pull Requests
| PR | Description |
|----|-------------|
| [#5810](https://github.com/opensearch-project/security/pull/5810) | Bump actions/checkout from 5 to 6 |
| [#5740](https://github.com/opensearch-project/security/pull/5740) | Bump actions/upload-artifact from 4 to 5 |
| [#5739](https://github.com/opensearch-project/security/pull/5739) | Bump actions/download-artifact from 5 to 6 |
| [#5704](https://github.com/opensearch-project/security/pull/5704) | Bump stefanzweifel/git-auto-commit-action from 6 to 7 |
| [#5702](https://github.com/opensearch-project/security/pull/5702) | Bump github/codeql-action from 3 to 4 |
| [#5630](https://github.com/opensearch-project/security/pull/5630) | Bump derek-ho/start-opensearch from 7 to 8 |
| PR | Description |
|----|-------------|
| [#2339](https://github.com/opensearch-project/security-dashboards-plugin/pull/2339) | Bump actions/checkout from 5 to 6 |
| [#2329](https://github.com/opensearch-project/security-dashboards-plugin/pull/2329) | Bump stefanzweifel/git-auto-commit-action from 6 to 7 |
| [#2323](https://github.com/opensearch-project/security-dashboards-plugin/pull/2323) | Bump actions/setup-java from 4 to 5 |
| [#2322](https://github.com/opensearch-project/security-dashboards-plugin/pull/2322) | Bump Wandalen/wretry.action from 3.3.0 to 3.8.0 |
| [#2321](https://github.com/opensearch-project/security-dashboards-plugin/pull/2321) | Bump derek-ho/setup-opensearch-dashboards from 1 to 3 |

## Related Feature Report

- [Full feature documentation](../../../features/security/github-actions-updates.md)
