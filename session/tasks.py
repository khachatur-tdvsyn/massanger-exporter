from celery import shared_task
from dataclasses import asdict, dataclass

from service.whatsapp import WhatsappSession
from django.conf import settings

from .selenium_manager import ThreadSafeSeleniumManager


@shared_task
def open_session(session_id, messanger_type, user_id):
    r = ThreadSafeSeleniumManager.create_session(session_id, messanger_type, user_id)
    return str(r)

@shared_task
def close_session(session_id):
    r = ThreadSafeSeleniumManager.close_session(session_id)
    return str(r)