from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_email_verified=models.BooleanField(default=False)
    hide_email=models.BooleanField(default=False)