---
tags:
  - domain/observability
  - component/dashboards
  - dashboards
  - indexing
  - observability
---
# Observability CI/Tests

## Summary

This release includes maintenance updates to the dashboards-observability CI/CD workflows, including a typo fix, updated test snapshots, and modernized integration test configurations. These changes ensure CI pipelines work correctly with OpenSearch 3.4.0 and use the new OpenSearch CI snapshot repository.

## Details

### What's New in v3.4.0

Three maintenance PRs improve the CI/CD infrastructure:

1. **Typo Fix**: Corrected "Functioanl" to "Functional" in workflow step name
2. **Snapshot Updates**: Updated unit test snapshots to include new `globalSearch` mock methods (`getAllSearchCommands$`, `registerSearchCommand`)
3. **CI Workflow Modernization**: Updated integration test workflows to use OpenSearch 3.4.0 and the new CI snapshot repository

### Technical Changes

#### CI Workflow Updates

| Workflow File | Change |
|---------------|--------|
| `ftr-e2e-dashboards-observability-test.yml` | Version bump to 3.4.0, new snapshot URL pattern |
| `integration-tests-workflow.yml` | Version bump to 3.4.0, new snapshot URL pattern |
| `dashboards-observability-test-and-build-workflow.yml` | Plugin version bump to 3.4.0.0 |
| `verify-binary-install.yml` | OpenSearch version bump to 3.4.0 |

#### Maven Repository Migration

The CI workflows now fetch plugin snapshots from the new OpenSearch CI repository instead of Sonatype:

| Before | After |
|--------|-------|
| `aws.oss.sonatype.org/service/local/artifact/maven/redirect?r=snapshots&g=org.opensearch.plugin&a={plugin}&v={version}-SNAPSHOT&p=zip` | `ci.opensearch.org/ci/dbc/snapshots/maven/org/opensearch/plugin/{plugin}/{version}/{plugin}-{snapshot-version}.zip` |

#### Dynamic Snapshot Version Resolution

New workflow steps dynamically resolve the latest snapshot version from maven-metadata.xml:

```yaml
- name: Get latest Job Scheduler snapshot version
  id: job-scheduler-snapshot
  run: |
    METADATA_URL="https://ci.opensearch.org/ci/dbc/snapshots/maven/org/opensearch/plugin/opensearch-job-scheduler/${{ env.OPENSEARCH_PLUGIN_VERSION }}/maven-metadata.xml"
    SNAPSHOT_VERSION=$(curl -s $METADATA_URL | grep '<value>' | head -1 | sed 's/.*<value>\(.*\)<\/value>.*/\1/')
    echo "version=$SNAPSHOT_VERSION" >> $GITHUB_OUTPUT
```

#### Improved Error Handling

Added debugging output when OpenSearch Dashboards fails to start:

```yaml
else
  echo "Timeout of 1200 seconds reached. OpenSearch Dashboards did not start successfully."
  echo "Last 100 lines of dashboard.log for debugging:"
  tail -100 dashboard.log
  exit 1
fi
```

#### Test Snapshot Updates

Updated component test snapshots to include new `globalSearch` mock interface methods:

- `getAllSearchCommands$`: Observable for search commands
- `registerSearchCommand`: Method to register search commands

Affected snapshot files:
- `log_config.test.tsx.snap`
- `service_config.test.tsx.snap`
- `trace_config.test.tsx.snap`
- `custom_panel_view.test.tsx.snap`
- `panel_grid.test.tsx.snap`
- `metrics_grid.test.tsx.snap`
- `dashboard.test.tsx.snap`
- `services.test.tsx.snap`
- `traces.test.tsx.snap`

## Limitations

- These are maintenance changes with no user-facing impact
- CI workflows are specific to the dashboards-observability repository

## References

### Documentation
- [dashboards-observability repository](https://github.com/opensearch-project/dashboards-observability)
- [OpenSearch CI Snapshots](https://ci.opensearch.org/ci/dbc/snapshots/maven/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#2501](https://github.com/opensearch-project/dashboards-observability/pull/2501) | Fix typo in checkout step name |
| [#2526](https://github.com/opensearch-project/dashboards-observability/pull/2526) | Update snapshots and unit tests |
| [#2528](https://github.com/opensearch-project/dashboards-observability/pull/2528) | Update CI workflows for Integ tests |

## Related Feature Report

- Full feature documentation
