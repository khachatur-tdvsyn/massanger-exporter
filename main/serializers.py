from rest_framework import serializers
from .models import User, Chat, Message, ChatIcon, UserIcon, Reaction, Attachment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatIcon
        fields = '__all__'


class UserIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIcon
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class MessangerLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})


class MessangerLogoutSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})


class TaskStatusSerializer(serializers.Serializer):
    task_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    result = serializers.JSONField(read_only=True, required=False)