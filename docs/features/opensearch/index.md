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
| [Query Optimization](opensearch-query-optimization.md) | Query performance |
| [Query Performance Optimizations](opensearch-query-performance-optimizations.md) | Performance tuning |
| [Query Rewriting](opensearch-query-rewriting.md) | Query transformation |
| [Query Builders](opensearch-query-builders.md) | Query construction |
| [Query Cache](opensearch-query-cache.md) | Query caching |
| [Query String & Regex](opensearch-query-string-regex.md) | String queries |
| [Query String Monitoring](opensearch-query-string-monitoring.md) | Query monitoring |
| [Combined Fields Query](opensearch-combined-fields-query.md) | Multi-field search |
| [Parent-Child Query](opensearch-parent-child-query.md) | Nested queries |
| [Terms Query](opensearch-terms-query.md) | Terms matching |
| [Terms Lookup Query](opensearch-terms-lookup-query.md) | Terms lookup |
| [BooleanQuery Rewrite](opensearch-booleanquery-rewrite-optimizations.md) | Boolean optimization |
| [Automata & Regex Optimization](opensearch-automata-regex-optimization.md) | Regex performance |
| [Filter Rewrite Optimization](opensearch-filter-rewrite-optimization.md) | Filter optimization |
| [Rescore Named Queries](opensearch-rescore-named-queries.md) | Rescoring |
| [Search Scoring](opensearch-search-scoring.md) | Relevance scoring |
| [Search Settings](opensearch-search-settings.md) | Search configuration |
| [Search API Enhancements](opensearch-search-api-enhancements.md) | API improvements |
| [Search API Tracker](opensearch-search-api-tracker.md) | API tracking |
| [Search Pipeline](opensearch-search-pipeline.md) | Search pipelines |
| [Search Backpressure](opensearch-search-backpressure.md) | Load management |
| [Search Request Stats](opensearch-search-request-stats.md) | Request metrics |
| [Search Shard Routing](opensearch-search-shard-routing.md) | Shard routing |
| [Search Tie-breaking](opensearch-search-tie-breaking.md) | Result ordering |
| [Multi-Search API](opensearch-multi-search-api.md) | Batch search |
| [Scroll API](opensearch-scroll-api.md) | Pagination |
| [Concurrent Segment Search](opensearch-concurrent-segment-search.md) | Parallel search |
| [Field Collapsing](opensearch-field-collapsing.md) | Result grouping |
| [Unified Highlighter](opensearch-unified-highlighter.md) | Highlighting |

## Aggregations

| Document | Description |
|----------|-------------|
| [Aggregation Optimizations](opensearch-aggregation-optimizations.md) | Aggregation performance |
| [Aggregation Task Cancellation](opensearch-aggregation-task-cancellation.md) | Task management |
| [Composite Aggregation](opensearch-composite-aggregation.md) | Composite aggs |
| [Cardinality Aggregation](opensearch-cardinality-aggregation.md) | Distinct counts |
| [Nested Aggregations](opensearch-nested-aggregations.md) | Nested aggs |
| [Percentiles Aggregation](opensearch-percentiles-aggregation.md) | Percentiles |
| [Scripted Metric Aggregation](opensearch-scripted-metric-aggregation.md) | Custom metrics |
| [Numeric Terms Aggregation](opensearch-numeric-terms-aggregation-optimization.md) | Numeric terms |
| [Streaming Transport & Aggregation](opensearch-streaming-transport-aggregation.md) | Streaming aggs |

## Indexing & Documents

| Document | Description |
|----------|-------------|
| [Bulk API](opensearch-bulk-api.md) | Bulk operations |
| [Reindex API](opensearch-reindex-api.md) | Reindexing |
| [Streaming Indexing](opensearch-streaming-indexing.md) | Stream ingestion |
| [Pull-based Ingestion](opensearch-pull-based-ingestion.md) | Pull ingestion |
| [System Ingest Pipeline](opensearch-system-ingest-pipeline.md) | Ingest pipelines |
| [Pipeline ID Limits](opensearch-pipeline-id-limits.md) | Pipeline limits |
| [Grok Processor](opensearch-grok-processor.md) | Grok parsing |
| [Index Settings](opensearch-index-settings.md) | Index configuration |
| [Index Refresh](opensearch-index-refresh.md) | Refresh behavior |
| [Index Output](opensearch-index-output.md) | Index output |
| [Refresh Task Scheduling](opensearch-refresh-task-scheduling.md) | Refresh scheduling |
| [Parallel Shard Refresh](opensearch-parallel-shard-refresh.md) | Parallel refresh |
| [Translog](opensearch-translog.md) | Transaction log |

## Field Types & Mapping

| Document | Description |
|----------|-------------|
| [Field Mapping](opensearch-field-mapping.md) | Field mappings |
| [Dynamic Mapping](opensearch-dynamic-mapping.md) | Auto mapping |
| [Mapping Transformer](opensearch-mapping-transformer.md) | Mapping transforms |
| [Derived Fields](opensearch-derived-fields.md) | Computed fields |
| [Derived Source](opensearch-derived-source.md) | Source derivation |
| [Flat Object Field](opensearch-flat-object-field.md) | Flat objects |
| [Wildcard Field](opensearch-wildcard-field.md) | Wildcard type |
| [Filter Field Type](opensearch-filter-field-type.md) | Filter type |
| [Scaled Float Field](opensearch-scaled-float-field.md) | Scaled floats |
| [Unsigned Long](opensearch-unsigned-long.md) | Unsigned longs |
| [Semantic Version Field](opensearch-semantic-version-field-type.md) | Semver type |
| [Phone Analyzer](opensearch-phone-analyzer.md) | Phone numbers |
| [Normalizer Enhancements](opensearch-normalizer-enhancements.md) | Normalizers |
| [Date Format](opensearch-date-format.md) | Date formatting |
| [Source Field Matching](opensearch-source-field-matching.md) | Source matching |

## Cluster Management

| Document | Description |
|----------|-------------|
| [Cluster Management](opensearch-cluster-management.md) | Cluster operations |
| [Cluster State Management](opensearch-cluster-state-management.md) | State management |
| [Cluster State Caching](opensearch-cluster-state-caching.md) | State caching |
| [Cluster State & Allocation](opensearch-cluster-state-allocation.md) | Allocation |
| [Cluster Stats API](opensearch-cluster-stats-api.md) | Cluster stats |
| [Cluster Info & Resource Stats](opensearch-cluster-info-resource-stats.md) | Resource stats |
| [Cluster Manager Metrics](opensearch-cluster-manager-metrics.md) | Manager metrics |
| [Cluster Manager Throttling](opensearch-cluster-manager-throttling.md) | Throttling |
| [Cluster Permissions](opensearch-cluster-permissions.md) | Permissions |
| [Cross-Cluster Settings](opensearch-cross-cluster-settings.md) | Cross-cluster |
| [Clusterless Mode](opensearch-clusterless-mode.md) | Standalone mode |

## Node Management

| Document | Description |
|----------|-------------|
| [Node Stats](opensearch-node-stats.md) | Node statistics |
| [Nodes Info API](opensearch-nodes-info-api.md) | Node info |
| [Node Join/Leave](opensearch-node-join-leave.md) | Node lifecycle |
| [Node Roles Configuration](opensearch-node-roles-configuration.md) | Node roles |
| [Offline Nodes](opensearch-offline-nodes.md) | Background tasks |

## Shard & Segment

| Document | Description |
|----------|-------------|
| [Shard Allocation](opensearch-shard-allocation.md) | Shard placement |
| [Async Shard Batch Fetch](opensearch-async-shard-batch-fetch.md) | Async fetch |
| [Async Shard Fetch Metrics](opensearch-async-shard-fetch-metrics.md) | Fetch metrics |
| [Segment Replication](segment-opensearch-replication.md) | Segment sync |
| [Segment Warmer](opensearch-segment-warmer.md) | Segment warming |
| [Context Aware Segments](opensearch-context-aware-segments.md) | Smart segments |
| [Merge & Segment Settings](opensearch-merge-segment-settings.md) | Merge config |
| [DocValues Optimization](opensearch-docvalues-optimization.md) | DocValues |

## Remote Store & Repository

| Document | Description |
|----------|-------------|
| [Remote Store](opensearch-remote-store.md) | Remote storage |
| [Remote Store Metadata API](opensearch-remote-store-metadata-api.md) | Metadata API |
| [Remote Store Metrics](opensearch-remote-store-metrics.md) | Store metrics |
| [S3 Repository](opensearch-s3-repository.md) | S3 backend |
| [Azure Repository](opensearch-azure-repository.md) | Azure backend |
| [HDFS Repository Kerberos](opensearch-hdfs-repository-kerberos.md) | HDFS auth |
| [Repository Encryption](opensearch-repository-encryption.md) | Encryption |
| [Repository Rate Limiters](opensearch-repository-rate-limiters.md) | Rate limiting |
| [Snapshot Restore Enhancements](opensearch-snapshot-restore-enhancements.md) | Snapshots |

## Caching

| Document | Description |
|----------|-------------|
| [Request Cache](opensearch-request-cache.md) | Request caching |
| [Field Data Cache](opensearch-field-data-cache.md) | Field data |
| [File Cache](opensearch-file-cache.md) | File caching |
| [Tiered Caching](opensearch-tiered-caching.md) | Cache tiers |

## Transport & Network

| Document | Description |
|----------|-------------|
| [gRPC Transport & Services](opensearch-grpc-transport--services.md) | gRPC support |
| [Reactor Netty Transport](opensearch-reactor-netty-transport.md) | Netty transport |
| [HTTP API](opensearch-http-api.md) | HTTP interface |
| [HTTP/2 Support](opensearch-http2-support.md) | HTTP/2 |
| [HTTP Client](opensearch-http-client.md) | Client library |
| [Network Configuration](opensearch-network-configuration.md) | Network config |
| [Netty Arena Settings](opensearch-netty-arena-settings.md) | Netty tuning |
| [Transport Actions API](opensearch-transport-actions-api.md) | Transport API |
| [Transport Nodes Action](opensearch-transport-nodes-action-optimization.md) | Node actions |
| [Arrow Flight RPC](opensearch-arrow-flight-rpc.md) | Arrow Flight |
| [Secure Transport Settings](opensearch-secure-transport-settings.md) | TLS config |
| [Secure Aux Transport Settings](opensearch-secure-aux-transport-settings.md) | Aux transport |

## Performance & Optimization

| Document | Description |
|----------|-------------|
| [Star Tree Index](opensearch-star-tree-index.md) | Pre-aggregation |
| [Approximation Framework](opensearch-approximation-framework.md) | Approximate queries |
| [Skip List](opensearch-skip-list.md) | Skip lists |
| [OOM Prevention](opensearch-oom-prevention.md) | Memory safety |
| [Workload Management](opensearch-workload-management.md) | Resource management |
| [Rule-Based Auto-Tagging](opensearch-rule-based-auto-tagging.md) | Query tagging |
| [Profiler](opensearch-profiler.md) | Query profiling |

## Replication

| Document | Description |
|----------|-------------|
| [Replication](opensearch-replication.md) | Data replication |
| [Search Replica & Reader-Writer](opensearch-search-replica-reader-writer-separation.md) | Read/write split |
| [Warm Storage Tiering](opensearch-warm-storage-tiering.md) | Storage tiers |

## Security

| Document | Description |
|----------|-------------|
| [Security Manager Replacement](opensearch-security-manager-replacement.md) | Security migration |
| [Cryptography & Security Libraries](opensearch-cryptography-security-libraries.md) | Crypto libs |
| [FIPS Compliance](opensearch-fips-compliance.md) | FIPS support |
| [Crypto KMS Plugin](opensearch-crypto-kms-plugin.md) | KMS integration |
| [Systemd Security](opensearch-systemd-security-configurations.md) | Systemd hardening |

## Plugin & Extension

| Document | Description |
|----------|-------------|
| [Plugin Installation](opensearch-plugin-installation.md) | Plugin setup |
| [Plugin Dependencies](opensearch-plugin-dependencies.md) | Dependencies |
| [Plugin Testing Framework](opensearch-plugin-testing-framework.md) | Testing |
| [Extensions Framework](opensearch-extensions-framework.md) | Extensions |
| [Query Phase Plugin Extension](opensearch-query-phase-plugin-extension.md) | Query plugins |
| [ActionPlugin REST Handler](opensearch-actionplugin-rest-handler-wrapper.md) | REST handlers |
| [RestHandler.Wrapper](opensearch-resthandler-wrapper.md) | Handler wrapper |

## APIs

| Document | Description |
|----------|-------------|
| [Cat Indices API](opensearch-cat-indices-api.md) | Cat API |
| [List APIs (Paginated)](opensearch-list-apis-paginated.md) | Paginated lists |
| [Client API Enhancements](opensearch-client-api-enhancements.md) | Client API |
| [Custom Index Name Resolver](opensearch-custom-index-name-resolver.md) | Name resolution |
| [Data Stream & Index Template](opensearch-data-stream-index-template.md) | Data streams |
| [Alias Write Index Policy](opensearch-alias-write-index-policy.md) | Alias policies |
| [Views](opensearch-views.md) | Index views |

## Engine & Storage

| Document | Description |
|----------|-------------|
| [Engine API](opensearch-engine-api.md) | Engine interface |
| [Engine Config](opensearch-engine-config.md) | Engine settings |
| [Store Factory](opensearch-store-factory.md) | Store creation |
| [Store Subdirectory Module](opensearch-store-subdirectory-module.md) | Store modules |
| [Composite Directory Factory](opensearch-composite-directory-factory.md) | Directory factory |

## Lucene

| Document | Description |
|----------|-------------|
| [Lucene 10 Upgrade](opensearch-lucene-10-upgrade.md) | Lucene 10 |
| [Lucene Upgrade](opensearch-lucene-upgrade.md) | Lucene updates |
| [Lucene Integration](opensearch-lucene-integration.md) | Integration |
| [Lucene Similarity](opensearch-lucene-similarity.md) | Similarity |

## Java & Runtime

| Document | Description |
|----------|-------------|
| [JDK 25 Support](opensearch-jdk-25-support.md) | JDK 25 |
| [Java 17 Modernization](opensearch-java-17-modernization.md) | Java 17 |
| [Java Runtime & JPMS](opensearch-java-runtime-and-jpms.md) | Module system |
| [Java Agent AccessController](opensearch-java-agent-accesscontroller.md) | Security manager |

## Threading & Tasks

| Document | Description |
|----------|-------------|
| [Thread Pool](opensearch-thread-pool.md) | Thread pools |
| [Dynamic Threadpool Resize](opensearch-dynamic-threadpool-resize.md) | Pool sizing |
| [Thread Context Permissions](opensearch-thread-context-permissions.md) | Context perms |
| [Task Management](opensearch-task-management.md) | Task handling |
| [Task Cancellation Monitoring](opensearch-task-cancellation-monitoring.md) | Cancellation |
| [Query Coordinator Context](opensearch-query-coordinator-context.md) | Coordinator |
| [Query Phase Result Consumer](opensearch-query-phase-result-consumer.md) | Result handling |

## Serialization

| Document | Description |
|----------|-------------|
| [XContent Filtering](opensearch-xcontent-filtering.md) | Content filtering |
| [XContent Transform](opensearch-xcontent-transform.md) | Content transform |
| [Stream Input/Output](opensearch-stream-inputoutput.md) | Streaming I/O |
| [Jackson & Query Limits](opensearch-jackson--query-limits.md) | JSON limits |

## Build & Infrastructure

| Document | Description |
|----------|-------------|
| [Gradle Build System](opensearch-gradle-build-system.md) | Build system |
| [Maven Snapshots Publishing](opensearch-maven-snapshots-publishing.md) | Maven publish |
| [Docker Image Base](opensearch-docker-image-base.md) | Docker images |
| [Docker Compose v2](opensearch-docker-compose-v2-support.md) | Compose v2 |
| [Platform Support](opensearch-platform-support.md) | OS support |
| [Code Coverage (Gradle)](opensearch-code-coverage-gradle.md) | Coverage |

## Configuration

| Document | Description |
|----------|-------------|
| [Settings Management](opensearch-settings-management.md) | Settings |
| [Dynamic Settings](opensearch-dynamic-settings.md) | Dynamic config |
| [Configuration Utilities](opensearch-configuration-utilities.md) | Config utils |
| [Locale Provider](opensearch-locale-provider.md) | Locale |
| [Randomness](opensearch-randomness.md) | Random generation |

## Maintenance

| Document | Description |
|----------|-------------|
| [Dependency Management](opensearch-dependency-management.md) | Dependencies |
| [OpenSearch Core Dependencies](opensearch-core-dependencies.md) | Core deps |
| [Code Cleanup](opensearch-code-cleanup.md) | Cleanup |
| [Deprecated Code Cleanup](deprecated-opensearch-code-cleanup.md) | Deprecations |
| [DocRequest Refactoring](opensearch-docrequest-refactoring.md) | Refactoring |
| [Stats Builder Pattern](opensearch-stats-builder-pattern.md) | Stats pattern |
| [Subject Interface](opensearch-subject-interface.md) | Subject API |
| [Identity Feature Flag Removal](opensearch-identity-feature-flag-removal.md) | Feature flags |
| [Hierarchical & ACL-aware Routing](opensearch-hierarchical-acl-aware-routing.md) | Routing |
| [Temporal Routing](opensearch-temporal-routing.md) | Time routing |
