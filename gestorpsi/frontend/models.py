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

from django.db import models
from django.contrib.auth.models import User, UserManager, Group


# ultimos cadastrados
# field SORT ? Alphabetics? Last 10? First 10?

SORT = (
    (1, u'alfabética'),
    (2, u'data cadastro'),
)

LIMIT = (
    (0, u'Não mostrar'),
    (10, u'10 ultimos'),
    (15, u'15 ultimos'),
    (010, u'10 primeiros'),
    (015, u'15 primeiros'),
    (99 , u'Todos?'),
)

class FrontendProfile(models.Model):
    """
    careprofessional:
        list of careprofessional, client, services and others
        don't show of other careprofessional'

    secretary:
        all clients, all services, all queue, all...
    """
    user = models.OneToOneField(User, unique=True)

    service = models.IntegerField(u'Serviço', default=10, choices=LIMIT)
    service_sort = models.IntegerField(u'Ordenar serviço', default=1, choices=SORT)

    referral = models.IntegerField(u'Inscrição', default=10, choices=LIMIT)
    referral_sort = models.IntegerField(u'Ordenar inscrição', default=1, choices=SORT)

    client = models.IntegerField(u'Client', default=10, choices=LIMIT)
    client_sort = models.IntegerField(u'Ordenar client', default=1, choices=SORT)

    student = models.IntegerField(u'Studante', default=10, choices=LIMIT)
    schedule = models.IntegerField(u'Agenda', default=10, choices=LIMIT)
    queue = models.IntegerField(u'Fila', default=10, choices=LIMIT)
    birthdate_client = models.IntegerField(u'Aniversário', default=10, choices=LIMIT)
    subscribe_client = models.IntegerField(u'Inscrição cliente', default=10, choices=LIMIT)

    def __unicode__(self):
        return u"%s" % (self.profile)
