# OpenSearch v3.3.2 Release Summary

OpenSearch v3.3.2 is a patch release focused on bug fixes, security patches, and incremental enhancements across multiple plugins.

## Highlights

### New Feature
- **Nova MME Support**: Amazon Nova multimodal embedding model support added to ML Commons

### Enhancements
- **Agentic Search**: Conversation search support, robust JSON extraction from LLM responses, model-type-aware summary trace extraction
- **ML Commons Agent**: MCP connector support in agent update API, refresh policy and checkpoint ID for model management

### Security Fixes
- CVE-2025-58057 patched in ML Commons
- Regex bypass vulnerability fixed in ML Commons and Skills plugins
- WildcardMatcher empty string handling fixed in Security plugin
- Security provider registered earlier in bootstrap process

### Bug Fixes
- **k-NN**: Fixed NPE when memory optimized search applied to pre-2.17 indices
- **ML Commons**: Execute tool API immutable map fix, streaming filtered output, return_history fix, JSON chunk combining
- **Core Engine**: Patch version build fix, terms aggregation IndexOutOfBoundsException fix
- **S3 Repository**: LEGACY_MD5_CHECKSUM_CALCULATION setting registered
- **Remote Store**: Netty codec version aligned with core engine

### Dependencies
- Logback: 1.5.18 → 1.5.20
- BouncyCastle bc-fips: 2.1.1 → 2.1.2

## Statistics

| Category | Count |
|----------|-------|
| Total Items | 24 |
| Features | 1 |
| Enhancements | 5 |
| Bug Fixes | 18 |
| Repositories | 7 |
