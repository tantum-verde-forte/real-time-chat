from django.shortcuts import render

from chat_api.models import Message
from rest_framework import viewsets
from rest_framework import permissions
from chat_api.serializers import MessageSerializer
from datetime import datetime
from rest_framework.decorators import api_view


def lobby(request):
    return render(request, 'chat/lobby.html')

class MessageViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


