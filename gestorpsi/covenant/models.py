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
from gestorpsi.organization.models import Organization

CATEGORY = ( 
    (1, _('Pagamento direto')),
    (2, _(u'Plano de saúde privado')),
    (3, _(u'Seguro de saúde privado')),
    (4, _('SUS')),
)

CHARGE = ( 
    (1, _(u'Por evento')),
    (2, _(u'Por pacote')),
    (3, _(u'Seguro de saúde privado')),

    (u'Por período', 
        (
            (10,u'Semanal'),
            (11,u'Quinzenal'),
            (12,u'Mensal'),
            (13,u'Bimestral'),
            (14,u'Semestral'), 
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
    category = models.IntegerField(u'Categoria', choices=CATEGORY, null=False, blank=False)
    charge = models.IntegerField(u'Cobrança', choices=CHARGE, null=False, blank=False)
    payment_way = models.CharField(u'Forma de pagamento', max_length=255, null=False, blank=False, choices=PAYMENT_WAY)
    deadline = models.IntegerField(u'Prazo', choices=DEADLINE, null=False, blank=False)
    active = models.BooleanField(u'Disponível', default=True)
    event_time = models.PositiveIntegerField(u'Número de eventos', null=True, blank=True) # if charge=2, show this field
    price = models.CharField(u'Valor', max_length=10, null=False, blank=False)
    description = models.TextField(u'Descrição', null=True, blank=True)
    organization = models.ForeignKey(Organization, editable=False, null=False, blank=False)

    def __unicode__(self):
        # return need show as this format, relation m2m.
        if self.event_time:
            return u"%s - %s (%s) - R$%s" % ( self.name, self.get_charge_display(), self.event_time, self.price )
        else:
            return u"%s - %s - R$%s" % ( self.name, self.get_charge_display(), self.price )

    class Meta:
        ordering = ['name']
