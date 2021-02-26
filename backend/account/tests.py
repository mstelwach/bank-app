from decimal import Decimal

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from account.models import BankAccount


class BankAccountCRUDTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(email='TestEmail@test.com',
                                                         first_name='TestFirstName',
                                                         last_name='TestLastName',
                                                         password='TestPassword',
                                                         phone='TestPhone',
                                                         is_admin=True)
        self.user.save()
        self.bank_account = BankAccount.objects.create(
            user=self.user,
            account_type='BC',
            sort_code=233,
            number=43433,
            currency='PLN',
            current_balance=Decimal('500.00')
        )
        self.bank_account.save()

    def test_create_bank_account(self):
        self.assertIn(self.bank_account, BankAccount.objects.all())

    def test_read_bank_account(self):
        self.assertEqual(self.bank_account.account_type, 'BC')
        self.assertEqual(self.bank_account.sort_code, 233)
        self.assertEqual(self.bank_account.number, 43433)
        self.assertEqual(self.bank_account.currency, 'PLN')
        self.assertEqual(self.bank_account.current_balance, Decimal('500.00'))

    def test_update_bank_account_account_type(self):
        self.bank_account.account_type = 'PM'
        self.bank_account.save()
        self.assertEqual(self.bank_account.account_type, 'PM')

    def test_update_bank_account_current_balance(self):
        self.bank_account.current_balance = Decimal('400.00')
        self.bank_account.save()
        self.assertEqual(self.bank_account.current_balance, Decimal('400.00'))

    def tearDown(self) -> None:
        self.bank_account.delete()
        self.user.delete()


class BankAccountViewCRUDTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(email='TestEmail@test.com',
                                                         first_name='TestFirstName',
                                                         last_name='TestLastName',
                                                         password='TestPassword',
                                                         phone='TestPhone',
                                                         is_admin=True)
        self.user.save()

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.response = self.client.post(
            reverse('bank-account-list'),
            {'user': self.user.pk,
             'account_type': 'BC',
             'sort_code': 233,
             'number': 43433,
             'currency': 'PLN',
             'current_balance': Decimal('300.00')},
            format='json'
        )

    def test_create_view(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_read_view(self):
        bank_account = BankAccount.objects.get()
        response_bank_account_list = self.client.get(
            reverse('bank-account-list'),
            format='json'
        )
        response_bank_account_detail = self.client.get(
            reverse('bank-account-detail', kwargs={'pk': bank_account.pk}),
            format='json'
        )
        self.assertEqual(response_bank_account_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_bank_account_detail.status_code, status.HTTP_200_OK)

    # def test_update_view(self):
    #     bank_account = BankAccount.objects.get()
    #     response = self.client.put(
    #         reverse('bank-account-detail', kwargs={'pk': bank_account.pk}),
    #         {'account_type': 'PM'},
    #         format='json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_view(self):
        bank_account = BankAccount.objects.get()
        response = self.client.delete(
            reverse('bank-account-detail', kwargs={'pk': bank_account.pk}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorization_view(self):
        client = APIClient()
        response = client.post(
            reverse('bank-account-list'),
            {'user': self.user.pk,
             'account_type': 'BC',
             'sort_code': 233,
             'number': 43433,
             'currency': 'EUR',
             'current_balance': Decimal('300.00')},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self) -> None:
        self.user.delete()


class UserTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(email='TestEmail@test.com',
                                                         first_name='TestFirstName',
                                                         last_name='TestLastName',
                                                         password='TestPassword',
                                                         phone='TestPhone',
                                                         is_admin=True)
        self.user.save()

    def test_correct_user(self):
        user = authenticate(email='TestEmail@test.com', password='TestPassword')
        self.assertTrue(user is not None and user.is_authenticated)

    def test_wrong_email(self):
        user = authenticate(email='WrongEmail', password='TestPassword')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(email='TestEmail@test.com', password='WrongPassword')
        self.assertFalse(user is not None and user.is_authenticated)

    def tearDown(self) -> None:
        self.user.delete()