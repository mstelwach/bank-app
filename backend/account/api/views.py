from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from account.api.filters import BankAccountFilter
from account.api.serializers import BankAccountSerializer
from account.models import BankAccount


class BankAccountViewSet(ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = BankAccountFilter
    ordering_fields = ('current_balance',)

    # def get_queryset(self):
    #     return self.request.user.bank_accounts.all()


