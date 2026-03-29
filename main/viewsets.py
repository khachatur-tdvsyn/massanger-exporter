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

    MessangerLoginSerializer,
    MessangerLogoutSerializer,
    TaskStatusSerializer
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

class WhatsappSessionViewSet(GenericViewSet):
    queryset = get_user_model().objects.none()  # satisfies DRF's basename inference, never actually used
    permission_classes = [IsAuthenticated]
    serializer_class = MessangerLoginSerializer
    """
    POST /api/instagram/login/        → enqueues login task, returns task_id
    POST /api/instagram/logout/       → enqueues logout task, returns task_id
    GET  /api/instagram/status/?task_id=<id> → polls task result
    """

    def list():
        return Response({'message': 'Everything is ok'})


    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = MessangerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = start_login_whatsapp.delay(
            phone_number=serializer.validated_data["phone_number"]
        )

        return Response(
            {"task_id": task.id, "status": "queued"},
            status=status.HTTP_202_ACCEPTED,
        )
    
    @action(detail=False, methods=["post"])
    def get_chats(self, request):
        serializer = MessangerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = get_chats_list.delay(
            phone_number=serializer.validated_data["phone_number"]
        )

        return Response(
            {"task_id": task.id, "status": "queued"},
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=False, methods=["get"], url_path="task-status/(?P<task_id>[^/.]+)")
    def task_status(self, request, task_id=None):
        result = AsyncResult(task_id)  # pk captures the task_id from the URL

        payload = {
            "task_id": task_id,
            "status": result.status,
        }

        if result.successful():
            payload["result"] = result.result
        elif result.failed():
            payload["result"] = {"error": str(result.result)}

        serializer = TaskStatusSerializer(payload)
        return Response(serializer.data)