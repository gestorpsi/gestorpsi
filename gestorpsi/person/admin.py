# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.person.models import MaritalStatus, Person

class MaritalStatusAdmin(admin.ModelAdmin):
    pass

class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(MaritalStatus, MaritalStatusAdmin)
admin.site.register(Person, PersonAdmin)