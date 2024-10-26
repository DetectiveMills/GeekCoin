from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView

from .models import Transactions
from .serializers import TransactionSerializer
from apps.users.models import User
from .permissions import UserPermissions
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .models import Transactions, User  
from .serializers import TransactionSerializer

class TransactionsAPIViews(GenericViewSet, 
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        from_user_id = request.data.get('from_user')
        to_user_id = request.data.get('to_user')
        amount = request.data.get('amount')

        print(f'from_user: {from_user_id}, to_user: {to_user_id}')  # Логирование

        try:
            from_user = User.objects.get(username=from_user_id)  # Используем username
            to_user = User.objects.get(username=to_user_id)

            if float(amount) > float(from_user.balance):
                return Response({'detail': 'Недостаточно средств для перевода'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            if from_user == to_user:
                return Response({'detail': 'Нельзя отправить coin самому себе'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            from_user.balance -= float(amount)
            to_user.wallet = (float(to_user.wallet) if to_user.wallet else 0) + float(amount)
            from_user.save()
            to_user.save()

            transfer = Transactions.objects.create(from_user=from_user, to_user=to_user, amount=amount)
            serializer = TransactionSerializer(transfer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist as e:
            return Response({'detail': f'Пользователь не найден: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return Response({'detail': 'Неверный формат суммы перевода'}, 
                            status=status.HTTP_400_BAD_REQUEST)


class Transactions_HistoryAPIViews(GenericViewSet, 
                           mixins.ListModelMixin):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transactions.objects.filter(from_user=user) | Transactions.objects.filter(to_user=user)

