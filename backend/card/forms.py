from django import forms

from account.models import BankAccount
from card.models import Card


class CardCreateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['account',
                  'number',
                  'code',
                  'pin',
                  'daily_online_limit',
                  'daily_withdrawal_limit',
                  'monthly_online_limit',
                  'monthly_withdrawal_limit']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = BankAccount.objects.filter(user=user, card__isnull=True)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })