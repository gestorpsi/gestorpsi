from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
#from django.newforms import form_for_model, form_for_instance
from django.core.exceptions import ObjectDoesNotExist
from gestorpsi.place.models import Place, PlaceForm, Room, RoomForm, RoomType, PlaceType
from gestorpsi.address.models import Address, AddressType, City
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.phone.views import phoneList
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.address.views import addressList
from gestorpsi.organization.models import Organization

def roomList( descriptions, dimensions, room_types, furniture_descriptions ):
    total= len(descriptions)
    rooms= []
    for i in range(0, total):
        if ( len( descriptions[i]) ):
            if not (dimensions[i]):
                dimensions[i] = None
            rooms.append( Room(description= descriptions[i], dimension= dimensions[i], place= Place(), room_type= RoomType.objects.get(pk=room_types[i]), furniture= furniture_descriptions[i]) )
    return rooms

def index(request):
    return render_to_response( "place/place_index.html", {'object': Place.objects.all(), 'PlaceTypes': PlaceType.objects.all(), 'countries': Country.objects.all(), 'RoomTypes': RoomType.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , } )

#######################SHOULD BE TESTED (waiting feedback from cuzido)
def form(request, object_id=0 ):
    try:
        phones = []
        addresses = []
        rooms = []
        object= get_object_or_404(Place, pk=object_id)
        
        #get all address
        addresses= object.address.all()
        
        #get all related phones
        phones= object.phones.all()
        
        #get all related rooms
        rooms= object.room_set.all()
        
        #place_type= PlaceType.objects.get( pk= a_place.place_type_id ) # commented by czd. sending it directly to template as: 'place_type': PlaceType.objects.all()
        
        organization= Organization.objects.get(pk= 1 ) # pk forcing to test view.
        #organization= Organization.objects.get(pk= a_place.organization_id ) # uncomment me, when organization is ready
        
    except (Http404, ObjectDoesNotExist): #new instances will be created if there is no place or organization
        object= Place()
        place_type= PlaceType()
        organization= Organization()
    return render_to_response('place/place_form.html', {'object': object, 'PlaceTypes': PlaceType.objects.all(), 
                                                        'organization': organization, 'addresses': addresses, 'phones': phones,
                                                        'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(),
                                                        'countries': Country.objects.all(),
                                                        'RoomTypes': RoomType.objects.all(),
                                                        'rooms': rooms,
                                                        } )

######### newforms not available Django version 1.0-alpha_2-SVN-8327
###TODO#######################
def add(request):
    place_form= PlaceForm()
    AddressForm= None  ### form_for_model( Address )
    address_form= AddressForm()
    PhoneForm= None ###form_for_model( Phone )
    phone_form= PhoneForm()
    return render_to_response( 'place/place_add.html', locals() )

#######################SHOULD BE TESTED (waiting feedback from cuzido)
def save(request, object_id= 0):
    try:
        object= get_object_or_404(Place, pk=object_id)
    except Http404:
        object= Place()
        
    # place label (name)
    object.label= request.POST['label']
    
    # is it visible
    try:
        object.visible= get_visible( request.POST['visible'] )
    except:
        object.visible = False
        
    #place type
    object.place_type= PlaceType.objects.get( pk= request.POST[ 'place_type' ] )
    
    #organization ** will come from session **
    #object.organization= Organization.objects.get(pk= request.POST[ 'organization' ] )
    
    object.save() 
    
    # flush addresses and re-insert it
    object.address.all().delete()
    for address in addressList(request.POST.getlist('addressPrefix'), request.POST.getlist('addressLine1'), 
                               request.POST.getlist('addressLine2'), request.POST.getlist('addressNumber'),
                               request.POST.getlist('neighborhood'), request.POST.getlist('zipCode'), 
                               request.POST.getlist('addressType'), request.POST.getlist('city'),
                               request.POST.getlist('foreignCountry'), request.POST.getlist('foreignState'),
                               request.POST.getlist('foreignCity')):
        address.content_object = object
        address.save()
    
    object.phones.all().delete()    
    for phone in phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType')):
        phone.content_object= object
        phone.save()
        
    rooms= object.room_set.all()
    #delete all rooms and...
    for room in rooms:
        room.delete()
    #create new ones
    for room in roomList( request.POST.getlist('description'), request.POST.getlist('dimension'), request.POST.getlist('room_type'),
                               request.POST.getlist('furniture') ):
        room.place= object
        room.save()
    
    return HttpResponse(object.id)

#######################SHOULD BE TESTED (waiting feedback from cuzido)
def delete(request, place_id):
    try:
        place= Place.objects.get( pk= int(place_id) )
        place.delete()
        return render_to_response( 'place/place_msg.html', { 'msg': "It was successfully deleted" } )
    except Place.DoesNotExist:
        return render_to_response( 'place/place_msg.html', { 'msg': "Some problem occurred while deleting the place (or a place with id equal to %s does not exist)" % place_id } )

def get(request, place_id):
    try:
        a_place= Place.objects.get( pk= int(place_id) )
        place_form= PlaceForm( instance= a_place )
        
        #get all address
        addresses= a_place.address.all()
        address_forms= []
        for address in addresses:
            address_forms.append( AddressForm( instance= address ) )
        #get all phones
        phones= a_place.phones.all()
        phones_forms= []
        for ph in phones:
            phones_forms.append( PhoneForm( instance= ph ) )
            
    except Place.DoesNotExist:
        return render_to_response( 'place/place_msg.html', { 'msg': "A place with id equal to %s does not exist, thus it could not be updated" % place_id } )
    else: 
        return render_to_response( 'place/place_update.html', { 'place_form': place_form, 'a_place': a_place, 'addresses': addresses, 'address_forms': address_forms, 'phones': phones, 'phones_forms': phones_forms } )
    
def add_room(request, place_id):
    a_place= load_place( place_id )
    room= Room( description= '', dimension= '', place= a_place, room_type= RoomType(), furniture= '' )
    room_form= RoomForm( instance= room )
    return render_to_response( 'place/add_room.html', locals() )

###TODO: this method yet uses form to perform its functionality, thus those implementation must be changed
def save_room(request, id_object):
    
    try:
        get_object_or_404( Place, pk= id_object)
    except:
        return render_to_response( 'place/place_msg.html', { 'msg': "some problem occurred while saving the room" } )
    
    print "method save_room"
    print id_object
    room= Room()
    room.description= request.POST['description']
    room.dimension= request.POST['dimension']
    room.place= Place.objects.get(pk= id_object)
    room.room_type= RoomType.objects.get(pk= request.POST['room_type'] )
    room.furniture= request.POST['furniture']
    room.save()
    object= Place.objects.all()
    return render_to_response( "place/place_index.html", locals() )

def list_rooms_related_to(request, place_id):
    room_list= []
    for room in Room.objects.filter( place__id__exact= int(place_id) ):
        room_list.append( RoomForm( instance= room ) )
    return render_to_response( 'place/list_of_rooms.html', { 'room_list': room_list } ) 

def delete_room(request, room_id):
    try:
        room= Room.objects.get( pk= int(room_id) )
        room.delete()
        return render_to_response( 'place/place_msg.html', { 'msg': "It was successfully deleted" } )
    except Room.DoesNotExist:
        return render_to_response( 'place/place_msg.html', { 'msg': "Some problem occurred while deleting the room (or a place with id equal to %s does not exist)" % room_id } )

def get_room(request, room_id ):
    try:
        a_room= Room.objects.get( pk= int(room_id) )
        room_form= RoomForm( instance= a_room )
    except Room.DoesNotExist:
        return render_to_response( 'place/place_msg.html', { 'msg': "A room with id equal to %s does not exist, thus it could not be updated" % room_id } )
    else: 
        return render_to_response( 'place/room_update.html', { 'room_form': room_form, 'a_room': a_room } )
    
def update_room(request, room_id):
    a_room= get_object_or_404(Room, pk=room_id) 
    room_form= RoomForm( request.POST, instance= a_room )
    if room_form.is_valid():
        room_form.save()
        return render_to_response( 'place/place_msg.html', { 'msg': "It was successfully updated" } )
    else:
        return render_to_response( 'place/place_msg.html', { 'msg': "some problem occurred while updating the room" } )

def load_place( place_id ):
    return get_object_or_404(Place, pk=place_id)

def get_visible( value ):
    if ( value == 'on' ):
        return True
    else:
        return False 
