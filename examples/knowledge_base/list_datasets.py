from dify_oapi.api.knowledge_base.v1.model.list_dataset_request import ListDatasetRequest
from dify_oapi.client import Client
from dify_oapi.core.model.request_option import RequestOption

def main():
    client = Client.builder().domain("https://api.dify.ai").build()

    req = ListDatasetRequest.builder().build()
    req_option = RequestOption.builder().api_key("<your-api-key>").build()

    response = client.knowledge_base.v1.dataset.list(req, req_option)
    if response.success:
        for dataset in response.data:
            print(f"Dataset: {dataset.name} (ID: {dataset.id})")

if __name__ == "__main__":
    main()
