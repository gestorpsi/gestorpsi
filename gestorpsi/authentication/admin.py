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
   I{This model was created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.authentication.models import Profile, Role

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username','organization__name']
admin.site.register(Profile, ProfileAdmin)    

class RoleAdmin(admin.ModelAdmin):
    search_fields = ['profile__user__username','profile__organization__name']
admin.site.register(Role, RoleAdmin)
