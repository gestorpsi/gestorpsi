from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from gestorpsi.service.models import Service, ServiceForm, ResearchProject, Agreement
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.organization.models import Organization
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    list_of_services= Service.objects.all()
    return render_to_response( "service/service_index.html", locals() )

def form(request, object_id):
    try:
        object= get_object_or_404( Service, pk= object_id )
    except (Http404, ObjectDoesNotExist):
        object= Service()
    service_form= ServiceForm( instance= object )
    return render_to_response('service/service_html.html', {'object': object, 'service_form': service_form } )

def save_agreements( list_of_agreements, object ):
    object.agreements.clear()
    object.save()
    for agreement_id in list_of_agreements:
        agreement= Agreement.objects.get( pk= agreement_id )
        object.agreements.add( agreement )
        
def save_responsibles( list_of_responsibles, object ):
    object.responsibles.clear()
    object.save()
    for responsible_id in list_of_responsibles:
        responsible= CareProfessional.objects.get(pk= responsible_id )
        object.responsibles.add( responsible )

def save(request, object_id):
    try:
        object= get_object_or_404( Service, pk= object_id )
    except (Http404, ObjectDoesNotExist):
        object= Service()
    
    object.name= request.POST['name']
    object.description= request.POST['description']
    object.keywords= request.POST['keywords']
    object.research_project= ResearchProject.objects.get(pk= request.POST['research_project'])
    object.save()
    
    if ( request.POST['organization'] != '' ):
        organization= Organization.objects.get(pk= request.POST['organization'] )
        object.organization= organization
    
    save_agreements( request.POST.getlist('agreements'), object )
    save_responsibles( request.POST.getlist('responsibles'), object )
     
    object.save()
    service_form= ServiceForm( instance= object )
    return render_to_response('service/service_html.html', {'object': object, 'service_form': service_form } )

def delete(request, object_id):
    object= get_object_or_404( Service, pk= object_id )
    object.delete()
    list_of_services= Service.objects.all()
    return render_to_response( "service/service_index.html", locals() )