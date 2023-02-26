from chat_api.models import Message
from rest_framework import serializers


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.CharField(required=False)
    time = serializers.TimeField(required=False)
    date = serializers.DateField(required=False)
    class Meta:
        model = Message
        fields = ['text', 'date', 'time', 'author']


