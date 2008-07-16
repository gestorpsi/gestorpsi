from django.shortcuts import render_to_response, get_object_or_404
from django.newforms import form_for_model
from gestorpsi.place.models import Place, PlaceForm, Room, RoomForm

def index(request):
    list_of_places= Place.objects.all()
    return render_to_response( "place/place_index.html", locals() )

def add(request):
    place_form= PlaceForm()
    return render_to_response( 'place/place_add.html', locals() )

def save(request):
    place= PlaceForm( request.POST )
    if place.is_valid():
        #Django doesn't hit the database until save() to be called
        place.save()
        return render_to_response( 'place/place_msg.html', { 'msg': "It was successfully saved" } )
    else:
        return render_to_response( 'place/place_msg.html', { 'msg': "some problem occurred while saving the place" } )

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
    except Place.DoesNotExist:
        return render_to_response( 'place/place_msg.html', { 'msg': "A place with id equal to %s does not exist, thus it could not be updated" % place_id } )
    else: 
        return render_to_response( 'place/place_update.html', { 'place_form': place_form, 'a_place': a_place } )

def update(request, place_id):
    # Create a form to edit an existing Place, but use
    # POST data to populate the form.
    a_place= load_place( place_id ) 
    place_form= PlaceForm( request.POST, instance= a_place )
    
    if place_form.is_valid():
        place_form.save()
        return render_to_response( 'place/place_msg.html', { 'msg': "It was successfully updated" } )
    else:
        return render_to_response( 'place/place_msg.html', { 'msg': "some problem occurred while updating the place" } )

def add_room(request, place_id):
    a_place= load_place( place_id )
    room= Room( description= '', size= '', place= a_place )
    room_form= RoomForm( instance= room )
    return render_to_response( 'place/add_room.html', locals() )

def save_room(request):
    room= RoomForm( request.POST )
    if room.is_valid():
        room.save()
        return render_to_response( 'place/place_msg.html', { 'msg': "It was successfully saved" } )
    else:
        return render_to_response( 'place/place_msg.html', { 'msg': "some problem occurred while saving the room" } )

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