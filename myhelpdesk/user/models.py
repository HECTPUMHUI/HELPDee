from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_user = models.BooleanField('Is user', default=False)