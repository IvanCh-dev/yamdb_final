from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'


class User(AbstractUser):
    ROLES = [
        ('user', 'USER'),
        ('moderator', 'MODERATOR'),
        ('admin', 'ADMIN'),
    ]
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Логин',
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=254,
        verbose_name='Почтовый адрес',
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.TextField(
        blank=True,
        choices=ROLES,
        default='user',
        verbose_name='Текущая роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое представление модели."""
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
