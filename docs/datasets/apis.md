# Dify Knowledge Base API Documentation

This document has been split into separate module-specific files for better organization. Please refer to the following files for detailed API documentation:

## API Modules

### [Dataset Management APIs](./dataset-api.md)
- Create Empty Dataset
- List Datasets
- Get Dataset Details
- Update Dataset Details
- Delete Dataset
- Dataset Retrieval
- Create Metadata
- Update Metadata
- Delete Metadata
- Toggle Built-in Metadata
- Update Document Metadata
- List Dataset Metadata
- Create Knowledge Type Tag
- Get Knowledge Type Tags
- Update Knowledge Type Tag Name
- Delete Knowledge Type Tag
- Bind Dataset and Knowledge Type Tags
- Unbind Dataset and Knowledge Type Tag
- Query Knowledge Base Bound Tags

### [Document Management APIs](./document-api.md)
- Create Document by Text
- Create Document by File
- Update Document by Text
- Update Document by File
- Get Document Indexing Status
- Delete Document
- List Documents
- Get Document Details
- Update Document Status
- Get Upload File

### [Segment Management APIs](./segment-api.md)
- Create Segments
- List Document Segments
- Delete Segment
- Get Segment Details
- Update Segment
- Create Child Chunks
- List Child Chunks
- Delete Child Chunk
- Update Child Chunk

### [System Configuration APIs](./system-api.md)
- Get Embedding Model List

## Authentication

All Service API requests use `API-Key` for authentication. Include your `API-Key` in the **`Authorization`** HTTP Header:

```
Authorization: Bearer {API_KEY}
```

## Summary

The Dify Knowledge Base system provides comprehensive APIs organized into 4 modules with a total of **39 APIs**:

- **Dataset Management**: 19 APIs for creating, listing, viewing, updating, deleting, searching knowledge bases, managing metadata, and tag operations
- **Document Management**: 10 APIs for document operations including creation, updates, status management, and file retrieval
- **Segment Management**: 9 APIs for managing document segments and hierarchical child chunks
- **System Configuration**: 1 API for embedding model information

Each module file includes complete parameter specifications, request/response examples, and detailed field descriptions to facilitate integration and development.
