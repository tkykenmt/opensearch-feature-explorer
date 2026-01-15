---
tags:
  - opensearch-dashboards
---
# Data Set Navigator

## Summary

This release re-adds the Data Set Navigator component to the control state in OpenSearch Dashboards. The Data Set Navigator is part of the "discover-next" feature that enables users to select and manage datasets when the query enhancements toggle is enabled. This change introduces a new `DataSetManager` service for managing dataset state and integrates it with the query state synchronization system.

## Details

### What's New in v2.16.0

The PR adds back the Data Set Navigator component that was temporarily removed during other changes. Key additions include:

1. **DataSetManager Service**: A new service (`DataSetManager`) that manages the current dataset state with reactive updates via RxJS observables
2. **Dataset State Synchronization**: Integration with the query state sync system to persist dataset selection in URL state
3. **UI Component Export**: The `DataSetNavigator` component is now exported from the data plugin's public API
4. **Data Types**: New TypeScript types for `SimpleDataSet`, `SimpleDataSource`, and related enums

### Technical Changes

#### New DataSetManager Service

```typescript
// src/plugins/data/public/query/dataset_manager/dataset_manager.ts
export class DataSetManager {
  private dataSet$: BehaviorSubject<SimpleDataSet | undefined>;
  
  public init = async (indexPatterns: IndexPatternsContract) => {...};
  public getUpdates$ = () => this.dataSet$.asObservable().pipe(skip(1));
  public getDataSet = () => this.dataSet$.getValue();
  public setDataSet = (dataSet: SimpleDataSet | undefined) => {...};
  public getDefaultDataSet = () => this.defaultDataSet;
}
```

#### New Data Types

| Type | Description |
|------|-------------|
| `SIMPLE_DATA_SOURCE_TYPES` | Enum for data source types (`data-source`, `external-source`) |
| `SIMPLE_DATA_SET_TYPES` | Enum for dataset types (`index-pattern`, `temporary`, `temporary-async`) |
| `SimpleDataSet` | Interface for dataset with id, title, fields, timeFieldName |
| `SimpleDataSource` | Interface for data source with id, name, indices, tables |
| `DataFrameQueryConfig` | Configuration for dataframe queries |

#### Query State Integration

The dataset state is now synchronized with URL state through `connectStorageToQueryState` and `connectToQueryState` functions, allowing dataset selection to persist across page navigation.

#### Exported APIs

New exports from `@opensearch-project/opensearch-dashboards/data`:
- `DataSetNavigator` - UI component for dataset selection
- `DataSetManager` - Service for managing dataset state
- `DataSetContract` - Type definition for the service contract
- `setAsyncSessionId`, `getAsyncSessionId`, `setAsyncSessionIdByObj` - Session management utilities

### Configuration

The Data Set Navigator is enabled when the query enhancements setting is turned on:

| Setting | Description | Default |
|---------|-------------|---------|
| `query:enhancements:enabled` | Enable query enhancements including Data Set Navigator | `false` |
| `home:useNewHomePage` | Enable new home page (used with enhancements) | `false` |

## Limitations

- The Data Set Navigator only appears when `query:enhancements:enabled` is set to `true`
- Dataset state synchronization requires the query enhancements feature flag
- Some dashboard listing tests were skipped due to state management changes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7492](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7492) | Add back data set navigator to control state | N/A |
| [#7532](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7532) | Backport to 2.x branch | N/A |
| [#7542](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7542) | Update fetch functions to include local cluster | N/A |
| [#7546](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7546) | Fixes Discover next styling | N/A |
| [#7552](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7552) | Fix query assist after data set navigator changes | N/A |
| [#7566](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7566) | Fixes dataset navigator menu styling & search error toast | N/A |
