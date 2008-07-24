from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from gestorpsi.person.models import Person, PersonForm
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address, AddressType

def phoneList(areas, numbers, exts, types):
    total = len(numbers)
    phones = []
    for i in range(0, total):
        if (len(numbers[i])): 
            phones.append(Phone(area=areas[i],phoneNumber=numbers[i],ext=exts[i],phoneType=types[i]))
    return phones

def index(request): 
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })

def form(request, person_id=0):
    try:
        phones = []
        person = get_object_or_404(Person, pk=person_id)
        for phone in client.phones.all():
            phones.append(phone)
    except:
        person = PersonForm()
    return render_to_response('person/person_html.html', {'person': person, 'phones': phones} )

def save(request, person_id=0):
    try:
        person = get_object_or_404(Person, pk=person_id)
    except Http404:
        person = Person()
    person.name = request.POST['name']
    person.nickname = request.POST['nickname']
    #person.photo = request.POST['photo']
    person.email = request.POST['email']
    person.birthDate = request.POST['birthDate']
    person.gender = request.POST['gender']
    person.maritalStatus = MaritalStatus.objects.get(pk = request.POST['maritalStatus'])
    person.birthPlace = City.objects.get(pk = request.POST['birthPlace'])    
    person.active = request.POST['active']
    person.address.addressPrefix = request.POST['addressPrefix']
    person.address.addressLine1 = request.POST['addressLine1']
    person.address.addressLine2 = request.POST['addressLine2']
    person.address.addressNumber = request.POST['addressNumber']
    person.address.neighborhood = request.POST['neighborhood']
    person.address.zipCode = request.POST['zipCode']
    person.address.addressType = AddressType.objects.get(pk=request.POST['addressType'])
    
    if (request.POST['city']==""):
        person.address.foreignCountry = Country.objects.get(pk= request.POST['country']) 
        person.address.foreignState = request.POST['state']
        person.address.foreignCity = request.POST['city']
    else:
        person.address.foreignCountry = Country.objects.get(pk= request.POST['country'])        
        person.address.city = City.objects.get(pk= request.POST['city'])
        
    person.save()
    
    person.phones.all().delete()
    for phone in phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType')):
        phone.content_object = person
        phone.save()
    return render_to_response('person/person_index.html', {'personList': person.objects.all().filter(active = True) })

def delete(request, person_id):
    person = get_object_or_404(person, pk=person_id)
    person.active = False
    person.save()
    return render_to_response('person/person_index.html', {'personList': person.objects.all().filter(active = True) })
