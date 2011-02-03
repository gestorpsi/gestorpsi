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

"""
@Autor: Fabio A. Martins
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.core.urlresolvers import reverse
from gestorpsi.util.views import get_object_or_None
from gestorpsi.admission.models import AdmissionReferral, ReferralChoice as AdmissionIndication
from gestorpsi.client.models import Client
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.organization.models import Organization
from gestorpsi.service.models import Service
from gestorpsi.referral.models import Referral, Indication as ReferralIndication, IndicationChoice as ReferralIndicationChoice, ReferralDischargeReason
from gestorpsi.util.views import percentage
from gestorpsi.settings import REFERRAL_DISCHARGE_REASON_CANCELED


VIEWS_CHOICES = (
    (1, _('Admisssions')),
    (2, _('Referrals')),
    #(3, _('Schedules')),
)

class Report(models.Model):
    def set_date(self, organization, date_start=None, date_end=None):
        if not date_start or not date_end:
            date_start = datetime.now()-relativedelta(months=1)
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

    def get_referral_range(self, organization, date_start, date_end):
        """
        get referral 'universe'
        all referrals that could be find in range
        """
        date_start,date_end = self.set_date(organization, date_start, date_end)
        range = Referral.objects_inrange.all(organization, date_start, date_end)
        
        if range:
            data = ReportReferral.objects.all(range, organization)
            
            return data,date_start,date_end
        
        return [], None, None

    #def get_schedule_range(self, organization, date_start, date_end):
        #"""
        #get schedule 'universe'
        #all schedules that could be find in range
        #"""
        #date_start,date_end = self.set_date(organization, date_start, date_end)
        #range = ScheduleOccurrence.objects_inrange.all(organization, date_start, date_end)
        
        #if range:
            #data = ReportReferral.objects.all(range, organization)
            
            #return data,date_start,date_end
        
        #return None, None, None

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
                if a.created >= start_tmp and a.created < next_month:
                    pks.append(a.id)
            dots.append((start_tmp.strftime("%m/%Y"), range.filter(pk__in=pks).count())) # coordinates here: x, y
        
            start_tmp = start_tmp+relativedelta(months=+1)
        return dots

class ReportsSavedManager(models.Manager):
    def from_user(self, user, organization):
        return super(ReportsSavedManager, self).get_query_set().filter(user=user, organization=organization, trash=False)

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
    def chart(self, range, date_start = None, date_end = None, lines=True, bars=False, points=False):

        """
        return coordinates to plot graph
        note: graph_type here can be: lines, bars or points
        and can be mixed like this: {'lines':'true', 'points':'true'}
        """

        graphs = []
        if not lines and not bars and not points: # the default graph type
            lines = 'true'

        graph_types = {
            'lines':'false' if not lines or 'true' not in lines else 'true',
            'bars':'false' if not bars or 'true' not in bars else 'true',
            'points':'false' if not points or 'true' not in points else 'true',
        }
        
        graphs.append({'title':_('All admissions'), 'data': Report().chart_coordinates(range, date_start, date_end), 'type': graph_types})
        graphs.append({'title':_('Individuals'), 'data': Report().chart_coordinates(range.filter(client__person__company__isnull=True), date_start, date_end), 'type': graph_types, })
        graphs.append({'title':_('Companies'), 'data': Report().chart_coordinates(range.filter(client__person__company__isnull=False), date_start, date_end), 'type': graph_types })

        return simplejson.dumps(graphs, sort_keys=True)

    def overview(self, range):

        """
        return a list with admission overview data splited
        in individuals and companies clients type
        """

        data = []
        total = len(range)
        individuals = range.filter(client__person__company__isnull=True).count()
        companies = range.filter(client__person__company__isnull=False).count()
        
        data.append({'name': _('Individuals'), 'total': individuals, 'percentage': percentage(individuals, total), 'url':reverse('admission_client_overview_individuals'), })
        data.append({'name': _('Companies'), 'total': companies, 'percentage': percentage(companies, total), 'url':reverse('admission_client_overview_companies'), })
        data.append({'name': _('Total'), 'total': total, 'percentage': '', 'url':reverse('admission_client_overview_total'), })
        
        return data

    def signed(self, range):
    
        """
        return a list with relation between client that have 'signed by client'
        and clients that have not signed it
        """

        data = []
        total = len(range)
        signed = range.filter(signed_bythe_client=True).count()
        not_signed = range.filter(signed_bythe_client=False).count()
        
        data.append({'name': _('Signed'), 'total': signed, 'percentage': percentage(signed, total), 'url':reverse('admission_client_signed_signed'), })
        data.append({'name': _('Not Signed'), 'total': not_signed, 'percentage': percentage(not_signed, total), 'url':reverse('admission_client_signed_notsigned'), })
        
        return data

    def knowledge(self, range):

        """
        return a list of clients x knowledge marked in admission form
        list sorted by ranking
        """

        qknowledge = AdmissionIndication.objects.filter(id__gt = 0)
        data = []

        tosort = []
        for i in qknowledge: # order reverse
            tosort.append((i.pk, range.filter(referral_choice=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            i = AdmissionIndication.objects.get(pk=id)
            count = range.filter(referral_choice=i).count()
            data.append({'name': i.description, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('admission_client_knowledge', args=[i.pk]), })

        return data

    def all(self, range):
        """
        return a list with all table data above
        """
        data = []
        
        data.append({'title': _('Admission Overview'), 'data': ReportAdmission.objects.overview(range)})
        data.append({'title': _('Admission Signed'), 'data': ReportAdmission.objects.signed(range)})
        data.append({'title': _('Admission Knowledge'), 'data': ReportAdmission.objects.knowledge(range)})

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
            obj = get_object_or_None(AdmissionIndication, pk=filter)
            verbose_name = _('Admission report - Knowledge - %s' % (obj.description))
        json = []

        if query:
            return verbose_name,Client.objects.from_user(user, None, [i.client.id for i in query]), Client.objects.from_organization(user.get_profile().org_active, query)
        
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
        for i in AdmissionIndication.objects.all():
            clients_reports.append(self.clients(user, date_start, date_end, 'knowledge', i.id))
        
        return clients_reports

class ReportReferralManager(models.Manager):
    def chart(self, range, date_start = None, date_end = None, lines=True, bars=False, points=False):

        """
        return coordinates to plot graph
        note: graph_type here can be: lines, bars or points
        and can be mixed like this: {'lines':'true', 'points':'true'}
        """

        graphs = []
        if not lines and not bars and not points: # the default graph type
            lines = 'true'

        graph_types = {
            'lines':'false' if not lines or 'true' not in lines else 'true',
            'bars':'false' if not bars or 'true' not in bars else 'true',
            'points':'false' if not points or 'true' not in points else 'true',
        }
        
        graphs.append({'title':_('Charged'), 'data': Report().chart_coordinates(range.filter(referraldischarge__isnull=True), date_start, date_end), 'type': graph_types, })
        graphs.append({'title':_('Discharged'), 'data': Report().chart_coordinates(range.filter(referraldischarge__isnull=False), date_start, date_end), 'type': graph_types })
        graphs.append({'title':_('Discharged Discussed'), 'data': Report().chart_coordinates(range.filter(referraldischarge__isnull=False, referraldischarge__was_discussed_with_client=True), date_start, date_end), 'type': graph_types })
        graphs.append({'title':_('Internals'), 'data': Report().chart_coordinates(range.filter(referral__isnull=False), date_start, date_end), 'type': graph_types })
        graphs.append({'title':_('Externals'), 'data': Report().chart_coordinates(range.filter(referralexternal__isnull=False), date_start, date_end), 'type': graph_types })
        

        return simplejson.dumps(graphs, sort_keys=True)

    def overview(self, range):

        """
        return a list with admission overview data splited
        in individuals and companies clients type
        """

        data = []

        total = len(range)

        charged = range.filter(referraldischarge__isnull=True).count()
        discharged = range.filter(referraldischarge__isnull=False).count()
        discharged_discussed_with_client = range.filter(referraldischarge__isnull=False, referraldischarge__was_discussed_with_client=True).count()
        referral_internal = range.filter(referral__isnull=False).count()
        referral_external = range.filter(referralexternal__isnull=False).count()

        data.append({'name': _('Subscriptions Charged'), 'total': charged, 'percentage': percentage(charged, total), 'url':reverse('referral_client_overview_charged'), })
        data.append({'name': _('Subscriptions Discharged'), 'total': discharged, 'percentage': percentage(discharged, total), 'url':reverse('referral_client_overview_discharged'), })
        data.append({'name': _('Subscriptions Discharged Discussed with Client'), 'total': discharged_discussed_with_client, 'percentage': percentage(discharged_discussed_with_client, discharged), 'url':reverse('referral_client_overview_discharged_discussed'), })
        data.append({'name': _('Internal Referrals'), 'total': referral_internal, 'percentage': percentage(referral_internal, total), 'url':reverse('referral_client_overview_internal'), })
        data.append({'name': _('External Referrals'), 'total': referral_external, 'percentage': percentage(referral_external, total), 'url':reverse('referral_client_overview_external'), })
        
        return data

    def knowledge(self, range):
        
        """
        return a list of clients x knowledge marked in admission form
        list sorted by ranking
        """

        qknowledge = ReferralIndicationChoice.objects.filter(id__gt = 0)
        data = []

        tosort = []
        for i in qknowledge: # order reverse
            tosort.append((i.pk, range.filter(indication__indication_choice=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(indication__indication_choice=id).count()
            data.append({'name': ReferralIndicationChoice.objects.get(pk=id).description, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_knowledge', args=[id]), })
        
        return data

    def services(self, range, organization):

        services = organization.service_set.all()
        data = []

        tosort = []
        for i in services: # order reverse
            tosort.append((i.pk, range.filter(service=i).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(service__pk=id).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()
            
            if count:
                data.append({'name': services.get(pk=id), 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_services', args=[id]), })
        
        return data

    def referral_internal(self, range, organization, from_service=None):

        services = organization.service_set.all()
        data = []

        tosort = []
        for i in services: # order reverse
            if not from_service:
                tosort.append((i.pk, range.filter(service=i, referral__isnull=False).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()))
            else:
                tosort.append((i.pk, range.filter(referral__service=i, referral__isnull=False).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            if not from_service:
                count = range.filter(service__pk=id, referral__isnull=False).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()
            else:
                count = range.filter(referral__service__pk=id, referral__isnull=False).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()
            
            if count:
                url = 'referral_client_internal' if not from_service else 'referral_client_internal_from'
                data.append({'name': services.get(pk=id), 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse(url, args=[id]), })
        
        return data

    def referral_external(self, range, organization):

        services = organization.service_set.all()
        data = []

        tosort = []
        for i in services: # order reverse
            tosort.append((i.pk, range.filter(service=i, referralexternal__isnull=False).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(service__pk=id, referralexternal__isnull=False).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()
            
            if count:
                data.append({'name': services.get(pk=id), 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_external', args=[id]), })
        
        return data

    def service_discharges(self, range, organization, discussed_with_client=None):

        services = organization.service_set.all()
        data = []

        tosort = []
        for i in services: # order reverse
            if not discussed_with_client:
                qs = range.filter(service=i, referraldischarge__isnull=False).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED)
            else:
                qs = range.filter(service=i, referraldischarge__isnull=False, referraldischarge__was_discussed_with_client=True).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED)
            
            tosort.append((i.pk, qs.count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            if not discussed_with_client:
                count = range.filter(service__pk=id, referraldischarge__isnull=False).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()
            else:
                count = range.filter(service__pk=id, referraldischarge__isnull=False, referraldischarge__was_discussed_with_client=True).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()
            
            if count:
                url = 'referral_client_discharge' if not discussed_with_client else 'referral_client_discharge_discussed'
                data.append({'name': services.get(pk=id), 'total': count, 'percentage': percentage(count, range.filter(referraldischarge__isnull=False).count()), 'url':reverse(url, args=[id]), })
        
        return data

    def service_discharge_reason(self, range):
        
        """
        return a list of reason discharges with a total of occurrences
        """

        qknowledge = ReferralDischargeReason.objects.filter(id__gt = 0)
        data = []

        tosort = []
        for i in qknowledge: # order reverse
            tosort.append((i.pk, range.filter(referraldischarge__reason=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(referraldischarge__reason=id).count()
            if count:
                data.append({'name': ReferralDischargeReason.objects.get(pk=id).name, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_discharge_reason', args=[id]), })
        
        return data

    def professionals(self, range, organization, from_professional=None):

        list = CareProfessional.objects.from_organization(organization)
        data = []

        tosort = []
        for i in list: # order reverse
            tosort.append((i.pk, range.filter(professional=i).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(professional=id).exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED).count()
            
            if count:
                data.append({'name': list.get(pk=id), 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_professional', args=[id]), })
        
        return data

    def all(self, range, organization=None):
        """
        return a list with all table data above
        """
        data = []
        
        data.append({'title': _('Subscriptions Overview'), 'data': ReportReferral.objects.overview(range)})
        data.append({'title': _('Subscriptions Indications'), 'data': ReportReferral.objects.knowledge(range)})
        data.append({'title': _('Service Subscriptions'), 'data': ReportReferral.objects.services(range, organization)})
        data.append({'title': _('Internal Referrals to Services'), 'data': ReportReferral.objects.referral_internal(range, organization)})
        data.append({'title': _('Internal Referrals from Services'), 'data': ReportReferral.objects.referral_internal(range, organization, True)})
        data.append({'title': _('Externals Referrals from Services'), 'data': ReportReferral.objects.referral_external(range, organization)})
        data.append({'title': _('Discharges from Services'), 'data': ReportReferral.objects.service_discharges(range, organization)})
        data.append({'title': _('Discharges Reason'), 'data': ReportReferral.objects.service_discharge_reason(range)})
        data.append({'title': _('Discharges Discussed with Client'), 'data': ReportReferral.objects.service_discharges(range, organization, True)})
        data.append({'title': _('Professional Subscriptions'), 'data': ReportReferral.objects.professionals(range, organization)})

        return data

    def clients(self,  user,  date_start, date_end, view, filter):
        """
        return a list of clients from selected report and selected range
        """
        
        """ admissions range """
        organization = user.get_profile().org_active
        query = Referral.objects_inrange.all(organization, date_start, date_end)
        service_pks = [s.pk for s in organization.service_set.all()]
        professional_pks = [p.pk for p in CareProfessional.objects.from_organization(organization)]

        if view == 'overview':

            if filter == 'total':
                verbose_name = _('Referral Total')

            if filter == 'charged':
                query = query.filter(referraldischarge__isnull=True)
                verbose_name = _('Referral Charged')

            if filter == 'discharged':
                query = query.filter(referraldischarge__isnull=False)
                verbose_name = _('Referral Discharged')
            
            if filter == 'discharged':
                query = query.filter(referraldischarge__isnull=False)
                verbose_name = _('Referral Discharged')

            if filter == 'discharged_discussed':
                query = query.filter(referraldischarge__isnull=False, referraldischarge__was_discussed_with_client=True)
                verbose_name = _('Referral Discharged Discussed')

            if filter == 'internal':
                query = query.filter(referral__isnull=False)
                verbose_name = _('Referral Internals')

            if filter == 'external':
                query = query.filter(referralexternal__isnull=False)
                verbose_name = _('Referral Externals')
            
        if view == 'knowledge':
            query = query.filter(indication__indication_choice=filter)
            obj = get_object_or_None(ReferralIndicationChoice, pk=filter)
            verbose_name = _('Referral Knowledge - %s' % (obj.description))
            
        if view == 'services':
            query = query.filter(service=filter, service__pk__in=service_pks)
            obj = get_object_or_None(Service, pk=filter, pk__in=service_pks )
            verbose_name = _(u'Referral Service - %s' % (obj))
            
        if view == 'internal':
            query = query.filter(service=filter, referral__isnull=False, service__pk__in=service_pks)
            obj = get_object_or_None(Service, pk=filter, pk__in=service_pks )
            verbose_name = _(u'Referral Internal to Service %s' % (obj))
            
        if view == 'internal_from':
            query = query.filter(referral__service=filter, referral__isnull=False, service__pk__in=service_pks)
            obj = get_object_or_None(Service, pk=filter, pk__in=service_pks )
            verbose_name = _(u'Referral Internal from Service %s' % (obj))
            
        if view == 'external':
            query = query.filter(service=filter, referralexternal__isnull=False, service__pk__in=service_pks)
            obj = get_object_or_None(Service, pk=filter, pk__in=service_pks )
            verbose_name = _(u'Referral External from Service %s' % (obj))
        
        if view == 'discharge':
            query = query.filter(service=filter, referraldischarge__isnull=False, service__pk__in=service_pks)
            obj = get_object_or_None(Service, pk=filter, pk__in=service_pks )
            verbose_name = _(u'Discharges from Service %s' % (obj))
        
        if view == 'discharge_reason':
            query = query.filter(referraldischarge__isnull=False, referraldischarge__reason=filter)
            obj = get_object_or_None(ReferralDischargeReason, pk=filter)
            verbose_name = _(u'Discharged by reason %s' % (obj))
        
        if view == 'discharge_discussed':
            query = query.filter(service=filter, referraldischarge__isnull=False, referraldischarge__was_discussed_with_client=True, service__pk__in=service_pks)
            obj = get_object_or_None(Service, pk=filter, pk__in=service_pks )
            verbose_name = _(u'Discharges discussed from Service %s' % (obj))

        if view == 'professional':
            query = query.filter(professional=filter, professional__pk__in=professional_pks)
            obj = get_object_or_None(CareProfessional, pk=filter, pk__in=professional_pks )
            verbose_name = _(u'Subscriptions to professional %s' % (obj))

        if query:
            pk_in = []
            for i in query:
                for c in i.client.all():
                    if c.id not in pk_in:
                        pk_in.append(c.id)

            return verbose_name,Client.objects.from_user(user, None, pk_in), Client.objects.from_organization(user.get_profile().org_active, query)
        
        return verbose_name,[], []

    def clients_all(self, user, date_start, date_end):
        """
        return a list of clients from ALL reports
        used to list clients when exporting data
        """

        organization = user.get_profile().org_active
        services = organization.service_set.all()
        professionals = CareProfessional.objects.from_organization(organization)

        clients_reports = []
        date_start,date_end = Report().set_date(user, date_start, date_end)
        clients_reports.append(self.clients(user, date_start, date_end, 'overview', 'charged'))
        clients_reports.append(self.clients(user, date_start, date_end, 'overview', 'discharged'))
        clients_reports.append(self.clients(user, date_start, date_end, 'overview', 'discharged_discussed'))
        clients_reports.append(self.clients(user, date_start, date_end, 'overview', 'internal'))
        clients_reports.append(self.clients(user, date_start, date_end, 'overview', 'external'))
        for i in ReferralIndicationChoice.objects.all():
            clients_reports.append(self.clients(user, date_start, date_end, 'knowledge', i.id))
        
        for i in services:
            clients_reports.append(self.clients(user, date_start, date_end, 'services', i.id))
        
        for i in services:
            clients_reports.append(self.clients(user, date_start, date_end, 'internal', i.id))
        
        for i in services:
            clients_reports.append(self.clients(user, date_start, date_end, 'internal_from', i.id))
        
        for i in services:
            clients_reports.append(self.clients(user, date_start, date_end, 'external', i.id))
        
        for i in services:
            clients_reports.append(self.clients(user, date_start, date_end, 'discharge', i.id))

        for i in services:
            clients_reports.append(self.clients(user, date_start, date_end, 'discharge_discussed', i.id))

        for i in professionals:
            clients_reports.append(self.clients(user, date_start, date_end, 'professional', i.id))
        
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
    

class ReportReferral(object):
    class Meta:
        abstract = True

    objects = ReportReferralManager()


#>>> for m in MaritalStatus.objects.all():
#...  print m, Client.objects.filter(person__maritalStatus=m).count()
#... 
#Casado(a) 0
#Divorciado(a) 0
#Separado(a) Judicial 2
#Solteiro(a) 2
#União Estável 1
#Viúvo(a) 0
