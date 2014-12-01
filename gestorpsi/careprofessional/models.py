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
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from gestorpsi.person.models import Person
from gestorpsi.place.models import Place
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.organization.models import Agreement
from south.modelsinspector import add_introspection_rules

# Allows South to recognize custom field
add_introspection_rules([], ["^gestorpsi\.util\.uuid_field\.UuidField"])

class InstitutionType(models.Model):
    """
    This class represents an institution type.
    @author: Danilo S. Sanches
    @version: 1.0
    """
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description

    class Meta:
        ordering = ['description']

reversion.register(InstitutionType)

class PostGraduate(models.Model):
    """
    An instance of this class represents the postgraduate of careprofessional. This instance is relation on with careprofessional's academic resume
    @author: Danilo S. Sanches
    @version: 1.0
    """
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description

    class Meta:
        ordering = ['description']

class AcademicResume(models.Model):
    """
    This class represents careprofessional's academic resume
    @author: Danilo S. Sanches
    @version: 1.0
    """
    id= UuidField( primary_key= True )
    teachingInstitute = models.CharField(max_length=100, null=True)
    institutionType = models.OneToOneField(InstitutionType, null=True)
    course = models.CharField(max_length=100, null=True)
    initialDateGraduation = models.DateField(null=True)
    finalDateGraduation = models.DateField(null=True)
    lattesResume = models.URLField(null=True)
    postGraduate = models.ForeignKey(PostGraduate, null=True)
    initialDatePostGraduate = models.DateField(null=True)
    finalDatePostGraduate = models.DateField(null=True)
    area = models.CharField(max_length=100, null=True)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(AcademicResume)

class Profession(models.Model):
    """
    This class represents the careprofessional's profession
        and other information about the class.

    type    :   The class name of the professional(Doctor, psychologist, ...)
    number  :   Is CBO(Pt_BR) (Classificação Brasileira de Ocupações)
    symbol  :   Symbol of the class of the professional (CRM, CRP, ...)
    symbolDesc : Description of the symbol
    academic_name : Name of the profession in academic context

    @author:Tiago de Souza Moraes
    @version: 1.0
    """
    type = models.CharField(max_length=50, null=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    symbol = models.CharField(max_length=20, null=True, blank=True)
    symbol_desc = models.CharField(max_length=100, null=True)
    academic_name = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.type

    class Meta:
        ordering = ['type']

reversion.register(Profession)

class ProfessionalProfile(models.Model):
    """
    This class represents the professional profile
    @author: Danilo S. Sanches
    @version: 1.0
    """
    id= UuidField( primary_key= True )
    academicResume = models.OneToOneField(AcademicResume, null=True)
    initialProfessionalActivities = models.CharField(max_length=10, null=True)
    agreement = models.ManyToManyField(Agreement, null=True)
    profession = models.OneToOneField(Profession, null=True)
    services = models.CharField(max_length=100, null=True)
    availableTime = models.CharField(max_length=100, null=True)
    workplace = models.ManyToManyField(Place, null=True)

    def __unicode__(self):
        try:
            p  = CareProfessional.objects.get(professionalProfile=self).person.name
        except:
            p = _('[no professional related]')
        return u'%s' % p

    def __str__(self):
        try:
            p  = CareProfessional.objects.get(professionalProfile=self).person.name
        except:
            p = _('[no professional related]')
        return u'%s' % p

    def __area__(self):
        return ''
    area = property(__area__)

    def __addressPrefix__(self):
        return ''
    addressPrefix = property(__addressPrefix__)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(ProfessionalProfile)

class LicenceBoard(models.Model):
    """
    This class represents the careprofessional's licence board
    @author: Danilo S. Sanches
    @version: 1.0
    """
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.name

class ProfessionalIdentification(models.Model):
    """
    This class represents the professional identification that is composed by careprofessional's licence board and register number
    @author: Danilo S. Sanches
    @version: 1.0
    """
    id= UuidField( primary_key= True )
    profession = models.ForeignKey(Profession, null=True)
    registerNumber = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        try:
            p  = CareProfessional.objects.get(professionalIdentification=self).person.name
        except:
            p = _('[no professional related]')
        return u'%s' % p

    def __str__(self):
        try:
            p  = CareProfessional.objects.get(professionalIdentification=self).person.name
        except:
            p = _('[no professional related]')
        return '%s' % p

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

reversion.register(ProfessionalIdentification)

class StudentProfile(models.Model):
    """
    This class represents the student profile
    """
    lecture_class = models.ForeignKey(Profession, null=True, blank=True, verbose_name=_('Lecture Class'))
    period = models.CharField(_('Student Class Period'), max_length=255, null=True, blank=True)
    class_duration = models.CharField(_('Student Class Duration'), max_length=255, null=True, blank=True)
    register_number = models.CharField(_('Student Register Number'), max_length=255, null=True, blank=True)
    professional = models.OneToOneField('CareProfessional')

    def __unicode__(self):
        return u'%s' % ( self.professional )

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(StudentProfile)

class CareProfessionalManager(models.Manager):
    def active(self, organization):
        return super(CareProfessionalManager, self).get_query_set().filter(active=True, studentprofile__id__isnull=True, person__organization = organization).order_by('person__name')

    def active_all(self, organization):
        return super(CareProfessionalManager, self).get_query_set().filter(active=True, person__organization = organization).order_by('person__name')

    def deactive(self, organization):
        return super(CareProfessionalManager, self).get_query_set().filter(active=False, studentprofile__id__isnull=True, person__organization = organization).order_by('person__name')

    def students_active(self, organization):
        return super(CareProfessionalManager, self).get_query_set().filter(active=True, studentprofile__id__isnull=False, person__organization = organization).order_by('person__name')

    def students_deactive(self, organization):
        return super(CareProfessionalManager, self).get_query_set().filter(active=False, studentprofile__id__isnull=False, person__organization = organization).order_by('person__name')

    def from_organization(self, organization, query_pk_in=None):

        """
        return clients list from logged organization
        and/or with a pk range filter
        ...
        actually used in report app
        """

        query = super(CareProfessionalManager, self).get_query_set().filter(person__organization = organization)

        if query_pk_in:
            query = query.filter(pk__in=[ i.careprofessional.id for i in query_pk_in])
        query = query.order_by('person__name')

        return query

class Availability(models.Model):
    """
    This class represents all possible hours to a professional.
    @author: Jefferson Xavier
    @version: 1.0
    """

    day = models.CharField(max_length=50, null=False)
    hour = models.TimeField(null=False)

    def __unicode__(self):
        return u"%s - %s" % (self.day, self.hour)

reversion.register(Availability)

class CareProfessional(models.Model):
    """
    This class represents a careprofessional
    @author: Danilo S. Sanches
    @version: 1.0
    """
    id= UuidField( primary_key= True )
    professionalIdentification = models.OneToOneField(ProfessionalIdentification, null=True)
    professionalProfile = models.OneToOneField(ProfessionalProfile, null = True)
    person = models.OneToOneField(Person)
    comments = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    objects = CareProfessionalManager()
    availability = models.ManyToManyField(Availability)

    def __unicode__(self):
        return u"%s" % self.person

    class Meta:
        ordering = ['person']
        permissions = (
            ("careprofessional_add", "Can add careprofessionals"),
            ("careprofessional_change", "Can change careprofessionals"),
            ("careprofessional_list", "Can list careprofessionals"),
            ("careprofessional_write", "Can write careprofessionals"),
        )

    def _is_student(self):
        return False if not hasattr(self, 'studentprofile') else True

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

    def revision_created(self):
        return reversion.get_for_object(self).order_by('revision__date_created').latest('revision__date_created').revision

    def is_busy(self, start_time, end_time):
        '''
        check if professional is busy in schedule for selected range
        filter 1: start time not in occurrence range
        filter 2: end time not in occurrence range
        filter 2: end time not in occurrence range
        filter 3: occurrence range are not between asked values
        note for exclude filters:
            presence = 4 -> occurrence unmarked
            presence = 5 -> occurrence rescheduled
        '''

        from gestorpsi.schedule.models import ScheduleOccurrence
        queryset = ScheduleOccurrence.objects.filter(event__referral__professional=self) \
            .exclude(occurrenceconfirmation__presence=4).exclude(occurrenceconfirmation__presence=5)

        return True if \
            queryset.filter(start_time__lte = start_time, end_time__gt = start_time) or \
            queryset.filter(start_time__lt = end_time, end_time__gte = end_time) or \
            queryset.filter(start_time__gte = start_time, end_time__lte = end_time) \
            else False

    def _url_form(self):
        if hasattr(self, 'studentprofile'):
            return reverse('student_form', args=[self.pk])
        return reverse('professional_form', args=[self.pk])
    url_form = property(_url_form)

    is_student = property(_is_student)

    def referrals_charged(self):
        return self.referral_set.filter(referraldischarge__isnull=True)

    def have_referral_charged(self):
        if self.referrals_charged():
            return True
        return False

    def upcoming_occurrences(self):
        a = []
        for i in self.referrals_charged():
            for n in i.upcoming_occurrences():
                a.append(n)
        return a

reversion.register(CareProfessional)
