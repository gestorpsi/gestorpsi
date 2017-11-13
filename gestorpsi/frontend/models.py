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
from django.contrib.auth.models import User
from gestorpsi.service.models import Service


# ultimos cadastrados
# field SORT ? Alphabetics? Last 10? First 10?

SORT = (
    (1, u'alfabética'),
    (2, u'data cadastro'),
)

LIMIT = (
    (0, u'Não mostrar'),
    (5, u'5 primeiros'),
    (10, u'10 primeiros'),
    (15, u'15 primeiros'),
    (20, u'20 primeiros'),
    (25, u'25 primeiros'),
    (30, u'30 primeiros'),
    (35, u'35 primeiros'),
    (40, u'40 primeiros'),
    (45, u'45 primeiros'),
    (50, u'50 primeiros'),
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
    my_service = models.ManyToManyField(Service, verbose_name=u'Serviço', null=True, blank=True)
    referral = models.IntegerField(u'Inscrição', default=10, choices=LIMIT)
    referral_sort = models.IntegerField(u'Ordenar inscrição', default=2, choices=SORT)
    client = models.IntegerField(u'Cliente', default=10, choices=LIMIT)
    client_sort = models.IntegerField(u'Ordenar cliente', default=1, choices=SORT)
    queue = models.IntegerField(u'Fila', default=10, choices=LIMIT)
    queue_sort = models.IntegerField(u'Ordenar fila', default=2, choices=SORT)
    birthdate_client = models.IntegerField(u'Aniversário', default=10, choices=LIMIT)
    birthdate_sort = models.IntegerField(u'Ordenar Aniversário', default=2, choices=SORT)
    student = models.IntegerField(u'Estagiário', default=10, choices=LIMIT)
    student_sort = models.IntegerField(u'Ordenar estagiário', default=1, choices=SORT)
    schedule = models.IntegerField(u'Agenda', default=10, choices=LIMIT)
    subscribe_client = models.IntegerField(u'Inscrição cliente', default=10, choices=LIMIT)

    def __unicode__(self):
        return u"%s" % (self.user)
