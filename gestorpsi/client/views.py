from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from gestorpsi.client.models import Client
from gestorpsi.person.models import Person, PersonForm
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.phone.views import phoneList
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.address.views import addressList
from gestorpsi.document.views import documentList

# list all active clients
def index(request):
    return render_to_response('client/client_index.html', {'object': Client.objects.all().filter(clientStatus = '1'), 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), })

# add or edit form
def form(request, object_id=0):
    
    phones = []
    addresses = []
    documents = []
        
    try:
        # if exists, get it to edit
        object = get_object_or_404(Client, pk=object_id)        
        print object
        
        # person have phones
        phones= object.person.phones.all()
        print phones
        
        # person have addresses
        addresses= object.person.address.all()
        print addresses
        
        # person have documents
        documents = object.person.document.all()
        print documents
        
            
    except:
        object = Client()
        
    return render_to_response('client/client_form.html', {'object': object, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'documents': documents, 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), } )
 


## NEED OPEN TRANSACTION FOR THIS VIEW
# Save or Update client object
def save(request, object_id=0):    
    try:
        object = get_object_or_404(Client, pk=object_id)
        person = object.person
    except Http404:
        object = Client()
        person = Person()
    
    person.name = request.POST['name']
    person.nickname = request.POST['nickname']
    
    if(request.POST['photo']):
        person.photo = request.POST['photo']
    else:
        person.photo = ''

    if(request.POST['birthDate']):
        person.birthDate = request.POST['birthDate']
    person.gender = request.POST['gender']
    #person.maritalStatus = MaritalStatus.objects.get(pk = request.POST['maritalStatus'])

    # birthPlace (Naturality)
    if not (request.POST['birthPlace']):
        person.birthPlace = None
    else:
        person.birthPlace = City.objects.get(pk = request.POST['birthPlace'])    
    
    person.save()
    object.person = person
    object.save()
    
    #
    #email = Email()
    #email.email=request.POST['email']
    #if(len(request.POST['email_type'])):
    #    email.email_type=EmailType.objects.get(pk=1)
    #else:
    #    email.email_type=EmailType.objects.get(pk=request.POST['email_type'])
    #email.content_object = object
    #email.save()   
    
    # flush phones and re-insert it
    object.person.phones.all().delete()
    for phone in phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType')):
        phone.content_object = object.person
        phone.save()
    
    # flush addresses and re-insert it
    object.person.address.all().delete()
    for address in addressList(request.POST.getlist('addressPrefix'), request.POST.getlist('addressLine1'), 
                               request.POST.getlist('addressLine2'), request.POST.getlist('addressNumber'),
                               request.POST.getlist('neighborhood'), request.POST.getlist('zipCode'), 
                               request.POST.getlist('addressType'), request.POST.getlist('city'),
                               request.POST.getlist('foreignCountry'), request.POST.getlist('foreignState'),
                               request.POST.getlist('foreignCity')):
        address.content_object = object.person
        address.save()
    
    # flush documents and re-insert it
    object.person.document.all().delete()
    for document in documentList(request.POST.getlist('document_typeDocument'), request.POST.getlist('document_document'), request.POST.getlist('document_issuer'), request.POST.getlist('document_state')):
        document.content_object = object.person
        document.save()

    return HttpResponse(object.id)

# delete, pero no mucho, an object
def delete(request, object_id):
    client = get_object_or_404(Client, pk=object_id)
    client.clientStatus = '0'
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(clientStatus = '1') })