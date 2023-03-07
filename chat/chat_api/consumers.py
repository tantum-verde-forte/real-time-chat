import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from datetime import datetime

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

    Messages = posts = Message.objects.all()

    def connect(self):
        self.room_name = '1'
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        pk = text_data_json["pk"]

        b = Message(room=Room.objects.get(pk=pk), text=message, user=self.user)
        async_to_sync(b.save())

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message, "user": self.scope['user'].username, "date": str(datetime.now().time())}))

