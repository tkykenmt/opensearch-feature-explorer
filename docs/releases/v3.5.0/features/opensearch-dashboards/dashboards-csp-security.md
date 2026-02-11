---
tags:
  - opensearch-dashboards
---
# Dashboards CSP Security

## Summary

OpenSearch Dashboards v3.5.0 introduces significant CSP (Content Security Policy) security improvements including nonce-based style protection in CSP Report-Only mode, dynamic CSP directive modification via the Application Config API, stricter input sanitization in visualizations, and removal of the legacy intentional CSP violation detection mechanism.

## Details

### What's New in v3.5.0

#### Nonce-Based Style Protection (PR #11074)

Per-request cryptographic nonces are now generated and injected into the `style-src-elem` directive of the CSP-Report-Only header. This replaces `'unsafe-inline'` for `<style>` elements with a more secure nonce-based approach. The implementation covers four categories of inline styles:

- **Server-rendered styles**: Nonce added during server-side rendering via a `<meta name="csp-nonce">` tag
- **Client-side dynamic styles**: Services like `styles_service.ts` and `inject_header_style.ts` retrieve the nonce via a shared `getNonce()` utility
- **Webpack-bundled styles**: Handled via the `__webpack_nonce__` global variable set during bootstrap
- **Third-party libraries**: DOM interception patches `document.createElement` to automatically add nonces to `<style>` elements created by libraries like nano-css and ace/brace editor

The CSP directive strategy splits into granular directives:
- `style-src-elem`: Receives the nonce (primary protection)
- `style-src-attr`: Allows `'unsafe-inline'` (required by Monaco editor)
- `style-src`: Set to `'self'` as fallback for legacy browsers

#### Dynamic CSP Modification (PR #11168)

CSP headers can now be modified dynamically through the Application Config API without restarting the Node server. This enables administrators to add, remove, or set CSP directives through configuration, useful for testing CSP policies in non-production environments.

#### Stricter Visualization Sanitization (PRs #11251, #11252)

- Axis labels and names in visualizations now undergo stricter sanitization to prevent XSS via crafted chart labels
- URL and `imageLabel` fields in visualizations are now sanitized using DOMPurify, replacing less robust sanitization methods

#### Removal of Legacy CSP Violation Detection (PR #11060)

The intentional CSP violation detection mechanism has been removed. This legacy approach injected an inline `<script>` tag that set `window.__osdCspNotEnforced__ = true` to detect browser CSP support. Since all modern browsers support CSP, this security anti-pattern was no longer necessary. Removed components include:
- Inline CSP violation script from `template.tsx`
- `browserSupportsCsp` parameter from core system initialization
- Legacy browser warning from `ChromeService`

### Technical Changes

| Area | Change | Impact |
|------|--------|--------|
| CSP-Report-Only | Nonce generation via `crypto.randomBytes()` (128-bit) | Prevents CSS injection attacks |
| `CspReportOnlyConfig` | New `buildHeaderWithNonce(nonce)` method | Dynamic nonce insertion per request |
| `csp_handler` plugin | Dynamic CSP directive modification support | Runtime CSP policy changes |
| Visualization axis labels | Stricter sanitization | Prevents XSS via chart labels |
| Visualization URLs/images | DOMPurify-based sanitization | Prevents XSS via URL/image fields |
| Core bootstrap | Removed `__osdCspNotEnforced__` flag | Cleaner security posture |

## Limitations

- `style-src-attr` must still allow `'unsafe-inline'` due to Monaco editor's reliance on inline style attributes (see [microsoft/monaco-editor#271](https://github.com/microsoft/monaco-editor/issues/271))
- Nonces are only applied in CSP-Report-Only mode; enforced CSP still uses static rules
- Dynamic CSP modification is intended for testing; production environments should use static YAML configuration

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11074](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11074) | Style-src-elem nonces for CSP report-only | |
| [#11168](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11168) | Add CSP modifications using dynamic config | |
| [#11251](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11251) | Add stricter sanitization on axis label and name in visualizations | |
| [#11252](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11252) | Use dompurify to sanitize URL and imageLabel | |
| [#11060](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11060) | Remove Intentional CSP Violation Detection Mechanism | |
