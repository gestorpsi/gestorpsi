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
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.contrib import messages
from gestorpsi.place.models import Place, Room, RoomType, PlaceType, HOURS
from gestorpsi.address.models import Country, AddressType, State, City
from gestorpsi.address.views import address_save
from gestorpsi.phone.models import PhoneType
from gestorpsi.phone.views import phone_save
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.careprofessional.models import CareProfessional


@permission_required_with_403('place.place_list')
def room_index(request, deactive=False):
    return render_to_response("place/place_room_list.html",
                              locals(),
                              context_instance=RequestContext(request))


@permission_required_with_403('place.place_list')
def index(request, deactive=False):
    return render_to_response("place/place_list.html",
                              locals(),
                              context_instance=RequestContext(request))


@permission_required_with_403('place.place_list')
def list(request, page=1, initial=None, filter=None, no_paging=False,
         deactive=False):

    if deactive:
        object = Place.objects.deactive().filter(
            organization=request.user.get_profile().org_active.id)
    else:
        object = Place.objects.active().filter(
            organization=request.user.get_profile().org_active.id)

    if initial:
        object = object.filter(label__istartswith=initial)

    if filter:
        object = object.filter(label__icontains=filter)

    object_length = len(object)
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)

    array = {}  # json
    i = 0

    array['util'] = {
        'has_perm_read': request.user.has_perm('place.place_read'),
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
            'type': u'%s' % o.place_type,
        }
        i = i + 1

    return HttpResponse(
        simplejson.dumps(array, sort_keys=True),
        mimetype='application/json')


@permission_required_with_403('place.place_write')
def form(request, object_id=None):

    if object_id:
        object = get_object_or_404(
            Place, pk=object_id,
            organization=request.user.get_profile().org_active)
        addresses = object.address.all()
        phones = object.phones.all()
    else:
        if not request.user.has_perm('place.place_write'):
            return render_to_response(
                '403.html',
                {'object': _("Oops! You don't have access for this service!"),
                 },
                context_instance=RequestContext(request))

        object = Place()
        place_type = PlaceType()

    try:
        cities = City.objects.filter(
            state=request.user.
            get_profile().org_active.address.all()[0].city.state)
    except:
        cities = {}

    return render_to_response('place/place_form.html',
                              {'object': object,
                               'PlaceTypes': PlaceType.objects.all(),
                               'addresses': object.address.all(),
                               'phones': object.phones.all(),
                               'PhoneTypes': PhoneType.objects.all(),
                               'AddressTypes': AddressType.objects.all(),
                               'countries': Country.objects.all(),
                               'RoomTypes': RoomType.objects.all(),
                               'States': State.objects.all(),
                               'Cities': cities,
                               'Hours': HOURS, },
                              context_instance=RequestContext(request))


@permission_required_with_403('place.place_write')
def save(request, object_id=None):

    if object_id:
        object = get_object_or_404(
            Place, pk=object_id,
            organization=request.user.get_profile().org_active)
    else:
        object = Place()

    try:
        object.visible = get_visible(request, request.POST['visible'])
    except:
        object.visible = False

    # all others place will be filial if place_type of object is Matriz
    if request.POST.get('place_type') == '1':  # hardcode
        for x in Place.objects.filter(
                organization=request.user.get_profile().org_active,
                place_type__id=1):  # todos que são matriz
            x.place_type = PlaceType.objects.get(pk=4)  # hardcode
            x.save()

    object.label = request.POST['label']
    object.comments = request.POST.get('comments')
    object.place_type = PlaceType.objects.get(pk=request.POST['place_type'])
    object.organization = request.user.get_profile().org_active
    object.hour_start = request.POST['hour_start']
    object.hour_end = request.POST['hour_end']
    object.save()

    phone_save(object, request.POST.getlist('phoneId'),
               request.POST.getlist('area'),
               request.POST.getlist('phoneNumber'),
               request.POST.getlist('ext'),
               request.POST.getlist('phoneType'))

    address_save(object, request.POST.getlist('addressId'),
                 request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'),
                 request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'),
                 request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'),
                 request.POST.getlist('addressType'),
                 request.POST.getlist('city'),
                 request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'),
                 request.POST.getlist('foreignCity'))

    messages.success(request, _('Place saved successfully'))

    return HttpResponseRedirect('/place/%s/' % object.id)


@permission_required_with_403('place.place_write')
def room_save(request, object_id=None):
    if object_id:
        object = get_object_or_404(
            Room,
            pk=object_id,
            place__organization=request.user.get_profile().org_active)
    else:
        object = Room()

    object.place = Place.objects.get(pk=request.POST.get('place_id'))
    object.description = request.POST.get('description')
    object.dimension = request.POST.get('dimension')
    object.room_type = RoomType.objects.get(pk=request.POST.get('room_type'))
    object.furniture = request.POST.get('furniture')
    object.comments = request.POST.get('comments')

    if object.id:
        object.save(force_update=True)
    else:
        object.save()

    messages.success(request, _('Room saved successfully'))

    return HttpResponseRedirect('/place/room/%s/' % object.id)


@permission_required_with_403('place.place_list')
def room_list(request, page=1, initial=None,
              filter=None, no_paging=False, deactive=False):

    if deactive:
        object = Room.objects.deactive().filter(
            place__organization=request.user.get_profile().org_active)
    else:
        object = Room.objects.active().filter(
            place__organization=request.user.get_profile().org_active)

    if initial:
        object = object.filter(description__istartswith=initial)

    if filter:
        object = object.filter(description__icontains=filter)

    object_length = len(object)
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)

    array = {}  # json
    i = 0

    array['util'] = {
        'has_perm_read': request.user.has_perm('place.place_read'),
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
            'name': o.description,
            'place': o.place.label,
            'type': u'%s' % o.room_type,
        }
        i = i + 1

    return HttpResponse(simplejson.dumps(array, sort_keys=True),
                        mimetype='application/json')


@permission_required_with_403('place.place_write')
def room_form(request, object_id=None):
    if object_id:
        object = get_object_or_404(
            Room, pk=object_id,
            place__organization=request.user.get_profile().org_active)
    else:
        if not request.user.has_perm('place.place_write'):
            return render_to_response(
                '403.html',
                {'object': _("Oops! You don't have access for this service!"),
                 },
                context_instance=RequestContext(request))

        object = Room()

    return render_to_response(
        'place/place_room_form.html',
        {'object': object, 'RoomTypes': RoomType.objects.all(),
        'CareProfessionals': CareProfessional.objects.all(),
         'Places': Place.objects.filter(organization=request.
                                        user.get_profile().org_active.id), },
        context_instance=RequestContext(request))


def get_visible(value):
    if value == 'on':
        return True
    else:
        return False


@permission_required_with_403('place.place_write')
def place_order(request, object_id=None):
    object = get_object_or_404(
        Place, pk=object_id,
        organization=request.user.get_profile().org_active)

    if object.active is True:
        if object.occurrences():
            occurence_list_html = ''
            for i in object.occurrences():
                occurence_list_html += u'<li><a href="/schedule/events/%s/confirmation/">%s - %s</a></li>' % (i.pk, i, i.event.referral)
                messages.success(request, (_('You can not disable a place with upcomming occurrences <ul>%s</ul>') % occurence_list_html))
                return HttpResponseRedirect('/place/%s/' % object.id)
        else:
            object.active = False
    else:
        object.active = True

    object.save(force_update=True)
    messages.success(request, ('%s' % (_('Place activated successfully')
                               if object.active
                               else _('Place deactivated successfully'))))
    return HttpResponseRedirect('/place/%s/' % object.id)


@permission_required_with_403('place.place_write')
def room_order(request, object_id=None):
    object = get_object_or_404(
        Room,
        pk=object_id,
        place__organization=request.user.get_profile().org_active)

    if object.active is True:
        if object.occurrences():
            occurence_list_html = ''
            for i in object.occurrences():
                occurence_list_html += u'<li><a href="/schedule/events/%s/confirmation/">%s - %s</a></li>' % (i.pk, i, i.event.referral)
            messages.success(request, (_('You can not disable a room with upcomming occurrences <ul>%s</ul>') % occurence_list_html))
            return HttpResponseRedirect('/place/room/%s/' % object.id)
        else:
            object.active = False
    else:
        object.active = True

    object.save(force_update=True)
    messages.success(request, ('%s' % (_('Room activated successfully')
                     if object.active
                     else _('Room deactivated successfully'))))
    return HttpResponseRedirect('/place/room/%s/' % object.id)
