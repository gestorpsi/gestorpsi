#!/usr/bin/env python
# -*- coding: utf-8 -*-
from packages.paypal.standard.forms import PayPalStandardBaseForm
from packages.paypal.standard.pdt.models import PayPalPDT


class PayPalPDTForm(PayPalStandardBaseForm):
    class Meta:
        model = PayPalPDT