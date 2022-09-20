import pytz

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Mailing(models.Model):
    date_start = models.DateTimeField(
        verbose_name='Дата начала рассылки'
    )
    date_end = models.DateTimeField(
        verbose_name='Дата конца рассылки'
    )
    time_send_start = models.TimeField(
        verbose_name='Отправить не раньше',
        blank=True
    )
    time_send_end = models.TimeField(
        verbose_name='Отправить не позже',
        blank=True
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=255
    )
    tag = models.CharField(
        verbose_name='Тег',
        max_length=100,
        blank=True
    )
    operator_code = models.CharField(
        verbose_name='Код оператора',
        max_length=3,
        blank=True
    )

    def to_send(self):
        now_date = timezone.now()
        return self.date_start <= now_date <= self.date_end

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.text[:30]}'


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone_validator = RegexValidator(
        regex=r'^7\d{10}$',
        message='Формат номера телефона: 7xxxxxxxxxx (x - цифра от 0 до 9)',
    )

    phone_number = models.CharField(
        verbose_name='Телефон',
        validators=[phone_validator],
        unique=True,
        max_length=11
    )
    operator_code = models.CharField(
        verbose_name='Код оператора',
        max_length=3,
        editable=False,
    )
    tag = models.CharField(
        verbose_name='Тег',
        max_length=100,
        blank=True
    )
    timezone = models.CharField(
        verbose_name='Часовой пояс',
        max_length=32,
        choices=TIMEZONES,
        default='UTC'
    )

    def save(self, *args, **kwargs):
        self.operator_code = str(self.phone_number)[1:4]
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.phone_number}'


class Message(models.Model):
    SENT, NO_SENT = 'Send', 'NO send'
    STATUS_CHOICES = [
        (NO_SENT, NO_SENT),
        (SENT, SENT),
    ]

    time_create = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=15,
        choices=STATUS_CHOICES,
        default=NO_SENT,
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=Mailing._meta.verbose_name
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=Client._meta.verbose_name
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('status', '-time_create')

    def __str__(self):
        return (
            f'Сообщение: {self.pk}. '
            f'Статус: {self.status}. '
            f'Получатель: {self.client}'
        )
