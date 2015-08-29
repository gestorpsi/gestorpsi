# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

TYPE = ( 
        ('1','Cartão crédito / Pagamento recorrente'),
        ('2','Boleto'),
        ('3','Depósito em conta'),
        ('99','Outro'),
)

TIME = ( 
        ('1', 'Mensal'),
        ('2', 'Bimestral'),
        ('3', 'Trimestral'),
        ('6', 'Semestral'),
        ('12','Anual'),
)

class PaymentType(models.Model):

    name = models.CharField(_('Tipo'), max_length=10, choices=TYPE )
    time = models.CharField(_('Tempo do plano'), max_length=10, choices=TIME, blank=False, null=False)
    active = models.BooleanField(default=True)
    show_to_client = models.BooleanField(default=True, help_text=_('Visivel para o cliente?') )
    detail = models.TextField(u'Detalhes sobre cobrança', null=True, blank=True)

    class Meta:
        app_label = 'gcm'
        ordering = ['name',]
    
    def __unicode__(self):
        return u'%s' % ( self.get_name_display() )
