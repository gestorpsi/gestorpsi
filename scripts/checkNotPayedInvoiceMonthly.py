#!/usr/bin/env python
# -*- coding: utf-8 -*-

import header
from datetime import date, timedelta

from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.invoice import Invoice, PaymentType

# main code
'''
    Check all org. If org have one or more not payed invoice and overdue
    call object.save() to check. Method save check not payed invoices.
'''
for o in Organization.objects.filter(suspension=False, organization=None):
    o.save()


'''
    Check all invoices. If is a overdue invoice, payment way will be billet.
'''
end = date.today()-timedelta(1) # yesterday
for x in Invoice.objects.filter(end_date=end, status=0).exclude(payment_type=2): # overdue, is not billet.
    x.payment_type = PaymentType.objects.get(pk=2) # billet, hardcode
    x.save()
