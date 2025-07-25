# Datasets API Design Document

## Overview

This document describes the design updates for the dify-oapi knowledge_base module based on the latest API documentation. This update will support a complete set of 39 APIs, covering four major modules: dataset management, document management, segment management, and system configuration.

## Design Decisions

### 1. Resource Organization Structure

**Decision**: Create new resource classes to organize APIs

**New Resource Classes**:
- `metadata` - Handle dataset metadata management (7 APIs)
- `tag` - Handle knowledge base type tag management (7 APIs)
- `child_chunk` - Handle segment child chunk management (4 APIs)
- `system` - Handle system configuration (1 API)

**Extended Existing Resources**:
- `dataset` - Add get, update, retrieve methods
- `document` - Add get_details, update_status, get_upload_file methods
- `segment` - Add get method

### 2. Method Naming Convention

**Decision**: Mixed naming approach

- **Core CRUD Operations**: Use simple verb naming (create, list, delete, update, get)
- **Special Functions**: Use descriptive naming (get_details, update_status, get_upload_file, hit_test, retrieve)

### 3. Model File Organization

**Decision**: Organize model files by resource grouping

**New Directory Structure**:
```
model/
├── dataset/          # Dataset-related models
├── document/         # Document-related models
├── segment/          # Segment-related models
├── metadata/         # Metadata-related models
├── tag/             # Tag-related models
├── child_chunk/     # Child chunk-related models
├── system/          # System-related models
└── common/          # Common models
```

### 4. Special API Path Handling

**Decision**: Maintain API documentation paths with appropriate code organization adjustments

**Special Path Handling**:
- Tag management API (`/datasets/tags`) - Global tag management, placed in tag resource
- System API (`/workspaces/current/models/model-types/text-embedding`) - System-level API, placed in system resource
- Document status API (`/datasets/{dataset_id}/documents/status/{action}`) - Use path parameter action pattern

### 5. Response Model Design

**Decision**: Create dedicated Response models for each API

Even for APIs that return `204 No Content` or simple `{"result": "success"}`, create corresponding response models to maintain consistency and type safety.

### 6. Nested Data Structure Handling

**Decision**: Define all nested objects as independent model class files

Regardless of the complexity of nested objects, create independent model class files to ensure:
- Code structure consistency and clarity
- Better type safety and IDE support
- Easier individual testing and maintenance
- Support for cross-model reuse

### 7. Backward Compatibility

**Decision**: Directly modify existing models and APIs

Do not consider backward compatibility; directly update existing implementations to comply with the latest API specifications, ensuring functional completeness and consistency.

## Implementation Plan

### Phase 1: Directory Structure Reorganization
1. Create model subdirectories grouped by resource
2. Migrate existing model files to corresponding directories
3. Update import paths

### Phase 2: Add New Resource Classes
1. Create metadata, tag, child_chunk, system resource classes
2. Implement corresponding API methods
3. Create related request/response models

### Phase 3: Extend Existing Resources
1. Extend dataset resource (get, update, retrieve methods)
2. Extend document resource (get_details, update_status, get_upload_file methods)
3. Extend segment resource (get method)

### Phase 4: Model Enhancement
1. Create independent model classes for complex nested objects
2. Complete all request/response models
3. Add appropriate type annotations and validation

### Phase 5: Version Integration
1. Update v1/version.py to include new resources
2. Update service.py initialization
3. Update related imports and exports

## API Coverage

### Dataset Management (19 APIs)
- ✅ Basic CRUD: create, list, delete
- 🆕 Details and updates: get, update
- 🆕 Retrieval functionality: retrieve
- 🆕 Metadata management: 7 metadata-related APIs
- 🆕 Tag management: 7 tag-related APIs

### Document Management (10 APIs)
- ✅ Basic operations: create_by_text, create_by_file, update_by_text, update_by_file, list, delete
- ✅ Status queries: indexing_status
- 🆕 Details and status: get_details, update_status, get_upload_file

### Segment Management (9 APIs)
- ✅ Basic CRUD: create, list, delete, update
- 🆕 Detail queries: get
- 🆕 Child chunk management: 4 child_chunk-related APIs

### System Configuration (1 API)
- 🆕 System configuration: get_embedding_models

## Technical Specifications

- **HTTP Client**: Continue using Transport/ATransport
- **Data Validation**: Use Pydantic models
- **Async Support**: All APIs provide both synchronous and asynchronous versions
- **Builder Pattern**: All request models support Builder pattern
- **Type Safety**: Complete type annotation support

## Summary

This design ensures that the dify-oapi knowledge_base module can fully support all datasets-related functionality of the Dify API while maintaining code structure clarity and maintainability. Through reasonable resource grouping, model organization, and naming conventions, it provides developers with a consistent and easy-to-use API interface.
