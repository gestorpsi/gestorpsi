from django.http import HttpResponse, Http404 
from gestorpsi.address.models import Country, Address, City, AddressType


# append addresses
def addressList(addressPrefixs, addressLines1, addressLines2, addressNumbers, neighborhoods, zipCodes, addressTypes, city_ids, country_ids, stateChars, cityChars):
    total = len(addressLines1)
    objects = []
    
    for i in range(0, total):
        if (len(addressLines1[i])):
            
            #Permitir que Cidade ou Pais seja em branco
            #Do jeito que esta ocorrera uma exception  
            if(len(city_ids[i])):
                #city_id=City.objects.get(pk=city_ids[i])          
                objects.append(Address(addressPrefix=addressPrefixs[i], addressLine1=addressLines1[i], addressLine2=addressLines2[i], 
                                   addressNumber=addressNumbers[i], neighborhood=neighborhoods[i], zipCode=zipCodes[i],
                                   addressType=AddressType.objects.get(pk=addressTypes[i]),
                                   city = City.objects.get(pk=city_ids[i])
                                  ))
            else:
                objects.append(Address(addressPrefix=addressPrefixs[i], addressLine1=addressLines1[i], addressLine2=addressLines2[i], 
                                   addressNumber=addressNumbers[i], neighborhood=neighborhoods[i], zipCode=zipCodes[i],
                                   addressType=AddressType.objects.get(pk=addressTypes[i]),
                                    foreignCountry=Country.objects.get(pk=country_ids[i]),
                                   foreignState=stateChars[i],
                                   foreignCity=cityChars[i]
                                   ))
            
    return objects



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