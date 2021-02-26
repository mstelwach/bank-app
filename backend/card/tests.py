from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from account.models import BankAccount
from card.models import Card


class CardCRUDTest(TestCase):

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
        self.card = Card.objects.create(
            account=self.bank_account,
            number='1234432112344321',
            code='080',
            pin=5050
        )
        self.card.save()

    def test_create_card(self):
        self.assertIn(self.card, Card.objects.all())

    def test_read_card(self):
        self.assertEqual(self.card.number, '1234432112344321')
        self.assertEqual(self.card.code, '080')
        self.assertEqual(self.card.pin, 5050)

    def test_update_card_daily_online_limit(self):
        self.card.daily_online_limit = 3000
        self.card.save()
        self.assertEqual(self.card.daily_online_limit, 3000)

    def test_update_card_daily_withdrawal_limit(self):
        self.card.daily_withdrawal_limit = 4000
        self.card.save()
        self.assertEqual(self.card.daily_withdrawal_limit, 4000)

    def test_update_card_monthly_online_limit(self):
        self.card.monthly_online_limit = 5000
        self.card.save()
        self.assertEqual(self.card.monthly_online_limit, 5000)

    def test_update_card_monthly_withdrawal_limit(self):
        self.card.monthly_withdrawal_limit = 6000
        self.card.save()
        self.assertEqual(self.card.monthly_withdrawal_limit, 6000)

    def tearDown(self) -> None:
        self.user.delete()
        self.bank_account.delete()
        self.card.delete()


class CardViewCRUDTest(TestCase):

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

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.response = self.client.post(
            reverse('card-list'),
            {
                'account': self.bank_account.pk,
                'number': '1234432112344321',
                'code': '080',
                'pin': 5050
            },
            format='json'
        )

    def test_create_view(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_read_view(self):
        card = Card.objects.get()
        response_card_list = self.client.get(
            reverse('card-list'),
            format='json'
        )
        response_card_detail = self.client.get(
            reverse('card-detail', kwargs={'pk': card.pk}),
            format='json'
        )
        self.assertEqual(response_card_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_card_detail.status_code, status.HTTP_200_OK)

    # def test_update_view(self):
    #     card = Card.objects.get()
    #     response = self.client.put(
    #         reverse('card-detail', kwargs={'pk': card.pk}),
    #         {
    #             'daily_online_limit': 4000,
    #             'daily_withdrawal_limit': 5000,
    #             'monthly_online_limit': 6000,
    #             'monthly_withdrawal_limit': 7000
    #         },
    #         format='json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_view(self):
        card = Card.objects.get()
        response = self.client.delete(
            reverse('card-detail', kwargs={'pk': card.pk}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorization_view(self):
        client = APIClient()
        response = client.post(
            reverse('bank-account-list'),
            {
                'account': self.user.pk,
                'number': '1234432112344321',
                'code': '080',
                'pin': 5050
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self) -> None:
        self.bank_account.delete()
        self.user.delete()
