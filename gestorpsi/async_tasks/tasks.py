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
from gestorpsi.boleto.functions import gera_boleto_bradesco
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
        '''
        for org in orgs:
            try:#check if there is any non-paid invoice that is not due
                last_invoice = Invoice.objects.filter(organization=org, status=1, due_date__gt=datetime.now()).order_by('-due_date')[0]
                check = True
            except:
                #check if this company last paid invoice is going to expire in ten days
                try:
                    last_invoice = Invoice.objects.filter(organization=org, status=2).order_by('-expiry_date')[0]
                    check = last_invoice.expiry_date is not None and (last_invoice.expiry_date < datetime.today()+timedelta(days=100))
                except:
                    #if there are no invoices matching the given criterias, it's going to generate a new one
                    last_invoice = None
                    check = False
    
            if check:#no need to do anything with this organization
                continue
            else:#send an email to the person responsible for the organization with a new billet to pay
                
                try:
                    person = ProfessionalResponsible.objects.get(organization=org).person
                except:
                    '''
                    * temporary code just to fix errors/mistakes due to the system improvement
                    * Jayme Tosi Neto - .doois. 2012
                    '''
                    person = org.person_set.all()[0]
                    prof = ProfessionalResponsible()
                    prof.organization = org
                    prof.person = person
                    prof.name = person.name
                    prof.save()
                user = person.user
    
                #create the new invoice
                inv = Invoice()
                inv.organization = org
                inv.due_date = datetime.today()+timedelta(days=10)
                
                #verifica se ha um invoice passado para extrair um plano, caso nao,
                #atribui um plano de um mes para a quantia de funcionarios cadastrados
                staff_count = org.person_set.all().count()
                if last_invoice is not None and last_invoice.plan is not None:
                    if last_invoice.plan.staff_size != staff_count:
                        inv.plan = Plan.objects.get(staff_size=staff_count, duration=last_invoice.plan.duration)
                    else:
                        inv.plan = last_invoice.plan
                else:
                    inv.plan = Plan.objects.get(staff_size=staff_count, duration=1)
                    
                inv.expiry_date = datetime.today() + relativedelta(months = inv.plan.duration) 
                inv.save()
                url_boleto = gera_boleto_bradesco(user.id, inv)
    
                email = user.email
                if email is not None and len(email) > 0:
                    bcc_list = ['jayme@doois.com.br']#, user.email]#, 'david@doois.com.br'
                else:
                    bcc_list = ['jayme@doois.com.br']
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
                msg.to = ['jayme@doois.com.br', ]
                msg.bcc =  bcc_list
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                
        logger.info("CheckAndCharge Finished.\n\n")

tasks.register(CheckAndCharge)


def check_and_charge():
    CheckAndCharge().run()
