# Document Management APIs

This document covers all document management APIs including creation, updating, listing, and status management operations.

## Authentication

All Service API requests use `API-Key` for authentication. Include your `API-Key` in the **`Authorization`** HTTP Header:

```
Authorization: Bearer {API_KEY}
```

## APIs

### 1. Create Document by Text

**POST** `/datasets/{dataset_id}/document/create-by-text`

Creates a new document in an existing knowledge base using text content.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Request Body
- `name` (string): Document name
- `text` (string): Document content
- `indexing_technique` (string): Indexing method
  - `high_quality`: High quality using Embedding model for vector database indexing
  - `economy`: Economy using keyword table index for inverted indexing
- `doc_form` (string, optional): Index content form
  - `text_model`: Direct text embedding (default for economy mode)
  - `hierarchical_model`: Parent-child mode
  - `qa_model`: Q&A mode - generates Q&A pairs for document segments
- `doc_language` (string, optional): Document language for Q&A mode (e.g., "English", "Chinese")
- `process_rule` (object, required): Processing rules
  - `mode` (string): Processing mode - `automatic`, `custom`, or `hierarchical`
  - `rules` (object): Custom rules (empty for automatic mode)
    - `pre_processing_rules` (array): Preprocessing rules
      - `id` (string): Rule identifier (`remove_extra_spaces`, `remove_urls_emails`)
      - `enabled` (boolean): Whether rule is enabled
    - `segmentation` (object): Segmentation rules
      - `separator` (string): Custom separator (default: `\n`)
      - `max_tokens` (integer): Maximum length in tokens (default: 1000)
    - `parent_mode` (string): Parent segment recall mode - `full-doc` or `paragraph`
    - `subchunk_segmentation` (object): Sub-segment rules
      - `separator` (string): Separator (default: `***`)
      - `max_tokens` (integer): Maximum length (must be less than parent)
      - `chunk_overlap` (integer, optional): Overlap between segments

#### First-time Upload Parameters (when knowledge base has no parameters set)
- `retrieval_model` (object, optional): Retrieval mode configuration
  - `search_method` (string): Search method - `hybrid_search`, `semantic_search`, `full_text_search`
  - `reranking_enable` (boolean): Enable reranking
  - `reranking_model` (object): Rerank model configuration
    - `reranking_provider_name` (string): Rerank model provider
    - `reranking_model_name` (string): Rerank model name
  - `top_k` (integer): Number of results to return
  - `score_threshold_enabled` (boolean): Enable score threshold
  - `score_threshold` (float): Score threshold value
- `embedding_model` (string, optional): Embedding model name
- `embedding_model_provider` (string, optional): Embedding model provider

#### Response
```json
{
  "document": {
    "id": "",
    "position": 1,
    "data_source_type": "upload_file",
    "data_source_info": {
        "upload_file_id": ""
    },
    "dataset_process_rule_id": "",
    "name": "text.txt",
    "created_from": "api",
    "created_by": "",
    "created_at": 1695690280,
    "tokens": 0,
    "indexing_status": "waiting",
    "error": null,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "archived": false,
    "display_status": "queuing",
    "word_count": 0,
    "hit_count": 0,
    "doc_form": "text_model"
  },
  "batch": ""
}
```

### 2. Create Document by File

**POST** `/datasets/{dataset_id}/document/create-by-file`

Creates a new document in an existing knowledge base using file upload.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Request Body (multipart/form-data)
- `data` (multipart/form-data json string): Configuration data
  - `original_document_id` (string, optional): Source document ID for updates
    - Used for re-uploading documents or modifying document cleaning/segmentation configuration
    - Missing information is copied from source document
    - Source document cannot be archived
    - When `original_document_id` is provided, represents document update operation, `process_rule` is optional
    - When `original_document_id` is not provided, represents document creation operation, `process_rule` is required
  - `indexing_technique` (string): Indexing method
    - `high_quality`: High quality using embedding model for vector database indexing
    - `economy`: Economy using keyword table index for inverted indexing
  - `doc_form` (string, optional): Index content form
    - `text_model`: Direct text embedding (default for economy mode)
    - `hierarchical_model`: Parent-child mode
    - `qa_model`: Q&A mode - generates Q&A pairs for document segments
  - `doc_language` (string, optional): Document language for Q&A mode (e.g., "English", "Chinese")
  - `process_rule` (object): Processing rules
    - `mode` (string): Processing mode - `automatic`, `custom`, or `hierarchical`
    - `rules` (object): Custom rules (empty for automatic mode)
      - `pre_processing_rules` (array): Preprocessing rules
        - `id` (string): Rule identifier (`remove_extra_spaces`, `remove_urls_emails`)
        - `enabled` (boolean): Whether rule is enabled
      - `segmentation` (object): Segmentation rules
        - `separator` (string): Custom separator (default: `\n`)
        - `max_tokens` (integer): Maximum length in tokens (default: 1000)
      - `parent_mode` (string): Parent segment recall mode - `full-doc` or `paragraph`
      - `subchunk_segmentation` (object): Sub-segment rules
        - `separator` (string): Separator (default: `***`)
        - `max_tokens` (integer): Maximum length (must be less than parent)
        - `chunk_overlap` (integer, optional): Overlap between segments
- `file` (multipart/form-data, required): File to upload

#### First-time Upload Parameters (when knowledge base has no parameters set)
- `retrieval_model` (object, optional): Retrieval mode configuration
  - `search_method` (string): Search method - `hybrid_search`, `semantic_search`, `full_text_search`
  - `reranking_enable` (boolean): Enable reranking
  - `reranking_model` (object): Rerank model configuration
    - `reranking_provider_name` (string): Rerank model provider
    - `reranking_model_name` (string): Rerank model name
  - `top_k` (integer): Number of results to return
  - `score_threshold_enabled` (boolean): Enable score threshold
  - `score_threshold` (float): Score threshold value
- `embedding_model` (string, optional): Embedding model name
- `embedding_model_provider` (string, optional): Embedding model provider

#### Response
```json
{
  "document": {
    "id": "",
    "position": 1,
    "data_source_type": "upload_file",
    "data_source_info": {
      "upload_file_id": ""
    },
    "dataset_process_rule_id": "",
    "name": "Dify.txt",
    "created_from": "api",
    "created_by": "",
    "created_at": 1695308667,
    "tokens": 0,
    "indexing_status": "waiting",
    "error": null,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "archived": false,
    "display_status": "queuing",
    "word_count": 0,
    "hit_count": 0,
    "doc_form": "text_model"
  },
  "batch": ""
}
```

### 3. Update Document by Text

**POST** `/datasets/{dataset_id}/documents/{document_id}/update-by-text`

Updates a document using text content based on an existing knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID

#### Request Body
- `name` (string, optional): Document name
- `text` (string, optional): Document content
- `process_rule` (object, optional): Processing rules
  - `mode` (string): Processing mode - `automatic`, `custom`, or `hierarchical`
  - `rules` (object): Custom rules (empty for automatic mode)
    - `pre_processing_rules` (array): Preprocessing rules
      - `id` (string): Rule identifier (`remove_extra_spaces`, `remove_urls_emails`)
      - `enabled` (boolean): Whether rule is enabled
    - `segmentation` (object): Segmentation rules
      - `separator` (string): Custom separator (default: `\n`)
      - `max_tokens` (integer): Maximum length in tokens (default: 1000)
    - `parent_mode` (string): Parent segment recall mode - `full-doc` or `paragraph`
    - `subchunk_segmentation` (object): Sub-segment rules
      - `separator` (string): Separator (default: `***`)
      - `max_tokens` (integer): Maximum length (must be less than parent)
      - `chunk_overlap` (integer, optional): Overlap between segments

#### Response
```json
{
  "document": {
    "id": "",
    "position": 1,
    "data_source_type": "upload_file",
    "data_source_info": {
      "upload_file_id": ""
    },
    "dataset_process_rule_id": "",
    "name": "name.txt",
    "created_from": "api",
    "created_by": "",
    "created_at": 1695308667,
    "tokens": 0,
    "indexing_status": "waiting",
    "error": null,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "archived": false,
    "display_status": "queuing",
    "word_count": 0,
    "hit_count": 0,
    "doc_form": "text_model"
  },
  "batch": ""
}
```

### 4. Update Document by File

**POST** `/datasets/{dataset_id}/documents/{document_id}/update-by-file`

Updates a document using file upload based on an existing knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID

#### Request Body (multipart/form-data)
- `name` (string, optional): Document name
- `file` (multipart/form-data, required): File to upload
- `process_rule` (object, optional): Processing rules
  - `mode` (string): Processing mode - `automatic`, `custom`, or `hierarchical`
  - `rules` (object): Custom rules (empty for automatic mode)
    - `pre_processing_rules` (array): Preprocessing rules
      - `id` (string): Rule identifier (`remove_extra_spaces`, `remove_urls_emails`)
      - `enabled` (boolean): Whether rule is enabled
    - `segmentation` (object): Segmentation rules
      - `separator` (string): Custom separator (default: `\n`)
      - `max_tokens` (integer): Maximum length in tokens (default: 1000)
    - `parent_mode` (string): Parent segment recall mode - `full-doc` or `paragraph`
    - `subchunk_segmentation` (object): Sub-segment rules
      - `separator` (string): Separator (default: `***`)
      - `max_tokens` (integer): Maximum length (must be less than parent)
      - `chunk_overlap` (integer, optional): Overlap between segments

#### Response
```json
{
  "document": {
    "id": "",
    "position": 1,
    "data_source_type": "upload_file",
    "data_source_info": {
      "upload_file_id": ""
    },
    "dataset_process_rule_id": "",
    "name": "Dify.txt",
    "created_from": "api",
    "created_by": "",
    "created_at": 1695308667,
    "tokens": 0,
    "indexing_status": "waiting",
    "error": null,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "archived": false,
    "display_status": "queuing",
    "word_count": 0,
    "hit_count": 0,
    "doc_form": "text_model"
  },
  "batch": "20230921150427533684"
}
```

### 5. Get Document Indexing Status

**GET** `/datasets/{dataset_id}/documents/{batch}/indexing-status`

Retrieves document embedding status and progress.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `batch` (string, required): Document upload batch number

#### Response
```json
{
  "data": [{
    "id": "",
    "indexing_status": "indexing",
    "processing_started_at": 1681623462.0,
    "parsing_completed_at": 1681623462.0,
    "cleaning_completed_at": 1681623462.0,
    "splitting_completed_at": 1681623462.0,
    "completed_at": null,
    "paused_at": null,
    "error": null,
    "stopped_at": null,
    "completed_segments": 24,
    "total_segments": 100
  }]
}
```

### 6. Delete Document

**DELETE** `/datasets/{dataset_id}/documents/{document_id}`

Deletes a document.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID

#### Response
```
204 No Content
```

### 7. List Documents

**GET** `/datasets/{dataset_id}/documents`

Retrieves a list of documents in a knowledge base.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID

#### Query Parameters
- `keyword` (string, optional): Search keyword (currently only searches document names)
- `page` (string, optional): Page number
- `limit` (string, optional): Number of results (default: 20, range: 1-100)

#### Response
```json
{
  "data": [
    {
      "id": "",
      "position": 1,
      "data_source_type": "file_upload",
      "data_source_info": null,
      "dataset_process_rule_id": null,
      "name": "dify",
      "created_from": "",
      "created_by": "",
      "created_at": 1681623639,
      "tokens": 0,
      "indexing_status": "waiting",
      "error": null,
      "enabled": true,
      "disabled_at": null,
      "disabled_by": null,
      "archived": false
    }
  ],
  "has_more": false,
  "limit": 20,
  "total": 9,
  "page": 1
}
```

### 8. Get Document Details

**GET** `/datasets/{dataset_id}/documents/{document_id}`

Retrieves detailed information about a specific document.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID

#### Query Parameters
- `metadata` (string, optional): Metadata filter - `all`, `only`, or `without` (default: `all`)

#### Response
```json
{
  "id": "f46ae30c-5c11-471b-96d0-464f5f32a7b2",
  "position": 1,
  "data_source_type": "upload_file",
  "data_source_info": {
    "upload_file": {}
  },
  "dataset_process_rule_id": "24b99906-845e-499f-9e3c-d5565dd6962c",
  "dataset_process_rule": {
    "mode": "hierarchical",
    "rules": {
      "pre_processing_rules": [
        {
          "id": "remove_extra_spaces",
          "enabled": true
        },
        {
          "id": "remove_urls_emails",
          "enabled": false
        }
      ],
      "segmentation": {
        "separator": "**********page_ending**********",
        "max_tokens": 1024,
        "chunk_overlap": 0
      },
      "parent_mode": "paragraph",
      "subchunk_segmentation": {
        "separator": "\n",
        "max_tokens": 512,
        "chunk_overlap": 0
      }
    }
  },
  "document_process_rule": {
    "id": "24b99906-845e-499f-9e3c-d5565dd6962c",
    "dataset_id": "48a0db76-d1a9-46c1-ae35-2baaa919a8a9",
    "mode": "hierarchical",
    "rules": {
      "pre_processing_rules": [
        {
          "id": "remove_extra_spaces",
          "enabled": true
        },
        {
          "id": "remove_urls_emails",
          "enabled": false
        }
      ],
      "segmentation": {
        "separator": "**********page_ending**********",
        "max_tokens": 1024,
        "chunk_overlap": 0
      },
      "parent_mode": "paragraph",
      "subchunk_segmentation": {
        "separator": "\n",
        "max_tokens": 512,
        "chunk_overlap": 0
      }
    }
  },
  "name": "xxxx",
  "created_from": "web",
  "created_by": "17f71940-a7b5-4c77-b60f-2bd645c1ffa0",
  "created_at": 1750464191,
  "tokens": null,
  "indexing_status": "waiting",
  "completed_at": null,
  "updated_at": 1750464191,
  "indexing_latency": null,
  "error": null,
  "enabled": true,
  "disabled_at": null,
  "disabled_by": null,
  "archived": false,
  "segment_count": 0,
  "average_segment_length": 0,
  "hit_count": null,
  "display_status": "queuing",
  "doc_form": "hierarchical_model",
  "doc_language": "Chinese Simplified"
}
```

### 9. Update Document Status

**PATCH** `/datasets/{dataset_id}/documents/status/{action}`

Updates the status of multiple documents.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `action` (string, required): Action to perform
  - `enable`: Enable documents
  - `disable`: Disable documents
  - `archive`: Archive documents
  - `un_archive`: Unarchive documents

#### Request Body
- `document_ids` (array[string], required): List of document IDs

#### Response
```json
{
  "result": "success"
}
```

### 10. Get Upload File

**GET** `/datasets/{dataset_id}/documents/{document_id}/upload-file`

Retrieves information about the uploaded file associated with a document.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID

#### Response
```json
{
  "id": "file_id",
  "name": "file_name",
  "size": 1024,
  "extension": "txt",
  "url": "preview_url",
  "download_url": "download_url",
  "mime_type": "text/plain",
  "created_by": "user_id",
  "created_at": 1728734540
}
```

