---
tags:
  - opensearch-dashboards
---
# Query Editor & Enhancements

## Summary

OpenSearch Dashboards v2.16.0 introduces a major overhaul of the query editing experience with a new Query Editor component, Query Editor Extensions framework, and the Query Enhancements plugin as a core plugin. These changes enable support for multiple query languages (DQL, PPL, SQL), extensible UI components, and enhanced search capabilities.

## Details

### What's New in v2.16.0

#### New Query Editor Component
The new Query Editor replaces the legacy query string input with a Monaco-based editor that supports:
- Multiple query languages (DQL, PPL, SQL)
- Syntax highlighting and autocomplete
- Single-line and multi-line editing modes
- Language selector with UI toggle

#### Query Editor Extensions Framework
A new extension point allows plugins to add custom UI components to the query editor:

```typescript
export interface QueryEditorExtensionConfig {
  id: string;
  order: number;
  isEnabled: (dependencies: QueryEditorExtensionDependencies) => Promise<boolean>;
  getComponent?: (dependencies: QueryEditorExtensionDependencies) => React.ReactElement | null;
  getBanner?: (dependencies: QueryEditorExtensionDependencies) => React.ReactElement | null;
}
```

Extensions can:
- Display UI components above the query editor
- Show banners above the language selector
- React to data source and language changes via observables

#### Query Enhancements Plugin (Core)
The Query Enhancements plugin is now a core plugin providing:
- PPL and SQL search interceptors
- Query Assist feature for natural language queries
- Data source connection management
- Server-side search strategies for PPL/SQL

#### Data Source Container
Plugins can mount custom data source selector components to the query editor, enabling flexible data source selection UI.

### Technical Changes

#### Configuration
Two settings control the feature:
- `data.enhancements.enabled` (config file): Master toggle for the feature
- `query:enhancements:enabled` (Advanced Settings): User-facing toggle

Both must be enabled for the new query editor to render.

#### Plugin Structure
```
src/plugins/query_enhancements/
├── opensearch_dashboards.json
├── common/config.ts
├── public/
│   ├── plugin.tsx
│   ├── query_assist/
│   │   └── components/query_assist_bar.tsx
│   ├── search/
│   │   ├── ppl_search_interceptor.ts
│   │   ├── sql_search_interceptor.ts
│   │   └── sql_async_search_interceptor.ts
│   └── data_source_connection/
└── server/
    ├── plugin.ts
    ├── routes/query_assist/
    └── search/
        ├── ppl_search_strategy.ts
        ├── sql_search_strategy.ts
        └── sql_async_search_strategy.ts
```

#### Observable-based Extension Enablement
The `isEnabled` property was changed from a Promise-based function to an Observable, allowing extensions to dynamically update their enabled state when the selected data source connection changes.

### UI Changes

The new query editor UI includes:
- Monaco editor with language-specific syntax highlighting
- Language selector dropdown
- Data source selector container
- Extension component slots (above editor and banner areas)

## Limitations

- Feature is disabled by default; requires explicit configuration
- When toggling off enhancements, query language resets to DQL
- PPL and SQL functionality requires the Query Enhancements plugin

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7001](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7001) | Query editor and UI settings toggle | [#6067](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6067) |
| [#7034](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7034) | Add query editor extensions | [#6077](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6077) |
| [#7157](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7157) | Query editor and dataframes datasources container | [#7129](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7129) |
| [#7183](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7183) | Change `isEnabled` to an observable | [#7034](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7034) |
| [#7212](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7212) | Add query enhancements plugin as a core plugin | [#6072](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6072) |
| [#7309](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7309) | Update query enhancement UI | [#7038](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7038) |

### Related Issues
- [#6067](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6067): Query editor and UI settings toggle
- [#6072](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6072): Query enhancements plugin
- [#6074](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6074): Related feature
- [#6075](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6075): Related feature
- [#6077](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6077): Query editor extensions
- [#7038](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7038): Query enhancement UI
- [#7129](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7129): Data source container
