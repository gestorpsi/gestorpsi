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
from swingtime.models import Occurrence

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
    name = models.CharField(_('Nome'), max_length=250, null=False, blank=False) # covenant name or billet
    created = models.DateTimeField(_('Criado'), auto_now_add=True, default='2000-12-31 00:00:00')
    status = models.CharField(_(u'Situação'), max_length=2, choices=STATUS, default='0')
    payment_way = models.ManyToManyField(PaymentWay, null=False, blank=False, verbose_name='Forma de pagamento')
    price = models.DecimalField(_(u'Valor'), max_digits=6, decimal_places=2, null=False, blank=False) # from covenant
    off = models.DecimalField(_(u'Desconto'), max_digits=6, decimal_places=2, null=False, blank=False)
    total = models.DecimalField(_(u'Total'), max_digits=6, decimal_places=2, null=False, blank=False)

    # from covenant
    covenant_charge = models.PositiveIntegerField(blank=True, null=True)
    covenant_pack_size = models.PositiveIntegerField(blank=True, null=True)
    covenant_payment_way_options = models.TextField(blank=True, null=True,)# editabled=False)
    covenant_payment_way_selected = models.TextField(blank=True, null=True,)# editabled=False)

    # fk
    occurrence = models.ManyToManyField(Occurrence, null=True, blank=True) # contador pacote


    def __unicode__(self):
        return u"%s" % self.id


    def terminated_(self):
        '''
            if pack have event times like as covenant
        '''
        if self.pack_size == self.occurrence.count():
            return True
        else:
            return False


    def status_color_(self):
        if self.status == '0':
            return '<span style="background-color:red;" class="service_name_html_inline">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'
        
        if self.status == '1':
            return '<span style="background-color:green;" class="service_name_html_inline">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'

        if self.status == '2':
            return '<span style="background-color:orange;" class="service_name_html_inline">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'

        if self.status == '3':
            return '<span style="background-color:yellow;" class="service_name_html_inline">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'
