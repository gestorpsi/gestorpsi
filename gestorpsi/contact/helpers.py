
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from django.contrib import messages

from gestorpsi.organization.models import Organization
from gestorpsi.contact.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType, City
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import CareProfessional, Profession, ProfessionalIdentification
from gestorpsi.address.views import address_save
from gestorpsi.contact.forms import PhoneForm
from gestorpsi.internet.views import email_save, site_save, im_save
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None
from gestorpsi.contact.models import Contact
from gestorpsi.contact.models import Phone, PhoneType

# Check if phone fields are equals
def is_equal(phone):
    try:
        phone_db = Phone.objects.get(pk=phone.id)
    except:
        return False
    if cmp(phone_db, phone) == 0:
        return True
    else:
        return False

# Create a phone's list, but don't append blank phone numbers 
def phone_list(ids, areas, numbers, exts, types): 
    objs = []
    for i in range(0, len(numbers)):
        if (len(numbers[i])):
            objs.append(Phone(id=ids[i], area=areas[i], phoneNumber=numbers[i], ext=exts[i], phoneType=PhoneType.objects.get(pk=types[i])))
    return objs

# 'number' field blank means that it was deleted by an user
# So, if len(number) == 0 AND len(id) != 0, delete phone using id
def phone_delete(ids, numbers): 
    for i in range(0, len(numbers)):
        if (not len(numbers[i]) and len(ids[i])):
            Phone.objects.get(pk=ids[i]).delete()

#def phone_save(object, ids, areas, numbers, exts, types):
#    phone_delete(ids, numbers)
#    for phone in phone_list(ids, areas, numbers, exts, types):
#        if not is_equal(phone):
#            phone.content_object = object
#            phone.save()

def phone_save(object, ids, areas, numbers, exts, types):
    object.phones.all().delete()
    for phone in phone_list(ids, areas, numbers, exts, types):
        phone.content_object = object
        phone.save()



def have_organization_perms_save(request, object):
    if  object.organization != request.user.get_profile().org_active \
        or ( not object.revision_created().user == request.user \
        and 'administrator' not in [ g.name for g in request.user.groups.all()] \
        and 'secretary' not in [ g.name for g in request.user.groups.all()]):
        return False
    else:
        return True

def have_careprofessional_perms_save(request, object):
    if  request.user.get_profile().org_active not in [ i.organization for i in object.person.organization.all()] \
        or ( not object.revision_created().user == request.user \
        and 'administrator' not in [ g.name for g in request.user.groups.all()] \
        and 'secretary' not in [ g.name for g in request.user.groups.all()]):
        return False
    else:
        return True

def extra_data_save(request, object = None):
    phone_save(object, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))
    email_save(object, request.POST.getlist('email_id'), request.POST.getlist('email_email'), request.POST.getlist('email_type'))
    site_save(object, request.POST.getlist('site_id'), request.POST.getlist('site_description'), request.POST.getlist('site_site'))
    im_save(object, request.POST.getlist('im_id'), request.POST.getlist('im_identity'), request.POST.getlist('im_network'))
    address_save(object, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
        request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
        request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
        request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
        request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
        request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))
    return object