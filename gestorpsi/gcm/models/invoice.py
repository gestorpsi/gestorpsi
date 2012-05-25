# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
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
    date_payed = models.DateTimeField(_('Data do Pagamento'), help_text=_('Preencher apenas quando efetuado pagamento. Formato dd/mm/aaaa. Ex.: 16/12/2009'), null=True, blank=True)
    due_date = models.DateTimeField(_('Data do Vencimento'), help_text=_('Formato dd/mm/aaaa. Ex.: 16/12/2009'), null=True, blank=True)
    expiry_date = models.DateTimeField(_('Data de Expiracao'), help_text=_('Formato dd/mm/aaaa. Ex.: 16/12/2009'), null=True, blank=True)
    ammount = models.DecimalField(_('Valor'), help_text=_('Utilizar pontos, nao virgulas. Ex.: 39.90'), decimal_places=2, max_digits=8, null=True, blank=True)
    discount = models.DecimalField(_('Desconto'), help_text=_('Valor para desconto. Utilizar apenas valor decimais aqui, NAO porcentagem. Ex.: 5.90'), decimal_places=2, max_digits=8, null=True, blank=True)
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
        self.ammount = '0.00' if not self.plan else self.plan.value
        super(Invoice, self).save()
