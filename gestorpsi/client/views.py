from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from gestorpsi.client.models import Client
from gestorpsi.person.models import Person, PersonForm
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, Address, AddressType
from gestorpsi.internet.models import Email, EmailType

def phoneList(areas, numbers, exts, types):
    total = len(numbers)
    phones = []
    for i in range(0, total):
        if (len(numbers[i])): 
            phones.append(Phone(area=areas[i], phoneNumber=numbers[i], ext=exts[i], phoneType=PhoneType.objects.get(pk=types[i])))
    return phones


def addressList(addressPrefixs, addressLines1, addressLines2, addressNumbers, neighborhoods, zipCodes, addressTypes, city_ids, country_ids, stateChars, cityChars):
    total = len(addressLines1)
    address = []
    
    for i in range(0, total):
        if (len(addressLines1[i])):
            
            #Permitir que Cidade ou Pais seja em branco
            #Do jeito que esta ocorrera uma exception  
            if(len(city_ids[i])):
                #city_id=City.objects.get(pk=city_ids[i])          
                address.append(Address(addressPrefix=addressPrefixs[i], addressLine1=addressLines1[i], addressLine2=addressLines2[i], 
                                   addressNumber=addressNumbers[i], neighborhood=neighborhoods[i], zipCode=zipCodes[i],
                                   addressType=AddressType.objects.get(pk=addressTypes[i]),                                   
                                   foreignCountry=Country.objects.get(pk=country_ids[i]),
                                   foreignState=stateChars[i],
                                   foreignCity=cityChars[i]))
            else:
                address.append(Address(addressPrefix=addressPrefixs[i], addressLine1=addressLines1[i], addressLine2=addressLines2[i], 
                                   addressNumber=addressNumbers[i], neighborhood=neighborhoods[i], zipCode=zipCodes[i],
                                   addressType=AddressType.objects.get(pk=addressTypes[i]),
                                   city = City.objects.get(pk=city_ids[i])))                            
            
    return address



def index(request): 
    return render_to_response('client/client_index.html', {'clientList': Person.objects.all() })

def form(request, object_id=0):
    try:
    	phones = []
        addresses = []
        object = get_object_or_404(Person, pk=object_id)
        #client = get_object_or_404(Client, pk=object_id)
        #person= Person.objects.filter( id__exact= client.id ).get( id= client.id )
        for phone in object.phones.all():
            phones.append(phone)
        for address in object.address.all():
            addresses.append(address)    
    except:
        #client = Client()
        object= Person()
    return render_to_response('client/client_form.html', {'object': object, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all() } )


def save(request, object_id=0):
    test=" "
    try:
        object = get_object_or_404(Person, pk=object_id)
    except Http404:
        object = Person()
    object.name = request.POST['name']
    person.nickname = request.POST['nickname']
    #person.photo = request.POST['photo']   
    if(request.POST['birthDate']):
        object.birthDate = request.POST['birthDate']
    object.gender = request.POST['gender']
    #person.maritalStatus = MaritalStatus.objects.get(pk = request.POST['maritalStatus'])
    if(request.POST['birthPlace']):
       object.birthPlace = City.objects.get(pk = request.POST['birthPlace'])
    
    object.save() 
    
    email = Email()
    email.email=request.POST['email']
    if(request.POST['email_type']==""):
        email.email_type=EmailType.objects.get(pk=1)
    else:
        email.email_type=EmailType.objects.get(pk=request.POST['email_type'])
    email.content_object = object
    email.save()   
    
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
        phone.content_object = object
        phone.save()
    
    return render_to_response('client/client_index.html')


def delete(request, object_id):
    client = get_object_or_404(Client, pk=object_id)
    client.active = False
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })
