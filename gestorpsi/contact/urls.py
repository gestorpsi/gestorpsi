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
from gestorpsi.contact.views import index, list, save_mini, save_mini_professional
from gestorpsi.contact.views import contact_organization_form, contact_professional_form
from gestorpsi.contact.views import contact_organization_save, contact_professional_save
from gestorpsi.contact.views import contact_organization_order, contact_professional_order
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    (r'^$', login_check(index)),
    (r'^page(?P<page>(\d)+)$', login_check(list)), #list objects
    (r'^initial/(?P<initial>[a-z])/page(?P<page>(\d)+)/$', login_check(list)), # quick filter
    (r'^filter/(?P<filter>.*)/page(?P<page>(\d)+)/$', login_check(list)), # quick search
    (r'^form/organization/$', login_check(contact_organization_form)), # add form
    (r'^form/professional/$', login_check(contact_professional_form)), # add form
    (r'^form/organization/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(contact_organization_form)), # edit form
    (r'^form/professional/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(contact_professional_form)), # edit form
    (r'^organization/save/$', login_check(contact_organization_save)), #save organization
    (r'^professional/save/$', login_check(contact_professional_save)), #save professional
    (r'^organization/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(contact_organization_save)),  #save organization
    (r'^professional/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(contact_professional_save)),  #save professional
    (r'^save_mini/$', login_check(save_mini)), #save new object
    (r'^save_mini_professional/$', login_check(save_mini_professional)), #save new object
    (r'^organization/order/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(contact_organization_order)),
    (r'^professional/order/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(contact_professional_order)),
)
