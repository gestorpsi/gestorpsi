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

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from gestorpsi.psychologist.models import Psychologist
from gestorpsi.careprofessional.views import care_professional_fill
from gestorpsi.util.decorators import permission_required_with_403

# Save or Update psychpsychologistologist object
@permission_required_with_403('careprofessional.careprofessional_write')
def save(request, object_id=''):    

    try:
        object = get_object_or_404(Psychologist, pk=object_id)        
    except Http404:
        object = Psychologist()

    object = care_professional_fill(request, object)
    object.save()

    request.user.message_set.create(message=_('Professional saved successfully'))

    return HttpResponseRedirect('/careprofessional/%s/' % object.id)


# disable a psychologist
@permission_required_with_403('careprofessional.careprofessional_write')
def delete(request, object_id):
    """
    This function view search for a psychologist which has the id equals to the C{int} (I{psychologist_id})
    passed as parameter and change the field I{active} to "False' 
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: represents the I{id} of the psychologist to be deleted.
    @type object_id: an instance of the built-in class C{int}.
    """
    object = get_object_or_404(Psychologist, pk=object_id)
    object.active = False
    object.save()    
    return HttpResponse()
