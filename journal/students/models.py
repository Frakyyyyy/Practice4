import os
import uuid
from django.db import models
from django.conf import settings


def avatar_upload_to(instance, filename):
    """Уникальное имя: <uuid>.<расширение>."""
    ext = os.path.splitext(filename)[1].lower()
    return f'avatars/{uuid.uuid4().hex}{ext}'


class Group(models.Model):
    name = models.CharField('Название группы', max_length=100, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    surname = models.CharField('Фамилия', max_length=100)
    name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='students'
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='student',
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to=avatar_upload_to,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'.strip()