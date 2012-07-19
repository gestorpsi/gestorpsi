# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi
"""

from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from gestorpsi.gcm.forms.auth import RegistrationForm
from django.views.generic.simple import direct_to_template as django_direct_to_template
from gestorpsi.gcm.views.generic import create_object, object_detail, update_object, update_invoice_wrapper, update_organization_wrapper, object_list, delete_object, direct_to_template
from gestorpsi.gcm.views.auth import object_activate

from gestorpsi.gcm.views.views import org_object_list, billet_config

from gestorpsi.gcm.models import Plan
from gestorpsi.gcm.models import Invoice
#from gestorpsi.gcm.forms.plan import PlanForm
from gestorpsi.gcm.forms.invoice import InvoiceForm
from gestorpsi.organization.models import Organization
from gestorpsi.boleto.models import ReturnFile
from django.contrib.auth import views as auth_views


import os
GCM_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


plan_list = { 'queryset':Plan.objects.all(), }
plan_update = { 'model':Plan, 'post_save_redirect': '/gcm/plan/',}
plan_add = { 'model':Plan, 'post_save_redirect': '/gcm/plan/', }

retfile_list = { 'queryset':ReturnFile.objects.all(), 'template_name': 'gcm/returnfile_list.html'}
retfile_update = { 'model':ReturnFile, 'post_save_redirect': '/gcm/retfile/', 'template_name': 'gcm/returnfile_form.html'}
retfile_add = { 'model':ReturnFile, 'post_save_redirect': '/gcm/retfile/', 'template_name': 'gcm/returnfile_form.html' }

invoice_list = { 'queryset':Invoice.objects.all(), }
invoice_update = { 'form_class':InvoiceForm, 'post_save_redirect': '/gcm/invoice/',}
invoice_add = { 'form_class':InvoiceForm, 'post_save_redirect': '/gcm/invoice/', }

org_list = {'queryset': Organization.objects.filter(organization__isnull=True, person__profile__user__registrationprofile__activation_key='ALREADY_ACTIVATED').distinct(), 'template_name':'gcm/org_list.html'}
org_update = { 'model':Organization, 'post_save_redirect': '/gcm/org/', 'template_name': 'gcm/org_form.html'}

org_bill_update = { 'model':Invoice }
org_org_update = { 'model':Organization }


org_pen_list = { 'queryset':Organization.objects.filter(organization__isnull=True).exclude(person__profile__user__registrationprofile__activation_key='ALREADY_ACTIVATED').distinct(), 'template_name': 'gcm/org_pen_list.html'}
org_pen_detail = { 'queryset':Organization.objects.filter(organization__isnull=True).exclude(person__profile__user__registrationprofile__activation_key='ALREADY_ACTIVATED').distinct(), 'template_name': 'gcm/org_pen_detail.html'}
org_pen_del = { 'model':Organization, 'post_delete_redirect': '/gcm/orgpen/', 'template_name': 'gcm/delete.html'}
#org_pen_update = { 'model':Organization, 'post_save_redirect': '/gcm/org/', 'template_name': 'gcm/org_form.html'}

urlpatterns = patterns('',
    url(r'^gcm/login/$', auth_views.login, {'template_name': 'gcm/login.html', }, name='gcm-login'),
    url(r'^gcm/logout/$', auth_views.logout, {'template_name': 'gcm/logout.html'}, name='gcm-logout'),
    url(r'^register/complete/$', 'gestorpsi.gcm.views.auth.complete', name='gcm-registration-complete'),
    #url(r'^register/complete/$', django_direct_to_template, {'template': 'gcm/registration_complete.html'}, name='gcm-registration-complete'),
    url(r'accounts/register/$', 'gestorpsi.gcm.views.auth.register', {'form_class': RegistrationForm, 'template_name':'gcm/registration_form.html' }, name='registration_register'),
    
    url(r'gcm/$', direct_to_template, {'template':'gcm/index.html'}, name='gcm-index'),
    
    url(r'gcm/plan/$', object_list, plan_list, name='plan-list'),
    url(r'gcm/plan/(?P<object_id>\d+)/$', update_object, plan_update, name='plan-update'),
    url(r'gcm/plan/add/$', create_object, plan_add, name='plan-add'),
    
    url(r'gcm/retfile/$', object_list, retfile_list, name='retfile-list'),
    url(r'gcm/retfile/(?P<object_id>\d+)/$', update_object, retfile_update, name='retfile-update'),
    url(r'gcm/retfile/add/$', create_object, retfile_add, name='retfile-add'),
    
    url(r'gcm/billet_config/$', billet_config, name='billet-config'),
    
    
    url(r'gcm/org/(?P<order_by>\w+)/$', org_object_list, org_list, name='org-list'),
    url(r'gcm/org/$', org_object_list, org_list, name='org-list'),
    url(r'gcm/org/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', update_object, org_update, name='org-update'),
    
    url(r'gcm/org/up/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', update_organization_wrapper, org_org_update, name='org-org-update'),
    
    url(r'gcm/bill/(?P<object_id>\w+)/$', update_invoice_wrapper, org_bill_update, name='org-bill-update'),
    
    url(r'gcm/orgpen/$', org_object_list, org_pen_list, name='org-pen-list'),
    url(r'gcm/orgpen/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', object_detail, org_pen_detail, name='org-pen-detail'),
    url(r'gcm/orgpen/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/del/$', delete_object, org_pen_del, name='org-pen-del'),
    url(r'gcm/orgpen/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/activate/$', object_activate, name='org-pen-activate'),
    #url(r'gcm/orgpen/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', update_object, org_update, name='org-update'),
    
    url(r'gcm/invoice/$', object_list, invoice_list, name='invoice-list'),
    url(r'gcm/invoice/(?P<object_id>\d+)/$', update_object, invoice_update, name='invoice-update'),
    url(r'gcm/invoice/add/$', create_object, invoice_add, name='invoice-add'),
    #url(r'gcm/$', 'gcm.views.admin.', {'form_class': RegistrationForm, 'template_name':'gcm/registration_form.html' }, name='registration_register'),
    url(r'gcm_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(GCM_ROOT_PATH, 'media/'), 'show_indexes': False}),
)
