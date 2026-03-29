from celery import shared_task
from dataclasses import asdict, dataclass

from service.whatsapp import WhatsappSession
from django.conf import settings


@shared_task
def start_login_whatsapp(phone_number):
    session = WhatsappSession(None, settings.PROFILES_PATH, phone_number)
    result = session.login()
    return result

@shared_task
def get_chats_list(phone_number):
    with WhatsappSession(None, settings.PROFILES_PATH, phone_number) as session:
        result = session.get_chats()
        return [asdict(r) for r in result]