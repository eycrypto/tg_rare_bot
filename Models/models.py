from datetime import datetime

from django.db import models


class Rare(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название редкости')

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.CharField(max_length=2 ** 13, verbose_name='Текст сообщения')
    rare = models.ForeignKey('Rare', on_delete=models.CASCADE, verbose_name='Редкость')



class API(models.Model):
    username = models.CharField(max_length=64, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=64, verbose_name='Номер телефона(должн начинаться с +')
    api_id = models.CharField(max_length=16, verbose_name='id API Telegram')
    api_hash = models.CharField(max_length=64, verbose_name='hash API Telegram')
    last_send_message = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки последнего сообщения')
    can_send_message = models.BooleanField(default=True, verbose_name='Можно ли отправить сообщение')
    is_activate = models.BooleanField(default=False, verbose_name='Активирована ли сессия')

    def has_24_hours_passed(self):
        time_difference = (datetime.now()-self.last_send_message.replace(tzinfo=None))
        return time_difference.total_seconds() > 24 * 60 * 60



class System(models.Model):
    min = models.PositiveIntegerField(default=50, verbose_name='Минимальная частота отправки сообщений')
    max = models.PositiveIntegerField(default=150, verbose_name='Максимальная частота отправки сообщений')

class SendMessage(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Отправленое сообщение')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки сообщения')
