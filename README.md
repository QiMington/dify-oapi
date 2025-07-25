# dify-oapi

A Dify App Service-API Client for building web applications by requesting the Dify Service-API. This Python SDK provides comprehensive access to Dify's API services including Chat, Completion, Knowledge Base, and Workflow features.

For detailed information about the project structure, modules, and technical stack, please see [docs/Overview.md](./docs/Overview.md).

## Features

- **Multiple Services**: Access to Chat, Completion, Knowledge Base, and Workflow services
- **Builder Pattern**: Fluent interface for constructing API calls
- **Sync and Async Support**: Both synchronous and asynchronous API calls
- **Streaming Responses**: Support for streaming responses in chat and completion APIs
- **Type Hints**: Comprehensive type hints throughout the codebase
- **Error Handling**: Built-in error handling and retry mechanisms

## Installation

```bash
pip install dify-oapi
```

## Quick Start

```python
from dify_oapi.api.chat.v1.model.chat_request import ChatRequest
from dify_oapi.api.chat.v1.model.chat_request_body import ChatRequestBody
from dify_oapi.client import Client
from dify_oapi.core.model.request_option import RequestOption

# Initialize the client
client = Client.builder().domain("https://api.dify.ai").build()

# Create request body
req_body = (
    ChatRequestBody.builder()
    .inputs({})
    .query("What can Dify API do?")
    .response_mode("blocking")
    .build()
)

# Create request
req = ChatRequest.builder().request_body(req_body).build()
req_option = RequestOption.builder().api_key("<your-api-key>").build()

# Make API call
response = client.chat.v1.chat.chat(req, req_option, False)

# Print response
print(response.answer)
```

## Examples

For more comprehensive examples, check out the [examples directory](./examples):

- **Chat API**
  - [Blocking Response](./examples/chat/blocking_response.py)
  - [Streaming Response](./examples/chat/streaming_response.py)
  - [Conversation Management](./examples/chat/conversation_management.py)

- **Completion API**
  - [Basic Completion](./examples/completion/basic_completion.py)

- **Knowledge Base API**
  - [List Datasets](./examples/knowledge_base/list_datasets.py)

## Development

### Setup Development Environment

1. Clone the repository:

```bash
git clone https://github.com/QiMington/dify-oapi.git
cd dify-oapi
```

2. Install dependencies using Poetry:

```bash
poetry install
```

Or using Mamba with the provided environment.yml:

```bash
mamba env create -f environment.yml
mamba activate dify-oapi
pip install -e .
```

### Running Tests

```bash
Set up environment variables for testing:

```bash
export DOMAIN="https://api.dify.ai"  # Or your Dify API endpoint
export CHAT_KEY="your-api-key"
```

Run tests:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
