from rest_framework import serializers
from file_upload_chat.models import Chat, Messages

class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'