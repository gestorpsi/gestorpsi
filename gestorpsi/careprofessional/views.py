# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, Profession, ProfessionalProfile, LicenceBoard, ProfessionalIdentification, CareProfessional
from gestorpsi.organization.models import Agreement
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.place.models import Place, PlaceType
from gestorpsi.organization.models import Organization
from gestorpsi.person.views import person_save

PROFESSIONAL_AREAS = (
    ('psycho','Psychologist','CRP'),
    )  

def index(request):
    user = request.user
    #care_professionals = CareProfessional.objects.all()
    care_professionals = CareProfessional.objects.filter(person__organization = user.org_active.id) 
          
#            
    #org_results = Person.objects.
    return render_to_response('careprofessional/careprofessional_index.html', {
                                    'object': care_professionals,
                                    'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,
                                    #'identification_form': identification_form,
                                    'licenceBoardTypes': LicenceBoard.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                   # 'WorkPlacesTypes': Place.objects.all(),
                                    'WorkPlacesTypes': Place.objects.filter(organization = user.org_active.id),  # aqui ta pegando todos os places, e eh preciso filtrar apenas para a organizacao que ta sendo usada. Mas nao consegui fazer isso =) ** ja inclui os imports de place e organization
                                    'countries': Country.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(),
                                    'AddressTypes': AddressType.objects.all(),
                                    'EmailTypes': EmailType.objects.all(),
                                    'IMNetworks': IMNetwork.objects.all(),
                                    'TypeDocuments': TypeDocument.objects.all(),
                                    'Issuers': Issuer.objects.all(),
                                    'States': State.objects.all(),
                                    'MaritalStatusTypes': MaritalStatus.objects.all(),
                                    'PlaceTypes': PlaceType.objects.all(),
                                    })
  

def form(request, object_id=''):
    user = request.user
    phones = []
    addresses = []
    emails    = []
    sites     = []
    instantMessengers = []
    documents = []
    workplaces = []
    agreements = []

    try:
        object = get_object_or_404(CareProfessional, pk=object_id)
        phones= object.person.phones.all()
        addresses= object.person.address.all()
        documents = object.person.document.all()                       
        emails    = object.person.emails.all()
        sites     = object.person.sites.all()
        instantMessengers = object.person.instantMessengers.all()
        workplaces = object.professionalProfile.workplace.all()
        agreements = object.professionalProfile.agreement.all()
    except:
        object = CareProfessional() 

    return render_to_response('careprofessional/careprofessional_form.html', {
                                    'object': object,
                                    'emails': emails,
                                    'websites': sites,
                                    'ims': instantMessengers,
                                    'addresses': addresses,
                                    'phones': phones,
                                    'documents': documents,
                                    'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,                                    
                                    'licenceBoardTypes': LicenceBoard.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                    'WorkPlacesTypes': Place.objects.filter(organization = user.org_active.id),
                                    'countries': Country.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(),
                                    'AddressTypes': AddressType.objects.all(),
                                    'EmailTypes': EmailType.objects.all(),
                                    'IMNetworks': IMNetwork.objects.all() ,
                                    'TypeDocuments': TypeDocument.objects.all(),
                                    'Issuers': Issuer.objects.all(),
                                    'States': State.objects.all(),
                                    'MaritalStatusTypes': MaritalStatus.objects.all(),
                                    'PlaceTypes': PlaceType.objects.all(),
                                    'workplaces': workplaces,
                                    'agreements': agreements,                                    
                                    })

def care_professional_fill(request, object):
    """
    This view function returns the informations about CareProfessional 
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    @param object: it is the tyoe of CareProfessional that must be filled.
    @type object: an instance of the built-in type C{Psychologist}.            
    """
    try:
        person= Person.objects.get(pk=object.person_id)        
    except:        
        person= Person()
       
    object.person= person_save(request, person)   
    
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

    #ProfessionalProfile
    try:
        profile= ProfessionalProfile.objects.get(pk= object.professionalProfile_id )
        print "existe perfil"        
    except:        
        print "nao existe perfil"
        profile= ProfessionalProfile()
    
    """
    #Agreement
    if(request.POST['professional_agreement']):
        agreement = Agreement()
        agreement.description = request.POST['professional_agreement']
        agreement.save()
        
    if(request.POST['academicResume']):
        profile.academicResume = AcademicResume.objects.get(pk=request.POST['academicResume'])
    else:
        profile.academicResume = resume
        
    if(request.POST['profession']):        
        profile.profession = Profession.objects.get(pk=1)
    else:
        profile.profession = profession        
    """
    
    profile.initialProfessionalActivities = request.POST[ 'professional_initialActivitiesDate' ]
    profile.availableTime = request.POST['professional_availableTime']
    profile.save()
    
    #profile.services = request.POST['professional_services']    
    
    if ( len( request.POST.getlist( 'professional_agreement' ) ) ):
        for agreemt_id in request.POST.getlist( 'professional_agreement' ):
               #load agreement using the id retrieved from POST
               agreemt= Agreement.objects.get( pk= agreemt_id )
               #links the recently loaded agreement
               profile.agreement.add( agreemt )

    if ( len(request.POST.getlist( 'professional_workplace' ) ) ):
        for wplace_id in request.POST.getlist( 'professional_workplace' ):
            #load the workplace
            wplace= Place.objects.get( pk= wplace_id )
            #associate the place loaded
            profile.workplace.add( wplace )

    object.professionalProfile= profile

    #ProfessionalIdentification
    try:
        identification =  ProfessionalIdentification.objects.get(pk = object.professionalIdentification_id )
    except:
        identification = ProfessionalIdentification()

    try:
        identification.licenceBoard = LicenceBoard.objects.get(pk=request.POST['professional_licenceBoard'])
    except:
        identification.licenceBoard = None
        
        
    
    identification.registerNumber = request.POST['professional_registerNumber']
    identification.save()

    object.professionalIdentification = identification   
     
    #object.comments = request.POST['comments']

    return object
