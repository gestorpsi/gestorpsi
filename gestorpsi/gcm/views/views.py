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
from gestorpsi.boleto.models import *
from gestorpsi.boleto.admin import *
from django.utils.translation import ugettext as _

from gestorpsi.gcm.models import Plan

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



def billet_config(request):
    dados = BradescoBilletData.objects.all()[0]        
    if request.method == 'POST':
        form = BradescoBilletDataAdminForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message= _('Successfully updated.'))
        else:
            request.user.message_set.create(message= _('Correct the errors bellow.'))
    else:
        form = BradescoBilletDataAdminForm(instance=dados)
        
    return render_to_response('gcm/billet_config.html', locals(), context_instance=RequestContext(request))


def update_organization(request):  
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message= _('Successfully updated.'))
        else:
            request.user.message_set.create(message= _('Correct the errors bellow.'))
    else:
        form = OrganizationForm(instance=dados)
    
    #plan = request.POST.get('prefered_plan')
    #request.POST['prefered_plan'] = Plan.objects.get(pk=plan)
    
    return generic_object_list(request, *args, **kwargs)



