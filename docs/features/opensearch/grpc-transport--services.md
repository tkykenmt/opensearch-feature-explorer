# gRPC Transport & Services

## Summary

gRPC Transport & Services provides an alternative communication protocol for OpenSearch, enabling high-performance, binary-encoded API access using protocol buffers over gRPC. This feature allows client applications in Java, Go, Python, and other languages to interact with OpenSearch using native gRPC stubs, offering lower latency and higher throughput compared to traditional HTTP REST APIs for high-volume workloads.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Client Applications"
        JavaClient[Java Client]
        GoClient[Go Client]
        PythonClient[Python Client]
        OtherClient[Other gRPC Clients]
    end
    
    subgraph "OpenSearch Cluster"
        subgraph "Node 1"
            HTTP1[HTTP Transport<br/>Port 9200]
            GRPC1[gRPC Transport<br/>Port 9400]
            Core1[OpenSearch Core]
        end
        
        subgraph "Node 2"
            HTTP2[HTTP Transport<br/>Port 9200]
            GRPC2[gRPC Transport<br/>Port 9400]
            Core2[OpenSearch Core]
        end
    end
    
    subgraph "gRPC Services"
        DocService[DocumentService<br/>- Bulk]
        SearchService[SearchService<br/>- Search]
    end
    
    JavaClient -->|Protocol Buffers| GRPC1
    GoClient -->|Protocol Buffers| GRPC1
    PythonClient -->|Protocol Buffers| GRPC2
    OtherClient -->|Protocol Buffers| GRPC2
    
    GRPC1 --> DocService
    GRPC1 --> SearchService
    GRPC2 --> DocService
    GRPC2 --> SearchService
    
    DocService --> Core1
    DocService --> Core2
    SearchService --> Core1
    SearchService --> Core2
```

### Data Flow

```mermaid
flowchart TB
    subgraph Client
        Proto[Protocol Buffer<br/>Message]
    end
    
    subgraph "gRPC Transport"
        Serialize[Serialize to<br/>Binary]
        TLS[TLS Encryption<br/>Optional]
        Deserialize[Deserialize<br/>Response]
    end
    
    subgraph "OpenSearch"
        Service[gRPC Service<br/>Handler]
        Execute[Execute<br/>Operation]
        Response[Build<br/>Response]
    end
    
    Proto --> Serialize
    Serialize --> TLS
    TLS -->|HTTP/2| Service
    Service --> Execute
    Execute --> Response
    Response -->|HTTP/2| Deserialize
    Deserialize --> Client
```

### Components

| Component | Description |
|-----------|-------------|
| `transport-grpc` | Plugin providing gRPC server transport capability |
| `Netty4GrpcServerTransport` | Base gRPC server implementation using Netty4 |
| `SecureNetty4GrpcServerTransport` | TLS-enabled gRPC transport for secure connections |
| `DocumentService` | gRPC service handling document operations (Bulk API) |
| `SearchService` | gRPC service handling search operations (Search API) |
| `opensearch-protobufs` | Protocol buffer definitions for OpenSearch APIs |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `grpc.port` | Port for gRPC server to listen on | `9400` |
| `grpc.publish_port` | Port published for external connections | Same as `grpc.port` |
| `grpc.bind_host` | Network interface to bind gRPC server | Network host setting |
| `grpc.publish_host` | Host address published for gRPC | Network host setting |

### Supported Services

#### DocumentService

The DocumentService provides the Bulk API for batch document operations:

| Operation | Description |
|-----------|-------------|
| `index` | Index a document (creates or replaces) |
| `create` | Create a new document (fails if exists) |
| `update` | Partially update an existing document |
| `delete` | Delete a document by ID |

**Request Fields:**
- `request_body`: List of bulk operations
- `index`: Default index for operations
- `pipeline`: Ingest pipeline ID
- `refresh`: Refresh behavior after indexing
- `routing`: Custom routing value
- `timeout`: Operation timeout

#### SearchService

The SearchService provides the Search API for querying documents:

**Supported Query Types:**
- `match_all`: Match all documents
- `term`: Exact term matching on a field
- `terms`: Match any of multiple terms
- `match_none`: Match no documents

**Request Fields:**
- `index`: Target indexes
- `request_body`: Search request with query DSL
- `source`: Control `_source` field return
- `from`/`size`: Pagination
- `sort`: Result ordering
- `timeout`: Query timeout

### Usage Example

**Installing the Plugin:**

```bash
bin/opensearch-plugin install transport-grpc
```

**Java Client Example:**

```java
import org.opensearch.protobufs.*;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import com.google.protobuf.ByteString;

// Create channel
ManagedChannel channel = ManagedChannelBuilder
    .forAddress("localhost", 9400)
    .usePlaintext()
    .build();

// Bulk indexing
DocumentServiceGrpc.DocumentServiceBlockingStub docStub = 
    DocumentServiceGrpc.newBlockingStub(channel);

BulkRequest bulkRequest = BulkRequest.newBuilder()
    .setIndex("my-index")
    .addRequestBody(BulkRequestBody.newBuilder()
        .setIndex(IndexOperation.newBuilder()
            .setId("1")
            .build())
        .setDoc(ByteString.copyFromUtf8("{\"title\": \"Document 1\"}"))
        .build())
    .build();

BulkResponse bulkResponse = docStub.bulk(bulkRequest);

// Search
SearchServiceGrpc.SearchServiceBlockingStub searchStub = 
    SearchServiceGrpc.newBlockingStub(channel);

SearchRequest searchRequest = SearchRequest.newBuilder()
    .addIndex("my-index")
    .setRequestBody(SearchRequestBody.newBuilder()
        .setQuery(QueryContainer.newBuilder()
            .setTerm(TermQuery.newBuilder()
                .putTerm("title", TermQueryField.newBuilder()
                    .setValue(FieldValue.newBuilder()
                        .setStringValue("Document")
                        .build())
                    .build())
                .build())
            .build())
        .setSize(10)
        .build())
    .build();

SearchResponse searchResponse = searchStub.search(searchRequest);

channel.shutdown();
```

**Document Encoding:**

Documents in gRPC requests must be Base64 encoded:

```json
// Original document
{"title": "Inception", "year": 2010}

// Base64 encoded for gRPC
"eyJ0aXRsZSI6ICJJbmNlcHRpb24iLCAieWVhciI6IDIwMTB9"
```

## Limitations

- **Experimental status**: Feature is experimental and not recommended for production
- **Limited query support**: Only basic queries (match_all, term, terms, match_none) supported
- **No aggregations**: Aggregation support not yet available
- **Limited services**: Only Bulk and Search endpoints implemented
- **Plugin required**: Must install transport-grpc plugin separately

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.0.0 | [#17796](https://github.com/opensearch-project/OpenSearch/pull/17796) | Enable TLS for Netty4GrpcServerTransport |
| v3.0.0 | [#17727](https://github.com/opensearch-project/OpenSearch/pull/17727) | Add DocumentService and Bulk gRPC endpoint v1 |
| v3.0.0 | [#17830](https://github.com/opensearch-project/OpenSearch/pull/17830) | SearchService and Search gRPC endpoint v1 |
| v3.0.0 | [#17888](https://github.com/opensearch-project/OpenSearch/pull/17888) | Add terms query support in Search gRPC endpoint |

## References

- [Issue #16787](https://github.com/opensearch-project/OpenSearch/issues/16787): gRPC Transport tracking issue
- [gRPC APIs Documentation](https://docs.opensearch.org/3.0/api-reference/grpc-apis/index/): Official documentation
- [Bulk (gRPC) API](https://docs.opensearch.org/3.0/api-reference/grpc-apis/bulk/): Bulk endpoint reference
- [Search (gRPC) API](https://docs.opensearch.org/3.0/api-reference/grpc-apis/search/): Search endpoint reference
- [opensearch-protobufs](https://github.com/opensearch-project/opensearch-protobufs): Protocol buffer definitions
- [Additional Plugins](https://docs.opensearch.org/3.0/install-and-configure/additional-plugins/index/): Plugin installation guide

## Change History

- **v3.0.0** (2025-03): Initial implementation with DocumentService (Bulk) and SearchService (Search), TLS support
