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
from django.utils.html import escape
from django.db.models import Q

from gestorpsi.admission.models import AdmissionReferral
from gestorpsi.report.forms import ReportForm
from gestorpsi.report.models import ReportAdmission, ReportsSaved, Report, ReportReferral
from gestorpsi.service.models import Service
from gestorpsi.settings import MEDIA_ROOT
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
    data, lines, date_start, date_end, sch_list, total_events, show_filter = Report().get_event_( request.user.get_profile().org_active , request.GET.get('date_start') , request.GET.get('date_end') , request.GET.get('professional') , request.GET.get('service'), request.GET.get('status'), request.GET.get('accumulated') )

    # variables of JS
    option_rows = data 
    column = lines

    return render_to_response(template, locals(), context_instance=RequestContext(request))


@permission_required_with_403('report.report_list')
def formfill_data(request):
    """
    check if field is fill of a form.
    """
    list_client, list_client_total, date_start, date_end, professional, service, fillform, attach, show_filters = Report().get_formfill_( request.user.get_profile().org_active, request.GET.get('date_start'), request.GET.get('date_end'), request.GET.get('professional'), request.GET.get('service'), request.GET.get('formfill'), request.GET.get('attach'), request.GET.get('charge'))

    if request.GET.get('formfill') == '1':
        template='report/report_medicalrecord.html'

    return render_to_response(template, locals(), context_instance=RequestContext(request))


@permission_required_with_403('report.report_list')
def report_client_list(request, report_class, view, filter):
    """
    fetch client list from selected admission report
    """
    
    organization = request.user.get_profile().org_active
    report = Report()
    date_start, date_end = report.set_date(organization, request.GET.get('date_start'), request.GET.get('date_end'))

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
    render {{ url_post }} at report/report_save_form.html and update <form action> to save report for right section, view.
    """
    if request.method == 'POST':
        save_form = form_class(request.POST)

        if save_form.is_valid():
            data = save_form.save(request.user, request.user.get_profile().org_active)
            return HttpResponse(escape(data.label))
        else:
            raise Exception(_('Error to save register'))

    report = Report()
    date_start, date_end = report.set_date(request.user.get_profile().org_active, request.GET.get('date_start'), request.GET.get('date_end'))

    # admission / referral
    if view == 'admission':
        form = form_class(date_start=date_start, date_end=date_end, accumulated=request.GET.get('accumulated'))

    # financial / revenues
    if view == 'receive':
        form = form_class(date_start=date_start, date_end=date_end, service=request.GET.get('service'),  professional=request.GET.get('professional'), pway=request.GET.get('pway'), receive=request.GET.get('receive'), covenant=request.GET.get('covenant'))

    # prontuario / medical record
    if view == 'formfill':
        form = form_class(date_start=date_start, date_end=date_end, professional=request.GET.get('professional'), service=request.GET.get('service'), formfill=request.GET.get('formfill'), attach=request.GET.get('attach'), charge=request.GET.get('charge'))

    url_post = reverse('report_%s_save' % view) # update <form action url>
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

        # event report
        if request.POST.get('view') == '4':

            view = 'event'
            title = u'Relatório de eventos'
            html = 'report/report_event_export.html'
    
            data, lines, date_start, date_end, sch_list, total_events, show_filter = Report().get_event_(request.user.get_profile().org_active, request.POST.get('date_start'), request.POST.get('date_end'), request.POST.get('professional'), request.POST.get('service'), request.POST.get('confirmation_status'), request.POST.get('accumulated'))

            IMG_PREFIX = '/media/' if int(request.POST.get('format')) == 1 else MEDIA_ROOT.replace('\\','/') + '/' # this a path bug fix. format == 1 (html)

            if int(request.POST.get('format')) == 2: # pdf print
                return write_pdf(html, locals(), ('%s-%s-%s-%s-%s.pdf' % (view, slugify(_('report-between')), request.POST.get('date_start').replace('/','-'), _('and'), request.POST.get('date_end').replace('/','-'))))


        # fill fields form report
        if request.POST.get('view') == '5':
            view = u'prontuario'
            title = _(u'Relatorio de prontuário')
            html = 'report/report_medicalrecord_export.html'

            list_client, list_client_total, date_start, date_end, professional, service, fillform, attach, show_filters = Report().get_formfill_(request.user.get_profile().org_active, request.POST.get('date_start'), request.POST.get('date_end'), request.POST.get('professional'), request.POST.get('service'), request.POST.get('formfill_choice'), request.POST.get('formfill_attach'), request.POST.get('formfill_status'))

            IMG_PREFIX = '/media/' if int(request.POST.get('format')) == 1 else MEDIA_ROOT.replace('\\','/') + '/' # this a path bug fix. format == 1 (html)

            if int(request.POST.get('format')) == 2: # pdf print
                return write_pdf(html, locals(), ('%s-%s-%s-%s-%s.pdf' % (view, slugify(_('report-between')), date_start, _('and'), date_end)))

        # default out is html format
        remove_links = True
        export_graph_type = request.POST.get('export_graph_type')
        return render_to_response(html, locals(), context_instance=RequestContext(request))
