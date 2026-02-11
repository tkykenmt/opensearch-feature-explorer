---
tags:
  - dashboards
---
# Dashboards Dependencies

## Summary

OpenSearch Dashboards v3.5.0 includes a significant set of dependency updates across both the core OpenSearch-Dashboards repository and the dashboards-assistant plugin. The most notable changes are the Node.js upgrade from v20 to v22 (22.21.1 → 22.22.0), the replacement of `handlebars` with `kbn-handlebars` to eliminate CSP `unsafe-eval` violations, and security-driven bumps to lodash, axios, and other packages.

## Details

### What's New in v3.5.0

#### Node.js Upgrade to v22

The runtime was upgraded from Node.js 20.18.3 to 22.21.1 ([#11076](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11076)), then further to 22.22.0 ([#11218](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11218)). This aligns OpenSearch Dashboards with the latest LTS Node.js version. Key compatibility changes include:

- Updated stream `destroy()` method signatures for Node.js 22 semantics
- Suppressed new deprecation warnings (`MODULE_TYPELESS_PACKAGE_JSON`, `fs.Stats constructor`)
- Updated test snapshots for Node.js 22 output changes
- Widened engine requirement in `package.json` from `<21` to `<23`

#### Handlebars → kbn-handlebars (CSP Security Fix)

Replaced the `handlebars` package with `kbn-handlebars` ([#11084](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11084)) to eliminate CSP `unsafe-eval` violations. The standard `handlebars.compile()` uses `new Function()` internally, which requires `unsafe-eval` in CSP. The replacement uses `compileAST()` which interprets the template AST directly without generating JavaScript code. A follow-up PR ([#11105](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11105)) temporarily added back the original handlebars to fix backward compatibility tests.

#### Security-Driven Library Updates

| Package | From | To | PR | Motivation |
|---------|------|----|-----|------------|
| lodash | 4.17.21 | 4.17.23 | [#11254](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11254), [#840](https://github.com/opensearch-project/dashboards-assistant/pull/840) | CVE fix |
| lodash-es | 4.17.21 | 4.17.23 | [#11254](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11254), [#838](https://github.com/opensearch-project/dashboards-assistant/pull/838) | CVE fix |
| axios | — | 1.13.3 | [#11233](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11233) | Removed monkey-patch workaround |
| less | — | 4.1.3 | [#11250](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11250) | Use `disablePluginRule` in Markdown panel |
| @modelcontextprotocol/sdk | — | 1.24.0 → 1.25.2 | [#11086](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11086), [#11151](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11151) | Feature update |
| qs | — | 6.14.1 | [#11151](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11151) | Security update |
| caniuse-lite | — | latest | [#11195](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11195) | Browser compatibility data |

#### UI Framework Update

OUI (OpenSearch UI) was upgraded from 1.21.0 to 1.22.1 ([#11042](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11042)), incorporating the latest UI component improvements across the entire application stack.

#### Version Increment

The dashboards-assistant plugin version was incremented to 3.5.0.0 ([#783](https://github.com/opensearch-project/dashboards-assistant/pull/783)).

## Limitations

- The `kbn-handlebars` `compileAST()` method uses AST interpretation instead of compiled JavaScript, which may be slower for dashboards with many TSVB visualizations or large datasets.
- The Node.js 22 upgrade required suppressing certain deprecation warnings that may need to be addressed in future versions.

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#11076](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11076) | Update Node.js to 22.21.1 | OpenSearch-Dashboards |
| [#11218](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11218) | Bump Node.js to v22.22.0 | OpenSearch-Dashboards |
| [#11084](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11084) | Replace handlebars with kbn-handlebars | OpenSearch-Dashboards |
| [#11105](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11105) | Add back handlebars to fix bwc tests | OpenSearch-Dashboards |
| [#11254](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11254) | Update lodash and lodash-es to 4.17.23 | OpenSearch-Dashboards |
| [#11233](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11233) | Bump axios to 1.13.3 | OpenSearch-Dashboards |
| [#11250](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11250) | Bump less to 4.1.3 | OpenSearch-Dashboards |
| [#11042](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11042) | Upgrade OUI to 1.22 | OpenSearch-Dashboards |
| [#11151](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11151) | Bump @modelcontextprotocol/sdk to 1.25.2 and qs to 6.14.1 | OpenSearch-Dashboards |
| [#11086](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11086) | Update @modelcontextprotocol/sdk to v1.24.0 | OpenSearch-Dashboards |
| [#11195](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11195) | Update caniuse-lite | OpenSearch-Dashboards |
| [#840](https://github.com/opensearch-project/dashboards-assistant/pull/840) | Bump lodash to 4.17.23 | dashboards-assistant |
| [#838](https://github.com/opensearch-project/dashboards-assistant/pull/838) | Bump lodash-es to 4.17.23 | dashboards-assistant |
| [#783](https://github.com/opensearch-project/dashboards-assistant/pull/783) | Increment version to 3.5.0.0 | dashboards-assistant |
