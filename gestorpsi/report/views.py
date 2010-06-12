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
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from gestorpsi.admission.models import AdmissionReferral
from gestorpsi.report.forms import ReportForm, ReportSaveAdmissionForm
from gestorpsi.report.models import ReportAdmission, ReportsSaved, Report
from gestorpsi.settings import MEDIA_URL, MEDIA_ROOT
from gestorpsi.util.views import write_pdf

def index(request):
    """
    display initial templates
    """

    form = ReportForm(request.user.get_profile().org_active.created(), datetime.now())
    
    """
    pass filter itens in right bar
    """
    
    r = Report()
    filters = r.filters()
    
    return render_to_response('report/report_index.html', locals(), context_instance=RequestContext(request))
    
def report_date(request):
    date_start,date_end = Report().set_date(request.user.get_profile().org_active, request.GET.get('date_start'), request.GET.get('date_end'))
    return HttpResponse(simplejson.dumps({'date_start':date_start.strftime('%d/%m/%Y'), 'date_end':date_end.strftime('%d/%m/%Y')}))
    
def chart(request, view='admission'):
    organization = request.user.get_profile().org_active
    report = Report()
    
    date_start,date_end = report.set_date(organization, request.GET.get('date_start'), request.GET.get('date_end'))

    if 'admission' in view:
        range = AdmissionReferral.objects_inrange.all(organization, date_start, date_end)
        if range:
            chart_json = ReportAdmission.objects.chart(range, date_start, date_end)
    
            return HttpResponse(chart_json)
    
    return HttpResponse()

def admission_data(request):
    """
    load admission dashboard reports
    """
    
    admission,date_start,date_end = Report().get_admissions_range(request.user.get_profile().org_active, request.GET.get('date_start'), request.GET.get('date_end'))

    return render_to_response('report/report_admission_table.html', locals(), context_instance=RequestContext(request))

def admission_client_report(request, view, filter):
    """
    fetch client list from selected admission report
    """
    
    organization = request.user.get_profile().org_active
    report = Report()
    date_start,date_end = report.set_date(organization, request.GET.get('date_start'), request.GET.get('date_end'))

    verbose_name, object_list, organization_total = ReportAdmission.objects.clients(request.user, date_start, date_end, view, filter)

    return render_to_response('report/report_client_list.html', locals(), context_instance=RequestContext(request))

def demographic_data(request, view='admission'):
    organization = request.user.get_profile().org_active
    report = Report()
    date_start,date_end = report.set_date(organization, request.GET.get('date_start'), request.GET.get('date_end'))
    if 'admission' in view:
        range = AdmissionReferral.objects_inrange.all(organization, date_start, date_end)
    
    if range:
        demographic = ReportAdmission.objects_demographic.all(organization, [i.client.id for i in range])
    
    return render_to_response('report/report_demographic_table.html', locals(), context_instance=RequestContext(request))
    
def report_save(request, form_class=ReportSaveAdmissionForm, view='admission', template='report/report_admission_save.html'):
    """
    save new report
    """
    if request.method == 'POST':
        save_form = form_class(request.POST)

        if save_form.is_valid():
            data = save_form.save(request.user, request.user.get_profile().org_active)
            return HttpResponse(data.label)
        else:
            raise Exception(_('Error to save register'))

    report = Report()
    date_start,date_end = report.set_date(request.user.get_profile().org_active, request.GET.get('date_start'), request.GET.get('date_end'))
    form = form_class(date_start=date_start, date_end=date_end)
    
    return render_to_response(template, locals(), context_instance=RequestContext(request))
    
def reports_saved(request, view='admission'):
    """
    list saved reports
    """
    organization = request.user.get_profile().org_active
    admissions = ReportsSaved.objects.admission(request.user, organization)
    referrals = ReportsSaved.objects.referral(request.user, organization)
    trash = ReportsSaved.objects.trash(request.user, organization)
    
    return render_to_response('report/report_saved.html', locals(), context_instance=RequestContext(request))
    
def report_del(request, object_id, undelete=False):
    """
    delete/undelete saved reports
    """
    obj = get_object_or_404(ReportsSaved, id=object_id, user=request.user, organization=request.user.get_profile().org_active)
    obj.trash = True if not undelete else False
    obj.save()
    
    return HttpResponse(obj.id)

def report_empty(request):
    """
    empty deleted reports from trash
    """
    ReportsSaved.objects.filter(trash=True, user=request.user, organization=request.user.get_profile().org_active).delete()
    return HttpResponse(True)

def admission_export(request):
    """
    export admission data in html or pdf
    """
    if request.method == 'POST':
        r = Report()
        org_active = request.user.get_profile().org_active
        
        # admission statistcs data
        admission,date_start,date_end = Report().get_admissions_range(org_active, request.POST.get('date_start'), request.POST.get('date_end'))

        # list of clients in admissions stats
        if request.POST.get('clients'):
            report_admission_clients = ReportAdmission.objects.clients_all(request.user, request.POST.get('date_start'), request.POST.get('date_end'))
        
        MEDIA_URL = MEDIA_URL if request.POST.get('format') == 1 else MEDIA_ROOT.replace('\\','/') + '/' # this a path bug fix. format == 1 (html)

        if int(request.POST.get('format')) == 2: # pdf print
            user = request.user
            return write_pdf('report/report_admission_export.html', locals(), '%s.pdf' % _('admission-report'))

        remove_links = True
        return render_to_response('report/report_admission_export.html', locals(), context_instance=RequestContext(request))

    
