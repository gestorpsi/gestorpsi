# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.address.models import AddressType

class AddressTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(AddressType, AddressTypeAdmin) 