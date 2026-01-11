# Search Utilities

## Summary

OpenSearch 3.0.0 adds a new depth-first search (DFS) transformation function to `XContentMapValues`, enabling efficient in-place or copy-based transformations of nested map structures. This utility is primarily designed to support the k-NN plugin's derived source feature, which removes vectors from `_source` to reduce storage overhead while maintaining full OpenSearch functionality.

## Details

### What's New in v3.0.0

A new `transform()` method has been added to `XContentMapValues` that performs depth-first traversal on maps, applying field-specific transformations along the way. This enables plugins to efficiently modify nested document structures without altering the overall map hierarchy.

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "XContentMapValues.transform()"
        Input[Source Map] --> Trie[Build Transformer Trie]
        Trie --> Stack[Initialize Stack]
        Stack --> DFS[Depth-First Traversal]
        DFS --> Apply[Apply Transformers]
        Apply --> Output[Transformed Map]
    end
    
    subgraph "Use Case: k-NN Derived Source"
        Vector[Vector Field] --> Mask[Mask/Transform]
        Mask --> Smaller[Smaller Representation]
        Smaller --> Storage[Reduced Storage]
    end
```

#### New Components

| Component | Description |
|-----------|-------------|
| `XContentMapValues.transform()` | Static method that applies field-specific transformations via DFS traversal |
| `TransformContext` | Internal class holding map and trie state during traversal |
| Transformer Trie | Path-based lookup structure for efficient transformer matching |

#### New API

```java
// Transform with copy
Map<String, Object> transform(
    Map<String, Object> source,
    Map<String, Function<Object, Object>> transformers,
    boolean inPlace
)

// Get reusable transform function
Function<Map<String, Object>, Map<String, Object>> transform(
    Map<String, Function<Object, Object>> transformers,
    boolean inPlace
)
```

| Parameter | Description |
|-----------|-------------|
| `source` | Source map to transform |
| `transformers` | Map from dot-notation path to transformer function |
| `inPlace` | If true, modify source directly; if false, create a copy |

### Usage Example

```java
// Define transformers for specific paths
Map<String, Function<Object, Object>> transformers = Map.of(
    "vector_field", v -> "[MASKED]",
    "nested.vector", v -> "[MASKED]"
);

// Transform a document map
Map<String, Object> source = Map.of(
    "title", "Document",
    "vector_field", List.of(0.1, 0.2, 0.3),
    "nested", Map.of("vector", List.of(0.4, 0.5))
);

// Create transformed copy
Map<String, Object> result = XContentMapValues.transform(source, transformers, false);
// Result: {"title": "Document", "vector_field": "[MASKED]", "nested": {"vector": "[MASKED]"}}
```

### Key Features

- **Path-based transformers**: Use dot notation (e.g., `"nested.field"`) to target specific fields
- **Nested structure support**: Handles deeply nested maps and lists of maps
- **In-place or copy mode**: Choose between modifying the original or creating a new map
- **Shortest path wins**: For overlapping paths, only the shorter path's transformer is applied
- **Preserves structure**: Unlike `filter()`, empty objects in arrays are not removed

### Migration Notes

This is a new utility method with no breaking changes. Existing code using `XContentMapValues.filter()` continues to work unchanged.

## Limitations

- Transformers are applied based on exact path matching; wildcard patterns are not supported
- The transformer function receives the current value and must return the transformed value
- For overlapping paths (e.g., `"test"` and `"test.nested"`), only the shorter path's transformer is applied

## Related PRs

| PR | Description |
|----|-------------|
| [#17612](https://github.com/opensearch-project/OpenSearch/pull/17612) | Add dfs transformation function in XContentMapValues |

## References

- [Issue #2377](https://github.com/opensearch-project/k-NN/issues/2377): RFC - Derived Source for Vectors
- [k-NN PR #2583](https://github.com/opensearch-project/k-NN/pull/2583): Related k-NN implementation

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/xcontent-transform.md)
