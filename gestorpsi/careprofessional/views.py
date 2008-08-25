from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, AcademicResumeForm, WorkPlaces, WorkPlacesForm, Profession, Agreement, ProfessionalProfile, ProfessionalProfileForm, LicenceBoard, ProfessionalIdentification, ProfessionalIdentificationForm, CareProfessional, CareProfessionalForm, InstitutionTypeForm, PostGraduateForm, ProfessionForm, AgreementForm
from gestorpsi.person.views import personSave
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.place.models import Place
from gestorpsi.organization.models import Organization

PROFESSIONAL_AREAS = (
    ('psycho','Psychologist','CRP'),
    )  


def index(request):
    workplaces = Place.objects.all()  # aqui ta pegando todos os places, e eh preciso filtrar apenas para a organizacao que ta sendo usada. Mas nao consegui fazer isso =) ** ja inclui os imports de place e organization
    return render_to_response('careprofessional/careprofessional_index.html', {
                                    'object': CareProfessional.objects.all().filter(active = True),
                                    
                                    'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,
                                    #'identification_form': identification_form,
                                    'licenceBoardTypes': LicenceBoard.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                    'WorkPlacesTypes': workplaces,
                                    'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(),
                                                                               
                                                                               })
  

def form(request, object_id=0):
    phones = []
    addresses = []
    workplaces = Place.objects.all()  # aqui ta pegando todos os places, e eh preciso filtrar apenas para a organizacao que ta sendo usada. Mas nao consegui fazer isso =) ** ja inclui os imports de place e organization
    
    try:
        object = get_object_or_404(CareProfessional, pk=object_id)
        
         # person have phones
        phones= object.person.phones.all()
        
        # person have addresses
        addresses= object.person.address.all()
        
        # person have documents
        documents = object.person.document.all()
                        
        #psychologist_form= PsychologistForm( instance=object )
        
        #person = Person.objects.filter(id=object.person_id)
        
        #person_form = PersonForm( instance=person )
        
    except:
        object = CareProfessional()
        '''
        careprofessional_form= CareProfessionalForm()
        person_form = PersonForm()
        address_form = AddressForm()
        institute_form = InstitutionTypeForm()
        postGraduate_form = PostGraduateForm()
        profession_form = ProfessionForm()
        agreement_form = AgreementForm ()
        resume_form = AcademicResumeForm()
        workPlaces_form = WorkPlacesForm()
        profile_form = ProfessionalProfileForm()
        identification_form = ProfessionalIdentificationForm()
        approaches_form = ApproachesForm()
        area_form = AreaForm()
        ageGroup_form = AgeGroupForm()
        psychologist_form= PsychologistForm()        
        '''

    '''    
    return render_to_response('careprofessional/careprofessional_form.html',
                               
                                {
                                    'object': object, 
                                    'careprofessional_form': careprofessional_form, 
                                    'person_form': person_form, 
                                    'institute_form': institute_form, 
                                    'postGraduate_form': postGraduate_form, 
                                    'profession_form': profession_form, 
                                    'agreement_form': agreement_form, 
                                    'resume_form': resume_form, 
                                    'workPlaces_form': workPlaces_form, 
                                    'profile_form': profile_form, 
                                    'identification_form': identification_form, 
                                    'address_form': address_form, 
                                    'phones': phones, 
                                    'countries': Country.objects.all(), 
                                    'PhoneTypes': PhoneType.objects.all(), 
                                    'AddressTypes': AddressType.objects.all(), 
                                    'States': State.objects.all(),
                                    'approaches_form': approaches_form,
                                    'area_form': area_form,
                                    'ageGroup_form': ageGroup_form,
                                    'psychologist_form': psychologist_form }
                                    
                                )
    '''

    return render_to_response('careprofessional/careprofessional_form.html',
                               
                                {
                                    'object': object,
                                    'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,
                                    #'identification_form': identification_form,
                                    'licenceBoardTypes': LicenceBoard.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                    'WorkPlacesTypes': workplaces,
                                    'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(),
                                }
                                    
                                )

def careProfessionalFill(request, object):
    
    """
    This view function returns the informations about CareProfessional 
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    @param object: it is the tyoe of CareProfessional that must be filled.
    @type object: an instance of the built-in type C{Psychologist}.            
    """
    
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
    
    #workPlaces = WorkPlaces()
    #workPlaces.name = request.POST['name']
    #workPlaces.save()
    
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




