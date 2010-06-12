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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.core.urlresolvers import reverse
from gestorpsi.util.views import get_object_or_None
from gestorpsi.admission.models import AdmissionReferral, ReferralChoice
from gestorpsi.client.models import Client
from gestorpsi.organization.models import Organization
from gestorpsi.util.views import percentage


VIEWS_CHOICES = (
    (1, _('Admisssions')),
    #(2, _('Referrals')),
)

class Report(models.Model):
    def set_date(self, organization, date_start=None, date_end=None):
        if not date_start or not date_end:
            date_start = organization.created()
            date_end = datetime.now()
        else:
            date_start = datetime.strptime(date_start, '%d/%m/%Y')
            date_end = datetime.strptime(date_end + ' 23:59:59', '%d/%m/%Y %H:%M:%S')
        
        return date_start,date_end

        class Meta:
            abstract = True
    
    def filters(self):
        """
        return date start and date end to filters in right bar
        """

        f = []
        now = datetime.now()
        
        f.append({'name':_('This Month'), 'date_start': now-timedelta(days=now.day-1), 'date_end':(now-timedelta(days=now.day-1))+relativedelta(months=1), })
        f.append({'name':_('Last three months'), 'date_start': (now-timedelta(days=now.day-1))-relativedelta(months=3), 'date_end':now-timedelta(days=now.day) })
        f.append({'name':_('Last six months'), 'date_start': (now-timedelta(days=now.day-1))-relativedelta(months=6), 'date_end':now-timedelta(days=now.day) })
        f.append({'name':_('This year'), 'date_start': datetime.strptime('%s-01-01' % now.year,'%Y-%m-%d'), 'date_end':now, })
        
        return f

    def get_admissions_range(self, organization, date_start, date_end):
        """
        get admission universe
        all admissions that could be find in range
        """
        date_start,date_end = self.set_date(organization, date_start, date_end)
        range = AdmissionReferral.objects_inrange.all(organization, date_start, date_end)
        
        if range:
            admission = ReportAdmission.objects.all(range)
            
            return admission,date_start,date_end
        
        return None, None, None

    def chart_coordinates(self, objects_range, date_start = None, date_end = None):
        """
        return x and y coordinates in objects range
        note: object must have created() attribute
        """
        dots = []
        start_tmp = date_start
        while start_tmp < date_end:
            range = objects_range
            next_month = start_tmp+relativedelta(months=+1)
            pks = []
            for a in range:
                if a.created() >= start_tmp and a.created() < next_month:
                    pks.append(a.id)
            dots.append((start_tmp.strftime("%m/%y"), range.filter(pk__in=pks).count())) # coordinates here: x, y
        
            start_tmp = start_tmp+relativedelta(months=+1)
        return dots

class ReportsSavedManager(models.Manager):
    def admission(self, user, organization):
        return super(ReportsSavedManager, self).get_query_set().filter(user=user, organization=organization, view=1, trash=False)
    
    def referral(self, user, organization):
        return super(ReportsSavedManager, self).get_query_set().filter(user=user, organization=organization, view=2, trash=False)
    
    def trash(self, user, organization):
        return super(ReportsSavedManager, self).get_query_set().filter(user=user, organization=organization, trash=True)

class ReportsSaved(models.Model):
    user = models.ForeignKey(User, null=True)
    organization = models.ForeignKey(Organization, null=True)
    date = models.DateTimeField(auto_now_add = True)
    view = models.IntegerField(choices=VIEWS_CHOICES)
    label = models.CharField(_('Report name to save'), max_length=255)
    data = models.TextField()
    trash = models.BooleanField(default=False)

    objects = ReportsSavedManager()

    def __unicode__(self):
        return '%s' % (self.label)

class ReportAdmissionManager(models.Manager):
    def chart(self, admissions_range, date_start = None, date_end = None):

        """
        return coordinates to plot graph
        note: graph_type here can be: lines, bars or points
        and can be mixed like this: {'lines':'true', 'points':'true'}
        """

        graphs = []

        graphs.append({'title':_('All admissions'), 'data': Report().chart_coordinates(admissions_range, date_start, date_end), 'lines':'true'})
        graphs.append({'title':_('Individuals'), 'data': Report().chart_coordinates(admissions_range.filter(client__person__company__isnull=True), date_start, date_end), 'lines':'true'})
        graphs.append({'title':_('Companies'), 'data': Report().chart_coordinates(admissions_range.filter(client__person__company__isnull=False), date_start, date_end), 'lines':'true', })

        return simplejson.dumps(graphs, sort_keys=True)

    def overview(self, admissions_range):

        """
        return a list with admission overview data splited
        in individuals and companies clients type
        """

        data = []
        total = len(admissions_range)
        individuals = admissions_range.filter(client__person__company__isnull=True).count()
        companies = admissions_range.filter(client__person__company__isnull=False).count()
        
        data.append({'name': _('Individuals'), 'total': individuals, 'percentage': percentage(individuals, total), 'url':reverse('admission_client_overview_individuals'), })
        data.append({'name': _('Companies'), 'total': companies, 'percentage': percentage(companies, total), 'url':reverse('admission_client_overview_companies'), })
        data.append({'name': _('Total'), 'total': total, 'percentage': '', 'url':reverse('admission_client_overview_total'), })
        
        return data

    def signed(self, admissions_range):
    
        """
        return a list with relation between client that have 'signed by client'
        and clients that have not signed it
        """

        data = []
        total = len(admissions_range)
        signed = admissions_range.filter(signed_bythe_client=True).count()
        not_signed = admissions_range.filter(signed_bythe_client=False).count()
        
        data.append({'name': _('Signed'), 'total': signed, 'percentage': percentage(signed, total), 'url':reverse('admission_client_signed_signed'), })
        data.append({'name': _('Not Signed'), 'total': not_signed, 'percentage': percentage(not_signed, total), 'url':reverse('admission_client_signed_notsigned'), })
        
        return data

    def knowledge(self, admissions_range):

        """
        return a list of clients x knowledge marked in admission form
        list sorted by ranking
        """

        qknowledge = ReferralChoice.objects.filter(id__gt = 0)
        data = []

        tosort = []
        for i in qknowledge: # order reverse
            tosort.append((i.pk, admissions_range.filter(referral_choice=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            i = ReferralChoice.objects.get(pk=id)
            count = admissions_range.filter(referral_choice=i).count()
            data.append({'name': i.description, 'total': count, 'percentage': percentage(count, admissions_range.count()), 'url':reverse('admission_client_knowledge', args=[i.pk]), })

        return data

    def all(self, admissions_range):
        """
        return a list with all table data above
        """
        data = []
        
        data.append({'title': _('Admission Overview'), 'data': ReportAdmission.objects.overview(admissions_range)})
        data.append({'title': _('Admission Signed'), 'data': ReportAdmission.objects.signed(admissions_range)})
        data.append({'title': _('Admission Knowledge'), 'data': ReportAdmission.objects.knowledge(admissions_range)})

        return data

    def clients(self,  user,  date_start, date_end, view, filter):
        """
        return a list of clients from selected report and selected range
        """
        
        """ admissions range """
        #date_start,date_end = Report().set_date(organization, date_start, date_end)
        query = AdmissionReferral.objects_inrange.all(user.get_profile().org_active, date_start, date_end)

        if 'overview' in view:
            if 'individuals' in filter:
                query = query.filter(client__person__company__isnull=True)
                verbose_name = _('Admission report - Individuals')

            if 'companies' in filter:
                query = query.filter(client__person__company__isnull=False)
                verbose_name = _('Admission report - Companies')
            
            if 'total' in filter:
                verbose_name = _('Admission report - Total')

        if 'signed' in view:
            if filter == 'signed':
                query = query.filter(signed_bythe_client=True)
                verbose_name = _('Admission report - Signed by client')

            if filter == 'notsigned':
                query = query.filter(signed_bythe_client=False)
                verbose_name = _('Admission report - Not signed by client')
            
        if 'knowledge' in view:
            query = query.filter(referral_choice=filter)
            obj = get_object_or_None(ReferralChoice, pk=filter)
            verbose_name = _('Admission report - Knowledge - %s' % (obj.description))
        json = []

        if query:
            return verbose_name,Client.objects.from_user(user, None, query), Client.objects.from_organization(user.get_profile().org_active, query)
        
        return verbose_name,None

    def clients_all(self, user, date_start, date_end):
        """
        return a list of clients from ALL reports
        used to list clients when exporting data
        """
        
        clients_reports = []
        date_start,date_end = Report().set_date(user, date_start, date_end)
        clients_reports.append(self.clients(user, date_start, date_end, 'overview', 'individuals'))
        clients_reports.append(self.clients(user, date_start, date_end, 'overview', 'companies'))
        clients_reports.append(self.clients(user, date_start, date_end, 'signed', 'signed'))
        clients_reports.append(self.clients(user, date_start, date_end, 'signed', 'notsigned'))
        for i in ReferralChoice.objects.all():
            clients_reports.append(self.clients(user, date_start, date_end, 'knowledge', i.id))
        
        return clients_reports

class ReportDemographicManager(models.Manager):
    def gender(self, organization, client_pk_in=None):
        data = []

        male = Client.objects.GenderMale(organization, client_pk_in).count()
        female = Client.objects.GenderFemale(organization, client_pk_in).count()
        unknown = Client.objects.GenderUnknown(organization, client_pk_in).count()
        total = len(client_pk_in)

        data.append({'name': _('Male'), 'total': male, 'percentage': percentage(male, total)})
        data.append({'name': _('Female'), 'total': female, 'percentage': percentage(male, total)})
        data.append({'name': _('Unknown'), 'total': unknown, 'percentage': percentage(unknown, total)})

        return data
    
    def age(self, organization, client_pk_in=None):
        data = []

        children = Client.objects.AgeChildren(organization, client_pk_in).count()
        teen = Client.objects.AgeTeen(organization, client_pk_in).count()
        adult = Client.objects.AgeAdult(organization, client_pk_in).count()
        elderly = Client.objects.AgeElderly(organization, client_pk_in).count()
        unknown = Client.objects.AgeUnknown(organization, client_pk_in).count()
        total = len(client_pk_in)

        data.append({'name': _('Children'), 'total': children, 'percentage': percentage(children, total)})
        data.append({'name': _('Teen'), 'total': teen, 'percentage': percentage(teen, total)})
        data.append({'name': _('Adult'), 'total': adult, 'percentage': percentage(adult, total)})
        data.append({'name': _('Elderly'), 'total': elderly, 'percentage': percentage(elderly, total)})
        data.append({'name': _('Unknown'), 'total': unknown, 'percentage': percentage(unknown, total)})

        return data
    
    def all(self, organization, client_pk_in=None):
        """
        return a list with all table data above
        """
        data = []
        data.append({'title': _('Gender'), 'data': ReportAdmission.objects_demographic.gender(organization, client_pk_in)})
        data.append({'title': _('Age'), 'data': ReportAdmission.objects_demographic.age(organization, client_pk_in)})
        
        return data
    

class ReportAdmission(object):
    class Meta:
        abstract = True

    objects = ReportAdmissionManager()
    objects_demographic = ReportDemographicManager()


#>>> for m in MaritalStatus.objects.all():
#...  print m, Client.objects.filter(person__maritalStatus=m).count()
#... 
#Casado(a) 0
#Divorciado(a) 0
#Separado(a) Judicial 2
#Solteiro(a) 2
#União Estável 1
#Viúvo(a) 0
