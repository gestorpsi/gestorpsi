from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from gestorpsi.client.models import Client, Phone, ClientForm, PhoneForm

def index(request):
    clientList = Client.objects.all()
    return render_to_response('client/client_index.html', {'clientList': clientList})

def detail (request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    c = ClientForm(instance=client)
    return render_to_response('client/client_detail.html', {'client': client, 'clientForm': c })
    
def detail1(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    ClientForm = forms.form_for_instance(client)
    clientForm = ClientForm()
    return render_to_response('client/client_detail.html', {'client': client, 'clientForm': clientForm })

def add(request):
    return render_to_response('client/client_add.html', {'clientForm': ClientForm(), 'phoneForm': PhoneForm() } )

def save(request):
    client = Client(name= request.POST['name'],email= request.POST['email'],birthDate= request.POST['birthDate'])
    phones_area   = request.POST.getlist('area')
    phones_number = request.POST.getlist('phoneNumber')
    phones_exts   = request.POST.getlist('ext')
    total = len(phones_number)
    client.save()
    for i in range(0, total):
        if (len(phones_number[i])):
            client.phone_set.create(area=phones_area[i],phoneNumber=phones_number[i],ext=phones_exts[i])
    return render_to_response('client/client_save.html', {'result': "OK"})
    
#def save2(request):
#    clientForm = ClientForm(request.POST)
#    if clientForm.is_valid():
#        print "--------------------------------------------> cliente eh valido!!!"
#        clientForm.save()
#        phones_area   = request.POST.getlist('area')
#        phones_number = request.POST.getlist('phoneNumber')
#        phones_exts   = request.POST.getlist('ext')
#        total = len(phones_number)
#        for i in range(0, total):
#            if (len(phones_number[i])):
#                phone = PhoneForm()
#                phone.area = phones_area[i]
#                phone.phoneNumber = phones_number[i]
#                phone.ext = phones_exts[i]
#                phone.client = clientForm
#                if phone.is_valid():
#                    print "--------------------------------------------> telefone eh valido!!!"
#                    phone.save()
#                else:
#                    print "--------------------------------------------> TELEFONE NAO EH VALIDO !!!"
#        return render_to_response('client/client_save.html', {'result': "OK"})
#    else:
#        return render_to_response('client/client_add.html', {'clientForm': clientForm, 'result': "Validation Problems"})
        
#def save1(request):
#    clientForm = ClientForm(request.POST)
#    
#    phones_area   = request.POST.getlist('area')
#    phones_number = request.POST.getlist('phoneNumber')
#    phones_exts   = request.POST.getlist('ext')
#    total = len(phones_number)
#    phoneList = []
#    for i in range(0,total):
#        if (len(phones_number[i])):    # verify if phone number isn't a blank field
#            phone  = PhoneForm()
#            phone.area = phones_area[i]
#            phone.phoneNumber = phones_number[i]
#            phone.ext = phones_exts[i]
#            phone.client = clientForm
#            phone.save()
#            #phoneList.append(phone)
#    #if clientForm.is_valid():
#    #    #for p in phoneList:
#    #    #    p.client = clientForm
#    #    #    print "cliente: %s" % p.client
#    #    #    if p.is_valid():
#    #    #        print "telefone eh valido"
#    #    #        p.save(commit=False)
#    #    #    else:
#    #    #        print "telefone nao eh valido: %s" % p.errors()
#    #    #    #clientForm.phone_set.create(p)
#    #    #clientForm.save()
#    #    #print "salvando cliente"
#    #    clientForm.phone = phoneList
#    #    print "-------------> %s" % clientForm.phone
#    #    clientForm.save()
#    #    return render_to_response('client/client_save.html', {'result': "OK"})
#    #else:
#    #    return render_to_response('client/client_add.html', {'clientForm': clientForm, 'result': "Validation Problems"})

def update(request):
    #FormCliente = forms.form_for_model(Cliente)
    #formCliente = FormCliente(request.POST)
    #if formCliente.is_valid():
    #    formCliente.save()
    #    return render_to_response('cliente_save.txt', {'resultado': "OK"})
    #else:
    #    return render_to_response('cliente_add.txt', {'formCliente': formCliente, 'resultado': "PROBLEMAS DE VALIDACAO"})
    return HttpResponse("Ainda falta arrumar ....")

def delete(request, client_id):
    return HttpResponse("O camarada numero %s foi excluido da face da Terra.<br><small><small><small>mentira.... a exclusao ainda sera desenvolvida</small></small></small>" % client_id)