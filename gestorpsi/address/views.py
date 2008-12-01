# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from gestorpsi.address.models import Country, Address, City, AddressType

# Check if addresses fields are equals
def is_equal(address):
    try:
        address_db = Address.objects.get(pk=address.id)
    except:
        return False
    if cmp(address_db, address) == 0:
        return True
    else:
        return False

# append addresses
def address_list(ids, addressPrefixs, addressLines1, addressLines2, addressNumbers, neighborhoods, zipCodes, addressTypes, city_ids, country_ids, stateChars, cityChars):
    objects = []
    for i in range(0, len(addressLines1)):
        if (len(addressLines1[i])):
            if(len(city_ids[i])):          
                objects.append(Address(id=ids[i], addressPrefix=addressPrefixs[i], addressLine1=addressLines1[i], addressLine2=addressLines2[i], 
                                   addressNumber=addressNumbers[i], neighborhood=neighborhoods[i], zipCode=zipCodes[i],
                                   addressType=AddressType.objects.get(pk=addressTypes[i]),
                                   city = City.objects.get(pk=city_ids[i])))
            else:
                objects.append(Address(id=ids[i], addressPrefix=addressPrefixs[i], addressLine1=addressLines1[i], addressLine2=addressLines2[i], 
                                   addressNumber=addressNumbers[i], neighborhood=neighborhoods[i], zipCode=zipCodes[i],
                                   addressType=AddressType.objects.get(pk=addressTypes[i]),
                                   foreignCountry=Country.objects.get(pk=country_ids[i]),
                                   foreignState=stateChars[i],
                                   foreignCity=cityChars[i]))
            
    return objects

# 'address' field blank means that it was deleted by an user
# So, if len(address) == 0 AND len(id) != 0, delete address using id
def address_delete(ids, addressLines1): 
    for i in range(0, len(addressLines1)):
        if (not len(addressLines1[i]) and len(ids[i])):
            Address.objects.get(pk=ids[i]).delete()

# Save address
#def address_save(object, ids, addressPrefixs, addressLines1, addressLines2, addressNumbers, neighborhoods, zipCodes, addressTypes, city_ids, country_ids, stateChars, cityChars):
#    address_delete(ids, addressLines1)
#    for address in address_list(ids, addressPrefixs, addressLines1, addressLines2, addressNumbers, neighborhoods, zipCodes, addressTypes, city_ids, country_ids, stateChars, cityChars):
#        if not is_equal(address):
#            address.content_object = object
#            address.save()

def address_save(object, ids, addressPrefixs, addressLines1, addressLines2, addressNumbers, neighborhoods, zipCodes, addressTypes, city_ids, country_ids, stateChars, cityChars):
    object.address.all().delete()
    for address in address_list(ids, addressPrefixs, addressLines1, addressLines2, addressNumbers, neighborhoods, zipCodes, addressTypes, city_ids, country_ids, stateChars, cityChars):
        address.content_object = object
        address.save()

# search a city by name via Ajax
def search_city(request, city_name):
    result = ""
    if len(city_name) >= 3:
        cities = City.objects.filter(name__istartswith = city_name)
        for city in cities:
            result += "%s (%s)|%s|\n" % (city.name, city.state.shortName, city.id)
    return HttpResponse("%s" % result)
