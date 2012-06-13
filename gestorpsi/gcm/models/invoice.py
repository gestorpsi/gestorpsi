# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi
"""

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from gestorpsi.organization.models import Organization
from gestorpsi.gcm.models.plan import Plan


INVOICE_STATUS_CHOICES = (
    (1, _('Emitido')),
    (2, _('Pago')),
    (3, _('Excluido')),
)

class Invoice(models.Model):
    organization = models.ForeignKey(Organization, verbose_name=_('Organizacao'))
    date = models.DateTimeField(_('Data'), auto_now_add=True)
    
    date_payed = models.DateField(_('Data do Pagamento'), null=True, blank=True)
    date_payed.help_text=_('Preencher apenas quando efetuado pagamento. Formato dd/mm/aaaa. Ex.: 16/12/2009')
    
    due_date = models.DateField(_('Data do Vencimento'), null=True, blank=True)
    due_date.help_text=_('Formato dd/mm/aaaa. Ex.: 16/12/2009')
    
    expiry_date = models.DateField(_('Data de Expiracao'), null=True, blank=True)
    expiry_date.help_text = _('Formato dd/mm/aaaa. Ex.: 16/12/2009. Data em que o plano vence (na qual o cliente deixara de ter acesso ao sistema).')
    expiry_date.widget = forms.TextInput(attrs={"format": "%d/%m/%Y",})
    
    ammount = models.DecimalField(_('Valor'), decimal_places=2, max_digits=8, null=True, blank=True)
    ammount.help_text=_('Utilizar pontos, nao virgulas. Ex.: 39.90')
    
    discount = models.DecimalField(_('Desconto'), decimal_places=2, max_digits=8, null=True, blank=True)
    discount.help_text=_('Valor para desconto. Utilizar apenas valores decimais aqui, NAO porcentagem. Ex.: 5.90')
    
    status = models.IntegerField(_('Estado'), choices=INVOICE_STATUS_CHOICES, default=1)
    plan = models.ForeignKey(Plan, verbose_name=_('Plan'), null=True, blank=True)
    billet_url = models.CharField(max_length=255, null=True, blank=True)
    
    billet_url.verbose_name = _("Billet URL")
    billet_url.help_text = _("URL of the billet to pay this invoice")
    
    class Meta:
        app_label = 'gcm'
        ordering = ['organization', '-date', ]
    
    def __unicode__(self):
        return u'%s - %s %s' % (self.organization, self.date.strftime('%d/%m/%Y'), self.plan)
    
    def save(self):
        #self.ammount = '0.00' if not self.plan else self.plan.value
        if self.plan is not None and self.plan != '':
            self.ammount = self.plan.value
            if self.date is None:
                self.date = datetime.now()
            self.expire_date = (self.date + relativedelta(months = int(self.plan.duration)))
    
        if self.date_payed is not None:
            self.status = 2
        else:
            self.status = 1
            
        super(Invoice, self).save()
            


