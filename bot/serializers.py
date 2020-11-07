from rest_framework import serializers

from .models import Message, Client

class MessagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'message',
            'status',
            'sended_at'
        )

class ClientsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'chat_id',
            'name'
        )
