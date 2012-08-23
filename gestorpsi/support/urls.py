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

from django.conf.urls.defaults import *
from gestorpsi.support.views import ticket_form
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    (r'^ticket/form/$', login_check(ticket_form)), #form
    (r'^ticket/sent/$', 'django.views.generic.simple.direct_to_template', {'template': 'support/ticket_sent.html'}), #form sent
)
