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
from django.utils.translation import ugettext as _
from gestorpsi.client.models import Client
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.referral.models import Referral

DIAGNOSIS_STATUS = (
    ('1', _('Open')),
    ('2', _('Closed')),
)

DIAGNOSIS_STATUS2= (
    ('1', _('Present')),
    ('2', _('Absence')),
)

SEVERITY = (
    ('1', _('Mild')),
    ('2', _('Moderate')),
    ('3', _('Severe')),
)

DEMAND_STATUS = (
    ('1', _('Stagnant')),
    ('2', _('In progress')),
    ('3', _('Resolved')),
)

UNITS = (
    ('01', _('Second(s)')),
    ('02', _('Minut(s)')),
    ('03', _('Hour(s)')),
    ('04', _('Day(s)')),
    ('05', _('Week(s)')),
    ('06', _('Month(s)')),
    ('07', _('Year(s)')),
)

SESSION_GOALS = (
    ('01', _('Collection Data')),
    ('02', _('Evaluation')),
    ('03', _('Intervation')),
    ('04', _('Give a Feedback')),
    ('05', _('Follow up')),
    ('06', _('Meeting')),
    ('07', _('Observation')),
    ('08', _('Supervision')),
)

EDIT_STATUS = (
    ('1', _("Pending student's confirmation")),
    ('2', _("Pending supervisor's confirmation")),
    ('3', _("Pending professional's confirmation")),
    ('4', _("Confirmed by the professional")),
    ('99', _("Unknown")),
)

class TimeUnit(models.Model):
    unit = models.CharField(max_length=10)
    time = models.CharField(max_length=2, choices=UNITS)

class Demand(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    edit_status = models.CharField(max_length=2, choices=EDIT_STATUS)
    initial_complaint = models.BooleanField()
    demand = models.TextField(blank=True)
    description = models.TextField(blank=True)
    how_long_it_happens = models.OneToOneField(TimeUnit, null=True, related_name="how_long_it_happens")
    frequency = models.OneToOneField(TimeUnit, null=True, related_name="frequency")
    severity = models.CharField(max_length=1, choices=SEVERITY)
    duration = models.OneToOneField(TimeUnit, null=True, related_name="duration")
    demand_status = models.CharField(max_length=1, choices=DEMAND_STATUS)
    demand_resolution = models.DateTimeField(null=True)
    bibliography = models.TextField(blank=True)
    related_sites = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    client = models.ForeignKey(Client)
    referral = models.ForeignKey(Referral)
    occurrence = models.ForeignKey(ScheduleOccurrence, null=True)
    #related_terminology -> terminologias
    #attached_files -> upload generico

    def __unicode__(self):
        return u"%s" % self.demand

    class Meta:
        ordering = ['-occurrence']

class Diagnosis(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    edit_status = models.CharField(max_length=2, choices=EDIT_STATUS)
    diagnosis_date = models.DateTimeField(null=True)
    diagnosis_resolution = models.DateTimeField(null=True)
    diagnosis = models.TextField(blank=True)
    diagnosis_status = models.CharField(max_length=1, choices=DIAGNOSIS_STATUS)
    diagnosis_status2 = models.CharField(max_length=1, choices=DIAGNOSIS_STATUS2)
    clinical_description = models.TextField(blank=True)
    severity = models.CharField(max_length=1, choices=SEVERITY)
    treatment_indicated = models.TextField(blank=True)
    bibliography = models.TextField(blank=True)
    related_sites = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    client = models.ForeignKey(Client)
    referral = models.ForeignKey(Referral)
    occurrence = models.ForeignKey(ScheduleOccurrence, null=True)
    #related_demand = models.ManyToMany(Demand, null=True)
    #diagnosis -> terminologias
    #comorbity -> terminologias
    #attached_files -> upload genérico

    def __unicode__(self):
        return u"%s" % self.diagnosis

    class Meta:
        ordering = ['-occurrence']

class Session(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    edit_status = models.CharField(max_length=2, choices=EDIT_STATUS)
    session_goals = models.CharField(max_length=2, choices=SESSION_GOALS)
    descriptive = models.TextField(blank=True)
    client = models.ForeignKey(Client)
    referral = models.ForeignKey(Referral)
    occurrence = models.OneToOneField(ScheduleOccurrence)
    comments = models.TextField(blank=True)
    #procedures -> procedimentos
    #device -> ja tem no pós-atendimento
    #upload
    
    def __unicode__(self):
        return u"%s" % self.descriptive
    
    class Meta:
        ordering = ['-occurrence']

reversion.register(Demand)
reversion.register(Diagnosis)
reversion.register(Session)

"""
class SessionRecord(models.Model):
    client = models.ForeignKey(Client)
    referral = models.ForeignKey(Referral, null=True)
    occurrency = models.OneToOneField(Occurency, null=True)
    #observacao -> Problem
    #avaliacao  -> Diagnosis
    referral  = models.ForeignKey()
    comments = models.TextField(blank=True)

class HealthRecord(models.Model):
    comments     = models.TextField(blank=True)
    timestamp    = models.DateTimeField(auto_add_now=True)
    client       = models.ForeignKey(Client)
    professional = models.ForeignKey(Professional)
    student      = models.ForeignKey(Student)
    status       = models.CharField(max_length=2, choices=STATUS)

    def __unicode__(self):
        return u"%s" % self.comments

class ClinicalSynopsis(models.Model):
    identification_of_establishment text		
    service				            text		
    health_professional             multi(text)
    summary				            text		
    Evaluation / Conclusion		    texto		
    date				            models.DateTimeField()
    comments				        models.TextField()

class PsychiatricEvaluation(models.Model):
    responsible psychiatrist		Health Professional		
    previous treatments	previous	Treatments		
    physical exammination		    Physical Examination		
    psychological examination		Psychological Examination		
    additional examinations		    Attached Documents		
    psychiatric diagnosis		    Diagnosis		
    prescription			        Medical Prescription		
    comments				        text 

class PreviousDiagnosis(models.Model):
    professional specialty		Care Professional		
    contact information			Health Professional		
    date                        Approximate Time		
    diagnosis				    texto		
    related_terminology         multi(BVS, DeCS, ICD-10, GestorPsi, DSM IV) - editavel
    comorbidity                 multi(BVS, DeCS, ICD-10, GestorPsi, DSM IV) - editavel    
    file upload				    attachment
    comments				    text

class CaseEvolution(models.Model):
    title				text		
    problem				Problem, Diagnosis
    theme       		multi(BVS, DeCS, ICD-10, GestorPsi, DSM IV) - editavel
    evolution			text		
    Comments			text

class LifeHistory(models.Model):
    life_period			Life Period
    theme               multi(BVS, DeCS, ICD-10, GestorPsi, DSM IV) - editavel
    related_issues		Problem, Diagnosis
    description			text
    comments			text

class EvaluationInstruments(models.Model):
    applied by			Health Professional contact
    version				Application		
    general_results		number
    subscale			number
    upload of files		attachment
    comments			text

class SupervisionRecord(models.Model):
    action				Supervision		
    evaluation			Evaluation of Supervisor 		
    instruction			Instructions of Supervisor		
    comments			text

"""
