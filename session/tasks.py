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

@shared_task
def start_login(session_id, phone_number):
    session_id = str(session_id)
    session = ThreadSafeSeleniumManager.get_session(session_id)
    result = session.login(phone_number)
    return result

@shared_task
def get_chats_list(session_id):
    session_id = str(session_id)
    session = ThreadSafeSeleniumManager.get_session(session_id)
    result = session.get_chats()
    return [asdict(r) for r in result]