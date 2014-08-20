#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import environ

environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
sys.path.append('..')

from gestorpsi.organization.models import Organization 

# main code
for o in Organization.objects.filter(suspension=False, organization=None):
    # call method
    o.automatic_on_()
