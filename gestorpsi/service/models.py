from django.db import models
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import CareProfessional

class ServiceType(models.Model):
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 100 )

PROCEDURE_LIST= ( ( '1', 'SUS'), ( '2', 'CFP'), ( '3', 'GESTORPSI') )    
class Procedure(models.Model):
    id_proc= models.CharField( max_length= 20, blank= True )
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 80, blank= True )
    type= models.CharField( max_length= 1, choices= PROCEDURE_LIST )

class Modality(models.Model):
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 100 )
    
class GenericArea(models.Model):
    services= models.ManyToManyField( ServiceType )
    modalities= models.ManyToManyField( Modality )
    procedures= models.ManyToManyField( Procedure )

class School(GenericArea):
    education_modality= models.CharField( max_length= 80 )

class Organizational(GenericArea):
    hierarchical_level= models.CharField( max_length= 80 )

class Clinic(GenericArea):
    #FAIXA ETARIA
    pass

class AgreementType(models.Model):
    description= models.CharField( max_length= 80 )

class Agreement(models.Model):
    name= models.CharField( max_length= 45 )
    description= models.CharField( max_length= 80 )
    agreement_type= models.ForeignKey( AgreementType )

class ResearchProject(models.Model):
    name= models.CharField( max_length= 45 )
    description= models.CharField( max_length= 80 )

class Service(models.Model):
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 100 )
    keywords= models.CharField( max_length= 100 )
    agreements= models.ManyToManyField( Agreement )
    research_project= models.ForeignKey( ResearchProject )    
    organization = models.ForeignKey(Organization, null=True)    
    
    research_project= models.ForeignKey( ResearchProject )
    organization= models.ForeignKey(Organization, null=True)
    responsibles= models.ForeignKey( CareProfessional )

"""

from gestorpsi.service.models import ResearchProject
research_project= ResearchProject( name= 'a research project', description= 'research project test' )
research_project.save()

from gestorpsi.service.models import AgreementType
agreement_type= AgreementType( description= 'agreement type test' )



"""