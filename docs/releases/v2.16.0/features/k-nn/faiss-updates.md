---
tags:
  - k-nn
---
# k-NN Faiss Updates

## Summary

This release bumps the Faiss submodule to commit 33c0ba5 and updates the CMake minimum required version to 3.24.0. This update is a prerequisite for enabling Faiss byte vector support, which provides significant memory savings for large-scale vector search applications.

## Details

### What's New in v2.16.0

The Faiss library dependency was updated to include support for the `SQ8_direct_signed` scalar quantizer, which enables direct encoding of signed byte vectors without training. This update:

1. **Faiss Submodule Bump**: Updated to commit [33c0ba5](https://github.com/facebookresearch/faiss/commit/33c0ba5d002a7cd9761513f06ecc9822079d4a2f)
2. **CMake Version Update**: Bumped minimum required CMake version to 3.24.0 to match Faiss requirements
3. **Patch Updates**: Updated patches to be compatible with the new Faiss version

### Technical Changes

The Faiss update introduces the `QT_8bit_direct_signed` quantizer type, which:

- Accepts signed byte vectors in the range [-128, 127]
- Does not require training (unlike other quantizers)
- Quantizes float vector values directly into byte-sized vectors
- Reduces memory footprint by a factor of 4 compared to float vectors

This change is foundational for the byte vector support feature that was fully implemented in v2.17.0.

## Limitations

- This is a dependency update only; the byte vector feature requires additional implementation (completed in v2.17.0)
- CMake 3.24.0 or higher is now required for building the k-NN plugin

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1796](https://github.com/opensearch-project/k-NN/pull/1796) | Bump faiss commit to 33c0ba5 | [#1659](https://github.com/opensearch-project/k-NN/issues/1659) |

### Issues
- [#1659](https://github.com/opensearch-project/k-NN/issues/1659): Support for Faiss byte vector

### External References
- [Faiss ScalarQuantizer Documentation](https://faiss.ai/cpp_api/struct/structfaiss_1_1ScalarQuantizer.html)
- [Faiss Issue #3488](https://github.com/facebookresearch/faiss/issues/3488): QT_8bit_direct_signed support
