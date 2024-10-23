from django.contrib import admin
from .models import Transactions

# Register your models here.
@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'is_complated', 'created', 'amount')