from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.device.models import DeviceDetails, Device, DeviceType, DeviceDetailsForm, DeviceForm, DeviceTypeForm

def index(request):
    list_of_device_details= DeviceDetails.objects.all()
    return render_to_response( "device/device_form.html", {'list_of_device_details': list_of_device_details } )

def form(request, object_id= 0):
    try :
        object= get_object_or_404( DeviceDetails, pk= object_id )
        device= object.device
        device_type= object.device_type
    except ObjectDoesNotExist:
        object= DeviceDetails()
        object.device= Device(); device= object.device
        object.device_type= DeviceType(); device_type= object.device_type
    
    device_details_form= DeviceDetailsForm( instance= object )
    device_form= DeviceForm( instance= device )
    device_type_form= DeviceTypeForm( instance= device_type )
    
    return render_to_response('device/device_html.html', {'object': object, 'device': device, 'device_type': device_type, 
                                                          'device_details_form':device_details_form, 'device_form': device_form, 
                                                          'device_type_form': device_type_form } )
    
def save(request, object_id=0 ):
    try:
        device_details= get_object_or_404( DeviceDetails, pk=object_id)
    except Http404:
        object= DeviceDetails()
        object.device= Device(); device= object.device
        object.device_type= DeviceType(); device_type= object.device_type
        
    device_details.brand= request.POST[ 'brand' ]
    device_details.model= request.POST[ 'model' ] 
    device_details.part_number= request.POST[ 'part_number' ]
    device_details.comments= request.POST[ 'comments' ]
    #device information
    device_description= request.POST[ 'description' ]
    device_total_quantity= request.POST[ 'total_quantity' ]
    device_available_quantity= request.POST[ 'available_quantity' ]
    
    if ( device_details.device != None ):
        device_details.device.description= device_description
        device_details.device.total_quantity= device_total_quantity
        device_details.device.available_quantity= device_available_quantity
    else:
        a_device= Device()
        a_device.description= device_description
        a_device.total_quantity= device_total_quantity
        a_device.available_quantity= device_available_quantity
        a_device.save()
        device_details.device= a_device
    
    #device type information
    device_type_durability= request.POST[ 'durability' ]
    device_type_mobility= request.POST[ 'mobility' ]
    device_type_restriction= request.POST[ 'restriction' ]
    
    if ( device_details.device_type != None ):
        device_details.device_type.durability = device_type_durability
        device_details.device_type.mobility = device_type_mobility
        device_details.device_type.restriction= device_type_restriction
        device_details.device_type.save()
    else:
        device_type= DeviceType()
        device_type.durability= device_type_durability
        device_type.mobility= device_type_mobility
        device_type.restriction= device_type_restriction
        device_type.save()
        device_details.device_type= device_type
    
    device_details.save()
    return render_to_response('device/device_form.html', {'list_of_device_details': [ device_details ] })

def delete(request, object_id= 0):
    try:
        device_details= get_object_or_404( DeviceDetails, pk=object_id)
        device_details.delete()
    except Http404:
        pass
    return render_to_response('device/device_form.html', {'list_of_device_details': DeviceDetails.objects.all() })   