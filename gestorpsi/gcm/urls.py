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
from django.views.generic.simple import direct_to_template

from gestorpsi.gcm.forms.auth import RegistrationForm
from gestorpsi.gcm.views.views import org_object_list

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template':'gcm/index.html'}, name='gcm-index'),

    # ???
    url(r'^register/complete/$', 'gestorpsi.gcm.views.auth.complete', name='gcm-registration-complete'),
    #url(r'^register/complete/$', django_direct_to_template, {'template': 'gcm/registration_complete.html'}, name='gcm-registration-complete'),
    url(r'accounts/register/$', 'gestorpsi.gcm.views.auth.register', {'form_class': RegistrationForm, 'template_name':'gcm/registration_form.html' }, name='registration_register'),
    url(r'gcm/org/$', org_object_list, name='org-list'),
)
