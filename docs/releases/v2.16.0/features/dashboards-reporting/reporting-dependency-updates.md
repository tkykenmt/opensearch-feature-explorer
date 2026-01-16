---
tags:
  - dashboards-reporting
---
# Reporting Dependency Updates

## Summary

OpenSearch Dashboards Reporting v2.16.0 includes critical security updates for three npm dependencies to address known CVEs. These updates fix vulnerabilities in jsdom, ws (WebSocket), and braces packages.

## Details

### What's New in v2.16.0

Three dependency updates were merged to address security vulnerabilities:

| Dependency | Update | CVE Fixed | Severity |
|------------|--------|-----------|----------|
| jsdom | 17.0.0 → 18.0.0 | CVE-2024-37890 | High (7.5) |
| ws | Resolution to v7.5.10 | CVE-2024-37890 | High |
| braces | Resolution to v3.0.3 | CVE-2024-4068 | - |

### Technical Changes

#### jsdom Update (PR #381)

The jsdom library was updated from v17.0.0 to v18.0.0. Key changes include:

- Fixed SSL certificate checking for WebSocket connections (previously invalid SSL certificates were always accepted)
- Changed the global context for Promise and TypeError instances to the jsdom global instead of Node.js global
- Fixed element tagName cache reset when moving elements between HTML and XML documents
- Fixed form submission to not happen when the form is invalid

#### ws WebSocket Update (PR #385)

Added resolution for ws package to v7.5.10 to address CVE-2024-37890, a high-severity vulnerability in the WebSocket library.

#### braces Update (PR #388)

Added braces v3.0.3 to package resolutions to address CVE-2024-4068, a vulnerability in the braces package used for brace expansion.

## Limitations

- The jsdom update changes the global context for Promise instances, which could affect code using `instanceof` checks

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#381](https://github.com/opensearch-project/dashboards-reporting/pull/381) | Update dependency jsdom to v18 | [#377](https://github.com/opensearch-project/dashboards-reporting/issues/377) |
| [#385](https://github.com/opensearch-project/dashboards-reporting/pull/385) | Update dependency ws to v7.5.10 | [#377](https://github.com/opensearch-project/dashboards-reporting/issues/377) |
| [#388](https://github.com/opensearch-project/dashboards-reporting/pull/388) | Add braces v3.0.3 to resolution | CVE-2024-4068 |

### CVE References
- [CVE-2024-37890](https://nvd.nist.gov/vuln/detail/CVE-2024-37890): WebSocket vulnerability
- [CVE-2024-4068](https://nvd.nist.gov/vuln/detail/CVE-2024-4068): braces vulnerability
