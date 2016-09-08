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

from gestorpsi.gcm.models.payment import PaymentType
from gestorpsi.gcm.models.plan import Plan


INVOICE_STATUS_CHOICES = (
    (0, _(u'Pendente')),
    (1, _(u'Pago pelo Cliente')),
    (2, _(u'Pago / 1 mês grátis')),
)

INVOICE_TYPES = (
    ('1', _('Inscription')),
    ('2', _('Monthly fee')),
)

PAYMENT_WAY = (
    ('1', _(u'Boleto')),
    ('2', _(u'Cartão crédito')),
)

BANK = (
    ('1', _(u'PagSeguro cartão crédito')),
    ('2', _(u'PagSeguro boleto')),
    ('99', _(u'Depósito em conta')),
)


class Invoice(models.Model):
    """
        Invoice of plan
           
        Future
            start, end, expiry date > today

        Pass
            start, end, expiry date < today

        Current
            start date < today < end date

        Not Paid
            pass and current invoice
            start, expiry date < today
    """
    type = models.CharField(max_length=2, null=False, blank=False, choices=INVOICE_TYPES, default='2')
    
    organization = models.ForeignKey('organization.Organization', verbose_name=_('Organizacao'))
    date = models.DateTimeField(_('Data'), auto_now_add=True) # data que foi gerado
    
    date_payed = models.DateField(_(u'Data do Pagamento'), null=True, blank=True)
    date_payed.help_text=_('Preencher apenas quando efetuado pagamento. Formato aaaa/mm/dd Ex: 2014-12-31')
    
    start_date = models.DateField(_(u'Início periodo'), null=False, blank=False, default='2000-01-01')
    start_date.help_text=_('Formato dd/mm/aaaa Ex: 31-12-2014')

    end_date = models.DateField(_(u'Fim Periodo'), null=False, blank=False, default='2000-01-01') # vencimento e sem acesso ao sistema
    end_date.help_text=_('Formato dd/mm/aaaa Ex: 31-12-2014')
    
    expiry_date = models.DateField(_('Pagamento/Vencimento'), null=True, blank=True)
    expiry_date.help_text = _('Formato dd/mm/aaaa  Ex: 31-12-2014 Data em que o plano vence, deve ser pago. Conta do cliente modo apenas leitura.')
    
    ammount = models.DecimalField(_('Valor'), decimal_places=2, max_digits=8, null=True, blank=True)
    ammount.help_text=_('Utilizar pontos, nao virgulas. Ex.: 39.90')
    
    discount = models.DecimalField(_('Desconto'), decimal_places=2, max_digits=8, null=True, blank=True)
    discount.help_text=_('Valor para desconto. Utilizar apenas valores decimais aqui, NAO porcentagem. Ex.: 5.90')
    
    payment_type = models.ForeignKey(PaymentType, null=False, blank=False, related_name='payment_type', verbose_name='Forma de pagamento', default='2') # from org choosen

    status = models.IntegerField(_(u'Situação'), choices=INVOICE_STATUS_CHOICES, default=0)
    plan = models.ForeignKey(Plan, verbose_name=_('Plan'), null=True, blank=True)

    bank = models.CharField(_('Que banco recebeu?'), choices=BANK, max_length=3, null=True, blank=True)
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


    # replace comma for dot
    def get_ammount_decimal_dot_(self): 
        return u"%s".replace(",",".") % self.ammount
    
    
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
            self.ammount = self.organization.prefered_plan.value
            self.plan = self.organization.prefered_plan

        # payed by client
        if self.status == 1 :
            if not self.date_payed:
                self.date_payed = date.today()
            if not self.bank :
                self.bank = 2

        # status pendente, reset fields
        if self.status == 0 :
            self.bank = None
            self.date_payed = None

        # gratis / register
        if self.status == 2:
            self.date_payed = date.today()
            self.start_date = self.date_payed
            self.end_date = self.start_date + relativedelta(months=1)
            self.expiry_date = self.start_date + relativedelta(days=7)
            self.payment_type = PaymentType.objects.get(pk=4)

        super(Invoice, self).save()

        # call method to update org
        self.organization.save()


    '''
        Is future, current or pass invoice?
        Most easy to find a invoice when manager invoices from org in admin page
    '''
    def situation_(self, *args, **kargs):

        if self.start_date > date.today():
            return u'Future'

        if self.start_date < date.today() and self.end_date < date.today():
            return u'Pass'

        if self.start_date <= date.today() and self.end_date >= date.today():
            return u'Current'
