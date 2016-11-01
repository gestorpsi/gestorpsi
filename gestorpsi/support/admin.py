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
   @author: Fabio Martins
   @version: 1.0
"""

from django.contrib import admin
from django import forms
from gestorpsi.support.models import Documentation, Ticket

class DocumentationAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('body'):
            return db_field.formfield(widget=forms.Textarea(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(DocumentationAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)

admin.site.register(Documentation, DocumentationAdmin)


class TicketAdmin(admin.ModelAdmin):

    def get_stat_(self):
        return self.get_status_display()

    list_display = ('user','date',get_stat_,'question')
    readonly_fields = ('user','date','ticket_id')
    search_fields = ['user__user__username','question']
    list_filter = ['date','status']

admin.site.register(Ticket, TicketAdmin)
