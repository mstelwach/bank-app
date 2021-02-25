from rest_framework.serializers import ModelSerializer

from account.models import BankAccount


class BankAccountSerializer(ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ('pk', 'user', 'account_type', 'sort_code', 'number', 'currency', 'current_balance')
