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

from django.conf.urls.defaults import url, patterns
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.generic.simple import direct_to_template

from django.contrib.auth.decorators import login_required
from gestorpsi.authentication.views import select_organization

urlpatterns = patterns('gestorpsi.authentication.views',
    url(r'^authentication/$', 'user_authentication', name='authentication-login-form'),
    url(r'^selectorganization/$', login_required(select_organization), name='authentication-select-organization'),
    url(r'^activate/complete/$', direct_to_template, {'template': 'registration/user_registration_complete.html'}, name='user-registration-complete'),
    url(r'^password/reset/$', password_reset, name='authentication-password-reset'),
    url(r'^password/reset/done/$', password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='authentication-password-reset-done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='authentication-password-reset-confirm'),
    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'registration/password_reset_complete.html'}, name='auth_password_reset_complete'),
)
