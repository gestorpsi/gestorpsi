#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Check all org. If org have one or more not payed invoice
    call object.save() to check. Method save check not payed invoices.
'''

import sys
from os import environ

environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
sys.path.append('..')

from gestorpsi.organization.models import Organization 

# main code
for o in Organization.objects.filter(suspension=False, organization=None):
    o.save()
