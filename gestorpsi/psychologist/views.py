from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, AcademicResumeForm, WorkPlaces, WorkPlacesForm, Profession, Agreement, ProfessionalProfile, ProfessionalProfileForm, LicenceBoard, ProfessionalIdentification, ProfessionalIdentificationForm, CareProfessional, CareProfessionalForm, InstitutionTypeForm, PostGraduateForm, ProfessionForm, AgreementForm
from gestorpsi.psychologist.models import Approaches, Area, AgeGroup, Psychologist, ApproachesForm, AreaForm, AgeGroupForm, PsychologistForm
from gestorpsi.careprofessional.views import careProfessionalFill


def index(request):
    return render_to_response('psychologist/psychologist_index.html', {'object': Psychologist.objects.all().filter(active = True)})
    
# Save or Update psychologist object
def save(request, object_id=0):    
    try:
        object = get_object_or_404(Psychologist, pk=object_id)        
    except Http404:
        object = Psychologist()
        
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
     
    if(request.POST['approaches']):
        object.approaches = Approaches.objects.get(pk=request.POST['approaches'])
    else:
        object.approaches = approaches
        
    if(request.POST['specialistArea']):
        object.specialistArea = Area.objects.get(pk=request.POST['specialistArea'])
    else:
        object.specialistArea = area
    
    if(request.POST['ageGroup']):
        object.ageGroup = AgeGroup.objects.get(pk=request.POST['ageGroup'])
    else:
        object.ageGroup = ageGroup
    
    object = careProfessionalFill(request, object)
    object.save()

    return HttpResponse(object.id)

# delete (disable) a psychologist
def delete(request, object_id):
    object = get_object_or_404(Psychologist, pk=object_id)
    object.active = False
    object.save()    
    return render_to_response('psychologist/psychologist_index.html', {'object': Psychologist.objects.all().filter(active = True)})

