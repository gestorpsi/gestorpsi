from django.http import HttpResponse, Http404 
from gestorpsi.address.models import City
#from django.core import serializers
#from django.utils import simplejson

def search_city(request, city_name):
    cidades = City.objects.filter(name__istartswith = city_name)
    resultado = "["
    for cidade in cidades:
        resultado += "[%s,\"%s (%s)\"]," % (cidade.id, cidade.name, cidade.state.shortName)
    resultado += "]"        
    return HttpResponse("%s" % resultado)

    #data1 = serializers.serialize("json", City.objects.filter(name__istartswith = city_name), ensure_ascii=False)
    #data2 = serializers.serialize("json", City.objects.filter(name__istartswith = city_name), fields=('id','name'), ensure_ascii=False)
    #return HttpResponse(data1, mimetype="text/javascript")
