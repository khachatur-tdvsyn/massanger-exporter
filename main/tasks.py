from celery import shared_task

from service.whatsapp import WhatsappSession
from django.conf import settings


@shared_task
def start_login_whatsapp(phone_number):
    session = WhatsappSession(None, settings.PROFILES_PATH, phone_number)
    result = session.login()
    return result