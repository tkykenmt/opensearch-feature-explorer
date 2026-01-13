---
tags:
  - domain/ml
  - component/dashboards
  - dashboards
  - security
---
# Dashboards Assistant Bugfixes

## Summary

This release includes two bugfixes for the Dashboards Assistant plugin: a fix for the text-to-visualization header display and a fix for capability services access settings before login.

## Details

### What's New in v3.4.0

#### Text2Viz Header Fix

The text-to-visualization (text2viz) feature had an incorrect header display. This fix corrects the header rendering to properly display the feature title.

#### Capability Services Access Settings Fix

Fixed an issue where capability services were being accessed before user login, which caused the browser to display an unwanted login dialog. This fix ensures that capability services settings are properly handled before authentication.

### Technical Changes

| Fix | Description | Impact |
|-----|-------------|--------|
| Text2Viz Header | Corrects header display in text-to-visualization | Improved UI consistency |
| Capability Services | Fixes settings access before login | Prevents unwanted browser login dialogs |

## Limitations

None identified.

## References

### Documentation
- [dashboards-investigation#244](https://github.com/opensearch-project/dashboards-investigation/pull/244): Related fix for capability services

### Pull Requests
| PR | Description |
|----|-------------|
| [#627](https://github.com/opensearch-project/dashboards-assistant/pull/627) | Fix text2viz header |
| [#628](https://github.com/opensearch-project/dashboards-assistant/pull/628) | Fix capability services access settings before login |
