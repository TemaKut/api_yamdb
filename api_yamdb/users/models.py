from django.contrib.auth.models import AbstractUser

from django.db import models

CHOICES_ROLES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль', max_length=30, choices=CHOICES_ROLES)
