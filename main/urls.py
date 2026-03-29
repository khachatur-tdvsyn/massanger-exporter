from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import routers
from .viewsets import (
    UserViewSet,
    ChatViewSet,
    MessageViewSet,
    ChatIconViewSet,
    UserIconViewSet,
    ReactionViewSet,
    AttachmentViewSet,
)

router = routers.DefaultRouter()
avaiable_viewsets = {
    r'users': UserViewSet,
    r'chats': ChatViewSet,
    r'messages': MessageViewSet,
    r'chat-icons': ChatIconViewSet,
    r'user-icons': UserIconViewSet,
    r'reactions': ReactionViewSet,
    r'attachments': AttachmentViewSet,
}

for v in avaiable_viewsets:
    router.register(v, avaiable_viewsets[v], basename=v)

urlpatterns = [
    path('', include(router.urls))
]