---
tags:
  - anomaly-detection
---
# Anomaly Detection

## Summary

OpenSearch 3.6.0 adds Terraform-based infrastructure-as-code support for anomaly detection detector provisioning and lifecycle management. A new `scripts/terraform/` module allows users to create, configure, start, stop, and destroy AD detectors using Terraform, with idempotent job handling via `local-exec` provisioners.

## Details

### What's New in v3.6.0

#### Terraform Detector Provisioning

A new Terraform configuration (`scripts/terraform/main.tf`) enables declarative management of anomaly detection detectors:

- Uses the `opensearch-project/opensearch` Terraform provider (v2.3.2+)
- Creates detectors via the `opensearch_anomaly_detection` resource
- Automatically handles detector job start/stop lifecycle through `null_resource` with `local-exec` provisioners
- Idempotent apply: stops then restarts the detector job on each apply
- Clean destroy: stops the detector job before deletion

#### Configurable Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `opensearch_url` | OpenSearch cluster endpoint | `http://localhost:9200` |
| `opensearch_username` | Authentication username | `""` (empty for unsecured) |
| `opensearch_password` | Authentication password (sensitive) | `""` |
| `detector_name` | Name of the detector | `tf-detector` |
| `indices` | Index pattern(s) to monitor | `["server-metrics"]` |
| `time_field` | Timestamp field name | `@timestamp` |
| `feature_field` | Numeric field for feature extraction (max aggregation) | `deny` |
| `detection_interval_minutes` | Detection interval in minutes | `1` |
| `window_delay_minutes` | Window delay in minutes | `1` |
| `result_index` | Custom result index name | `opensearch-ad-plugin-result-tf` |

#### Usage

```bash
# Initialize
terraform init

# Configure via environment variables (recommended for credentials)
export TF_VAR_opensearch_url='https://your-cluster:9200'
export TF_VAR_opensearch_username='admin'
export TF_VAR_opensearch_password='<password>'

# Apply
terraform apply

# Get detector ID
terraform output detector_id

# Destroy
terraform destroy
```

### Technical Changes

- Added `scripts/terraform/main.tf` with full Terraform configuration
- Added `scripts/terraform/README.md` with prerequisites, configuration, and usage documentation
- Updated `.gitignore` to exclude Terraform artifacts (`.terraform/`, `*.tfstate*`, `*.tfvars`)
- Test improvements in `CheckpointReadWorkerTests` to align request timestamps with both model state and queued checkpoint samples, preventing duplicate second-level timestamps during scoring
- Test fix in `AnomalyDetectorJobTransportActionTests` replacing `waitUntil` with `assertBusy` for more reliable historical analysis completion checks

## Limitations

- Terraform state may contain credentials even when provided via environment variables, due to `null_resource` trigger storage
- The Terraform module creates a single-feature detector using `max` aggregation; more complex configurations require manual customization
- Requires Terraform >= 1.5.0 and `curl` installed locally

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1680](https://github.com/opensearch-project/anomaly-detection/pull/1680) | Terraform-based AD detector provisioning and lifecycle automation | |
