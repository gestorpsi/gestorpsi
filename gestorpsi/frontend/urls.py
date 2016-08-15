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
from gestorpsi.frontend.views import start
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    url(r'^$', login_check(start), name='frontend-home'), #list objects
    #url(r'^(?P<month>\d+)/month/$', login_check(start), name="frontend-month"), # list objects
    #(r'^page(?P<page>(\d)+)$', login_check(list)), #list objects
    #(r'^add/$', login_check(form)), #new object form
    #(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)),
    #(r'^save/$', login_check(save)), #save new object
    #(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save)),  #update object
    #(r'^(?P<object_id>\d+)/delete/$', login_check(delete)), # delete object
    #(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/delete/$', login_check(delete)),  #delete object
    #(r'^print/$', login_required(print_list)), # print client list
    #(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/print/$', login_required(print_record)),  # print record
)
