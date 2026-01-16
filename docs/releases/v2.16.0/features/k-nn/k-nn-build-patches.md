---
tags:
  - k-nn
---
# k-NN Build & Patches

## Summary

Bug fixes for the k-NN plugin build infrastructure in v2.16.0, addressing custom patch application issues and developer guide improvements for ARM-based development environments.

## Details

### What's New in v2.16.0

#### Custom Patch Application Fix

The build system now applies custom patches only once by comparing the patch-id of the last commit. Previously, when multiple custom patches touched the same file, re-applying patches would fail, causing consistent build failures when building the JNI library more than once.

The fix modifies the CMake configuration to:
1. Check the patch-id of the last commit before applying patches
2. Skip patch application if the patch has already been applied
3. Eliminate the need to manually remove `git rebase-apply` and `external/faiss` folders

This improvement reduces development time by avoiding the workaround of rebuilding from scratch.

#### Developer Guide Update for ARM

Updated the `DEVELOPER_GUIDE.md` with corrected instructions for building on Apple M-series chips. The previous instructions had clang linking issues on ARM architecture. The updated guide uses gcc/g++ instead of clang to build and link the external k-NN libraries.

### Technical Changes

| Change | Description |
|--------|-------------|
| CMake patch logic | Compare patch-id before applying to prevent duplicate application |
| CI configuration | Removed `submodule: true` option (no longer needed after Linux image upgrade) |
| Developer guide | Updated M-series build instructions to use gcc/g++ |

## Limitations

- The patch-id comparison requires git to be available in the build environment
- ARM build instructions are specific to Apple M-series chips (M2, M3)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1833](https://github.com/opensearch-project/k-NN/pull/1833) | Apply custom patch only once by comparing the patch-id of the last commit | - |
| [#1746](https://github.com/opensearch-project/k-NN/pull/1746) | Update dev guide to fix clang linking issue on ARM | - |
