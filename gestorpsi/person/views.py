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

from django.core.paginator import Paginator
from django.conf import settings
from django.utils.translation import ugettext as _
from gestorpsi.address.models import City
from gestorpsi.address.views import address_save
from gestorpsi.document.views import document_save
from gestorpsi.person.models import MaritalStatus
from gestorpsi.phone.views import phone_save
from gestorpsi.internet.views import email_save, site_save, im_save
from datetime import datetime

def person_save(request, person):

    person.name= request.POST['name']
    person.nickname = request.POST['nickname']
    person.comments = request.POST.get('comments')

    if(request.POST['photo']):
        person.photo = request.POST['photo']
    else:
        person.photo = ''

    """ AGE """
    if(request.POST.get('dateBirth')):
        person.birthDate = datetime.strptime(request.POST.get('dateBirth'),'%d/%m/%Y')
    else:
        if request.POST.get('Years'):
            birthYear = (( int(datetime.now().strftime("%Y")) ) - ( int(request.POST.get('Years')) ) ) 
            today = (datetime.now().strftime("%d/%m/"))
            dt = "%s%s" % (today, birthYear)
            person.birthDate = datetime.strptime(dt ,'%d/%m/%Y')

    if(request.POST.get('aprox')):
        person.birthDateSupposed = True
    else:
        person.birthDateSupposed = False
    """ AGE """

    person.gender = request.POST['gender']
    
    # maritalStatus
    try:
        if not (request.POST['maritalStatus']):
            person.maritalStatus = None
        else:
            person.maritalStatus = MaritalStatus.objects.get(pk = request.POST['maritalStatus'])
    except:
        person.maritalStatus = None

    # birthPlace (Naturality)
    person.birthForeignCity= ''
    person.birthForeignState= ''
    person.birthForeignCountry= None
    
    try:
        person.birthPlace = City.objects.get(pk = request.POST['birthPlace'])
    except:
        person.birthPlace = None
        try:
            person.birthForeignCity= request.POST['birthForeignCity']
        except:
            person.birthForeignCity = None
        try:
            person.birthForeignState= request.POST['birthForeignState']
        except:
            person.birthForeignState = None
        try:
            person.birthForeignCountry= request.POST['birthForeignCountry']
        except:
            person.birthForeignCountry= None


    person.save()    
    user = request.user
    person.organization.add(user.get_profile().org_active)

    # save phone numbers (using Phone APP)
    phone_save(person, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))

    # save addresses (using Address APP)
    address_save(person, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
                 request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))
    
    # save documents (using Document APP) 
    document_save(person, request.POST.getlist('documentId'), request.POST.getlist('document_typeDocument'), request.POST.getlist('document_document'), request.POST.getlist('document_issuer'), request.POST.getlist('document_state'))
    
    # save internet data
    email_save(person, request.POST.getlist('email_id'), request.POST.getlist('email_email'), request.POST.getlist('email_type'))
    site_save(person, request.POST.getlist('site_id'), request.POST.getlist('site_description'), request.POST.getlist('site_site'))
    im_save(person, request.POST.getlist('im_id'), request.POST.getlist('im_identity'), request.POST.getlist('im_network'))

    return person

def person_type_url(person):
    """ Return an URL linking to a Client, Care Professional or an Employee form """
    try:
        x = person.client
        return "/client/%s/" % x.id
    except:
        pass
        
    try:
        x = person.careprofessional
        return "/careprofessional/%s/" % x.id
    except:
        pass
        
    try:
        x = person.employee
        return "/employee/%s/" % x.id
    except:
        pass

def person_json_list(request, object, perm, page, no_paging = False, with_client_services = False):
    object_length = len(object)
    
    array = {} #json
    i = 0

    if not no_paging:
        paginator = Paginator(object, settings.PAGE_RESULTS)
        object = paginator.page(page)
        object_list = object.object_list
        paginator_has_previous = object.has_previous().real
        paginator_has_next = object.has_next().real
        paginator_previous_page_number = object.previous_page_number().real
        paginator_next_page_number = object.next_page_number().real
        paginator_actual_page = object.number
        paginator_num_pages = paginator.num_pages
        
        array['paginator'] = {}
        for p in paginator.page_range:
            array['paginator'][p] = p
    else:
        object_list = object
        paginator_has_previous = None
        paginator_has_next = None
        paginator_previous_page_number = None
        paginator_next_page_number = None
        paginator_actual_page = None
        paginator_num_pages = None

    array['util'] = {
        'has_perm_read': request.user.has_perm(perm),
        'paginator_has_previous': paginator_has_previous,
        'paginator_has_next': paginator_has_next,
        'paginator_previous_page_number': paginator_previous_page_number,
        'paginator_next_page_number': paginator_next_page_number,
        'paginator_actual_page': paginator_actual_page,
        'paginator_num_pages': paginator_num_pages,
        'object_length': object_length,
    }
    
    for c in object_list:
        try:
            username = c.user.username
        except:
            username = ''
        
        array[i] = {
            'id': c.id,
            'person_id': c.person.id,
            'name': c.person.name.title(),
            'phone': u'%s' % c.person.get_first_phone(),
            'email': u'%s' % c.person.get_first_email(),
            'username': username,
            'age': c.person.age,
        }
        
        if with_client_services:
            html = ''
            for r in c.referrals_charged():
                html += u"<a title='%s' href='/client/%s/referral/%s/' style='color:#%s;'><div class='service_name_html' style='background-color:#%s;'>&nbsp;</div></a>" % (r, c.pk, r.pk, r.service.font_color, r.service.color)
            
            array[i]['services_html'] = html
        
        i = i + 1

    return array
