# System Configuration APIs

This document covers system configuration APIs for knowledge base settings and model information.

## Authentication

All Service API requests use `API-Key` for authentication. Include your `API-Key` in the **`Authorization`** HTTP Header:

```
Authorization: Bearer {API_KEY}
```

## APIs

### 1. Get Embedding Model List

**GET** `/workspaces/current/models/model-types/text-embedding`

Retrieves available embedding model list.

#### Response
```json
{
  "data": [
    {
      "provider": "zhipuai",
      "label": {
        "zh_Hans": "智谱 AI",
        "en_US": "ZHIPU AI"
      },
      "icon_small": {
        "zh_Hans": "http://127.0.0.1:5001/console/api/workspaces/current/model-providers/zhipuai/icon_small/zh_Hans",
        "en_US": "http://127.0.0.1:5001/console/api/workspaces/current/model-providers/zhipuai/icon_small/en_US"
      },
      "icon_large": {
        "zh_Hans": "http://127.0.0.1:5001/console/api/workspaces/current/model-providers/zhipuai/icon_large/zh_Hans",
        "en_US": "http://127.0.0.1:5001/console/api/workspaces/current/model-providers/zhipuai/icon_large/en_US"
      },
      "status": "active",
      "models": [
        {
          "model": "embedding-3",
          "label": {
            "zh_Hans": "embedding-3",
            "en_US": "embedding-3"
          },
          "model_type": "text-embedding",
          "features": null,
          "fetch_from": "predefined-model",
          "model_properties": {
            "context_size": 8192
          },
          "deprecated": false,
          "status": "active",
          "load_balancing_enabled": false
        },
        {
          "model": "embedding-2",
          "label": {
            "zh_Hans": "embedding-2",
            "en_US": "embedding-2"
          },
          "model_type": "text-embedding",
          "features": null,
          "fetch_from": "predefined-model",
          "model_properties": {
            "context_size": 8192
          },
          "deprecated": false,
          "status": "active",
          "load_balancing_enabled": false
        },
        {
          "model": "text_embedding",
          "label": {
            "zh_Hans": "text_embedding",
            "en_US": "text_embedding"
          },
          "model_type": "text-embedding",
          "features": null,
          "fetch_from": "predefined-model",
          "model_properties": {
            "context_size": 512
          },
          "deprecated": false,
          "status": "active",
          "load_balancing_enabled": false
        }
      ]
    }
  ]
}
```