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

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.device.models import DeviceDetails, Device, DeviceType
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, Profession, ProfessionalProfile, LicenceBoard, ProfessionalIdentification, CareProfessional
from gestorpsi.careprofessional.views import PROFESSIONAL_AREAS
from gestorpsi.place.models import Place

def index(request):
    """
    Returns details about all currently existing devices.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    """
    user = request.user
    return render_to_response( "device/device_index.html", {'object': Device.objects.all(),
                                                            'organizations': Organization.objects.all(),
                                                            'places': Place.objects.filter(organization=user.org_active.id), 
                                                            'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS } )

def form(request, object_id= ''):
    user = request.user
    try:
        device_details = get_object_or_404( DeviceDetails, pk= object_id )
    except Http404:
        device_details= DeviceDetails()
    return render_to_response('device/device_form.html', {'object': Device.objects.all(), 
                                                          'device_details': device_details,
                                                          'organizations': Organization.objects.all(), 
                                                          'places': Place.objects.filter(organization=user.org_active.id),                                                          
                                                          'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS } )

#def form(request, object_id= ''):
#    """
#    This function views creates some I{forms objects} based on the I{object_id} passed, these I{forms} are
#    used to organize and easier the presentation of the information.
#    @param request: this is a request sent by the browser.
#    @type request: an instance of the class C{HttpRequest} created by the framework Django.
#    @param object_id: the id of the C{DeviceDetails} instance which the information will be displayed.
#    @type object_id: an instance of the built-in class c{int}.
#    """
#    try :
#        object= get_object_or_404( DeviceDetails, pk= object_id )
#        device= object.device
#        device_type= object.device_type
#    except ObjectDoesNotExist:
#        object= DeviceDetails()
#        object.device= Device(); device= object.device
#        object.device_type= DeviceType(); device_type= object.device_type
#    
#
#    device_categ= Device.objects.all()
#    device_type= DeviceType.objects.all()
#    list_of_dev_details= DeviceDetails.objects.all()
#    
#    return render_to_response('device/device_form.html', {'object': object, 'device': device, 'device_type': device_type, 
#                                                          'dc': device_categ, 'dt': device_type,
#                                                          'list_dvt': list_of_dev_details } )

def save_device(request):
    user = request.user
    device = Device()
    device.description = request.POST['label']
    device.organization = user.org_active
    device.save()
    return HttpResponse(device.id)

def save(request, object_id='' ):
    print "entrando no save!!!!!!!!  [%s]  " % object_id
    """
    This function view creates an instance of the class C{DeviceDetails} with id equals to I{object_id} and
    uses the I{request} object to set the newly created class attributes. If there is some C{DeviceDetails}
    with id equals to I{object_id} then this instance is updated with the I{request} information.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: the id of the C{DeviceDetails} instance to be saved or updated.
    @type object_id: an instance of the built-in class c{int}.
    """
    
    try:
        device_details= get_object_or_404( DeviceDetails, pk=object_id)
    except Http404:
        device_details = DeviceDetails()

    device_details.device = get_object_or_404(Device, pk=request.POST['select_device'])
    device_details.brand = request.POST[ 'brand' ]
    device_details.model = request.POST[ 'model' ] 
    device_details.part_number = request.POST[ 'part_number' ]
    device_details.comments = request.POST[ 'comments' ]
    try:
        device_details.lendable = get_visible( request.POST['lendable'] )
    except:
        device_details.lendable = False
        
    device_details.device = get_object_or_404( Device, pk=request.POST['select_device'])
    device_details.save()

#    device_details.room= Room.objects.get( pk= request.POST['room'] )
#    device_details.durability= request.POST[ 'durability' ]

    return HttpResponse(device_details.id)

def get_visible( value ):
    if ( value == 'on' ):
        return True
    else:
        return False
     
def delete(request, object_id= ''):
    """
    This function view deletes the C{DeviceDetails} which has the id equals to I{object_id}.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: the id of the C{DeviceDetails} instance to be deleted.
    @type object_id: an instance of the built-in class c{int}.
    """
    try:
        device_details= get_object_or_404( DeviceDetails, pk=object_id)
        device_details.delete()
    except Http404:
        pass
    return render_to_response('device/device_form.html', {'list_of_device_details': DeviceDetails.objects.all() })   