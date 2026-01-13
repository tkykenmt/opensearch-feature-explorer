---
tags:
  - ml-commons
---
# ML Commons Multi-tenancy

## Summary

OpenSearch v2.19.0 introduces multi-tenancy support for ML Commons, enabling multiple tenants to share a single OpenSearch instance while maintaining data isolation. This feature adds tenant ID tracking to connectors, models, model groups, agents, and tasks, making ML Commons suitable for cloud service environments.

## Details

### What's New in v2.19.0

Multi-tenancy support was added across all major ML Commons components through a series of PRs:

1. **Primary Infrastructure Setup** ([#3307](https://github.com/opensearch-project/ml-commons/pull/3307))
   - Added `tenant_id` field to index mappings for agents, config, connectors, models, model groups, and tasks
   - Introduced `TenantAwareHelper` utility class for tenant validation
   - Added `x-tenant-id` header support for API requests
   - Integrated `opensearch-remote-metadata-sdk` for SDK client support

2. **Connector Multi-tenancy** ([#3382](https://github.com/opensearch-project/ml-commons/pull/3382))
   - Applied multi-tenancy to connector Create, Get, and Delete operations
   - Tenant isolation ensures one tenant cannot access another tenant's connectors

3. **Model and Model Group Multi-tenancy** ([#3399](https://github.com/opensearch-project/ml-commons/pull/3399))
   - Added tenant ID support to model registration, retrieval, and updates
   - Model groups now include tenant context for access control

4. **Task and Inference APIs** ([#3416](https://github.com/opensearch-project/ml-commons/pull/3416))
   - Multi-tenancy applied to task APIs, deploy, and predict operations
   - Tasks are now tenant-scoped

5. **Undeploy API** ([#3425](https://github.com/opensearch-project/ml-commons/pull/3425))
   - Added tenant ID to undeploy requests

6. **Agent Multi-tenancy** ([#3432](https://github.com/opensearch-project/ml-commons/pull/3432))
   - Agents now support tenant isolation
   - Agent execution respects tenant boundaries

7. **Search Operations** ([#3433](https://github.com/opensearch-project/ml-commons/pull/3433))
   - Multi-tenancy applied to search APIs for models, model groups, agents, and connectors
   - Tenant filtering ensures search results are scoped to the requesting tenant

8. **Config API and Master Key** ([#3439](https://github.com/opensearch-project/ml-commons/pull/3439))
   - Multi-tenancy support for configuration API
   - Master key handling updated for tenant context

9. **Skills Plugin Support** ([skills#489](https://github.com/opensearch-project/skills/pull/489))
   - Added multi-tenancy support for tools in the skills plugin

### Technical Changes

#### Index Schema Updates

All ML Commons indices received schema updates to include `tenant_id`:

```json
{
  "_meta": { "schema_version": N },
  "properties": {
    "tenant_id": { "type": "keyword" }
  }
}
```

#### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.ml_commons.multi_tenancy_enabled` | Enable multi-tenancy | `false` |
| `plugins.ml_commons.remote_metadata_type` | Remote metadata storage type | - |
| `plugins.ml_commons.remote_metadata_endpoint` | Remote metadata endpoint | - |
| `plugins.ml_commons.remote_metadata_region` | AWS region for remote metadata | - |
| `plugins.ml_commons.remote_metadata_service_name` | Remote metadata service name | - |

#### API Changes

When multi-tenancy is enabled, API requests must include the `x-tenant-id` header:

```bash
curl -X GET "localhost:9200/_plugins/_ml/connectors/<connector_id>" \
  -H "x-tenant-id: my-tenant"
```

## Limitations

- Multi-tenancy is a static setting requiring cluster restart to enable
- Existing clusters must migrate ML resources when enabling multi-tenancy
- Only externally hosted models support multi-tenancy (local models are not tenant-aware)

## References

### Documentation
- [Plugin as a Service](https://docs.opensearch.org/2.19/developer-documentation/plugin-as-a-service/index/): Multi-tenancy configuration guide

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [ml-commons#3307](https://github.com/opensearch-project/ml-commons/pull/3307) | Primary setup for Multi-tenancy | - |
| [ml-commons#3382](https://github.com/opensearch-project/ml-commons/pull/3382) | Apply multi-tenancy in Connector (Create + Get + Delete) | - |
| [ml-commons#3399](https://github.com/opensearch-project/ml-commons/pull/3399) | Multi-tenancy for model, model group, connector update | - |
| [ml-commons#3416](https://github.com/opensearch-project/ml-commons/pull/3416) | Multi-tenancy for task APIs, deploy, predict | - |
| [ml-commons#3425](https://github.com/opensearch-project/ml-commons/pull/3425) | Adding tenantID to request + undeploy | - |
| [ml-commons#3432](https://github.com/opensearch-project/ml-commons/pull/3432) | Multi-tenancy for agents | - |
| [ml-commons#3433](https://github.com/opensearch-project/ml-commons/pull/3433) | Multi-tenancy in search (model, model group, agent, connector) | - |
| [ml-commons#3439](https://github.com/opensearch-project/ml-commons/pull/3439) | Multi-tenancy for config API and master key | - |
| [skills#489](https://github.com/opensearch-project/skills/pull/489) | Add multi-tenancy support for tools | [ml-commons#3416](https://github.com/opensearch-project/ml-commons/pull/3416) |
