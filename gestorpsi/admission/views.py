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

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from gestorpsi.client.models import Client
from gestorpsi.careprofessional.models import LicenceBoard, CareProfessional
from gestorpsi.careprofessional.views import PROFESSIONAL_AREAS

def form(request, object_id=''):
    object    = get_object_or_404(Client, pk=object_id)  
    return render_to_response('client/client_admission.html', {
        'object': object,
        'CareProfessionals': CareProfessional.objects.all(),
        'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,
        'licenceBoardTypes': LicenceBoard.objects.all(),
    })
