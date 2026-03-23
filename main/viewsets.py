from rest_framework.viewsets import ModelViewSet
from .models import User, Chat, Message, ChatIcon, UserIcon, Reaction, Attachment
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


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatIconViewSet(ModelViewSet):
    queryset = ChatIcon.objects.all()
    serializer_class = ChatIconSerializer


class UserIconViewSet(ModelViewSet):
    queryset = UserIcon.objects.all()
    serializer_class = UserIconSerializer


class ReactionViewSet(ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


class AttachmentViewSet(ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer