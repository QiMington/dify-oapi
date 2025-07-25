# Dataset Management APIs

This document covers all dataset (knowledge base) management APIs including creation, listing, updating, and deletion operations.

## Authentication

All Service API requests use `API-Key` for authentication. Include your `API-Key` in the **`Authorization`** HTTP Header:

```
Authorization: Bearer {API_KEY}
```

## APIs

### 1. Create Empty Dataset

**POST** `/datasets`

Creates an empty knowledge base.

#### Request Body
- `name` (string, required): Knowledge base name
- `description` (string, optional): Knowledge base description
- `indexing_technique` (string, optional): Indexing mode (recommended to provide)
  - `high_quality`: High quality
  - `economy`: Economy
- `permission` (string, optional): Permission level (default: `only_me`)
  - `only_me`: Only me
  - `all_team_members`: All team members
  - `partial_members`: Partial team members
- `provider` (string, optional): Provider type (default: `vendor`)
  - `vendor`: Upload files
  - `external`: External knowledge base
- `external_knowledge_api_id` (string, optional): External knowledge base API ID
- `external_knowledge_id` (string, optional): External knowledge base ID
- `embedding_model` (string, optional): Embedding model name
- `embedding_model_provider` (string, optional): Embedding model provider
- `retrieval_model` (object, optional): Retrieval mode configuration
  - `search_method` (string): Search method - `hybrid_search`, `semantic_search`, `full_text_search`
  - `reranking_enable` (boolean): Enable reranking
  - `reranking_model` (object): Rerank model configuration
    - `reranking_provider_name` (string): Rerank model provider
    - `reranking_model_name` (string): Rerank model name
  - `top_k` (integer): Number of results to return
  - `score_threshold_enabled` (boolean): Enable score threshold
  - `score_threshold` (float): Score threshold value

#### Response
```json
{
  "id": "",
  "name": "name",
  "description": null,
  "provider": "vendor",
  "permission": "only_me",
  "data_source_type": null,
  "indexing_technique": null,
  "app_count": 0,
  "document_count": 0,
  "word_count": 0,
  "created_by": "",
  "created_at": 1695636173,
  "updated_by": "",
  "updated_at": 1695636173,
  "embedding_model": null,
  "embedding_model_provider": null,
  "embedding_available": null
}
```

### 2. List Datasets

**GET** `/datasets`

Retrieves a list of knowledge bases.

#### Query Parameters
- `keyword` (string, optional): Search keyword
- `tag_ids` (array[string], optional): Tag ID list
- `page` (integer, optional): Page number (default: 1)
- `limit` (string, optional): Number of results (default: 20, range: 1-100)
- `include_all` (boolean, optional): Include all datasets (owner only, default: false)

#### Response
```json
{
  "data": [
    {
      "id": "",
      "name": "知识库名称",
      "description": "描述信息",
      "permission": "only_me",
      "data_source_type": "upload_file",
      "indexing_technique": "",
      "app_count": 2,
      "document_count": 10,
      "word_count": 1200,
      "created_by": "",
      "created_at": "",
      "updated_by": "",
      "updated_at": ""
    }
  ],
  "has_more": true,
  "limit": 20,
  "total": 50,
  "page": 1
}
```

### 3. Get Dataset Details

**GET** `/datasets/{dataset_id}`

Retrieves detailed information about a specific knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Response
```json
{
  "id": "eaedb485-95ac-4ffd-ab1e-18da6d676a2f",
  "name": "Test Knowledge Base",
  "description": "",
  "provider": "vendor",
  "permission": "only_me",
  "data_source_type": null,
  "indexing_technique": null,
  "app_count": 0,
  "document_count": 0,
  "word_count": 0,
  "created_by": "e99a1635-f725-4951-a99a-1daaaa76cfc6",
  "created_at": 1735620612,
  "updated_by": "e99a1635-f725-4951-a99a-1daaaa76cfc6",
  "updated_at": 1735620612,
  "embedding_model": null,
  "embedding_model_provider": null,
  "embedding_available": true,
  "retrieval_model_dict": {
    "search_method": "semantic_search",
    "reranking_enable": false,
    "reranking_mode": null,
    "reranking_model": {
      "reranking_provider_name": "",
      "reranking_model_name": ""
    },
    "weights": null,
    "top_k": 2,
    "score_threshold_enabled": false,
    "score_threshold": null
  },
  "tags": [],
  "doc_form": null,
  "external_knowledge_info": {
    "external_knowledge_id": null,
    "external_knowledge_api_id": null,
    "external_knowledge_api_name": null,
    "external_knowledge_api_endpoint": null
  },
  "external_retrieval_model": {
    "top_k": 2,
    "score_threshold": 0.0,
    "score_threshold_enabled": null
  }
}
```

### 4. Update Dataset Details

**PATCH** `/datasets/{dataset_id}`

Updates knowledge base details.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Request Body
- `name` (string, optional): Knowledge base name
- `indexing_technique` (string, optional): Indexing mode (recommended to provide)
  - `high_quality`: High quality
  - `economy`: Economy
- `permission` (string, optional): Permission level (default: `only_me`)
  - `only_me`: Only me
  - `all_team_members`: All team members
  - `partial_members`: Partial team members
- `embedding_model_provider` (string, optional): Embedding model provider (must be configured in system first, corresponds to provider field)
- `embedding_model` (string, optional): Embedding model
- `retrieval_model` (object, optional): Retrieval parameters (if not provided, uses default recall method)
  - `search_method` (string, required): Search method (one of four keywords)
    - `keyword_search`: Keyword search
    - `semantic_search`: Semantic search
    - `full_text_search`: Full text search
    - `hybrid_search`: Hybrid search
  - `reranking_enable` (boolean, optional): Enable reranking (required if search method is semantic_search or hybrid_search)
  - `reranking_mode` (string, optional): Reranking mode for hybrid search
    - `weighted_score`: Weight setting
    - `reranking_model`: Rerank model
  - `reranking_model` (object, optional): Rerank model configuration (required if reranking is enabled)
    - `reranking_provider_name` (string): Rerank model provider
    - `reranking_model_name` (string): Rerank model name
  - `weights` (float, optional): Semantic search weight for hybrid search mode
  - `top_k` (integer, optional): Number of results to return
  - `score_threshold_enabled` (boolean, optional): Enable score threshold
  - `score_threshold` (float, optional): Score threshold
- `partial_member_list` (array, optional): Partial team member ID list

#### Response
```json
{
  "id": "eaedb485-95ac-4ffd-ab1e-18da6d676a2f",
  "name": "Test Knowledge Base",
  "description": "",
  "provider": "vendor",
  "permission": "only_me",
  "data_source_type": null,
  "indexing_technique": "high_quality",
  "app_count": 0,
  "document_count": 0,
  "word_count": 0,
  "created_by": "e99a1635-f725-4951-a99a-1daaaa76cfc6",
  "created_at": 1735620612,
  "updated_by": "e99a1635-f725-4951-a99a-1daaaa76cfc6",
  "updated_at": 1735622679,
  "embedding_model": "embedding-3",
  "embedding_model_provider": "zhipuai",
  "embedding_available": null,
  "retrieval_model_dict": {
      "search_method": "semantic_search",
      "reranking_enable": false,
      "reranking_mode": null,
      "reranking_model": {
          "reranking_provider_name": "",
          "reranking_model_name": ""
      },
      "weights": null,
      "top_k": 2,
      "score_threshold_enabled": false,
      "score_threshold": null
  },
  "tags": [],
  "doc_form": null,
  "external_knowledge_info": {
      "external_knowledge_id": null,
      "external_knowledge_api_id": null,
      "external_knowledge_api_name": null,
      "external_knowledge_api_endpoint": null
  },
  "external_retrieval_model": {
      "top_k": 2,
      "score_threshold": 0.0,
      "score_threshold_enabled": null
  },
  "partial_member_list": []
}
```

### 5. Delete Dataset

**DELETE** `/datasets/{dataset_id}`

Deletes a knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Response
```
204 No Content
```

### 6. Dataset Retrieval

**POST** `/datasets/{dataset_id}/retrieve`

Performs retrieval search in a knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Request Body
- `query` (string, required): Search query
- `retrieval_model` (object, optional): Retrieval configuration (if not provided, uses default recall method)
  - `search_method` (string, required): Search method (one of four keywords)
    - `keyword_search`: Keyword search
    - `semantic_search`: Semantic search
    - `full_text_search`: Full text search
    - `hybrid_search`: Hybrid search
  - `reranking_enable` (boolean, optional): Enable reranking (required if search method is semantic_search or hybrid_search)
  - `reranking_mode` (string, optional): Reranking mode for hybrid search
    - `weighted_score`: Weight setting
    - `reranking_model`: Rerank model
  - `reranking_model` (object, optional): Rerank model configuration (required if reranking is enabled)
    - `reranking_provider_name` (string): Rerank model provider
    - `reranking_model_name` (string): Rerank model name
  - `weights` (float, optional): Semantic search weight for hybrid search mode
  - `top_k` (integer, optional): Number of results to return
  - `score_threshold_enabled` (boolean, optional): Enable score threshold
  - `score_threshold` (float, optional): Score threshold
  - `metadata_filtering_conditions` (object, optional): Metadata filtering conditions
    - `logical_operator` (string): Logical operator - `and` or `or`
    - `conditions` (array): Filter conditions
      - `name` (string): Metadata field name
      - `comparison_operator` (string): Comparison operator
        - String comparison: `contains`, `not contains`, `start with`, `end with`, `is`, `is not`, `empty`, `not empty`
        - Number comparison: `=`, `≠`, `>`, `<`, `≥`, `≤`
        - Time comparison: `before`, `after`
      - `value` (string|number|null): Comparison value
- `external_retrieval_model` (object, optional): External retrieval model (not enabled)

#### Response
```json
{
  "query": {
    "content": "test"
  },
  "records": [
    {
      "segment": {
        "id": "7fa6f24f-8679-48b3-bc9d-bdf28d73f218",
        "position": 1,
        "document_id": "a8c6c36f-9f5d-4d7a-8472-f5d7b75d71d2",
        "content": "Operation guide",
        "answer": null,
        "word_count": 847,
        "tokens": 280,
        "keywords": [
          "install",
          "java",
          "base",
          "scripts",
          "jdk",
          "manual",
          "internal",
          "opens",
          "add",
          "vmoptions"
        ],
        "index_node_id": "39dd8443-d960-45a8-bb46-7275ad7fbc8e",
        "index_node_hash": "0189157697b3c6a418ccf8264a09699f25858975578f3467c76d6bfc94df1d73",
        "hit_count": 0,
        "enabled": true,
        "disabled_at": null,
        "disabled_by": null,
        "status": "completed",
        "created_by": "dbcb1ab5-90c8-41a7-8b78-73b235eb6f6f",
        "created_at": 1728734540,
        "indexing_at": 1728734552,
        "completed_at": 1728734584,
        "error": null,
        "stopped_at": null,
        "document": {
          "id": "a8c6c36f-9f5d-4d7a-8472-f5d7b75d71d2",
          "data_source_type": "upload_file",
          "name": "readme.txt"
        }
      },
      "score": 3.730463140527718e-05,
      "tsne_position": null
    }
  ]
}
```

## Metadata Management

### 7. Create Metadata

**POST** `/datasets/{dataset_id}/metadata`

Creates new metadata for a knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Request Body
- `type` (string, required): Metadata type
- `name` (string, required): Metadata name

#### Response
```json
{
  "id": "abc",
  "type": "string",
  "name": "test"
}
```

### 8. Update Metadata

**PATCH** `/datasets/{dataset_id}/metadata/{metadata_id}`

Updates metadata configuration.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `metadata_id` (string, required): Metadata ID

#### Request Body
- `name` (string, required): Metadata name

#### Response
```json
{
  "id": "abc",
  "type": "string",
  "name": "test"
}
```

### 9. Delete Metadata

**DELETE** `/datasets/{dataset_id}/metadata/{metadata_id}`

Deletes metadata configuration.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `metadata_id` (string, required): Metadata ID

#### Response
```
204 No Content
```

### 10. Toggle Built-in Metadata

**POST** `/datasets/{dataset_id}/metadata/built-in/{action}`

Enables or disables built-in metadata.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `action` (string, required): Action to perform - `disable` or `enable`

#### Response
```json
{
  "result": "success"
}
```

### 11. Update Document Metadata

**POST** `/datasets/{dataset_id}/documents/metadata`

Updates document metadata values.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Request Body
- `operation_data` (array[object], required): Operation data list
  - `document_id` (string): Document ID
  - `metadata_list` (array): Metadata list
    - `id` (string): Metadata ID
    - `value` (string): Metadata value
    - `name` (string): Metadata name

#### Response
```json
{
  "result": "success"
}
```

### 12. List Dataset Metadata

**GET** `/datasets/{dataset_id}/metadata`

Retrieves metadata configuration list for a knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Response
```json
{
  "doc_metadata": [
    {
      "id": "",
      "name": "name",
      "type": "string",
      "use_count": 0
    }
  ],
  "built_in_field_enabled": true
}
```
## Tag Management

### 13. Create Knowledge Type Tag

**POST** `/datasets/tags`

Creates a new knowledge base type tag.

#### Request Body
- `name` (string, required): Tag name (maximum length: 50)

#### Response
```json
{
  "id": "eddb66c2-04a1-4e3a-8cb2-75abd01e12a6",
  "name": "testtag1",
  "type": "knowledge",
  "binding_count": 0
}
```

### 14. Get Knowledge Type Tags

**GET** `/datasets/tags`

Retrieves knowledge base type tags.

#### Response
```json
[
  {
    "id": "39d6934c-ed36-463d-b4a7-377fa1503dc0",
    "name": "testtag1",
    "type": "knowledge",
    "binding_count": "0"
  }
]
```

### 15. Update Knowledge Type Tag Name

**PATCH** `/datasets/tags`

Updates knowledge base type tag name.

#### Request Body
- `name` (string, required): Updated tag name (maximum length: 50)
- `tag_id` (string, required): Tag ID

#### Response
```json
{
  "id": "eddb66c2-04a1-4e3a-8cb2-75abd01e12a6",
  "name": "tag-renamed",
  "type": "knowledge",
  "binding_count": 0
}
```

### 16. Delete Knowledge Type Tag

**DELETE** `/datasets/tags`

Deletes a knowledge base type tag.

#### Request Body
- `tag_id` (string, required): Tag ID

#### Response
```json
{
  "result": "success"
}
```

### 17. Bind Dataset and Knowledge Type Tags

**POST** `/datasets/tags/binding`

Binds a knowledge base to one or more knowledge type tags.

#### Request Body
- `tag_ids` (list, required): Tag ID list
- `target_id` (string, required): Knowledge base ID

#### Response
```json
{
  "result": "success"
}
```

### 18. Unbind Dataset and Knowledge Type Tag

**POST** `/datasets/tags/unbinding`

Unbinds a knowledge base from a knowledge type tag.

#### Request Body
- `tag_id` (string, required): Tag ID
- `target_id` (string, required): Knowledge base ID

#### Response
```json
{
  "result": "success"
}
```

### 19. Query Knowledge Base Bound Tags

**POST** `/datasets/{dataset_id}/tags`

Retrieves tags bound to a knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Response
```json
{
  "data": [
    {
      "id": "4a601f4f-f8a2-4166-ae7c-58c3b252a524",
      "name": "123"
    }
  ],
  "total": 3
}
```