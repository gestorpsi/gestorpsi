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
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.core.urlresolvers import reverse
from pygooglechart import PieChart3D
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis
from gestorpsi.util.views import get_object_or_None, color_rand
from gestorpsi.admission.models import AdmissionReferral, ReferralChoice as AdmissionIndication
from gestorpsi.client.models import Client
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.organization.models import Organization
from gestorpsi.service.models import Service
from gestorpsi.referral.models import Referral, Indication as ReferralIndication, IndicationChoice as ReferralIndicationChoice, ReferralDischargeReason
from gestorpsi.util.views import percentage

VIEWS_CHOICES = (
    (1, _('Admisssions')),
    (2, _('Referrals')),
    #(3, _('Schedules')),
)

PIE_CHART_WIDTH = 620
PIE_CHART_HEIGHT = 180

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
        
        """
        Simple helper to set/get date
        """
        
        date_start,date_end = self.set_date(organization, date_start, date_end)
        
        """
        get admission range in organization between dates
        """
        range = AdmissionReferral.objects_inrange.all(organization, date_start, date_end)
        
        if range:
            admission = ReportAdmission.objects.all(range, date_start, date_end)
            
            return admission,date_start,date_end
        
        return None, None, None

    def get_referral_range(self, organization, date_start, date_end, service):
        """
        get referral 'universe'
        all referrals that could be find in range
        """
        
        """
        Simple helper to set/get date
        """

        date_start,date_end = self.set_date(organization, date_start, date_end)
        
        """
        get referral range in organization between dates
        """
        
        range = Referral.objects_inrange.all(organization, date_start, date_end, service)
        
        if range:
            data = ReportReferral.objects.all(range, date_start, date_end, organization, service)
            
            return data,date_start,date_end, service
        
        return [], None, None, None

    def get_chart_x_axis_label(self, date_start, date_end):
        """
        return x and y coordinates in objects range
        note: object must have created() attribute
        """
        dots = []
        start_tmp = date_start

        period = date_end-date_start
        if period.days <= 45: # daily X axis
            scale = relativedelta(days=1) # monthly X axis
            strftime_format = "%d"
        else:
            scale = relativedelta(months=1) # monthly X axis
            strftime_format = "%m/%y"
        
        
        while start_tmp < date_end:
            next_period = start_tmp+scale
            dots.append(start_tmp.strftime(strftime_format)) # coordinates here: x, y
            start_tmp = start_tmp+scale
        return dots

    def chart_dots_by_period(self, objects_range, date_start = None, date_end = None, accumulated=None):
        """
        return x and y coordinates in objects range
        note: object must have created() attribute
        """
        dots = []
        start_tmp = date_start

        """
        start chart with actual count of registers
        """
        accumulated = accumulated or 0

        period = date_end-date_start
        if period.days <= 45: # daily X axis
            scale = relativedelta(days=1) # monthly X axis
            strftime_format = "%d"
        else:
            scale = relativedelta(months=1) # monthly X axis
            strftime_format = "%m/%y"
        
        
        while start_tmp < date_end:
            range = objects_range
            next_period = start_tmp+scale
            admission_in_period = range.filter(date__gte=start_tmp, date__lt=next_period).count()
            dots.append(admission_in_period + accumulated) # coordinates here: x, y
        
            start_tmp = start_tmp+scale
            accumulated = admission_in_period + accumulated
        
        if len(dots):
            return dots
        
        return []

    def get_chart(self, data, date_start, date_end, colours=None):
        # Set the vertical range from max_value plus 10
        if not data:
            return None

        max_y = max([max(l) for l in data])

        if max_y < 10:
            mult = 1
        else:
            y_scale = max_y
            mult = 1
            while y_scale/10 > 1:
                mult = mult*10
                y_scale = y_scale/10
        max_y = max_y + mult

        # Chart size of 200x125 pixels and specifying the range for the Y axis
        chart = SimpleLineChart(600, 300, y_range=[0, max_y])

        for i in data:
            chart.add_data(i)

        if not colours:
            chart.set_colours(['0000FF']) # Set the line colour to blue
        else:
            chart.set_colours(colours)

        # Set the vertical stripes
        chart.fill_linear_stripes(Chart.CHART, 0, 'F2F2F2', 0.2, 'FFFFFF', 0.2)

        # Set the horizontal dotted lines
        chart.set_grid(0, 25, 5, 5)
        
        left_axis = range(0, max_y + 1, mult)
        left_axis[0] = ''
        chart.set_axis_labels(Axis.LEFT, left_axis)

        # X axis labels
        chart.set_axis_labels(Axis.BOTTOM, \
            self.get_chart_x_axis_label(date_start, date_end))
        
        return chart.get_url()


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
    def overview(self, range, date_start, date_end, return_chart_url=False):

        """
        return a list with admission overview data splited
        in individuals and companies clients type
        """

        data = []
        total = len(range)
        individuals_range = range.filter(client__person__company__isnull=True)
        companies_range = range.filter(client__person__company__isnull=False)
        
        if return_chart_url:
            data = []
            data.append(Report().chart_dots_by_period(individuals_range, date_start, date_end))
            data.append(Report().chart_dots_by_period(companies_range, date_start, date_end))
            data.append(Report().chart_dots_by_period(range, date_start, date_end))
            
            return Report().get_chart(data, date_start, date_end, ['0000ff','ffa542', '000000'])
        
        data.append({'name': _('Individuals'), 'total': individuals_range.count(), 'percentage': percentage(individuals_range.count(), total), 'url':reverse('admission_client_overview_individuals'), 'color':'0000ff' })
        data.append({'name': _('Companies'), 'total': companies_range.count(), 'percentage': percentage(companies_range.count(), total), 'url':reverse('admission_client_overview_companies'), 'color':'ffa542'})
        data.append({'name': _('Total'), 'total': total, 'percentage': '', 'url':reverse('admission_client_overview_total'), 'color':'000000'})
        
        return data

    def signed(self, range, return_chart_url=False):
    
        """
        return a list with relation between client that have 'signed by client'
        and clients that have not signed it
        """

        data = []
        total = len(range)
        signed = range.filter(signed_bythe_client=True).count()
        not_signed = range.filter(signed_bythe_client=False).count()
        
        if return_chart_url:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart.add_data([Decimal(percentage(signed, total)), Decimal(percentage(not_signed, total))])
            chart.set_pie_labels([_('Signed'), _('Not')])
            chart.set_colours(['00ff00','ff0000']) # red, green
            return chart.get_url()
        
        data.append({'name': _('Signed'), 'total': signed, 'percentage': percentage(signed, total), 'url':reverse('admission_client_signed_signed'), 'color':'00ff00' })
        data.append({'name': _('Not Signed'), 'total': not_signed, 'percentage': percentage(not_signed, total), 'url':reverse('admission_client_signed_notsigned'), 'color': 'ff0000' })
        
        return data

    def knowledge(self, range, return_chart_url=False):

        """
        return a list of clients x knowledge marked in admission form
        list sorted by ranking
        """

        qknowledge = AdmissionIndication.objects.filter(id__gt = 0)
        data = []

        if return_chart_url:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart_add_data = []
            #chart_set_pie_labels = []
            chart_set_colours = []
            for i in qknowledge:
                count = range.filter(referral_choice=i).count()
                if count:
                    chart_add_data.append(Decimal(percentage(count, range.count())))
                    #chart_set_pie_labels.append(i.description.encode('UTF-8'))
                    chart_set_colours.append(i.color or '000000') # red, green

            chart.add_data(chart_add_data)
            #chart.set_pie_labels(chart_set_pie_labels)
            chart.set_colours(chart_set_colours)
            return chart.get_url()

        tosort = []
        for i in qknowledge: # order reverse
            tosort.append((i.pk, range.filter(referral_choice=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            i = AdmissionIndication.objects.get(pk=id)
            count = range.filter(referral_choice=i).count()
            if count > 0:
                data.append({'name': i.description, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('admission_client_knowledge', args=[i.pk]), 'color':i.color  or '000000'})

        return data

    def all(self, range, date_start, date_end):
        """
        return a list with all table data above
        """
        data = []
        
        data.append({'title': _('Admission Overview'), 'data': ReportAdmission.objects.overview(range, date_start, date_end), 'chart_url': ReportAdmission.objects.overview(range, date_start, date_end, True)})
        data.append({'title': _('Admission Signed'), 'data': ReportAdmission.objects.signed(range), 'chart_url': ReportAdmission.objects.signed(range, True)})
        data.append({'title': _('Admission Knowledge'), 'data': ReportAdmission.objects.knowledge(range), 'chart_url': ReportAdmission.objects.knowledge(range, True)})

        return data

    def clients(self,  user,  date_start, date_end, view, filter, service=None):
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
    def chart(self, range, date_start = None, date_end = None, lines=True, bars=False, points=False, service=None):

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
        
        graphs.append({
            'title':_('Charged'), 'data': Report().chart_coordinates(range, date_start, date_end),
            'type': graph_types, })

        graphs.append({
            'title':_('Discharged'), 'data': Report().chart_coordinates(range.filter(referraldischarge__isnull=False), date_start, date_end),
            'type': graph_types })
            
        graphs.append({
            'title':_('Discharged Discussed'), 'data': Report().chart_coordinates(range.filter(referraldischarge__isnull=False, referraldischarge__was_discussed_with_client=True), date_start, date_end),
            'type': graph_types })
        
        graphs.append({
            'title':_('Internals'), 'data': Report().chart_coordinates(range.filter(referral__isnull=False), date_start, date_end),
            'type': graph_types })

        graphs.append({
            'title':_('Externals'), 'data': Report().chart_coordinates(range.filter(referralexternal__isnull=False), date_start, date_end),
            'type': graph_types })
        

        return simplejson.dumps(graphs, sort_keys=True)

    def overview(self, range, date_start, date_end, return_chart_url=False):

        """
        return a list with admission overview data splited
        in individuals and companies clients type
        """

        data = []

        total = len(range)

        subscriptions = range.filter(referral__isnull=True)
        discharged_range = range.filter(referraldischarge__isnull=False)
        referral_internal_range = range.filter(referral__isnull=False)
        referral_external_range = range.filter(referralexternal__isnull=False)

        if return_chart_url:
            data = []
            data.append(Report().chart_dots_by_period(subscriptions, date_start, date_end))
            data.append(Report().chart_dots_by_period(discharged_range, date_start, date_end))
            data.append(Report().chart_dots_by_period(referral_internal_range, date_start, date_end))
            data.append(Report().chart_dots_by_period(referral_external_range, date_start, date_end))

            return Report().get_chart(data, date_start, date_end, ['000000', '0000ff', '557700', 'aa88aa' ])

        data.append({'name': _('Subscriptions'), 'total': subscriptions.count(), 'url':reverse('referral_client_overview_charged'), 'color':'000000', })
        data.append({'name': _('Subscriptions Discharged'), 'total': discharged_range.count(), 'url':reverse('referral_client_overview_discharged'), 'color':'0000ff' })
        data.append({'name': _('Internal Referrals'), 'total': referral_internal_range.count(), 'url':reverse('referral_client_overview_internal'), 'color':'557700'})
        data.append({'name': _('External Referrals'), 'total': referral_external_range.count(), 'url':reverse('referral_client_overview_external'), 'color':'aa88aa'})
        
        return data

    def discussed(self, range, return_chart_url=False):

        """
        return a list with referral discussed or not with client
        """

        data = []

        range = range.filter(referraldischarge__isnull=False)
        total = len(range)

        discharged_discussed_with_client = range.filter(referraldischarge__was_discussed_with_client=True).count()
        discharged_not_discussed_with_client = range.filter(referraldischarge__was_discussed_with_client=False).count()
        
        if return_chart_url and range:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart.add_data([Decimal(percentage(discharged_discussed_with_client, total)), Decimal(percentage(discharged_not_discussed_with_client, total))])
            chart.set_pie_labels([_('Discussed with client'), _('Not discussed with client')])
            chart.set_colours(['00ff00','ff0000']) # red, green
            return chart.get_url()

        data.append({'name': _('Discussed with client'), 'total': discharged_discussed_with_client, 'percentage': percentage(discharged_discussed_with_client, total), 'url':reverse('referral_client_overview_discharged_discussed'), 'color':'00ff00', })
        data.append({'name': _('Not discussed with client'), 'total': discharged_not_discussed_with_client, 'percentage': percentage(discharged_not_discussed_with_client, total), 'url':reverse('referral_client_overview_discharged_not_discussed'), 'color':'ff0000', })
        
        return data

    def knowledge(self, range, return_chart_url=False):
        
        """
        return a list of clients x knowledge marked in admission form
        list sorted by ranking
        """

        qknowledge = ReferralIndicationChoice.objects.filter(id__gt = 0)
        
        if return_chart_url:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart_add_data = []
            chart_set_pie_labels = []
            chart_set_colours = []
            
            for i in qknowledge:
                count = range.filter(indication__indication_choice=i.pk, referral__isnull=True).count()
                if count:
                    chart_add_data.append(Decimal(percentage(count, range.count())))
                    #chart_set_pie_labels.append(i.description.encode('UTF-8'))
                    chart_set_colours.append(i.color or '000000')
                
            chart.add_data(chart_add_data)
            #chart.set_pie_labels(chart_set_pie_labels)
            chart.set_colours(chart_set_colours)
            return chart.get_url()
        
        data = []

        tosort = []
        for i in qknowledge: # order reverse
            tosort.append((i.pk, range.filter(indication__indication_choice=i, referral__isnull=True).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(indication__indication_choice=id, referral__isnull=True).count()
            if count:
                i = ReferralIndicationChoice.objects.get(pk=id)
                data.append({'name': ReferralIndicationChoice.objects.get(pk=id).description, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_knowledge', args=[id]), 'color': i.color or '000000',})
        
        return data

    def services(self, range, organization, date_start, date_end, return_chart_url=False):

        services = organization.service_set.all()

        if return_chart_url:
            data = []
            service_colors = []
            for i in services: # order reverse
                results = range.filter(service=i, referral__isnull=True)
                if results:
                    data.append(Report().chart_dots_by_period(results, date_start, date_end))
                    service_colors.append(i.color or '000000')

            return Report().get_chart(data, date_start, date_end, service_colors)

        data = []

        tosort = []
        for i in services: # order reverse
            tosort.append((i.pk, range.filter(service=i, referral__isnull=True).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            s = services.get(pk=id)
            count = range.filter(service__pk=id, referral__isnull=True).count()
            
            if count:
                data.append({'name': u'%s' % s.name, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_services', args=[id]), 'color':s.color or '000000'})
        
        return data

    def referral_internal(self, range, organization, from_service=None, return_chart_url=False):

        services = organization.service_set.all()

        data = []

        range = range.filter(referral__isnull=False)

        if return_chart_url:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart_add_data = []
            #chart_set_pie_labels = []
            chart_set_colours = []

        tosort = []
        for i in services: # order reverse
            if not from_service:
                tosort.append((i.pk, range.filter(service=i, referral__service__isnull=False).count()))
            else:
                tosort.append((i.pk, range.filter(referral__service=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            s = services.get(pk=id)

            if not from_service:
                count = range.filter(service=id, referral__service__isnull=False).count()
            else:
                count = range.filter(referral__service=id).count()
            
            if count:
                
                if return_chart_url and count:
                    chart_add_data.append(Decimal(percentage(count, range.count())))
                    #chart_set_pie_labels.append(s.name.encode('UTF-8'))
                    chart_set_colours.append(s.color)
                else:
                    url = 'referral_client_internal' if not from_service else 'referral_client_internal_from'
                    data.append({'name': u'%s' % s.name, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse(url, args=[id]), 'color': s.color})
        
        
        if return_chart_url:
            chart.add_data(chart_add_data)
            #chart.set_pie_labels(chart_set_pie_labels)
            chart.set_colours(chart_set_colours)
            return chart.get_url()

        return data

    def referral_external(self, range, organization, return_chart_url=False):

        services = organization.service_set.all()
        data = []

        total = range.filter(referralexternal__isnull=False).count()

        if return_chart_url:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart_add_data = []
            chart_set_colours = []
            
            for i in services: # order reverse
                results = range.filter(service=i, referralexternal__isnull=False).count()
                if results:
                    chart_add_data.append(Decimal(percentage(results, total)))
                    chart_set_colours.append(i.color or '000000')
            chart.add_data(chart_add_data)
            chart.set_colours(chart_set_colours)
            return chart.get_url()

        tosort = []
        for i in services: # order reverse
            tosort.append((i.pk, range.filter(service=i, referralexternal__isnull=False).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(service__pk=id, referralexternal__isnull=False).count()
            s = Service.objects.get(pk=id)
            if count:
                data.append({'name': services.get(pk=id), 'total': total, 'percentage': percentage(count, total), 'url':reverse('referral_client_external', args=[id]), 'color':s.color})
        
        return data

    def service_discharges(self, range, organization, date_start, date_end, discussed_with_client=None, return_chart_url=False):

        services = organization.service_set.all()
        data = []

        range = range.filter(referraldischarge__isnull=False)

        if return_chart_url:
            data = []
            service_colors = []
            if discussed_with_client:
                total = range.filter(referraldischarge__was_discussed_with_client=True).count()
                # PIE CHART
                chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
                chart_add_data = []
                chart_set_colours = []
                
                for i in services: # order reverse
                    results = range.filter(service=i, referraldischarge__was_discussed_with_client=True)
                    if results:
                        chart_add_data.append(Decimal(percentage(results.count(), total)))
                        chart_set_colours.append(i.color or '000000')
                chart.add_data(chart_add_data)
                chart.set_colours(chart_set_colours)
                return chart.get_url()
            else:
                # LINE CHART
                for i in services: # order reverse
                    if not discussed_with_client:
                        results = range.filter(service=i)
                    else:
                        results = range.filter(service=i, referraldischarge__was_discussed_with_client=True)

                    if results:
                        data.append(Report().chart_dots_by_period(results, date_start, date_end))
                        service_colors.append(i.color or '000000')

                return Report().get_chart(data, date_start, date_end, service_colors)

        tosort = []
        for i in services: # order reverse
            if not discussed_with_client:
                qs = range.filter(service=i)
            else:
                qs = range.filter(service=i, referraldischarge__was_discussed_with_client=True)
            
            tosort.append((i.pk, qs.count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            s = services.get(pk=id)
            if not discussed_with_client:
                count = range.filter(service__pk=id).count()
            else:
                count = range.filter(service__pk=id, referraldischarge__was_discussed_with_client=True).count()
            
            if count:
                url = 'referral_client_discharge' if not discussed_with_client else 'referral_client_discharge_discussed'
                data.append({'name': u'%s' % s.name, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse(url, args=[id]), 'color':s.color})
        
        return data

    def service_discharge_reason(self, range, return_chart_url=False):
        
        """
        return a list of reason discharges with a total of occurrences
        """

        qknowledge = ReferralDischargeReason.objects.filter(id__gt = 0)
        range = range.filter(referraldischarge__reason__isnull=False)

        if return_chart_url:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart_add_data = []
            chart_set_pie_labels = []
            chart_set_colours = []
            
            for i in qknowledge:
                count = range.filter(referraldischarge__reason=i).count()
                if count:
                    chart_add_data.append(Decimal(percentage(count, range.count())))
                    #chart_set_pie_labels.append(i.name.encode('UTF-8'))
                    chart_set_colours.append(i.color or '000000')
                
            chart.add_data(chart_add_data)
            chart.set_pie_labels(chart_set_pie_labels)
            chart.set_colours(chart_set_colours)
            return chart.get_url()

        data = []

        tosort = []
        for i in qknowledge: # order reverse
            tosort.append((i.pk, range.filter(referraldischarge__reason=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            rdr = ReferralDischargeReason.objects.get(pk=id)
            count = range.filter(referraldischarge__reason=id).count()
            if count:
                data.append({'name': u'%s' % rdr.name, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_discharge_reason', args=[id]), 'color':rdr.color})
        
        return data

    def professionals(self, range, organization, from_professional=None):

        list = CareProfessional.objects.from_organization(organization)
        data = []

        tosort = []
        for i in list: # order reverse
            tosort.append((i.pk, range.filter(professional=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(professional=id).count()
            
            if count:
                data.append({'name': list.get(pk=id), 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_professional', args=[id]), })
        
        return data

    def all(self, range, date_start, date_end, organization=None, service=None):
        """
        return a list with all table data above
        """
        data = []

        if service:
            in_service_range = range.filter(service__pk=service)
            to_service_range = range.filter(referral__service__pk=service).exclude(service__pk=service)
            from_service_range = range.filter(service__pk=service, referral__service__isnull=False).exclude(referral__service__pk=service)
            range = in_service_range
        
        data.append({'title': _('Subscriptions Overview'), 'data': ReportReferral.objects.overview(range if not service else in_service_range, date_start, date_end), 'chart_url': ReportReferral.objects.overview(range if not service else in_service_range, date_start, date_end, True), 'without_percentage':True })

        if not service:
            data.append({'title': _('Service Subscriptions'), 'data': ReportReferral.objects.services(range, organization, date_start, date_end), 'chart_url':ReportReferral.objects.services(range, organization, date_start, date_end, True)})
            data.append({'title': _('Discharges from Services'), 'data': ReportReferral.objects.service_discharges(range, organization, date_start, date_end), 'chart_url':ReportReferral.objects.service_discharges(range, organization, date_start, date_end, None, True)})

        data.append({'title': _('Subscriptions Discharged Discussed'), 'data': ReportReferral.objects.discussed(range if not service else in_service_range), 'chart_url': ReportReferral.objects.discussed(range if not service else in_service_range, True)})
        data.append({'title': _('Subscriptions Indications'), 'data': ReportReferral.objects.knowledge(range if not service else in_service_range), 'chart_url': ReportReferral.objects.knowledge(range if not service else in_service_range, True)})

        data.append({'title': _('Internal Referrals to Services'), 'data': ReportReferral.objects.referral_internal(range if not service else to_service_range, organization), 'chart_url':ReportReferral.objects.referral_internal(range if not service else to_service_range, organization, None, True)})
        data.append({'title': _('Internal Referrals from Services'), 'data': ReportReferral.objects.referral_internal(range if not service else from_service_range, organization, True), 'chart_url':ReportReferral.objects.referral_internal(range if not service else from_service_range, organization, True, True)})

        if not service:
            data.append({'title': _('Externals Referrals from Services'), 'data': ReportReferral.objects.referral_external(range, organization), 'chart_url':ReportReferral.objects.referral_external(range, organization, True)})

        data.append({'title': _('Discharges Reason'), 'data': ReportReferral.objects.service_discharge_reason(range), 'chart_url': ReportReferral.objects.service_discharge_reason(range, True)})

        if not service:
            data.append({'title': _('Discharges Discussed with Client'), 'data': ReportReferral.objects.service_discharges(range, organization, date_start, date_end, True), 'chart_url': ReportReferral.objects.service_discharges(range, organization, date_start, date_end, True, True)})

        data.append({'title': _('Professional Subscriptions'), 'data': ReportReferral.objects.professionals(range, organization)})

        return data

    def clients(self,  user,  date_start, date_end, view, filter, service=None):
        """
        return a list of clients from selected report and selected range
        """
        
        """ admissions range """
        organization = user.get_profile().org_active
        query = Referral.objects_inrange.all(organization, date_start, date_end)
        query_full = query
        service_pks = [s.pk for s in organization.service_set.all()]
        professional_pks = [p.pk for p in CareProfessional.objects.from_organization(organization)]
        if service:
            query = query.filter(service__pk=service)

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

            if filter == 'discharged_not_discussed':
                query = query.filter(referraldischarge__isnull=False, referraldischarge__was_discussed_with_client=False)
                verbose_name = _('Referral Discharged Not Discussed')

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
            if not service:
                query = query.filter(service=filter, referral__isnull=False, service__pk__in=service_pks)
            else:
                query = query_full.filter(service=filter, referral__isnull=False, service__pk__in=service_pks)
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
