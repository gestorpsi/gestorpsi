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
from gestorpsi.device.views import index, form, save, save_device, index_type, form_type, list, list_types, order
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    url(r'^$', login_check(index), name='device-index'), # list objects
    (r'^page(?P<page>(\d)+)$', login_check(list)), #list objects
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)), # edit object form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order)), # edit object form
    (r'^add/$', login_check(form)), # new object form
    #(r'^add/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)), # edit object form
    (r'^save/$', login_check(save)), # save new object
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save)), # update object
    (r'^save_device/$', login_check(save_device)), # save device from device_mini form
    (r'^type/$', login_check(index_type)), # list types
    (r'^type/page(?P<page>(\d)+)$', login_check(list_types)), #list type objects
    (r'^type/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form_type)), # edit type form
    (r'^type/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save_device)), # save type

    (r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$', login_check(list)), # quick filter
    (r'^filter/(?P<filter>[a-zA-Z ]+)/page(?P<page>(\d)+)/$', login_check(list)), # quick search
    (r'^filter/(?P<filter>[a-zA-Z ]+)/$', login_check(list), {'no_paging': True}), # quick search

    # DEACTIVE
    (r'^initial/(?P<initial>[a-z])/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^initial/(?P<initial>[a-z])/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^filter/(?P<filter>[a-zA-Z ]+)/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick search
    (r'^filter/(?P<filter>[a-zA-Z ]+)/deactive/$', login_check(list), {'no_paging': True, 'deactive':True } ), # quick search
    (r'^deactive/$', login_check(index), {'deactive':True}), # list objects deactive
    (r'^page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True}), #list objects
)
