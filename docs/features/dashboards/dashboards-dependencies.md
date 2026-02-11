---
tags:
  - dashboards
---
# Dashboards Dependencies

## Summary

Dependency management for OpenSearch Dashboards and its plugins, covering runtime upgrades (Node.js), security patches (CVE fixes for lodash, axios), CSP compliance improvements (handlebars replacement), and UI framework updates (OUI).

## Details

### Key Dependencies

| Dependency | Purpose | Current Version |
|-----------|---------|-----------------|
| Node.js | Runtime | 22.22.0 |
| OUI (OpenSearch UI) | UI component library | 1.22.1 |
| lodash / lodash-es | Utility library | 4.17.23 |
| axios | HTTP client | 1.13.3 |
| kbn-handlebars | Template engine (CSP-safe) | 1.0.0 |
| less | CSS preprocessor | 4.1.3 |
| @modelcontextprotocol/sdk | MCP integration | 1.25.2 |

### CSP Compliance

The `handlebars` package was replaced with `kbn-handlebars` to eliminate CSP `unsafe-eval` violations. The standard `handlebars.compile()` generates JavaScript via `new Function()`, while `kbn-handlebars` provides `compileAST()` that interprets the template AST directly. This affects TSVB visualizations (`replace_vars.js`, `tick_formatter.js`) on the client side.

### Node.js Upgrade Strategy

OpenSearch Dashboards follows the Node.js LTS release cycle. The v3.5.0 release upgraded from Node.js 20 to Node.js 22, requiring compatibility adjustments for stream APIs, deprecation warnings, and test infrastructure.

## Limitations

- `kbn-handlebars` AST interpretation is slower than compiled JavaScript execution, potentially impacting dashboards with many TSVB visualizations.
- Node.js 22 deprecation warnings for `MODULE_TYPELESS_PACKAGE_JSON` and `fs.Stats constructor` are suppressed but may need future resolution.

## Change History

- **v3.5.0**: Node.js upgraded to 22.22.0; handlebars replaced with kbn-handlebars for CSP compliance; lodash/lodash-es updated to 4.17.23 (CVE fix); axios bumped to 1.13.3; OUI upgraded to 1.22.1; less bumped to 4.1.3; @modelcontextprotocol/sdk updated to 1.25.2

## References

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v3.5.0 | [#11076](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11076) | Update Node.js to 22.21.1 |
| v3.5.0 | [#11218](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11218) | Bump Node.js to v22.22.0 |
| v3.5.0 | [#11084](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11084) | Replace handlebars with kbn-handlebars |
| v3.5.0 | [#11105](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11105) | Add back handlebars to fix bwc tests |
| v3.5.0 | [#11254](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11254) | Update lodash and lodash-es to 4.17.23 |
| v3.5.0 | [#11233](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11233) | Bump axios to 1.13.3 |
| v3.5.0 | [#11250](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11250) | Bump less to 4.1.3 |
| v3.5.0 | [#11042](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11042) | Upgrade OUI to 1.22 |
| v3.5.0 | [#11151](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11151) | Bump @modelcontextprotocol/sdk to 1.25.2 and qs to 6.14.1 |
| v3.5.0 | [#11086](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11086) | Update @modelcontextprotocol/sdk to v1.24.0 |
| v3.5.0 | [#11195](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11195) | Update caniuse-lite |
| v3.5.0 | [#840](https://github.com/opensearch-project/dashboards-assistant/pull/840) | Bump lodash to 4.17.23 |
| v3.5.0 | [#838](https://github.com/opensearch-project/dashboards-assistant/pull/838) | Bump lodash-es to 4.17.23 |
| v3.5.0 | [#783](https://github.com/opensearch-project/dashboards-assistant/pull/783) | Increment version to 3.5.0.0 |
