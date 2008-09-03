# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.internet.models import EmailType, IMNetwork

class EmailTypeAdmin(admin.ModelAdmin):
    pass

class IMNetworkAdmin(admin.ModelAdmin):
    pass

admin.site.register(EmailType, EmailTypeAdmin)
admin.site.register(IMNetwork, IMNetworkAdmin)