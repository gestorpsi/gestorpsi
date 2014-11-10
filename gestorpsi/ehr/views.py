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
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.utils import simplejson
from django.contrib import messages
from gestorpsi.util.views import get_object_or_None
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.ehr.forms import DemandForm, DiagnosisForm, TimeUnitForm, SessionForm
from gestorpsi.ehr.models import Demand, Diagnosis, TimeUnit, Session
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.client.models import Client
from gestorpsi.referral.models import Referral
from gestorpsi import settings

def _access_ehr_check_read(request, object=None):
    """
    this method checks if professional have rights to read client ehr
    in others words, check if client is referred by logged professional
    @object: client
    """

    if not object:
        return False

    if request.user.groups.filter(name='administrator'):
        return True
    
    if request.user.groups.filter(name='professional') or request.user.groups.filter(name='student'):
        professional_have_referral_with_client = False
        professional_is_responsible_for_service = False

        # professional. lets check if request.user (professional) have referral with this client
        for r in object.referral_set.all():
            if request.user.profile.person.careprofessional in [p for p in r.professional.all()]:
                professional_have_referral_with_client = True

        # professional. lets check if request.user (professional) is responsible for referral service
        for r in object.referral_set.all():
            if request.user.profile.person.careprofessional in [p for p in r.service.responsibles.all()]:
                professional_is_responsible_for_service = True

        # check if client is referred by professional or if professional is owner of this record
        if professional_have_referral_with_client or professional_is_responsible_for_service or object.revision().user == request.user:
            return True

    return False

def _access_ehr_check_write(request, referral=None):
    """
    this method checks if professional have rights to write client ehr
    in others words, check if client is referred by logged professional
    @referral: referral
    """

    if not referral:
        return False

    if request.user.groups.filter(name='administrator'):
        return True

    if request.user.groups.filter(name='professional') or request.user.groups.filter(name='student'):
        professional_referral_with_client = False
        professional_is_responsible_for_service = False
        
        # lets check if request.user (professional) have referral with this client
        if request.user.profile.person.careprofessional in [p for p in referral.professional.all()]:
            professional_referral_with_client = True
        
        # professional. lets check if request.user (professional) is responsible for referral service
        if request.user.profile.person.careprofessional in [p for p in referral.service.responsibles.all()]:
            professional_is_responsible_for_service = True

        if professional_referral_with_client or professional_is_responsible_for_service:
            return True

    return False
    
def _ehr_set_edit_status(request):
    """
    this method checks if professional have rights to write a ehr object
    @request: request
    """
    
    status = 99 # unknown
    
    if 'professional' in [i.name for i in request.user.groups.all()]:
        if request.POST.get('draft') == 'true':
            status = 3
        else:
            status = 4
    elif 'student' in [i.name for i in request.user.groups.all()]:
        if request.POST.get('draft') == 'true':
            status = 1
        else:
            status = 2
    
    return status

def _ehr_can_save(request, object):
    """
    this method checks if professional have rights to save (display save button in form)
    @request: request
    @object: session, demand, diagnosis
    """
    
    status = 99 # unknown
    
    if not object.pk: # adding new
        return True
    
    if 'professional' in [i.name for i in request.user.groups.all()]:
        if object.edit_status == '3' or object.edit_status == '2': # is professional and is draft
            return True

    if 'student' in [i.name for i in request.user.groups.all()]:
        if object.edit_status == '1': # is student and is draft
            return True

    return False

@permission_required_with_403('ehr.ehr_read')
def demand_list(request, client_id, referral_id):
    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)

    # check if logged user can read it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    demands = referral.demand_set.all()

    return render_to_response('ehr/ehr_demand_list.html', {
                                    'object': client,
                                    'referral': referral,
                                    'demands': demands,                              
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_write')
def demand_form(request, client_id, referral_id, demand_id=0):
    if not settings.DEBUG and not request.is_ajax(): raise Http404

    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    # check if logged user can write it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    demand = get_object_or_None(Demand, pk=demand_id) or Demand()
    
    if demand.pk and demand.referral.service.organization != request.user.get_profile().org_active:
        raise Http404

    have_perms_to_write = None
    # check if logged user can write on it, just to hide save button on template, is verified by post method also
    if _ehr_can_save(request, demand):
        have_perms_to_write = True

    """ need pass to template time unit forms """
    howlong_form = TimeUnitForm(instance=demand.how_long_it_happens, prefix="howlong")
    frequency_form = TimeUnitForm(instance=demand.frequency, prefix="frequency")
    duration_form = TimeUnitForm(instance=demand.duration, prefix="duration")

    if request.method == 'POST':
        if not _access_ehr_check_write(request, referral):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

        form = DemandForm(request.POST, instance=demand)
        form.fields['occurrence'].queryset = referral.occurrences()

        if not form.is_valid() or demand.pk and not _ehr_can_save(request, demand):
            return render_to_response('ehr/ehr_demand_form.html', {
                                'object': client,
                                'referral': referral,
                                'form': form,
                                'howlong_form': howlong_form,
                                'frequency_form': frequency_form,
                                'duration_form': duration_form,
                                'clss':request.GET.get('clss'),
                                'have_perms_to_write': have_perms_to_write,
                                }, context_instance=RequestContext(request))
        else:
            demand = form.save(commit=False)
            demand.client_id = client.id
            demand.referral_id = referral.id
            demand.occurrence = get_object_or_None(ScheduleOccurrence, pk=request.POST.get('occurrence')) if request.POST.get('occurrence') else None
            
            demand.edit_status = _ehr_set_edit_status(request)
            
            if request.POST.get('howlong-unit'):
                howlong_form = TimeUnitForm(request.POST, instance=demand.how_long_it_happens if demand.how_long_it_happens else TimeUnit(), prefix="howlong")
                if not howlong_form.is_valid():
                    messages.success(request, _("There's an error in 'How long it happens' field."))
                    return HttpResponseRedirect('/client/%s/%s/demand/%s/?clss=error' % (client_id, referral_id, demand.id)) if demand.id else HttpResponseRedirect('/client/%s/%s/demand/add/?clss=error' % (client_id, referral_id))
                demand.how_long_it_happens = howlong_form.save()
            else:
                demand.how_long_it_happens = None

            if request.POST.get('frequency-unit'):
                frequency_form = TimeUnitForm(request.POST, instance=demand.frequency if demand.frequency else TimeUnit(), prefix="frequency")
                if not frequency_form.is_valid():
                    messages.success(request, _("There's an error in 'Frequency' field."))
                    return HttpResponseRedirect('/client/%s/%s/demand/%s/?clss=error' % (client_id, referral_id, demand.id)) if demand.id else HttpResponseRedirect('/client/%s/%s/demand/add/?clss=error' % (client_id, referral_id))
                demand.frequency = frequency_form.save()
            else:
                demand.frequency = None

            if request.POST.get('duration-unit'):
                duration_form = TimeUnitForm(request.POST, instance=demand.duration if demand.duration else TimeUnit(), prefix="duration")
                if not duration_form.is_valid():
                    messages.success(request, _("There's an error in 'Duration' field."))
                    return HttpResponseRedirect('/client/%s/%s/demand/%s/?clss=error' % (client_id, referral_id, demand.id)) if demand.id else HttpResponseRedirect('/client/%s/%s/demand/add/?clss=error' % (client_id, referral_id))
                demand.duration = duration_form.save()
            else:
                demand.duration = None

            demand.save()
            return render_to_response('ehr/ehr_demand_form_done.html', {
                                'demand': demand,
                                'client': client,
                                'referral': referral,
                                }, context_instance=RequestContext(request))

    else:
        form = DemandForm(instance=demand)
        form.fields['occurrence'].queryset = referral.occurrences()
        
        return render_to_response('ehr/ehr_demand_form.html', {
                                        'object': client,
                                        'referral': referral,
                                        'form': form,
                                        'howlong_form': howlong_form,
                                        'frequency_form': frequency_form,
                                        'duration_form': duration_form,
                                        'clss':request.GET.get('clss'),
                                        'have_perms_to_write': have_perms_to_write,
                                        }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_list')
def demand_item_html(request, client_id, referral_id, demand_id):
    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)

    # check if logged user can read it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    demand = get_object_or_None(Demand, pk=demand_id) or Demand()

    if demand.pk and demand.referral.service.organization != request.user.get_profile().org_active:
        raise Http404

    return render_to_response('ehr/ehr_demand_list_item.html', {
                                    'i': demand,
                                    'object': client,
                                    'referral': referral,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_read')
def diagnosis_list(request, client_id, referral_id):
    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)

    # check if logged user can read it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    diagnoses = referral.diagnosis_set.all()

    return render_to_response('ehr/ehr_diagnosis_list.html', {
                                    'object': client,
                                    'referral': referral,
                                    'diagnoses': diagnoses,                              
                                    }, context_instance=RequestContext(request))


@permission_required_with_403('ehr.ehr_list')
def diagnosis_item_html(request, client_id, referral_id, diagnosis_id):
    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)

    # check if logged user can read it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    diagnosis = get_object_or_None(Diagnosis, pk=diagnosis_id) or Demand()

    if diagnosis.pk and diagnosis.referral.service.organization != request.user.get_profile().org_active:
        raise Http404

    return render_to_response('ehr/ehr_diagnosis_list_item.html', {
                                    'i': diagnosis,
                                    'object': client,
                                    'referral': referral,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_read')
def diagnosis_form(request, client_id, referral_id, diagnosis_id=0):
    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    # check if logged user can read it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    diagnosis = get_object_or_None(Diagnosis, pk=diagnosis_id) or Diagnosis()

    if diagnosis.pk and diagnosis.referral.service.organization != request.user.get_profile().org_active:
        raise Http404

    have_perms_to_write = None
    # check if logged user can write on it, just to hide save button on template, is verified by post method also
    if _ehr_can_save(request, diagnosis):
        have_perms_to_write = True
    
    if request.method == 'POST':
        # check if logged user can write it
        if not _access_ehr_check_write(request, referral):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))
        else:
            have_perms_to_write = True

        form = DiagnosisForm(request.POST, instance=diagnosis)
        
        if diagnosis.edit_status == '4':
            form._errors["demand"] = _("You cannot change a confirmed demand.")
        
        if not form.is_valid() or diagnosis.pk and not _ehr_can_save(request, diagnosis):
            return render_to_response('ehr/ehr_diagnosis_form.html', {
                                            'object': client,
                                            'referral': referral,
                                            'form': form,
                                            'have_perms_to_write': have_perms_to_write,
                                            }, context_instance=RequestContext(request))
        else:
            diagnosis = form.save(commit=False)
            diagnosis.client_id = client.id
            diagnosis.referral_id = referral.id
            diagnosis.occurrence = get_object_or_None(ScheduleOccurrence, pk=request.POST.get('occurrence')) if request.POST.get('occurrence') else None

            diagnosis.edit_status = _ehr_set_edit_status(request)

            diagnosis.save()
            return render_to_response('ehr/ehr_diagnosis_form_done.html', {
                                'diagnosis': diagnosis,
                                'client': client,
                                'referral': referral,
                                }, context_instance=RequestContext(request))
    else: # GET
        # check if logged user can write on it
        if _access_ehr_check_write(request, referral):
            have_perms_to_write = True

        diagnosis = get_object_or_None(Diagnosis, pk=diagnosis_id) or Diagnosis()

        if diagnosis.pk and diagnosis.referral.service.organization != request.user.get_profile().org_active:
            raise Http404

        form = DiagnosisForm(instance=diagnosis, label_suffix='')
        if not diagnosis.diagnosis_date:
            form.initial = {'diagnosis_date': datetime.strftime(datetime.now(), "%d/%m/%Y")}
        form.fields['occurrence'].queryset = referral.occurrences()
        return render_to_response('ehr/ehr_diagnosis_form.html', {
                                        'object': client,
                                        'referral': referral,
                                        'form': form,
                                        'clss':request.GET.get('clss'),
                                        'have_perms_to_write': have_perms_to_write,
                                        }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_read')
def session_list(request, client_id, referral_id):
    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)

    # check if logged user can read it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    return render_to_response('ehr/ehr_session_list.html', {
                                    'object': client,
                                    'referral': referral,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_list')
def session_item_html(request, client_id, referral_id, session_id):
    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)

    # check if logged user can read it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    occurrence = referral.session_set.get(pk=session_id).occurrence
    
    return render_to_response('ehr/ehr_session_list_item.html', {
                                    'occurrence': occurrence,
                                    'object': client,
                                    'referral': referral,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('ehr.ehr_write')
def session_form(request, client_id, referral_id, session_id=0):

    if not settings.DEBUG and not request.is_ajax(): raise Http404

    client = get_object_or_404(Client, pk=client_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    # check if logged user can read it
    if not _access_ehr_check_read(request, client):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    session = get_object_or_None(Session, pk=session_id) or Session()

    have_perms_to_write = None
    # check if logged user can write on it
    if _ehr_can_save(request, session):
        have_perms_to_write = True

    if session.pk and session.referral.service.organization != request.user.get_profile().org_active:
        raise Http404
    
    if request.method == 'POST':
        if not _access_ehr_check_write(request, referral):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))
        
        form = SessionForm(request.POST, instance=session, initial={'occurrence':request.POST.get('occurrence')})

        form.fields['occurrence'].queryset = referral.occurrences().filter(session=None) if session_id==0 else referral.occurrences()
        form.fields['occurrence'].widget = forms.HiddenInput()

        if not form.is_valid() or session.pk and not _ehr_can_save(request, session):
            return render_to_response('ehr/ehr_session_form.html', {
                                            'object': client,
                                            'referral': referral,
                                            'session': session,
                                            'form': form,
                                            'clss':request.GET.get('clss'),
                                            'have_perms_to_write': have_perms_to_write,
                                            }, context_instance=RequestContext(request))

        else:
            session = form.save(commit=False)
            session.client_id = client.id
            session.referral_id = referral.id
            session.occurrence_id = ScheduleOccurrence.objects.get(pk=request.POST.get('occurrence')).id

            session.edit_status = _ehr_set_edit_status(request)

            session.save()

            url = '/client/%s/%s/session/%s/item/' % (client_id, referral_id, session.pk)
            return HttpResponse(simplejson.dumps({'occurrence_pk':request.POST.get('occurrence'), 'url':url}))

    else: # GET

        if request.GET.get('o') or session.pk:
            occurrence_pk = session.occurrence if session.pk else request.GET.get('o')
            form = SessionForm(instance=session, initial={'occurrence':occurrence_pk})
        else:
            form = SessionForm(instance=session)
            
        form.fields['occurrence'].queryset = referral.occurrences().filter(session=None) if session_id==0 else referral.occurrences()
        form.fields['occurrence'].widget = forms.HiddenInput()
            
        return render_to_response('ehr/ehr_session_form.html', {
                                        'object': client,
                                        'referral': referral,
                                        'session': session,
                                        'form': form,
                                        'clss':request.GET.get('clss'),
                                        'have_perms_to_write': have_perms_to_write,
                                        }, context_instance=RequestContext(request))
