from rest_framework.routers import DefaultRouter
from django.urls import path

from apps.transaction.views import TransactionsAPIViews, UserTransactionsAPIView

urlpatterns = [
    path('transfer/', TransactionsAPIViews.as_view(), name='api_transfer_coins'),
    path('transfer_history/', UserTransactionsAPIView.as_view(), name='api_history_transfer_coins'),
]
