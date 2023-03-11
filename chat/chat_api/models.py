from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rooms")
    current_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="current_rooms", blank=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages")

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=30)
    profile_image = models.ImageField(upload_to='images/', max_length=100, default=None)
