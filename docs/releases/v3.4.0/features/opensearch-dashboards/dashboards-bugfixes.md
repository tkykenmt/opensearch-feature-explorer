# Dashboards Bugfixes

## Summary

This release includes several important bugfixes across OpenSearch Dashboards and related plugins, addressing issues with SQL query parsing, security vulnerabilities, XSS protection, and dashboard embeddable error handling.

## Details

### What's New in v3.4.0

This release addresses multiple bugfixes across the OpenSearch Dashboards ecosystem:

1. **SQL Query Parser Fix**: Resolves an issue where table identifiers containing wildcards (`*`) were incorrectly flagged as errors
2. **Axios Security Update**: Upgrades Axios to v1.12 to address CVE-2025-58754
3. **DOMPurify Import Fix**: Adds missing DOMPurify import for XSS protection
4. **Dashboard Utilities Type Checks**: Adds type checking to dashboard utilities to support index datasets in saved objects
5. **Text2Viz Header Fix**: Corrects the header display in the text-to-visualization feature
6. **Capability Services Fix**: Fixes capability services access settings before login to prevent browser dialog issues
7. **Workflow Resource Handling**: Gracefully handles workflows with no provisioned resources

### Technical Changes

#### OpenSearch-Dashboards Core Fixes

| Fix | Description | Impact |
|-----|-------------|--------|
| TableIdents with `*` | Temporarily handles table identifiers with wildcards until grammar is fixed | Prevents false error flagging in SQL queries |
| Axios CVE Fix | Updates axios to ^1.12.0 with TypeScript patch | Addresses CVE-2025-58754 security vulnerability |
| DOMPurify Import | Adds missing dompurify import | Ensures XSS protection is properly applied |
| Type Checks | Adds type checking to dashboard utilities | Enables viewing saved objects with index datasets |

#### Dashboards Assistant Fixes

| Fix | Description | Impact |
|-----|-------------|--------|
| Text2Viz Header | Fixes header display in text-to-visualization | Improves UI consistency |
| Capability Services | Fixes settings access before login | Prevents unwanted browser login dialogs |

#### Dashboards Flow Framework Fixes

| Fix | Description | Impact |
|-----|-------------|--------|
| No Provisioned Resources | Gracefully handles workflows without resources | Improves UX for agentic search workflows |

### Migration Notes

For the Axios upgrade, a TypeScript patch is applied using `patch-package` to handle a breaking change in axios v1.12.0 where the `cause` property type changed from `Error | undefined` to `unknown`.

## Limitations

- The TableIdents fix is a temporary workaround until the SQL grammar is properly updated (tracked in [opensearch-project/sql#4444](https://github.com/opensearch-project/sql/issues/4444))

## Related PRs

| PR | Repository | Description |
|----|------------|-------------|
| [#10687](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10687) | OpenSearch-Dashboards | Fix TableIdents with * |
| [#10688](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10688) | OpenSearch-Dashboards | Upgrade Axios for CVE-2025-58754 |
| [#10691](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10691) | OpenSearch-Dashboards | Add dompurify import |
| [#10693](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10693) | OpenSearch-Dashboards | Add type checks to dashboard utilities |
| [#627](https://github.com/opensearch-project/dashboards-assistant/pull/627) | dashboards-assistant | Fix text2viz header |
| [#628](https://github.com/opensearch-project/dashboards-assistant/pull/628) | dashboards-assistant | Fix capability services access settings |
| [#821](https://github.com/opensearch-project/dashboards-flow-framework/pull/821) | dashboards-flow-framework | Gracefully handle workflows with no provisioned resources |

## References

- [Issue #10523](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/10523): Axios CVE tracking
- [Issue #10685](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/10685): Axios CVE tracking
- [Issue #4444](https://github.com/opensearch-project/sql/issues/4444): SQL grammar fix for TableIdents
- [Axios PR #6982](https://github.com/axios/axios/pull/6982): Breaking TypeScript change
- [Axios Issue #7059](https://github.com/axios/axios/issues/7059): TypeScript type issue
