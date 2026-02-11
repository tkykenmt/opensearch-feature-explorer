---
tags:
  - opensearch-dashboards
---
# Dashboards Build (Rspack Migration)

## Summary

OpenSearch Dashboards v3.5.0 migrates the entire build toolchain from Webpack 4 to [Rspack](https://rspack.dev/) (v1.6.4), a high-performance Rust-based bundler with Webpack-compatible APIs. This also replaces Babel with SWC for JavaScript/TypeScript transpilation and upgrades Storybook to Webpack 5. The migration improves build speed while maintaining full compatibility with the existing plugin ecosystem.

## Details

### What's New in v3.5.0

The core build system (`osd-optimizer`) and all supporting packages have been migrated from Webpack 4 (a custom fork `@amoo-miki/webpack@4.46.0-xxhash.1`) to `@rspack/core@1.6.4`.

### Technical Changes

| Area | Before (Webpack 4) | After (Rspack 1.6.4) |
|------|--------------------|-----------------------|
| Bundler | `webpack` (custom fork) | `@rspack/core` |
| Transpiler | Babel (`babel-loader`) | SWC (built-in to Rspack via `getSwcLoaderConfig`) |
| Sass | `@amoo-miki/sass-loader` + `sass-embedded@1.66.1` | `sass-loader@16.0.5` + `sass-embedded@1.93.3` |
| PostCSS | `postcss-loader@4.x` | `postcss-loader@8.x` |
| Compression | `@amoo-miki/compression-webpack-plugin@4.0.1-rc.1` | `compression-webpack-plugin@11.x` |
| Merge | `webpack-merge@4.x` | `webpack-merge@5.x` |
| Minifier | `terser-webpack-plugin` | `rspack.SwcJsMinimizerRspackPlugin` + `LightningCssMinimizerRspackPlugin` |
| Bundle refs | `BundleRefsPlugin` + `BundleRefModule` (custom webpack Module) | `VirtualModulesPlugin` + `BundleDepsCheckPlugin` |
| Hash function | `Xxh64` | `xxhash64` |
| Storybook | Webpack 4 | Webpack 5 |
| Asset handling | `url-loader`, `file-loader`, `raw-loader` | Rspack native `asset`, `asset/resource`, `asset/source` types |

#### Key Architectural Changes

1. `BundleRefsPlugin` and `BundleRefModule` (which intercepted webpack's module factory to replace cross-bundle imports with custom Module instances) are removed. Replaced by `rspack.experiments.VirtualModulesPlugin` which creates virtual files that resolve to `__osdBundles__.get(exportId)`.

2. `BundleDepsCheckPlugin` is a new plugin that validates bundle dependency declarations at build time by inspecting `NormalModule` instances in `finishModules` hook.

3. Entry point creator changed from `__osdBundles__.define(id, __webpack_require__, require.resolve(path))` to `__osdBundles__.define(id, () => { return require(path) })` — a lazy factory pattern.

4. Sass compilation uses a pool of 3 async `sass-embedded` compilers for parallel SCSS processing, with proper disposal on build completion.

5. CI cypress workflow switched from `--dev` to `--dist` (production) builds to address disk space constraints on GitHub Actions runners.

#### Modified Packages

| Package | Changes |
|---------|---------|
| `osd-optimizer` | Core migration: Rspack config, SWC loader, VirtualModulesPlugin, BundleDepsCheckPlugin |
| `osd-monaco` | Build script uses `rspack` CLI, SWC replaces Babel, native asset types |
| `osd-pm` | Build script uses `rspack` CLI, SWC replaces Babel |
| `osd-ui-shared-deps` | Webpack config migrated to Rspack |
| `osd-ui-framework` | Build config migrated to Rspack |
| `osd-std` | Updated `json11` dependency to `^2.0.2` |

## Limitations

- Rspack produces slightly larger assets in development mode compared to Webpack 4
- Chunk file naming changed (e.g., `chunk.1.js` → `chunk.0.js`), which may affect plugins that reference chunk files by name
- Compression for async chunks in tests may behave differently (`.gz` files not created for chunks in test environment, but work correctly in actual builds)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11102](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11102) | Migrate OSD build from Webpack4 to Rspack | |
| [#11107](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11107) | Webpack 5 migration of Storybook (combined into #11102) | |
| [#11125](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11125) | RFC: Rspack migration | |
