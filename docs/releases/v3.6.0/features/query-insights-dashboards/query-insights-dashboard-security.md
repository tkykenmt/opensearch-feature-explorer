---
tags:
  - query-insights-dashboards
---
# Query Insights Dashboard Security

## Summary

Security dependency updates for the Query Insights Dashboards plugin in v3.6.0, addressing five CVEs across four JavaScript packages: minimatch, lodash, qs, and serialize-javascript. All fixes were applied via yarn resolutions in `package.json` and backported to the 3.6 release branch.

## Details

### What's New in v3.6.0

Five CVEs were resolved through dependency version bumps:

| CVE | Severity | Package | Before | After | Description |
|-----|----------|---------|--------|-------|-------------|
| CVE-2026-26996 | HIGH | minimatch | 3.1.2 | 3.1.5 | ReDoS via exponential backtracking with repeated wildcards |
| CVE-2025-13465 | MEDIUM | lodash | 4.17.21 | 4.17.23 | Prototype pollution in `_.unset` and `_.omit` (4.0.0–4.17.22) |
| CVE-2025-15284 | MEDIUM | qs | 6.14.0 | 6.15.0 | arrayLimit bypass in bracket notation allowing DoS |
| GHSA-5c6j-r48x-rmvq | - | serialize-javascript | 6.0.2 | 7.0.3 | Security vulnerability in serialization |
| CVE-2026-4800 | - | lodash | 4.17.23 | 4.18.1 | Additional lodash vulnerability |

### Technical Changes

All changes were made to `package.json` (yarn resolutions) and `yarn.lock`:

- PR #489 (backport of #488): Added yarn resolutions for `minimatch@^3.1.3`, `lodash@^4.17.23`, and `qs@^6.14.1`
- PR #491 (backport of #490): Bumped `serialize-javascript` from 6.0.2 to 7.0.3 in resolutions, removing the `randombytes` dependency
- PR #496 (backport of #495): Updated `lodash` from `^4.17.23` to `^4.18.0`, resolving to 4.18.1 to address CVE-2026-4800

The serialize-javascript 7.0.3 upgrade is notable as it removes the `randombytes` dependency entirely, simplifying the dependency tree.

## Limitations

- These are dependency-only changes with no functional impact on the plugin
- The fixes address transitive dependency vulnerabilities in the dashboards build toolchain

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#489](https://github.com/opensearch-project/query-insights-dashboards/pull/489) | Backport: Fix CVE-2026-26996, CVE-2025-13465, CVE-2025-15284 via yarn resolutions | Backport of [#488](https://github.com/opensearch-project/query-insights-dashboards/pull/488) |
| [#491](https://github.com/opensearch-project/query-insights-dashboards/pull/491) | Backport: Bump serialize-javascript to 7.0.3 for GHSA-5c6j-r48x-rmvq | Backport of [#490](https://github.com/opensearch-project/query-insights-dashboards/pull/490) |
| [#496](https://github.com/opensearch-project/query-insights-dashboards/pull/496) | Backport: Update lodash to 4.18.1 for CVE-2026-4800 | Backport of [#495](https://github.com/opensearch-project/query-insights-dashboards/pull/495), [opensearch-build#5966](https://github.com/opensearch-project/opensearch-build/issues/5966) |
