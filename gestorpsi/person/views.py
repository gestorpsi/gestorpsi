from gestorpsi.address.views import addressSave
from gestorpsi.document.views import documentSave
from gestorpsi.phone.views import phoneSave

def personSave(request, person):

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

    # save phone numbers (using Phone APP)
    phoneSave(person, request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))

    # save addresses (using Address APP)
    addressSave(person, request.POST.getlist('addressPrefix'), request.POST.getlist('addressLine1'),
                request.POST.getlist('addressLine2'), request.POST.getlist('addressNumber'),
                request.POST.getlist('neighborhood'), request.POST.getlist('zipCode'), 
                request.POST.getlist('addressType'), request.POST.getlist('city'),
                request.POST.getlist('foreignCountry'), request.POST.getlist('foreignState'),
                request.POST.getlist('foreignCity'))
    
    # save documents (using Document APP)
    documentSave(person, request.POST.getlist('document_typeDocument'), request.POST.getlist('document_document'), request.POST.getlist('document_issuer'), request.POST.getlist('document_state'))

    return person