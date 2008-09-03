# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.sponsor.models import Sponsor, TaxWithHold

class TaxWithHoldAdmin(admin.ModelAdmin):
    pass

class SponsorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(TaxWithHold, TaxWithHoldAdmin)