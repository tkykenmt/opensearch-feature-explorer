# Dashboards Dependencies

## Summary

This release updates the DOMPurify dependency from version 3.1.6 to 3.2.4 in OpenSearch Dashboards to address CVE-2025-26791, a mutation cross-site scripting (mXSS) vulnerability caused by an incorrect template literal regular expression.

## Details

### What's New in v3.0.0

The DOMPurify library has been updated to fix a security vulnerability that could allow attackers to bypass XSS sanitization through specially crafted input.

### Technical Changes

#### Security Fix

| CVE | Severity | Description |
|-----|----------|-------------|
| CVE-2025-26791 | Medium | Mutation XSS vulnerability due to incorrect template literal regex |

#### Dependency Update

| Package | Previous Version | New Version |
|---------|------------------|-------------|
| dompurify | 3.1.6 | 3.2.4 |

### Background

DOMPurify is a DOM-only, super-fast, uber-tolerant XSS sanitizer for HTML, MathML, and SVG. OpenSearch Dashboards uses DOMPurify to sanitize user-provided HTML content before rendering, protecting against cross-site scripting attacks.

The vulnerability (CVE-2025-26791) existed in versions before 3.2.4 where an incorrect template literal regular expression could lead to mutation XSS (mXSS) attacks. In mXSS attacks, malicious content that appears safe during initial sanitization can mutate into executable code when the browser parses the DOM.

### Migration Notes

No migration steps required. The dependency update is transparent to users and administrators.

## Limitations

None specific to this update.

## Related PRs

| PR | Description |
|----|-------------|
| [#9447](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9447) | Bump dompurify from 3.1.6 to 3.2.4 |

## References

- [CVE-2025-26791 - NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-26791): Official CVE entry
- [DOMPurify GitHub](https://github.com/cure53/DOMPurify): DOMPurify library repository

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-dashboards/dompurify-sanitization.md)
