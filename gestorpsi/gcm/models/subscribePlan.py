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

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from threadlocals.threadlocals import get_current_request

#from gestorpsi.gcm.models.payment import PaymentType
from gestorpsi.gcm.models.plan import Plan


INVOICE_STATUS_CHOICES = (
    (0, _(u'Pendente')),
    (1, _(u'Pago')),
    (2, _(u'Cancelado')),
)

PAYMENT_WAY = (
    ('1', _(u'Boleto')),
    ('2', _(u'Cartão crédito')),
)

GATEWAY = (
    ('1', _(u'PagSeguro')),
    ('2', _(u'PayPal')),
    ('99', _(u'Depósito em conta')),
)


class SubscribePlan(models.Model):
    organization = models.ForeignKey('organization.Organization', verbose_name=_('Organizacao'))
    date = models.DateTimeField(_('Data'), auto_now_add=True) # data que foi gerado
    status = models.IntegerField(_(u'Situação'), choices=INVOICE_STATUS_CHOICES, default=0)
    plan = models.ForeignKey(Plan, verbose_name=_('Plano'), null=True, blank=True)
    gateway = models.CharField(_('Que gateway recebeu?'), choices=GATEWAY, max_length=3, null=True, blank=True)
    gateway_id = models.CharField(_('Referencia do gateway'), choices=GATEWAY, max_length=3, null=False, blank=False)
    payment_detail = models.TextField(_(u'Detalhes do pagamento'), null=True, blank=True)

    # read only - auditing
    aud_author = models.ForeignKey(User, null=True, blank=True, verbose_name=u'Autor')
    aud_date = models.DateTimeField(u'Cad/Alt', auto_now=True, null=False, blank=False, editable=True, default="2000-01-01")
    aud_ip = models.CharField(('IP'), max_length=15, null=True, blank=True)
    
    class Meta:
        app_label = 'gcm'
        ordering = ['organization', '-date', ]
    
    def __unicode__(self):
        return u'%s - %s %s' % (self.organization, self.date.strftime('%d/%m/%Y'), self.plan)

    def save(self, *args, **kargs):

        # get ip and user from request
        # crontab and registration don't have request
        try:
            request = get_current_request()
            self.aud_author = request.user
            self.aud_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        except:
            self.aud_author = None # crontab
            self.aud_ip = '127.0.0.1' # localhost

        # new
        if not self.id:
            self.date = datetime.now()
            #self.ammount = self.organization.prefered_plan.value
            self.plan = self.organization.prefered_plan

        ## payed by client
        #if self.status == 1 :
            #if not self.date_payed:
                #self.date_payed = date.today()
            #if not self.bank :
                #self.bank = 2

        ## status pendente, reset fields
        #if self.status == 0 :
            #self.bank = None
            #self.date_payed = None

        ## gratis / register
        #if self.status == 2:
            #self.date_payed = date.today()
            #self.start_date = self.date_payed
            #self.end_date = self.start_date + relativedelta(months=1)
            #self.expiry_date = self.start_date + relativedelta(days=7)
            #self.payment_type = PaymentType.objects.get(pk=4)

        super(SubscribePlan, self).save()

        # call method to update org
        #self.organization.save()

    #'''
        #Is future, current or pass invoice?
        #Most easy to find a invoice when manager invoices from org in admin page
    #'''
    #def situation_(self, *args, **kargs):

        #if self.start_date > date.today():
            #return u'Future'

        #if self.start_date < date.today() and self.end_date < date.today():
            #return u'Pass'

        #if self.start_date <= date.today() and self.end_date >= date.today():
            #return u'Current'
