from dify_oapi.api.chat.v1.model.get_conversation_list_request import GetConversationListRequest
from dify_oapi.api.chat.v1.model.message_history_request import MessageHistoryRequest
from dify_oapi.client import Client
from dify_oapi.core.model.request_option import RequestOption

def main():
    client = Client.builder().domain("https://api.dify.ai").build()
    req_option = RequestOption.builder().api_key("<your-api-key>").build()

    # Get conversation list
    conv_req = GetConversationListRequest.builder().build()
    conv_response = client.chat.v1.conversation.get_conversation_list(conv_req, req_option)

    if conv_response.data and len(conv_response.data) > 0:
        conversation_id = conv_response.data[0].id

        # Get message history for a conversation
        history_req = MessageHistoryRequest.builder().conversation_id(conversation_id).build()
        history_response = client.chat.v1.message.message_history(history_req, req_option)

        for message in history_response.data:
            print(f"Role: {message.role}, Content: {message.content}")

if __name__ == "__main__":
    main()
