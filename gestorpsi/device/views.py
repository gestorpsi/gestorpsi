# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.device.models import DeviceDetails, Device, DeviceType, DeviceDetailsForm, DeviceForm, DeviceTypeForm

def index(request):
    """
    Returns details about all currently existing devices.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    """
    list_of_device_details= []
    for device in Device.objects.all():
        details= {}
        details['device']= device
        #total
        details['total']= len( DeviceDetails.objects.filter( device__id= device.id ) )
        #available
        details['available']= len( DeviceDetails.objects.filter( device__id= device.id, active= False ) )
        details['dt']= DeviceDetails.objects.all().filter( device= device.id )
        list_of_device_details.append( details )
         
    return render_to_response( "device/device_index.html", {'object': list_of_device_details, 'device_types': DeviceType.objects.all()} )

def form(request, object_id= ''):
    """
    This function views creates some I{forms objects} based on the I{object_id} passed, these I{forms} are
    used to organize and easier the presentation of the information.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: the id of the C{DeviceDetails} instance which the information will be displayed.
    @type object_id: an instance of the built-in class c{int}.
    """
    

    try :
        object= get_object_or_404( DeviceDetails, pk= object_id )
        device= object.device
        device_type= object.device_type
    except ObjectDoesNotExist:
        object= DeviceDetails()
        object.device= Device(); device= object.device
        object.device_type= DeviceType(); device_type= object.device_type
    

    device_categ= Device.objects.all()
    device_type= DeviceType.objects.all()
    list_of_dev_details= DeviceDetails.objects.all()
    
    return render_to_response('device/device_form.html', {'object': object, 'device': device, 'device_type': device_type, 
                                                          'dc': device_categ, 'dt': device_type,
                                                          'list_dvt': list_of_dev_details } )
    
#def device_list(request, object_id= ''):
#    try:
#        device= Device.objects.get(pk= object_id)
#    except:
#        device= Device()
#    
#    list_of_dev_details= DeviceDetails.objects.all().filter( device= device.id )
#   return render_to_response('device/device_list_details.html', { 'object': list_of_dev_details } )

    
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
    device_details.comments= request.POST[ 'comments' ]
    #device information
    print "POST= %s" % request.POST
    try:
        device= get_object_or_404( Device, pk= request.POST[ 'device' ])
    except Http404:
        device= Device()
        device.description= ''
        device.save()
    
    print device 
    device_details.device= device
    
    #device type information
    #device_type_durability= request.POST[ 'durability' ]
    #device_type_mobility= request.POST[ 'mobility' ]
    #device_type_restriction= request.POST[ 'restriction' ]
    
    try:
        device_type= get_object_or_404( DeviceType, pk= request.POST[ 'select_device_type' ])
    except Http404:
        device_type= DeviceType()
        device_type.durability= '1'
        device_type.mobility= '1'
        device_type;restriction= 'none'
        device_type.save()
    
    device_details.device_type= device_type    
    device_details.save()
    #return render_to_response('device/device_form.html', {'list_of_device_details': [ device_details ] })
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