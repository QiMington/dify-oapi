# Segment Management APIs

This document covers all document segment management APIs including creation, listing, updating, and deletion operations.

## Authentication

All Service API requests use `API-Key` for authentication. Include your `API-Key` in the **`Authorization`** HTTP Header:

```
Authorization: Bearer {API_KEY}
```

## APIs

### 1. Create Segments

**POST** `/datasets/{dataset_id}/documents/{document_id}/segments`

Creates new segments in a document.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID

#### Request Body
- `segments` (array[object], required): List of segments to create
  - `content` (string, required): Text content/question content
  - `answer` (string, optional): Answer content (required if knowledge base is in Q&A mode)
  - `keywords` (array[string], optional): Keywords

#### Response
```json
{
  "data": [{
    "id": "",
    "position": 1,
    "document_id": "",
    "content": "1",
    "answer": "1",
    "word_count": 25,
    "tokens": 0,
    "keywords": ["a"],
    "index_node_id": "",
    "index_node_hash": "",
    "hit_count": 0,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }],
  "doc_form": "text_model"
}
```

### 2. List Document Segments

**GET** `/datasets/{dataset_id}/documents/{document_id}/segments`

Retrieves segments from a document.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID

#### Query Parameters
- `keyword` (string, optional): Search keyword
- `status` (string, optional): Search status (`completed`)
- `page` (string, optional): Page number
- `limit` (string, optional): Number of results (default: 20, range: 1-100)

#### Response
```json
{
  "data": [{
    "id": "",
    "position": 1,
    "document_id": "",
    "content": "1",
    "answer": "1",
    "word_count": 25,
    "tokens": 0,
    "keywords": ["a"],
    "index_node_id": "",
    "index_node_hash": "",
    "hit_count": 0,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }],
  "doc_form": "text_model",
  "has_more": false,
  "limit": 20,
  "total": 9,
  "page": 1
}
```

### 3. Delete Segment

**DELETE** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}`

Deletes a document segment.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID
- `segment_id` (string, required): Document segment ID

#### Response
```
204 No Content
```

### 4. Get Segment Details

**GET** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}`

Retrieves detailed information about a specific document segment.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID
- `segment_id` (string, required): Segment ID

#### Response
```json
{
  "data": {
    "id": "分段唯一ID",
    "position": 2,
    "document_id": "所属文档ID",
    "content": "分段内容文本",
    "sign_content": "签名内容文本",
    "answer": "答案内容(如果有)",
    "word_count": 470,
    "tokens": 382,
    "keywords": ["关键词1", "关键词2"],
    "index_node_id": "索引节点ID",
    "index_node_hash": "索引节点哈希值",
    "hit_count": 0,
    "enabled": true,
    "status": "completed",
    "created_by": "创建者ID",
    "created_at": "创建时间戳",
    "updated_at": "更新时间戳",
    "indexing_at": "索引时间戳",
    "completed_at": "完成时间戳",
    "error": null,
    "child_chunks": []
  },
  "doc_form": "text_model"
}
```

### 5. Update Segment

**POST** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}`

Updates a document segment.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID
- `segment_id` (string, required): Document segment ID

#### Request Body
- `segment` (object, required): Segment update data
  - `content` (string, required): Text content/question content
  - `answer` (string, optional): Answer content (required if knowledge base is in Q&A mode)
  - `keywords` (array[string], optional): Keywords
  - `enabled` (boolean, optional): Enable/disable segment
  - `regenerate_child_chunks` (boolean, optional): Whether to regenerate child chunks

#### Response
```json
{
  "data": {
    "id": "",
    "position": 1,
    "document_id": "",
    "content": "1",
    "answer": "1",
    "word_count": 25,
    "tokens": 0,
    "keywords": ["a"],
    "index_node_id": "",
    "index_node_hash": "",
    "hit_count": 0,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  },
  "doc_form": "text_model"
}
```

## Child Chunk Management

### 6. Create Child Chunks

**POST** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks`

Creates new child chunks for a document segment.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID
- `segment_id` (string, required): Segment ID

#### Request Body
- `content` (string, required): Child chunk content

#### Response
```json
{
  "data": {
    "id": "",
    "segment_id": "",
    "content": "子分段内容",
    "word_count": 25,
    "tokens": 0,
    "index_node_id": "",
    "index_node_hash": "",
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }
}
```

### 7. List Child Chunks

**GET** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks`

Retrieves child chunks from a document segment.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID
- `segment_id` (string, required): Document segment ID

#### Query Parameters
- `keyword` (string, optional): Search keyword
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Number of results per page (default: 20, max: 100)

#### Response
```json
{
  "data": [{
    "id": "",
    "segment_id": "",
    "content": "子分段内容",
    "word_count": 25,
    "tokens": 0,
    "index_node_id": "",
    "index_node_hash": "",
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }],
  "total": 1,
  "total_pages": 1,
  "page": 1,
  "limit": 20
}
```

### 8. Delete Child Chunk

**DELETE** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks/{child_chunk_id}`

Deletes a child chunk.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID
- `segment_id` (string, required): Document segment ID
- `child_chunk_id` (string, required): Child chunk ID

#### Response
```
204 No Content
```

### 9. Update Child Chunk

**PATCH** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks/{child_chunk_id}`

Updates a child chunk.

#### Path Parameters
- `dataset_id` (string, required): Knowledge base ID
- `document_id` (string, required): Document ID
- `segment_id` (string, required): Document segment ID
- `child_chunk_id` (string, required): Child chunk ID

#### Request Body
- `content` (string, required): Child chunk content

#### Response
```json
{
  "data": {
    "id": "",
    "segment_id": "",
    "content": "更新的子分段内容",
    "word_count": 25,
    "tokens": 0,
    "index_node_id": "",
    "index_node_hash": "",
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }
}
```

