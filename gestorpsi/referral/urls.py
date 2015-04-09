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
from gestorpsi.authentication.views import login_check
from gestorpsi.referral.views import referral_off, client_referrals


urlpatterns = patterns('gestorpsi.referral.views',
    (r'^client/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',  # noqa
        login_check(client_referrals)),  # MOVED TO CLIENT VIEW
    (r'^(?P<object_id>\d+)/off/$', login_check(referral_off)),
)
