# ML Commons Connectors & Blueprints

## Summary

This release adds new connector blueprints and tutorials for ML Commons, including support for Amazon Bedrock Converse API, cross-account model invocation, role-based temporary credentials, and Titan Embedding V2 model configuration.

## Details

### What's New in v2.18.0

Four documentation and blueprint improvements were added to ML Commons:

1. **Amazon Bedrock Converse Blueprint** - New connector blueprint for the Amazon Bedrock Converse API
2. **Cross-Account Model Invocation Tutorial** - Guide for invoking Bedrock models from a different AWS account
3. **Role Temporary Credential Support** - Enhanced AIConnectorHelper to support IAM role-based authentication
4. **Titan Embedding V2 Blueprint** - Updated blueprint with V2-specific parameters

### Technical Changes

#### New Connector Blueprint: Bedrock Converse

A new blueprint was added for Amazon Bedrock's Converse API, enabling chat-style interactions with models like Claude 3 Sonnet:

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Amazon Bedrock Converse",
    "description": "Connector for Amazon Bedrock Converse",
    "version": 1,
    "protocol": "aws_sigv4",
    "credential": {
        "roleArn": "<YOUR_ROLE_ARN>"
    },
    "parameters": {
        "region": "<AWS_REGION>",
        "service_name": "bedrock",
        "response_filter": "$.output.message.content[0].text",
        "model": "anthropic.claude-3-sonnet-20240229-v1:0"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
            "request_body": "{\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"${parameters.inputs}\"}]}]}"
        }
    ]
}
```

#### Cross-Account Model Invocation

New tutorial for invoking Bedrock models across AWS accounts using:

| Credential | Description |
|------------|-------------|
| `roleArn` | IAM role in Account A to assume external role |
| `externalAccountRoleArn` | IAM role in Account B with Bedrock permissions |

This feature enables organizations to centralize ML model access while maintaining separate OpenSearch clusters.

#### AIConnectorHelper Enhancements

The `AIConnectorHelper` Python class was updated to support:

- IAM role-based authentication (in addition to IAM user)
- Flexible trust policy generation for both users and roles
- Session token support for temporary credentials

```python
helper = AIConnectorHelper(
    region,
    opensearch_domain_name,
    opensearch_domain_username,
    opensearch_domain_password,
    aws_user_name,      # Optional: IAM user name
    aws_role_name       # Optional: IAM role name
)
```

#### Titan Embedding V2 Configuration

Updated blueprint for Titan Embedding V2 with new parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `model` | Model identifier | `amazon.titan-embed-text-v2:0` |
| `dimensions` | Embedding dimensions | 1024 |
| `normalize` | Normalize embeddings | true |
| `embeddingTypes` | Output type | `["float"]` |

### Usage Example

Cross-account connector configuration:

```json
{
  "credential": {
    "roleArn": "arn:aws:iam::<account_A>:role/my_cross_account_role",
    "externalAccountRoleArn": "arn:aws:iam::<account_B>:role/my_invoke_bedrock_role"
  }
}
```

## Limitations

- Cross-account model invocation requires OpenSearch 2.15+
- `binary` embedding type not supported in built-in post-process function for Titan V2
- Neural search plugin only supports one embedding per document

## Related PRs

| PR | Description |
|----|-------------|
| [#2960](https://github.com/opensearch-project/ml-commons/pull/2960) | Connector blueprint for Amazon Bedrock Converse |
| [#3058](https://github.com/opensearch-project/ml-commons/pull/3058) | Support role temporary credential in connector tutorial |
| [#3064](https://github.com/opensearch-project/ml-commons/pull/3064) | Add tutorial for cross-account model invocation |
| [#3094](https://github.com/opensearch-project/ml-commons/pull/3094) | Tune Titan embedding model blueprint for V2 |

## References

- [Connector Blueprints Documentation](https://docs.opensearch.org/2.18/ml-commons-plugin/remote-models/blueprints/)
- [Connectors Overview](https://docs.opensearch.org/2.18/ml-commons-plugin/remote-models/connectors/)
- [Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [Bedrock Titan Embedding Models](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-commons-blueprints.md)
