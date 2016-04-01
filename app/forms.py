# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from .models import Account


def validate_inns(value):
    parts = value.split(' ')
    inns = Account.objects.distinct().values_list('inn', flat=True).\
        filter(inn__in=parts)
    bad_inns = [inn for inn in parts if inn not in inns]
    if bad_inns:
        messages = {
            True: 'Пользователи с ИНН: {} не найдены',
            False: 'Пользователь с ИНН {} не найден'
        }
        error_message = messages[len(bad_inns) > 1].format(', '.join(bad_inns))
        raise forms.ValidationError(error_message)


class TransferForm(forms.Form):
    user = forms.ModelChoiceField(label='Пользователь',
                                  queryset=User.objects.order_by('first_name'))
    inns = forms.CharField(label='Список ИНН для перевода, разделенных пробелом',
                           validators=[validate_inns])
    amount = forms.DecimalField(label='Сумма (поделится на всех поровну)')

    def clean(self):
        cleaned_data = super(TransferForm, self).clean()
        if not cleaned_data:
            return
        user = User.objects.select_related('account').get(pk=cleaned_data['user'].pk)
        amount = cleaned_data['amount']
        if amount > user.account.balance:
            error_message = '{} не имеет достаточной суммы для перевода'
            raise forms.ValidationError(error_message.format(user))
