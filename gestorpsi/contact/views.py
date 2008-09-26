from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from gestorpsi.organization.models import Organization
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address
from gestorpsi.person.models import Person
from gestorpsi.place.models import Place


def index(request):
    
    total= []
    
    #list_of_orgs= []
    #for orgs in Organization.objects.all():
     #   orgs= {}
      #  orgs['organization']= orgs
       # list_of_orgs.append( orgs )
        #total.append( orgs )
    
    list_of_places= []
    for places in Place.objects.all():
        places= {}
        places['places']= places
        list_of_places.append( places )
        total.append( places )
    
    list_of_pers= []    
    for persons in Person.objects.all():
        persons= {}
        persons['person']= persons
        list_of_pers.append( persons )
        total.append( persons )
        
         
    return render_to_response('contact/contact_index.html', { 'object': total, 'places': Place.objects.all(), 'persons': Person.objects.all() })
    #return render_to_response('contact/contact_index.html', { 'object': total, 'orgs': Organization.objects.all(), 'persons': Person.objects.all() })

# function needed because was declared in urls.py
def form(request):
    pass

"""
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.organization.models import Organization
from gestorpsi.address.views import addressList
from gestorpsi.phone.views import phoneList


def careProfessionalList(names):
    total = len(name)
    careProfessionals = []
    for i in range(0, total):
        if (len(numbers[i])): 
            careProfessionals.append(Person(name=names[i], organization = organization()))
    return careProfessionals


def index(request):
    object = Organization.objects.all()        
    return render_to_response('contact/contact_index.html', {'organization': object})


def form(request, object_id):    
    try:
        phones = []
        addresses = []
        careProfessionals = []
        object = get_object_or_404(Organization, pk=object_id)        
        persons = object.person_set.all() 
        for phone in person.phones.all():
            phones.append(phone)
        for address in person.address.all():
            addresses.append(address)
        for careProfessional in persons:
            careProfessionals.append(careProfessional)    
    except:        
        object= Organization()

        return render_to_response('contact/contact_details.html', {'contactList': object, 
                                                                   'phones': phones, 
                                                                   'addresses': addresses, 
                                                                   'careProfessionals':careProfessionals})


def save(request, object_id= 0):
    try:
        object= get_object_or_404(Organization, pk=object_id)
    except Http404:
        object= Organization()
    object.name= request.POST['name']
    object.businessName= request.POST['businessName']
    object.visible= get_visible( request.POST['visible'] )
    
    #Used if exist an organization in the session
    #if(len(object.organization_id)):
    #    object.organization = org_idSection
    #organization
    #object.organization= Organization.objects.get(pk= request.POST[ 'organization' ] )
    object.save() 
    
    object.address.all().delete()
    for address in addressList(request.POST.getlist('addressPrefix'), request.POST.getlist('addressLine1'), 
                               request.POST.getlist('addressLine2'), request.POST.getlist('addressNumber'),
                               request.POST.getlist('neighborhood'), request.POST.getlist('zipCode'), 
                               request.POST.getlist('addressType'), request.POST.getlist('city'),
                               request.POST.getlist('foreignCountry'), request.POST.getlist('foreignState'),
                               request.POST.getlist('foreignCity') ):
        address.content_object= object
        address.save()
    
    object.phones.all().delete()    
    for phone in phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType')):
        phone.content_object= object
        phone.save()       
        
    persons = object.person_set.all()
    for person in persons:
        person.delete()
    
        
    #    for phone in phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType')):
    #        phone.content_object= object
    #        phone.save()
                  
    for person in careProfessionalList(request.POST.getlist('name')):
        person.organization = object
        person.save()
        care = CareProfessional()
        care.person = careProfessional
        care.save()
    
    return render_to_response( "contact/contact_index.html", { 'contactList': [ object ] } )


def list_careProfessionals_related_to(request, organization_id):
    careProfessional_list= []
    for careProfessional in CareProfessional.objects.filter( organization__id__exact= int(organization_id) ):
        careProfessional_list.append( CareProfessionalForm( instance= careProfessional ) )
    return render_to_response( 'contact/list_careProfessional.html', { 'careProfessional_list': careProfessional_list } ) 



def delete_organization(request, organization_id):       
    try:
        organization = Organization.objects.get(id=organization_id)
        organization.delete()                
        return render_to_response('contact/contact_msg.html', {'message': "It was successfully deleted"})
    except:
        return render_to_response('contact/contact_msg.html', {'message': "some problem occurred while deleting the organization"})

    
def delete_CareProfessional(request, careProfessional_id):       
    try:
        careProfessional = CareProfessional.objects.get(id=organization_id)
        careProfessional.delete()                
        return render_to_response('contact/contact_msg.html', {'message': "It was successfully deleted"})
    except:
        return render_to_response('contact/contact_msg.html', {'message': "some problem occurred while deleting the CareProfessional"})


def save_CareProfessional(request):
    careProfessional= CareProfessionalForm( request.POST )
    try:        
        careProfessional.save()
        return render_to_response( 'contact/contact_msg.html', { 'message': "It was successfully saved" } )
    except:
        return render_to_response( 'contact/contact_msg.html', { 'message': "some problem occurred while saving the CareProfessional" } )


def delete_CareProfessional(request, organization_id):
    try:
        careProfessional= CareProfessional.objects.get( pk=int(organization_id))           
        careProfessional.save()
        return render_to_response( 'contact/contact_msg.html', { 'message': "It was successfully saved" } )
    except:
        return render_to_response( 'contact/contact_msg.html', { 'message': "some problem occurred while saving the place" } )




def add_careProfessional(request, organization_id):              
        org = get_object_or_404(Organization, pk= organization_id )        
        careProfessional= CareProfessional( name= '', gender= '', organization= org )
        care_form= CareProfessionalForm( instance= careProfessional )
        return render_to_response( 'contact/add_careProfessional.html', {'care_form': care_form, 'message': message} )

"""