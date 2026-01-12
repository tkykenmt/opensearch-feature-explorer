# ISM Transitions Enhancement

## Summary

OpenSearch v3.2.0 introduces two new transition conditions for Index State Management (ISM): `no_alias` and `min_state_age`. These conditions enable more expressive lifecycle policies by allowing transitions based on alias presence and time spent in a specific state, addressing real-world operational workflows like retention-based archiving and alias-aware index management.

## Details

### What's New in v3.2.0

This release adds two new ISM transition conditions:

1. **`no_alias` (boolean)**: Gates transitions based on whether an index has any aliases
   - `true`: Transition only if the index has no aliases
   - `false`: Transition only if the index has at least one alias

2. **`min_state_age` (duration string)**: Allows transitions only after an index has spent a minimum time in its current ISM state
   - Accepts time values like `"5m"`, `"7d"`, `"24h"`
   - Starts counting from when the index enters the current state

Additionally, the ISM history index pattern (`.opendistro-ism-managed-index-history*`) is now registered as a System Index descriptor, improving security integration.

### Technical Changes

#### Why `min_state_age` vs `min_index_age`

The existing `min_index_age` condition measures time since index creation, which can lead to premature transitions. For example, if an index stays in a `hot` state for 5 days before transitioning to `archive` due to `no_alias: true`, a `min_index_age: 7d` condition would cause the index to move to `delete` just 2 days after entering `archive`.

`min_state_age` solves this by counting from when the index enters its current state, enabling accurate state-specific retention periods.

#### New Components

| Component | Description |
|-----------|-------------|
| `TransitionConditionContext` | New data class encapsulating all transition evaluation context |
| `checkNoAlias()` | Evaluates alias-based transition conditions |
| `checkMinStateAge()` | Evaluates state age-based transition conditions |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `no_alias` | Boolean condition for alias presence | N/A |
| `min_state_age` | Duration condition for time in current state | N/A |

### Usage Example

```json
{
  "policy": {
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [],
        "transitions": [
          {
            "state_name": "archive",
            "conditions": {
              "no_alias": true
            }
          }
        ]
      },
      {
        "name": "archive",
        "actions": [],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": {
              "min_state_age": "7d"
            }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [{ "delete": {} }],
        "transitions": []
      }
    ]
  }
}
```

This policy:
1. Transitions indexes from `hot` to `archive` when they are removed from all aliases
2. Keeps indexes in `archive` for exactly 7 days regardless of when they were created
3. Deletes indexes after the 7-day archive retention period

### Migration Notes

- Existing ISM policies continue to work without modification
- New conditions are available in v3.2.0+ only
- Version compatibility is handled automatically during cluster upgrades

## Limitations

- Only one transition condition can be specified per transition (cannot combine `no_alias` with `min_state_age` in a single transition)
- `min_state_age` requires the state metadata to have a valid `startTime`; if missing, the condition will not trigger
- The `no_alias` condition requires `indexAliasesCount` to be available in the transition context

## References

### Documentation
- [ISM Policies Documentation](https://docs.opensearch.org/3.0/im-plugin/ism/policies/): Official ISM documentation
- [Index State Management](https://docs.opensearch.org/3.0/im-plugin/ism/index/): ISM overview

### Pull Requests
| PR | Description |
|----|-------------|
| [#1440](https://github.com/opensearch-project/index-management/pull/1440) | Support for no_alias and min_state_age in ISM Transitions |
| [#1444](https://github.com/opensearch-project/index-management/pull/1444) | Add history index pattern to list of System Index descriptors |
| [#1442](https://github.com/opensearch-project/index-management/pull/1442) | Fix Integration test and lint errors |

### Issues (Design / RFC)
- [Issue #1439](https://github.com/opensearch-project/index-management/issues/1439): Feature request for no_alias and min_state_age
- [Issue #1441](https://github.com/opensearch-project/index-management/issues/1441): Integration test failure

## Related Feature Report

- [Full feature documentation](../../../../features/index-management/index-management.md)
