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

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models, connection

import reversion

from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.util.uuid_field import UuidField


class EmailType(models.Model):
    description= models.CharField(max_length=45)
    def __unicode__(self):
        return self.description
    class Meta:
        ordering = ['description']

class Email(models.Model):
    id = UuidField(primary_key= True)
    email = models.CharField(max_length=100, blank=True)
    email_type = models.ForeignKey(EmailType)
    
    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()

    def __cmp__(self, other):
        if (self.email == other.email) and \
           (self.email_type == other.email_type):
            return 0
        else:
            return 1

    def __unicode__(self):
        return self.email

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Email)

class Site(models.Model):
    id = UuidField(primary_key=True)
    description = models.CharField(max_length=100, blank=True)
    site = models.CharField(max_length=100, blank=True)

    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()

    def __cmp__(self, other):
        if (self.description == other.description) and \
           (self.site == other.site):
            return 0
        else:
            return 1    
    
    def __unicode__(self):
        return self.site

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Site)

class IMNetwork(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return self.description
    class Meta:
        ordering = ['description']

class InstantMessenger(models.Model):
    id = UuidField(primary_key=True)
    identity = models.CharField(max_length=100, blank=True)
    network = models.ForeignKey(IMNetwork, blank=True)

    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()

    def __cmp__(self, other):
        if (self.identity == other.identity) and \
           (self.network == other.network):
            return 0
        else:
            return 1

    def __unicode__(self):
        return "%s (%s)" % (self.identity, self.network)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(InstantMessenger)



class PhoneType(models.Model):
    """
    This class was created to represent phone types. Each phone type has
    a short description.
    @author: Sergio Durand
    @version: 1.0
    @see: Phone
    """
    description = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.description
    class Meta:
        ordering = ['description']

class Phone(models.Model):
    """
    This class holds information related to phone numbers.
    @author: Sergio Durand
    @version: 1.0
    @see: PhoneType
    """
    id = UuidField(primary_key=True)
    area = models.CharField(max_length=2)
    phoneNumber = models.CharField(max_length=15)
    ext = models.CharField(max_length=4, blank=True)
    phoneType = models.ForeignKey(PhoneType)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()

    def __cmp__(self, other):
        if (self.area == other.area) and \
           (self.phoneNumber == other.phoneNumber) and \
           (self.ext == other.ext) and \
           (self.phoneType == other.phoneType):
            return 0
        else:
            return 1
    
    def __unicode__(self):
        return "(%s) %s %s" % (self.area, self.phoneNumber, self.phoneType)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Phone)





def cursor_to_list(cursor, filter_type = None):
    list = []
    for item in cursor:
        if not filter_type or filter_type == item[2]:
            c = Contact()
            c.id = item[0]
            c.name = item[1]
            c.type = item[2]
            c.org_type_id = item[3]
            list.append(c)

    return list

class ContactManager(object):
    
    """
    contact filter(*args, **kwargs)
    
    Usage:
    Contact.objects.filter(
        org_id = request.user.get_profile().org_active.id, 
        person_id = request.user.get_profile().person.id, 
        filter_name = 'elvis presley',
        filter_type = 1, # where 1 = org, 2 = professional
        deactive = False # True or False
        )
    """

    def filter(self, *args, **kwargs):
         
        """ GestorPSI Organizations """
        query = \
            'SELECT o1.id, o1.name, 1 as type, 2 as org_type_id FROM organization_organization o1  LEFT OUTER JOIN ' \
            'organization_organization o2 ON (o1.organization_id = o2.id) WHERE ' \
            '(o1.active = true AND o2.id IS NULL AND o1.visible = true ' \
            'AND NOT (o1.id = %s )) AND LOWER(o1.name) LIKE LOWER(%s) AND o1.active=%s '

        """ Local Organizations """
        query += \
            'UNION SELECT o1.id, o1.name, 1 as type, 1 as org_type_id FROM organization_organization o1 ' \
            'WHERE o1.organization_id LIKE %s AND o1.contact_owner_id LIKE %s AND LOWER(o1.name) LIKE LOWER(%s) AND o1.active=%s '

        """ Local Professionals """
        query += \
            'UNION SELECT c.id, p.name, 2 as type, 1 as org_type_id FROM careprofessional_careprofessional c '\
            'INNER JOIN person_person p ON (c.person_id = p.id) INNER JOIN person_person_organization po ON (p.id = po.person_id) '\
            'INNER JOIN organization_organization o ON (po.organization_id = o.id) '\
            'WHERE o.organization_id LIKE %s AND o.contact_owner_id LIKE %s AND LOWER(p.name) LIKE LOWER(%s) AND c.active=%s '

        """ GestorPsi Professionals, excluding me """
        query += \
            'UNION SELECT careprofessional_careprofessional.id, person_person.name, 2 as type, 2 as org_type_id FROM careprofessional_careprofessional ' \
            'INNER JOIN person_person ON (careprofessional_careprofessional.person_id = person_person.id) ' \
            'LEFT OUTER JOIN person_person_organization ON (person_person.id = person_person_organization.person_id) ' \
            'LEFT OUTER JOIN organization_organization ON (person_person_organization.organization_id = organization_organization.id) ' \
            'LEFT OUTER JOIN organization_organization T5 ON (organization_organization.organization_id = T5.id) '\
            'WHERE (organization_organization.active = true AND organization_organization.visible = true  AND T5.id IS NULL ' \
            'AND NOT (careprofessional_careprofessional.person_id IN (SELECT U2.person_id FROM person_person_organization U2 ' \
            'WHERE U2.organization_id = %s ) AND careprofessional_careprofessional.person_id IS NOT NULL) '\
            'AND (LOWER(organization_organization.name) LIKE LOWER(%s) OR LOWER(person_person.name) LIKE LOWER(%s)) \
            ) AND careprofessional_careprofessional.active=%s  ORDER BY name'
        
        cursor = connection.cursor()

        cursor.execute(query, [ \
            kwargs.get('org_id') or '%', \
            kwargs.get('filter_name') or '%', \
            False if kwargs.get('deactive') else True, \
            kwargs.get('org_id') or '%', \
            kwargs.get('person_id') or '%', \
            kwargs.get('filter_name') or '%', \
            False if kwargs.get('deactive') else True, \
            kwargs.get('org_id') or '%', \
            kwargs.get('person_id') or '%', \
            kwargs.get('filter_name') or '%', \
            False if kwargs.get('deactive') else True, \
            kwargs.get('org_id') or '%', \
            kwargs.get('filter_name') or '%', \
            kwargs.get('filter_name') or '%', \
            False if kwargs.get('deactive') else True, \
            ])

        return cursor_to_list(cursor.fetchall(), kwargs.get('filter_type') or None)

    def filter_internal(self, *args, **kwargs):

        """ Local Organizations """
        query = \
            'SELECT o1.id, o1.name, 1 as type, 1 as org_type_id FROM organization_organization o1 ' \
            'WHERE o1.organization_id LIKE %s AND o1.contact_owner_id LIKE %s AND LOWER(o1.name) LIKE LOWER(%s) AND o1.active=%s '

        """ Local Professionals """
        query += \
            'UNION SELECT c.id, p.name, 2 as type, 1 as org_type_id FROM careprofessional_careprofessional c '\
            'INNER JOIN person_person p ON (c.person_id = p.id) INNER JOIN person_person_organization po ON (p.id = po.person_id) '\
            'INNER JOIN organization_organization o ON (po.organization_id = o.id) '\
            'WHERE o.organization_id LIKE %s AND o.contact_owner_id LIKE %s AND LOWER(p.name) LIKE LOWER(%s) AND c.active=%s ORDER BY name'

        cursor = connection.cursor()

        cursor.execute(query, [ \
            kwargs.get('org_id') or '%', \
            kwargs.get('person_id') or '%', \
            kwargs.get('filter_name') or '%', \
            False if kwargs.get('deactive') else True, \
            kwargs.get('org_id') or '%', \
            kwargs.get('person_id') or '%', \
            kwargs.get('filter_name') or '%', \
            False if kwargs.get('deactive') else True, \
            ])

        return cursor_to_list(cursor.fetchall(), kwargs.get('filter_type') or None)

    def filter_external(self, *args, **kwargs):
         
        """ GestorPSI Organizations """
        query = \
            'SELECT o1.id, o1.name, 1 as type, 2 as org_type_id FROM organization_organization o1  LEFT OUTER JOIN ' \
            'organization_organization o2 ON (o1.organization_id = o2.id) WHERE ' \
            '(o1.active = true AND o2.id IS NULL AND o1.visible = true ' \
            'AND NOT (o1.id = %s )) AND LOWER(o1.name) LIKE LOWER(%s) AND o1.active=%s '

        """ GestorPsi Professionals, excluding me """
        query += \
            'UNION SELECT careprofessional_careprofessional.id, person_person.name, 2 as type, 2 as org_type_id FROM careprofessional_careprofessional ' \
            'INNER JOIN person_person ON (careprofessional_careprofessional.person_id = person_person.id) ' \
            'LEFT OUTER JOIN person_person_organization ON (person_person.id = person_person_organization.person_id) ' \
            'LEFT OUTER JOIN organization_organization ON (person_person_organization.organization_id = organization_organization.id) ' \
            'LEFT OUTER JOIN organization_organization T5 ON (organization_organization.organization_id = T5.id) '\
            'WHERE (organization_organization.active = true AND organization_organization.visible = true  AND T5.id IS NULL ' \
            'AND NOT (careprofessional_careprofessional.person_id IN (SELECT U2.person_id FROM person_person_organization U2 ' \
            'WHERE U2.organization_id = %s ) AND careprofessional_careprofessional.person_id IS NOT NULL) '\
            'AND (LOWER(organization_organization.name) LIKE LOWER(%s) OR LOWER(person_person.name) LIKE LOWER(%s)) \
            ) AND careprofessional_careprofessional.active=%s  ORDER BY name'
        
        cursor = connection.cursor()

        cursor.execute(query, [ \
            kwargs.get('org_id') or '%', \
            kwargs.get('filter_name') or '%', \
            False if kwargs.get('deactive') else True, \
            kwargs.get('org_id') or '%', \
            kwargs.get('filter_name') or '%', \
            kwargs.get('filter_name') or '%', \
            False if kwargs.get('deactive') else True, \
            ])

        return cursor_to_list(cursor.fetchall(), kwargs.get('filter_type') or None)

class Contact(object):
    objects = ContactManager()
    
    class Meta:
        permissions = (
            ("contact_list", "Can list contact"),
            ("contact_write", "Can write contact"),
        )
    
    def __unicode__(self):
        return u'%s' % self.name

    def is_organization(self):
        return True if self.type == 1 else False

    def is_professional(self):
        return True if self.type == 2 else False

    def instance(self):
        if self.is_organization(): # is organization
            return Organization.objects.get(pk=self.id)
        if self.is_professional(): # is professional
            return CareProfessional.objects.get(pk=self.id)
        return None

    def _get_org_type(self):
        if self.org_type_id == 1: # is local
            return "%s" % 'LOCAL'
        if self.org_type_id == 2: # is from gestorpsi network
            return "%s" % 'GESTORPSI'
        return None

    def _get_first_phone(self):
        if self.is_organization():
            return "%s" % self.instance().get_first_phone() or None
        if self.is_professional():
            return "%s" % self.instance().person.get_first_phone() or None
        return None
    
    def _get_first_email(self):
        if self.is_organization():
            return "%s" % self.instance().get_first_email()
        if self.is_professional():
            return "%s" % self.instance().person.get_first_email()
        return None
    
    def _get_professional_profession(self):
        if(self.is_professional()):
            try:
                return self.instance().professionalIdentification.profession.type
            except:
                 return None
        else:
            return None
    
    def _get_professional_organizations(self):
        if(self.is_professional()):
            organizations = ''
            for o in self.instance().person.organization.all():
                if o.public:
                    organizations += "%s " % (o.name)
            return organizations or None
        else:
            return None

    phone = property(_get_first_phone)
    email = property(_get_first_email)
    org_type = property(_get_org_type)
    profession = property(_get_professional_profession)
    organization = property(_get_professional_organizations)
    

