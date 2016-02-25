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

from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Q

from gestorpsi.admission.models import AdmissionReferral
from gestorpsi.report.forms import ReportForm, ReportSaveAdmissionForm
from gestorpsi.report.models import ReportAdmission, ReportsSaved, Report, ReportReferral
from gestorpsi.referral.models import Referral
from gestorpsi.service.models import Service
from gestorpsi.settings import MEDIA_URL, MEDIA_ROOT
from gestorpsi.util.views import write_pdf
from gestorpsi.util.decorators import permission_required_with_403

@permission_required_with_403('report.report_list')
def index(request):
    """
    display initial templates

    permission:
        all:
        administrator or secretary can use all.

        professional:
        professional can filter just yours own services and covenant.

        False:
        others can't user report
    """

    form = ReportForm(request.user.get_profile().org_active.created(), datetime.now(), request.user.get_profile().org_active)

    # permission, can't use professional filter
    permission = False 

    if request.user.groups.filter(name__icontains='professional'):
        permission = 'professional'

    if request.user.groups.filter(Q(name__icontains='administrator')|Q(name__icontains='secretary')).distinct():
        permission = 'all'

    """
    pass filter itens in right bar
    """
    
    r = Report()
    filters = r.filters()
    
    return render_to_response('report/report_index.html', locals(), context_instance=RequestContext(request))


@permission_required_with_403('report.report_list')
def report_date(request):

    date_start,date_end = Report().set_date(request.user.get_profile().org_active, request.GET.get('date_start'), request.GET.get('date_end'))
    accumulated = request.GET.get('accumulated')

    return HttpResponse(simplejson.dumps({'date_start':date_start.strftime('%d/%m/%Y'), 'date_end':date_end.strftime('%d/%m/%Y'), 'accumulated': accumulated}))


@permission_required_with_403('report.report_list')
def admission_data(request, template='report/report_table.html'):
    """
    load admission dashboard reports
    """

    data, chart_url, date_start,date_end = Report().get_admissions_range(request.user.get_profile().org_active, request.GET.get('date_start'), request.GET.get('date_end'), request.GET.get('accumulated'))

    return render_to_response(template, locals(), context_instance=RequestContext(request))



@permission_required_with_403('report.report_list')
def referral_data(request, template='report/report_table.html'):
    """
    load referral dashboard reports
    """
    data, date_start,date_end,service = Report().get_referral_range(request.user.get_profile().org_active, request.GET.get('date_start'), request.GET.get('date_end'), request.GET.get('service'), request.GET.get('accumulated'))

    return render_to_response(template, locals(), context_instance=RequestContext(request))


@permission_required_with_403('report.report_list')
def receive_data(request, template='report/report_receive.html'):
    """
    receive
    """

    data , colors , date_start, date_end, list_receive, total_receive = Report().get_receive_( request.user.get_profile().org_active , request.GET.get('date_start') , request.GET.get('date_end') , request.GET.get('professional') , request.GET.get('receive') , request.GET.get('service'), request.GET.get('pway'), request.GET.get('covenant') )

    # variables of JS
    option_title = u'Estatística de todos os profíssionais, serviços e pagamentos para o período escolhido.'
    option_rows = data 
    option_colors = colors

    return render_to_response(template, locals(), context_instance=RequestContext(request))


@permission_required_with_403('report.report_list')
def event_data(request, template='report/report_event.html'):
    """
    event
    """
    data, lines, date_start, date_end, sch_list, total_events = Report().get_event_( request.user.get_profile().org_active , request.GET.get('date_start') , request.GET.get('date_end') , request.GET.get('professional') , request.GET.get('service'), request.GET.get('status'), request.GET.get('accumulated') )

    # variables of JS
    option_rows = data 
    column = lines

    #option_rows = "([ [new Date(2015, 0, 1), 5],  [new Date(2015, 0, 2), 7],  [new Date(2015, 0, 3), 3], [new Date(2015, 0, 4), 1],  [new Date(2015, 0, 5), 3],  [new Date(2015, 0, 6), 4], [new Date(2015, 0, 7), 3],  [new Date(2015, 0, 8), 4],  [new Date(2015, 0, 9), 2], [new Date(2015, 0, 10), 5], [new Date(2015, 0, 11), 8], [new Date(2015, 0, 12), 6], [new Date(2015, 0, 13), 3], [new Date(2015, 0, 14), 3], [new Date(2015, 0, 15), 5], [new Date(2015, 0, 16), 7], [new Date(2015, 0, 17), 6], [new Date(2015, 0, 18), 6], [new Date(2015, 0, 19), 3], [new Date(2015, 0, 20), 1], [new Date(2015, 0, 21), 2], [new Date(2015, 0, 22), 4], [new Date(2015, 0, 23), 6], [new Date(2015, 0, 24), 5], [new Date(2015, 0, 25), 9], [new Date(2015, 0, 26), 4], [new Date(2015, 0, 27), 9], [new Date(2015, 0, 28), 8], [new Date(2015, 0, 29), 6], [new Date(2015, 0, 30), 4], [new Date(2015, 0, 31), 6], [new Date(2015, 1, 1), 7], [new Date(2015, 1, 2), -10] ]);"
     
    return render_to_response(template, locals(), context_instance=RequestContext(request))


@permission_required_with_403('report.report_list')
def report_client_list(request, report_class, view, filter):
    """
    fetch client list from selected admission report
    """
    
    organization = request.user.get_profile().org_active
    report = Report()
    date_start,date_end = report.set_date(organization, request.GET.get('date_start'), request.GET.get('date_end'))

    verbose_name, object_list, organization_total = report_class.objects.clients(request.user, date_start, date_end, view, filter, request.GET.get('service'))

    not_diplay_count = int(len(organization_total))-int(len(object_list))

    return render_to_response('report/report_client_list.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('report.report_list')
def demographic_data(request, view='admission'):
    organization = request.user.get_profile().org_active
    report = Report()
    date_start,date_end = report.set_date(organization, request.GET.get('date_start'), request.GET.get('date_end'))
    if 'admission' in view:
        range = AdmissionReferral.objects_inrange.all(organization, date_start, date_end)
    
    if range:
        demographic = ReportAdmission.objects_demographic.all(organization, [i.client.id for i in range])
    
    return render_to_response('report/report_demographic_table.html', locals(), context_instance=RequestContext(request))


@permission_required_with_403('report.report_write')
def report_save(request, form_class=None, view=None, template='report/report_save_form.html'):

    """
    save new report
    """
    if request.method == 'POST':

        save_form = form_class(request.POST)

        if save_form.is_valid():
            data = save_form.save( request.user , request.user.get_profile().org_active )
            return HttpResponse( data.label )
        else:
            raise Exception(_('Error to save register'))

    report = Report()

    date_start , date_end = report.set_date( request.user.get_profile().org_active , request.GET.get('date_start') , request.GET.get('date_end') )

    # financial / revenues
    if view == 'receive':
        form = form_class( date_start=date_start , date_end=date_end , service=request.GET.get('service') ,  professional=request.GET.get('professional') , pway=request.GET.get('pway'), receive=request.GET.get('receive') , covenant=request.GET.get('covenant') )
    # admission / referral
    else:
        form = form_class( date_start=date_start , date_end=date_end , service=Service.objects.get( organization=request.user.get_profile().org_active, pk=request.GET.get('service')) if request.GET.get('service') else None, accumulated=request.GET.get('accumulated'))

    url_post = reverse('report_%s_save' % view) # url to post form
    
    return render_to_response(template, locals(), context_instance=RequestContext(request))


@permission_required_with_403('report.report_write')
def reports_saved(request, view='admission'):
    """
    list saved reports
    """
    organization = request.user.get_profile().org_active
    #admissions = ReportsSaved.objects.admission(request.user, organization)
    #referrals = ReportsSaved.objects.referral(request.user, organization)
    reports = ReportsSaved.objects.from_user(request.user, organization)
    trash = ReportsSaved.objects.trash(request.user, organization)
    
    return render_to_response('report/report_saved.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('report.report_write')
def report_del(request, object_id, undelete=False):
    """
    delete/undelete saved reports
    """
    obj = get_object_or_404(ReportsSaved, id=object_id, user=request.user, organization=request.user.get_profile().org_active)
    obj.trash = True if not undelete else False
    obj.save()
    
    return HttpResponse(obj.id)

@permission_required_with_403('report.report_write')
def report_empty(request):
    """
    empty deleted reports from trash
    """
    ReportsSaved.objects.filter(trash=True, user=request.user, organization=request.user.get_profile().org_active).delete()
    return HttpResponse(True)

@permission_required_with_403('report.report_list')
def report_export(request):
    """
    export admission data in html or pdf
    """

    html = 'report/report_export.html'

    if request.method == 'POST':

        r = Report()
        org_active = request.user.get_profile().org_active
        
        # admission statistcs data
        if request.POST.get('view') == '1': # admission
            title = _('Admission Report')
            view = 'admission'
            data = Report().get_admissions_range(org_active, request.POST.get('date_start'), request.POST.get('date_end'), request.POST.get('accumulated'))

            if request.POST.get('clients'):
                report_clients = ReportAdmission.objects.clients_all(request.user, request.POST.get('date_start'), request.POST.get('date_end'))
            data, chart_url, date_start,date_end = data

        if request.POST.get('view') == '2': # referral
            title = _('Referral Report')
            if request.POST.get('service'):
                sub_title = u'%s %s' % (_('Service'), Service.objects.get(organization=request.user.get_profile().org_active, pk=request.POST.get('service')))
            view = 'referral'
            data = Report().get_referral_range(org_active, request.POST.get('date_start'), request.POST.get('date_end'), request.POST.get('service'), request.POST.get('accumulated'))

            if request.POST.get('clients'):
                report_clients = ReportReferral.objects.clients_all(request.user, request.POST.get('date_start'), request.POST.get('date_end'))
            
            data,date_start,date_end, service = data

        # renevues / faturamento
        if request.POST.get('view') == '3':

            view = 'receive'
            title = _('Revenues Report')
            html = 'report/report_receive_export.html'

            data , colors , date_start , date_end , list_receive , total_receive = Report().get_receive_( org_active, request.POST.get('date_start'), request.POST.get('date_end'), request.POST.get('professional'), request.POST.get('receipt_status'), request.POST.get('service'), request.POST.get('payment_way'), request.POST.get('cove') )

            # variables of JS
            option_title = u'Estatística de todos os profíssionais, serviços e pagamentos para o período escolhido.'
            option_rows = data 
            option_colors = colors

            IMG_PREFIX = '/media/' if int(request.POST.get('format')) == 1 else MEDIA_ROOT.replace('\\','/') + '/' # this a path bug fix. format == 1 (html)

            if int(request.POST.get('format')) == 2: # pdf print
                return write_pdf( html , locals(), ('%s-%s-%s-%s-%s.pdf' % (view, slugify(_('report-between')), request.POST.get('date_start').replace('/','-'), _('and'), request.POST.get('date_end').replace('/','-'))))

        # default out is html format
        remove_links = True
        export_graph_type = request.POST.get('export_graph_type')
        return render_to_response( html , locals(), context_instance=RequestContext(request))

