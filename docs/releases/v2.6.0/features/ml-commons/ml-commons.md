---
tags:
  - ml-commons
---
# ML Commons

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to ML Commons, along with 7 bug fixes.

## Details

### New Features

- **Enable prebuilt model**: As we have published prebuilt models to OpeSearch repo, we can enable uploading prebuilt model function now. Example: ``` POST /_plugins/_ml/models/_upload { "name": "huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2", "version": "1.0.1", "model_format": "TORCH_SCRIPT" } ```

### Bug Fixes

- Update gpu doc with docker test
- Add text embedding API example doc
- Fix profile API in example doc
- Change model url to public repo in text embedding model example doc
- JSON listing of all the pretrianed models
- Increment version to 2.6.0-SNAPSHOT
- Add DL model class

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#729](https://github.com/opensearch-project/ml-commons/pull/729) | Enable prebuilt model | ml-commons |
| [#702](https://github.com/opensearch-project/ml-commons/pull/702) | Update gpu doc with docker test | ml-commons |
| [#710](https://github.com/opensearch-project/ml-commons/pull/710) | Add text embedding API example doc | ml-commons |
| [#712](https://github.com/opensearch-project/ml-commons/pull/712) | Fix profile API in example doc | ml-commons |
| [#713](https://github.com/opensearch-project/ml-commons/pull/713) | Change model url to public repo in text embedding model example doc | ml-commons |
| [#730](https://github.com/opensearch-project/ml-commons/pull/730) | JSON listing of all the pretrianed models | ml-commons |
| [#671](https://github.com/opensearch-project/ml-commons/pull/671) | Increment version to 2.6.0-SNAPSHOT | ml-commons |
| [#722](https://github.com/opensearch-project/ml-commons/pull/722) | Add DL model class | ml-commons |
