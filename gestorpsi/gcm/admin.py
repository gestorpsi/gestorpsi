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

"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django import forms
from django.contrib import admin

from gestorpsi.gcm.models.invoice import Invoice
from gestorpsi.gcm.models.plan import Plan
from gestorpsi.gcm.models.payment import PaymentType

from datetime import datetime

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'value','duration','staff_size','active')
    list_filter = ('active',)
    pass
admin.site.register(Plan, PlanAdmin)



'''
    filter and action invoice
'''
# pendente
def pendente(modeladmin, request, queryset):
    for obj in queryset:
        obj.date_payed = None
        obj.status = 0
        obj.save()
pendente.short_description = u"Pendente"

# pago pelo cliente - boleto ou cartao
def pagoCliente(modeladmin, request, queryset):
    for obj in queryset:
        obj.date_payed = datetime.today()
        obj.status = 1
        obj.save()
pagoCliente.short_description = u"Pago pelo cliente"

# pago pelo GestorPSI - gratis/teste/cortesia
def pagoGratis(modeladmin, request, queryset):
    for obj in queryset:
        obj.date_payed = datetime.today()
        obj.status = 2
        obj.save()
pagoGratis.short_description = u"Pago / Grátis"


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('organization','start_date','end_date','status','date_payed','plan','ammount')
    list_filter = ('status',)
    actions = [pendente, pagoCliente, pagoGratis]
    search_fields = ['organization__name']
admin.site.register(Invoice, InvoiceAdmin)


class PaymentTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(PaymentType, PaymentTypeAdmin)
