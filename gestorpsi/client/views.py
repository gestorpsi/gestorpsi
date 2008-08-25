from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.client.models import Client
from gestorpsi.person.models import Person
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.person.views import personSave

# list all active clients
def index(request):
    return render_to_response('client/client_index.html', {'object': Client.objects.all().filter(clientStatus = '1'), 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), })

# add or edit form
def form(request, object_id=0):
    phones    = []
    addresses = []
    documents = []
    emails    = []
    sites     = []
    instantMessengers = []
    try:
        object    = get_object_or_404(Client, pk=object_id)        
        phones    = object.person.phones.all()
        addresses = object.person.address.all()
        documents = object.person.document.all()
        emails    = object.person.emails.all()
        sites     = object.person.sites.all()
        instantMessengers = object.person.instantMessengers.all()
    except:
        object = Client()
    
    return render_to_response('client/client_form.html', {'object': object, 'emails': emails, 'websites': sites, 'ims': instantMessengers, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'documents': documents, 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), } )

# Save or Update client object
def save(request, object_id=0):    
    try:
        object = get_object_or_404(Client, pk=object_id)
        person = object.person
    except Http404:
        object = Client()
        person = Person()

    object.person = personSave(request, person)
    object.save()

    return HttpResponse(object.id)

# delete (disable) a client
def delete(request, object_id):
    client = get_object_or_404(Client, pk=object_id)
    client.clientStatus = '0'
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(clientStatus = '1') })