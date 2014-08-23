# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi
"""

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q

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

def org_object_list(request):

    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)

    # store filter data
    # arry order follow order code
    request.session['filter'] = [False]*10

    if request.POST:

        # filter sort / c crescente / d decrescente
        if request.POST.get('order_by') == 'd' :
            # all real organization
            object_list = Organization.objects.filter(organization=None).order_by('-name')
        else:
            object_list = Organization.objects.filter(organization=None).order_by('name')
        # order by
        request.session['filter'][3] = request.POST.get('order_by')


        # filter from navbar
        search_org_name = request.POST.get('search_org_name')
        if search_org_name:
            object_list = object_list.filter(name__icontains=search_org_name)
            request.session['filter'][0] = request.POST.get('search_org_name')


        if request.POST.get('subscription_start') and request.POST.get('subscription_end'):
            d,m,a = request.POST.get('subscription_start').split('/')
            s = "%s-%s-%s" % (a,m,d)
            dd,mm,aa = request.POST.get('subscription_end').split('/')
            e = "%s-%s-%s" % (aa,mm,dd)
            object_list = object_list.filter(date_created__gt=s, date_created__lt=e)

            request.session['filter'][1] = request.POST.get('subscription_start')
            request.session['filter'][2] = request.POST.get('subscription_end')

        if request.POST.get('option_active'):
            object_list = object_list.filter(active=True)
            request.session['filter'][4] = request.POST.get('option_active')


        if request.POST.get('option_inactive'):
            object_list = object_list.filter(active=False)
            request.session['filter'][5] = request.POST.get('option_inactive')


        if request.POST.get('option_suspension'):
            object_list = object_list.filter(suspension=True)
            request.session['filter'][6] = request.POST.get('option_suspension')


        if request.POST.get('option_notsuspension'):
            object_list = object_list.filter(suspension=False)
            request.session['filter'][7] = request.POST.get('option_notsuspension')


        if request.POST.get('option_zero_client'):
            exclude = []
            for x in object_list:
                if x.clients().count() > 0 :
                    exclude.append(x.id)
            object_list = object_list.exclude(id__in=exclude)
            request.session['filter'][8] = request.POST.get('option_zero_client')


        if request.POST.get('option_notpayed_invoice'):
            exclude = []
            for x in object_list:
                # do not have overdue invoice
                if len(x.invoice_()[2]) == 0 :
                    exclude.append(x.id)

            object_list = object_list.exclude(id__in=exclude)
            request.session['filter'][9] = request.POST.get('option_notpayed_invoice')

        '''
        if order_by: # column
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
            object_list = object_list.order_by(request.session['order_by'])
        '''

        # create email list of result, all organization
        export_email = ''
        for o in object_list:
            for p in o.profile_set.all().filter( Q(user__groups__name__icontains='administrator') | Q(user__groups__name__icontains='secretary') ):
                export_email += u"%s, " % p.user.email

    return render_to_response('gcm/org_list.html', locals(), context_instance=RequestContext(request) )




def billet_config(request):
    dados = BradescoBilletData.objects.all()[0]        
    if request.method == 'POST':
        form = BradescoBilletDataAdminForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            messages.success(request,  _('Successfully updated.'))
        else:
            messages.success(request,  _('Correct the errors bellow.'))
    else:
        form = BradescoBilletDataAdminForm(instance=dados)
        
    return render_to_response('gcm/billet_config.html', locals(), context_instance=RequestContext(request))




def update_org_object(request, *args, **kwargs):
    object_id = kwargs['object_id']
    dados = Organization.objects.get(pk=object_id)  
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            messages.success(request,  _('Successfully updated.'))
        else:
            messages.success(request,  _('Correct the errors bellow.'))
    else:
        form = OrganizationForm(instance=dados)
    
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)
    return generic_object_detail(request, *args, **kwargs)
