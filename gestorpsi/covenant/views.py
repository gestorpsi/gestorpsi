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
from gestorpsi.financial.models import PaymentWay

from gestorpsi.settings import PAGE_RESULTS #DEBUG, MEDIA_URL, MEDIA_ROOT

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
    tab = 'deactive' if not active else 'active'

    return render_to_response('covenant/covenant_index.html',
        {
            'tab' : tab,
            'list_url_base': list_url_base,
        },
        context_instance=RequestContext(request)
    )



def form(request, obj=False):
    """
        covenant form, update or save new
        obj: Covenant.id
    """
    tab = 'form' # new register

    # all services
    service_list = Service.objects.filter( active=True, organization=request.user.get_profile().org_active)

    if obj: # update register

        tab = 'edit' # edit register
        obj = get_object_or_404(Covenant, pk=obj)

        # individual services
        if obj.charge > 1:
            service_list = Service.objects.filter(is_group=False, active=True, organization=request.user.get_profile().org_active)

    if request.POST:

        # new
        if not obj:
            form = CovenantForm(request.POST)
        else:
            form = CovenantForm(request.POST, instance=obj)

        if form.is_valid():
            # update or new
            obj = form.save(commit=False) # A org is required
            obj.organization = request.user.get_profile().org_active
            obj.save() # save before add services

            # add services
            obj.service_set.clear() # remove all
            for x in request.POST.getlist('services'): # add selected
                obj.service_set.add( Service.objects.get(pk=x) )

            # payment way
            obj.payment_way.clear() # remove all
            for x in request.POST.getlist('payment_way'):
                obj.payment_way.add( PaymentWay.objects.get(pk=x) )

            obj.save() # update

            messages.success(request, _(u'Salvo com sucesso!'))
            return HttpResponseRedirect('/covenant/%s/' % obj.id )

        else:
            messages.error(request, _(u'Erro no preenchimento do campo'))
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
                                    'tab': tab,
                                    'category': CATEGORY,
                                    'charge': CHARGE,
                                    'service_list': service_list,
                                },
                                context_instance=RequestContext(request)
    )



def list_json(request, service=False, obj=False, order=False):
    '''
        return json
        return all covenant when choosen a service in referral client form, subscription a service.

        service : Service.id
        obj: Covenant.id

        order: string. 'all' or 'group'
            group: All active covenant for a group, by event.
            all: All active covenants
    '''
    c = 0
    covenant = {} # json

    # return all active covenant for a group
    if order == 'group':
        for o in Covenant.objects.filter(charge=1, active=True, organization=request.user.get_profile().org_active):
            covenant[c] = {
                'id': o.id,
                'name': u'%s' % o.name,
                'price': u'%s' % o.price,
                'charge': u'%s' % o.get_charge_display(),
                'events': u'%s' % o.event_time,
            }
            c += 1

    # return all active covenants
    if order == 'all':
        for o in Covenant.objects.filter(active=True, organization=request.user.get_profile().org_active):
            covenant[c] = {
                'id': o.id,
                'name': u'%s' % o.name,
                'price': u'%s' % o.price,
                'charge': u'%s' % o.get_charge_display(),
                'events': u'%s' % o.event_time,
            }
            c += 1

    # return all covenant of a service
    if service:
        for o in Covenant.objects.filter(active=True, organization=request.user.get_profile().org_active, service__id=service):
            covenant[c] = {
                'id': o.id,
                'name': u'%s' % o.name,
                'price': u'%s' % o.price,
                'charge': u'%s' % o.get_charge_display(),
                'events': u'%s' % o.event_time,
            }
            c += 1

    # get Covenant and return informations
    if obj:
        for o in Covenant.objects.filter(organization=request.user.get_profile().org_active, pk=obj):

            # mount html checkbox
            payment = ''
            for x in o.payment_way.all():
                payment += '<li><label><input type="checkbox" value="%s" name="TEMPID999FORM-pw" class="small" />&nbsp;%s</label></li>' % (x.id, x.name)

            covenant[c] = {
                'id': o.id,
                'name': u'%s' % o.name,
                'price': u'%s' % o.price,
                'charge': u'%s' % o.get_charge_display(),
                'events': u'%s' % o.event_time,
                'payment_way':u'%s' % payment,
            }
            c += 1

    return HttpResponse(simplejson.dumps(covenant, encoding = 'iso8859-1'), mimetype='application/json')



def list_filter(request, active=True):
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

        # next and previus letter
        if ord(initial) < 90:
            initial_next = chr(ord(initial) + 1)

        if ord(initial) > 65:
            initial_prev = chr(ord(initial) - 1)

    service = request.GET.get('service')
    if service:
        obj_list = obj_list.filter(service__id=service).distinct()
        url_extra += '&service=%s' % service

    search = request.GET.get('search')
    if search:
        obj_list = obj_list.filter(name__icontains = search)
        url_extra += '&search=%s' % search
    else:
        search = ''

    # paginator result
    p = Paginator(obj_list, PAGE_RESULTS)
    page_number = 1 if not request.GET.get('page') else request.GET.get('page')
    page = p.page(page_number)
    object_list = page.object_list

    # mount page
    service_list = Service.objects.filter( active=True, organization=request.user.get_profile().org_active )
    initials = string.uppercase

    return render_to_response('tags/list_item_covenant.html', locals(), context_instance=RequestContext(request))



def order(request, obj=False):
    """
        active or deactive a covenant
    """
    if obj:

        obj = get_object_or_404(Covenant, pk=obj)

        if obj.active:
            obj.active = False
            messages.success(request, _(u'Convênio desativado com sucesso!'))
        else:
            obj.active = True
            messages.success(request, _(u'Convênio ativado com sucesso!'))

        obj.save()
        return HttpResponseRedirect('/covenant/%s/' % obj.id )

    return False
