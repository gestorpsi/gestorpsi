from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from gestorpsi.employee.models import Employee
from gestorpsi.person.models import Person, PersonForm
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.address.views import addressList
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.phone.views import phoneList
from gestorpsi.document.views import documentList


def index(request): 
    #return render_to_response('employee/employee_index.html', {'object': Employee.objects.all().filter(active = True) })
    return render_to_response('employee/employee_index.html', {'object': Employee.objects.all() })

def form(request, object_id=0):
    phones = []
    addresses = []
    documents = []
    
    try:
   
        object = get_object_or_404(Employee, pk=object_id)        
      
        # person have phones
        phones= object.person.phones.all()
        
        # person have addresses
        addresses= object.person.address.all()
        
        # person have documents
        documents =  object.person.document.all()
        
    except:        
        object= Employee()
        
    return render_to_response('employee/employee_form.html', {'object': object, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'documents': documents, 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), } )


def save(request, object_id=0):    
    try:
        object = get_object_or_404(Employee, pk=object_id)
    except Http404:
        object = Employee()   
    
    person = Person()
    person.name = request.POST['name']
    person.nickname = request.POST['nickname']
    
    if(request.POST['birthDate']):
        person.birthDate = request.POST['birthDate']
    
    person.gender = request.POST['gender']
    
    #if(request.POST['maritalStatus']):
    #    person.maritalStatus = MaritalStatus.objects.get(pk = request.POST['maritalStatus'])
    
    if(request.POST['birthPlace']):
       person.birthPlace = City.objects.get(pk = request.POST['birthPlace'])
       
    if(request.POST['photo']):
       person.photo = request.POST['photo']
    
    person.save()
    
    '''
    email = Email()
    email.email=request.POST['email']
    if(len(request.POST['email_type'])):        
        email.email_type=EmailType.objects.get(pk=1)
    else:
        email.email_type=EmailType.objects.get(pk=request.POST['email_type'])
    email.content_object = person
    email.save()
    '''
    
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
        
    person.document.all().delete()
    for document in documentList(request.POST.getlist('document_typeDocument'), request.POST.getlist('document_document'), request.POST.getlist('document_issuer'), request.POST.getlist('document_state')):
        document.content_object = person
        document.save()
        
    object.job = request.POST['job']
    if(request.POST['hiredate']):
        object.hiredate = request.POST['hiredate']
    object.person = person
    object.save()
    
    return HttpResponse(object.id)


def delete(request, object_id):
    object = get_object_or_404(Employee, pk=object_id)
    object.active = False
    object.save()
    return render_to_response('employee/employee_index.html', {'employeeList': Employee.objects.all().filter(active = True) })
