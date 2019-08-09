from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    description = models.TextField('profile summary', null=True, blank=True)
    location = models.CharField('Location', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'CustomUser'
