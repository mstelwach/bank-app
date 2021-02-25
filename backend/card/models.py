from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.core.validators import MaxValueValidator
from django.db import models

from account.models import BankAccount


class Card(models.Model):
    account = models.OneToOneField(BankAccount, on_delete=models.CASCADE, related_name='card')
    is_active = models.BooleanField(default=False)
    number = CardNumberField('card number')
    expires_date = CardExpiryField('expiration date', default='01/25')
    code = SecurityCodeField('security code')
    pin = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    daily_online_limit = models.PositiveIntegerField(blank=True, null=True, default=2000)
    daily_withdrawal_limit = models.PositiveIntegerField(default=2000)
    monthly_online_limit = models.PositiveIntegerField(default=5000)
    monthly_withdrawal_limit = models.PositiveIntegerField(default=5000)

    def __str__(self):
        return 'Card account: {}'.format(self.account)
