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
from gestorpsi.careprofessional.views import index, form, list, order, save
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    (r'^$', login_check(index)),
    (r'^add/$', login_check(form)),
    (r'^page(?P<page>(\d)+)$', login_check(list)),
    (r'^deactive/$', login_check(index), {'deactive':True} ),
    (r'^page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order)),
    (r'^save/$', login_check(save)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save)),

    (r'^initial/(?P<initial>[a-z])/page(?P<page>(\d)+)/$', login_check(list)), # quick filter
    (r'^filter/(?P<filter>.*)/page(?P<page>(\d)+)/$', login_check(list)), # quick search
    (r'^filter/(?P<filter>.*)/$', login_check(list), {'no_paging': True}), # quick search

    # DEACTIVE
    (r'^initial/(?P<initial>[a-z])/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^initial/(?P<initial>[a-z])/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^filt/(?P<filter>.*)/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick search
    (r'^filt/(?P<filter>.*)/deacive/$', login_check(list), {'no_paging': True, 'deactive':True } ), # quick search
    (r'^deactive/$', login_check(index), {'deactive':True}), # list objects deactive
    (r'^page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True}), #list objects


)
