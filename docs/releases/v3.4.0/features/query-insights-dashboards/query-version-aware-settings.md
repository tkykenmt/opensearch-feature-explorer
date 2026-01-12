---
tags:
  - dashboards
  - performance
  - search
---

# Query Version-Aware Settings

## Summary

This release adds version-aware settings support to the Query Insights Dashboards plugin, enabling the UI to dynamically adapt its features based on the connected OpenSearch cluster version. This ensures backward compatibility when connecting to older clusters and prevents errors from calling APIs that don't exist in earlier versions.

## Details

### What's New in v3.4.0

The Query Insights Dashboards plugin now detects the OpenSearch cluster version and conditionally enables or disables features accordingly:

- **Live Queries tab**: Only shown for OpenSearch 3.1.0 or higher
- **Workload Management (WLM) features**: Only enabled for OpenSearch 3.3.0 or higher
- **WLM Group selector and stats panels**: Conditionally rendered based on version support

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Query Insights Dashboards"
        A[Application Mount] --> B[Service Initialization]
        B --> C[RouteService]
        C --> D[/api/cluster/version]
        D --> E[Version Cache]
        
        E --> F{Version Check}
        F -->|>= 3.1.0| G[Show Live Queries Tab]
        F -->|< 3.1.0| H[Hide Live Queries Tab]
        
        F -->|>= 3.3.0| I[Enable WLM Features]
        F -->|< 3.3.0| J[Disable WLM Features]
    end
    
    subgraph "OpenSearch Cluster"
        K[Cluster Info API]
    end
    
    D --> K
```

#### New Components

| Component | Description |
|-----------|-------------|
| `RouteService` | Service class for making HTTP requests, including cluster version retrieval |
| `version-utils.ts` | Utility functions for version comparison and caching |
| `service.ts` | Centralized service registry using getter/setter pattern |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `DEFAULT_SHOW_LIVE_QUERIES_ON_ERROR` | Whether to show Live Queries tab when version check fails | `false` |

#### API Changes

New server-side endpoint added:

```
GET /api/cluster/version
```

Returns:
```json
{
  "ok": true,
  "version": "3.4.0"
}
```

The deprecated `/api/cat_plugins` endpoint was removed in favor of direct API calls to check feature availability.

### Usage Example

The version utilities provide semantic version comparison:

```typescript
import { getVersionOnce, isVersion31OrHigher, isVersion33OrHigher } from './utils/version-utils';

// Get version (cached after first call per data source)
const version = await getVersionOnce(dataSourceId);

// Check version thresholds
if (isVersion31OrHigher(version)) {
  // Show Live Queries tab
}

if (isVersion33OrHigher(version)) {
  // Enable WLM features
}
```

### Migration Notes

- No user action required - the plugin automatically detects cluster version
- When connecting to clusters older than 3.1.0, the Live Queries tab will not appear
- When connecting to clusters older than 3.3.0, WLM-related UI elements (workload group selector, stats panels, WLM Group column) will be hidden

## Limitations

- Version detection requires a successful API call to the cluster
- If version detection fails, Live Queries tab defaults to hidden (`DEFAULT_SHOW_LIVE_QUERIES_ON_ERROR = false`)
- Version is cached per data source ID; changing data sources triggers a new version check

## References

### Documentation
- [Query Insights Dashboards Documentation](https://docs.opensearch.org/3.4/observing-your-data/query-insights/query-insights-dashboard/)
- [Live Queries Documentation](https://docs.opensearch.org/3.4/observing-your-data/query-insights/live-queries/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#407](https://github.com/opensearch-project/query-insights-dashboards/pull/407) | Add version-aware settings support |
| [#403](https://github.com/opensearch-project/query-insights-dashboards/pull/403) | MDS support for live queries page |

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights.md)
