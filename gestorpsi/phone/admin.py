# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{This model was created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.phone.models import PhoneType

class PhoneTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(PhoneType, PhoneTypeAdmin)