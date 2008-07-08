from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from gestorpsi.contacts.models import Establishment, CareProfessional
from django import newforms as forms

def index(request):
    eList = Establishment.objects.all()
    cpList = CareProfessional.objects.all()
    return render_to_response('contacts/contacts_index.html', {'eList': eList, 'cpList': cpList})

def details(request, pID):       
    establishment = get_object_or_404(Establishment, pk=pID)    
    establishmentForm = forms.form_for_instance(establishment)
    eForm = establishmentForm()
    message=""
    
    if request.method =="POST":
        if request.POST['submit']=='Alterar':                    
            
            try:                
                eForm = establishmentForm(request.POST.copy())
                eForm.save()
                message = 'Estabelecimento alterado'
            except:
                message = 'Nao foi possivel alterar este registro!'

    return render_to_response(
        'contacts/contacts_details.html', {'eForm': eForm, 'message': message})

def delete(request, pID):       
    try:
        establishment = Establishment.objects.get(id=pID)
        establishment.delete()
        #establishment = get_object_or_404(Establishment, pk=pID)    
        #establishmentForm = forms.form_for_instance(establishment)    
        #eForm = establishmentForm()
        #eForm.delete()        
        message = 'Estabelecimento excluido'
    except:
        message = 'Nao foi possivel excluir este registro!'

    return render_to_response('contacts/contacts_msg.html', {'message': message})



def add(request):
    EstablishmentForm = forms.form_for_model(Establishment)
    eForm = EstablishmentForm()    
    message=""    
    
    if request.method =="POST":
        if request.POST['submit']=='Adicionar':            
            postData = request.POST.copy()            
            name = postData['name']            
            
            try:                
                eForm = EstablishmentForm(request.POST.copy())
                eForm.save()
                message = 'Estabelecimento %s adicionado com sucesso' % name
            except:
                message = 'Nao foi possivel incluir este registro!'
            
            
    
    return render_to_response(
        'contacts/contacts_add.html', {'eForm': eForm, 'message': message})

