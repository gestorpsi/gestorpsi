# -*- coding: utf-8 -*-

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime, timedelta
from celery.task import Task
from celery.registry import tasks

import httplib
import urllib
import urllib2
import re

from django.utils.encoding import smart_str, force_unicode
from django.contrib.auth.models import User
from gestorpsi.document.models import Document, TypeDocument
from gestorpsi.address.models import City, Address, Country

from gestorpsi.gcm.models import Plan, Invoice
from gestorpsi.organization.models import Organization, ProfessionalResponsible, Activitie
from gestorpsi.boleto.functions import gera_boleto_bradesco

# this will run everyday at 3:00 am, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
#@periodic_task(run_every=crontab(hour="3", minute="0", day_of_week="*"))
#@periodic_task(run_every=crontab(hour="*", minute="*", second=5, day_of_week="*"))
@periodic_task(run_every=timedelta(minutes=0, seconds=10))
def check_and_charge():
    orgs = Organization.objects.filter(organization__isnull=True)
    #d = str(datetime.now())
    #a = Activitie(description=str(orgs))
    #a.save()
    for org in orgs:
        person = org.professionalresponsible.person
        user = person.user
        try:
            url_boleto = gera_boleto_bradesco(user.id, days=10)
        except:
            pass
        email = user.email
        if email is not None and len(email) > 0:
            bcc_list = ['jayme@doois.com.br', user.email]#, 'david@doois.com.br'
        else:
            bcc_list = ['jayme@doois.com.br']
        msg = EmailMessage()
        msg.subject = 'Teste: Cobrança de mensalidade'
        msg.body = 'Vamos senhor, tem de pagar para continuar usando o sistema.\n'
        msg.body += 'Numero de funcionarios: '+ str(org.employees().count())
        msg.body += '\n Boleto exemplo: '+url_boleto
        #msg.from = 'GestoPSI <webmaster@gestorpsi.com.br>'
        msg.to = ['jayme@doois.com.br', ]
        msg.bcc =  bcc_list
        #msg.content_subtype = "text"  # Main content is now text/html
        msg.send()
    '''
    gera_boleto_bradesco(resp_usuario_id, days=7)
    user = User.objects.get( pk=int(resp_usuario_id) )
    profile = user.get_profile()
    person = profile.person

    d = Document()
    t = TypeDocument.objects.get(description='CPF')
    cpf = person.document.get(typeDocument__id=t.id).document
    addr = endereco = person.address.all()[0]
    data = BradescoBilletData.objects.all()[0]
    inv = Invoice.objects.get(organization=org)'''


'''class CheckAndCharge(Task):
    def run(self, some_arg, **kwargs):
        from gestorpsi.organization.models import Activitie
        d = str(datetime.now())
        a = Activitie(description= d )
        a.save()
        print d
        logger = self.get_logger(**kwargs)
        logger.info("Did something: %s" % some_arg)
        return d
tasks.register(CheckAndCharge)'''