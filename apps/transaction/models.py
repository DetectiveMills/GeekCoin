from django.db import models
from apps.users.models import User

# Create your models here.

class Transactions(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'to_user')
    is_complated = models.BooleanField(default = False, verbose_name = 'Статус транзакции')
    created = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')
    amount = models.IntegerField(verbose_name = "Кол-во Coins")

    def __str__(self) -> str:
        return "Транзакция"

    class Meta:
        verbose_name = 'Транзакии'
        verbose_name_plural = "Транзакцию"