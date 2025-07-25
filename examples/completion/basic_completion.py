from dify_oapi.api.completion.v1.model.completion_request import CompletionRequest
from dify_oapi.api.completion.v1.model.completion_request_body import CompletionRequestBody
from dify_oapi.client import Client
from dify_oapi.core.model.request_option import RequestOption

def main():
    client = Client.builder().domain("https://api.dify.ai").build()

    req_body = (
        CompletionRequestBody.builder()
        .inputs({})
        .query("Write a short poem about AI")
        .response_mode("blocking")
        .user("user-123")
        .build()
    )

    req = CompletionRequest.builder().request_body(req_body).build()
    req_option = RequestOption.builder().api_key("<your-api-key>").build()

    response = client.completion.v1.completion.completion(req, req_option, False)
    print(response.answer)

if __name__ == "__main__":
    main()
