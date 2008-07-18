from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from gestorpsi.contact.models import CareProfessional, CareProfessionalForm
from gestorpsi.organization.models import Organization
from django.newforms import form_for_model

def index(request):
    organization = Organization.objects.all()    
    return render_to_response('contact/contact_index.html', {'organization': organization})


def get(request, organization_id):       
    organization = get_object_or_404(Organization, pk=organization_id)    
    organizationForm = forms.form_for_instance(organization)
    eForm = organizationForm()
    message=""
    
    if request.method =="POST":
        if request.POST['submit']=='Alterar':                    
            
            try:                
                eForm = organizationForm(request.POST.copy())
                eForm.save()
                message = 'Estabelecimento alterado'
            except:
                message = 'Nao foi possivel alterar este registro!'

    return render_to_response(
        'contact/contact_details.html', {'eForm': eForm, 'message': message})


def list_careProfessionals_related_to(request, organization_id):
    careProfessional_list= []
    for careProfessional in CareProfessional.objects.filter( organization__id__exact= int(organization_id) ):
        careProfessional_list.append( CareProfessionalForm( instance= careProfessional ) )
    return render_to_response( 'contact/list_careProfessional.html', { 'careProfessional_list': careProfessional_list } ) 


def delete_organization(request, organization_id):       
    try:
        organization = Organization.objects.get(id=organization_id)
        organization.delete()                
        return render_to_response('contact/contact_msg.html', {'message': "It was successfully deleted"})
    except:
        return render_to_response('contact/contact_msg.html', {'message': "some problem occurred while deleting the organization"})

    
def delete_CareProfessional(request, careProfessional_id):       
    try:
        careProfessional = CareProfessional.objects.get(id=organization_id)
        careProfessional.delete()                
        return render_to_response('contact/contact_msg.html', {'message': "It was successfully deleted"})
    except:
        return render_to_response('contact/contact_msg.html', {'message': "some problem occurred while deleting the CareProfessional"})


def save_CareProfessional(request):
    careProfessional= CareProfessionalForm( request.POST )
    try:        
        careProfessional.save()
        return render_to_response( 'contact/contact_msg.html', { 'message': "It was successfully saved" } )
    except:
        return render_to_response( 'contact/contact_msg.html', { 'message': "some problem occurred while saving the CareProfessional" } )


def delete_CareProfessional(request, organization_id):
    try:
        careProfessional= CareProfessional.objects.get( pk=int(organization_id))           
        careProfessional.save()
        return render_to_response( 'contact/contact_msg.html', { 'message': "It was successfully saved" } )
    except:
        return render_to_response( 'contact/contact_msg.html', { 'message': "some problem occurred while saving the place" } )


def form(request, organization_id):
    try:
        organization = Organization.objects.get(pk=organization_id)
        
        organizationForm = forms.form_for_model(organization)    
        eForm = organizationForm()
        #CareProfessionalForm = forms.form_for_model(CareProfessional, fields=('name', 'gender'))
        #cpForm = CareProfessionalForm()    
        
        message=""    
        
        if request.method =="POST":
            if request.POST['submit']=='Adicionar':            
                postData = request.POST.copy()            
                gender = postData['gender']            
                
                try:                
                    eForm = organizationForm(request.POST.copy())
                    eForm.save()
                    message = 'Estabelecimento %s adicionado com sucesso' % name
                except:
                    message = 'Nao foi possivel incluir este registro!'
                
                
        
        return render_to_response(
            'contact/contact_add.html', {'eForm': eForm, 'message': message})
    except:
        return render_to_response(
            'contact/contact_add.html', {'eForm': eForm, 'message': message})


def add_careProfessional(request, organization_id):              
        org = get_object_or_404(Organization, pk= organization_id )        
        careProfessional= CareProfessional( name= '', gender= '', organization= org )
        care_form= CareProfessionalForm( instance= careProfessional )
        return render_to_response( 'contact/add_careProfessional.html', {'care_form': care_form, 'message': message} )
