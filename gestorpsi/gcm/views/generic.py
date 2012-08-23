# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi
"""

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.views.generic.list_detail import object_list as generic_object_list
from django.views.generic.list_detail import object_detail as generic_object_detail
from django.views.generic.create_update import create_object as generic_create_object
from django.views.generic.create_update import update_object as generic_update_object
from django.views.generic.create_update import delete_object as generic_delete_object
from django.views.generic.simple import direct_to_template as generic_direct_to_template

from gestorpsi.organization.models import Organization
from gestorpsi.organization.forms import OrganizationForm


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

def update_invoice_wrapper(request, object_id, *args, **kwargs):
    data = request.POST
    org_id = data.get('organization')

    from django.core.urlresolvers import reverse
    from datetime import datetime
    redirect_to = reverse('org-update', args={org_id:''})    
    kwargs['object_id'] = object_id
    kwargs['post_save_redirect'] = redirect_to

    return update_object(request, *args, **kwargs)


def update_organization_wrapper(request, object_id, *args, **kwargs):
    from django.core.urlresolvers import reverse
    from datetime import datetime
    from gestorpsi.gcm.models.plan import Plan

    redirect_to = reverse('org-update', args={object_id:''})    
    if request.method == 'POST':
        data = request.POST
        org_id = data.get('organization')
        object = Organization.objects.get(pk=org_id)  

        kwargs['object_id'] = object_id
        kwargs['post_save_redirect'] = redirect_to
            
    return update_object(request, *args, **kwargs)


def update_object(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)

    #from gestorpsi.organization.models import Organization
    #from gestorpsi.phone.models import Phone
    #p = Phone()
    #p.area = '99'
    #p.phoneNumber = '87654321'
    #p.phoneType_id = 2
    #org = Organization.objects.get(pk=kwargs['object_id'])
    #org.phones.add(p)
    #org.save()
    #raise Exception(kwargs['object_id'])
    
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
