# Dify-OAPI Project Overview

## Project Description
Dify-OAPI is a Python SDK client for interacting with the Dify Service-API. The SDK allows developers to easily build web applications that communicate with Dify's API services for AI-powered features like chat, completion, workflow, and knowledge base.

## Directory Structure

### Main Modules

- **dify_oapi**: Root package for the SDK
  - **__init__.py**: Package initialization
  - **client.py**: Main client interface that provides access to all services
  - **api/**: Contains all API services organized by feature
    - **chat/**: Chat API service
    - **completion/**: Completion API service
    - **dify/**: Core Dify API service
    - **knowledge_base/**: Knowledge base API service
    - **workflow/**: Workflow API service
  - **core/**: Core functionality used across the SDK
    - **http/**: HTTP transport layer for making API requests
      - **transport/**: Implementations for sync and async transport
    - **model/**: Base models for requests and responses
    - **utils/**: Utility functions
    - **const.py**: Constants used in the SDK
    - **enum.py**: Enumerations used in the SDK
    - **json.py**: JSON handling utilities
    - **log.py**: Logging configuration
    - **misc.py**: Miscellaneous utilities
    - **type.py**: Type definitions

### API Structure Pattern
Each API service follows a consistent structure:
- **service.py**: Service class that initializes version-specific implementations
- **v1/**: Version 1 implementation of the API
  - **version.py**: Provides access to different resources
  - **model/**: Data models for requests and responses
  - **resource/**: Resource classes that implement actual API endpoints

### Tests
- **tests/**: Test suite for all API features
  - **test_chat.py**: Tests for chat API
  - **test_completion.py**: Tests for completion API
  - **test_dify.py**: Tests for core Dify API
  - **test_knowledge.py**: Tests for knowledge base API
  - **test_workflow.py**: Tests for workflow API

## Tech Stack

### Programming Language
- **Python 3.11+**: The SDK is built with Python 3.11 or higher

### Core Dependencies
- **httpx**: Modern HTTP client for Python
- **pydantic**: Data validation and settings management
- **typing_extensions**: Backported typing features

### Development Dependencies
- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **black**: Code formatting
- **isort**: Import sorting
- **poetry**: Dependency management and packaging

### Build System
- **poetry-core**: Used as the build backend

### Project Organization
- **Poetry**: Used for dependency management and packaging

## Key Features

1. **Builder Pattern**: The SDK uses the builder pattern for creating requests, providing a fluent interface for constructing API calls
2. **Sync and Async Support**: Both synchronous and asynchronous API calls are supported
3. **Streaming Responses**: Support for streaming responses in chat and completion APIs
4. **Type Hints**: Comprehensive type hints throughout the codebase
5. **Error Handling**: Built-in error handling and retry mechanisms
6. **Multiple Services**: Support for various Dify services (Chat, Completion, Knowledge Base, etc.)

## API Services

### Chat API
Allows interaction with Dify's chat capabilities, including:
- Creating chat messages
- Managing conversations
- Processing audio to text
- Streaming chat responses

### Completion API
Provides text completion capabilities through Dify's API.

### Knowledge Base API
Interfaces with Dify's knowledge base functionality, including:
- Managing datasets
- Managing documents within datasets
- Managing segments within documents
- Testing and indexing knowledge base content

### Workflow API
Provides access to Dify's workflow features.

### Dify API
Core API functionality for Dify services.
