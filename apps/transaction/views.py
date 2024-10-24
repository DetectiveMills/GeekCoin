from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .permissions import UserPermissions
from apps.users.models import User
from .models import Transactions
from .serializers import TransactionSerializer


# Create your views here.
class TransactionsAPIViews(CreateAPIView):
    serializer_class = TransactionSerializer

    def post(self, request):
        from_user_id = request.data.get('from_user')
        to_user_id = request.data.get('to_user')
        amount = request.data.get('amount')
        try:
            from_user = User.objects.get(id=from_user_id)
            to_user = User.objects.get(id=to_user_id)
            if float(amount) > float(from_user.balance):
                return Response({'detail': 'Недостаточно средств для перевода'}, status=status.HTTP_400_BAD_REQUEST)
            if from_user == to_user:
                return Response({'detail': 'Нельзя отправить coin самому себе'}, status=status.HTTP_400_BAD_REQUEST)
            from_user.balance = float(from_user.balance) - float(amount)
            to_user.wallet = float(to_user.balance) + float(amount)
            from_user.save()
            to_user.save()
            transfer = Transactions.objects.create(from_user=from_user, to_user=to_user, amount=amount)
            serializer = TransactionSerializer(transfer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'Неверный формат суммы перевода'}, status=status.HTTP_400_BAD_REQUEST)

class UserTransactionsAPIView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Transactions.objects.filter(from_user=user) | Transactions.objects.filter(to_user=user)

