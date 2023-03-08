from .models import Room, Message
from rest_framework import serializers
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ["username"]



class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ["text", "user", "created_at"]
        depth = 1

    def get_created_at(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["pk", "name", "host", "messages", "current_users", "last_message"]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj: Room):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data
