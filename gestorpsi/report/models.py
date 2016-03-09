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
@Date: 01/2012
"""

from datetime import datetime, timedelta
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.db.models import Q
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
from gestorpsi.referral.models import Referral, Indication as ReferralIndication, IndicationChoice as ReferralIndicationChoice, ReferralDischargeReason, ReferralDischarge
from gestorpsi.util.views import percentage
from gestorpsi.financial.models import Receive
from gestorpsi.schedule.models import ScheduleOccurrence

VIEWS_CHOICES = (
    (1, _('Admisssions')),
    (2, _('Referrals')),
    (3, _('Faturamento')),
    (4, _('Evento')),
)

PIE_CHART_WIDTH = 620
PIE_CHART_HEIGHT = 180

class Report(models.Model):
    class Meta:
        permissions = (
            ("report_list", "Can list report"),
            ("report_write", "Can write report"),
        )

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

    def get_admissions_range(self, organization, date_start, date_end, accumulated):
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
            admission, chart_url = ReportAdmission.objects.all(range, date_start, date_end, accumulated)
            
            return admission, chart_url, date_start,date_end
        
        return None, None, None, None


    def get_event_(self, organization, date_start, date_end, professional, service, status, accumulated):

        sch_list = [] # list of objects for each presence
        '''
            array to print each presence list
            sch_list = []
            sch_list[0] = []
            sch_list[0][0] = label/line
            sch_list[0][1] = ScheduleOccurrence.objects
        '''

        data = [] # main array for google pie char array
        total_events = 0 # total of all events, show in resume
        date_start , date_end = self.set_date(organization, date_start, date_end)

        # filter by date range, all professional and all presence 
        sch_objs = ScheduleOccurrence.objects.filter(start_time__gte=date_start, start_time__lte=date_end, event__referral__organization=organization).order_by('event__referral__client')

        # professional
        if not 'all' in professional:
            sch_objs = sch_objs.filter( event__referral__professional__id=professional )

        # service
        if service:
            sch_objs = sch_objs.filter( event__referral__service__id=service )

        #
        # filter by presence confirmation
        #

        # all presence options confirmed or none marked
        if '999' in status or not status:
            status = "1,2,3,4,5,6,888" # Filter for each presence id end "not confirmed"

        if '1' in status:
            l = sch_objs.filter( occurrenceconfirmation__presence=1 ).distinct()
            sch_list.append([u'Cliente chegou no horário',l])
            total_events += l.count()

        if '2' in status:
            l = sch_objs.filter( occurrenceconfirmation__presence=2 ).distinct()
            sch_list.append([u'Cliente chegou atrasado',l])
            total_events += l.count()

        if '3' in status:
            l = sch_objs.filter( occurrenceconfirmation__presence=3 ).distinct()
            sch_list.append([u'Cliente não compareceu',l])
            total_events += l.count()

        if '4' in status:
            l = sch_objs.filter( occurrenceconfirmation__presence=4 ).distinct()
            sch_list.append([u'Evento desmarcado',l])
            total_events += l.count()

        if '5' in status:
            l = sch_objs.filter( occurrenceconfirmation__presence=5 ).distinct()
            sch_list.append([u'Evento remarcado',l])
            total_events += l.count()

        if '6' in status:
            l = sch_objs.filter( occurrenceconfirmation__presence=6 ).distinct()
            sch_list.append([u'Profissional não compareceu',l])
            total_events += l.count()

        # all not confirmed
        if '888' in status:
            l = sch_objs.filter(occurrenceconfirmation__isnull=True)
            sch_list.append([u'Não confirmado',l])
            total_events += l.count()

        # all confirmed
        if '777' in status:
            l = sch_objs.filter(occurrenceconfirmation__isnull=False)
            sch_list.append([u'Confirmado',l])
            total_events += l.count()

        #
        # graphic google chart
        #
        lines = [] # label for google graphic lines

        if '1' in status:
            lines.append(u'Cliente chegou no horário')
        if '2' in status:
            lines.append(u'Cliente chegou atrasado')
        if '3' in status:
            lines.append(u'Cliente não compareceu')
        if '4' in status:
            lines.append(u'Evento desmarcado')
        if '5' in status:
            lines.append(u'Evento remarcado')
        if '6' in status:
            lines.append(u'Profissional não compareceu')
        if '888' in status:
            lines.append(u'Não confirmado')
        if '777' in status:
            lines.append(u'Confirmado')


        def filter_range_date(presence):
            ds = date_start
            l = 0 # store last counter
            t = []

            while ds < date_end :
                l += sch_objs.filter(occurrenceconfirmation__presence=presence, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()
                t.append( l )
                ds += relativedelta(months=1)

            return t


        #
        # accumulated 
        #

        if accumulated == 'True':

                # tmp = []
                # tmp = [ [presence counter] ]
                # tmp = [ [0,10,25,50,100] , [presence1] , [presenceN] ]
                tmp = []

                if '1' in status:
                    tmp.append( filter_range_date(1) )
                if '2' in status:
                    tmp.append( filter_range_date(2) )
                if '3' in status:
                    tmp.append( filter_range_date(3) )
                if '4' in status:
                    tmp.append( filter_range_date(4) )
                if '5' in status:
                    tmp.append( filter_range_date(5) )
                if '6' in status:
                    tmp.append( filter_range_date(6) )

                # confirmed
                if '777' in status:
                    ds = date_start
                    l = 0 # last
                    t = [] # list of counter

                    while ds < date_end :
                        l += sch_objs.filter(occurrenceconfirmation__isnull=False, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()
                        t.append( l )
                        ds += relativedelta(months=1)

                    tmp.append(t)

                # not confirmed
                if '888' in status:
                    ds = date_start
                    l = 0 # last
                    t = []

                    while ds < date_end :
                        l += sch_objs.filter(occurrenceconfirmation__isnull=True, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()
                        t.append( l )
                        ds += relativedelta(months=1)

                    tmp.append(t)

                c = 0 # TMP array position
                data = '([' # open
                ds = date_start

                while ds < date_end :

                    t = ""
                    for x in tmp:
                        t += "%s," % x[c]

                    tl = "[new Date(%s, %s), %s]," % (ds.year, ds.month, t)
                    data += tl

                    c += 1
                    ds += relativedelta(months=1)

                    del(tl)

                data += '])' # close


        #
        # not accumulated 
        #
        if accumulated == 'False':

            ds = date_start
            data = '([' # open

            while ds < date_end :
                tmp = ""

                if '1' in status:
                    tmp += "%s," % sch_objs.filter(occurrenceconfirmation__presence=1, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()

                if '2' in status:
                    tmp += "%s," % sch_objs.filter(occurrenceconfirmation__presence=2, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()

                if '3' in status:
                    tmp += "%s," % sch_objs.filter(occurrenceconfirmation__presence=3, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()

                if '4' in status:
                    tmp += "%s," % sch_objs.filter(occurrenceconfirmation__presence=4, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()

                if '5' in status:
                    tmp += "%s," % sch_objs.filter(occurrenceconfirmation__presence=5, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()

                if '6' in status:
                    tmp += "%s," % sch_objs.filter(occurrenceconfirmation__presence=6, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()

                # confirmed
                if '777' in status:
                    tmp += "%s," % sch_objs.filter(occurrenceconfirmation__isnull=False, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()

                # not confirmed
                if '888' in status:
                    tmp += "%s," % sch_objs.filter(occurrenceconfirmation__isnull=True, start_time__gte=ds, end_time__lte=ds+relativedelta(months=1)).count()

                tl = "[new Date(%s, %s), %s]," % (ds.year, ds.month, tmp)
                data += tl
                del(tmp)
                
                ds += relativedelta(months=1)

            data += '])' # close

        # return
        return data, lines, date_start, date_end, sch_list, total_events


    def get_receive_(self, organization, date_start, date_end, professional, receive, service, pway, covenant ):
        date_start , date_end = self.set_date(organization, date_start, date_end)

        '''
            data : array or False
            data return False when no numbers to make a graphic
            covenant : Covenant.id

            PaymentWay hardcode
                Dinheiro 1
                Cheque 2
                Cartão débito 3
                Cartão crédito 4
                Boleto 5
                Depósito em conta 6
        '''

        data = []
        receive_list = []
        receive_ar = []
        total_receive = 0
        colors = []

        # overview of all status
        # date range, all professional and all services
        aberto = Receive.objects.filter(status=0, created__gte=date_start, created__lte=date_end).filter( Q(occurrence__event__referral__client__person__organization=organization)| Q(referral__client__person__organization=organization) ).distinct().order_by('-created')

        recebido = Receive.objects.filter(status=1, created__gte=date_start, created__lte=date_end).filter( Q(occurrence__event__referral__client__person__organization=organization)| Q(referral__client__person__organization=organization) ).distinct().order_by('-created')

        faturado = Receive.objects.filter(status=2, created__gte=date_start, created__lte=date_end).filter( Q(occurrence__event__referral__client__person__organization=organization)| Q(referral__client__person__organization=organization) ).distinct().order_by('-created')

        cancelado = Receive.objects.filter(status=3, created__gte=date_start, created__lte=date_end).filter( Q(occurrence__event__referral__client__person__organization=organization)| Q(referral__client__person__organization=organization) ).distinct().order_by('-created')

        # professional
        if not professional == 'all':
            aberto = aberto.filter( Q( occurrence__event__referral__professional__id=professional )| Q( referral__professional__id=professional ) ).distinct()
            recebido = recebido.filter( Q( occurrence__event__referral__professional__id=professional )| Q( referral__professional__id=professional ) ).distinct()
            faturado = faturado.filter( Q( occurrence__event__referral__professional__id=professional )| Q( referral__professional__id=professional ) ).distinct()
            cancelado = cancelado.filter( Q( occurrence__event__referral__professional__id=professional )| Q( referral__professional__id=professional ) ).distinct()

        # covenant
        if not covenant == 'all':
            aberto = aberto.filter( covenant_id=covenant )
            recebido = recebido.filter( covenant_id=covenant )
            faturado = faturado.filter( covenant_id=covenant )
            cancelado = cancelado.filter( covenant_id=covenant )

        # payment_way 
        if not pway == 'all':

            if pway == '1':
                aberto = aberto.filter(covenant_payment_way_selected__icontains='1').distinct()
                recebido = recebido.filter(covenant_payment_way_selected__icontains='1').distinct()
                faturado = faturado.filter(covenant_payment_way_selected__icontains='1').distinct()
                cancelado = cancelado.filter(covenant_payment_way_selected__icontains='1').distinct()

            if pway == '2':
                aberto = aberto.filter(covenant_payment_way_selected__icontains='2').distinct()
                recebido = recebido.filter(covenant_payment_way_selected__icontains='2').distinct()
                faturado = faturado.filter(covenant_payment_way_selected__icontains='2').distinct()
                cancelado = cancelado.filter(covenant_payment_way_selected__icontains='2').distinct()

            if pway == '3':
                aberto = aberto.filter(covenant_payment_way_selected__icontains='3').distinct()
                recebido = recebido.filter(covenant_payment_way_selected__icontains='3').distinct()
                faturado = faturado.filter(covenant_payment_way_selected__icontains='3').distinct()
                cancelado = cancelado.filter(covenant_payment_way_selected__icontains='3').distinct()

            if pway == '4':
                aberto = aberto.filter(covenant_payment_way_selected__icontains='4').distinct()
                recebido = recebido.filter(covenant_payment_way_selected__icontains='4').distinct()
                faturado = faturado.filter(covenant_payment_way_selected__icontains='4').distinct()
                cancelado = cancelado.filter(covenant_payment_way_selected__icontains='4').distinct()

            if pway == '5':
                aberto = aberto.filter(covenant_payment_way_selected__icontains='5').distinct()
                recebido = recebido.filter(covenant_payment_way_selected__icontains='5').distinct()
                faturado = faturado.filter(covenant_payment_way_selected__icontains='5').distinct()
                cancelado = cancelado.filter(covenant_payment_way_selected__icontains='5').distinct()

            if pway == '6':
                aberto = aberto.filter(covenant_payment_way_selected__icontains='6').distinct()
                recebido = recebido.filter(covenant_payment_way_selected__icontains='6').distinct()
                faturado = faturado.filter(covenant_payment_way_selected__icontains='6').distinct()
                cancelado = cancelado.filter(covenant_payment_way_selected__icontains='6').distinct()

        if receive == 'all': # receive status

            receive_ar = ['0','1','2','3'] # all

            # graphic pizza
            data.append( ['Aberto',aberto.count()] )
            data.append( ['Recebido',recebido.count()] )
            data.append( ['Faturado',faturado.count()] )
            data.append( ['Cancelado',cancelado.count()] )

            total_receive = aberto.count()+recebido.count()+faturado.count()+cancelado.count()

            colors = ['red', 'green', 'orange', 'blue']

        else:

            if receive == '0':
                receive_ar.append('0')
                data.append( ['Aberto',aberto.count()] )
                total_receive += aberto.count()
                colors.append('red')

            if receive == '1':
                receive_ar.append('1')
                data.append( ['Recebido',recebido.count()] )
                total_receive += recebido.count()
                colors.append('green')

            if receive == '2':
                receive_ar.append('2')
                data.append( ['Faturado',faturado.count()] )
                total_receive += faturado.count()
                colors.append('orange')

            if receive == '3':
                receive_ar.append('3')
                data.append( ['Cancelado',cancelado.count()] )
                total_receive += cancelado.count()
                colors.append('blue')


        # filter by service
        if not service == '':

            if '0' in receive_ar :
                aberto = aberto.filter(Q(occurrence__event__referral__service=service)|Q(referral__service=service) ).distinct()

            if '1' in receive_ar :
                recebido = recebido.filter(Q(occurrence__event__referral__service=service)|Q(referral__service=service) ).distinct()

            if '2' in receive_ar :
                faturado = faturado.filter(Q(occurrence__event__referral__service=service)|Q(referral__service=service) ).distinct()

            if '3' in receive_ar :
                cancelado = cancelado.filter(Q(occurrence__event__referral__service=service)|Q(referral__service=service) ).distinct()


        # amount of earch status, total column
        total_aberto = 0
        for x in aberto:
            total_aberto += x.total

        total_recebido = 0
        for x in recebido:
            total_recebido += x.total

        total_faturado = 0
        for x in faturado:
            total_faturado += x.total

        total_cancelado = 0
        for x in cancelado:
            total_cancelado += x.total


        '''
            array
                0 = Status label
                1 = list of payment. Payment object
                2 = color of status
                3 = sum total of status
        '''
        # list of clients and counter %
        if '0' in receive_ar :
            receive_list.append( ['Aberto',aberto,'red',total_aberto] )

        if '1' in receive_ar :
            receive_list.append( ['Recebido',recebido,'green',total_recebido] )

        if '2' in receive_ar :
            receive_list.append( ['Faturado',faturado,'orange',total_faturado] )

        if '3' in receive_ar :
            receive_list.append( ['Cancelado',cancelado,'blue',total_cancelado] )

        if total_receive == 0 :  # no data
            data = False

        return data, colors, date_start, date_end, receive_list, total_receive
        

    def get_referral_range(self, organization, date_start, date_end, service, accumulated):
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
            data = ReportReferral.objects.all(range, date_start, date_end, organization, service, accumulated)
            
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

    def chart_dots_by_period(self, objects_range, date_start = None, date_end = None, accumulated=None, referral_discharged=False, accumulated_each_period=True):
        """
        return x and y coordinates in objects range
        note: object must have created() attribute
        """
        dots = []
        start_tmp = date_start
        registers_in_period_last = 0

        """
        start chart with actual count of registers
        """

        accumulated_increase = 0 if not accumulated else accumulated

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
            if not referral_discharged:
                registers_in_period = range.filter(date__gte=start_tmp, date__lte=next_period).count()
            else:
                registers_in_period = range.filter(referraldischarge__date__gte=start_tmp, referraldischarge__date__lte=next_period).count()

            dots.append(registers_in_period + registers_in_period_last + accumulated_increase) # coordinates here: x, y
            
            if accumulated_each_period == 'True': # start point from the last loop
                registers_in_period_last = registers_in_period + registers_in_period_last
            
            if accumulated: # start graph with initials Y values
                accumulated_increase = registers_in_period + accumulated_increase
        
            start_tmp = start_tmp+scale
            
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
    def overview(self, range, date_start, date_end, accumulated=True):

        """
        return a list with admission overview data splited
        in individuals and companies clients type
        """

        data = []
        total = len(range)
        individuals_range = range.filter(client__person__company__isnull=True)
        companies_range = range.filter(client__person__company__isnull=False)
        
        chart_data = []
        chart_data.append(Report().chart_dots_by_period(individuals_range, date_start, date_end, None, False, accumulated))
        chart_data.append(Report().chart_dots_by_period(companies_range, date_start, date_end, None, False, accumulated))
        chart_data.append(Report().chart_dots_by_period(range, date_start, date_end, None, False, accumulated))
        chart_url = Report().get_chart(chart_data, date_start, date_end, ['0000ff','ffa542', '000000'])
        
        data.append({'name': _('Individuals'), 'total': individuals_range.count(), 'percentage': percentage(individuals_range.count(), total), 'url':reverse('admission_client_overview_individuals'), 'color':'0000ff' })
        data.append({'name': _('Companies'), 'total': companies_range.count(), 'percentage': percentage(companies_range.count(), total), 'url':reverse('admission_client_overview_companies'), 'color':'ffa542'})
        data.append({'name': _('Total'), 'total': total, 'percentage': '', 'url':reverse('admission_client_overview_total'), 'color':'000000'})
        
        return data, chart_url

    def signed(self, range):
    
        """
        return a list with relation between client that have 'signed by client'
        and clients that have not signed it
        """

        data = []
        total = len(range)
        signed = range.filter(signed_bythe_client=True).count()
        not_signed = range.filter(signed_bythe_client=False).count()
        
        chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
        chart.add_data([Decimal(percentage(signed, total)), Decimal(percentage(not_signed, total))])
        chart.set_pie_labels([_(u"Admission Signed").encode('utf8'), _(u"Admission Not Signed").encode('utf8')])
        chart.set_colours(['00ff00','ff0000']) # red, green
        
        data.append({'name': _('Signed'), 'total': signed, 'percentage': percentage(signed, total), 'url':reverse('admission_client_signed_signed'), 'color':'00ff00' })
        data.append({'name': _('Not Signed'), 'total': not_signed, 'percentage': percentage(not_signed, total), 'url':reverse('admission_client_signed_notsigned'), 'color': 'ff0000' })
        
        return data, chart.get_url()

    def knowledge(self, range):

        """
        return a list of clients x knowledge marked in admission form
        list sorted by ranking
        """

        qknowledge = AdmissionIndication.objects.filter(id__gt = 0)
        data = []

        # start chart
        chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
        chart_add_data = []
        chart_set_colours = []

        tosort = []
        for i in qknowledge: # order reverse
            tosort.append((i.pk, range.filter(referral_choice=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            i = AdmissionIndication.objects.get(pk=id)
            count = range.filter(referral_choice=i).count()
            if count > 0:
                data.append({'name': i.description, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('admission_client_knowledge', args=[i.pk]), 'color':i.color  or '000000'})
                chart_add_data.append(Decimal(percentage(count, range.count())))
                chart_set_colours.append(i.color or '000000') # red, green
        chart.add_data(chart_add_data)
        chart.set_colours(chart_set_colours)
            
        return data, chart.get_url()

    def all(self, range, date_start, date_end, accumulated=True):
        """
        return a list with all table data above
        """
        data = []
        
        table_data, chart_url = ReportAdmission.objects.overview(range, date_start, date_end, accumulated)
        data.append({'title': _('Admission Overview'), 'data': table_data, 'chart_url': chart_url })
        
        table_data, chart_url = ReportAdmission.objects.signed(range)
        data.append({'title': _('Admission Signed'), 'data': table_data, 'chart_url': chart_url})
        
        table_data, chart_url = ReportAdmission.objects.knowledge(range)
        data.append({'title': _('Admission Knowledge'), 'data': table_data, 'chart_url': chart_url})

        return data, chart_url

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
    def overview(self, range, date_start, date_end, return_chart_url=False, organization=None, service=None, accumulated=True):

        """
        return a list with admission overview data splited
        in individuals and companies clients type
        """

        data = []

        total = len(range)

        subscriptions = range
        discharged_range = Referral.objects.filter(service__organization=organization, referraldischarge__date__gte=date_start, referraldischarge__date__lt=date_end)

        if service:
            discharged_range = discharged_range.filter(service=service)

        referral_internal_range = range.filter(referral__isnull=False)
        referral_external_range = range.filter(referralexternal__isnull=False)

        if return_chart_url:
            data = []
            data.append(Report().chart_dots_by_period(subscriptions, date_start, date_end, None, False, accumulated))
            data.append(Report().chart_dots_by_period(ReferralDischarge.objects.filter(referral__in=discharged_range), date_start, date_end, None, False, accumulated))
            data.append(Report().chart_dots_by_period(referral_internal_range, date_start, date_end, None, False, accumulated))
            data.append(Report().chart_dots_by_period(referral_external_range, date_start, date_end, None, False, accumulated))

            return Report().get_chart(data, date_start, date_end, ['000000', '0000ff', '557700', 'aa88aa' ])

        data.append({'name': _('Subscriptions'), 'total': subscriptions.count(), 'url':reverse('referral_client_overview_charged'), 'color':'000000', })
        data.append({'name': _('Subscriptions Discharged'), 'total': discharged_range.count(), 'url':reverse('referral_client_overview_discharged'), 'color':'0000ff' })
        data.append({'name': _('Internal Referrals'), 'total': referral_internal_range.count(), 'url':reverse('referral_client_overview_internal'), 'color':'557700'})
        data.append({'name': _('External Referrals'), 'total': referral_external_range.count(), 'url':reverse('referral_client_overview_external'), 'color':'aa88aa'})
        
        return data

    def discussed(self, range, organization, date_start, date_end, return_chart_url=False, service=None):

        """
        return a list with referral discussed or not with client
        """

        data = []

        range = Referral.objects.filter(service__organization=organization, referraldischarge__date__gte=date_start, referraldischarge__date__lt=date_end)
        
        if service:
            range = range.filter(service=service)

        total = len(range)

        discharged_discussed_with_client = range.filter(referraldischarge__was_discussed_with_client=True).count()
        discharged_not_discussed_with_client = range.filter(referraldischarge__was_discussed_with_client=False).count()
        
        if return_chart_url and range:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart.add_data([Decimal(percentage(discharged_discussed_with_client, total)), Decimal(percentage(discharged_not_discussed_with_client, total))])
            chart.set_pie_labels([_(u"Referral Discharge Discussed with client").encode('utf8'), _(u"Referral Discharge Not discussed with client").encode('utf8')])
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
        range = range.filter(indication__isnull=False)
        
        if return_chart_url:
            chart = PieChart3D(PIE_CHART_WIDTH, PIE_CHART_HEIGHT)
            chart_add_data = []
            chart_set_pie_labels = []
            chart_set_colours = []
            
            for i in qknowledge:
                count = range.filter(indication__indication_choice=i.pk).count()
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
            tosort.append((i.pk, range.filter(indication__indication_choice=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            count = range.filter(indication__indication_choice=id).count()
            if count:
                i = ReferralIndicationChoice.objects.get(pk=id)
                data.append({'name': ReferralIndicationChoice.objects.get(pk=id).description, 'total': count, 'percentage': percentage(count, range.count()), 'url':reverse('referral_client_knowledge', args=[id]), 'color': i.color or '000000',})
        
        return data

    def services(self, range, organization, date_start, date_end, return_chart_url=False, accumulated=True):

        services = organization.service_set.all()

        if return_chart_url:
            data = []
            service_colors = []
            for i in services: # order reverse
                results = range.filter(service=i)
                if results:
                    data.append(Report().chart_dots_by_period(results, date_start, date_end, None, False, accumulated))
                    service_colors.append(i.color or '000000')

            return Report().get_chart(data, date_start, date_end, service_colors)

        data = []

        tosort = []
        for i in services: # order reverse
            tosort.append((i.pk, range.filter(service=i).count()))

        ids_ordered = sorted(tosort, key=lambda total: total[1], reverse=True)

        for id,total in ids_ordered:
            s = services.get(pk=id)
            count = range.filter(service__pk=id).count()
            
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

    def service_discharges(self, range, organization, date_start, date_end, discussed_with_client=None, return_chart_url=False, service=None, accumulated=True):

        services = organization.service_set.all()
        data = []

        range = Referral.objects.filter(service__organization=organization, referraldischarge__date__gte=date_start, referraldischarge__date__lt=date_end)

        if service:
            range = range.filter(service=service)

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
                        data.append(Report().chart_dots_by_period(results, date_start, date_end, False, True, accumulated))
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

    def service_discharge_reason(self, range, organization, date_start, date_end, return_chart_url=False, service=None):
        
        """
        return a list of reason discharges with a total of occurrences
        """

        qknowledge = ReferralDischargeReason.objects.filter(id__gt = 0)

        range = Referral.objects.filter(service__organization=organization, referraldischarge__date__gte=date_start, referraldischarge__date__lt=date_end)

        if service:
            range = range.filter(service=service)

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

    def all(self, range, date_start, date_end, organization=None, service=None, accumulated=True):
        """
        return a list with all table data above
        """
        data = []

        if service:
            in_service_range = range.filter(service__pk=service)
            to_service_range = range.filter(referral__service__pk=service).exclude(service__pk=service)
            from_service_range = range.filter(service__pk=service, referral__service__isnull=False).exclude(referral__service__pk=service)
            range = in_service_range
        
        data.append({'title': _('Subscriptions Overview'), 'data': ReportReferral.objects.overview(range if not service else in_service_range, date_start, date_end, False, organization, service, accumulated), 'chart_url': ReportReferral.objects.overview(range if not service else in_service_range, date_start, date_end, True, organization, service, accumulated), 'without_percentage':True })

        if not service:
            data.append({'title': _('Service Subscriptions'), 'data': ReportReferral.objects.services(range, organization, date_start, date_end, False, accumulated), 'chart_url':ReportReferral.objects.services(range, organization, date_start, date_end, True, accumulated)})
            data.append({'title': _('Discharges from Services'), 'data': ReportReferral.objects.service_discharges(range, organization, date_start, date_end), 'chart_url':ReportReferral.objects.service_discharges(range, organization, date_start, date_end, None, True, None, accumulated)})

        data.append({'title': _('Subscriptions Discharged Discussed'), 'data': ReportReferral.objects.discussed(range if not service else in_service_range, organization, date_start, date_end, False, service), 'chart_url': ReportReferral.objects.discussed(range if not service else in_service_range, organization, date_start, date_end, True, service)})
        data.append({'title': u'%s (%s)' % (_('Subscriptions Indications'), _('Excluding internal referrals')), 'data': ReportReferral.objects.knowledge(range if not service else in_service_range), 'chart_url': ReportReferral.objects.knowledge(range if not service else in_service_range, True)})

        data.append({'title': _('Internal Referrals to Services'), 'data': ReportReferral.objects.referral_internal(range if not service else to_service_range, organization), 'chart_url':ReportReferral.objects.referral_internal(range if not service else to_service_range, organization, None, True)})
        data.append({'title': _('Internal Referrals from Services'), 'data': ReportReferral.objects.referral_internal(range if not service else from_service_range, organization, True), 'chart_url':ReportReferral.objects.referral_internal(range if not service else from_service_range, organization, True, True)})

        if not service:
            data.append({'title': _('Externals Referrals from Services'), 'data': ReportReferral.objects.referral_external(range, organization), 'chart_url':ReportReferral.objects.referral_external(range, organization, True)})

        data.append({'title': _('Discharges Reason'), 'data': ReportReferral.objects.service_discharge_reason(range, organization, date_start, date_end, False, service), 'chart_url': ReportReferral.objects.service_discharge_reason(range, organization, date_start, date_end, True, service)})

        if not service:
            data.append({'title': _('Discharges Discussed with Client'), 'data': ReportReferral.objects.service_discharges(range, organization, date_start, date_end, True, False, service), 'chart_url': ReportReferral.objects.service_discharges(range, organization, date_start, date_end, True, True, service)})

        data.append({'title': _('Professional Subscriptions'), 'data': ReportReferral.objects.professionals(range, organization)})

        return data

    def clients(self,  user,  date_start, date_end, view, filter, service=None):
        """
        return a list of clients from selected report and selected range
        """
        
        """ admissions range """
        organization = user.get_profile().org_active
        query = Referral.objects_inrange.all(organization, date_start, date_end)
        query_discharged = Referral.objects.filter(service__organization=organization, referraldischarge__date__gte=date_start, referraldischarge__date__lt=date_end)
        query_full = query
        service_pks = [s.pk for s in organization.service_set.all()]
        professional_pks = [p.pk for p in CareProfessional.objects.from_organization(organization)]
        if service:
            query = query.filter(service__pk=service)

        if view == 'overview':

            if filter == 'total':
                verbose_name = _('Referral Total')

            if filter == 'charged':
                query = query.filter()
                verbose_name = _('Referral Charged')

            if filter == 'discharged':
                query = query_discharged
                verbose_name = _('Referral Discharged')
            
            if filter == 'discharged_discussed':
                query = query_discharged.filter(referraldischarge__was_discussed_with_client=True)
                verbose_name = _('Referral Discharged Discussed')

            if filter == 'discharged_not_discussed':
                query = query.query_discharged(referraldischarge__was_discussed_with_client=False)
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
            obj = get_object_or_None(Service, pk=filter, pk__in=service_pks)
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
            query = query_discharged.filter(service=filter, service__pk__in=service_pks)
            obj = get_object_or_None(Service, pk=filter, pk__in=service_pks )
            verbose_name = _(u'Discharges from Service %s' % (obj))
        
        if view == 'discharge_reason':
            query = query_discharged.filter(referraldischarge__reason=filter)
            obj = get_object_or_None(ReferralDischargeReason, pk=filter)
            verbose_name = _(u'Discharged by reason %s' % (obj))
        
        if view == 'discharge_discussed':
            query = query_discharged.filter(service=filter, referraldischarge__was_discussed_with_client=True, service__pk__in=service_pks)
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
        data.append({'name': _('Female'), 'total': female, 'percentage': percentage(female, total)})
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
