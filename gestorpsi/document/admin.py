# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.document.models import TypeDocument, Issuer

class IssuerAdmin(admin.ModelAdmin):
    pass

class TypeDocumentAdmin(admin.ModelAdmin):
    pass

admin.site.register(TypeDocument, TypeDocumentAdmin)
admin.site.register(Issuer, IssuerAdmin)
