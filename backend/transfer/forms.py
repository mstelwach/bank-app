from django import forms
from django.core.exceptions import ValidationError

from account.models import BankAccount, User
from transfer.models import Transfer


class TransferCreateForm(forms.ModelForm):

    class Meta:
        model = Transfer
        fields = ['sender', 'receiver', 'title', 'amount', 'reference', 'method']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['sender'].queryset = BankAccount.objects.filter(user=user, currency='PLN')
            self.fields['receiver'].queryset = BankAccount.objects.exclude(user=user, currency='PLN')

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })

    def clean_amount(self):
        sender = self.cleaned_data.get('sender')
        amount = self.cleaned_data.get('amount')

        if sender and amount and amount > sender.current_balance:
            raise ValidationError("Amount too much!")
        return amount

