# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, Profession, Agreement, ProfessionalProfile, LicenceBoard, ProfessionalIdentification, CareProfessional 
from gestorpsi.psychologist.models import Approaches, Area, AgeGroup, Psychologist
from gestorpsi.careprofessional.views import careProfessionalFill


def index(request):
    """
    This view function returns a list that contains all psychologists currently in the system.
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    """
    return render_to_response('psychologist/psychologist_index.html', {'object': Psychologist.objects.all().filter(active = True)})
    

def form(request, object_id=0):
    """
    This function view creates a psychologist form. If the object_id has a value, this form will be fill with psychologist information.
    otherwise, a new form will be create
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: it is the I{id} of the psychologist that must be saved.
    @type object_id: an instance of the built-in type C{int}. 
    """
    try:
        phones = []
        addresses = []
        
        object = get_object_or_404(Psychologist, pk=object_id)
        
         # person have phones
        phones= object.person.phones.all()
        
        # person have addresses
        addresses= object.person.address.all()               
                
        person = Person.objects.filter(id=object.person_id)
       
        
    except:
        object = Psychologist()
                
        
    return render_to_response('psychologist/psychologist_form.html', {'object': object,                                                                               
                                                                              'phones': phones, 
                                                                              'countries': Country.objects.all(), 
                                                                              'PhoneTypes': PhoneType.objects.all(), 
                                                                              'AddressTypes': AddressType.objects.all(), 
                                                                              'States': State.objects.all(),
                                                                              })

# Save or Update psychpsychologistologist object
def save(request, object_id=0):    
    """
    This function view saves a psychologist, its address and phones.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: it is the I{id} of the psychologist that must be saved.
    @type object_id: an instance of the built-in type C{int}. 
    """
    try:
        object = get_object_or_404(Psychologist, pk=object_id)        
    except Http404:
        object = Psychologist()
    
    """    
    #Approaches
    approaches = Approaches()
    approaches.description = request.POST['professional_approaches']
    approaches.save()
    
    #Area
    area = Area()
    area.description = request.POST['professional_area']
    area.save()        
    
    #AgeGroup
    ageGroup = AgeGroup()
    ageGroup.description = request.POST['professional_age']
    ageGroup.save()     
     
    if(request.POST['professional_approaches']):
        object.approaches = Approaches.objects.get(pk=request.POST['professional_approaches'])    
        
    if(request.POST['professional_area']):
        object.specialistArea = Area.objects.get(pk=request.POST['professional_area'])
        
    if(request.POST['professional_age']):
        object.ageGroup = AgeGroup.objects.get(pk=request.POST['professional_age'])
    """
        
    object = careProfessionalFill(request, object)
    object.save()

    return HttpResponse(object.id)

# delete (disable) a psychologist
def delete(request, object_id):
    """
    This function view search for a psychologist which has the id equals to the C{int} (I{psychologist_id})
    passed as parameter and change the field I{active} to "False' 
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: represents the I{id} of the psychologist to be deleted.
    @type object_id: an instance of the built-in class C{int}.
    """
    object = get_object_or_404(Psychologist, pk=object_id)
    object.active = False
    object.save()    
    return render_to_response('psychologist/psychologist_index.html', {'object': Psychologist.objects.all().filter(active = True)})

