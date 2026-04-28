from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices
from django.db.models.fields import CharField

from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = 'admin', 'Admin'
        AUTHOR = 'author', 'Author'
        READER = 'reader', 'Reader'

    number = CharField(max_length=10, unique=True, null=True, blank=True)
    role = CharField(default=Role.READER, max_length=10, choices=Role.choices)

    objects = CustomUserManager()
