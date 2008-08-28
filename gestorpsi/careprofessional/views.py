from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, Profession, Agreement, ProfessionalProfile, LicenceBoard, ProfessionalIdentification, CareProfessional
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.place.models import Place
from gestorpsi.organization.models import Organization
from gestorpsi.person.views import person_save

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
    emails    = []
    sites     = []
    instantMessengers = []

    try:
        object = get_object_or_404(CareProfessional, pk=object_id)
        phones= object.person.phones.all()
        addresses= object.person.address.all()
        documents = object.person.document.all()                       
        emails    = object.person.emails.all()
        sites     = object.person.sites.all()
        instantMessengers = object.person.instantMessengers.all()
    except:
        object = CareProfessional() 
    

    return render_to_response('careprofessional/careprofessional_form.html',
                               
                                {
                                    'object': object,
                                    'emails': emails,
                                    'websites': sites,
                                    'ims': instantMessengers,
                                    'addresses': addresses,
                                    'phones': phones,
                                    'documents': documents,
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
    object.person = person_save(request, person)   
    
    """
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
    
    #Profession
    profession = Profession()
    profession.number = request.POST['number']
    profession.description = request.POST['description']
    profession.save()
    """ 
    
    #Agreement
    if(request.POST['professional_agreement']):
        agreement = Agreement()
        agreement.description = request.POST['professional_agreement']
        agreement.save()
    
    #ProfessionalProfile
    profile = ProfessionalProfile()
    
    """
    if(request.POST['academicResume']):
        profile.academicResume = AcademicResume.objects.get(pk=request.POST['academicResume'])
    else:
        profile.academicResume = resume
    
    profile.initialPrifessionalActivities = request.POST['initialPrifessionalActivities']
        
    if(request.POST['agreement']):
        profile.agreement = Agreement.objects.get(pk=1)
    else:
        profile.agreement = agreement
    """
    
    if(request.POST['professional_agreement']):
       profile.agreement = Agreement.objects.get(pk=request.POST['professional_agreement'])
    
    """
    if(request.POST['profession']):        
        profile.profession = Profession.objects.get(pk=1)
    else:
        profile.profession = profession
        
    profile.services = request.POST['services']
    profile.availableTime = request.POST['availableTime']
    """
       
    if(request.POST['professional_workplace']):
        profile.workplace = Place.objects.get(pk=request.POST['professional_workplace'])
        
    profile.save()
    
    """
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
    """
    object.professionalProfile = profile
    
    """
    object.professionalIdentification = identification    
    object.comments = request.POST['comments']
    """
        
    return object