# -*- coding: utf-8 -*-

"""
    Copyright (C) 2008 GestorPsi
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from gestorpsi.organization.models import Organization

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
        export_email_count = 0
        export_email = ''
        for o in object_list:
            for p in o.profile_set.all().filter( Q(user__groups__name__icontains='administrator') | Q(user__groups__name__icontains='secretary') ):
                if not p.user.email in export_email:
                    export_email += u"%s, " % p.user.email
                    export_email_count += 1

    return render_to_response('gcm/org_list.html', locals(), context_instance=RequestContext(request) )
