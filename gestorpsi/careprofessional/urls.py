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

professional_index = {
    'template_name': 'careprofessional/careprofessional_list.html'}
professional_list_deactive = {'deactive': True}
professional_form = {
    'template_name': 'careprofessional/careprofessional_form.html'}

student_index = {'template_name': 'careprofessional/student_list.html'}
student_index_deactive = {
    'template_name': 'careprofessional/student_list.html', 'deactive': True}
student_list = {'is_student': True}
student_list_deactive = {'is_student': True, 'deactive': True}
student_form = {
    'template_name': 'careprofessional/student_form.html', 'is_student': True}
student_save = {'is_student': True}

urlpatterns = patterns('',
    url(r'^$', login_check(index), professional_index),
    url(r'^page(?P<page>(\d)+)$', login_check(list)),
    url(r'^deactive/$', login_check(index), professional_list_deactive),
    url(r'^page(?P<page>(\d)+)/deactive/$', login_check(list),
        professional_list_deactive),
    url(r'^add/$', login_check(form), professional_form),
    url(r'^save/$', login_check(save)),
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form), professional_form, name='professional_form'),  # noqa
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save)),  # noqa
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order), name='professional_order'),  # noqa
    url(r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$',
        login_check(list)),
    url(r'^initial/(?P<initial>[a-zA-Z])/deactive/$', login_check(list),
        {'deactive': True}),
    url(r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/deactive/$',
        login_check(list), professional_list_deactive),
    url(r'^filter/(?P<filter>\w+)/$', login_check(list)),
    url(r'^filter/(?P<filter>\w+)/page(?P<page>(\d)+)/$', login_check(list)),
    url(r'^filter/(?P<filter>\w+)/deactive/$',
        login_check(list), {'no_paging': True, 'deactive': True}),
    url(r'^filter/(?P<filter>\w+)/page(?P<page>(\d)+)/deactive/$',
        login_check(list), {'deactive': True}),
    url(r'^student/$', login_check(index), student_index),
    url(r'^student/page(?P<page>(\d)+)$', login_check(list), student_list),
    url(r'^student/deactive/$', login_check(index), student_index_deactive),
    url(r'^student/page(?P<page>(\d)+)/deactive/$', login_check(list),
        student_list_deactive),
    url(r'^student/add/$', login_check(form), student_form),
    url(r'^student/save/$', login_check(save), student_save),
    url(r'^student/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form), student_form, name='student_form'),  # noqa
    url(r'^student/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save), student_save),  # noqa
    url(r'^student/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order), student_save, name='student_order'),  # noqa
    url(r'^student/initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$',
        login_check(list), student_list),
    url(r'^student/initial/(?P<initial>[a-zA-Z])/deactive/$',
        login_check(list), student_list_deactive),
    url(r'^student/initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/deactive/$', login_check(list), student_list_deactive),  # noqa
    url(r'^student/filter/(?P<filter>\w+)/$', login_check(list), student_list),
    url(r'^student/filter/(?P<filter>\w+)/page(?P<page>(\d)+)/$',
        login_check(list), student_list),
    url(r'^student/filter/(?P<filter>\w+)/deactive/$',
        login_check(list), student_list_deactive),
    url(r'^student/filter/(?P<filter>\w+)/page(?P<page>(\d)+)/deactive/$',
        login_check(list), student_list_deactive),
)
