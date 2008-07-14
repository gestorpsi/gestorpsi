from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from gestorpsi.client.models import Client, Phone, ClientForm, PhoneForm

def index(request): 
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })

def form(request, client_id=0):
    phones = []
    try:
        client = get_object_or_404(Client, pk=client_id)
        for phone in client.phone_set.all():
            phones.append(phone)
    except:
        client = Client()
    return render_to_response('client/client_form.html', {'client': client, 'phones': phones } )
    

def save(request):
    client = Client(name= request.POST['name'],email= request.POST['email'],birthDate= request.POST['birthDate'])
    client.save()
    phones_area   = request.POST.getlist('area')
    phones_number = request.POST.getlist('phoneNumber')
    phones_exts   = request.POST.getlist('ext')
    total = len(phones_number)
    for i in range(0, total):
        if (len(phones_number[i])):
            client.phone_set.create(area=phones_area[i],phoneNumber=phones_number[i],ext=phones_exts[i])
    return render_to_response('client/client_save.html', {'result': "OK"})

def update(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.name = request.POST['name']
    client.email = request.POST['email']
    client.birthDate = request.POST['birthDate']
    client.save()
    client.ob
    phones = phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'))
    for p in phones:
        print p
 

    #FormCliente = forms.form_for_model(Cliente)
    #formCliente = FormCliente(request.POST)
    #if formCliente.is_valid():
    #    formCliente.save()
    #    return render_to_response('cliente_save.txt', {'resultado': "OK"})
    #else:
    #    return render_to_response('cliente_add.txt', {'formCliente': formCliente, 'resultado': "PROBLEMAS DE VALIDACAO"})
    return HttpResponse("Alteracao do Cliente %s efetuada com sucesso." % client.name)

def phoneList(areas, numbers, exts):
    total = len(numbers)
    phones = []
    for i in range(0, total):
        if (len(numbers[i])): 
            phones.append(Phone(area=areas[i],phoneNumber=numbers[i],ext=exts[i]))
    return phones

def delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.active = False
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })