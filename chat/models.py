from django.db import models
from django.conf import settings

from . import StatusesAndTypes


def attachment_file_upload_to(instance, filename):
    chat = instance.message.chat
    return f'attachments/{chat.get_chat_for_path()}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.PROTECT)

    tg_id = models.IntegerField('Tg id')
    tg_hash = models.CharField('Tg hash', max_length=300)
    tg_username = models.CharField('Юзернейм тг', max_length=150)
    tg_password = models.CharField('Пароль тг', max_length=150)
    session = models.CharField('Сессия', max_length=5000)

    banned = models.BooleanField('Забанен на сервисе', default=False)

    def __str__(self):
        return f'[{self.id}]: {self.tg_username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Chat(models.Model):
    profile = models.ForeignKey('Profile', related_name='chats', on_delete=models.PROTECT)
    tg_id = models.IntegerField('Tg id')
    username = models.CharField('Юзернейм тг', max_length=150)
    firstname = models.CharField('Имя', max_length=150)
    lastname = models.CharField('Фамилия', max_length=150)

    def __str__(self):
        return f'[{self.id}]: {self.profile.tg_username} - {self.username}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        unique_together = ('profile', 'tg_id')

    def get_chat_for_path(self):
        return f'{self.username}_{self.profile.tg_username}'


class Message(models.Model):
    chat = models.ForeignKey('Chat', related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField('Отправитель', choices=[
        (StatusesAndTypes.IN, 'Входящее'),
        (StatusesAndTypes.OUT, 'Исходящие')
    ], max_length=10)
    text = models.TextField('Текст', blank=True)
    sent_date = models.DateTimeField('Время отправки', auto_now_add=True)

    def __str__(self):
        return f'[{self.id}]: {self.chat}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Attachment(models.Model):
    type = models.CharField('Тип', max_length=10, choices=[
        (StatusesAndTypes.AUDIO, 'Аудио'),
        (StatusesAndTypes.VIDEO, 'Видео'),
        (StatusesAndTypes.IMAGE, 'Картинка'),
        (StatusesAndTypes.FILE, 'Файл'),
    ])
    message = models.ForeignKey('Message', related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField('Файл', upload_to=attachment_file_upload_to)

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
