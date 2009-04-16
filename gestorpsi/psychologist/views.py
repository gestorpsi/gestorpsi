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
from django.contrib.auth.decorators import permission_required
from gestorpsi.psychologist.models import Psychologist
from gestorpsi.careprofessional.views import care_professional_fill

# *********************** THIS FUNCTION IS NECESSARY ???????
def index(request):
    """
    This view function returns a list that contains all psychologists currently in the system.
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    """
    user = request.user
    
    return render_to_response('psychologist/psychologist_index.html', {'object': Psychologist.objects.filter(person__organization = user.get_profile().org_active.id, active = True)})
    

# *********************** THIS FUNCTION IS NECESSARY ???????
def form(request, object_id=''):
    """
    This function view creates a psychologist form. If the object_id has a value, this form will be fill with psychologist information.
    otherwise, a new form will be create
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: it is the I{id} of the psychologist that must be saved.
    @type object_id: an instance of the built-in type C{int}. 
    """
    try:
        phones = []
        addresses = []
        object = get_object_or_404(Psychologist, pk=object_id)
        phones= object.person.phones.all()
        addresses= object.person.address.all()               
        person = Person.objects.filter(id=object.person_id)
    except:
        object = Psychologist()

    return render_to_response('psychologist/psychologist_form.html', {
                                    'object': object,
                                    'phones': phones, 
                                    'countries': Country.objects.all(), 
                                    'PhoneTypes': PhoneType.objects.all(), 
                                    'AddressTypes': AddressType.objects.all(), 
                                    'States': State.objects.all(), })

# Save or Update psychpsychologistologist object
@permission_required('professional.professional_write', '/')
def save(request, object_id=''):    

    try:
        object = get_object_or_404(Psychologist, pk=object_id)        
    except Http404:
        object = Psychologist()

    object = care_professional_fill(request, object)
    object.save()

    return HttpResponse(object.id)

# delete (disable) a psychologist
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
    return render_to_response('psychologist/psychologist_index.html', {'object': Psychologist.objects.all().filter(active = True)})
