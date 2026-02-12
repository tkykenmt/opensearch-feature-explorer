---
tags:
  - neural-search
---
# Agentic Search Enhancements

## Summary

Enhancements to the Agentic Search feature in v3.3.2 focused on improving conversation search support, robust JSON extraction from LLM responses, and model-type-aware summary trace extraction.

## Details

### What's New in v3.3.2

#### Conversation Search Support (neural-search#1626)
Added conversation search support with agentic search by storing the `ext` parameters passed in the search request. This enables the `retrieval_augmented_generation` extension to carry conversation context (answer and message_id) through the search pipeline.

Response extension format:
```json
{
  "ext": {
    "retrieval_augmented_generation": {
      "answer": "...",
      "message_id": "L0rWA5oBxjfdJ-H1juTm"
    }
  }
}
```

#### JSON Extraction from Agent Response (neural-search#1631)
Added a helper function to extract valid JSON from LLM responses that may contain surrounding text. When a model produces output like `"Here is your query: {\"query\":{\"match\":{\"title\":\"test\"}}}"`, the actual JSON is now correctly extracted. Also changed the exception type from `IllegalStateException` to `IllegalArgumentException` when the LLM responds with malformed JSON.

#### Model-Type-Aware Summary Extraction (neural-search#1633)
Extracts agent summary trace based on the model type, enabling more accurate summary extraction from different LLM providers.

#### Query Planning Tool JSON Processor (ml-commons#4356)
Added an extract JSON processor in the Query Planning Tool to handle cases where models produce extra text around the generated DSL query. This ensures the actual JSON query is correctly parsed even when wrapped in explanatory text.

## References

| PR | Repository | Description |
|----|------------|-------------|
| [#1626](https://github.com/opensearch-project/neural-search/pull/1626) | neural-search | Add conversation search support with agentic search |
| [#1631](https://github.com/opensearch-project/neural-search/pull/1631) | neural-search | Extract JSON from Agent Response |
| [#1633](https://github.com/opensearch-project/neural-search/pull/1633) | neural-search | Extract agent summary based on models |
| [#4356](https://github.com/opensearch-project/ml-commons/pull/4356) | ml-commons | Add extract JSON processor in Query Planning Tool |
| [#1525](https://github.com/opensearch-project/neural-search/issues/1525) | neural-search | Related tracking issue |
