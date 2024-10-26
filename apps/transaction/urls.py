from rest_framework.routers import DefaultRouter
from django.urls import path

from apps.transaction.views import TransactionsAPIViews, Transactions_HistoryAPIViews

router = DefaultRouter()

router.register('transfer', TransactionsAPIViews, 'api_transactions')
router.register('transfer_history', Transactions_HistoryAPIViews, 'api_transactions_history')



urlpatterns = [
    # path('transfer/', TransactionsAPIViews.as_view(), name='api_transfer_coins'),
    # path('transfer_history/', UserTransactionsAPIView.as_view(), name='api_history_transfer_coins'),
]

urlpatterns = router.urls