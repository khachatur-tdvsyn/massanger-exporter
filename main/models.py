from django.db import models
from django.contrib.auth.models import User


class TimestampableModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AssignableModel(TimestampableModel):
    # Temporary set null for successful migration
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

class BaseIcon(TimestampableModel):
    file = models.FileField(upload_to='icons')
    class Meta:
        abstract = True
        
# Create your models here.
class MessangerType(models.TextChoices):
    WHATS_APP = ("wapp", "WhatsApp")
    TELEGRAM = ("tg", "Telegram")

class User(TimestampableModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=64, null=True, blank=True)
    messanger_type = models.CharField(max_length=8, choices=MessangerType)
    settings = models.JSONField(default=dict)

class Chat(AssignableModel):
    messanger_type = models.CharField(max_length=8, choices=MessangerType)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, related_name="chats", on_delete=models.CASCADE, null=True, blank=True)
    admin_users = models.ManyToManyField(User, related_name="admin_users", blank=True)

class Message(AssignableModel):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, related_name="messages", on_delete=models.SET_NULL)
    text = models.TextField(null=True, blank=True)
    replied_to = models.ForeignKey("self", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='replies'
    )

class Reaction(AssignableModel):
    symbol = models.CharField(max_length=2)
    user = models.ForeignKey(User, related_name='reactions', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='reactions', on_delete=models.CASCADE)

class FileType(models.IntegerChoices):
    BINARY = (0, 'Binary')
    IMAGE = (1, 'Image')
    VIDEO = (2, 'Video')
    TEXT = (3, 'Text')
    AUDIO = (4, 'Audio')

class Attachment(AssignableModel):
    message = models.ForeignKey(Message, null=True, related_name='attachments', on_delete=models.SET_NULL)
    file = models.FileField(upload_to='attachments')
    name = models.CharField(max_length=255)
    file_type = models.IntegerField(choices=FileType)

class ChatIcon(BaseIcon):
    chat = models.ForeignKey(Chat, related_name='icons', on_delete=models.CASCADE)

class UserIcon(BaseIcon):
    user = models.ForeignKey(User, related_name='icons', on_delete=models.CASCADE)