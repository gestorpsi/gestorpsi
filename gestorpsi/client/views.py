from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from gestorpsi.client.models import Client
from gestorpsi.phone.models import Phone

def phoneList(areas, numbers, exts, types):
    total = len(numbers)
    phones = []
    for i in range(0, total):
        if (len(numbers[i])): 
            phones.append(Phone(area=areas[i],phoneNumber=numbers[i],ext=exts[i],phoneType=types[i]))
    return phones

def index(request): 
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })

def form(request, client_id=0):
    try:
        phones = []
        client = get_object_or_404(Client, pk=client_id)
        # colocar client.phones.all() direto no return
        for phone in client.phones.all():
            phones.append(phone)
    except:
        client = Client()
    return render_to_response('client/client_form.html', {'client': client, 'phones': phones, 'person': client } )

def save(request, client_id=0):
    try:
        client = get_object_or_404(Client, pk=client_id)
    except Http404:
        client = Client()
    client.name = request.POST['name']
    client.email = request.POST['email']
    client.birthDate = request.POST['birthDate']
    client.save()
    client.phones.all().delete()
    for phone in phoneList(request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType')):
        phone.content_object = client
        phone.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })

def delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.active = False
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(active = True) })