---
tags:
  - opensearch-dashboards
---
# Data Source Form Tests

## Summary

OpenSearch Dashboards v2.16.0 adds comprehensive unit test coverage for the Data Source Management plugin's form components, including edit data source form, multi-selectable component, error menu, data source item, toast buttons, and validation form.

## Details

### What's New in v2.16.0

This release adds unit tests for multiple components in the `data_source_management` plugin to improve code quality and prevent regressions.

#### Edit Data Source Form Tests
Tests for the edit data source form covering:
- Username & Password authentication: title validation, username/password required fields, update password modal, credential type switching, form reset, and save changes
- No Authentication: credential type switching, form validation, delete/set default actions, test connection
- AWS SigV4 authentication: access key/secret key validation, update credentials modal, form reset and save
- Registered authentication types: custom credential form rendering and save

#### Multi-Selectable Component Tests
Tests for `DataSourceMultiSelectable` component:
- Rendering with local cluster visible/hidden
- Toast notifications on exceptions
- onChange callback handling
- UI settings integration for default data source
- No available data source error handling

#### Data Source Item Tests
Tests for `ShowDataSourceOption` component:
- Label rendering
- Default badge display
- Default data source indicator

#### Toast Button Tests
Tests for `ManageDataSourceButton` and `ReloadButton`:
- Button rendering with correct labels
- Navigation to management app on click
- Window reload functionality

#### Validation Form Tests
Tests for `datasource_form_validation`:
- Title validation (empty, duplicate, length limit)
- Endpoint validation
- Username/password required field validation for Username & Password auth
- Access key/secret key required field validation for SigV4 auth
- No Auth credential type handling
- Registered auth type validation

## Limitations

- Tests are focused on unit testing; integration tests for end-to-end flows are not included

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6742](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6742) | Add test for edit data source form | [#6741](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6741) |
| [#6752](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6752) | Add test for error_menu, item, data_source_multi_selectable | [#6748](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6748), [#6749](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6749), [#6750](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6750) |
| [#6755](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6755) | Add test for toast button and validation form | - |
