from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from account.managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class BankAccount(models.Model):
    BASIC = 'BC'
    PREMIUM = 'PM'
    GOLD = 'GD'
    ACCOUNT_TYPE = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (GOLD, 'Gold')
    ]
    PLN = 'PLN'
    EUR = 'EUR'
    GBP = 'GBP'
    CURRENCY_TYPE = [
        (PLN, 'PLN'),
        (EUR, 'EUR'),
        (GBP, 'GBP')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPE, default=BASIC)
    sort_code = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_TYPE, default=PLN)
    current_balance = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return '{} | {} Account'.format(self.user, self.get_account_type_display())
