# Dataset API Design Document

## Overview

This document outlines the design for implementing comprehensive dataset management functionality in the dify-oapi knowledge_base module. The implementation will support 19 dataset-related APIs covering dataset CRUD operations, metadata management, tag management, and retrieval functionality.

## Design Decisions

### 1. Module Organization
**Decision**: Extend existing `knowledge_base/v1/` module structure
- Continue using the established version-based API organization
- Maintain consistency with existing chat, completion, and workflow modules
- Leverage existing infrastructure and patterns

### 2. Resource Structure
**Decision**: Create new resource classes within knowledge_base module

**New Resource Classes**:
- `metadata` - Dataset metadata management (7 APIs)
- `tag` - Knowledge base type tag management (7 APIs)

**Extended Existing Resources**:
- `dataset` - Add get, update, retrieve methods (3 new APIs)

### 3. Response Model Strategy
**Decision**: Create dedicated Response models for every API
- Maintain type safety and consistency across all endpoints
- Include specific response models even for simple `{"result": "success"}` responses
- Ensure comprehensive IDE support and validation

### 4. Nested Object Handling
**Decision**: Define all nested objects as independent model class files
- Create separate model files regardless of complexity
- Place shared nested objects in `common/` directory for reuse
- Ensure maintainability and cross-model compatibility

**Shared Common Models**:
- `retrieval_model.py` - Used across dataset and document APIs
- `reranking_model.py` - Nested within retrieval_model
- `external_knowledge_info.py` - Dataset external knowledge configuration
- `metadata_filtering_conditions.py` - Search filtering configuration

### 5. Method Naming Convention
**Decision**: Use descriptive method names for clarity
- Core CRUD: `create`, `list`, `get`, `update`, `delete`
- Special operations: `retrieve`, `bind_tags`, `unbind_tags`
- Maintain intuitive and self-documenting API interface

### 6. Backward Compatibility
**Decision**: Complete rewrite without backward compatibility
- Align all implementations with latest API specifications
- Ensure functional completeness and consistency
- Prioritize correctness over migration convenience

### 7. Model File Organization
**Decision**: Organize models by resource grouping with shared common models

```
model/
├── dataset/          # Dataset-specific models
│   ├── create_request.py
│   ├── create_response.py
│   ├── list_request.py
│   ├── list_response.py
│   ├── get_request.py
│   ├── get_response.py
│   ├── update_request.py
│   ├── update_response.py
│   ├── delete_request.py
│   ├── delete_response.py
│   ├── retrieve_request.py
│   └── retrieve_response.py
├── metadata/         # Metadata management models
│   ├── create_request.py
│   ├── create_response.py
│   ├── list_request.py
│   ├── list_response.py
│   ├── update_request.py
│   ├── update_response.py
│   ├── delete_request.py
│   ├── delete_response.py
│   ├── toggle_builtin_request.py
│   ├── toggle_builtin_response.py
│   ├── update_document_request.py
│   └── update_document_response.py
├── tag/             # Tag management models
│   ├── create_request.py
│   ├── create_response.py
│   ├── list_request.py
│   ├── list_response.py
│   ├── update_request.py
│   ├── update_response.py
│   ├── delete_request.py
│   ├── delete_response.py
│   ├── bind_request.py
│   ├── bind_response.py
│   ├── unbind_request.py
│   ├── unbind_response.py
│   ├── query_bound_request.py
│   └── query_bound_response.py
└── common/          # Shared models
    ├── retrieval_model.py
    ├── reranking_model.py
    ├── external_knowledge_info.py
    ├── metadata_filtering_conditions.py
    ├── dataset_info.py
    ├── tag_info.py
    └── metadata_info.py
```

## API Implementation Plan

### Dataset Management APIs (6 APIs)

#### Core CRUD Operations
1. **POST /datasets** → `dataset.create()`
2. **GET /datasets** → `dataset.list()`
3. **GET /datasets/{dataset_id}** → `dataset.get()`
4. **PATCH /datasets/{dataset_id}** → `dataset.update()`
5. **DELETE /datasets/{dataset_id}** → `dataset.delete()`

#### Retrieval Operations
6. **POST /datasets/{dataset_id}/retrieve** → `dataset.retrieve()`

### Metadata Management APIs (7 APIs)

#### Metadata CRUD
1. **POST /datasets/{dataset_id}/metadata** → `metadata.create()`
2. **GET /datasets/{dataset_id}/metadata** → `metadata.list()`
3. **PATCH /datasets/{dataset_id}/metadata/{metadata_id}** → `metadata.update()`
4. **DELETE /datasets/{dataset_id}/metadata/{metadata_id}** → `metadata.delete()`

#### Built-in Metadata Management
5. **POST /datasets/{dataset_id}/metadata/built-in/{action}** → `metadata.toggle_builtin()`

#### Document Metadata Operations
6. **POST /datasets/{dataset_id}/documents/metadata** → `metadata.update_document()`

### Tag Management APIs (7 APIs)

#### Tag CRUD (Global Operations)
1. **POST /datasets/tags** → `tag.create()`
2. **GET /datasets/tags** → `tag.list()`
3. **PATCH /datasets/tags** → `tag.update()`
4. **DELETE /datasets/tags** → `tag.delete()`

#### Tag Binding Operations
5. **POST /datasets/tags/binding** → `tag.bind_tags()`
6. **POST /datasets/tags/unbinding** → `tag.unbind_tags()`

#### Tag Query Operations
7. **POST /datasets/{dataset_id}/tags** → `tag.query_bound()`

## Technical Implementation Details

### Resource Class Structure
```python
# Example: metadata resource
class Metadata:
    def __init__(self, transport: Transport):
        self._transport = transport
    
    def create(self, request: MetadataCreateRequest, request_option: RequestOption) -> MetadataCreateResponse:
        # Implementation
    
    async def acreate(self, request: MetadataCreateRequest, request_option: RequestOption) -> MetadataCreateResponse:
        # Async implementation
```

### Model Class Pattern
```python
# Example: shared common model
@dataclass
class RetrievalModel:
    search_method: str
    reranking_enable: Optional[bool] = None
    reranking_model: Optional[RerankingModel] = None
    top_k: Optional[int] = None
    score_threshold_enabled: Optional[bool] = None
    score_threshold: Optional[float] = None
    
    @classmethod
    def builder(cls) -> "RetrievalModelBuilder":
        return RetrievalModelBuilder()
```

### Version Integration
Update `v1/version.py` to include new resources:
```python
class V1:
    def __init__(self, transport: Transport):
        self.dataset = Dataset(transport)
        self.document = Document(transport)
        self.segment = Segment(transport)
        self.metadata = Metadata(transport)  # New
        self.tag = Tag(transport)            # New
```

## Quality Assurance

### Type Safety
- Comprehensive type hints for all models and methods
- Pydantic validation for request/response models
- Builder pattern support for all request models

### Error Handling
- Consistent error response handling across all APIs
- Proper HTTP status code mapping
- Detailed error message propagation

### Testing Strategy
- Unit tests for all resource methods
- Integration tests with mock API responses
- Validation tests for all model classes

## Migration Impact

### Breaking Changes
- Complete rewrite of existing dataset-related functionality
- New model structure requires import path updates
- Method signature changes for existing APIs

### Benefits
- Full API coverage with 19 dataset management endpoints
- Improved type safety and developer experience
- Consistent architecture across all knowledge base features
- Enhanced maintainability and extensibility

## Summary

This design provides a comprehensive solution for dataset management in dify-oapi, covering all 19 dataset-related APIs with a clean, maintainable architecture. The implementation prioritizes type safety, consistency, and developer experience while ensuring full compatibility with the latest Dify API specifications.

The modular resource-based organization, combined with shared common models and descriptive method naming, creates an intuitive and powerful interface for dataset management operations including CRUD operations, metadata management, tag management, and advanced retrieval functionality.