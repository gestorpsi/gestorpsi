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

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.core.paginator import Paginator
from django.utils import simplejson
from gestorpsi.organization.models import Organization
from gestorpsi.place.models import Place, Room, RoomType, PlaceType
from gestorpsi.address.models import Country, AddressType, State
from gestorpsi.address.views import address_save
from gestorpsi.phone.models import PhoneType
from gestorpsi.phone.views import phone_save
from gestorpsi.util.decorators import permission_required_with_403

@permission_required_with_403('place.place_list')
def index(request):
    user = request.user
    return render_to_response( "place/place_index.html", {
                                                          'PlaceTypes': PlaceType.objects.all(),
                                                          'countries': Country.objects.all(),
                                                          'RoomTypes': RoomType.objects.all(),
                                                          'PhoneTypes': PhoneType.objects.all(),
                                                          'AddressTypes': AddressType.objects.all(),
                                                          'States': State.objects.all(),
                                                          },
                                                          context_instance=RequestContext(request))

@permission_required_with_403('place.place_list')
def list(request, page = 1):
    user = request.user
    object = Place.objects.filter(organization=user.get_profile().org_active.id)
    
    object_length = len(object)
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)

    array = {} #json
    i = 0

    array['util'] = {
        'has_perm_read': user.has_perm('place.place_read'),
        'paginator_has_previous': object.has_previous().real,
        'paginator_has_next': object.has_next().real,
        'paginator_previous_page_number': object.previous_page_number().real,
        'paginator_next_page_number': object.next_page_number().real,
        'paginator_actual_page': object.number,
        'paginator_num_pages': paginator.num_pages,
        'object_length': object_length,
    }

    
    array['paginator'] = {}
    for p in paginator.page_range:
        array['paginator'][p] = p
    
    for o in object.object_list:
        array[i] = {
            'id': o.id,
            'name': o.label,
            'phone': u'%s' % o.get_first_phone(),
        }
        i = i + 1

    return HttpResponse(simplejson.dumps(array), mimetype='application/json')

@permission_required_with_403('place.place_list')
def room_list( request, ids, descriptions, dimensions, room_types, furniture_descriptions ):
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

@permission_required_with_403('place.place_read')
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
        organization= Organization.objects.get(pk= user.get_profile().org_active.id)
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
                                                        'last_update': last_update,
                                                        'States': State.objects.all(),
                                                        },
                                                        context_instance=RequestContext(request))

@permission_required_with_403('place.place_write')
def save(request, object_id=''):
    user = request.user
    try:
        object = get_object_or_404(Place, pk=object_id)
    except Http404:
        object = Place()

    try:
        object.visible= get_visible( request, request.POST['visible'] )
    except:
        object.visible = False
    object.label = request.POST['label']
    object.place_type= PlaceType.objects.get( pk= request.POST[ 'place_type' ] )
    object.organization = user.get_profile().org_active    
    object.save() 

    save_rooms( request, object, request.POST.getlist( 'room_id' ), request.POST.getlist('description'), request.POST.getlist('dimension'), request.POST.getlist('room_type'), request.POST.getlist('furniture') )
    phone_save(object, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))
    address_save(object, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
                 request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))

    return HttpResponse(object.id)

@permission_required_with_403('place.place_write')
def save_rooms(request, place, ids, descriptions, dimensions, room_types, furnitures):
 #  place.room_set.all().delete() # If uncomment this line, all event of scheduled will be deleted when add a new room or modifi one of it.
    for room in room_list( request, ids, descriptions, dimensions, room_types, furnitures ):
        room.place = place
        room.save()

#def save_rooms( request, place, ids, descriptions, dimensions, room_types, furnitures ):
#    for room in room_list( ids, descriptions, dimensions, room_types, furnitures ):
#        result = is_equal( request, room )
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

@permission_required_with_403('place.place_read')
def is_equal(request, a_room):
    try:
        room_loaded_from_db = Room.objects.get( pk= a_room.id )
    except:
        return -1
    
    if cmp(room_loaded_from_db, a_room) == 0:
        return 0
    else:
        return 1

@permission_required_with_403('place.place_read')
def get_visible( request, value ):
    if ( value == 'on' ):
        return True
    else:
        return False 
