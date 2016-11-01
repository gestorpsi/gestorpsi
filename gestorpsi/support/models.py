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

import reversion
from django.db import models
from django.utils.translation import ugettext as _
from gestorpsi.person.models import Person
from gestorpsi.util.uuid_field import UuidField

STATUS= ( 
        (1,_('Open')), 
        (2, _('Processing')),
        (3, _('Closed')),
    )

class Ticket(models.Model):
    """
    This class register tickets supports.
    @author: Fabio A Martins
    @version: 1.0
    """
    id = UuidField(primary_key=True)
    user = models.ForeignKey(Person, null=True)
    contact_name = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255)
    ticket_id = models.IntegerField(max_length=8)
    question = models.TextField()
    status = models.IntegerField(max_length=1, choices=STATUS, default=1)
    date = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return "%s %s" % (self.ticket_id, self.question)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

    def save(self, force_insert=False, force_update=False):
        self.ticket_id = len(Ticket.objects.all()) + 1
        super(Ticket, self).save(force_insert, force_update)

reversion.register(Ticket)

class TicketIteration(models.Model):
    """
    This class register tickets iterations.
    @author: Fabio A Martins
    @version: 1.0
    """
    id= UuidField(primary_key=True)
    ticket = models.ForeignKey(Ticket)
    operator = models.ForeignKey(Person, null=True, related_name='operator')
    answer = models.TextField(max_length=765, blank=True)
    date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s %s" % (self.operator, self.answer)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(TicketIteration)

class Documentation(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('Documentation', blank=True, null=True)
    
    def __unicode__(self):
        return '%s' % self.title

reversion.register(Documentation)
