# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, verbose_name='пользователь')
    inn = models.CharField('ИНН', max_length=12, null=True)
    balance = models.DecimalField('баланс', max_digits=12, decimal_places=2,
                                  default=0)