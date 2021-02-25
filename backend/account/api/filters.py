from django_filters.rest_framework import FilterSet

from account.models import BankAccount


class BankAccountFilter(FilterSet):
    class Meta:
        model = BankAccount
        fields = ('account_type', 'currency', 'current_balance', )

