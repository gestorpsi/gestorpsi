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
from django.utils.translation import ugettext_lazy as _

from gestorpsi.util.uuid_field import UuidField

CATEGORY = ( 
    (1, _('Pagamento direto')),
    (2, _(u'Plano de saúde privado')),
    (3, _(u'Seguro de saúde privado')),
    (3, _('SUS')),
)

CHARGE = ( 
    (1, _(u'Por evento')),
    (2, _(u'Por pacote')),
    (3, _(u'Seguro de saúde privado')),

    (u'Por período', 
        (
            (10,u'Semana'),
            (11,u'Quinzena'),
            (12,u'Mês'),
            (13,u'Bimestre'),
            (14,u'Semestre'), 
        )
    ),
)

PAYMENT_WAY = (
    (1, _(u'Dinheiro')),
    (2, _(u'Cartão')),
    (3, _(u'Boleto')),
    (4, _(u'Depósito bancário')),
)

DEADLINE = (
    (1, _(u'A vista')),
    (2, _(u'Faturado')),
)

class Covenant(models.Model):
    id = UuidField(primary_key=True)
    date_join = models.DateField(auto_now_add=True, null=False, editable=False)
    name = models.CharField(_(u'Name'), max_length=250, null=False, blank=False)
    active = models.BooleanField(u'Disponível', default=True)
    category = models.IntegerField(u'Categoria', choices=CATEGORY, max_length=2, null=False, blank=False)
    charge = models.IntegerField(u'Cobrança', choices=CHARGE, max_length=2, null=False, blank=False)
    event_time = models.PositiveIntegerField(u'Número de eventos', null=True, blank=True) # if charge=2, show this field
    payment_way = models.IntegerField(u'Forma de pagamento', choices=PAYMENT_WAY, max_length=2, null=False, blank=False)
    price = models.DecimalField(u'Valor', max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(u'Descrição', null=True, blank=True)
    dead_line = models.IntegerField(u'Prazo', choices=DEADLINE, max_length=2, null=False, blank=False)

    def __unicode__(self):
        return u"%s" % self.name
