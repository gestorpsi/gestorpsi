from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.organization.models import Organization
from django.newforms import form_for_model

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
    organization = Organization.objects.all()
    #object = organization    
    return render_to_response('contact/contact_index.html', {'organization': organization})


def form(request, object_id):       
    object = get_object_or_404(Organization, pk=organization_id)    
    organizationForm = forms.form_for_instance(organization)
    eForm = organizationForm()
        
    orgAddressbook = Organization()
    orgAddressbook = Organization.objects.filter(organization=object.id)

    return render_to_response(
        'contact/contact_details.html', {'eForm': eForm, 'message': message})



def save(request, object_id= 0, org_id=0):
    try:
        object= get_object_or_404(Organization, pk=object_id)
    except Http404:
        object= Place()
    object.name= request.POST['name']
    object.businessName= request.POST['businessName']
    object.visible= get_visible( request.POST['visible'] )
    
    if(len(object.organization_id)):
        object.organization = org_id
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
