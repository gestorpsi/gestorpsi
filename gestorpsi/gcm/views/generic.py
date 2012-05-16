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

def object_list(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)
    return generic_object_list(request, *args, **kwargs)

def object_detail(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)
    return generic_object_detail(request, *args, **kwargs)

def create_object(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)
    return generic_create_object(request, *args, **kwargs)

def update_object(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)
    return generic_update_object(request, *args, **kwargs)

def delete_object(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)
    #if request.POST:
        #print kwargs
        #if kwargs['model']._meta.app_label == 'organization':
            #o = kwargs['model'].objects.get(pk=kwargs['object_id'])
            #for i in o.person_set.all():
                #i.profile.user.delete()
                #i.profile.delete()
                #i.delete()
            #o.care_professionals().delete()
            #print o
            #0/0
    return generic_delete_object(request, *args, **kwargs)

def direct_to_template(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)
    return generic_direct_to_template(request, *args, **kwargs)
