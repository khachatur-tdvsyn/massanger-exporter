from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from celery.result import AsyncResult

from django.contrib.auth import get_user_model

from .models import User, Chat, Message, ChatIcon, UserIcon, Reaction, Attachment
from .tasks import start_login_whatsapp, get_chats_list
from .serializers import (
    UserSerializer,
    ChatSerializer,
    MessageSerializer,
    ChatIconSerializer,
    UserIconSerializer,
    ReactionSerializer,
    AttachmentSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]



class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]



class ChatIconViewSet(ModelViewSet):
    queryset = ChatIcon.objects.all()
    serializer_class = ChatIconSerializer
    permission_classes = [IsAuthenticated]


class UserIconViewSet(ModelViewSet):
    queryset = UserIcon.objects.all()
    serializer_class = UserIconSerializer
    permission_classes = [IsAuthenticated]


class ReactionViewSet(ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]


class AttachmentViewSet(ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]