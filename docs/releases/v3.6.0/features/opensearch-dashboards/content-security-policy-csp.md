---
tags:
  - opensearch-dashboards
---
# Content Security Policy (CSP)

## Summary

OpenSearch Dashboards v3.6.0 introduces strict CSP enforcement mode for the main `Content-Security-Policy` header (previously only available in report-only mode), fixes a CSP violation in the Console plugin's Ace editor Web Worker, renames the configuration key from `csp.strict` to `csp.enable`, and adds backward compatibility for the deprecated `csp.strict` key.

## Details

### What's New in v3.6.0

#### Strict CSP Enforcement Mode (PR #11536)

The CSP subsystem now supports a strict enforcement mode that applies a comprehensive set of CSP directives to the main `Content-Security-Policy` header. Previously, strict rules were only available in CSP-Report-Only mode.

When `csp.enable: true` (or the deprecated `csp.strict: true`) is set in `opensearch_dashboards.yml`, the server applies a full set of strict directives:

| Directive | Strict Value |
|-----------|-------------|
| `default-src` | `'self'` |
| `script-src` | `'self'` |
| `script-src-attr` | `'none'` |
| `style-src` | `'self'` |
| `style-src-elem` | `'self'` |
| `style-src-attr` | `'self' 'unsafe-inline'` |
| `child-src` | `'none'` |
| `worker-src` | `'self'` |
| `frame-src` | `'none'` |
| `object-src` | `'none'` |
| `manifest-src` | `'self'` |
| `media-src` | `'none'` |
| `font-src` | `'self'` |
| `connect-src` | `'self'` + trusted OpenSearch endpoints |
| `img-src` | `'self' data:` + trusted OpenSearch endpoints |
| `form-action` | `'self'` |
| `frame-ancestors` | `'self'` |

New configuration options added:

| Setting | Description | Default |
|---------|-------------|---------|
| `csp.nonceDirectives` | Directives that receive nonce values | `['style-src-elem']` |
| `csp.allowedFrameAncestorSources` | Additional sources for `frame-ancestors` | (none) |
| `csp.allowedConnectSources` | Additional sources for `connect-src` | (none) |
| `csp.allowedImgSources` | Additional sources for `img-src` | (none) |
| `csp.loosenCspDirectives` | Directives to relax back to loose defaults | (none) |

When strict mode is enabled, nonces are automatically injected into the CSP header for HTML resource responses via `buildHeaderWithNonce()`, enabling nonce-based protection for directives like `style-src-elem`.

The `loosenCspDirectives` option allows selectively relaxing specific directives back to the loose defaults while keeping the rest strict. For example, setting `csp.loosenCspDirectives: ['script-src']` would change `script-src` from `'self'` to `'unsafe-eval' 'self'`.

#### Console Worker CSP Fix (PR #11353)

The Console plugin's Ace editor previously created Web Workers using blob URLs (`new Worker(blobUrl)`), which violated the `worker-src 'self'` CSP policy. The fix changes the worker loading mechanism from `raw-loader` (which inlines JavaScript as a string and creates a blob URL) to `file-loader` (which emits the worker file as a static asset and returns its URL). The Console plugin also overrides `URL.createObjectURL` to intercept blob-based worker creation and redirect to the file-based URL.

#### Config Key Rename: `csp.strict` → `csp.enable` (PR #11572)

The `csp.strict` configuration key was renamed to `csp.enable` to better reflect its purpose of enabling CSP hardening mode. The `CspConfig` class now exposes both `enable` and `strict` properties, with `strict` marked as `@deprecated`.

#### Backward Compatibility for `csp.strict` (PR #11594)

To prevent fatal startup crashes for deployments that still have `csp.strict` set in their `opensearch_dashboards.yml`, the deprecated `strict` key was added back to the config schema. The runtime resolves `enable || strict`, so behavior is unchanged regardless of which key is used. The `strict` key will be removed in a future release.

### Technical Changes

Key files modified:
- `src/core/server/constants.ts` — New `CSP_DIRECTIVES` map, `STRICT_CSP_RULES_DEFAULT_VALUE`, `LOOSE_CSP_RULES_DEFAULT_VALUE`, and `AllowedSourcesConfig` interface
- `src/core/server/csp/csp_config.ts` — `CspConfig` class with `buildHeaderWithNonce()`, `applyLoosenCspRules()`, `applyAllowedSources()`, and `applyNonces()` methods; new `enable` property
- `src/core/server/csp/config.ts` — Schema updated with `enable`, `nonceDirectives`, `allowedFrameAncestorSources`, `allowedConnectSources`, `allowedImgSources`, `loosenCspDirectives`; deprecated `strict` key retained
- `src/core/server/http_resources/http_resources_service.ts` — Uses `buildHeaderWithNonce()` when strict mode is enabled
- `src/legacy/ui/ui_render/ui_render_mixin.js` — Uses `buildHeaderWithNonce()` when strict mode is enabled
- `src/plugins/console/public/plugin.ts` — Overrides `URL.createObjectURL` to redirect blob workers to file URL
- `src/plugins/console/public/.../mode/worker/index.js` — Switched from `raw-loader` to `file-loader`

## Limitations

- `style-src-attr` must allow `'unsafe-inline'` due to Monaco editor's reliance on inline style attributes
- The `csp.strict` config key is deprecated and will be removed in a future release; migrate to `csp.enable`
- `loosenCspDirectives` only takes effect when strict/enable mode is active

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11353](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11353) | Fix CSP violation for Console worker by loading from URL instead of blob | — |
| [#11536](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11536) | Update CSP configuration to support strict enforcement mode | — |
| [#11572](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11572) | Rename CSP strict config flag to `csp.enable` | — |
| [#11594](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11594) | Add deprecated `csp.strict` config key back for backward compatibility | — |
