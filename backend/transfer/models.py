from django.db import models

from account.models import BankAccount, User


class Transfer(models.Model):
    PLN = 'PLN'
    EUR = 'EUR'
    GBP = 'GBP'
    CURRENCY_TYPE = [
        (PLN, 'PLN'),
        (EUR, 'EUR'),
        (GBP, 'GBP')
    ]
    FAILED = 'FD'
    PANDING = "PG"
    COMPLETE = 'CT'
    STATUS_TYPE = [
        (FAILED, 'Failed'),
        (PANDING, 'Panding'),
        (COMPLETE, 'Complete')
    ]
    NORMAL = 'NL'
    EXPRESS = 'EX'
    METHOD_TYPE = [
        (NORMAL, 'Normal'),
        (EXPRESS, 'Express')
    ]
    sender = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='sender_transfers')
    receiver = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='receiver_transfers')
    title = models.CharField(max_length=140)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_TYPE, default=PLN)
    reference = models.CharField(max_length=40)
    status = models.CharField(max_length=2, choices=STATUS_TYPE, default=PANDING)
    method = models.CharField(max_length=2, choices=METHOD_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Sender: {} | Receiver: {} | Amount: {}'.format(self.sender.user.email,
                                                               self.receiver.user.email,
                                                               self.amount)
