# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.device.models import DeviceDetails, Device, DeviceType, DeviceDetailsForm, DeviceForm, DeviceTypeForm
from gestorpsi.organization.models import Organization

def index(request):
    """
    Returns details about all currently existing devices.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    """
    return render_to_response( "device/device_index.html", {'all_dev': Device.objects.all() } )

def save_device(request, object_id= ''):
    new_device= request.POST['description']
    new_device= Organization.objects.get( pk= request.POST['organization'] )
    new_device.save()
    return HttpResponse(new_device.id)

def form(request, device_id= '', device_details_id= ''):
    try: 
        device= get_object_or_404( Device, pk= device_id )
    except Http404:
        device= Device() #if there isn't such a device_id, a new device will be created
    
    try:
        device_details= get_object_or_404( DeviceDetails, pk= device_details_id )
    except Http404:
        device_details= DeviceDetails() #if there isn't such a device_details_id, a new 'device details' will be created
    
    return render_to_response('device/device_form.html', {'device': device, 'device_details': device_details } )
                     

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
        device_details= DeviceDetails()
        device_details.device= Device(); device= device_details.device
        device_details.device_type= DeviceType(); device_type= device_details.device_type            
          
    device_details.brand= request.POST[ 'brand' ]
    device_details.model= request.POST[ 'model' ] 
    device_details.part_number= request.POST[ 'part_number' ]
    device_details.durability= request.POST[ 'durability' ]
    device_details.lendable= request.POST[ 'lendable' ]
    device_details.room= Room.objects.get( pk= request.POST['room'] )
    device_details.comments= request.POST[ 'comments' ]
    #device information
    try:
        device= get_object_or_404( Device, pk= request.POST[ 'device' ])
    except Http404:
        device= Device()
        user = request.user
        device.description= ''
        device.organization = user.org_active 
        device.save()
        
    device_details.device= device
        
    device_details.save()
    return HttpResponse(device_details.id)


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