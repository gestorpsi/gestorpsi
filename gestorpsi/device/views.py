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
from django.template import RequestContext
from gestorpsi.device.models import DeviceDetails, Device
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.views import PROFESSIONAL_AREAS
from gestorpsi.place.models import Place, Room

@permission_required('device.device_list', '/')
def index(request):
    """
    Returns details about all currently existing devices.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    """
    user = request.user
    return render_to_response( "device/device_index.html", {'object': Device.objects.filter(organization=user.get_profile().org_active),
                                                            'places': Place.objects.filter(organization=user.get_profile().org_active), 
                                                            'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS },
                                                            context_instance=RequestContext(request))

@permission_required('device.device_read', '/')
def form(request, object_id= ''):
    user = request.user
    try:
        device_details = get_object_or_404( DeviceDetails, pk= object_id )
    except Http404:
        device_details= DeviceDetails()
    return render_to_response('device/device_form.html', {'object': Device.objects.filter(organization=user.get_profile().org_active),
                                                          'device_details': device_details,
                                                          'places': Place.objects.filter(organization=user.get_profile().org_active.id),                                                          
                                                          'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS },
                                                          context_instance=RequestContext(request))

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

@permission_required('device.device_list', '/')
def index_type(request):
    return render_to_response( "device/device_type_list.html", {'object': Device.objects.filter(organization=user.get_profile().org_active), }, context_instance=RequestContext(request))

@permission_required('device.device_read', '/')
def form_type(request, object_id= ''):
    return render_to_response('device/device_type_form.html', {'object': get_object_or_404( Device, pk=object_id) }, context_instance=RequestContext(request) )

@permission_required('device.device_write', '/')
def save_device(request, object_id= ''):
    try:
        device= get_object_or_404( Device, pk=object_id)
    except Http404:
        device = Device()

    user = request.user
    device.description = request.POST.get('label')
    device.organization = user.get_profile().org_active
    device.save()
    return HttpResponse(device.id)

@permission_required('device.device_write', '/')
def save(request, object_id='' ):
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

    device_details.device = get_object_or_404(Device, pk=request.POST.get('select_device'))
    device_details.brand = request.POST.get('brand')
    device_details.model = request.POST.get('model')
    device_details.part_number = request.POST.get('part_number')
    device_details.comments = request.POST.get('comments')
    device_details.lendable = get_visible(request.POST.get('lendable'))
    device_details.device = get_object_or_404(Device, pk=request.POST.get('select_device'))
    
    """ Device Durability """
    device_details.durability = request.POST.get('select_durability_type')

    """ Device Restriction """
    if request.POST['select_restriction_type'] == '2':
        device_details.prof_restriction = request.POST.get('professional_area')
    else:
        device_details.prof_restriction = ''

    """ Device Mobility """
    mobility = request.POST.get('select_mobility_type')
    device_details.mobility = mobility
    device_details.place = get_object_or_404(Place, pk=request.POST.get('place_associated'))
    device_details.room = get_object_or_404(Room, pk=request.POST.get('room_associated'))
    device_details.save()
    return HttpResponse(device_details.id)

def get_visible(value):
    if (value == 'on'):
        return True
    else:
        return False
     
def delete(request, object_id= ''):
    pass
#    """
#    This function view deletes the C{DeviceDetails} which has the id equals to I{object_id}.
#    @param request: this is a request sent by the browser.
#    @type request: an instance of the class C{HttpRequest} created by the framework Django.
#    @param object_id: the id of the C{DeviceDetails} instance to be deleted.
#    @type object_id: an instance of the built-in class c{int}.
#    """
#    try:
#        device_details= get_object_or_404( DeviceDetails, pk=object_id)
#        device_details.delete()
#    except Http404:
#        pass
#    return render_to_response('device/device_form.html', {'list_of_device_details': DeviceDetails.objects.all() })
