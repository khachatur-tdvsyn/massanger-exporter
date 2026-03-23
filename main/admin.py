from django.contrib import admin
from django.utils.html import format_html
from .models import User, Chat, Message, ChatIcon, UserIcon, Reaction, Attachment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'phone_number', 'messanger_type')
    search_fields = ('first_name', 'last_name', 'username', 'phone_number')
    list_filter = ('messanger_type',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'messanger_type', 'creator', 'description')
    search_fields = ('name', 'description')
    list_filter = ('messanger_type',)
    filter_horizontal = ('admin_users',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'author', 'text', 'replied_to')
    search_fields = ('text',)
    list_filter = ('chat', 'author')


@admin.register(ChatIcon)
class ChatIconAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'file')


@admin.register(UserIcon)
class UserIconAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'image')

    def image(self, obj):
        if obj.file:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; object-fit: cover;" />',
                obj.file.url
            )
        return "No image"

    image.short_description = 'Preview'


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'user', 'message')
    list_filter = ('symbol',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file_type', 'message', 'file')
    list_filter = ('file_type',)