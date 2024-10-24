from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(
        max_length=155,
        verbose_name="Номер телефона",
    )
    age = models.IntegerField(
        max_length=155,
        verbose_name='Возраст',
        blank = True, null= True,
    )
    direction = models.CharField(
        max_length=155,
        verbose_name='Направление',
    )
    balance = models.IntegerField(
        default=4,
        verbose_name='Коины',
        blank = True, null= True,
    )
    wallet = models.CharField(
        max_length=15,
        verbose_name='Кошелёк',
        unique=True,
        blank = True, 
        null= True,
    )

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name="Пользователи"
        verbose_name_plural="Пользователя"