#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Copyright (C) 2008 GestorPsi
     
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

import header
from datetime import date, timedelta, datetime
from django.core.mail import EmailMessage

from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.invoice import Invoice, PaymentType
from django.conf import settings

# main code
'''
    Check all org. If org have one or more not payed invoice and overdue
    call object.save() to check. Method save check not payed invoices.
'''
s = ""

for o in Organization.objects.filter(suspension=False, organization=None):
    o.save()

    # to check if resources of chosen plan are over of limit.
    if o.active: 
        if o.prefered_plan.staff_size and o.care_professionals().count() > o.prefered_plan.staff_size or o.prefered_plan.student_size and o.get_student_().count() > o.prefered_plan.student_size:
            s += u"--- %s - %s/admin/organization/organization/%s/\n" % (o.name, settings.URL_APP, o.id)

            if o.prefered_plan.staff_size and o.care_professionals().count() > o.prefered_plan.staff_size:
                s += u"Professional %s Plan %s\n" % (o.care_professionals().count(), o.prefered_plan.staff_size)

            if o.prefered_plan.student_size and  o.get_student_().count() > o.prefered_plan.student_size:
                s += u"Student %s Plan %s\n" % (o.get_student_().count(), o.prefered_plan.student_size)

            s += u'\n'

# send email if not empty list for both
if s and settings.ADMINS_REGISTRATION:
    # sendmail
    msg = EmailMessage()
    msg.encoding = "utf-8"
    msg.subject = u"GestorPsi - orgs over of limit - %s " % datetime.today()
    msg.body = s
    msg.to = settings.ADMINS_REGISTRATION
    msg.send()

'''
    Check all invoices. If is a overdue invoice, payment way will be billet.
'''
expiry = date.today()-timedelta(1) # yesterday
for x in Invoice.objects.filter(expiry_date=expiry, status=0).exclude(payment_type=2): # overdue, is not billet.
    x.payment_type = PaymentType.objects.get(pk=2) # billet, hardcode
    x.save()
