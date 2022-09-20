from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Mailing, Client, Message
from .serializers import MailingSerializer, ClientSerializer, MessageSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        get_object_or_404(Mailing, pk=pk)
        messages_qs = Message.objects.filter(mailing_id=pk)
        serializer = MessageSerializer(messages_qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def fullinfo(self, request):
        total_count = Mailing.objects.count()
        mailings = Mailing.objects.values('id')
        content = {
            'Total number of mailings': total_count,
            'The number of messages sent': '',
        }
        result = {}

        for mailing in mailings:
            message = Message.objects.filter(mailing_id=mailing['id'])
            mailing_result = {
                'Total messages': 0,
                Message.SENT: 0,
                Message.NO_SENT: 0
            }
            count_sent = message.filter(status=Message.SENT).count()
            count_no_sent = message.filter(status=Message.NO_SENT).count()

            mailing_result['Total messages'] = len(message)
            mailing_result[Message.SENT] = count_sent
            mailing_result[Message.NO_SENT] = count_no_sent

            result[mailing['id']] = mailing_result

        content['The number of messages sent'] = result
        return Response(content)
