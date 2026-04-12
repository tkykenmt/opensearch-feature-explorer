---
tags:
  - release
  - v2.6.0
---
# OpenSearch v2.6.0 Release Summary

## Overview

OpenSearch 2.6.0 was released with 43 feature groups encompassing 71 new features, 37 enhancements, and 150 bug fixes across the OpenSearch ecosystem.

## Highlights

### Security Analytics Enhancements
Security Analytics received the largest set of changes with 37 items including new log types, dashboard creation capabilities, field mapping improvements, multi-select data source support for detectors, and various UX/UI improvements across the detectors and findings pages.

### SQL/PPL Engine Improvements
The SQL/PPL engine gained 12 enhancements focused on date/time functions including `DATE_ADD`, `DATE_SUB`, `GET_FORMAT`, `TIME_FORMAT`, `last_day`, and `WeekOfYear`. Additional improvements include escape character support for string literals, extended comparison methods for datetime types, and `concat()` supporting multiple arguments.

### Index Management Operations
New index management operations were added including force merge, data stream management page, and rollover operations, expanding the ISM policy capabilities.

### Dashboards Maps as Embeddable
Maps can now be embedded directly into dashboards with support for sample datasets, dashboard filters via index patterns, and improved layer management with scroll bars and close buttons for tooltips.

### OpenSearch Core Features

#### Index Create Block
A new mechanism automatically blocks index creation when all nodes breach the high disk watermark, with a configurable setting to control auto-release of the block.

#### Segment Replication
New `cat/segment_replication` API to surface replication metrics, along with fixes for peer recovery and sequence number accuracy during replication.

#### Extensions Framework
Extensions gained query support for initialized extensions, CompletableFutures replacing latches, and minimum compatible version support.

#### Search Task Cancellation
In-flight search tasks can now be cancelled based on resource consumption, improving cluster stability under heavy load.

#### Cluster Guardrails
A new guardrail limits the maximum number of shards on a cluster, preventing resource exhaustion.

#### Weighted Shard Routing
Support for disallowing search requests with preference parameter under strict weighted shard routing, plus state consistency fixes across search requests.

### Multiple DataSource (Dashboards)
SigV4 authentication support was added for multiple data sources, with refactored test connection to support the new auth type.

### ML Commons
Prebuilt model support was enabled, allowing users to deploy pre-trained models more easily.

### Alerting
Document-level monitors now support multiple indices as input, expanding monitoring capabilities.

## Statistics

| Category | Count |
|----------|-------|
| Feature Groups | 43 |
| New Features | 71 |
| Enhancements | 37 |
| Bug Fixes | 150 |
| Total Items | 258 |

## Feature Groups

| Group | Features | Enhancements | Bug Fixes | Total |
|-------|----------|--------------|-----------|-------|
| Security Analytics | 12 | 10 | 15 | 37 |
| SQL/PPL Engine | 0 | 12 | 18 | 30 |
| Observability | 1 | 0 | 19 | 20 |
| Dependency Upgrades | 16 | 0 | 3 | 19 |
| Security Plugin | 1 | 5 | 10 | 16 |
| Index Management | 3 | 0 | 10 | 13 |
| Dashboards Maps | 2 | 6 | 5 | 13 |
| Alerting | 1 | 0 | 11 | 12 |
| ML Commons | 1 | 0 | 7 | 8 |
| Anomaly Detection | 0 | 3 | 5 | 8 |
| k-NN | 0 | 0 | 8 | 8 |
| Notifications | 0 | 0 | 8 | 8 |
| CI/Build Infrastructure | 0 | 0 | 8 | 8 |
| Performance Analyzer | 1 | 0 | 5 | 6 |
| Geospatial | 2 | 0 | 3 | 5 |
| Extensions | 4 | 0 | 0 | 4 |
| Segment Replication | 4 | 0 | 0 | 4 |
| Reporting | 0 | 0 | 3 | 3 |
| Query Workbench | 0 | 0 | 3 | 3 |
| Index Create Block | 3 | 0 | 0 | 3 |
| Cross-Cluster Replication | 0 | 1 | 1 | 2 |
| Code Refactoring | 1 | 0 | 1 | 2 |
| Weighted Shard Routing | 2 | 0 | 0 | 2 |
| Remote-Backed Indexes | 2 | 0 | 0 | 2 |
| Refactor | 2 | 0 | 0 | 2 |
| Multiple DataSource | 2 | 0 | 0 | 2 |
| OpenSearch Dashboards Build | 0 | 0 | 2 | 2 |
| Neural Search | 0 | 0 | 1 | 1 |
| Asynchronous Search | 0 | 0 | 1 | 1 |
| Cluster Manager Throttling | 1 | 0 | 0 | 1 |
| Feature Flags | 1 | 0 | 0 | 1 |
| Searchable Snapshots | 1 | 0 | 0 | 1 |
| Cluster Guardrails | 1 | 0 | 0 | 1 |
| Search Task Cancellation | 1 | 0 | 0 | 1 |
| Platform Support | 1 | 0 | 0 | 1 |
| Node Decommissioning | 1 | 0 | 0 | 1 |
| API Improvements | 1 | 0 | 0 | 1 |
| Search Optimizations | 1 | 0 | 0 | 1 |
| Repository S3 Plugin | 1 | 0 | 0 | 1 |
| OpenSearch Dashboards Core | 1 | 0 | 0 | 1 |
| Search Telemetry | 0 | 0 | 1 | 1 |
| Region Maps | 0 | 0 | 1 | 1 |
| Documentation Fixes | 0 | 0 | 1 | 1 |

## References

- [OpenSearch 2.6.0 Release Notes](https://github.com/opensearch-project/opensearch-build/blob/main/release-notes/opensearch-release-notes-2.6.0.md)
- [OpenSearch Dashboards 2.6.0 Release Notes](https://github.com/opensearch-project/opensearch-build/blob/main/release-notes/opensearch-dashboards-release-notes-2.6.0.md)
