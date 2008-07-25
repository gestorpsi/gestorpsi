from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from gestorpsi.client.models import Client
from gestorpsi.person.models import Person, PersonForm
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, Address, AddressType

def phoneList(areas, numbers, exts, types):
    total = len(numbers)
    phones = []
    for i in range(0, total):
        if (len(numbers[i])): 
            phones.append(Phone(area=areas[i], phoneNumber=numbers[i], ext=exts[i], phoneType=PhoneType.objects.get(pk=types[i])))
    return phones


def addressList(addressPrefix, addressLine1, addressLine2, addressNumber, neighborhood, zipCode, addressType, city_id, country_id, stateChar, cityChar):
    total = len(addressLine1)
    address = []
    for i in range(0, total):
        if (len(addressLine1[i])):
            address.append(Address(addressPrefix=addressPrefix[i], addressLine1=addressLine1[i], addressLine2=addressLine2[1], 
                                   addressNumber=addressNumber[i], neighborhood=neighborhood[i], zipCode=zipCode[i],                                    
                                   stateChar=stateChar[i], cityChar=cityChar[i]))
            if(len(addressType[i])):
               addressType=AddressType.objects.get(pk=addressType[i])
            if(len(city_id[i])):
                city_id=City.objects.get(pk=city_id[i])
            if(len(country_id[i])):
                country_id=Country.objects.get(pk=country_id[i])
            
    return address



def index(request): 
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })

def form(request, client_id=0):
    try:
        phones = []
        addresses = []
        client = get_object_or_404(Client, pk=client_id)
        person= Person.objects.filter( id__exact= client.id ).get( id= client.id )
        for phone in person.phones.all():
            phones.append(phone)
        for address in person.address.all():
            addresses.append(address)    
    except:
        client = Client()
        person= Person()
    return render_to_response('client/client_form.html', {'client': client, 'phones': phones, 'person': person } )


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
    person.save() 
      
#    address = Address()
#    address.addressPrefix = request.POST['addressPrefix']
#    address.addressLine1 = request.POST['addressLine1']
#    address.addressLine2 = request.POST['addressLine2']
#    address.addressNumber = request.POST['addressNumber']
#    address.neighborhood = request.POST['neighborhood']
#    address.zipCode = request.POST['zipCode']
#    address.addressType = AddressType.objects.get(pk=request.POST['addressType'])
#    if (request.POST['city']==""):
#        person.address.foreignCountry = Country.objects.get(pk= request.POST['country']) 
#        person.address.foreignState = request.POST['state']
#        person.address.foreignCity = request.POST['city']
#    else:
#        person.address.foreignCountry = Country.objects.get(pk= request.POST['country'])        
#        person.address.city = City.objects.get(pk= request.POST['city'])
   
   
    person.address.all().delete()
    for address in addressList(request.POST.getlist('addressPrefix'), request.POST.getlist('addressLine1'), 
                               request.POST.getlist('addressLine2'), request.POST.getlist('addressNumber'),
                               request.POST.getlist('neighborhood'), request.POST.getlist('zipCode'), 
                               request.POST.getlist('addressType'), request.POST.getlist('city'),
                               request.POST.getlist('foreignCountry'), request.POST.getlist('foreignState'),
                               request.POST.getlist('foreignCity')):
        address.content_object = person
        address.save()
    
    person.phones.all().delete()
    for phone in phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType')):
        phone.content_object = person
        phone.save()
    
    return render_to_response('client/client_index.html', {'clientList': person.objects.all().filter(active = True) })


def delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.active = False
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })