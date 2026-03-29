from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import routers
from .viewsets import (
    UserViewSet,
    UserSessionViewSet
)

router = routers.DefaultRouter()
avaiable_viewsets = {
    r'users': UserViewSet,
    r'sessions': UserSessionViewSet
}

for v in avaiable_viewsets:
    router.register(v, avaiable_viewsets[v], basename=v)

urlpatterns = [
    path('', include(router.urls))
]