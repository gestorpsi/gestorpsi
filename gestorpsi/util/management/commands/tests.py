# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str
from django.core.management.base import BaseCommand, CommandError

from gestorpsi.person.models import Person
from gestorpsi.address.models import Country

#este arquivo é só para testes
class Command(BaseCommand):
    def handle(self, *args, **options):
        for per in Person.objects.all():
            if per.birthForeignCity is not None and len(per.birthForeignCity) > 0:
                per.birthCountry = Country.objects.get(id=per.birthForeignCountry)
            elif per.birthPlace is not None:
                per.birthCountry = per.birthPlace.state.country
                per.birthState = per.birthPlace.state
            per.save()
        
    
    
    
    
    
    
    
    
        
