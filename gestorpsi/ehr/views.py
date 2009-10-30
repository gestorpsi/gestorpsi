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
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from django.template import RequestContext

from gestorpsi.util.views import get_object_or_None
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.ehr.forms import DemandForm, DiagnosisForm, TimeUnitForm, SessionForm
from gestorpsi.ehr.models import Demand, Diagnosis, TimeUnit, Session
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.client.models import Client
from gestorpsi.referral.models import Referral

@permission_required_with_403('ehr.ehr_list')
def demand_list(request, client_id, referral_id):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    demands = referral.demand_set.all()
    return render_to_response('ehr/ehr_demand_list.html', {
                                    'object': client,
                                    'referral': referral,
                                    'demands': demands,                              
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_read')
def demand_form(request, client_id, referral_id, demand_id=0):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    demand = get_object_or_None(Demand, pk=demand_id) or Demand()
    demand_form = DemandForm(instance=demand)
    demand_form.fields['occurrence'].queryset = referral.occurrences()
    
    """ need pass to template time unit forms """
    howlong_form = TimeUnitForm(instance=demand.how_long_it_happens, prefix="howlong")
    frequency_form = TimeUnitForm(instance=demand.frequency, prefix="frequency")
    duration_form = TimeUnitForm(instance=demand.duration, prefix="duration")
    
    return render_to_response('ehr/ehr_demand_form.html', {
                                    'object': client,
                                    'referral': referral,
                                    'demand_form': demand_form,
                                    'howlong_form': howlong_form,
                                    'frequency_form': frequency_form,
                                    'duration_form': duration_form,
                                    'clss':request.GET.get('clss'),
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_write')
def demand_save(request, client_id, referral_id, demand_id=0):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    
    demand = get_object_or_None(Demand, pk=demand_id) or Demand()
    if demand.edit_status in ('2', '4'):
        request.user.message_set.create(message=_("You cannot change a confirmed demand."))
        return HttpResponseRedirect('/client/%s/%s/demand/%s/?clss=error' % (client_id, referral_id, demand.id))

    demand_form = DemandForm(request.POST, instance=demand)
    if not demand_form.is_valid():
        request.user.message_set.create(message=_('Choosen occurence already in use by another demand.')) if session_form.errors.get('occurrence') else request.user.message_set.create(message=_("There's been an error in demand form."))
        return HttpResponseRedirect('/client/%s/%s/demand/%s/?clss=error' % (client_id, referral_id, demand.id)) if demand.id else HttpResponseRedirect('/client/%s/%s/demand/add/?clss=error' % (client_id, referral_id))

    demand = demand_form.save(commit=False)
    demand.client_id = client.id
    demand.referral_id = referral.id
    demand.occurrence = get_object_or_None(ScheduleOccurrence, pk=request.POST.get('occurrence')) if request.POST.get('occurrence') else None
    
    """ need check who saved the demand: professional or student """
    if 1==1:    # <- if professional
        demand.edit_status = '3' if request.POST.get('draft') == 'is_draft' else '4'
    else:       # <- if student
        demand.edit_status = '1' if request.POST.get('draft') == 'is_draft' else '2'

    if request.POST.get('howlong-unit'):
        howlong_form = TimeUnitForm(request.POST, instance=demand.how_long_it_happens if demand.how_long_it_happens else TimeUnit(), prefix="howlong")
        if not howlong_form.is_valid():
            request.user.message_set.create(message=_("There's an error in 'How long it happens' field."))
            return HttpResponseRedirect('/client/%s/%s/demand/%s/?clss=error' % (client_id, referral_id, demand.id)) if demand.id else HttpResponseRedirect('/client/%s/%s/demand/add/?clss=error' % (client_id, referral_id))
        demand.how_long_it_happens = howlong_form.save()
    else:
        demand.how_long_it_happens = None

    if request.POST.get('frequency-unit'):
        frequency_form = TimeUnitForm(request.POST, instance=demand.frequency if demand.frequency else TimeUnit(), prefix="frequency")
        if not frequency_form.is_valid():
            request.user.message_set.create(message=_("There's an error in 'Frequency' field."))
            return HttpResponseRedirect('/client/%s/%s/demand/%s/?clss=error' % (client_id, referral_id, demand.id)) if demand.id else HttpResponseRedirect('/client/%s/%s/demand/add/?clss=error' % (client_id, referral_id))
        demand.frequency = frequency_form.save()
    else:
        demand.frequency = None

    if request.POST.get('duration-unit'):
        duration_form = TimeUnitForm(request.POST, instance=demand.duration if demand.duration else TimeUnit(), prefix="duration")
        if not duration_form.is_valid():
            request.user.message_set.create(message=_("There's an error in 'Duration' field."))
            return HttpResponseRedirect('/client/%s/%s/demand/%s/?clss=error' % (client_id, referral_id, demand.id)) if demand.id else HttpResponseRedirect('/client/%s/%s/demand/add/?clss=error' % (client_id, referral_id))
        demand.duration = duration_form.save()
    else:
        demand.duration = None

    demand.save()
    request.user.message_set.create(message=_('Demand saved successfully'))
    return HttpResponseRedirect('/client/%s/%s/demand/%s/' % (client_id, referral_id, demand.id))

@permission_required_with_403('ehr.ehr_list')
def diagnosis_list(request, client_id, referral_id):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    diagnoses = referral.diagnosis_set.all()
    return render_to_response('ehr/ehr_diagnosis_list.html', {
                                    'object': client,
                                    'referral': referral,
                                    'diagnoses': diagnoses,                              
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_read')
def diagnosis_form(request, client_id, referral_id, diagnosis_id=0):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    diagnosis = get_object_or_None(Diagnosis, pk=diagnosis_id) or Diagnosis()
    diagnosis_form = DiagnosisForm(instance=diagnosis, label_suffix='')
    if not diagnosis.diagnosis_date:
        diagnosis_form.initial = {'diagnosis_date': datetime.strftime(datetime.now(), "%d/%m/%Y")}
    diagnosis_form.fields['occurrence'].queryset = referral.occurrences()
    return render_to_response('ehr/ehr_diagnosis_form.html', {
                                    'object': client,
                                    'referral': referral,
                                    'diagnosis_form': diagnosis_form,
                                    'clss':request.GET.get('clss'),
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_write')
def diagnosis_save(request, client_id, referral_id, diagnosis_id=0):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    
    diagnosis = get_object_or_None(Diagnosis, pk=diagnosis_id) or Diagnosis()
    if diagnosis.edit_status in ('2', '4'):
        request.user.message_set.create(message=_("You cannot change a confirmed diagnosis."))
        return HttpResponseRedirect('/client/%s/%s/diagnosis/%s/?clss=error' % (client_id, referral_id, diagnosis.id))

    diagnosis_form = DiagnosisForm(request.POST, instance=diagnosis)
    if not diagnosis_form.is_valid():
        request.user.message_set.create(message=_('Choosen occurence already in use by another diagnosis.')) if diagnosis_form.errors.get('ooccurrence') else request.user.message_set.create(message=_("There's been an error in diagnosis form."))
        return HttpResponseRedirect('/client/%s/%s/diagnosis/%s/?clss=error' % (client_id, referral_id, diagnosis.id)) if diagnosis.id else HttpResponseRedirect('/client/%s/%s/diagnosis/add/?clss=error' % (client_id, referral_id))

    diagnosis = diagnosis_form.save(commit=False)
    diagnosis.client_id = client.id
    diagnosis.referral_id = referral.id
    diagnosis.occurrence = get_object_or_None(ScheduleOccurrence, pk=request.POST.get('occurrence')) if request.POST.get('occurrence') else None

    """ need check who saved the diagnosis: professional or student """
    if 1==1:    # <- if professional
        diagnosis.edit_status = '3' if request.POST.get('draft') == 'is_draft' else '4'
    else:       # <- if student
        diagnosis.edit_status = '1' if request.POST.get('draft') == 'is_draft' else '2'

    diagnosis.save()
    request.user.message_set.create(message=_('Diagnosis saved successfully'))
    return HttpResponseRedirect('/client/%s/%s/diagnosis/%s/' % (client_id, referral_id, diagnosis.id))

@permission_required_with_403('ehr.ehr_list')
def session_list(request, client_id, referral_id):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    sessions = referral.session_set.all()
    return render_to_response('ehr/ehr_session_list.html', {
                                    'object': client,
                                    'referral': referral,
                                    'sessions': sessions,                              
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_read')
def session_form(request, client_id, referral_id, session_id=0):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    session = get_object_or_None(Session, pk=session_id) or Session()
    session_form = SessionForm(instance=session)
    session_form.fields['occurrence'].queryset = referral.occurrences().filter(session=None) if session_id==0 else referral.occurrences()
    return render_to_response('ehr/ehr_session_form.html', {
                                    'object': client,
                                    'referral': referral,
                                    'session_form': session_form,
                                    'clss':request.GET.get('clss'),
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_write')
def session_save(request, client_id, referral_id, session_id=0):
    client = get_object_or_404(Client, pk=client_id)
    referral = get_object_or_404(Referral, pk=referral_id)
    
    session = get_object_or_None(Session, pk=session_id) or Session()
    if session.edit_status in ('2', '4'):
        request.user.message_set.create(message=_("You cannot change a confirmed session."))
        return HttpResponseRedirect('/client/%s/%s/session/%s/?clss=error' % (client_id, referral_id, session.id))

    session_form = SessionForm(request.POST, instance=session)
    if not session_form.is_valid():
        request.user.message_set.create(message=_('Choosen occurence already in use by another session.')) if session_form.errors.get('occurrence') else request.user.message_set.create(message=_("There's been an error in session form."))
        return HttpResponseRedirect('/client/%s/%s/session/%s/?clss=error' % (client_id, referral_id, session.id)) if session.id else HttpResponseRedirect('/client/%s/%s/session/add/?clss=error' % (client_id, referral_id))

    session = session_form.save(commit=False)
    session.client_id = client.id
    session.referral_id = referral.id
    session.occurrence_id = ScheduleOccurrence.objects.get(pk=request.POST.get('occurrence')).id

    """ need check who saved the session: professional or student """
    if 1==1:    # <- if professional
        session.edit_status = '3' if request.POST.get('draft') == 'is_draft' else '4'
    else:       # <- if student
        session.edit_status = '1' if request.POST.get('draft') == 'is_draft' else '2'

    session.save()
    request.user.message_set.create(message=_('Session saved successfully'))
    return HttpResponseRedirect('/client/%s/%s/session/%s/' % (client_id, referral_id, session.id))
