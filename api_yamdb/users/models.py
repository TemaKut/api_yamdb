from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

CHOICES_ROLES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """ Переопределяем поля пользователя. """
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    password = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(
        'Роль', max_length=30,
        choices=CHOICES_ROLES, default='user'
    )
    confirmation_code = models.CharField(max_length=100, blank=True)
