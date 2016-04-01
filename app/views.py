# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal, ROUND_DOWN

from django.views.generic import FormView
from django.contrib.auth.models import User
from django.db.models import F
from django.db import transaction

from .forms import TransferForm
from .models import Account


class TransferView(FormView):
    form_class = TransferForm
    template_name = 'transfer.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.cleaned_data['user']
        amount = form.cleaned_data['amount']
        inns = form.cleaned_data['inns'].split(' ')
        accounts = Account.objects.select_related('user').filter(inn__in=inns)
        accounts_count = len(accounts)
        amount_part = amount / accounts_count
        amount_part = amount_part.quantize(Decimal('.01'), rounding=ROUND_DOWN)
        amount = amount_part * accounts_count

        with transaction.atomic():
            Account.objects.filter(user__in=[x.id for x in accounts]).\
                update(balance=F('balance')+amount_part)
            Account.objects.filter(user=user).update(balance=F('balance')-amount)

        data = {
            'form': TransferForm(),
            'amount': amount,
            'amount_part': amount_part,
            'accounts': accounts,
        }
        return self.render_to_response(self.get_context_data(**data))
