# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.device.models import DeviceType, Device, DeviceDetails

class DeviceTypeAdmin(admin.ModelAdmin):
    pass

class DeviceAdmin(admin.ModelAdmin):
    pass

class DeviceDetailsAdmin(admin.ModelAdmin):
    pass

admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceDetails, DeviceDetailsAdmin)    