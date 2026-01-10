# Query Profiler

## Summary

The Query Profiler (Profile API) provides detailed timing information about the execution of individual components of a search request. It helps debug slow queries and understand how to improve search performance by breaking down query execution into measurable components.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Search Request"
        SR[Search Request with profile=true]
    end
    
    subgraph "Query Execution"
        QE[Query Execution]
        CW[Create Weight]
        BS[Build Scorer]
        SC[Score Documents]
        CO[Collectors]
    end
    
    subgraph "Profiling Layer"
        QPB[QueryProfileBreakdown]
        CQPB[ConcurrentQueryProfileBreakdown]
        PT[Profile Timers]
    end
    
    subgraph "Output"
        PR[Profile Results]
        BD[Breakdown Map]
        CT[Collector Times]
        AT[Aggregation Times]
    end
    
    SR --> QE
    QE --> CW
    CW --> BS
    BS --> SC
    SC --> CO
    
    QE --> QPB
    QE --> CQPB
    QPB --> PT
    CQPB --> PT
    
    PT --> PR
    PR --> BD
    PR --> CT
    PR --> AT
```

### Data Flow

```mermaid
flowchart LR
    subgraph Input
        Q[Query with profile:true]
    end
    
    subgraph Execution
        W[Weight Creation]
        S[Scorer Building]
        D[Document Scoring]
        C[Collection]
    end
    
    subgraph Timing
        T1[create_weight]
        T2[build_scorer]
        T3[next_doc/advance]
        T4[score]
    end
    
    subgraph Output
        R[Profile Response]
    end
    
    Q --> W --> S --> D --> C
    W --> T1
    S --> T2
    D --> T3
    D --> T4
    T1 & T2 & T3 & T4 --> R
```

### Components

| Component | Description |
|-----------|-------------|
| `QueryProfileBreakdown` | Tracks timing for non-concurrent query execution |
| `ConcurrentQueryProfileBreakdown` | Tracks timing for concurrent segment search with slice-level statistics |
| `ProfileTimer` | Low-level timer for measuring individual operations |
| `ProfileCollector` | Wraps collectors to measure collection time |

### Configuration

The Profile API is enabled per-request using the `profile` parameter:

| Setting | Description | Default |
|---------|-------------|---------|
| `profile` | Enable profiling for the request | `false` |
| `human` | Return human-readable time values | `false` |

### Usage Example

```json
GET /myindex/_search
{
  "profile": true,
  "query": {
    "match": { "title": "opensearch" }
  }
}
```

Response includes breakdown timing:

```json
{
  "profile": {
    "shards": [{
      "searches": [{
        "query": [{
          "type": "TermQuery",
          "description": "title:opensearch",
          "time_in_nanos": 123456,
          "breakdown": {
            "create_weight": 10000,
            "create_weight_count": 1,
            "build_scorer": 50000,
            "build_scorer_count": 2,
            "next_doc": 30000,
            "next_doc_count": 100,
            "score": 20000,
            "score_count": 100
          }
        }]
      }]
    }]
  }
}
```

### Concurrent Segment Search Support

When concurrent segment search is enabled, the profiler provides additional slice-level statistics:

| Field | Description |
|-------|-------------|
| `max_slice_time_in_nanos` | Maximum time across all slices |
| `min_slice_time_in_nanos` | Minimum time across all slices |
| `avg_slice_time_in_nanos` | Average time across all slices |
| `slice_count` | Number of slices executed |

## Limitations

- Profiling adds overhead to search operations
- Does not measure network latency
- Does not measure fetch phase time
- Does not measure queue wait time

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.2.0 | [#18540](https://github.com/opensearch-project/OpenSearch/pull/18540) | Fix concurrent timings in profiler |

## References

- [Profile API Documentation](https://docs.opensearch.org/3.0/api-reference/search-apis/profile/): Official API reference
- [Concurrent Segment Search](https://docs.opensearch.org/3.0/search-plugins/concurrent-segment-search/): Related feature

## Change History

- **v3.2.0** (2025-06-21): Fixed incorrect timing values for concurrent segment search when timers have zero invocations
