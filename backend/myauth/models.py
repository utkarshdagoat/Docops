from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator , MinValueValidator
from .manager import MyUserManager
# Create your models here


class User(AbstractBaseUser):
    username = models.CharField(
                    max_length=32
                )
    year  = models.IntegerField(
                validators=[
                    MinValueValidator(1),
                    MaxValueValidator(5)
                ]
            )
    display_picture = models.CharField(max_length=200)
    email = models.EmailField(
                verbose_name="email address",
                max_length=255,
                unique=True
            )
    password=None

    objects=MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['year']
