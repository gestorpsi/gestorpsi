from django.http import HttpResponse, Http404 
from gestorpsi.address.models import City

def search_city(request, city_name):
    result = ""
    if len(city_name) >= 3:
        cities = City.objects.filter(name__istartswith = city_name)
        for city in cities:
            result += "%s (%s)|%s|\n" % (city.name, city.state.shortName, city.id)
        #result = "["
        #for city in cities:
        #    result += "[%s,\"%s (%s)\"]," % (city.id, city.name, city.state.shortName)
        #result += "]" 
    return HttpResponse("%s" % result)

#def select_city(request, city_id):
#    city = City.objects.get(pk=city_id)
#    return HttpResponse("[[\"%s\",\"%s\"]]" % (city.id, city.name))
#
#def select_state(request, city_id):
#    city = City.objects.get(pk=city_id)
#    return HttpResponse("[[\"%s\",\"%s\"]]" % (city.state.id, city.state.shortName))
#
#def select_country(request, city_id):
#    city = City.objects.get(pk=city_id)
#    return HttpResponse("[[\"%s\",\"%s\"]]" % (city.state.country.id, city.state.country.name))