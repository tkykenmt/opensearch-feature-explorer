---
tags:
  - opensearch
---
# Repository S3 Plugin

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to Repository S3 Plugin.

## Details

### New Features

- **Fix Opensearch repository-s3 plugin cannot read ServiceAccount token (**: Allow to specify the identity web token file relatively to the `config` folder location (configured by `OPENSEARCH_PATH_CONFIG` so it would be possible to use soft links to access it): ``` ln -s $AWS_WEB_IDENTITY_TOKEN_FILE "${OPENSEARCH_PATH_CONFIG}/aws-web-identity-token-file" ``` And refer to it 

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#6390](https://github.com/opensearch-project/OpenSearch/pull/6390) | Fix Opensearch repository-s3 plugin cannot read ServiceAccount token ( | OpenSearch |
