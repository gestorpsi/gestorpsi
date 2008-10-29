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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from gestorpsi.organization.models import Organization
from gestorpsi.place.models import Place, Room, RoomType, PlaceType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.address.views import address_save
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.phone.views import phone_save

def index(request):
    user = request.user
    return render_to_response( "place/place_index.html", {'object': Place.objects.filter(organization=user.org_active.id),
                                                          'PlaceTypes': PlaceType.objects.all(),
                                                          'countries': Country.objects.all(),
                                                          'RoomTypes': RoomType.objects.all(),
                                                          'PhoneTypes': PhoneType.objects.all(),
                                                          'AddressTypes': AddressType.objects.all(), } )


def room_list( ids, descriptions, dimensions, room_types, furniture_descriptions ):
    rooms= []
    for i in range(0, len(descriptions)):
        if ( len( descriptions[i]) ):
            if not (dimensions[i]):
                dimensions[i] = None
            rooms.append( Room(id = ids[i],
                               description = descriptions[i],
                               dimension = dimensions[i],
                               place = Place(),
                               room_type = RoomType.objects.get(pk=room_types[i]),
                               furniture = furniture_descriptions[i]) )
    return rooms


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
        organization= Organization.objects.get(pk= user.org_active.id)
        last_update = object.history.latest('_audit_timestamp')._audit_timestamp
    except (Http404, ObjectDoesNotExist):
        object= Place()
        place_type= PlaceType()
    return render_to_response('place/place_form.html', {'object': object,
                                                        'PlaceTypes': PlaceType.objects.all(), 
                                                        'organization': organization,
                                                        'addresses': addresses,
                                                        'phones': phones,
                                                        'PhoneTypes': PhoneType.objects.all(),
                                                        'AddressTypes': AddressType.objects.all(),
                                                        'countries': Country.objects.all(),
                                                        'RoomTypes': RoomType.objects.all(),
                                                        'rooms': rooms,
                                                        'last_update': last_update, } )

def save(request, object_id=''):
    user = request.user
    try:
        object = get_object_or_404(Place, pk=object_id)
    except Http404:
        object = Place()

    try:
        object.visible= get_visible( request.POST['visible'] )
    except:
        object.visible = False
    object.label = request.POST['label']
    object.place_type= PlaceType.objects.get( pk= request.POST[ 'place_type' ] )
    object.organization = user.org_active    
    object.save() 

    save_rooms( object, request.POST.getlist( 'room_id' ), request.POST.getlist('description'), request.POST.getlist('dimension'), request.POST.getlist('room_type'), request.POST.getlist('furniture') )
    phone_save(object, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))
    address_save(object, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
                 request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))

    return HttpResponse(object.id)

def save_rooms(place, ids, descriptions, dimensions, room_types, furnitures):
    place.room_set.all().delete()
    for room in room_list( ids, descriptions, dimensions, room_types, furnitures ):
        room.place = place
        room.save()

#def save_rooms( place, ids, descriptions, dimensions, room_types, furnitures ):
#    for room in room_list( ids, descriptions, dimensions, room_types, furnitures ):
#        result = is_equal( room )
#        if result == -1:
#            room.place = place
#            room.save()
#        elif result == 1:
#            room_from_db = Room.objects.get(pk= room.id)
#            room_from_db.description = room.description
#            room_from_db.dimension = room.dimension
#            room_from_db.room_type = room.room_type
#            room_from_db.furnitures = room.furniture
#            room_from_db.save() 

def is_equal(a_room):
    try:
        room_loaded_from_db = Room.objects.get( pk= a_room.id )
    except:
        return -1
    
    if cmp(room_loaded_from_db, a_room) == 0:
        return 0
    else:
        return 1

def get_visible( value ):
    if ( value == 'on' ):
        return True
    else:
        return False 