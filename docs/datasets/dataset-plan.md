# Dataset API Implementation Plan

This document provides step-by-step prompts for implementing the complete dataset management functionality in the dify-oapi knowledge_base module. Each step includes implementation and testing phases to ensure code quality.

## Overview

The implementation covers 19 dataset-related APIs organized into three main resource groups:
- **Dataset Management**: 6 APIs (CRUD + retrieval)
- **Metadata Management**: 7 APIs (CRUD + built-in + document operations)
- **Tag Management**: 7 APIs (CRUD + binding operations)

## Implementation Steps

### Phase 1: Common Models Foundation

#### Step 1: Create Shared Common Models
**Prompt:**
```
Create the shared common models for the dataset API implementation in `dify_oapi/api/knowledge_base/v1/model/common/`. 

Implement the following model files with proper type hints, builder patterns, and Pydantic validation:

1. `retrieval_model.py` - RetrievalModel class with fields:
   - search_method: str (required)
   - reranking_enable: Optional[bool]
   - reranking_mode: Optional[str]
   - reranking_model: Optional[RerankingModel]
   - weights: Optional[float]
   - top_k: Optional[int]
   - score_threshold_enabled: Optional[bool]
   - score_threshold: Optional[float]
   - metadata_filtering_conditions: Optional[MetadataFilteringConditions]

2. `reranking_model.py` - RerankingModel class with fields:
   - reranking_provider_name: str
   - reranking_model_name: str

3. `external_knowledge_info.py` - ExternalKnowledgeInfo class with fields:
   - external_knowledge_id: Optional[str]
   - external_knowledge_api_id: Optional[str]
   - external_knowledge_api_name: Optional[str]
   - external_knowledge_api_endpoint: Optional[str]

4. `metadata_filtering_conditions.py` - MetadataFilteringConditions class with fields:
   - logical_operator: str
   - conditions: List[FilterCondition]

5. `filter_condition.py` - FilterCondition class with fields:
   - name: str
   - comparison_operator: str
   - value: Optional[Union[str, int, float]]

6. `dataset_info.py` - DatasetInfo class with comprehensive dataset fields
7. `tag_info.py` - TagInfo class for tag information
8. `metadata_info.py` - MetadataInfo class for metadata information

Follow the existing project patterns and ensure all models have builder methods and proper serialization support.
```

#### Step 2: Test Common Models
**Prompt:**
```
Create comprehensive unit tests for all common models created in Step 1. 

Create test file `tests/test_knowledge_base_common_models.py` that covers:

1. Model instantiation and validation
2. Builder pattern functionality
3. Serialization/deserialization
4. Edge cases and validation errors
5. Optional field handling
6. Nested model relationships

Ensure all tests pass and provide good coverage for the common model functionality.
```

### Phase 2: Dataset Management APIs (6 APIs)

#### Step 3: Dataset Request/Response Models
**Prompt:**
```
Create all request and response models for dataset management APIs in `dify_oapi/api/knowledge_base/v1/model/dataset/`.

Implement the following model files:

1. `create_request.py` - DatasetCreateRequest with fields:
   - name: str (required)
   - description: Optional[str]
   - indexing_technique: Optional[str]
   - permission: Optional[str]
   - provider: Optional[str]
   - external_knowledge_api_id: Optional[str]
   - external_knowledge_id: Optional[str]
   - embedding_model: Optional[str]
   - embedding_model_provider: Optional[str]
   - retrieval_model: Optional[RetrievalModel]

2. `create_response.py` - DatasetCreateResponse using DatasetInfo
3. `list_request.py` - DatasetListRequest with pagination and filtering
4. `list_response.py` - DatasetListResponse with data array and pagination
5. `get_request.py` - DatasetGetRequest with dataset_id
6. `get_response.py` - DatasetGetResponse with full dataset details
7. `update_request.py` - DatasetUpdateRequest with partial update fields
8. `update_response.py` - DatasetUpdateResponse using DatasetInfo
9. `delete_request.py` - DatasetDeleteRequest with dataset_id
10. `delete_response.py` - DatasetDeleteResponse (empty for 204 response)
11. `retrieve_request.py` - DatasetRetrieveRequest with query and retrieval config
12. `retrieve_response.py` - DatasetRetrieveResponse with query and records

Use the common models created in Step 1 and follow existing project patterns for builder methods and validation.
```

#### Step 4: Test Dataset Models
**Prompt:**
```
Create comprehensive unit tests for dataset request/response models in `tests/test_dataset_models.py`.

Test all models created in Step 3, covering:
1. Model validation and required fields
2. Builder pattern functionality
3. Serialization/deserialization
4. Integration with common models
5. Edge cases and error handling

Ensure all tests pass with good coverage.
```

#### Step 5: Dataset Resource Implementation
**Prompt:**
```
Implement the Dataset resource class in `dify_oapi/api/knowledge_base/v1/resource/dataset.py`.

Create a Dataset class with the following methods:
1. `create(request: DatasetCreateRequest, request_option: RequestOption) -> DatasetCreateResponse`
2. `acreate(request: DatasetCreateRequest, request_option: RequestOption) -> DatasetCreateResponse`
3. `list(request: DatasetListRequest, request_option: RequestOption) -> DatasetListResponse`
4. `alist(request: DatasetListRequest, request_option: RequestOption) -> DatasetListResponse`
5. `get(request: DatasetGetRequest, request_option: RequestOption) -> DatasetGetResponse`
6. `aget(request: DatasetGetRequest, request_option: RequestOption) -> DatasetGetResponse`
7. `update(request: DatasetUpdateRequest, request_option: RequestOption) -> DatasetUpdateResponse`
8. `aupdate(request: DatasetUpdateRequest, request_option: RequestOption) -> DatasetUpdateResponse`
9. `delete(request: DatasetDeleteRequest, request_option: RequestOption) -> DatasetDeleteResponse`
10. `adelete(request: DatasetDeleteRequest, request_option: RequestOption) -> DatasetDeleteResponse`
11. `retrieve(request: DatasetRetrieveRequest, request_option: RequestOption) -> DatasetRetrieveResponse`
12. `aretrieve(request: DatasetRetrieveRequest, request_option: RequestOption) -> DatasetRetrieveResponse`

Follow the existing transport patterns and HTTP method mappings. Ensure proper error handling and response parsing.
```

#### Step 6: Test Dataset Resource
**Prompt:**
```
Create comprehensive integration tests for the Dataset resource in `tests/test_dataset_resource.py`.

Test all methods implemented in Step 5, including:
1. HTTP method and URL mapping verification
2. Request serialization and response deserialization
3. Error handling for various HTTP status codes
4. Both sync and async method variants
5. Mock API responses based on the API documentation

Use pytest fixtures and mock responses to simulate API interactions. Ensure all tests pass.
```

### Phase 3: Metadata Management APIs (7 APIs)

#### Step 7: Metadata Request/Response Models
**Prompt:**
```
Create all request and response models for metadata management APIs in `dify_oapi/api/knowledge_base/v1/model/metadata/`.

Implement the following model files:

1. `create_request.py` - MetadataCreateRequest with dataset_id, type, name
2. `create_response.py` - MetadataCreateResponse using MetadataInfo
3. `list_request.py` - MetadataListRequest with dataset_id
4. `list_response.py` - MetadataListResponse with doc_metadata array and built_in_field_enabled
5. `update_request.py` - MetadataUpdateRequest with dataset_id, metadata_id, name
6. `update_response.py` - MetadataUpdateResponse using MetadataInfo
7. `delete_request.py` - MetadataDeleteRequest with dataset_id, metadata_id
8. `delete_response.py` - MetadataDeleteResponse (empty for 204)
9. `toggle_builtin_request.py` - MetadataToggleBuiltinRequest with dataset_id, action
10. `toggle_builtin_response.py` - MetadataToggleBuiltinResponse with result field
11. `update_document_request.py` - MetadataUpdateDocumentRequest with operation_data
12. `update_document_response.py` - MetadataUpdateDocumentResponse with result field

Include proper validation and use common models where applicable.
```

#### Step 8: Test Metadata Models
**Prompt:**
```
Create comprehensive unit tests for metadata request/response models in `tests/test_metadata_models.py`.

Test all models created in Step 7, covering:
1. Model validation and required fields
2. Builder pattern functionality
3. Serialization/deserialization
4. Complex nested structures (operation_data)
5. Edge cases and error handling

Ensure all tests pass with good coverage.
```

#### Step 9: Metadata Resource Implementation
**Prompt:**
```
Implement the Metadata resource class in `dify_oapi/api/knowledge_base/v1/resource/metadata.py`.

Create a Metadata class with the following methods:
1. `create(request: MetadataCreateRequest, request_option: RequestOption) -> MetadataCreateResponse`
2. `acreate(request: MetadataCreateRequest, request_option: RequestOption) -> MetadataCreateResponse`
3. `list(request: MetadataListRequest, request_option: RequestOption) -> MetadataListResponse`
4. `alist(request: MetadataListRequest, request_option: RequestOption) -> MetadataListResponse`
5. `update(request: MetadataUpdateRequest, request_option: RequestOption) -> MetadataUpdateResponse`
6. `aupdate(request: MetadataUpdateRequest, request_option: RequestOption) -> MetadataUpdateResponse`
7. `delete(request: MetadataDeleteRequest, request_option: RequestOption) -> MetadataDeleteResponse`
8. `adelete(request: MetadataDeleteRequest, request_option: RequestOption) -> MetadataDeleteResponse`
9. `toggle_builtin(request: MetadataToggleBuiltinRequest, request_option: RequestOption) -> MetadataToggleBuiltinResponse`
10. `atoggle_builtin(request: MetadataToggleBuiltinRequest, request_option: RequestOption) -> MetadataToggleBuiltinResponse`
11. `update_document(request: MetadataUpdateDocumentRequest, request_option: RequestOption) -> MetadataUpdateDocumentResponse`
12. `aupdate_document(request: MetadataUpdateDocumentRequest, request_option: RequestOption) -> MetadataUpdateDocumentResponse`

Handle path parameters correctly and follow existing patterns.
```

#### Step 10: Test Metadata Resource
**Prompt:**
```
Create comprehensive integration tests for the Metadata resource in `tests/test_metadata_resource.py`.

Test all methods implemented in Step 9, including:
1. HTTP method and URL mapping verification (including path parameters)
2. Request serialization and response deserialization
3. Error handling for various HTTP status codes
4. Both sync and async method variants
5. Mock API responses based on the API documentation

Use pytest fixtures and mock responses. Ensure all tests pass.
```

### Phase 4: Tag Management APIs (7 APIs)

#### Step 11: Tag Request/Response Models
**Prompt:**
```
Create all request and response models for tag management APIs in `dify_oapi/api/knowledge_base/v1/model/tag/`.

Implement the following model files:

1. `create_request.py` - TagCreateRequest with name field
2. `create_response.py` - TagCreateResponse using TagInfo
3. `list_request.py` - TagListRequest (no parameters)
4. `list_response.py` - TagListResponse with array of TagInfo
5. `update_request.py` - TagUpdateRequest with name and tag_id
6. `update_response.py` - TagUpdateResponse using TagInfo
7. `delete_request.py` - TagDeleteRequest with tag_id
8. `delete_response.py` - TagDeleteResponse with result field
9. `bind_request.py` - TagBindRequest with tag_ids array and target_id
10. `bind_response.py` - TagBindResponse with result field
11. `unbind_request.py` - TagUnbindRequest with tag_id and target_id
12. `unbind_response.py` - TagUnbindResponse with result field
13. `query_bound_request.py` - TagQueryBoundRequest with dataset_id
14. `query_bound_response.py` - TagQueryBoundResponse with data array and total

Include proper validation and use TagInfo from common models.
```

#### Step 12: Test Tag Models
**Prompt:**
```
Create comprehensive unit tests for tag request/response models in `tests/test_tag_models.py`.

Test all models created in Step 11, covering:
1. Model validation and required fields
2. Builder pattern functionality
3. Serialization/deserialization
4. Array field handling (tag_ids)
5. Edge cases and error handling

Ensure all tests pass with good coverage.
```

#### Step 13: Tag Resource Implementation
**Prompt:**
```
Implement the Tag resource class in `dify_oapi/api/knowledge_base/v1/resource/tag.py`.

Create a Tag class with the following methods:
1. `create(request: TagCreateRequest, request_option: RequestOption) -> TagCreateResponse`
2. `acreate(request: TagCreateRequest, request_option: RequestOption) -> TagCreateResponse`
3. `list(request: TagListRequest, request_option: RequestOption) -> TagListResponse`
4. `alist(request: TagListRequest, request_option: RequestOption) -> TagListResponse`
5. `update(request: TagUpdateRequest, request_option: RequestOption) -> TagUpdateResponse`
6. `aupdate(request: TagUpdateRequest, request_option: RequestOption) -> TagUpdateResponse`
7. `delete(request: TagDeleteRequest, request_option: RequestOption) -> TagDeleteResponse`
8. `adelete(request: TagDeleteRequest, request_option: RequestOption) -> TagDeleteResponse`
9. `bind_tags(request: TagBindRequest, request_option: RequestOption) -> TagBindResponse`
10. `abind_tags(request: TagBindRequest, request_option: RequestOption) -> TagBindResponse`
11. `unbind_tags(request: TagUnbindRequest, request_option: RequestOption) -> TagUnbindResponse`
12. `aunbind_tags(request: TagUnbindRequest, request_option: RequestOption) -> TagUnbindResponse`
13. `query_bound(request: TagQueryBoundRequest, request_option: RequestOption) -> TagQueryBoundResponse`
14. `aquery_bound(request: TagQueryBoundRequest, request_option: RequestOption) -> TagQueryBoundResponse`

Handle different URL patterns correctly (global vs dataset-specific endpoints).
```

#### Step 14: Test Tag Resource
**Prompt:**
```
Create comprehensive integration tests for the Tag resource in `tests/test_tag_resource.py`.

Test all methods implemented in Step 13, including:
1. HTTP method and URL mapping verification
2. Request serialization and response deserialization
3. Error handling for various HTTP status codes
4. Both sync and async method variants
5. Mock API responses based on the API documentation
6. Different endpoint patterns (global vs dataset-specific)

Use pytest fixtures and mock responses. Ensure all tests pass.
```

### Phase 5: Integration and Version Updates

#### Step 15: Update Version Integration
**Prompt:**
```
Update the knowledge_base v1 version integration to include the new resources.

Modify `dify_oapi/api/knowledge_base/v1/version.py` to:
1. Import the new Metadata and Tag resource classes
2. Add metadata and tag properties to the V1 class
3. Initialize them with the transport instance
4. Ensure backward compatibility with existing resources

Update any necessary import statements and maintain the existing API structure.
```

#### Step 16: Test Version Integration
**Prompt:**
```
Create integration tests for the updated V1 version class in `tests/test_knowledge_base_v1_integration.py`.

Test:
1. All resources are properly initialized
2. Transport is correctly passed to all resources
3. New resources (metadata, tag) are accessible
4. Existing resources still work correctly
5. Client integration works end-to-end

Ensure the complete knowledge_base module works as expected.
```

### Phase 6: Documentation and Examples

#### Step 17: Create Usage Examples
**Prompt:**
```
Create comprehensive usage examples for the dataset management functionality in `examples/knowledge_base/`.

Create the following example files:
1. `dataset_management.py` - Complete dataset CRUD operations
2. `metadata_management.py` - Metadata operations and document metadata updates
3. `tag_management.py` - Tag operations and binding/unbinding
4. `dataset_retrieval.py` - Advanced retrieval with filtering and reranking
5. `complete_workflow.py` - End-to-end workflow combining all features

Each example should include:
- Proper error handling
- Clear comments explaining each step
- Real-world use cases
- Both sync and async variants where applicable
```

#### Step 18: Test Examples
**Prompt:**
```
Create validation tests for all examples created in Step 17.

Create `tests/test_examples_validation.py` that:
1. Validates example code syntax and imports
2. Mocks API calls to test example logic
3. Ensures examples follow best practices
4. Verifies error handling works correctly
5. Tests both sync and async example variants

Ensure all examples are functional and educational.
```

### Phase 7: Final Integration and Quality Assurance

#### Step 19: Comprehensive Integration Testing
**Prompt:**
```
Create comprehensive end-to-end integration tests in `tests/test_dataset_api_integration.py`.

Test complete workflows:
1. Dataset lifecycle (create → update → retrieve → delete)
2. Metadata management workflow
3. Tag management and binding workflow
4. Cross-resource interactions
5. Error scenarios and edge cases
6. Performance considerations for large datasets

Use realistic test data and scenarios. Ensure all 19 APIs work together correctly.
```

#### Step 20: Final Quality Assurance and Documentation
**Prompt:**
```
Perform final quality assurance and create comprehensive documentation.

Tasks:
1. Run all tests and ensure 100% pass rate
2. Verify code coverage meets project standards
3. Update API documentation with new functionality
4. Create migration guide for existing users
5. Update README with new dataset management features
6. Perform code review checklist:
   - Type hints are comprehensive
   - Error handling is consistent
   - Builder patterns work correctly
   - Async/sync parity is maintained
   - Documentation is complete

Create a final validation report confirming all requirements are met.
```

## Success Criteria

Each step should meet the following criteria:
- ✅ All code follows existing project patterns and conventions
- ✅ Comprehensive type hints and Pydantic validation
- ✅ Both sync and async method variants implemented
- ✅ Builder pattern support for all request models
- ✅ Proper error handling and HTTP status code mapping
- ✅ Unit tests with good coverage (>90%)
- ✅ Integration tests with mock API responses
- ✅ Documentation and examples provided
- ✅ Backward compatibility maintained where possible

## Notes

- Each implementation step should be followed immediately by its corresponding test step
- Use existing project patterns and maintain consistency with other API modules
- Ensure all 19 dataset APIs are fully functional and well-tested
- Prioritize type safety and developer experience throughout the implementation
- Follow the established directory structure and naming conventions