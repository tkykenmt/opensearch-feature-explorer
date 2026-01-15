---
tags:
  - dashboards-observability
---
# Observability Getting Started & Dashboards

## Summary

OpenSearch v2.16.0 introduces the Observability Overview and Getting Started pages in OpenSearch Dashboards. These new pages provide a guided onboarding experience for users to set up data ingestion pipelines and explore observability features. The Getting Started page offers step-by-step tutorials for configuring collectors, uploading files, and using sample datasets. Additionally, the OTel Services integration dashboards were replaced with streamlined getting started dashboards.

## Details

### What's New in v2.16.0

This release adds two new navigation pages to the Observability plugin:

1. **Observability Overview Page**: A landing page providing an overview of observability capabilities
2. **Getting Started Page**: An interactive wizard guiding users through data ingestion setup

### Technical Changes

#### New Components

| Component | File | Description |
|-----------|------|-------------|
| `GettingStartedHome` | `getting_started/home.tsx` | Main entry point for Getting Started page |
| `OverviewHome` | `overview/home.tsx` | Main entry point for Overview page |
| `NewGettingStarted` | `getting_started/components/getting_started.tsx` | Core Getting Started component |
| `CollectAndShipData` | `getting_started/components/getting_started_collectData.tsx` | Data collection wizard with three methods |
| `QueryAndAnalyze` | `getting_started/components/getting_started_queryAndAnalyze.tsx` | Query and visualization section |
| `IntegrationCards` | `getting_started/components/getting_started_integrationCards.tsx` | Sample dataset integration cards |

#### Navigation Registration

New navigation IDs and plugin order constants added to `common/constants/shared.ts`:

| Constant | Value | Description |
|----------|-------|-------------|
| `observabilityOverviewID` | `observability-overview` | Overview page ID |
| `observabilityOverviewPluginOrder` | `5088` | Navigation order |
| `observabilityGettingStartedID` | `observability-gettingStarted` | Getting Started page ID |
| `observabilityGettingStartedPluginOrder` | `5089` | Navigation order |

#### Data Collection Methods

The Getting Started page supports three data collection methods:

1. **Configure Collectors**: Setup agents like OpenTelemetry, Nginx, Java, Python, Golang
2. **Upload CSV/JSON**: Upload files using Fluent Bit
3. **Use Sample Dataset**: Explore with pre-built integration datasets

#### Getting Started Artifacts

New getting started artifacts added for multiple technologies:

- `csv_file/` - CSV file upload workflows with Fluent Bit and Data Prepper
- `golang_client/` - Golang client integration
- `java_client/` - Java client integration  
- `nginx/` - Nginx log integration
- `otel-services/` - OpenTelemetry services integration
- `python_client/` - Python client integration

#### OTel Services Dashboard Changes

The OTel Services integration was simplified by replacing multiple dashboards with index patterns only:

**Removed dashboards:**
- `otel_services_dashboard`
- `otel_single_service_dashboard`
- `otel_ingestion_rate_dashboard`
- `otel_amp_network_metrics_dashboard`
- `otel_apm_network_services`

**Added:**
- `otel-index-patterns` - Simplified index pattern asset

### Feature Flag

The new navigation pages are behind the new navigation home page feature flag.

## Limitations

- Feature requires the new navigation feature flag to be enabled
- Getting Started workflows are technology-specific and may not cover all use cases
- Sample datasets require the Integrations plugin to be installed

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1957](https://github.com/opensearch-project/dashboards-observability/pull/1957) | Observability Overview and GettingStarted pages | [#1929](https://github.com/opensearch-project/dashboards-observability/issues/1929) |
| [#1963](https://github.com/opensearch-project/dashboards-observability/pull/1963) | Replace dashboards with getting started dashboards | [opensearch-catalog#170](https://github.com/opensearch-project/opensearch-catalog/issues/170) |

### Related Issues
- [#1929](https://github.com/opensearch-project/dashboards-observability/issues/1929) - [FEATURE] Getting Started
- [opensearch-catalog#170](https://github.com/opensearch-project/opensearch-catalog/issues/170) - [BUG] Otel Services Demo is broken
