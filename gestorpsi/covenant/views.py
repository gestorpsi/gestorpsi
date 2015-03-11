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

import string
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.core.paginator import Paginator

from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.covenant.models import Covenant, CATEGORY, CHARGE
from gestorpsi.covenant.forms import CovenantForm
from gestorpsi.service.models import Service

from gestorpsi.settings import PAGE_RESULTS #DEBUG, MEDIA_URL, MEDIA_ROOT

from decimal import Decimal

"""
    Tiago de Souza Moraes
    tiago @ futuria com br
    13 11 2014
"""

def index(request, active=True):
    """
        covenant index, show all objects, list.
    """
    list_url_base = '/covenant/list/deactive/' if not active else '/covenant/list/active/'

    return render_to_response('covenant/covenant_index.html',
        {
            'all' : True,
            'list_url_base': list_url_base,
        },
        context_instance=RequestContext(request)
    )



def form(request, obj=False):
    """
        covenant form, update or save new
        obj: Covenant.id
    """

    add = False

    if obj: # update register
        obj = get_object_or_404(Covenant, pk=obj)
    else:
        add = True

    if request.POST:

        # new
        if not obj:
            obj = Covenant()

        # update or new
        obj.organization = request.user.get_profile().org_active
        obj.name = request.POST.get('name')
        obj.active = True if request.POST.get('active') else False
        obj.category = request.POST.get('category')
        obj.deadline = request.POST.get('deadline')
        obj.charge = request.POST.get('charge')
        obj.payment_way = request.POST.getlist('payment_way')

        if request.POST.get('event_time'):
            obj.event_time = request.POST.get('event_time')
        
        obj.price = request.POST.get('price')
        obj.description = request.POST.get('description')

        obj.save()
        messages.success(request, _(u'Salvo com sucesso!'))
        return HttpResponseRedirect('/covenant/%s/' % obj.id )

    # mount form
    else:
        if obj:
            form = CovenantForm( instance=obj )
        else:
            form = CovenantForm()
            obj = Covenant()

    return render_to_response('covenant/covenant_form.html',
                                {
                                    'form': form,
                                    'obj': obj,
                                    'add': add,
                                    'category': CATEGORY,
                                    'charge': CHARGE
                                },
                                context_instance=RequestContext(request)
    )




def list_json(request, active=True):
    """
        return object list in json format
        service: Service.id
    """

    list_url_base = '/covenant/list/deactive/' if not active else '/covenant/list/active/'

    if active:
        obj_list = Covenant.objects.filter(active=True, organization=request.user.get_profile().org_active)
    else:
        obj_list = Covenant.objects.filter(active=False, organization=request.user.get_profile().org_active)

    # filters
    url_extra = ''

    initial = request.GET.get('initial')
    if initial:
        obj_list = obj_list.filter(name__startswith=initial).distinct()
        url_extra += '&initial=%s' % initial

    service = request.GET.get('service')
    if service:
        obj_list = obj_list.filter(service__id=service).distinct()
        url_extra += '&service=%s' % service

    search = request.GET.get('search')
    if search:
        obj_list = obj_list.filter(name__icontains = search)
        url_extra += '&search=%s' % search

    # paginator result
    p = Paginator(obj_list, PAGE_RESULTS)
    page_number = 1 if not request.GET.get('page') else request.GET.get('page')
    page = p.page(page_number)
    object_list = page.object_list

    # mount page
    service_list = Service.objects.filter( active=True, organization=request.user.get_profile().org_active )
    initials = string.uppercase

    return render_to_response('tags/list_item_covenant.html', locals(), context_instance=RequestContext(request))



"""
    Tiago de Souza Moraes - 06/05/2014
    retrn: JSON or HTML
    search person family return JSON
    search client/initial letter return HTML
"""
@permission_required_with_403('client.client_list')
def list(request, page=1, initial=None, filter=None, no_paging=False, deactive=False, retrn=False):

    user = request.user
    object_list = Client.objects.from_user(user, 'deactive' if deactive else 'active')

    """
        return json
    """
    if retrn == 'json':

        person = {}
        i = 0

        for c in object_list.filter(person__name__icontains=filter):
            person[i] = {
                'id': c.id, # client id
                'name': c.person.name,
            }
            i = i + 1

        return HttpResponse(simplejson.dumps(person, encoding = 'iso8859-1'), mimetype='application/json')

    """
        return default
        client index / paginator
    """
    list_url_base = '/client/list/' if not deactive else '/client/list/deactive/'

    url_extra = ''
    initial = ''

    if request.GET.get('initial'):
        initial = request.GET.get('initial')
        
        if ord(initial) < 90:
            initial_next = chr(ord(initial) + 1)

        if ord(initial) > 65:
            initial_prev = chr(ord(initial) - 1)

        object_list = object_list.filter(person__name__istartswith = initial)
        url_extra += '&initial=%s' % initial

    if request.GET.get('search'):
        search = request.GET.get('search')
        object_list = object_list.filter(person__name__icontains = search)
        url_extra += '&search=%s' % search

    # filters
    if request.GET.get('service'):
        service = request.GET.get('service')
        object_list = object_list.filter(referral__service=service).distinct()
        url_extra += '&service=%s' % service
    
    client_service_pk_list = []

    # subscribed
    subscribed = True if request.GET.get('subscribed') == 'true' else False
    if subscribed:
        if not request.GET.get('service'):
            object_list = object_list.filter(referral__service__isnull=False).distinct()
        else:
            for c in object_list:
                for r in c.referrals_charged():
                    if r.service.pk == request.GET.get('service') and c.pk not in client_service_pk_list:
                        client_service_pk_list.append(c.pk)
                        break
        
        url_extra += '&subscribed=%s' % subscribed
    

    # discharged
    discharged = True if request.GET.get('discharged') == "true" else False
    if discharged:
        if not request.GET.get('service'):
            object_list = object_list.filter(referral__referraldischarge__isnull=False).distinct()
        else:
            for c in object_list:
                for r in c.referrals_discharged():
                    if r.service.pk == request.GET.get('service') and c.pk not in client_service_pk_list:
                        client_service_pk_list.append(c.pk)
                        break

        url_extra += '&discharged=%s' % discharged


    # queued
    queued = True if request.GET.get('queued') == "true" else False
    if queued:
        queued = request.GET.get('queued')
        object_list = object_list.filter(referral__queue__isnull=False).distinct()
            
        url_extra += '&queued=%s' % queued


    # nooccurrences
    nooccurrences = True if request.GET.get('nooccurrences') == "true" else False
    if nooccurrences:
        nooccurrences = request.GET.get('nooccurrences')
        object_list = object_list.filter(referral__occurrence__isnull=True).distinct()
        url_extra += '&nooccurrences=%s' % nooccurrences


    # service filter
    if client_service_pk_list: # exclude filtered for charged and discharged results
        object_list = object_list.filter(pk__in=client_service_pk_list)
    

    # paginator result
    p = Paginator(object_list, PAGE_RESULTS)
    page_number = 1 if not request.GET.get('page') else request.GET.get('page')
    page = p.page(page_number)
    object_list = page.object_list
    

    # mount page
    service_list = Service.objects.filter( active=True, organization=request.user.get_profile().org_active )
    initials = string.uppercase

    return render_to_response('tags/list_item.html', locals(), context_instance=RequestContext(request))
