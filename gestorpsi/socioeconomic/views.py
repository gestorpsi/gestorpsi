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

from gestorpsi.socioeconomic.forms import TransportationForm, IncomeForm, IncomeSourceForm, PossessionForm, EletricityForm
from gestorpsi.socioeconomic.forms import SanitationForm, PavingForm, DwellingFeaturesForm, PeopleHouseholdForm
from gestorpsi.socioeconomic.models import Transportation

@permission_required_with_403('client.client_read')
def socioeconomic_home(request, object_id):
    object = get_object_or_404(Client, pk=object_id)
    transportations = [t for t in object.transportation_set.all()]
    try:
        possessions = object.housing.possession_set.all()
    except:
        possessions = None
    
    try:
        people_household = object.housing.peoplehousehold
    except:
        people_household = None
    
    try:
        dwelling = object.housing.dwellingfeatures
    except:
        dwelling = None
    
    try:
        paving = object.housing.paving
    except:
        paving = None
    
    try:
        sanitation = object.housing.sanitation
    except:
        sanitation = None
    
    try:
        eletricity = object.housing.eletricity
    except:
        eletricity = None


    return render_to_response('client/client_socioeconomic.html', {
                                        'object': object,
                                        'socioeconomic_menu': True,
                                        'transportations': transportations,
                                        'possessions': possessions,
                                        'people_household': people_household,
                                        'dwelling': dwelling,
                                        'paving': paving,
                                        'sanitation': sanitation,
                                        'eletricity': eletricity,
                                        }, context_instance=RequestContext(request))

@permission_required_with_403('client.client_read')
def socioeconomic_transportation(request, object_id, transportation_id=0):
    object = get_object_or_404(Client, pk=object_id)
    transportation_object = get_object_or_None(Transportation, id=transportation_id) or Transportation()
    transportation_form = TransportationForm(instance=transportation_object)
    transportations = [t for t in object.transportation_set.all()]
    return render_to_response('client/client_socio_transportation.html', {
                                        'object': object,
                                        'socioeconomic_menu': True,
                                        'transportations': transportations,
                                        'transportation_form': transportation_form,
                                        }, context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def socioeconomic_transportation_save(request, object_id, transportation_id=0):
    object = get_object_or_404(Client, pk=object_id)
    transportation_object = get_object_or_None(Transportation, id=transportation_id) or Transportation()
    transportation_form = TransportationForm(request.POST, instance=transportation_object)
    transp = transportation_form.save(commit=False)
    transp.client = object
    transp.save()
    transportations = [t for t in object.transportation_set.all()]
    request.user.message_set.create(message=_('Transportation saved successfully'))
    return render_to_response('client/client_socio_transportation.html', {
                                        'object': object,
                                        'socioeconomic_menu': True,
                                        'transportations': transportations,
                                        'transportation_form': transportation_form,
                                        }, context_instance=RequestContext(request))

