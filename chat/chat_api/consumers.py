import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from datetime import datetime
from django.forms.models import model_to_dict

from django.core import serializers
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer

from .models import Room, Message
from django.contrib.auth.models import User
from .serializers import MessageSerializer, RoomSerializer, UserSerializer


class RoomConsumer(WebsocketConsumer):


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_pk = Room.objects.get(name=self.room_name).pk
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        self.get_messages()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.create_message(Room.objects.get(pk=self.room_pk), message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message, "user": self.scope['user'].username, "date": str(datetime.now())}))

    def create_message(self, room, text):
        message = Message(room=room, text=text, user=self.user)
        async_to_sync(message.save())

    def get_messages(self):
        messages = Message.objects.filter(room=self.room_pk)
        messages_json = json.dumps(MessageSerializer(messages, many=True).data)
        self.send(text_data=messages_json)