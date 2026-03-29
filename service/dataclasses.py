from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

from main.models import User, Chat, Message, Reaction, Attachment, ChatIcon, UserIcon

# Define choices as strings for simplicity
class MessangerType:
    WHATS_APP = "wapp"
    TELEGRAM = "tg"

class FileType:
    BINARY = 0
    IMAGE = 1
    VIDEO = 2
    TEXT = 3
    AUDIO = 4

@dataclass
class UserData:
    id: Optional[int] = None
    first_name: str = ""
    last_name: Optional[str] = None
    username: str = ""
    phone_number: Optional[str] = None
    messanger_type: str = MessangerType.WHATS_APP
    settings: Dict[str, Any] = None

    def __post_init__(self):
        if self.settings is None:
            self.settings = {}

    def to_model(self) -> User:
        user = User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            phone_number=self.phone_number,
            messanger_type=self.messanger_type,
            settings=self.settings
        )
        return user

@dataclass
class ChatData:
    id: Optional[int] = None
    messanger_type: str = MessangerType.WHATS_APP
    name: str = ""
    description: Optional[str] = None
    creator_id: int = 0
    admin_user_ids: List[int] = None

    def __post_init__(self):
        if self.admin_user_ids is None:
            self.admin_user_ids = []

    def to_model(self) -> Chat:
        creator = User.objects.get(id=self.creator_id)
        chat = Chat(
            id=self.id,
            messanger_type=self.messanger_type,
            name=self.name,
            description=self.description,
            creator=creator
        )
        return chat

@dataclass
class MessageData:
    id: Optional[int] = None
    chat_id: int = 0
    author_id: Optional[int] = None
    text: Optional[str] = None
    replied_to_id: Optional[int] = None

    def to_model(self) -> Message:
        chat = Chat.objects.get(id=self.chat_id)
        author = User.objects.get(id=self.author_id) if self.author_id else None
        replied_to = Message.objects.get(id=self.replied_to_id) if self.replied_to_id else None
        message = Message(
            id=self.id,
            chat=chat,
            author=author,
            text=self.text,
            replied_to=replied_to
        )
        return message

@dataclass
class ReactionData:
    id: Optional[int] = None
    symbol: str = ""
    user_id: int = 0
    message_id: int = 0

    def to_model(self) -> Reaction:
        user = User.objects.get(id=self.user_id)
        message = Message.objects.get(id=self.message_id)
        reaction = Reaction(
            id=self.id,
            symbol=self.symbol,
            user=user,
            message=message
        )
        return reaction

@dataclass
class AttachmentData:
    id: Optional[int] = None
    message_id: Optional[int] = None
    file_path: str = ""
    name: str = ""
    file_type: int = FileType.BINARY

    def to_model(self) -> Attachment:
        message = Message.objects.get(id=self.message_id) if self.message_id else None
        attachment = Attachment(
            id=self.id,
            message=message,
            file=self.file_path,
            name=self.name,
            file_type=self.file_type
        )
        return attachment

@dataclass
class ChatIconData:
    id: Optional[int] = None
    chat_id: int = 0
    file_path: str = ""

    def to_model(self) -> ChatIcon:
        chat = Chat.objects.get(id=self.chat_id)
        icon = ChatIcon(
            id=self.id,
            chat=chat,
            file=self.file_path
        )
        return icon

@dataclass
class UserIconData:
    id: Optional[int] = None
    user_id: int = 0
    file_path: str = ""

    def to_model(self) -> UserIcon:
        user = User.objects.get(id=self.user_id)
        icon = UserIcon(
            id=self.id,
            user=user,
            file=self.file_path
        )
        return icon