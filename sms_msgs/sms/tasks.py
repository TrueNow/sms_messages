import datetime
import os
import pytz
import requests

from celery.utils.log import get_task_logger

from .models import Message, Client, Mailing
from ..sms_msgs.celery import app


logger = get_task_logger(__name__)

URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
SECONDS_IN_HOUR = 3600


@app.task(bind=True, retry_backoff=True)
def send_message(self, data, client_id, mailing_id, url=URL, token=TOKEN):
    mail = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    index = data['id']

    timezone = pytz.timezone(client.timezone)
    if mail.can_send(timezone):
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        try:
            requests.post(url=url + str(index), headers=header, json=data)
        except requests.exceptions.RequestException as exc:
            logger.error(f"Message if: {index} is error")
            raise self.retry(exc=exc)
        else:
            logger.info(f"Message id: {index}, Sending status: 'Sent'")
            Message.objects.filter(pk=index).update(status=Message.SENT)
    else:
        time = (
            24 - datetime.datetime.now().time().hour
            + mail.time_start.time().hour
        )
        logger.info(f'Message id: {index}, '
                    f'The current time is not for sending the message, '
                    f'restarting task after {SECONDS_IN_HOUR * time} seconds')
        return self.retry(countdown=SECONDS_IN_HOUR * time)
