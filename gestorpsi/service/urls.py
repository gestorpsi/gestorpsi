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
from gestorpsi.service.views import select_area, index, form, save, disable, list, list_professional, order, queue, client_list_index, list_filter_covenant, group_form, group_list

urlpatterns= patterns('',
    (r'^$', login_check(index)),
    (r'^page(?P<page>(\d)+)$', login_check(list)), #list objects
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/listprofessional/$', login_check(list_professional)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order)),
    (r'^add/$', login_check(select_area)),
    (r'^add/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(select_area)),
    (r'^form/$', login_check(form)),
    (r'^form/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)),
    (r'^save/$', login_check(save)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/queue/$', login_check(queue)),

    # service group
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/group/add/$', login_check(group_form)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/group/(?P<group_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/form/$', login_check(group_form)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/group/$', login_check(group_list)),    
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/group/json/$', login_check(group_list), {'return_json':True}),
    # deactive
    (r'^deactive/$', login_check(index), {'deactive': True} ),
    (r'^page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), #list objects

    # list client - active 
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/clientlist/$', login_check(client_list_index)), # mount html client list
    url(r'initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$', login_check(list)),
    url(r'initial/(?P<initial>[a-zA-Z])/deactive/$', login_check(list), {'deactive': True}),
    url(r'initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive': True}),
    url(r'filter/(?P<filter>\w+)/$', login_check(list)),
    url(r'filter/(?P<filter>\w+)/page(?P<page>(\d)+)/$', login_check(list)),
    url(r'filter/(?P<filter>\w+)/deactive/$', login_check(list), {'deactive': True} ),
    url(r'filter/(?P<filter>\w+)/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive': True}),
    #  filter covenant form
    url(r'list/all/$', login_check(list_filter_covenant), {'alls': True} ), # all services
    url(r'list/indiv/$', login_check(list_filter_covenant), {'indiv': True} ), # just group services
)
