# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Account


class TestTransfer(TestCase):
    def get_account(self, number, inn=None, balance=0):
        username = 'user{}'.format(number)
        user = User.objects.create(username=username)
        inn = str(inn or number)
        return Account.objects.create(user=user, inn=inn, balance=balance)

    def test_available(self):
        self.assertEqual(self.client.get('/').status_code, 200)

    def check_balance(self, user, balance):
        self.assertEqual(Account.objects.get(user=user).balance, balance)

    def test_transfer(self):
        account1 = self.get_account(1, balance=100)
        account2 = self.get_account(2)
        account3 = self.get_account(3)
        account4 = self.get_account(4)
        account5 = self.get_account(5, 2)
        data = {
            'user': account1.user.pk,
            'inns': '2 3 4',
            'amount': Decimal('97.5')

        }
        # import pudb; pu.db
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, 200)
        self.check_balance(account1, Decimal('2.52'))
        self.check_balance(account2, Decimal('24.37'))
        self.check_balance(account3, Decimal('24.37'))
        self.check_balance(account4, Decimal('24.37'))
        self.check_balance(account5, Decimal('24.37'))

