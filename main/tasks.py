from celery import shared_task

from service.whatsapp import WhatsappSession
from django.conf import settings


@shared_task
def login_whatsapp(phone_number):
    with WhatsappSession(None, settings.PROFILES_PATH, phone_number) as session:
        result = session.login()
        return result