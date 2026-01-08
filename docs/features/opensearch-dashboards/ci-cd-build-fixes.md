# CI/CD & Build Fixes

## Summary

This feature tracks CI/CD pipeline improvements and build system fixes for OpenSearch Dashboards. It includes GitHub Actions workflow updates, permission configurations, and cross-platform build compatibility enhancements.

## Details

### Architecture

```mermaid
graph TB
    subgraph "GitHub Actions Workflows"
        CY[Cypress Workflow]
        PT[Performance Testing]
    end
    
    subgraph "Build System"
        FS[fs.ts - File Operations]
        CP[cross-platform Package]
    end
    
    CY --> |uses| Cache[actions/cache@v4]
    PT --> |requires| Perms[PR Write Permissions]
    FS --> |uses| CP
    FS --> |handles| WinPath[Windows Long Paths]
    FS --> |implements| Retry[Retry Logic]
```

### Components

| Component | Description |
|-----------|-------------|
| `cypress_workflow.yml` | Cypress test workflow with caching |
| `performance_testing.yml` | Bundle analyzer and performance CI |
| `src/dev/build/lib/fs.ts` | File system operations for build |
| `@osd/cross-platform` | Cross-platform path utilities |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `actions/cache` version | GitHub Actions cache action version | v4 |
| `pull-requests` permission | PR comment write access | write |
| Retry attempts | File deletion retry count | 3 |
| Retry delay | Wait time between retries | 1000ms |

### Usage Example

#### Workflow Permissions Configuration

```yaml
permissions:
  contents: read
  issues: write
  pull-requests: write
```

#### File Deletion with Retry

```typescript
import { standardize } from '@osd/cross-platform';

async function deleteWithRetry(folder: string, log: ToolingLog) {
  if (process.platform === 'win32') {
    folder = standardize(folder, false, false, true);
  }

  for (let i = 0; i < 3; i++) {
    try {
      await rm(folder, { force: true, recursive: true });
      return;
    } catch (err) {
      if (i === 2) throw err;
      log.debug(`Retry ${i + 1}/3 on ${folder}, waiting for 1000ms`);
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }
}
```

## Limitations

- Retry logic may add latency to builds (up to 3 seconds per failed deletion)
- Windows long path support requires extended path prefix (`\\?\`)

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.0.0 | [#9366](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9366) | Update actions/cache from v1 to v4 |
| v3.0.0 | [#9534](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9534) | Add PR write permission |
| v3.0.0 | [#9581](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9581) | Fix bundler performance testing permissions |
| v3.0.0 | [#9561](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9561) | Windows longpath support with retry |

## References

- [Issue #9397](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9397): Windows build failure
- [Issue #3747](https://github.com/opensearch-project/opensearch-build/issues/3747): opensearch-build Windows issue
- [GitHub Actions Cache](https://github.com/actions/cache): Official cache action

## Change History

- **v3.0.0** (2025-05-06): Initial implementation with cache update, workflow permissions, and Windows build fixes
