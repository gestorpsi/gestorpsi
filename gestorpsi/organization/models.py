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

import re
import reversion
from datetime import datetime, date
from django.db import models
from django.db.models import Q
from django.contrib.contenttypes import generic
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext as _

from gestorpsi.phone.models import Phone
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.address.models import Address
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util.first_capitalized import first_capitalized
from gestorpsi.boleto.models import BradescoBilletData

from gestorpsi.gcm.models.plan import Plan
from gestorpsi.gcm.models.invoice import Invoice
from gestorpsi.gcm.models.payment import PaymentType

class ProfessionalResponsible(models.Model):
    """    
    This class represents the professional and Subscription of the Organization
    @author: Tiago de Souza Moraes
    @version: 1.0 
    """
    id = UuidField(primary_key=True)
    name = models.CharField(max_length=50, default="", null=True, blank=True, editable=False)
    subscription = models.CharField(max_length=50, null=True, blank=True, default="")
    organization_subscription = models.CharField(max_length=50, null=True, blank=True, default="")
    organization = models.ForeignKey('Organization', null=False, blank=False)
    profession = models.ForeignKey('careprofessional.Profession', null=True, blank=False)
    
    def __empty__(self):
        return ''
    area = property(__empty__)
    addressPrefix = property(__empty__)
    addressLine1 = property(__empty__)
    addressLine2 = property(__empty__)
    addressNumber = property(__empty__)
    neighborhood = property(__empty__)
    zipCode = property(__empty__)
    addressType = property(__empty__)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return u"%s" % self.name

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision
    
    def save(self, *args, **kwargs):
        super(ProfessionalResponsible, self).save(*args, **kwargs)
    
reversion.register(ProfessionalResponsible)

class PersonType(models.Model):
    """
    This class represents a person type for organization profile. The person type can be (physical or juridical)  
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class UnitType(models.Model):
    """
    This class represents unity type  
    @author: Fabio Martins
    @version: 1.0 
    """
    description = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class AdministrationEnvironment(models.Model):
    """
    This class represents a administration type of Organization. This administration type can be (municipal, state, federal or private)  
    @author: Fabio Martins
    @version: 1.0 
    """
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class Source(models.Model):
    """
    This class represents the organization situation
    @author: Fabio Martins
    @version: 1.0 
    """
    description = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class ProvidedType(models.Model):
    """    
    This class represents a care type provided
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

reversion.register(ProvidedType)

class Management(models.Model):
    """    
    This class represents a management type of organization 
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class Dependence(models.Model):
    """    
    This class represents a Dependence type
    @author: Fabio Martins
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class Activitie(models.Model):
    """    
    This class represents the research activities from Organization.  
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class OrganizationManager(models.Manager):
    def real(self):
        return super(OrganizationManager, self).get_query_set().filter(active=True, organization__isnull=True)


try:
    DEFAULT_PAYMENT_DAY = BradescoBilletData.objects.all()[0].default_payment_day
except:
    DEFAULT_PAYMENT_DAY = 10


TIME_SLOT_SCHEDULE = ( 
            ("30",'30'),
            ("40",'40'),
            ("45",'45'),
            ("60",'60'),
        )

class Organization(models.Model):
    """    
    This class represents the organization model.   
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    id= UuidField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # identity
    name = models.CharField(max_length=100)
    trade_name = models.CharField(max_length=100, blank=True)
    short_name = models.CharField(max_length=100, blank=True, unique=True)
    register_number = models.CharField(max_length=100, blank=True)
    cnes = models.CharField(max_length=100, blank=True)
    state_inscription = models.CharField(max_length=30, blank=True)
    city_inscription = models.CharField(max_length=30, blank=True)
    last_id_record = models.PositiveIntegerField(default=0)
            # subscriptions_professional_institutional = models.CharField(max_length=100, blank=True)
            # professional_responsible = models.CharField(max_length=100, blank=True) 
    
    # profile
    person_type = models.ForeignKey(PersonType, null=True, blank=True)
    unit_type = models.ForeignKey(UnitType, null=True, blank=True)
    environment = models.ForeignKey(AdministrationEnvironment, null=True, blank=True)
    management = models.ForeignKey(Management, null=True, blank=True)
    source = models.ForeignKey(Source, null=True, blank=True)
    dependence = models.ForeignKey(Dependence, null=True, blank=True)
    provided_type = models.ManyToManyField(ProvidedType, null=True, blank=True)
    activity = models.ForeignKey(Activitie, null=True, blank=True)
    public = models.BooleanField(default=True)
    comment = models.CharField(max_length=765, blank=True)
    active = models.BooleanField(u'Ativo. Todas as faturas pagas?', default=True)
    suspension = models.BooleanField(u'Cliente suspendeu serviço. Não gera nova fatura ou notificação.', default=False)
    suspension_reason = models.TextField(u'Motivos da suspensão', blank=True, null=True)
    visible = models.BooleanField(default=True)
    photo = models.CharField(max_length=200, blank=True)          
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True) 
    organization = models.ForeignKey('self', related_name="%(class)s_related", null=True, blank=True)
    contact_owner = models.ForeignKey('person.Person', related_name="contact_owner", null=True, blank=True, default=None)
    
    employee_number = models.IntegerField(default=1, null=True, blank=True)
    employee_number.help_text = "Number of employees (field used by the system DON'T change it)." 
    employee_number.verbose_name = "Number of employees"
    #employee_number.editable = False
    
    prefered_plan = models.ForeignKey(Plan, null=True, blank=True)
    prefered_plan.verbose_name = _("Preferred plan")
    prefered_plan.help_text= _("The plan the organization will use next time the system gives a billet.")
    
    # is old, to remove next alteration. Can be used org.invoice_() method to check
    #current_invoice = models.ForeignKey(Invoice, null=True, blank=True, related_name='current_invoice')
    #current_invoice.verbose_name = _("Current invoice")
    #current_invoice.help_text= _("Field used by the system DON'T change it.")
    #current_invoice.editable = False

    payment_type = models.ForeignKey(PaymentType, null=True, blank=True)
    payment_type.verbose_name = _("Tipo de pagamento")
    payment_detail = models.TextField(u'Detalhes do pagamento. Usado pelo ADM gestorPSI.', null=True, blank=True)
    
    default_payment_day = models.PositiveIntegerField(validators=[MaxValueValidator(28), MinValueValidator(1)], default=DEFAULT_PAYMENT_DAY)
    default_payment_day.verbose_name = _("Default payment day")
    default_payment_day.help_text= _("The default day in which the billets have to be paid at the most by this organization.")

    time_slot_schedule = models.CharField(u"Tempo de cada consulta (minutos)", null=False, blank=False, choices=TIME_SLOT_SCHEDULE, max_length=2, default=30)
    
    objects = OrganizationManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):

        # payment type default, credit card, id=1.
        if not self.id:
            self.payment_type = PaymentType.objects.get(pk=1) 

        if self.id: # save original state from register to verify if it has been changed from latest save
            original_state = Organization.objects.get(pk=self.id)
            if self.date_created is None or not self.date_created:
                try:
                    temp = reversion.models.Version.objects.get_for_object(self).order_by('revision__date_created').latest('revision__date_created').revision
                    temp = temp.date_created
                except:
                    temp = datetime.now()
                self.date_created = temp
        else:
            original_state = None
            self.date_created = datetime.now()
            if Plan.objects.filter(staff_size__gte=self.employee_number, duration=1):
                self.prefered_plan = Plan.objects.filter(staff_size__gte=self.employee_number, duration=1).order_by('staff_size')[0]
                self.payment_type = PaymentType.objects.get(pk=1) # cartao

        # suspension
        if self.suspension == True:
            self.active = False
        else:
            # read only?
            if self.invoice_()[2]: # one not payed overdue invoice
                self.active = False
            else:
                self.active = True
                self.suspension_reason = None # clean old data

        super(Organization, self).save(*args, **kwargs)
        
        if self.id and original_state:
            if original_state.active != self.active and not original_state.organization: # active state has been changed and organization is a real organization
                if not self.active: # organization has been deactivated, lets set all users as read-only mode
                    for person in self.person_set.all():
                        if hasattr(person, 'profile'): # is valid user (maybe) =)
                            for group in person.profile.user.groups.all():
                                new_group = Group.objects.get(name=('%s_ro' % group.name))
                                person.profile.user.groups.add(new_group) # add user to new group (a readonly group)
                                person.profile.user.groups.remove(Group.objects.get(name=group.name)) # remove user from past group
                else: # organization has been activated, lets set all users as NOT read-only mode
                    for person in self.person_set.all():
                        if hasattr(person, 'profile'): # is valid user (maybe) =)
                            for group in person.profile.user.groups.all():
                                new_group = Group.objects.get(name=re.sub('_ro','',group.name))
                                person.profile.user.groups.add(new_group) # add user to new group (a readonly group)
                                person.profile.user.groups.remove(Group.objects.get(name=group.name)) # remove user from past group 

    def professionalresponsible_(self):
        try:
            return ProfessionalResponsible.objects.filter(organization=self)[0]
        except:
            return None
    professionalresponsible = property(professionalresponsible_)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

    def revision_created(self):
        return reversion.get_for_object(self).order_by('revision__date_created').latest('revision__date_created').revision

    def created(self):
        return self.date_created

    def get_first_phone(self):
        if ( len( self.phones.all() ) != 0 ):
            return self.phones.all()[0]
        else:
            return ''

    def get_first_email(self):
        if ( len( self.emails.all() ) != 0 ):
            return self.emails.all()[0]
        else:
            return ''

    def get_first_address(self):
        text = ""
        if self.address.all().count():
            addr = self.address.all()[0]
            text = "%s %s, %s" % (addr.addressPrefix, addr.addressLine1, addr.addressNumber)
            
            city = first_capitalized(addr.city.name) if hasattr(addr, "city") and addr.city else ""
            state = addr.city.state.shortName if hasattr(addr, "city") and hasattr(addr.city, "state") and addr.city.state else ""
            country = addr.city.state.country.name if hasattr(addr, "city") and hasattr(addr.city, "state") and hasattr(addr.city.state, "country") and addr.city.state.country  else ""
            
            if len(addr.addressLine2): text += " - %s" % addr.addressLine2
            if len(addr.neighborhood): text += " - %s" % addr.neighborhood
            text += "<br />%s - %s - %s" % (city, state, country)
            if len(addr.zipCode): text += " - CEP: %s" % addr.zipCode
        return text

    def clients(self):
        return self.person_set.filter(client__isnull = False, client__active = True)

    def care_professionals(self):
        return self.person_set.filter(careprofessional__isnull = False, careprofessional__active = True)

    def employees(self):
        return self.person_set.filter(employee__isnull = False, employee__active = True)

    def is_real(self):
        return True if not self.organization else False

    def is_local(self):
        return True if self.organization else False

    def administrators_(self):
        return self.person_set.filter(Q(profile__user__groups__name='administrator') | Q(profile__user__groups__name='administrator_ro')).order_by('profile__user__date_joined').distinct()

    def secretary_(self):
        return self.person_set.filter(profile__user__groups__name='secretary').order_by('profile__user__date_joined')

    def services(self):
        return self.service_set.filter(active=True)



    '''
        return number of rooms from org
    '''
    def room_count_(self):
        c = 0 
        for x in self.place_set.all():
            c += x.room_set.all().count()
        return c
    

    '''
        retorna todas as faturas
        array
            0 = proxima
            1 = corrente/atual
            2 = vencida

        filter pago ou não no html
    '''
    def invoice_(self):

        r = [False]*4

        # future
        r[0] = self.invoice_set.filter( start_date__gt=date.today() )

        # current 
        r[1] = self.invoice_set.filter( start_date__lte=date.today(), end_date__gte=date.today() )

        # past
        # 1t all overdue invoices
        r[2] = []
        for x in self.invoice_set.filter( start_date__lt=date.today(), end_date__lt=date.today(), status=0 ).order_by('-date'):
            r[2].append(x)

        # copy r2
        import copy
        r[3] = copy.deepcopy(r[2])
        for x in self.invoice_set.filter( start_date__lt=date.today(), end_date__lt=date.today, status__gt=0).order_by('-date'):
            r[3].append(x)

        return r


    class Meta:
        ordering = ['name']
        permissions = (
            ("organization_add", "Can add organizations"),
            ("organization_change", "Can change organizations"),
            ("organization_list", "Can list organizations"),
            ("organization_write", "Can write organizations"),
        )

reversion.register(Organization, follow=['provided_type', 'phones', 'address', 'emails', 'sites', 'instantMessengers'])

class AgreementType(models.Model):
    """
    This class represents an agreement type.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    description= models.CharField( max_length= 80 )
    def __unicode__(self):
        return u'%s' % self.description
    class Meta:
        ordering = ['description']

class Agreement(models.Model):
    """
    This class represents an agreement type that the careprofessional works
    @author: Danilo S. Sanches
    @version: 1.0
    """
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class AgeGroup(models.Model):
    """
    This class was created to represent an interval of ages as follows: for instance,
    if some client is 6 years old and there is a instance of AgeGroup which represents and labels the
    interval between 0 and 8 as 'child', then such client will be classified as child since his/her age is contained
    in the bounded interval [0-8]*.
    *The interval [0-8] includes every number between 0 and 8 as well as 0 and 8.
    """
    minimum_age_endpoint= models.PositiveIntegerField()
    maximum_age_endpoint= models.PositiveIntegerField()
    label= models.CharField( max_length= 30, null= False )
    
    def __unicode__(self):
        return u"%s (%i-%i)" % ( self.label, self.minimum_age_endpoint, self.maximum_age_endpoint )
    class Meta:
        ordering = ['minimum_age_endpoint']    

class EducationLevel(models.Model):
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.description
    
    class Meta:
        ordering = ['id']

class HierarchicalLevel(models.Model):
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.description

    class Meta:
        ordering = ['id']

class ProcedureProvider(models.Model):
    """
    This class was created to represent entities which provide some kind of health care service.
    """
    name= models.CharField( max_length= 20 )
    def __unicode__(self):
        return u"name: %s" % self.name
    class Meta:
        ordering = ['name']

class Procedure(models.Model):
    """
    This class represents procedures provided by entities like the Sistema Único de Saúde (SUS).
    """
    procedure_code= models.CharField( max_length= 20, null= True )
    description= models.CharField( max_length= 255, null= False )
    procedure= models.ForeignKey( ProcedureProvider )

    def __unicode__(self):
        return u"code: %s, description: %s" % (self.procedure_code, self.description)
    class Meta:
        ordering = ['description']

