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