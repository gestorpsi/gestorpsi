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


DURATION = (
    (1,  _('Mensal')),
    (3,  _('Trimestral')),
    (6,  _('Semestral')),
    (12, _('Anual')),
    (24, _('Bianual')),
)

FORM = (
    (0,  _(u'Desligado')),
    (1,  _(u'Form principal')),
    (2,  _(u'Form promoção')),
)

class Plan(models.Model):
    name = models.CharField(_('Nome do Plano'), help_text=_('Ex: de 1 a 9 profissionais'), max_length=255)
    staff_size = models.IntegerField(_('Qtade profissionais'), null=True, blank=True, help_text=_(u'No máximo de profissionais ativos'))
    student_size = models.IntegerField(_('Qtade estudantes'), null=True, blank=True, help_text=_(u'No máximo de estudantes ativos'))
    value = models.DecimalField(_('Valor em R$'), max_digits=8, decimal_places=2, help_text=_('Utilizar pontos, nao virgulas'))
    duration = models.IntegerField(_('Duracao'), choices=DURATION)
    weight = models.IntegerField(_('Peso'), max_length=4, null=True, blank=True, help_text = _('Peso para ordenacao visual no formulario de cadastro. Utilizar valores inteiros aqui'))
    gateway_code = models.TextField(u'Código do gateway', null=True, blank=True, help_text='codigo criado pelo gateway.')
    form = models.IntegerField(_('Formulario'), choices=FORM, default=1, help_text="Plano estará disponível no form escolhido ou desligado.")

    class Meta:
        app_label = 'gcm'
        ordering = ['weight',]
    
    def __unicode__(self):
        return u'%s - R$ %s / %s' % (self.name, self.value, self.get_duration_display())
