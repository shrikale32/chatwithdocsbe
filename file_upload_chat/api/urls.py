from django.urls import path
from file_upload_chat.api.views import ChatList, ChatDetail, LoadDataPineCone, MessageDetail, chat_view

urlpatterns = [
    path('chats/', ChatList.as_view(), name='chat-list'),
    path('chats/<int:pk>/', ChatDetail.as_view(), name='chat-detail'),
    path('ai/', chat_view, name="chat-view"),
    path('pinecone/', LoadDataPineCone.as_view(), name="pinecone"),
    path('messages/', MessageDetail.as_view(), name="messages"),
]