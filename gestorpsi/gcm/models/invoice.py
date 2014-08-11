# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi
"""

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

#from gestorpsi.organization.models import Organization
from gestorpsi.gcm.models.plan import Plan

from datetime import datetime


INVOICE_STATUS_CHOICES = (
    (0, _(u'Pendente')),
    (1, _(u'Pago pelo Cliente')),
    (2, _(u'Pago / 28 dias grátis')),
)

INVOICE_TYPES = (
    ('1', _('Inscription')),
    ('2', _('Monthly fee')),
)


class Invoice(models.Model):
    type = models.CharField(max_length=2, null=False, blank=False, choices=INVOICE_TYPES, default='2')
    
    organization = models.ForeignKey('organization.Organization', verbose_name=_('Organizacao'))
    date = models.DateTimeField(_('Data'), auto_now_add=True) # data que foi gerado
    
    date_payed = models.DateField(_('Data do Pagamento'), null=True, blank=True)
    date_payed.help_text=_('Preencher apenas quando efetuado pagamento. Formato aaaa/mm/dd Ex: 2014-12-31')
    
    due_date = models.DateField(_('Data do Vencimento'), null=False, blank=False)
    due_date.help_text=_('Formato aaaa/mm/dd Ex: 2014-12-31')
    
    expiry_date = models.DateField(_('Data de Expiracao'), null=True, blank=True)
    expiry_date.help_text = _('Formato aaaa/mm/dd  Ex: 2014-12-31 Data em que o plano vence. Conta do cliente modo apenas leitura.')
    #expiry_date.widget = forms.TextInput(attrs={"format": "%d/%m/%Y",})
    
    ammount = models.DecimalField(_('Valor'), decimal_places=2, max_digits=8, null=True, blank=True)
    ammount.help_text=_('Utilizar pontos, nao virgulas. Ex.: 39.90')
    
    discount = models.DecimalField(_('Desconto'), decimal_places=2, max_digits=8, null=True, blank=True)
    discount.help_text=_('Valor para desconto. Utilizar apenas valores decimais aqui, NAO porcentagem. Ex.: 5.90')
    
    status = models.IntegerField(_('Estado'), choices=INVOICE_STATUS_CHOICES, default=1)
    plan = models.ForeignKey(Plan, verbose_name=_('Plan'), null=True, blank=True)
    billet_url = models.CharField(max_length=255, null=True, blank=True)
    
    billet_url.verbose_name = _("Billet URL")
    billet_url.help_text = _("URL of the billet to pay this invoice")

    observation = models.TextField(_(u'Observação'), null=True, blank=True)
    
    
    
    class Meta:
        app_label = 'gcm'
        ordering = ['organization', '-date', ]
    
    def __unicode__(self):
        return u'%s - %s %s' % (self.organization, self.date.strftime('%d/%m/%Y'), self.plan)
    
    def dued(self):
        return self.due_date < datetime.today()
            
    
    def save(self):

        # new
        if not self.id:
            self.date = datetime.now()

        self.ammount = self.plan.value
        super(Invoice, self).save()

    """
            if self.date is None:
            self.expire_date = (self.date + relativedelta(months = int(self.plan.duration)))

        if self.status < 3:
            if self.date_payed is None:
                self.status = 1 #emitido
            else:
                self.status = 2 #pago
            
        #raise Exception(self.status)
    """
