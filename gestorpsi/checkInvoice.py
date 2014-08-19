#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import environ

environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
sys.path.append('..')

from gestorpsi.organization.models import Organization 

# main code
for o in Organization.objects.filter(suspension=False, organization=None):

    # all overdue invoice
    for x in o.invoice_()[2]:
        if x.status == 0 : # not payed
            o.active = False
            o.save()
            break # one invoice is enough to turn off the org
