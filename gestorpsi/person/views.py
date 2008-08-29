from gestorpsi.address.models import City
from gestorpsi.address.views import address_save
from gestorpsi.document.views import document_save
from gestorpsi.phone.views import phone_save
from gestorpsi.internet.views import email_save, site_save, im_save

def person_save(request, person):
    # CHECK IF HAS CHANGES BEFORE SAVE
    person.name= request.POST['name']
    person.nickname = request.POST['nickname']
    
    
    print "photo"
    if(request.POST['photo']):
        person.photo = request.POST['photo']
    else:
        person.photo = ''

    print "birthdate"
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

    # save phone numbers (using Phone APP)
    phone_save(person, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))

    # save addresses (using Address APP)
    address_save(person, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
                 request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))
    
    # save documents (using Document APP) 
    document_save(person, request.POST.getlist('documentId'), request.POST.getlist('document_typeDocument'), request.POST.getlist('document_document'), request.POST.getlist('document_issuer'), request.POST.getlist('document_state'))
    
    # save internet data
    email_save(person, request.POST.getlist('email_id'), request.POST.getlist('email_email'), request.POST.getlist('email_type'))
    site_save(person, request.POST.getlist('site_id'), request.POST.getlist('site_description'), request.POST.getlist('site_site'))
    im_save(person, request.POST.getlist('im_id'), request.POST.getlist('im_identity'), request.POST.getlist('im_network'))

    return person