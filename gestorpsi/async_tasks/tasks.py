# -*- coding: utf-8 -*-

from django.utils.encoding import smart_str, force_unicode
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMessage, BadHeaderError
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from gestorpsi.address.models import City, Address, Country
#from gestorpsi.boleto.functions import gera_boleto_bradesco
from gestorpsi.document.models import Document, TypeDocument
from gestorpsi.gcm.models import Plan, Invoice
from gestorpsi.organization.models import Organization, ProfessionalResponsible, Activitie

from celery.task import PeriodicTask
from celery.schedules import crontab
from celery.task import Task
from celery.registry import tasks

import httplib
import urllib
import urllib2
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange


class CheckAndCharge(PeriodicTask):
    #run_every = timedelta(seconds=30)
    run_every = crontab(hour=2, minute=0, day_of_week="*")

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("CheckAndCharge Started.")

        orgs = Organization.objects.filter(organization__isnull=True, active=True)
        #for p in Invoice.objects.all():
        #    p.expiry_date = p.expiry_date
        #    p.save()
    
        '''
        INVOICE_STATUS_CHOICES = (
            (1, _('Emitido')),
            (2, _('Pago')),
            (3, _('Excluido')),
        )
        INVOICE_TYPES = (
            (1, _('Inscription')),
            (2, _('Monthly fee')),
        )
        '''
        for org in orgs:
            last_invoice = org.current_invoice
            
            #correcao temporaria para evitar problemas no desenvolvimento
            try:
                len(last_invoice.status)
            except:
                last_invoice = Invoice.objects.filter(organization=org).order_by('-date')[0]
            
            if last_invoice.status == 1: #check if the last invoice isn't paid
                check = last_invoice.due_date > datetime.now() #check if the invoice is not due
            elif last_invoice.status == 2:
                #check if this company last paid invoice is going to expire in ten days
                check = last_invoice.expiry_date < datetime.today()+timedelta(days=10)
            else:
                check = True
    
            if check: #no need to do anything with this organization
                continue
            else:#send an email to the person responsible for the organization with a new billet to pay
                person = ProfessionalResponsible.objects.get(organization=org).person
                user = person.user
    
                #create the new invoice
                inv = Invoice()
                inv.organization = org
                
                #prefered plan
                pplan = org.prefered_plan
                
                #verifica se ha um invoice passado para extrair um plano, caso nao,
                #atribui um plano de um mes para a quantia de funcionarios cadastrados
                staff_count = org.person_set.all().count()
                if pplan is not None:
                    inv.plan = pplan
                elif last_invoice.plan is not None:
                    inv.plan = last_invoice.plan
                else:
                    inv.plan = None
                
                #define a data de vencimento(pagamento) do boleto
                dday = org.default_payment_day
                inv.due_date = last_invoice.expiry_date.replace(day=dday)
                
                #define a data de vencimento(acesso ao sistema) do boleto
                pplan = org.prefered_plan
                inv.expiry_date = inv.due_date + relativedelta(months=pplan.duration)
                inv.save()
                
                org.current_invoice = inv
                org.save()
                url_boleto = gera_boleto_bradesco(user.id, inv)
    
    
                email = user.email
                if email is not None and len(email) > 0:
                    bcc_list = ['teagom@gmail.com', user.email]
                else:
                    bcc_list = ['teagom@gmail.com']
                msg = EmailMessage()
                msg.subject = 'Teste: Cobrança de mensalidade'
                #temp = request.META
                #if request is None:
                msg.body = render_to_string('async_tasks/email_cobranca_mensalidade.html', locals())
                #else:
                #    from celery.schedules import discard_all
                #    discard_all()
                #    return render_to_response('async_tasks/email_cobranca_mensalidade.html', locals())
                #msg.from = 'GestoPSI <webmaster@gestorpsi.com.br>'
                msg.to = ['teagom@gmail.com', ]
                msg.bcc =  bcc_list
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                
        logger.info("CheckAndCharge Finished.\n\n")

tasks.register(CheckAndCharge)


def check_and_charge():
    CheckAndCharge().run()
