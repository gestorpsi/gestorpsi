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

from datetime import datetime
from ast import literal_eval
from django.utils.translation import ugettext_lazy as _
from django.db import models

from gestorpsi.util.uuid_field import UuidField
from gestorpsi.client.models import Client
from swingtime.models import Occurrence

CHARGE = ( 
            (1, _(u'Por evento')),
            (2, _(u'Por pacote')),
                
            (u'Por período', 
                (
                    (10,u'Semanal'),
                    (11,u'Quinzenal'),
                    (12,u'Mensal'),
                    #(13,u'Bimestral'),
                    #(14,u'Semestral'), 
                )
             ),
)


STATUS = ( 
        ('0',_(u'Aberto')),
        ('1',_(u'Recebido')),
        ('2',_(u'Faturado')),
        ('3',_(u'Cancelado')),
)


class PaymentWay(models.Model):
    name = models.CharField(_(u"Name"), max_length=100)
    is_active = models.BooleanField(u'Disponível', default=True)
    comment = models.TextField(_('Comments'), blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name


class Receive(models.Model):
    '''
        receive
            referral covenant
            to pay, phone, internet, monthly bullet
        informations about receive, payment way, check, value, dead line and others
    '''
    id = UuidField(primary_key=True)
    name = models.CharField(_('Nome'), max_length=250, null=False, blank=False) # covenant name or billet
    created = models.DateTimeField(_('Criado'), auto_now_add=True, default='2000-12-31 00:00:00')
    status = models.CharField(_(u'Situação'), max_length=2, choices=STATUS, default='0')
    price = models.DecimalField(_(u'Valor'), max_digits=6, decimal_places=2, null=False, blank=False) # from covenant
    off = models.DecimalField(_(u'Desconto'), max_digits=6, decimal_places=2, null=False, blank=False)
    total = models.DecimalField(_(u'Total'), max_digits=6, decimal_places=2, null=False, blank=False)

    # from covenant
    '''
        covenant can be changed, price, name and others. 
        To store fields of covenant to compare when financial report filter are used.
    '''
    covenant_id = models.CharField(max_length=36, blank=False, null=False)
    covenant_charge = models.PositiveIntegerField(blank=False, null=False, choices=CHARGE)
    covenant_pack_size = models.PositiveIntegerField(blank=True, null=True)
    covenant_payment_way_options = models.TextField(blank=False, null=False)
    covenant_payment_way_selected = models.TextField(blank=False, null=False)
    # fk
    occurrence = models.ManyToManyField(Occurrence, null=True, blank=True, editable=False) # por evento, inscrição e evento.
    referral = models.ForeignKey("referral.Referral", null=True, blank=True, editable=False) # por periodo, apenas inscrição.


    def __unicode__(self):
        return u"%s" % self.id


    def terminated_(self):
        '''
            if pack have event times like as covenant
        '''
        if self.covenant_pack_size == self.occurrence.count():
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
            return '<span style="background-color:blue;" class="service_name_html_inline">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'


    def get_display_payment_way_name_(self):
        '''
            covenant_payment_way_select store id from PaymentWay object
            get obj and return string name
        '''
        r = []
        try: # maybe empty
            for x in literal_eval(self.covenant_payment_way_selected):
                r.append(PaymentWay.objects.get(pk=x).name)
        except:
            pass

        return r


    def save(self, *args, **kwargs):
        self.created = datetime.now()
        # real save
        super(Receive, self).save(*args, **kwargs)

    
    def get_is_conclude_(self):
        '''
            is package or event? 
            both have occurrence
            conclude if all occurrences are past
            return True or False, conclude or not.
        '''
        if self.covenant_charge == 1 or self.covenant_charge == 2 : # package(2) or event(1)
            if self.occurrence.filter( start_time__gte=datetime.today() ):
                return False
            else:
                return True

        '''
            by period do not have occurrence date, start_time.
            conclude if created(date) less than igual today
            return True or False, conclude or not.
        '''
        if self.covenant_charge == 10 or self.covenant_charge == 11 or self.covenant_charge == 12 : # week, fortnightly or monthly
            if self.created > datetime.today() :
                return False
            else:
                return True
