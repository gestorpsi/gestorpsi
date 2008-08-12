from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, AcademicResumeForm, WorkPlaces, WorkPlacesForm, Profession, Agreement, ProfessionalProfile, ProfessionalProfileForm, LicenceBoard, ProfessionalIdentification, ProfessionalIdentificationForm, CareProfessional, CareProfessionalForm, InstitutionTypeForm, PostGraduateForm, ProfessionForm, AgreementForm
from gestorpsi.person.views import personSave


def careProfessionalFill(request, object):
    
    person = Person()
    object.person = personSave(request, person)   
    
    #InstitutionType
    instType = InstitutionType()
    instType.description = request.POST['description']
    instType.save()
    
    #PostGraduate
    postGraduate = PostGraduate()
    postGraduate.description = request.POST['description']
    postGraduate.save()
    
    #AcademicResume
    resume = AcademicResume()    
    resume.teachingInstitute = request.POST['teachingInstitute']
    
    if(request.POST['institutionType']):
        resume.institutionType = InstitutionType.objects.get(pk=request.POST['institutionType'])
    else:
        resume.institutionType = instType
        
    resume.course = request.POST['course']
    resume.initialDateGraduation = request.POST['initialDateGraduation']
    resume.finalDateGraduation = request.POST['finalDateGraduation']
    resume.lattesResume = request.POST['lattesResume']
    
    if(request.POST['postGraduate']):
        resume.postGraduate = PostGraduate.objects.get(pk=request.POST['postGraduate'])
    else:
        resume.postGraduate = postGraduate
        
    resume.initialDatePostGraduate = request.POST['initialDatePostGraduate']
    resume.finalDatePostGraduate = request.POST['finalDatePostGraduate']
    resume.area = request.POST['area']
    resume.save()
    
    workPlaces = WorkPlaces()
    workPlaces.name = request.POST['name']
    workPlaces.save()
    
    #    >>>>>>It's necessary for workplaces
    #    addressType=AddressType(description='Home')
    #    addressType.save()
    #    address = Address()
    #    address.addressPrefix = "Rua"
    #    address.addressLine1 = "Rui Barbosa, 1234"
    #    address.addressLine2 = "Anexo II - Sala 4"object = get_object_or_404(Employee, pk=object_id)    
    #    address.neighborhood = "Centro"
    #    address.zipCode = "12345-123"
    #    address.addressType = AddressType.objects.get(pk=1)
    #    address.city = City.objects.get(pk=44085)
    #    address.content_object = WorkPlaces.objects.get(pk=1)
    #    address.save()
    #    
    #    phoneType = PhoneType( description='Home' )
    #    phoneType.save()
    #    phone = Phone(area='16', phoneNumber='33643223', ext='ttt', phoneType=PhoneType.objects.get(pk=1))
    #    phone.content_object = WorkPlaces.objects.get(pk=1)
    #    phone.save()
    
    #Profession
    profession = Profession()
    profession.number = request.POST['number']
    profession.description = request.POST['description']
    profession.save()
    
    #Agreement
    agreement = Agreement()
    agreement.description = request.POST['description']
    agreement.save()
    
    #ProfessionalProfile
    profile = ProfessionalProfile()
    if(request.POST['academicResume']):
        profile.academicResume = AcademicResume.objects.get(pk=request.POST['academicResume'])
    else:
        profile.academicResume = resume
    
    profile.initialPrifessionalActivities = request.POST['initialPrifessionalActivities']
    
    if(request.POST['agreement']):
        profile.agreement = Agreement.objects.get(pk=1)
    else:
        profile.agreement = agreement
    
    if(request.POST['profession']):        
        profile.profession = Profession.objects.get(pk=1)
    else:
        profile.profession = profession
        
    profile.services = request.POST['services']
    profile.availableTime = request.POST['availableTime']
    
    if(request.POST['workplace']):
        profile.workplace = WorkPlaces.objects.get(pk=1)
    else:
        profile.workplace = workPlaces
    
    profile.save()
    
    #LicenceBoard
    licence = LicenceBoard()
    licence.name = request.POST['name']
    licence.description = request.POST['description']
    licence.save()
    
    #ProfessionalIdentification
    identification = ProfessionalIdentification()
    identification.registerNumber = request.POST['registerNumber']
    
    if(request.POST['licenceBoard']): 
        identification.licenceBoard = LicenceBoard.objects.get(pk=1)
    else:
        identification.licenceBoard = licence
    identification.save()

    object.professionalProfile = profile
    object.professionalIdentification = identification    
    object.comments = request.POST['comments']
        
    return object



