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

from django.utils.translation import ugettext_lazy as _
from django.db import models

from gestorpsi.client.models import Client

STATUS = ( 
        ('0',_(u'Aberto')),
        ('1',_(u'Pago')),
        ('2',_(u'Faturado')),
        ('3',_(u'Cancelado')),
)


class PaymentWay(models.Model):
    name = models.CharField(_(u"Name"), max_length=100)
    is_active = models.BooleanField(u'Disponível', default=True)
    comment = models.TextField(_('Comments'), blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name


class Payment(models.Model):
    '''
        receive payment
            referral covenant
            to pay, phone, internet, monthly bullet
        informations about payment, payment way, check, value, dead line and others
    '''
    created = models.DateTimeField(_('Criado'), auto_now_add=True, default='2000-12-31 00:00:00')
    status = models.CharField(_(u'Status'), max_length=2, choices=STATUS, default='0')
    payment_way = models.ForeignKey(PaymentWay, null=False, blank=False)
    price = models.DecimalField(_(u'Valor'), max_digits=6, decimal_places=2, null=False, blank=False) # from covenance
    off = models.DecimalField(_(u'Desconto'), max_digits=6, decimal_places=2, null=False, blank=False)
    total = models.DecimalField(_(u'Total'), max_digits=6, decimal_places=2, null=False, blank=False)
    comment = models.TextField(_('Comments'), blank=True, null=True)

    # fk
    referral = models.ForeignKey('referral.Referral', null=True, blank=True)
    #client = models.ForeignKey(Client, null=True, blank=True)
    #service = models.ForeignKey('service.Service', null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.id
