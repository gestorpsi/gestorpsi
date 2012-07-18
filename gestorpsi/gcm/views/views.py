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
from gestorpsi.boleto.models import *
from gestorpsi.boleto.admin import *


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

    if request.method == 'POST': # If the form has been submitted...
        form = BradescoBilletDataAdminForm(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = BradescoBilletDataAdminForm() # An unbound form

    #if not object.is_active():
    #    request.user.message_set.create(message= _('This client is not enabled.'))
    return render_to_response('gcm/billet_config.html', locals(), context_instance=RequestContext(request))
