from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.newforms import form_for_model, form_for_instance
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, AcademicResumeForm, WorkPlaces, WorkPlacesForm, Profession, Agreement, ProfessionalProfile, ProfessionalProfileForm, LicenceBoard, ProfessionalIdentification, ProfessionalIdentificationForm, CareProfessional, CareProfessionalForm, InstitutionTypeForm, PostGraduateForm, ProfessionForm, AgreementForm
from gestorpsi.psychologist.models import Approaches, Area, AgeGroup, Psychologist, ApproachesForm, AreaForm, AgeGroupForm, PsychologistForm
from gestorpsi.careprofessional.views import careProfessionalFill


def index(request):
    return render_to_response('psychologist/psychologist_index.html', {'object': Psychologist.objects.all().filter(active = True)})
    

def form(request, object_id=0):
    try:
        phones = []
        addresses = []
        
        object = get_object_or_404(Psychologist, pk=object_id)
        
         # person have phones
        phones= object.person.phones.all()
        
        # person have addresses
        addresses= object.person.address.all()       
                        
        psychologist_form= PsychologistForm( instance=object )
        
        person = Person.objects.filter(id=object.person_id)
        
        person_form = PersonForm( instance=person )
        
    except:
        object = CareProfessional()
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
        
    return render_to_response('psychologist/psychologist_form.html', {'object': object, 
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
                                                                              'psychologist_form': psychologist_form })

# Save or Update psychologist object
def save(request, object_id=0):    
    try:
        object = get_object_or_404(Psychologist, pk=object_id)        
    except Http404:
        object = Psychologist()
        
    #Approaches
    approaches = Approaches()
    approaches.description = request.POST['description']
    approaches.save()
    
    #Area
    area = Area()
    area.description = request.POST['description']
    area.save()        
    
    #AgeGroup
    ageGroup = AgeGroup()
    ageGroup.description = request.POST['description']
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

