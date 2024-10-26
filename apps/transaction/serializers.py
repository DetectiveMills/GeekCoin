from rest_framework import serializers
from .models import Transactions
from apps.users import models as model
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('from_user', 'to_user', 'is_complated', 'created', 'amount')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Replace 'from_user' and 'to_user' id with username
        from_user_id = representation.get('from_user')
        to_user_id = representation.get('to_user')

        if from_user_id:
            from_user = model.User.objects.get(id=from_user_id)
            representation['from_user'] = from_user.username

        if to_user_id:
            to_user = model.User.objects.get(id=to_user_id)
            representation['to_user'] = to_user.username

        return representation
    
    def create(self, validated_data):
        # Extract 'user' from validated_data
        user = validated_data.pop('user', None)

        # Create the Transactions instance without the 'user' field
        transaction = Transactions.objects.create(**validated_data)

        # If 'user' is provided, set it separately
        if user:
            transaction.user = user
            transaction.save()

        return transaction


   