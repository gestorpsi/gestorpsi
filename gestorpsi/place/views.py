# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from gestorpsi.place.models import Place, PlaceForm, Room, RoomForm, RoomType, PlaceType
from gestorpsi.address.models import Address, AddressType, City
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.organization.models import Organization
from gestorpsi.address.views import address_save
from gestorpsi.phone.views import phone_save

def room_list( ids, descriptions, dimensions, room_types, furniture_descriptions ):
    """
    This I{helper} function view creates and returns a list of room based on a set of descriptions,
    dimensions, room types and furnitures' descriptions that are passed as parameter.
    @param descriptions: this is a list of descriptions which each of its elements will be used during the creation
    of the rooms.
    @type descriptions: a list of strings
    @param dimensions: this is a list of dimensions
    which each of its elements will be used during the creation
    of the rooms.
    @type dimensions: a list of integers
    @param room_types: this is a list of room types; these room types will be used during the creation of the rooms.
    @type room_types: a list of C{RoomType} instances.
    @param furniture_descriptions: a list of funiture descriptions to be used during the creation of the rooms.
    @type furniture_descriptions: a list of strings
    """
    rooms= []
    for i in range(0, len(descriptions)):
        if ( len( descriptions[i]) ):
            if not (dimensions[i]):
                dimensions[i] = None
            rooms.append( Room(id=ids[i], description= descriptions[i], dimension= dimensions[i], place= Place(), room_type= RoomType.objects.get(pk=room_types[i]), furniture= furniture_descriptions[i]) )
    return rooms

def index(request):
    """
    This view function returns a list that contains all places currently in the system.
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    """
    user = request.user
    print request.user
    print user.org_active
    return render_to_response( "place/place_index.html", {'object': Place.objects.filter(organization=user.org_active.id), 'PlaceTypes': PlaceType.objects.all(), 'countries': Country.objects.all(), 'RoomTypes': RoomType.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), } )

def form(request, object_id=''):
    try:
        user = request.user
        phones = []
        addresses = []
        rooms = []
        object= get_object_or_404(Place, pk=object_id)
        addresses= object.address.all()
        phones= object.phones.all()
        rooms= object.room_set.all()
        organization= Organization.objects.get(pk= user.org_active.id) # pk forcing to test view.
        #organization= Organization.objects.get(pk= a_place.organization_id ) # uncomment me, when organization is ready
    except (Http404, ObjectDoesNotExist):
        object= Place()
        place_type= PlaceType()
        #organization= Organization()
    return render_to_response('place/place_form.html', {'object': object, 'PlaceTypes': PlaceType.objects.all(), 
                                                        'organization': organization, 'addresses': addresses, 'phones': phones,
                                                        'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(),
                                                        'countries': Country.objects.all(),
                                                        'RoomTypes': RoomType.objects.all(),
                                                        'rooms': rooms, } )

def save(request, object_id=''):
    """
    This function view saves a place, its address, phones and rooms.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: it is the I{id} of the place that must be saved.
    @type object_id: an instance of the built-in type C{int}. 
    """
    try:
        object= get_object_or_404(Place, pk=object_id)
    except Http404:
        object= Place()

    object.label= request.POST['label']
    
    # is it visible?
    try:
        object.visible= get_visible( request.POST['visible'] )
    except:
        object.visible = False
        
    #place type
    object.place_type= PlaceType.objects.get( pk= request.POST[ 'place_type' ] )
    
    #organization ** will come from session **
    #object.organization= Organization.objects.get(pk= request.POST[ 'organization' ] )    
    #get organization from the user session
    user = request.user
    object.organization = user.org_active    
    object.save() 
    
    # save addresses (using Address APP)
    address_save(object, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
                 request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))
    
    # save phone numbers (using Phone APP)
    phone_save(object, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))
    
    save_rooms( object, request.POST.getlist( 'room_id' ), request.POST.getlist('description'), request.POST.getlist('dimension'), request.POST.getlist('room_type'), request.POST.getlist('furniture') )
    
    return HttpResponse(object.id)

def save_rooms( place, ids, descriptions, dimensions, room_types, furnitures ):

    for room in room_list( ids, descriptions, dimensions, room_types, furnitures ):
        result= is_equal( room )
        if result == -1:
            room.place= place
            room.save()
        elif result == 1:
            room_from_db= Room.objects.get(pk= room.id)
            room_from_db.description= room.description
            room_from_db.dimension= room.dimension
            room_from_db.room_type= room.room_type
            room_from_db.furnitures= room.furniture
            room_from_db.save() 

def is_equal(a_room):
    try:
        print "ROOM ID= %s" % a_room.id
        room_loaded_from_db= Room.objects.get( pk= a_room.id )
    except:
        return -1
    if cmp(room_loaded_from_db, a_room) == 0:
        return 0
    else:
        return 1

def delete(request, place_id):
    """
    This function view search for a place which has the id equals to the C{int} (I{place_id})
    passed as parameter. If there is such a place, it will be deleted; otherwise
    it notifies that the operation has not been carried out.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param place_id: represents the I{id} of the place to be deleted.
    @type place_id: an instance of the built-in class c{int}.
    """
    try:
        place= Place.objects.get( pk=place_id)
        place.delete()
        return render_to_response( 'place/place_msg.html', { 'msg': "It was successfully deleted" } )
    except Place.DoesNotExist:
        return render_to_response( 'place/place_msg.html', { 'msg': "Some problem occurred while deleting the place (or a place with id equal to %s does not exist)" % place_id } )
    
def add_room(request, place_id):
    """
    This function view adds a I{empty} (filled with default values) room to the place which has the I{id} equals to I{place_id}.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param place_id: represents the I{id} of the place which the empty room will be added.
    @type place_id: an instance of the built-in class c{int}. 
    """
    a_place= load_place( place_id )
    room= Room( description= '', dimension= '', place= a_place, room_type= RoomType(), furniture= '' )
    room_form= RoomForm( instance= room )
    return render_to_response( 'place/add_room.html', locals() )

###TODO: this function view yet uses form to perform its functionality, thus those implementation must be changed
def save_room(request, id_object=''):
    """
    This function view search for a place with the id equals to I{id_object}. If there is a place
    with id equals to I{id_object}, a room is created and initialized using values retrieved of the
    I{request} object and associated to the place which has the id equals to I{id_object}.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param place_id: represents the I{id} of the place which the room will be associated.
    @type place_id: an instance of the built-in class c{int}.
    """
    try:
        get_object_or_404( Place, pk= id_object)
    except:
        return render_to_response( 'place/place_msg.html', { 'msg': "some problem occurred while saving the room" } )
    
    try:
        print 'chamou save_room'
        print request.POST[ 'room_id' ]
        room= get_object_or_404(Room, pk= request.POST['room_id'] )
    except:
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
    """
    Returns all rooms belonging to the place that has the id equals to the integer
    passed as parameter.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param place_id: the id of the place.
    @type place_id: an instance of the built-in class c{int}.
    """
    room_list= []
    for room in Room.objects.filter( place__id__exact= int(place_id) ):
        room_list.append( RoomForm( instance= room ) )
    return render_to_response( 'place/list_of_rooms.html', { 'room_list': room_list } ) 

def delete_room(request, room_id):
    """
    Deletes the room which has the id equals to I{room_id}.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param room_id: the id of the room to be deleted.
    @type room_id: an instance of the built-in class c{int}.
    """
    try:
        room= Room.objects.get( pk= room_id )
        room.delete()
        return render_to_response( 'place/place_msg.html', { 'msg': "It was successfully deleted" } )
    except Room.DoesNotExist:
        return render_to_response( 'place/place_msg.html', { 'msg': "Some problem occurred while deleting the room (or a place with id equal to %s does not exist)" % room_id } )

def get_room(request, id_object):
    """
    If there is a room with id equals to I{room_id}, this function view retrieves and shows it.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param room_id: the id of the room.
    @type room_id: an instance of the built-in class c{int}.
    """
    try:
        a_room= Room.objects.get( pk= int(id_object) )
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
    """
    Loads the place with id equals to I{place_id}
    @param place_id: the id of the place.
    @type place_id: an instance of the built-in class c{int}.
    """
    return get_object_or_404(Place, pk=place_id)

def get_visible( value ):
    """
    It is a helper function view used to handle the values I{'on'} and I{'off'}. If I{'on'} is passed to this function view
    it returns C{True}, otherwise it returns C{False}.
    @param value: a value, I{'on'} or I{'off'}.
    @type value: a string that contains one of the following values: I{'on'} or I{'off'}.
    """
    if ( value == 'on' ):
        return True
    else:
        return False 
