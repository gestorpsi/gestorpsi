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

# append documents
def documentList(typeDocuments, documents, issuers, states):
    objs = []
    for i in range(0, len(documents)):
        if (len(documents[i])):
            
            if len(typeDocuments[i]): td = TypeDocument.objects.get(pk=typeDocuments[i])
            else: td = None

            if len(issuers[i]): iss = Issuer.objects.get(pk=issuers[i])
            else: iss = None

            if len(states[i]): st = State.objects.get(pk=states[i])
            else: st = None

            objs.append(Document(typeDocument=td, document=documents[i], issuer=iss, state=st))

    return objs

# list objects
def index(request):
    return render_to_response('client/client_index.html', {'object': Person.objects.all(), 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), })

# add and edit form
def form(request, object_id=0):
    try:
        phones = []
        addresses = []
        documents = []
        
        # if exists, get it to edit
        object = get_object_or_404(Person, pk=object_id)        

        # person have phones
        phones= object.phones.all()
        
        # person have addresses
        addresses= object.address.all()
        
        # person have documents
        documents =  object.document.all()
            
    except:
        object= Person()
        
    return render_to_response('client/client_form.html', {'object': object, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'documents': documents, 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), } )

# save object
## NEED OPEN TRANSACTION FOR THIS VIEW
def save(request, object_id=0):    
    try:
        object = get_object_or_404(Person, pk=object_id)
    except Http404:
        object = Person()
        
    object.name = request.POST['name']
    object.nickname = request.POST['nickname']
    #person.photo = request.POST['photo']   
    if(request.POST['birthDate']):
        object.birthDate = request.POST['birthDate']
    object.gender = request.POST['gender']
    #person.maritalStatus = MaritalStatus.objects.get(pk = request.POST['maritalStatus'])

    # birthPlace (Naturality)
    if not (request.POST['birthPlace']):
        object.birthPlace = None
    else:
        object.birthPlace = City.objects.get(pk = request.POST['birthPlace'])    
    
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
    object.phones.all().delete()
    for phone in phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType')):
        phone.content_object = object
        phone.save()
    
    # flush addresses and re-insert it
    object.address.all().delete()
    for address in addressList(request.POST.getlist('addressPrefix'), request.POST.getlist('addressLine1'), 
                               request.POST.getlist('addressLine2'), request.POST.getlist('addressNumber'),
                               request.POST.getlist('neighborhood'), request.POST.getlist('zipCode'), 
                               request.POST.getlist('addressType'), request.POST.getlist('city'),
                               request.POST.getlist('foreignCountry'), request.POST.getlist('foreignState'),
                               request.POST.getlist('foreignCity')):
        address.content_object = object
        address.save()
    
    # flush documents and re-insert it
    object.document.all().delete()
    for document in documentList(request.POST.getlist('document_typeDocument'), request.POST.getlist('document_document'), request.POST.getlist('document_issuer'), request.POST.getlist('document_state')):
        document.content_object = object
        document.save()

    return HttpResponse(object.id)

# delete object
def delete(request, object_id):
    client = get_object_or_404(Client, pk=object_id)
    client.active = False
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })
