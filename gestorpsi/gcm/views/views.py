# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi
"""

from django.http import HttpResponseRedirect
from django.views.generic.list_detail import object_list as generic_object_list
from django.views.generic.list_detail import object_detail as generic_object_detail
from django.views.generic.create_update import create_object as generic_create_object
from django.views.generic.create_update import update_object as generic_update_object
from django.views.generic.create_update import delete_object as generic_delete_object
from django.views.generic.simple import direct_to_template as generic_direct_to_template

from gestorpsi.organization.models import Organization

def org_object_list(request, order_by=False, *args, **kwargs):

    if order_by:
        if "order_by" in request.session:
            if request.session['order_by'].replace("-", "") == order_by:
                if request.session['order_by'].find("-") > -1:
                    request.session['order_by'] = order_by
                else:
                    request.session['order_by'] = "-" + order_by
            else:
                request.session['order_by'] = order_by
        else: 
            request.session['order_by'] = order_by

    if "order_by" in request.session:
        kwargs['queryset'] = kwargs['queryset'].order_by(request.session['order_by'])

    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)
    return generic_object_list(request, *args, **kwargs)
