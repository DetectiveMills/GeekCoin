from rest_framework import serializers
from .models import Transactions
from apps.users import models 
    
class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transactions
        fields = ('from_user', 'to_user', 'is_complated', 'created', 'amount')


   