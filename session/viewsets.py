from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User

from .models import UserSession
from .serializers import (
    UserSessionSerializer,

    UserSerializer,
    UserCreateSerializer,
    UserDetailSerializer
)
from .tasks import (open_session, close_session)

from .selenium_manager import ThreadSafeSeleniumManager
from hashlib import md5


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        elif self.action in ['list', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """Create a new user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ThreadSafeSeleniumManager.create_session()
        
        return Response(
            {
                "message": "User created successfully",
                "user": UserSerializer(serializer.instance).data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def current_user(self, request):
        """Get current authenticated user information"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """
        Change password for a user.
        POST with old_password and new_password
        """
        user = self.get_object()
        
        # Check if user is changing their own password or is admin
        if user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You can only change your own password."},
                status=status.HTTP_403_FORBIDDEN
            )

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {"detail": "Both old_password and new_password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK
        )

class UserSessionViewSet(viewsets.ModelViewSet):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserSession.objects.all()
        return UserSession.objects.filter(created_by=self.request.user)
    
    @classmethod
    def _generate_user_id(cls, user: User):
        return md5(
            f'{user.date_joined}{user.username}'.encode()
        ).hexdigest() + str((user.id * 74) % 214)
    
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = self.request.user.id
        request.data['is_open'] = True
        
        user_id = self._generate_user_id(self.request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        data = UserSessionSerializer(serializer.instance).data
        
        task = open_session.delay(
            session_id=data['session_id'],
            messanger_type=data['messanger_type'],
            user_id=user_id
        )

        return Response(
            {
                "message": "Session is creating",
                "task_id": task.id,
                "task_status": "queued",
                "session": UserSessionSerializer(serializer.instance).data
            },
            status=status.HTTP_201_CREATED
        )
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to close browser when session is deleted"""
        session = self.get_object()
        session_id = session.session_id

        if not (self.request.user.is_superuser or session.created_by == self.request.user):
            return Response(
                {'error': 'Not enough permission to make actions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Close browser
            task = close_session.delay(session_id=str(session_id))
            # Delete model instance
            self.perform_destroy(session)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Invalid request'},
            status=status.HTTP_400_BAD_REQUEST
        )