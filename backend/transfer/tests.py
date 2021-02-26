from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from account.models import BankAccount
from transfer.models import Transfer


class TransferCRUDTest(TestCase):

    def setUp(self) -> None:
        self.user_sender = get_user_model().objects.create_user(email='TestSenderEmail@test.com',
                                                                first_name='TestSenderFirstName',
                                                                last_name='TestSenderLastName',
                                                                password='TestSenderPassword',
                                                                phone='TestSenderPhone')

        self.user_receiver = get_user_model().objects.create_user(email='TestReceiverEmail@test.com',
                                                                  first_name='TestReceiverFirstName',
                                                                  last_name='TestReceiverLastName',
                                                                  password='TestReceiverPassword',
                                                                  phone='TestReceiverPhone')
        self.user_sender.save()
        self.user_receiver.save()

        self.bank_account_sender = BankAccount.objects.create(
            user=self.user_sender,
            account_type='BC',
            sort_code=233,
            number=43433,
            currency='PLN',
            current_balance=Decimal('500.00')
        )
        self.bank_account_receiver = BankAccount.objects.create(
            user=self.user_receiver,
            account_type='BC',
            sort_code=2335,
            number=4343444,
            currency='PLN',
            current_balance=Decimal('1000.00')
        )

        self.bank_account_sender.save()
        self.bank_account_receiver.save()

        self.transfer = Transfer.objects.create(
            sender=self.bank_account_sender,
            receiver=self.bank_account_receiver,
            title='TestTitle',
            amount=Decimal('50000.00'),
            reference='TestReference',
            method='NL'
        )
        self.transfer.save()

    def test_create_transfer(self):
        self.assertIn(self.transfer, Transfer.objects.all())

    def test_read_transfer(self):
        self.assertEqual(self.transfer.title, 'TestTitle')
        self.assertEqual(self.transfer.amount, Decimal('50000.00'))
        self.assertEqual(self.transfer.reference, 'TestReference')
        self.assertEqual(self.transfer.method, 'NL')

    def tearDown(self) -> None:
        self.user_sender.delete()
        self.user_receiver.delete()
        self.bank_account_sender.delete()
        self.bank_account_receiver.delete()
        self.transfer.delete()


class TransferViewCRUDTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(email='TestEmail@test.com',
                                                         first_name='TestFirstName',
                                                         last_name='TestLastName',
                                                         password='TestPassword',
                                                         phone='TestPhone',
                                                         is_admin=True)

        self.user_sender = get_user_model().objects.create_user(email='TestSenderEmail@test.com',
                                                                first_name='TestSenderFirstName',
                                                                last_name='TestSenderLastName',
                                                                password='TestSenderPassword',
                                                                phone='TestSenderPhone')

        self.user_receiver = get_user_model().objects.create_user(email='TestReceiverEmail@test.com',
                                                                  first_name='TestReceiverFirstName',
                                                                  last_name='TestReceiverLastName',
                                                                  password='TestReceiverPassword',
                                                                  phone='TestReceiverPhone')
        self.user.save()
        self.user_sender.save()
        self.user_receiver.save()

        self.bank_account_sender = BankAccount.objects.create(
            user=self.user_sender,
            account_type='BC',
            sort_code=233,
            number=43433,
            currency='PLN',
            current_balance=Decimal('500.00')
        )
        self.bank_account_receiver = BankAccount.objects.create(
            user=self.user_receiver,
            account_type='BC',
            sort_code=2335,
            number=4343444,
            currency='PLN',
            current_balance=Decimal('1000.00')
        )

        self.bank_account_sender.save()
        self.bank_account_receiver.save()

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.response = self.client.post(
            reverse('transfer-list'),
            {
                'sender': self.bank_account_sender.pk,
                'receiver': self.bank_account_receiver.pk,
                'title': 'TestTitle',
                'amount': Decimal('50000.00'),
                'reference': 'TestReference',
                'method': 'NL'
            },
            format='json'
        )

    def test_create_view(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_read_view(self):
        transfer = Transfer.objects.get()
        response_transfer_list = self.client.get(
            reverse('transfer-list'),
            format='json'
        )
        response_transfer_detail = self.client.get(
            reverse('transfer-detail', kwargs={'pk': transfer.pk}),
            format='json'
        )
        self.assertEqual(response_transfer_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_transfer_detail.status_code, status.HTTP_200_OK)

    def test_delete_view(self):
        transfer = Transfer.objects.get()
        response = self.client.delete(
            reverse('transfer-detail', kwargs={'pk': transfer.pk}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorization_view(self):
        client = APIClient()
        response = client.post(
            reverse('transfer-list'),
            {
                'sender': self.bank_account_sender.pk,
                'receiver': self.bank_account_receiver.pk,
                'title': 'TestTitle',
                'amount': Decimal('50000.00'),
                'reference': 'TestReference',
                'method': 'NL'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self) -> None:
        self.user.delete()
        self.user_sender.delete()
        self.user_receiver.delete()
        self.bank_account_sender.delete()
        self.bank_account_receiver.delete()
