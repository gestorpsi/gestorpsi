from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.employee.models import Employee
from gestorpsi.person.models import Person
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.person.views import personSave

def index(request): 
    return render_to_response('employee/employee_index.html', {'object': Employee.objects.all().filter(active = True), 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), })

def form(request, object_id=0):
    phones    = []
    addresses = []
    documents = []
    try:
        object    = get_object_or_404(Employee, pk=object_id)        
        phones    = object.person.phones.all()
        addresses = object.person.address.all()
        documents = object.person.document.all()
    except:        
        object= Employee()
        
    return render_to_response('employee/employee_form.html', {'object': object, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'documents': documents, 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), } )

def save(request, object_id=0):    
    try:
        object = get_object_or_404(Employee, pk=object_id)
        person = object.person
    except Http404:
        object = Employee()
        person = Person()
    
    object.person = personSave(request, person)
    object.job = request.POST['job']
    if(request.POST['hiredate']):
        object.hiredate = request.POST['hiredate']
    object.save()

    return HttpResponse(object.id)

def delete(request, object_id):
    object = get_object_or_404(Employee, pk=object_id)
    object.active = False
    object.save()
    return render_to_response('employee/employee_index.html', {'employeeList': Employee.objects.all().filter(active = True) })