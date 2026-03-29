from django.db import models
from main.models import MessangerType, AssignableModel
from django.contrib.auth.models import User

from uuid import uuid4

# Create your models here.
class UserSession(AssignableModel):
    session_id = models.UUIDField(default=uuid4, primary_key=True)
    messanger_type = models.CharField(max_length=8, choices=MessangerType, default=MessangerType.WHATS_APP)
    is_open = models.BooleanField(default=False)