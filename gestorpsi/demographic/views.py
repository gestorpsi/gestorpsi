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
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.contrib import messages
from gestorpsi.util.views import get_object_or_None
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.client.models import Client
from gestorpsi.demographic.forms import EducationalLevelForm, ProfessionForm
from gestorpsi.demographic.models import EducationalLevel, Profession

from gestorpsi.cbo.models import Occupation

from gestorpsi.client.views import _access_check

@permission_required_with_403('demographic.demographic_read')
def home(request, object_id):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    # check access by requested user
    if not _access_check(request, object) or object.is_company():
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    return render_to_response('demographic/demographic_home.html', {
                                    'object': object,
                                    'demographic_menu': True,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('demographic.demographic_read')
def education(request, object_id):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    # check access by requested user
    if not _access_check(request, object) or object.is_company():
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if hasattr(object, 'educationallevel'):
        education_form = EducationalLevelForm(instance=object.educationallevel)
    else:
        education_form = EducationalLevelForm()

    return render_to_response('demographic/demographic_education.html', {
                                    'object': object,
                                    'demographic_menu': True,
                                    'education_form': education_form,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('demographic.demographic_write')
def education_save(request, object_id):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    # check access by requested user
    if not _access_check(request, object) or object.is_company():
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if hasattr(object, 'educationallevel'):
        education_form = EducationalLevelForm(request.POST, instance=object.educationallevel)
    else:
        education_form = EducationalLevelForm(request.POST, instance=EducationalLevel())
    education = education_form.save(commit=False)
    education.client = object
    education.save()
    messages.success(request, _('Education saved successfully'))
    return render_to_response('demographic/demographic_education.html', {
                                        'object': object,
                                        'demographic_menu': True,
                                        'education_form': education_form,
                                        }, context_instance=RequestContext(request))

@permission_required_with_403('demographic.demographic_read')
def occupation(request, object_id, occupation_id=0):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object) or object.is_company():
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    occupation_object = get_object_or_None(Profession, id=occupation_id) or Profession()

    profession_form = ProfessionForm(instance=occupation_object)

    professions = [p for p in object.profession_set.all()]
    return render_to_response('demographic/demographic_occupation.html', {
                                    'object': object,
                                    'demographic_menu': True,
                                    'professions': professions,
                                    'profession_form': profession_form,
                                    'occupation': occupation_object,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('demographic.demographic_write')
def occupation_save(request, object_id, occupation_id=0):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    # check access by requested user
    if not _access_check(request, object) or object.is_company():
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    occupation_object = get_object_or_None(Profession, id=occupation_id) or Profession()
    profession_form = ProfessionForm(request.POST, instance=occupation_object)

    ocup = request.POST.get('ocup_class').replace('-','')

    # occupation found
    try:
        profession = profession_form.save(commit=False)
        profession.profession = Occupation.objects.get(cbo_code=ocup)
        profession.client = object
        profession.save()
        messages.success(request, _('Occupation saved successfully'))
        professions = [p for p in object.profession_set.all()]
        return render_to_response('demographic/demographic_occupation.html', {
                                        'object': object,
                                        'demographic_menu': True,
                                        'professions': professions,
                                        'profession_form': profession_form,
                                        }, context_instance=RequestContext(request))
    # occupation not found
    except:
        messages.error(request, _('Occupation not found'))
        professions = [p for p in object.profession_set.all()]
        return render_to_response('demographic/demographic_occupation.html', {
                                        'object': object,
                                        'demographic_menu': True,
                                        'professions': professions,
                                        'profession_form': profession_form,
                                        }, context_instance=RequestContext(request))
