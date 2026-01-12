---
tags:
  - search
  - indexing
  - performance
---

# OpenSearch Core

Core engine features for OpenSearch.

## Search & Query

| Document | Description |
|----------|-------------|
| [Query Optimization](query-optimization.md) | Query performance |
| [Query Performance Optimizations](query-performance-optimizations.md) | Performance tuning |
| [Query Rewriting](query-rewriting.md) | Query transformation |
| [Query Builders](query-builders.md) | Query construction |
| [Query Cache](query-cache.md) | Query caching |
| [Query String & Regex](query-string-regex.md) | String queries |
| [Query String Monitoring](query-string-monitoring.md) | Query monitoring |
| [Combined Fields Query](combined-fields-query.md) | Multi-field search |
| [Parent-Child Query](parent-child-query.md) | Nested queries |
| [Terms Query](terms-query.md) | Terms matching |
| [Terms Lookup Query](terms-lookup-query.md) | Terms lookup |
| [BooleanQuery Rewrite](booleanquery-rewrite-optimizations.md) | Boolean optimization |
| [Automata & Regex Optimization](automata-regex-optimization.md) | Regex performance |
| [Filter Rewrite Optimization](filter-rewrite-optimization.md) | Filter optimization |
| [Rescore Named Queries](rescore-named-queries.md) | Rescoring |
| [Search Scoring](search-scoring.md) | Relevance scoring |
| [Search Settings](search-settings.md) | Search configuration |
| [Search API Enhancements](search-api-enhancements.md) | API improvements |
| [Search API Tracker](search-api-tracker.md) | API tracking |
| [Search Pipeline](search-pipeline.md) | Search pipelines |
| [Search Backpressure](search-backpressure.md) | Load management |
| [Search Request Stats](search-request-stats.md) | Request metrics |
| [Search Shard Routing](search-shard-routing.md) | Shard routing |
| [Search Tie-breaking](search-tie-breaking.md) | Result ordering |
| [Multi-Search API](multi-search-api.md) | Batch search |
| [Scroll API](scroll-api.md) | Pagination |
| [Concurrent Segment Search](concurrent-segment-search.md) | Parallel search |
| [Field Collapsing](field-collapsing.md) | Result grouping |
| [Unified Highlighter](unified-highlighter.md) | Highlighting |

## Aggregations

| Document | Description |
|----------|-------------|
| [Aggregation Optimizations](aggregation-optimizations.md) | Aggregation performance |
| [Aggregation Task Cancellation](aggregation-task-cancellation.md) | Task management |
| [Composite Aggregation](composite-aggregation.md) | Composite aggs |
| [Cardinality Aggregation](cardinality-aggregation.md) | Distinct counts |
| [Nested Aggregations](nested-aggregations.md) | Nested aggs |
| [Percentiles Aggregation](percentiles-aggregation.md) | Percentiles |
| [Scripted Metric Aggregation](scripted-metric-aggregation.md) | Custom metrics |
| [Numeric Terms Aggregation](numeric-terms-aggregation-optimization.md) | Numeric terms |
| [Streaming Transport & Aggregation](streaming-transport-aggregation.md) | Streaming aggs |

## Indexing & Documents

| Document | Description |
|----------|-------------|
| [Bulk API](bulk-api.md) | Bulk operations |
| [Reindex API](reindex-api.md) | Reindexing |
| [Streaming Indexing](streaming-indexing.md) | Stream ingestion |
| [Pull-based Ingestion](pull-based-ingestion.md) | Pull ingestion |
| [System Ingest Pipeline](system-ingest-pipeline.md) | Ingest pipelines |
| [Pipeline ID Limits](pipeline-id-limits.md) | Pipeline limits |
| [Grok Processor](grok-processor.md) | Grok parsing |
| [Index Settings](index-settings.md) | Index configuration |
| [Index Refresh](index-refresh.md) | Refresh behavior |
| [Index Output](index-output.md) | Index output |
| [Refresh Task Scheduling](refresh-task-scheduling.md) | Refresh scheduling |
| [Parallel Shard Refresh](parallel-shard-refresh.md) | Parallel refresh |
| [Translog](translog.md) | Transaction log |

## Field Types & Mapping

| Document | Description |
|----------|-------------|
| [Field Mapping](field-mapping.md) | Field mappings |
| [Dynamic Mapping](dynamic-mapping.md) | Auto mapping |
| [Mapping Transformer](mapping-transformer.md) | Mapping transforms |
| [Derived Fields](derived-fields.md) | Computed fields |
| [Derived Source](derived-source.md) | Source derivation |
| [Flat Object Field](flat-object-field.md) | Flat objects |
| [Wildcard Field](wildcard-field.md) | Wildcard type |
| [Filter Field Type](filter-field-type.md) | Filter type |
| [Scaled Float Field](scaled-float-field.md) | Scaled floats |
| [Unsigned Long](unsigned-long.md) | Unsigned longs |
| [Semantic Version Field](semantic-version-field-type.md) | Semver type |
| [Phone Analyzer](phone-analyzer.md) | Phone numbers |
| [Normalizer Enhancements](normalizer-enhancements.md) | Normalizers |
| [Date Format](date-format.md) | Date formatting |
| [Source Field Matching](source-field-matching.md) | Source matching |

## Cluster Management

| Document | Description |
|----------|-------------|
| [Cluster Management](cluster-management.md) | Cluster operations |
| [Cluster State Management](cluster-state-management.md) | State management |
| [Cluster State Caching](cluster-state-caching.md) | State caching |
| [Cluster State & Allocation](cluster-state-allocation.md) | Allocation |
| [Cluster Stats API](cluster-stats-api.md) | Cluster stats |
| [Cluster Info & Resource Stats](cluster-info-resource-stats.md) | Resource stats |
| [Cluster Manager Metrics](cluster-manager-metrics.md) | Manager metrics |
| [Cluster Manager Throttling](cluster-manager-throttling.md) | Throttling |
| [Cluster Permissions](cluster-permissions.md) | Permissions |
| [Cross-Cluster Settings](cross-cluster-settings.md) | Cross-cluster |
| [Clusterless Mode](clusterless-mode.md) | Standalone mode |

## Node Management

| Document | Description |
|----------|-------------|
| [Node Stats](node-stats.md) | Node statistics |
| [Nodes Info API](nodes-info-api.md) | Node info |
| [Node Join/Leave](node-join-leave.md) | Node lifecycle |
| [Node Roles Configuration](node-roles-configuration.md) | Node roles |
| [Offline Nodes](offline-nodes.md) | Background tasks |

## Shard & Segment

| Document | Description |
|----------|-------------|
| [Shard Allocation](shard-allocation.md) | Shard placement |
| [Async Shard Batch Fetch](async-shard-batch-fetch.md) | Async fetch |
| [Async Shard Fetch Metrics](async-shard-fetch-metrics.md) | Fetch metrics |
| [Segment Replication](segment-replication.md) | Segment sync |
| [Segment Warmer](segment-warmer.md) | Segment warming |
| [Context Aware Segments](context-aware-segments.md) | Smart segments |
| [Merge & Segment Settings](merge-segment-settings.md) | Merge config |
| [DocValues Optimization](docvalues-optimization.md) | DocValues |

## Remote Store & Repository

| Document | Description |
|----------|-------------|
| [Remote Store](remote-store.md) | Remote storage |
| [Remote Store Metadata API](remote-store-metadata-api.md) | Metadata API |
| [Remote Store Metrics](remote-store-metrics.md) | Store metrics |
| [S3 Repository](s3-repository.md) | S3 backend |
| [Azure Repository](azure-repository.md) | Azure backend |
| [HDFS Repository Kerberos](hdfs-repository-kerberos.md) | HDFS auth |
| [Repository Encryption](repository-encryption.md) | Encryption |
| [Repository Rate Limiters](repository-rate-limiters.md) | Rate limiting |
| [Snapshot Restore Enhancements](snapshot-restore-enhancements.md) | Snapshots |

## Caching

| Document | Description |
|----------|-------------|
| [Request Cache](request-cache.md) | Request caching |
| [Field Data Cache](field-data-cache.md) | Field data |
| [File Cache](file-cache.md) | File caching |
| [Tiered Caching](tiered-caching.md) | Cache tiers |

## Transport & Network

| Document | Description |
|----------|-------------|
| [gRPC Transport & Services](grpc-transport--services.md) | gRPC support |
| [Reactor Netty Transport](reactor-netty-transport.md) | Netty transport |
| [HTTP API](http-api.md) | HTTP interface |
| [HTTP/2 Support](http2-support.md) | HTTP/2 |
| [HTTP Client](http-client.md) | Client library |
| [Network Configuration](network-configuration.md) | Network config |
| [Netty Arena Settings](netty-arena-settings.md) | Netty tuning |
| [Transport Actions API](transport-actions-api.md) | Transport API |
| [Transport Nodes Action](transport-nodes-action-optimization.md) | Node actions |
| [Arrow Flight RPC](arrow-flight-rpc.md) | Arrow Flight |
| [Secure Transport Settings](secure-transport-settings.md) | TLS config |
| [Secure Aux Transport Settings](secure-aux-transport-settings.md) | Aux transport |

## Performance & Optimization

| Document | Description |
|----------|-------------|
| [Star Tree Index](star-tree-index.md) | Pre-aggregation |
| [Approximation Framework](approximation-framework.md) | Approximate queries |
| [Skip List](skip-list.md) | Skip lists |
| [OOM Prevention](oom-prevention.md) | Memory safety |
| [Workload Management](workload-management.md) | Resource management |
| [Rule-Based Auto-Tagging](rule-based-auto-tagging.md) | Query tagging |
| [Profiler](profiler.md) | Query profiling |

## Replication

| Document | Description |
|----------|-------------|
| [Replication](replication.md) | Data replication |
| [Search Replica & Reader-Writer](search-replica-reader-writer-separation.md) | Read/write split |
| [Warm Storage Tiering](warm-storage-tiering.md) | Storage tiers |

## Security

| Document | Description |
|----------|-------------|
| [Security Manager Replacement](security-manager-replacement.md) | Security migration |
| [Cryptography & Security Libraries](cryptography-security-libraries.md) | Crypto libs |
| [FIPS Compliance](fips-compliance.md) | FIPS support |
| [Crypto KMS Plugin](crypto-kms-plugin.md) | KMS integration |
| [Systemd Security](systemd-security-configurations.md) | Systemd hardening |

## Plugin & Extension

| Document | Description |
|----------|-------------|
| [Plugin Installation](plugin-installation.md) | Plugin setup |
| [Plugin Dependencies](plugin-dependencies.md) | Dependencies |
| [Plugin Testing Framework](plugin-testing-framework.md) | Testing |
| [Extensions Framework](extensions-framework.md) | Extensions |
| [Query Phase Plugin Extension](query-phase-plugin-extension.md) | Query plugins |
| [ActionPlugin REST Handler](actionplugin-rest-handler-wrapper.md) | REST handlers |
| [RestHandler.Wrapper](resthandler-wrapper.md) | Handler wrapper |

## APIs

| Document | Description |
|----------|-------------|
| [Cat Indices API](cat-indices-api.md) | Cat API |
| [List APIs (Paginated)](list-apis-paginated.md) | Paginated lists |
| [Client API Enhancements](client-api-enhancements.md) | Client API |
| [Custom Index Name Resolver](custom-index-name-resolver.md) | Name resolution |
| [Data Stream & Index Template](data-stream-index-template.md) | Data streams |
| [Alias Write Index Policy](alias-write-index-policy.md) | Alias policies |
| [Views](views.md) | Index views |

## Engine & Storage

| Document | Description |
|----------|-------------|
| [Engine API](engine-api.md) | Engine interface |
| [Engine Config](engine-config.md) | Engine settings |
| [Store Factory](store-factory.md) | Store creation |
| [Store Subdirectory Module](store-subdirectory-module.md) | Store modules |
| [Composite Directory Factory](composite-directory-factory.md) | Directory factory |

## Lucene

| Document | Description |
|----------|-------------|
| [Lucene 10 Upgrade](lucene-10-upgrade.md) | Lucene 10 |
| [Lucene Upgrade](lucene-upgrade.md) | Lucene updates |
| [Lucene Integration](lucene-integration.md) | Integration |
| [Lucene Similarity](lucene-similarity.md) | Similarity |

## Java & Runtime

| Document | Description |
|----------|-------------|
| [JDK 25 Support](jdk-25-support.md) | JDK 25 |
| [Java 17 Modernization](java-17-modernization.md) | Java 17 |
| [Java Runtime & JPMS](java-runtime-and-jpms.md) | Module system |
| [Java Agent AccessController](java-agent-accesscontroller.md) | Security manager |

## Threading & Tasks

| Document | Description |
|----------|-------------|
| [Thread Pool](thread-pool.md) | Thread pools |
| [Dynamic Threadpool Resize](dynamic-threadpool-resize.md) | Pool sizing |
| [Thread Context Permissions](thread-context-permissions.md) | Context perms |
| [Task Management](task-management.md) | Task handling |
| [Task Cancellation Monitoring](task-cancellation-monitoring.md) | Cancellation |
| [Query Coordinator Context](query-coordinator-context.md) | Coordinator |
| [Query Phase Result Consumer](query-phase-result-consumer.md) | Result handling |

## Serialization

| Document | Description |
|----------|-------------|
| [XContent Filtering](xcontent-filtering.md) | Content filtering |
| [XContent Transform](xcontent-transform.md) | Content transform |
| [Stream Input/Output](stream-inputoutput.md) | Streaming I/O |
| [Jackson & Query Limits](jackson--query-limits.md) | JSON limits |

## Build & Infrastructure

| Document | Description |
|----------|-------------|
| [Gradle Build System](gradle-build-system.md) | Build system |
| [Maven Snapshots Publishing](maven-snapshots-publishing.md) | Maven publish |
| [Docker Image Base](docker-image-base.md) | Docker images |
| [Docker Compose v2](docker-compose-v2-support.md) | Compose v2 |
| [Platform Support](platform-support.md) | OS support |
| [Code Coverage (Gradle)](code-coverage-gradle.md) | Coverage |

## Configuration

| Document | Description |
|----------|-------------|
| [Settings Management](settings-management.md) | Settings |
| [Dynamic Settings](dynamic-settings.md) | Dynamic config |
| [Configuration Utilities](configuration-utilities.md) | Config utils |
| [Locale Provider](locale-provider.md) | Locale |
| [Randomness](randomness.md) | Random generation |

## Maintenance

| Document | Description |
|----------|-------------|
| [Dependency Management](dependency-management.md) | Dependencies |
| [OpenSearch Core Dependencies](opensearch-core-dependencies.md) | Core deps |
| [Code Cleanup](code-cleanup.md) | Cleanup |
| [Deprecated Code Cleanup](deprecated-code-cleanup.md) | Deprecations |
| [DocRequest Refactoring](docrequest-refactoring.md) | Refactoring |
| [Stats Builder Pattern](stats-builder-pattern.md) | Stats pattern |
| [Subject Interface](subject-interface.md) | Subject API |
| [Identity Feature Flag Removal](identity-feature-flag-removal.md) | Feature flags |
| [Hierarchical & ACL-aware Routing](hierarchical-acl-aware-routing.md) | Routing |
| [Temporal Routing](temporal-routing.md) | Time routing |
